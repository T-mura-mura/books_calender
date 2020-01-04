from django import forms
from .models import WhenEmail
from accounts.models import CustomUser


class WhenEmailAddForm(forms.ModelForm):
  class Meta:
    model = WhenEmail
    fields = ('date_email', 'date_reminder',)
    labels = { 'date_email': '１通目のメール', 'date_reminder': 'リマインダー' }

  def clean(self):
    cleaned_data = super().clean()
    days_1st = cleaned_data.get('date_email')
    days_2nd = cleaned_data.get('date_reminder')

    if days_1st < 0:
      raise forms.ValidationError('0以上の整数を入力してください')

    if days_2nd != None and days_2nd < 0:
      raise forms.ValidationError('0以上の整数を入力してください。あるいは空欄 \
        のままにすると、リマインダーを送らない設定になります')

    if days_2nd != None and days_1st <= days_2nd:
      raise forms.ValidationError('リマインダーは１回目のお知らせメールより \
        後に届くよう、小さな数字を選んでください')

class EmailEditForm(forms.ModelForm):
  class Meta:
    model = CustomUser
    fields = ('email',)
    labels = { 'email': '新しいメールアドレス' }

  def clean_email(self):
    email = self.cleaned_data['email']
    is_email_another = CustomUser.objects.filter(email = email)
    if not email:
      raise forms.ValidationError('メールアドレスを入力してください')
    if is_email_another:
      raise forms.ValidationError('他のユーザーが既に使用しているメールアドレスです')
    return email
