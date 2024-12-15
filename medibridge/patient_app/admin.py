from django.contrib import admin

from .models import *

# Register your models here.

admin.site.register(MedicalReport)
admin.site.register(Appointment)
admin.site.register(AddPrescription)
admin.site.register(Prescription)
admin.site.register(Payment)
admin.site.register(Notification)
