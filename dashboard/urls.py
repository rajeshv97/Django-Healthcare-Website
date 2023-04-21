from django.urls import path
from . import views
from .views import home_view,book_appointment_view,available_doctors_view,doctor_availability_view,successfully_booked_appointment_view,patient_medical_history_view,patient_views_appointment_view,patientbillview,highestpaidres,equipmentview,equipment

from .views import home_view,book_appointment_view,available_doctors_view, payslip,medical_record_view,medical_record_suc,medrecordsearch,medrecordview,doctorappointments,adminstats,patientbillsearch,highestpaid,adminappointment,adminappointmentres
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('',home_view,name = 'home'),
    path('bookappointment/',book_appointment_view,name = 'bookappointment'),
    path('patientappointment/',patient_views_appointment_view,name = 'patientappointment'),
    path('bookappointment/availabledoctors/',available_doctors_view,name = 'availabledoctors'),
    path('bookappointment/availabledoctors/doctoravailability',doctor_availability_view,name = 'doctoravailability'),
    path('bookappointment/availabledoctors/appointmentbookedsuccessfully',successfully_booked_appointment_view,name = 'appointmentbookedsuccessfully'),
    path('patientmedicalhistory/',patient_medical_history_view,name = 'patientmedicalhistory'),
    path('payslip/',payslip,name = 'payslip'),
    path('docmedicalrecord/',medical_record_view,name = 'docmedicalrecord'),
    path('docmedicalrecord/medrecordsuccess',medical_record_suc,name = 'medrecordsuccess'),
    path('medrecordsearch/',medrecordsearch,name = 'medrecordsearch'),
    path('medrecordsearch/medrecordview',medrecordview,name = 'medrecordview'),
    path('doctorappointments/',doctorappointments,name = 'doctorappointments'),
    path('adminstats/',adminstats,name = 'adminstats'),
    path('adminstats-patientbillsearch/',patientbillsearch,name = 'adminstats-patientbillsearch'),
    path('adminstats-patientbillsearch/adminstats-patientbill',patientbillview,name = 'adminstats-patientbill'),
    path('adminstats-highestpaidsearch/',highestpaid,name = 'adminstats-highestpaidsearch'),
    path('adminstats-highestpaidsearch/adminstats-highestpaid',highestpaidres,name = 'adminstats-highestpaid'),
    path('adminstats-appointmentsearch/',adminappointment,name = 'adminstats-appointmentsearch'),
    path('adminstats-appointmentsearch/adminstats-appointment',adminappointmentres,name = 'adminstats-appointment'),
    path('adminstats-equipmentsearch/',equipment,name = 'adminstats-equipmentsearch'),
    path('adminstats-equipmentsearch/adminstats-equipment',equipmentview,name = 'adminstats-equipment'),
    #path('docmedicalrecord//medrecordssuccess',medical_record_success,name = 'docmedicalrecord'),
    # path('medrecordsuccess/',medical_record_view,name = 'medrecordsuccess'),,
    # path('docmedicalrecord/medrecordssuccess',medical_record,name = 'medrecordssuccess'),
    

   
    
]