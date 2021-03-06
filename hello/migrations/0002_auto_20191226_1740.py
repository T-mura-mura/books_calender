# Generated by Django 2.2.7 on 2019-12-26 17:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hello', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='emaillog',
            name='is_email_1st',
            field=models.BooleanField(null=True),
        ),
        migrations.AddField(
            model_name='emaillog',
            name='is_email_2nd',
            field=models.BooleanField(null=True),
        ),
        migrations.AddField(
            model_name='sendingbooks',
            name='is_send_1st',
            field=models.BooleanField(null=True),
        ),
        migrations.AddField(
            model_name='sendingbooks',
            name='is_send_2nd',
            field=models.BooleanField(null=True),
        ),
        migrations.AddField(
            model_name='sendingbooks',
            name='publishing_date',
            field=models.DateField(null=True),
        ),
    ]
