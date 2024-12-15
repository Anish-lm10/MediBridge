'''
For sending Notifications
'''

from .models import Notification

def create_notification(patient,message):
     Notification.objects.create(patient=patient,message=message)
