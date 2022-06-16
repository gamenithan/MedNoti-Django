from django import forms
from django.conf import settings
from django.forms import ModelForm
from django.contrib.auth.models import User

from .models import *

class ContactForm(ModelForm):
    class Meta:
        model = Schedule
        fields = ['check1', 'check2', 'check3', 'check4']
        # exclude = ['user']