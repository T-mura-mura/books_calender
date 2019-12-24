import requests
from bs4 import BeautifulSoup
import re
import datetime

html = requests.get('https://gagagabunko.jp/newrelease/index.html')
soup = BeautifulSoup(html.content, "html.parser")
titles = soup.select("h3.blueBold")
authors_pri = soup.select("span.textsize14")
authors = authors_pri[0::2]
for i in range(len(titles)):
  titles[i] = titles[i].string
for i in range(len(authors)):
  authors[i] = authors[i].string
  authors[i] = re.findall(r'著：.*\u3000', authors[i])
  authors[i] = authors[i][0][2:-1]
authors = authors[0:len(titles)]
publisher = 'ガガガ文庫'
publishing_date = '2019年11月19日'

books = []
for i in range(len(titles)):
  book = {
    'title':titles[i],
    'author':authors[i],
    'publisher':publisher,
    'publishing_date':publishing_date,
    }
  books.append(book)
  print(book['title'])
# print(books)
