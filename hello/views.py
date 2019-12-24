from django.shortcuts import render
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
# from django.http import HttpResponseRedirect
from django.core.mail import EmailMessage

from .models import Keyword, WhenEmail, EmailLog, SendingBooks
from accounts.models import CustomUser
from .forms import KeywordAddForm, WhenEmailAddForm

import requests
from bs4 import BeautifulSoup
import re
import datetime


# Create your views here.

class BooksListView(generic.TemplateView):
  template_name = "index.html"

  def send_email_1st(self, name, email, book):
    subject = '発売日が近い本があります'
    body = 'test message.' + name + ' ' + email + ' ' + book['title']
    from_email = 'test@example.com'
    to = [ email ]
    message = EmailMessage(subject = subject, body = body,
    from_email = from_email, to = to)
    message.send()

  def check_if_send_1st(self, user, books):
    today = datetime.date.today()
    when = WhenEmail.objects.filter(user = user)
    days0 = datetime.timedelta(days = 0)
    days1 = datetime.timedelta(days = when.date_email)
    if when.date_reminder:
      days2 = datetime.timedelta(days = when.date_reminder)

    for book in books:
      is_1st_sent = is_2nd_sent = False
      if EmailLog.objects.filter(user = user, title = book['title']):
        log = EmailLog.objects.filter(user = user, title = book['title'])
        is_1st_sent = log.is_email_1st
        is_2nd_sent = log.is_email_2nd

        if (book['publishing_date'] - today >= days0):
          if (is_1st_sent is False and is_2nd_sent is False):
            if days2:
              if (book['publishing_date'] - today <= days1 and
              book['publishing_date'] - today > days2):
                return True
            else:
              if (book['publishing_date'] - today <= days1):
                return True


  def check_if_send_2nd(self, user, books):
    today = datetime.date.today()
    when = WhenEmail.objects.filter(user = user)
    days0 = datetime.timedelta(days = 0)
    if when.date_reminder:
      days2 = datetime.timedelta(days = when.date_reminder)
    
    if days2:
      for book in books:
        is_2nd_sent = False
        if EmailLog.objects.filter(user = user, title = book['title']):
          log = EmailLog.objects.filter(user = user, title = book['title'])
          is_2nd_sent = log.is_email_2nd

        if (book['publishing_date'] - today >= days0):
          if (is_2nd_sent is False):
            if (book['publishing_date'] - today <= days2):
              return True

  def get(self, request, *args, **kwargs):
    html = requests.get('https://gagagabunko.jp/newrelease/index.html')
    soup = BeautifulSoup(html.content, "html.parser")
    
    titles = soup.select("h3.blueBold")
    authors_pri = soup.select("span.textsize14")
    authors = authors_pri[0::2]
    for i in range(len(titles)):
      titles[i] = titles[i].string
      # titleがうまくとれなくてNoneになったときの処置----
      if titles[i] == None:
        titles[i] = '#'
      # -------------------------------------------
    for i in range(len(authors)):
      authors[i] = authors[i].string
      authors[i] = re.findall(r'著：.*\u3000', authors[i])
      authors[i] = authors[i][0][2:-1]
    authors = authors[0:len(titles)]
    publisher = 'ガガガ文庫'
    publishing_date = datetime.date(2019, 11, 19)

    books = []
    users = CustomUser.objects.all()

    for i in range(len(titles)):
      book = {
        'title':titles[i],
        'author':authors[i],
        'publisher':publisher,
        'publishing_date':publishing_date.strftime('%Y/%m/%d')
      }
      books.append(book)

      for user in users:
        keywords = Keyword.objects.filter(user = user)
        if keywords:
          for keyword in keywords:
            if (keyword.content in book['title'] or
            keyword.content in book['author']):
              register = SendingBooks()
              register.user = user
              register.title = book['title']
              register.author = book['author']
              register.publisher = book['publisher']
              register.publishing_date = datetime.datetime.strptime(book['publishing_date'], '%Y/%m/%d')
              register.save()
              
    
    for user in users:
      registers = SendingBooks.objects.filter(user = user)
      if registers:
        self.check_if_send_1st(user, registers)
        self.check_if_send_2nd(user, registers)
        self.send_email_1st(keyword.user.username, keyword.user.email, book)

    context = super(BooksListView, self).get_context_data(**kwargs)
    context['books'] = books
    return render(self.request, self.template_name, context)

