from django.db import models

from mainpage.models import *

# Create your models here.
class DoctorNotification(models.Model):
    doctor=models.ForeignKey(Doctor,on_delete=models.CASCADE)
    message=models.TextField()
    is_read=models.BooleanField(default=False)
    timestamp=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.doctor}"