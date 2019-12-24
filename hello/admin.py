from django.contrib import admin

# Register your models here.

from .models import Keyword, WhenEmail, EmailLog, SendingBooks

admin.site.register(Keyword)
admin.site.register(WhenEmail)
admin.site.register(EmailLog)
admin.site.register(SendingBooks)