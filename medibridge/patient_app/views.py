'''
This urls.py file contains logic of patient app
'''

import requests
import uuid

from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from mainpage.models import *
from .models import *
from .utils import create_notification
from doctor_app.utils import doctor_create_notification

# Create your views here.

@login_required(login_url='/home')
def patient_dashboard(request):
    appoint=Appointment.objects.filter(patient=request.user)[:3]
    doct=Doctor.objects.all()
    records=MedicalReport.objects.filter(patient=request.user)[:3]

    user=Patient.objects.get(user=request.user)
    medical=AddPrescription.objects.filter(patients=user)

    notification_count=Notification.objects.filter(patient=user).count()

    context={
        'appoint':appoint,
        'doct':doct,
        'records':records,
        'medical':medical,
        'notification_count':notification_count
    }

    return render(request,'patient_nav/pdashboard.html',context)

def patient_appointment(request):
    doctor = Doctor.objects.filter(verified=True, is_available=True)
    if request.method == "POST":
        user = request.user
        doctors = request.POST.get('doctor')  # Doctor ID
        doctorss = Doctor.objects.get(id=doctors)  # Get doctor instance
        date = request.POST.get('date')
        time = request.POST.get('time')
        reason = request.POST.get('reason')

        # Payment parameters
        amt = 140  # Base Fee
        tAmt = 150  # Total Amount
        txAmt = 10  # Tax
        psc = 0     # Service Charge
        pdc = 0     # Delivery Charge
        scd = "EPAYTEST"
        pid = uuid.uuid4().hex  # Generate unique ID
        su = request.build_absolute_uri('/payment/success/')
        fu = request.build_absolute_uri('/payment/failure/')

        # Save appointment data in session
        request.session['appointment_data'] = {
            'user': user.id,
            'doctor_id': doctors,
            'date': date,
            'time': time,
            'reason': reason,
            'pid': pid,  # Save PID to validate later
        }

        # Redirect to eSewa
        esewa_url = "https://uat.esewa.com.np/epay/main"
        params = {
            'amt': amt,
            'tAmt': tAmt,
            'txAmt': txAmt,
            'psc': psc,
            'pdc': pdc,
            'scd': scd,
            'pid': pid,
            'su': su,
            'fu': fu,
        }
        query_string = '&'.join([f"{key}={value}" for key, value in params.items()])
        return redirect(f"{esewa_url}?{query_string}")

    return render(request, 'patient_nav/appointment.html', {'doctors': doctor})


def payment_success(request):
    # Get transaction details
    pid = request.GET.get('oid')
    amt = request.GET.get('amt')
    ref_id = request.GET.get('refId')

    print(f"Received PID: {pid}, Amount: {amt}, Reference ID: {ref_id}")

    # Verify payment
    verification_url = "https://uat.esewa.com.np/epay/transrec"
    data = {
        'amt': amt,
        'scd': 'EPAYTEST',
        'pid': pid,
        'rid': ref_id,
    }
    print(f"Verification data: {data}")

    response = requests.post(verification_url, data=data)
    print(f"eSewa Verification Response: {response.status_code}, {response.text}")

    if response.status_code == 200 and 'Success' in response.text:
        # Retrieve appointment data from session
        appointment_data = request.session.get('appointment_data')
        if appointment_data and appointment_data['pid'] == pid:
            try:
                # Retrieve doctor instance using the doctor ID stored in the session
                doctor = Doctor.objects.get(id=appointment_data['doctor_id'])
            except Doctor.DoesNotExist:
                messages.error(request, "The selected doctor does not exist.")
                return redirect('patient_appointment')
            # Save appointment to the database
            appointment=Appointment.objects.create(
                patient=request.user,
                d_name=doctor.user,
                date=appointment_data['date'],
                time=appointment_data['time'],
                description=appointment_data['reason'],
            )

            # Save the payment record
            Payment.objects.create(
                user=request.user,
                appointment=appointment,
                transaction_id=pid,
                amount=amt,
                payment_status='Success',
            )
            
            user=Patient.objects.get(user=request.user)

            docc=Doctor.objects.get(user=doctor.user)

            # Notification
            create_notification(user,"Your Appointment has been booked!!.Do verify your payment status!!")

            # doctor notification
            doctor_create_notification(docc,"New Appointment has been booked. Do check it out!!")

            # Clear session data after success
            del request.session['appointment_data']
            messages.success(request, "Your appointment has been successfully booked.")
            return redirect('patient_appointment')
    else:
        # Save failed payment record
        Payment.objects.create(
            user=request.user,
            transaction_id=pid,
            amount=amt,
            payment_status='Failure',
        )
        messages.error(request, "Payment verification failed. Please try again.")
        return redirect('patient_appointment')


