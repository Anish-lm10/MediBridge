'''
this is models section of mainpage without login
->for generationg quotes
->doctor models
->patient models
'''

from django.db import models
from django.contrib.auth.models import User
from datetime import datetime


# Create your models here.

class Quote(models.Model):
    quote=models.TextField()
    author=models.CharField(max_length=255)

    def __str__(self):
        return self.author


class Doctor(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name='doctor_profile',default=None)
    full_name=models.CharField(max_length=255,null=True)
    email=models.EmailField(unique=True,default=None)
    specialization = models.CharField(max_length=100, help_text="Doctor's area of specialization",default=None)
    certificate = models.FileField(upload_to='doctor_certificates/', help_text="Upload your medical certificate",default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    verified=models.BooleanField(default=False)
    is_available=models.BooleanField(default=False)

    def __str__(self):
        return f"Dr. {self.full_name} - {self.specialization}"

class Patient(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name='patient_profile',default=None)
    full_name=models.CharField(max_length=255,null=True)
    email=models.EmailField(unique=True,default=None)
    phone_number=models.CharField(max_length=20,default=None)

    def __str__(self):
        return f"Patient: {self.full_name}"