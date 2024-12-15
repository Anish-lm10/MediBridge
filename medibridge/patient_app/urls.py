'''
This urls.py file contains routes of patient app
'''

from django.urls import path

from .views import *

urlpatterns = [
    path('',patient_dashboard,name='patient_dashboard'),
    path('appointment',patient_appointment,name='patient_appointment'),
    path('payment/success/',payment_success, name='payment_success'),
    path('payment/failure/', payment_failure, name='payment_failure'),
    path('medical_report',patient_medical,name='medical_report'),
    path('prescription',patient_pres,name='patient_pres'),
    path('telemedicine',patient_telemedicine,name='telemedicine'),
    path('new_meeting',new_meeting,name='new_meeting'),
    path('join_meeting',join_meeting,name='patient_join_meeting'),
    path('payment',patient_payment,name='payment'),
    path('notification_list',notification_list,name='notification_list'),
    path('delete_medical/<int:id>',delete_medical,name='delete_medical'),
    path('edit_medical/<int:id>',edit_medical,name='edit_medical'),
    path('delete_pres/<int:id>',delete_pres,name='delete_pres'),
    path('edit_pres/<int:id>',edit_pres,name='edit_pres'),
    path('delete_all_transaction',delete_all_transaction,name='delete_all_transaction'),
    path('clear_add_pres',clear_add_pres,name='clear_add_pres'),
    path('clear_all_notification',clear_all_notification,name='clear_all_notification'),
    path('doctors_lists',doctors_lists,name='doctors_lists'),
    path('view_doctors_lists/<int:id>',view_doctors_lists,name='view_doctors_lists'),
]
