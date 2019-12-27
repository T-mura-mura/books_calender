from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
# from django.http import HttpResponseRedirect

from .models import Keyword, WhenEmail, ShowingBooks
from .forms import KeywordAddForm, WhenEmailAddForm



# Create your views here.


class BooksListView(generic.ListView):
  model = ShowingBooks
  template_name = 'index.html'

  def get_queryset(self):
    books = ShowingBooks.objects.all()
    return books

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