# Generated by Django 3.0.4 on 2020-04-20 10:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('MedNoti', '0003_auto_20200420_1701'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='NewUserModel',
            new_name='Profile',
        ),
    ]