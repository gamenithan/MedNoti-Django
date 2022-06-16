# Generated by Django 3.0.4 on 2020-04-23 18:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MedNoti', '0008_profile'),
    ]

    operations = [
        migrations.RenameField(
            model_name='medicine',
            old_name='desc',
            new_name='cate',
        ),
        migrations.RenameField(
            model_name='medicine',
            old_name='exp',
            new_name='freq',
        ),
        migrations.RemoveField(
            model_name='medicine',
            name='date',
        ),
        migrations.AddField(
            model_name='medicine',
            name='when',
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
    ]