def payment_failure(request):
    messages.error(request, "Payment was unsuccessful. Please try again.")
    return redirect('patient_appointment')


def patient_medical(request):
    medical=MedicalReport.objects.filter(patient=request.user)
    if request.method == 'POST':
        user=request.user
        date=request.POST.get('date')
        diagnosis=request.POST.get('diagnosis')
        treatment=request.POST.get('treatment')

        report=MedicalReport.objects.create(
            patient=user,
            date=date,
            diagnosis=diagnosis,
            treatment=treatment
        )
        report.save()
        messages.success(request,"Report entry successfull")
        return redirect('medical_report')
    return render(request,'patient_nav/medical_report.html',{'medical':medical})

def patient_pres(request):
    press=Prescription.objects.filter(patient=request.user)
    if request.method == 'POST':
        user=request.user
        medication=request.POST.get('medication')
        dosage=request.POST.get('dosage')
        instruction=request.POST.get('instruction')
        date=request.POST.get('date')

        pres=Prescription.objects.create(
            patient=user,
            medication_name=medication,
            dosage=dosage,
            instruction=instruction,
            date=date
        )
        pres.save()
        messages.success(request,"New Prescription Created!!!")
        return redirect('patient_pres')
    
    return render(request,'patient_nav/prescription.html',{'pres':press})

def patient_telemedicine(request):
    return render(request,'patient_nav/telemedicine.html')

def new_meeting(request):
    return render(request,'videos/videocall.html',{'name':request.user})

def join_meeting(request):
    if request.method == 'POST':
        roomID=request.POST.get('roomID')
        return redirect('/new_meeting?roomID='+roomID)
    return render(request,'videos/join.html')

def patient_payment(request):
    payments = Payment.objects.filter(user=request.user).order_by('-created_at')
    return render(request,'patient_nav/payment.html',{'payments':payments})

def delete_medical(request,id):
    medical=MedicalReport.objects.get(id=id)
    medical.delete()
    return redirect('medical_report')

def edit_medical(request,id):
    medical=MedicalReport.objects.get(id=id)
    if request.method == 'POST':
        user=request.user
        date=request.POST.get('date')
        diagnosis=request.POST.get('diagnosis')
        treatment=request.POST.get('treatment')

        medical.date=date
        medical.diagnosis=diagnosis
        medical.treatment=treatment

        medical.save()
        messages.success(request, "Medical report updated successfully!")
        return redirect('medical_report')

    return render(request,'edit/edit.html',{'i':medical})

def delete_pres(request,id):
    press=Prescription.objects.get(id=id)
    press.delete()
    return redirect('patient_pres')

def edit_pres(request,id):
    press=Prescription.objects.get(id=id)
    if request.method == 'POST':
        user=request.user
        medication=request.POST.get('medication')
        dosage=request.POST.get('dosage')
        instruction=request.POST.get('instruction')
        date=request.POST.get('date')

        press.medication_name=medication
        press.dosage=dosage
        press.instruction=instruction
        press.date=date

        press.save()
        messages.success(request, "Prescription updated successfully!")
        return redirect('patient_pres')

    return render(request,'edit/edit2.html',{'i':press})

def delete_all_transaction(request):
    dele=Payment.objects.all()
    dele.delete()
    return redirect('payment')

def clear_add_pres(request):
    press=AddPrescription.objects.all()
    press.delete()
    return redirect('patient_dashboard')

def notification_list(request):
    user=Patient.objects.get(user=request.user)
    notifications=Notification.objects.filter(patient=user)
    context={
        'notifications':notifications
    }
    return render(request,'patient_nav/list.html',context)

def clear_all_notification(request):
    press=Notification.objects.all()
    press.delete()
    return redirect('patient_dashboard')

def doctors_lists(request):
    doc_details=Doctor.objects.all()

     # Filter by name if provided
    name_query = request.GET.get('name', '')
    if name_query:
        doc_details = doc_details.filter(full_name__icontains=name_query)

    # Filter by specialization if provided
    specialization_query = request.GET.get('specialization', '')
    if specialization_query:
        doc_details = doc_details.filter(specialization__iexact=specialization_query)

    # Get unique specializations for the dropdown
    specializations = Doctor.objects.values_list('specialization', flat=True).distinct()

    context={
        'doctors':doc_details,
        'specializations': specializations,

    }
    return render(request,'doctors_list/doctors_list.html',context)

def view_doctors_lists(request,id):
    doc_details_view=Doctor.objects.get(id=id)
    context={
        'doctor':doc_details_view
    }
    return render(request,'doctors_list/view_details.html',context)

