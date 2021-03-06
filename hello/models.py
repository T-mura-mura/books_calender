from accounts.models import CustomUser
from django.db import models


# Create your models here.

class Keyword(models.Model):
  """登録キーワードモデル"""
  user = models.ForeignKey(CustomUser, verbose_name = 'ユーザー',
  on_delete = models.CASCADE)
  content = models.CharField(max_length = 50, verbose_name = 'キーワード')

  class Meta:
    verbose_name_plural = 'Keyword'


class WhenEmail(models.Model):
  """各ユーザー毎の、何日まえにメールを送るかを登録するモデル"""
  user = models.ForeignKey(CustomUser, unique=True,
  on_delete = models.CASCADE)
  date_email = models.IntegerField(default = 7,
  verbose_name = '何日前に通知しますか？')
  date_reminder = models.IntegerField(blank = True, null = True,
  verbose_name = 'リマインダーを何日前に送りますか？')

  class Meta:
    verbose_name_plural = 'WhenEmail'

class ShowingBooks(models.Model):
  """ページに表示する本をデータベースに貯めるモデル"""
  title = models.CharField(max_length = 50)
  author = models.CharField(max_length = 50)
  publisher = models.CharField(max_length = 50)
  publishing_date = models.DateField(null = True)

  class Meta:
    verbose_name_plural = 'ShowingBooks'

class SendingBooks(models.Model):
  """登録キーワードにヒットした、メールで送る候補の本のモデル"""
  user = models.ForeignKey(CustomUser, on_delete = models.DO_NOTHING)
  title = models.CharField(max_length = 50)
  author = models.CharField(max_length = 50)
  publisher = models.CharField(max_length = 50)
  publishing_date = models.DateField(null = True)
  is_send_1st = models.BooleanField(null = True)
  is_send_2nd = models.BooleanField(null = True)
  is_overlapping = models.BooleanField(default = False)

  class Meta:
    verbose_name_plural = 'SendingBooks'

class EmailLog(models.Model):
  """検索ヒットした本とユーザーへのメール送信履歴モデル"""
  user = models.ForeignKey(CustomUser, on_delete = models.DO_NOTHING)
  title = models.CharField(max_length = 50)
  author = models.CharField(max_length = 50)
  is_email_1st = models.BooleanField(default = False)
  is_email_2nd = models.BooleanField(default = False)
  date_time_1st_email = models.DateTimeField(auto_now_add = True)
  date_time_2nd_email = models.DateTimeField(auto_now = True)

  class Meta:
    verbose_name_plural = 'EmailLog'


