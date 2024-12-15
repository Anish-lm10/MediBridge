'''
This urls.py file contains logic of doctor app
'''

from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from mainpage.models import *
from patient_app.models import *
from .utils import create_notification
from .models import *


# Create your views here.

@login_required(login_url='/home')
def doctor_dashboard(request):
    doctor = get_object_or_404(Doctor, user=request.user)
    notification_count=DoctorNotification.objects.filter(doctor=doctor).count()
    return render(request,'doctor_nav/d_dashboard.html',{'doctors':doctor,'notification_count':notification_count})

def doctor_appointment(request):
    appoint=Appointment.objects.filter(d_name=request.user)
    return render(request,'doctor_nav/manage_appointment.html',{'appoint':appoint})

def doctor_telemedicine(request):
    return render(request,'doctor_nav/dtelemedicine.html')

def new_meeting(request):
    return render(request,'videos/videocall.html',{'name':request.user})

def join_meeting(request):
    if request.method == 'POST':
        roomID=request.POST.get('roomID')
        return redirect('/new_meeting?roomID='+roomID)
    return render(request,'videos/join.html')

def doctor_add_prescription(request):
    if request.method == 'POST':
        medication=request.POST.get('medication')
        email=request.POST.get('email')
        dosage=request.POST.get('dosage')
        instruction=request.POST.get('instruction')

        if not Patient.objects.filter(email=email).exists():
            messages.error(request,"No such patient found")
            return redirect('doctor_add_prescription')
        
        patient=Patient.objects.get(email=email)
        doctor=Doctor.objects.get(user=request.user)
        
        doc_pres=AddPrescription.objects.create(
            patients=patient,
            doctors=doctor,
            medication_names=medication,
            dosages=dosage,
            instructions=instruction,
            dates=datetime.now()
        )
        doc_pres.save()
        messages.success(request,"Precription sent to the patient")

        userss=Patient.objects.get(email=email)
        create_notification(userss,"Doctor has added a prescription do check it out in your dashboard!!")

        return redirect('doctor_add_prescription')

    return render(request,'doctor_nav/d_addprescription.html')

def doctor_prescription(request):
    patients=Appointment.objects.filter(d_name=request.user)
    presc = None 
    medical = None 
    if request.method == 'POST':
        patientSelect=request.POST.get('patientSelect')

        if patientSelect:
            presc=Prescription.objects.filter(patient_id=patientSelect)            
            medical=MedicalReport.objects.filter(patient_id=patientSelect)  


    return render(request,'doctor_nav/d_prescription.html',{'patients':patients,'pres':presc,'medical':medical})

def mark_as_available(request,doctor_id):
    doc=Doctor.objects.get(id=doctor_id)
    doc.is_available=True
    doc.save()
    return redirect('doctor_dashboard')

def mark_as_unavailable(request,doctor_id):
    doc=Doctor.objects.get(id=doctor_id)
    doc.is_available=False
    doc.save()
    return redirect('doctor_dashboard')

def delete_appoint(request,id):
    press=Appointment.objects.get(id=id)
    press.delete()
    return redirect('doctor_appointment')

def edit_appoint(request,id):
    press=Appointment.objects.get(id=id)
    if request.method == 'POST':
        date=request.POST.get('date')
        time=request.POST.get('time')

        press.date=date
        press.time=time

        press.save()
        messages.success(request, "Appointment updated successfully!")
        return redirect('doctor_appointment')

    return render(request,'edit/appoitnmentedit.html',{'i':press})

def doctor_notification_list(request):
    user=Doctor.objects.get(user=request.user)
    notifications=DoctorNotification.objects.filter(doctor=user)
    context={
        'notifications':notifications
    }
    return render(request,'doctor_nav/dlist.html',context)

def dclear_all_notification(request):
    press=DoctorNotification.objects.all()
    press.delete()
    return redirect('doctor_dashboard')
