# Generated by Django 3.2.9 on 2021-12-25 17:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Register', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='email',
        ),
    ]
