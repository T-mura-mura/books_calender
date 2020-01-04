from django.core.management.base import BaseCommand
from accounts.models import CustomUser
from hello.models import Keyword, WhenEmail, EmailLog, SendingBooks, \
  ShowingBooks
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

import requests
from bs4 import BeautifulSoup
import re
import datetime


class Command(BaseCommand):
  help = "１日１回、本の情報をスクレイピングして、データベースを更新する"

  def send_email_1st(self, user, books):
    subject = "発売日が近い本があります"
    book_list = ''
    for book in books:
      book_list += 'タイトル : ' + book.title + '   ' \
      + '著者 : ' + book.author + '   ' + '出版社 : ' + book.publisher \
      + '   ' + '発売日 : ' + book.publishing_date.strftime('%Y/%m/%d') + '\n\n'

    body = user.username + '様\n\n' + '次の本の発売日が近づいています。\n\n' + book_list
    from_email = "admin@books-calender.com"
    to_email = user.email
    mail = Mail(from_email, to_email, subject, body)
    response = None
    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(mail)
    except Exception as e:
        print(str(e))

    if response:
      for book in books:
        log = EmailLog()
        log.user = user
        log.title = book.title
        log.author = book.author
        log.is_email_1st = True
        log.save()

  def send_email_2nd(self, user, books):
    subject = 'まもなく発売日となる本があります'
    book_list = ''
    for book in books:
      book_list += 'タイトル : ' + book.title + '   ' \
      + '著者 : ' + book.author + '   ' + '出版社 : ' + book.publisher \
      + '   ' + '発売日 : ' + book.publishing_date.strftime('%Y/%m/%d') + '\n\n'
    body = user.username + '様\n\n' + '次の本はもうすぐ発売日です。\n\n' + book_list
    from_email = 'admin@books-calender.com'
    to_email = user.email
    mail = Mail(from_email, to_email, subject, body)
    response = None
    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(mail)
    except Exception as e:
        print(str(e))

    if response:
      for book in books:
        existing_log = EmailLog.objects.filter(user = user, \
          title = book.title, author = book.author)
        if existing_log:
          existing_log[0].is_email_2nd = True
          existing_log[0].save()
        else:
          log = EmailLog()
          log.user = user
          log.title = book.title
          log.author = book.author
          log.is_email_2nd = True
          log.save()

  def check_if_send_1st(self, user, books):
    today = datetime.date.today()
    when = WhenEmail.objects.filter(user = user)
    days0 = datetime.timedelta(days = 0)
    days1 = datetime.timedelta(days = when[0].date_email)
    days2 = None
    if when[0].date_reminder != None:
      days2 = datetime.timedelta(days = when[0].date_reminder)

    for book in books:
      is_1st_sent = is_2nd_sent = False
      log = EmailLog.objects.filter(user = user, title = book.title, \
        author = book.author)
      if log:
        is_1st_sent = log[0].is_email_1st
        is_2nd_sent = log[0].is_email_2nd

      if (book.publishing_date - today >= days0):
        if (is_1st_sent is False and is_2nd_sent is False):
          if days2 != None:
            if (book.publishing_date - today <= days1 and \
            book.publishing_date - today > days2):
              book.is_send_1st = True
              book.save()
          else:
            if (book.publishing_date - today <= days1):
              book.is_send_1st = True
              book.save()


  def check_if_send_2nd(self, user, books):
    today = datetime.date.today()
    when = WhenEmail.objects.filter(user = user)
    days0 = datetime.timedelta(days = 0)
    days2 = None
    if when[0].date_reminder != None:
      days2 = datetime.timedelta(days = when[0].date_reminder)
    
    if days2 != None:
      for book in books:
        is_2nd_sent = False
        log = EmailLog.objects.filter(user = user, title = book.title, \
        author = book.author)
        if log:
          is_2nd_sent = log[0].is_email_2nd

        if (book.publishing_date - today >= days0):
          if (is_2nd_sent is False):
            if (book.publishing_date - today <= days2):
              book.is_send_2nd = True
              book.save()

  def check_unique(self, books):
    for i in range(len(books)-1):
      for j in range(i+1, len(books)):
        if books[i].title == books[j].title and \
          books[i].author == books[j].author and \
          books[i].publisher == books[j].publisher and \
          books[i].publishing_date == books[j].publishing_date:

          books[j].is_overlapping = True

  def scraping_gagaga(self):
    html = requests.get('https://gagagabunko.jp/newrelease/index.html')
    soup = BeautifulSoup(html.content, "html.parser")
    
    titles = soup.select("#contBg2 > div > h3")
    authors = soup.select("#contBg2 > div > p")

    for i in range(len(titles)):
      titles[i] = titles[i].string
      # titleがうまくとれなくてNoneになったときの処置----
      if titles[i] == None:
        titles[i] = '<取得失敗> 公式ホームページをご覧ください'
      # -------------------------------------------
    for i in range(len(authors)):
      authors[i] = authors[i].string
      authors[i] = re.findall(r'著：.*\u3000', authors[i])
      authors[i] = authors[i][0][2:-1]
    authors = authors[0:len(titles)]
    publisher = 'ガガガ文庫'
    pub_day = soup.select("#contBg2 > div.heading > \
    span.headingReleasedate")[0].string
    pub_day = re.findall(r'\d月\d+日', pub_day)
    pub_day_month = re.sub(r'月\d+日', '', pub_day[0])
    pub_day_proc = re.sub(r'\d月', '', pub_day[0])
    pub_day_day = re.sub(r'日', '', pub_day_proc)
    pub_day_month = int(pub_day_month)
    pub_day_day = int(pub_day_day)
    publishing_date = datetime.date(2020, pub_day_month, pub_day_day)

    for i in range(len(titles)):
      if not ShowingBooks.objects.filter(title = titles[i], \
        author = authors[i], publisher = publisher, \
        publishing_date = publishing_date):
        
        book = ShowingBooks()
        book.title = titles[i]
        book.author = authors[i]
        book.publisher = publisher
        book.publishing_date = publishing_date
        book.save()

  def scraping_overlap(self):
    html = requests.get('https://over-lap.co.jp/lnv/')
    soup = BeautifulSoup(html.content, "html.parser")
    titles = soup.select("#lightnovel_next h2 > a")
    authors = soup.select("#lightnovel_next span:nth-child(1) > strong")
    pub_day = soup.select("#lightnovel_next small.info > span")

    for i in range(len(titles)):
      titles[i] = titles[i].string
      titles[i] = re.sub(r'\r|\n|\s{2,}', '', titles[i])

    for i in range(len(authors)):
      authors[i] = authors[i].string

    pub_day_year = [None] * len(pub_day)
    pub_day_month = [None] * len(pub_day)
    pub_day_day = [None] * len(pub_day)
    publishing_date = [None] * len(pub_day)
    for i in range(len(pub_day)):
      pub_day[i] = pub_day[i].string
      pub_day_year[i] = re.findall(r'\d+年', pub_day[i])
      pub_day_year[i] = re.sub(r'年', '', pub_day_year[i][0])
      pub_day_month[i] = re.findall(r'\d+月', pub_day[i])
      pub_day_month[i] = re.sub(r'月', '', pub_day_month[i][0])
      pub_day_day[i] = re.findall(r'\d+日', pub_day[i])
      pub_day_day[i] = re.sub(r'日', '', pub_day_day[i][0])

      pub_day_year[i] = int(pub_day_year[i])
      pub_day_month[i] = int(pub_day_month[i])
      pub_day_day[i] = int(pub_day_day[i])

      publishing_date[i] = datetime.date(pub_day_year[i], pub_day_month[i], \
        pub_day_day[i])

    publisher = 'オーバーラップ文庫'

    for i in range(len(titles)):
      if not ShowingBooks.objects.filter(title = titles[i], \
        author = authors[i], publisher = publisher, \
        publishing_date = publishing_date[i]):

        book = ShowingBooks()
        book.title = titles[i]
        book.author = authors[i]
        book.publisher = publisher
        book.publishing_date = publishing_date[i]
        book.save()


  def handle(self, *args, **options):

    showing_books = ShowingBooks.objects.all()
    today = datetime.date.today()
    days0 = datetime.timedelta(days = 0)
    for book in showing_books:
      if book.publishing_date - today < days0:
        book.delete()

    self.scraping_gagaga()
    self.scraping_overlap()

    users = CustomUser.objects.all()
    books = ShowingBooks.objects.all()
    for user in users:
      keywords = Keyword.objects.filter(user = user)
      if keywords:
        for keyword in keywords:
          for book in books:
            if (keyword.content in book.title or \
            keyword.content in book.author):
              register = SendingBooks()
              register.user = user
              register.title = book.title
              register.author = book.author
              register.publisher = book.publisher
              register.publishing_date = book.publishing_date
              register.save()
              
    for user in users:
      if WhenEmail.objects.filter(user = user):
        registers = SendingBooks.objects.filter(user = user)
        if registers:
          self.check_unique(registers)
          self.check_if_send_1st(user, registers)
          self.check_if_send_2nd(user, registers)
          books_1st = registers.filter(is_send_1st = True, \
            is_overlapping = False)
          books_2nd = registers.filter(is_send_2nd = True, \
            is_overlapping = False)
          if books_1st:
            self.send_email_1st(user, books_1st)
          if books_2nd:
            self.send_email_2nd(user, books_2nd)

    registers = SendingBooks.objects.all()
    registers.delete()
