# Generated by Django 2.2.7 on 2019-12-26 21:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hello', '0002_auto_20191226_1740'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='emaillog',
            name='keyword',
        ),
    ]
