# Generated by Django 3.0.4 on 2020-04-24 18:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MedNoti', '0022_remove_medicine_neighbor_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='medicine',
            name='who',
            field=models.CharField(max_length=255, null=True),
        ),
    ]