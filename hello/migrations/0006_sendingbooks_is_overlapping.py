# Generated by Django 2.2.7 on 2020-01-01 18:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hello', '0005_showingbooks'),
    ]

    operations = [
        migrations.AddField(
            model_name='sendingbooks',
            name='is_overlapping',
            field=models.BooleanField(default=False),
        ),
    ]