class KeywordsListView(LoginRequiredMixin, generic.ListView):
  model = Keyword
  template_name = 'keyword_list.html'

  def get_queryset(self):
    keywords = Keyword.objects.filter(user = self.request.user)
    return keywords


class KeywordAddView(LoginRequiredMixin, generic.CreateView):
  model = Keyword
  template_name = 'keyword_add.html'
  form_class = KeywordAddForm

  def get_success_url(self):
    return reverse_lazy('hello:keyword_list',
    kwargs={'pk': self.request.user.pk })

  def form_valid(self, form):
    keyword = form.save(commit = False)
    keyword.user = self.request.user
    keyword.save()
    messages.success(self.request, 'キーワードを登録しました')
    return super().form_valid(form)

  def form_invalid(self, form):
    messages.error(self.request, 'キーワード登録に失敗しました')
    return super().form_invalid(form)

class KeywordEditView(LoginRequiredMixin, generic.UpdateView):
  model = Keyword
  template_name = 'keyword_edit.html'
  form_class = KeywordAddForm

  def get_success_url(self):
    return reverse_lazy('hello:keyword_list',
    kwargs={'pk': self.request.user.pk })

  def form_valid(self, form):
    messages.success(self.request, 'キーワードを登録しました')
    return super().form_valid(form)

  def form_invalid(self, form):
    messages.error(self.request, 'キーワード登録に失敗しました')
    return super().form_invalid(form)

class KeywordDeleteView(LoginRequiredMixin, generic.DeleteView):
  model = Keyword
  template_name = 'keyword_delete.html'
  
  def delete(self, request, *args, **kwargs):
    messages.success(self.request, "キーワードを削除しました")
    return super().delete(request, *args, **kwargs)

  def get_success_url(self):
    return reverse_lazy('hello:keyword_list',
    kwargs={'pk': self.request.user.pk })

# うまく動かないdeleteメソッド。できたらdeleteする時に確認なしで消したい。
# def keyword_delete(self, id):
#   Keyword.objects.filter(id = self.request.object.id).delete()
#   redirect_url = reverse_lazy('hello:keyword_list',
#     kwargs={'pk': self.request.user.id })
#   return HttpResponseRedirect(redirect_url)

class SendDateView(LoginRequiredMixin, generic.ListView):
  model = WhenEmail
  template_name = 'send_date.html'

  def get_queryset(self):
    when = WhenEmail.objects.filter(user = self.request.user)
    return when

class SendSetView(LoginRequiredMixin, generic.CreateView):
  model = WhenEmail
  template_name = 'send_set.html'
  form_class = WhenEmailAddForm

  def get_success_url(self):
    return reverse_lazy('hello:send_date',
    kwargs={'pk': self.request.user.pk })

  def form_valid(self, form):
    when = form.save(commit = False)
    when.user = self.request.user
    when.save()
    messages.success(self.request, 'メール通知日を登録しました')
    return super().form_valid(form)

  def form_invalid(self, form):
    messages.error(self.request, 'メール通知日設定に失敗しました')
    return super().form_invalid(form)

class SendChangeView(LoginRequiredMixin, generic.UpdateView):
  model = WhenEmail
  template_name = 'send_change.html'
  form_class = WhenEmailAddForm

  def get_success_url(self):
    return reverse_lazy('hello:send_date',
    kwargs={'pk': self.request.user.pk })

  def form_valid(self, form):
    messages.success(self.request, 'メール通知日を変更しました')
    return super().form_valid(form)

  def form_invalid(self, form):
    messages.error(self.request, 'メール通知日変更に失敗しました')
    return super().form_invalid(form)

class SendDeleteView(LoginRequiredMixin, generic.DeleteView):
  model = WhenEmail
  template_name = 'send_delete.html'
  
  def delete(self, request, *args, **kwargs):
    messages.success(self.request, "メール通知日設定を消去しました")
    return super().delete(request, *args, **kwargs)

  def get_success_url(self):
    return reverse_lazy('hello:send_date',
    kwargs={'pk': self.request.user.pk })