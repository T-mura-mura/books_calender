from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.http import HttpResponse

from accounts.models import CustomUser
from allauth.account.models import EmailAddress
from .models import Keyword, WhenEmail, ShowingBooks
from .forms import KeywordAddForm, WhenEmailAddForm, EmailEditForm



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


def keyword_ajax_delete(request):
  keyword_id_pri = request.POST.getlist("keyword_id")
  keyword_id = keyword_id_pri[0]
  del_obj = Keyword.objects.filter(id = keyword_id)
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
