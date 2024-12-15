'''
For sending Notifications
'''

from patient_app.models import Notification
from .models import DoctorNotification

def create_notification(patient,message):
     Notification.objects.create(patient=patient,message=message)

def doctor_create_notification(doctor,message):
     DoctorNotification.objects.create(doctor=doctor,message=message)
