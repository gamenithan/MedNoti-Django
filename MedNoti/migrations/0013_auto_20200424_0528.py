# Generated by Django 3.0.4 on 2020-04-23 22:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MedNoti', '0012_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='image_url',
            field=models.ImageField(null=True, upload_to='static/static_dirs/images/'),
        ),
        migrations.DeleteModel(
            name='Image',
        ),
    ]
