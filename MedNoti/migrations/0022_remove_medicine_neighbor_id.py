# Generated by Django 3.0.4 on 2020-04-24 18:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('MedNoti', '0021_auto_20200425_0110'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='medicine',
            name='neighbor_id',
        ),
    ]
