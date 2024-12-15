'''
Model for patient
->appointment
->medical report
->prescription
->Payment
'''

from django.db import models
from django.contrib.auth.models import User

from mainpage.models import *

# Create your models here.


class Appointment(models.Model):
    patient=models.ForeignKey(User,on_delete=models.CASCADE,related_name='appointments')
    d_name=models.ForeignKey(User,on_delete=models.CASCADE,related_name='d_appointments',null=True)
    doctor_name=models.CharField(max_length=100)
    date=models.DateField()
    time=models.TimeField()
    description=models.TextField(null=True)
    status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('Completed', 'Completed')],default='Pending')

class MedicalReport(models.Model):
    patient=models.ForeignKey(User,on_delete=models.CASCADE,related_name='medical_reports')
    date=models.DateField()
    diagnosis=models.CharField(max_length=100)
    treatment=models.CharField(max_length=100)

class Prescription(models.Model):
    patient=models.ForeignKey(User,on_delete=models.CASCADE,related_name='prescription')
    medication_name=models.CharField(max_length=100)
    dosage=models.CharField(max_length=100)
    instruction=models.TextField()
    date=models.DateField()

class AddPrescription(models.Model):
    patients=models.ForeignKey(Patient,on_delete=models.CASCADE,related_name='prescription')
    doctors=models.ForeignKey(Doctor,on_delete=models.CASCADE,related_name='prescription')
    medication_names=models.CharField(max_length=100)
    dosages=models.CharField(max_length=100)
    instructions=models.TextField()
    dates=models.DateField()

class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments')
    appointment = models.ForeignKey('Appointment', on_delete=models.CASCADE, null=True, blank=True)
    transaction_id = models.CharField(max_length=100, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.CharField(max_length=20, choices=[('Success', 'Success'), ('Failure', 'Failure')])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.transaction_id} - {self.payment_status}"
    
class Notification(models.Model):
    patient=models.ForeignKey(Patient,on_delete=models.CASCADE)
    message=models.TextField()
    is_read=models.BooleanField(default=False)
    timestamp=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.patient}"

