from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.http import HttpResponse

from accounts.models import CustomUser
from allauth.account.models import EmailAddress
from .models import Keyword, WhenEmail, ShowingBooks
from .forms import WhenEmailAddForm, EmailEditForm
import re



# Create your views here.


class BooksListView(generic.ListView):
  model = ShowingBooks
  template_name = 'index.html'

  def get_queryset(self):
    books = ShowingBooks.objects.all()
    return books


def book_ajax_search(request):
  search_word = request.GET.get("search_word")
  search_word = re.sub(r'\s', '', search_word)
  books = ShowingBooks.objects.all()
  hit_books = ''

  if search_word:
    for book in books:
      title_match = search_word in book.title
      author_match = search_word in book.author

      if (title_match and not author_match):
        if not (book.title == '<取得失敗>'):
          hit_books += book.title + ',' + book.author + ',' + \
          book.publisher + ',' + \
          book.publishing_date.strftime('%Y年%m月%d日') + ','

      if (author_match and not title_match):
        if not (book.author == '<取得失敗>'):
          hit_books += book.title + ',' + book.author + ',' + \
          book.publisher + ',' + \
          book.publishing_date.strftime('%Y年%m月%d日') + ','

      if (author_match and title_match):
        if not (book.title == book.author == '<取得失敗>'):
          hit_books += book.title + ',' + book.author + ',' + \
          book.publisher + ',' + \
          book.publishing_date.strftime('%Y年%m月%d日') + ','

  hit_books += search_word

  return HttpResponse(hit_books)

class KeywordsListView(LoginRequiredMixin, generic.ListView):
  model = Keyword
  template_name = 'keyword_list.html'

  def get_queryset(self):
    keywords = Keyword.objects.filter(user = self.request.user)
    return keywords


def keyword_ajax_add(request):
  keyword_content = request.POST.get("keyword_content")
  keyword_content = re.sub(r'\s', '', keyword_content)
  add_obj = Keyword()
  if keyword_content:
    add_obj.user = request.user
    add_obj.content = keyword_content
    add_obj.save()
    id_content = str(add_obj.pk) + ',' + keyword_content
  else:
    id_content = ''

  return HttpResponse(id_content)

def keyword_ajax_update(request):
  keyword_id = request.POST.get("keyword_id")
  keyword_content = request.POST.get("keyword_content")
  keyword_content = re.sub(r'\s', '', keyword_content)
  upd_obj = Keyword.objects.get(id = keyword_id)
  if keyword_content:
    upd_obj.content = keyword_content
    upd_obj.save()
  else:
    upd_obj.delete()

  return HttpResponse(keyword_content)

def keyword_ajax_delete(request):
  keyword_id = request.POST.get("keyword_id")
  del_obj = Keyword.objects.get(id = keyword_id)
  del_obj.delete()
  return HttpResponse(keyword_id)

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

class EmailListView(LoginRequiredMixin, generic.ListView):
  model = CustomUser
  template_name = 'email_list.html'

  def get_queryset(self):
    user_for_email = CustomUser.objects.filter(id = self.request.user.id)
    return user_for_email

class EmailEditView(LoginRequiredMixin, generic.UpdateView):
  model = CustomUser
  template_name = 'email_edit.html'
  form_class = EmailEditForm

  def get_success_url(self):
    return reverse_lazy('hello:index')

  def form_valid(self, form):
    try:
        email_address = EmailAddress.objects.get(user = self.request.user)
        email_address.delete()
    except EmailAddress.DoesNotExist:
        pass

    messages.success(self.request, 'メールアドレスを登録しました')
    return super().form_valid(form)

  def form_invalid(self, form):
    messages.error(self.request, 'メールアドレス更新に失敗しました')
    return super().form_invalid(form)
