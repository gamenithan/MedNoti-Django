from django.db import models
from django.contrib.auth.models import User
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    allergy = models.CharField(max_length=255, null=True)
    disease = models.CharField(max_length=255, null=True)
    sex = models.CharField(max_length=20, null=True)
    age = models.IntegerField(null=True)
    date_of_birth = models.DateField(null=True)
    image_url = models.ImageField(upload_to='static/static_dirs/images/', null=True)

class Neighbor(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255, null=True)
    allergy = models.CharField(max_length=255, null=True)
    disease = models.CharField(max_length=255, null=True)
    sex = models.CharField(max_length=20)
    age = models.IntegerField()
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    image_url = models.ImageField(upload_to='static/static_dirs/images/', null=True)

class Medicine(models.Model):
    name = models.CharField(max_length=255)
    med_type = models.CharField(max_length=255)
    cate = models.CharField(max_length=255)
    take_start = models.DateField()
    unit_eat = models.IntegerField()
    freq1 = models.CharField(max_length=255, null=True)
    freq2 = models.CharField(max_length=255, null=True)
    freq3 = models.CharField(max_length=255, null=True)
    freq4 = models.CharField(max_length=255, null=True)
    when = models.CharField(max_length=255)
    hmt = models.IntegerField()
    who = models.CharField(max_length=255, null=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)


class Calendar(models.Model):
    activity = models.CharField(max_length=255)
    date = models.DateField(null=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

# class Performance(models.Model):
#     date = models.DateField(null=True)
#     result = models.CharField(max_length=255, null=True)
#     forweek = models.CharField(max_length=255, null=True)
#     user_id = models.ForeignKey(User, on_delete=models.CASCADE)

# class Detail(models.Model):
#     missing = models.CharField(max_length=255)
#     medicine_id = models.ForeignKey(Medicine, on_delete=models.CASCADE)
#     performance_id = models.ForeignKey(Performance, on_delete=models.CASCADE)

class Schedule(models.Model):
    date = models.DateField()
    check1 = models.BooleanField(default=False)
    check2 = models.BooleanField(default=False)
    check3 = models.BooleanField(default=False)
    check4 = models.BooleanField(default=False)
    count = models.IntegerField()
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    medicine_id = models.ForeignKey(Medicine, on_delete=models.CASCADE)
