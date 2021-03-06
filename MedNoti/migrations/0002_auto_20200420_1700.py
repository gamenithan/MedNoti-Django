# Generated by Django 3.0.4 on 2020-04-20 10:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MedNoti', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='NewUserModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('allergy', models.CharField(max_length=255, null=True)),
                ('disease', models.CharField(max_length=255, null=True)),
                ('sex', models.CharField(max_length=20)),
                ('age', models.IntegerField()),
                ('date_of_birth', models.DateField(null=True)),
            ],
        ),
        migrations.AlterField(
            model_name='calendar',
            name='date',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='calendar',
            name='end_time',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='calendar',
            name='start_time',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='neighbor',
            name='age',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='neighbor',
            name='allergy',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='neighbor',
            name='disease',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='performance',
            name='date',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='schedule',
            name='count',
            field=models.IntegerField(),
        ),
    ]
