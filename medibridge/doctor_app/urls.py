'''
This urls.py file contains routes of doctor app
'''

from django.urls import path

from .views import *


urlpatterns = [
    path('',doctor_dashboard,name='doctor_dashboard'),
    path('manage_appointment',doctor_appointment,name='doctor_appointment'),
    path('doctor_telemedicine',doctor_telemedicine,name='doctor_telemedicine'),
    path('doctor_add_prescription',doctor_add_prescription,name='doctor_add_prescription'),
    path('doctor_prescription',doctor_prescription,name='doctor_prescription'),
    path('new_meeting',new_meeting,name='new_meeting'),
    path('join_meeting',join_meeting,name='doctor_join_meeting'),
    path('doctor_notification_list',doctor_notification_list,name='doctor_notification_list'),
    path('dclear_all_notification',dclear_all_notification,name='dclear_all_notification'),
    path('mark_as_available/<int:doctor_id>',mark_as_available,name='mark_as_available'),
    path('mark_as_unavailable/<int:doctor_id>',mark_as_unavailable,name='mark_as_unavailable'),
    path('delete_appoint/<int:id>',delete_appoint,name='delete_appoint'),
    path('edit_appoint/<int:id>',edit_appoint,name='edit_appoint'),

]
