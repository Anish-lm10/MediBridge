"""
This urls.py file contains all the routes of mainpage

"""
from django.urls import path
from django.contrib.auth import views as auth_views

from .views import *
from patient_app.views import *

urlpatterns = [
    path('',home,name='home'),
    path('home',home,name='home'),
    path('about',about,name='about'),
    path('contact',contact,name='contact'),
    path('service',service,name='service'),
    path('doctor_log_in',dlog_in,name='doctor_log_in'),
    path('patient_log_in',plog_in,name='patient_log_in'),
    path('register_doctor',register_doctor,name='register_doctor'),
    path('register_patient',register_patient,name='register_patient'),
    path('log_out',log_out,name='log_out'),
    path('dashboard',dashboard,name='dashboard'),
    path('payment/success/',payment_success, name='payment_success'),
    path('payment/failure/', payment_failure, name='payment_failure'),
    path("change_password/", change_password, name="change_password"),
    path(
        "password_reset/",
        auth_views.PasswordResetView.as_view(template_name="auth/change_password.html"),
        name="password_reset",
    ),
    path(
        "password_reset_done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="auth/password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "password_reset_confirm/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="auth/password_reset_confirm.html"
        ),
        name="password_reset_confirm",
    ),
    path(
        "password_reset_complete/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="auth/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
]
