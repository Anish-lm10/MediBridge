"""
This views.py file contains all the backends of mainpage
->home
->about us
->contact
->features
->login
->register

"""

import re

from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.forms import PasswordChangeForm

from .models import *
from patient_app.models import *

# Create your views here.


def home(request):
    quote=Quote.objects.order_by('?').first()
    d_count=Doctor.objects.all().count()
    p_count=Patient.objects.all().count()
    a_count=Appointment.objects.all().count()
    return render(request,'nav_elements/home.html',{'quote':quote,'d_count':d_count,'p_count':p_count,'a_count':a_count})

def dashboard(request):
    user=request.user
    if user.is_authenticated:
        try:
            doctor_profile = Doctor.objects.get(user=user)
            return redirect('doctor_dashboard')
        except Doctor.DoesNotExist:
            try:
                patient_profile = Patient.objects.get(user=user)
                return redirect('patient_dashboard') 
            except Patient.DoesNotExist:
                return redirect('home')
    else:
        return redirect('doctor_log_in')  

def about(request):
    return render(request,'nav_elements/about.html')

def contact(request):
    if request.method == 'POST':
        name=request.POST.get('name')
        email=request.POST.get('email')
        message=request.POST.get('message')


        if name and email and message:  # Validate fields are not empty
            try:
                subject = f"Contact Form Submission from {name}"
                full_message = f"Message from {name} ({email}):\n\n{message}"
                from_email = email  # Replace with your email
                recipient_list = ['anishnepal000@gmail.com']  # Replace with the recipient's email

                send_mail(subject, full_message, from_email, recipient_list)
                messages.success(request, "Your message has been sent successfully!")
            except Exception as e:
                messages.error(request, f"Failed to send your message: {e}")
        else:
            messages.error(request, "Please fill in all the fields.")

    return render(request,'nav_elements/contact.html',)

def service(request):
    return render(request,'nav_elements/services.html')

def dlog_in(request):
    if request.method=='POST':
        email=request.POST.get('demail')
        password=request.POST.get('dpassword')

        if not Doctor.objects.filter(email=email).exists():
            messages.error(request,"Email is not Registered")
            return redirect('doctor_log_in')
        
        user=authenticate(request,username=email,password=password)
        if user is not None:
            login(request,user)
            messages.success(request, "You have successfully logged in.")
            return redirect('/doctor/') 
        else:
            # Authentication failed
            messages.error(request, "Invalid email or password.")
            return redirect('doctor_log_in')  # Redirect back to the login page

    return render(request,'auth/dlogin.html')

def plog_in(request):
    if request.method=='POST':
        email=request.POST.get('pemail')
        password=request.POST.get('ppassword')

        if not Patient.objects.filter(email=email).exists():
            messages.error(request,"Email is not Registered")
            return redirect('patient_log_in')
        
        user=authenticate(request,username=email,password=password)
        if user is not None:
            login(request,user)
            messages.success(request, "You have successfully logged in.")
            return redirect('/patient/') 
        else:
            # Authentication failed
            messages.error(request, "Invalid email or password.")
            return redirect('patient_log_in')  # Redirect back to the login page
    return render(request,'auth/plogin.html')

def register_doctor(request):
    if request.method == 'POST' and request.FILES:
        # Retrieve form data
        full_name = request.POST.get('doctor-name')
        email = request.POST.get('demail')
        password = request.POST.get('dpassword')
        cpassword = request.POST.get('dcpassword')
        specialization = request.POST.get('specialization')
        certificate = request.FILES.get('certificate')

        # Validate password match
        if password != cpassword:
            messages.error(request, "Passwords do not match.")
            return redirect('register_doctor')

        # Validate email format
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_regex, email):
            messages.error(request, "Invalid email address.")
            return redirect('register_doctor')

        # Check if email already exists
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return redirect('register_doctor')

        # Validate password complexity
        password_regex = r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)[A-Za-z\d@$!%*?&]{8,}$'
        if not re.match(password_regex, password):
            messages.error(request, "Password must be at least 8 characters long, contain an uppercase letter, a lowercase letter, and a number.")
            return redirect('register_doctor')

        # Create user and doctor profile
        try:
            user = User.objects.create_user(username=email, email=email, password=password)
            doctor = Doctor.objects.create(
                user=user,
                full_name=full_name,
                email=email,
                specialization=specialization,
                certificate=certificate,
                verified=False,  # Initial verification status
            )
            messages.success(request, "Registration successful. Your profile is pending verification.")
            return redirect('home')  # Redirect to the desired page after registration
        except Exception as e:
            messages.error(request, f"An error occurred during registration: {str(e)}")
            return redirect('register_doctor')

    return render(request, 'auth/dregister.html')

def register_patient(request):
    if request.method == 'POST':
        full_name = request.POST.get('patient-name')
        email = request.POST.get('pemail')
        password = request.POST.get('password')
        cpassword = request.POST.get('cpassword')
        phone_number=request.POST.get('number')

        if password == cpassword:
            #email
            email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if not email or not re.match(email_regex, email):
                messages.error(request, "Please enter a valid email address.")
                return redirect('register_patient')
                
            if User.objects.filter(email=email).exists():
                messages.error(request, "Email already exists.")
                return redirect('register_patient')
                
            password_regex = r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)[A-Za-z\d@$!%*?&]{8,}$'
            if not password or not re.match(password_regex, password):
                messages.error(request, "Password must be at least 8 characters long, include at least one uppercase letter, one lowercase letter, and one number.")
                return redirect('register_patient')   
            
            phone_regex = r'^(97|98)\d{8}$'
            if not phone_number or not re.match(phone_regex, phone_number):
                messages.error(request, "Please enter a valid Nepali phone number starting with 97 or 98.")
                return redirect('register_patient')
            
            try:
                user=User.objects.create_user(username=email,email=email,password=password)
                patient = Patient.objects.create(
                    user=user,
                    full_name=full_name,
                    email=email,
                    phone_number=phone_number
                )
                patient.save()
                messages.success(request, "Profile created sucessfully.")
                return redirect('home')  # Redirect to login or a verification pag
            except Exception as e:
                messages.error(request,f"An error occured {e}")
                return redirect('register_patient')
        else:
            messages.error(request,"Password donot match")
            return redirect('register_patient')
            
    return render(request,'auth/pregister.html')

def log_out(request):
    logout(request)
    return redirect('home')

def change_password(request):
    form = PasswordChangeForm(user=request.user)
    if request.method == "POST":
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect("log_in")
    return render(request, "auth/change_password.html", {"form": form})