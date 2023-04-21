from django.shortcuts import render
from django.http import HttpResponse
from django.db import connection
from collections import namedtuple
from django.utils import timezone
import datetime
from datetime import date
from django.utils.dateparse import parse_date
from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.mail import send_mail

def docview(request):
    return render(request, 'dashboard/doctorbase.html')


# Create your views here.
@cache_control(no_cache=True, must_revalidate=True,no_store=True)
@login_required(login_url='/employeelogin/')
def home_view(request):
        if request.user.is_superuser:
                return HttpResponse('')
                
        if request.user.is_staff:
                current_user = request.user
                us = current_user.username
                with connection.cursor() as cursor:
                        cursor.execute("select count(*) as count from online_appointment o join appointment a on o.appid = a.appid where appointment_date >= sysdate and  employeeid = %s",[us])
                        query1 = cursor.fetchone()
                        cursor.execute("select  count(*) as count from offline_appointment o join appointment a on o.appid = a.appid where appointment_date >= sysdate and   employeeid =%s",[us])
                        query2 = cursor.fetchone()
                        cursor.execute("select count(distinct patientID) as count from appointment where employeeID = %s",[us])
                        query3 = cursor.fetchone()
                        cursor.execute("select count(employeeID) from employee where deptID = (select deptID from employee where employeeID = %s)",[us])
                        query4 = cursor.fetchone()
                        print(type(query1))
                return render(request, 'dashboard/employeehome.html',{'query1':query1,'query2':query2,'query3':query3,'query4':query4})
                

        else:
            current_user = request.user
            us = current_user.username
            with connection.cursor() as cursor:
                    cursor.execute("with pivoted_paitent_bill as (select * from (select * from patient_bill pb) pivot (sum(pbamount) for PBStatus in ('Paid' as Patient_Bill_Paid, 'Pending' as Patient_Bill_Pending))),patient_all_bills as (select patientid, coalesce(sum(Patient_Bill_Paid), 0) as Bill_paid, coalesce(sum(Patient_Bill_Pending), 0) as Bill_Due from pivoted_paitent_bill group by patientid) select p.PatientID, firstname, lastname, age, phoneno, Bill_Paid, Bill_Due, (Bill_Paid + Bill_Due) as Total_Bill from patient p join patient_all_bills pab on p.patientid = pab.patientid where p.patientID =%s;",[us])
                    query = dictfetchall(cursor)
                    print(query)
            return render(request, 'dashboard/patienthome.html',{'query':query})


def dictfetchall(cursor):
        "Return all rows from a cursor as a dict"
        columns = [col[0] for col in cursor.description]
        return [
                dict(zip(columns, row))
                for row in cursor.fetchall()
        ]

@cache_control(no_cache=True, must_revalidate=True,no_store=True)
@login_required(login_url='/login/')
def book_appointment_view(request):
        if request.user.is_superuser:
                return HttpResponse('')
                
        if request.user.is_staff:
                return HttpResponse('')
                

        else:
            with connection.cursor() as cursor:
                    cursor.execute("select distinct DEPTNAME FROM DEPARTMENT")
                    query = dictfetchall(cursor)
            return render(request, 'dashboard/bookanappointment.html',{'query': query})



def adminappointment(request):
    if request.user.is_superuser:
        return HttpResponse('')
        
    if request.user.is_staff:
        return HttpResponse('')
        

    else:
    	with connection.cursor() as cursor:
	        cursor.execute("select distinct DEPTNAME FROM DEPARTMENT")
	        query = dictfetchall(cursor)

	        return render(request, 'dashboard/adminstats-appointmentsearch.html',{'query': query})


def adminappointmentres(request):
    if request.user.is_superuser:
        return HttpResponse('')
        
    if request.user.is_staff:
        return HttpResponse('')
        

    else:
    	result = request.GET["departments"]
    	print(result)
    	with connection.cursor() as cursor:
	        cursor.execute("with dept_appointment as ( select deptname, e.firstname, e.lastname, count(*) as no_of_appointments from appointment a join employee e on a.employeeid = e.employeeid join department d on e.deptid = d.deptid group by deptname, e.firstname, e.lastname) select * from dept_appointment where deptname = %s order by no_of_appointments desc",[result])
	        query = dictfetchall(cursor)

	    
    	
    	return render(request, 'dashboard/adminstats-appointment.html',{'query' : query,'query1' : result})


def available_doctors_view(request):
        if request.user.is_superuser:
                return HttpResponse('')
                
        if request.user.is_staff:
                return HttpResponse('')
                

        else:
            result = request.GET["departments"]
            print(type(result))
            with connection.cursor() as cursor:
                    cursor.execute("SELECT employeeID, firstname,lastname, deptname FROM employee e JOIN department d ON e.deptID = d.deptID WHERE designation = 'Doctor' and deptname = %s ORDER BY deptname, employeeID, firstname, lastname",[result])
                    query = dictfetchall(cursor)

            
            
            return render(request, 'dashboard/available_doctors.html',{'query' : query})


def highestpaid(request):
    if request.user.is_superuser:
        return HttpResponse('')
        
    if request.user.is_staff:
        return HttpResponse('')
        

    else:
    	with connection.cursor() as cursor:
	        cursor.execute("select distinct DEPTNAME FROM DEPARTMENT")
	        query = dictfetchall(cursor)

	        return render(request, 'dashboard/adminstats-highestpaidsearch.html',{'query': query})
    
def highestpaidres(request):
    if request.user.is_superuser:
        return HttpResponse('')
        
    if request.user.is_staff:
        return HttpResponse('')
        

    else:
    	result = request.GET["departments"]
    	print(result)
    	with connection.cursor() as cursor:
	        cursor.execute("select EmployeeID, e.deptID, DeptName as Department_Name ,firstname as Employee_First_Name , lastname as Employee_Last_Name, Age, Gender, Designation, salary, row_number() over (partition by e.deptID order by salary desc) from employee e join  department d on e.deptid = d.deptid where DeptName= %s",[result])
	        query = dictfetchall(cursor)

	    
    	
    	return render(request, 'dashboard/adminstats-highestpaid.html',{'query' : query,'query1' : result})

    
@cache_control(no_cache=True, must_revalidate=True,no_store=True)
@login_required(login_url='/login/')
def doctor_availability_view(request):
        if request.user.is_superuser:
                return HttpResponse('')
                
        if request.user.is_staff:
                return HttpResponse('')
                

        else:
            today = date.today()

            dates = []
            for i in range(1,8):
                tom = today + datetime.timedelta(days = i)
                dates.append(datetime.datetime.strptime(str(tom), '%Y-%m-%d').strftime('%y/%m/%d'))
                print(datetime.datetime.strptime(str(tom), '%Y-%m-%d').strftime('%y/%m/%d'))



            result2 = request.GET["employeeid"]

            print(result2)
            print(type(result2))
            
            

            
            
            return render(request, 'dashboard/doctor_availability.html',{'dates':dates,'result2':result2})

@cache_control(no_cache=True, must_revalidate=True,no_store=True)
@login_required(login_url='/login/')
def successfully_booked_appointment_view(request):

    try:
        if request.user.is_superuser:
                return HttpResponse('')
                
        if request.user.is_staff:
                return HttpResponse('')
                

        else:
            current_user = request.user
            us = current_user.username
            result2 = request.GET.get("employeeid")
            date = request.GET.get("dates")

            time = request.GET["time"]
            onlineoffline = request.GET["onlineoffline"]
            print(onlineoffline)
            print(type(onlineoffline))
            print(date)
            print(type(date))
            print(result2)
            with connection.cursor() as cursor:
                    query = "INSERT INTO appointment (patientID, appointment_time, appointment_date, type, employeeid) VALUES (%s,%s,%s,%s,%s)"
                    cursor.execute(query,[us,time,date,onlineoffline,result2])
                    cursor.execute("select EMAIL from patient where patientid=%s",[us])
                    res = cursor.fetchone()
                    print(res)
                    print(type(res))
                    zoomlink = 'https://us04web.zoom.us/j/8998767064?pwd=eUszNEs1dG54ZE95ZlIrMGV0bWxPZz09'

            subject = 'Successfully Booked Appontment for' + date
            if onlineoffline =='Online':
                message = 'Hello' + ' ' + us + "\n" + onlineoffline + ' ' 'appointment has been booked for' + ' ' + date + ' ' + 'and zoom link is' + ' ' + zoomlink + "\n" 
            else:
                message = 'Hello' + ' ' + us + "\n" + onlineoffline + ' ' + 'appointment has been booked for' + ' ' + date + '.' + ' ' + 'Please contact reception on arrival for cabin no'
            
            email_from = settings.EMAIL_HOST_USER
            recepient = res
            send_mail(subject,message,email_from,recepient)

            return render(request, 'dashboard/appointmentbookedsuccessfully.html')

    except:
        return render(request, 'dashboard/cannotbookappointment.html')

   







@cache_control(no_cache=True, must_revalidate=True,no_store=True)
@login_required(login_url='/login/')
def patient_medical_history_view(request):
        if request.user.is_superuser:
                return HttpResponse('')
                
        if request.user.is_staff:
                return HttpResponse('')
                

        else:
            current_user = request.user
            us = current_user.username
            with connection.cursor() as cursor:
                    cursor.execute("select p.patientID, firstname, lastname, age, gender, diagnosis, knowndisease from patient p join medical_record m on p.patientID = m.patientID where p.patientID = %s",[us])
                    query = dictfetchall(cursor)

            
            
            

            
            print(query)
            return render(request, 'dashboard/patientmedicalhistory.html',{'query':query})

@cache_control(no_cache=True, must_revalidate=True,no_store=True)
@login_required(login_url='/login/')
def patient_views_appointment_view(request):
        if request.user.is_superuser:
                return HttpResponse('')
                
        if request.user.is_staff:
                return HttpResponse('')
                

        else:
            current_user = request.user
            us = current_user.username
            with connection.cursor() as cursor:
                        cursor.execute("select firstname, lastname, email, meetinglink, to_char(appointment_date, 'DD-MON-YYYY') as appdate,appointment_time from appointment a join employee e on a.employeeid = e.employeeid join online_appointment oa on a.appid = oa.appid WHERE patientid = %s",[us])
                        query = dictfetchall(cursor)
                        cursor.execute("select a.appid, firstname, lastname, email, to_char(appointment_date, 'DD-MON-YYYY') as appdate,appointment_time, cabinno from appointment a join employee e on a.employeeid = e.employeeid join offline_appointment oa on a.appid = oa.appid WHERE patientid = %s",[us])
                        query2 = dictfetchall(cursor)
                    # cursor.execute("select firstname, lastname, email, meetinglink, appointment_date,appointment_time from appointment a join employee e on a.employeeid = e.employeeid join online_appointment oa on a.appid = oa.appid WHERE patientid = %s",[us])


                     
                 
            
            

            
            print(query)
            return render(request, 'dashboard/patientappointments.html',{'query':query,'query2':query2})
##should change the if condition because the patient can also see the payslip 

@cache_control(no_cache=True, must_revalidate=True,no_store=True)
@login_required(login_url='/employeelogin/')
def payslip(request):
        if request.user.is_superuser:
                return HttpResponse('')
                
        else:
                current_user = request.user
                us = current_user.username
                with connection.cursor() as cursor:
                        cursor.execute("select e.employeeID, firstname, lastname, designation, to_char(paymentdate, 'DD-MON-YYYY') as paymentdate, amount, deptid, paymentID from payslip p join employee e on p.employeeid = e.employeeid where e.employeeID = %s order by paymentdate",[us])
                        query = dictfetchall(cursor)
                        print(query)
                return render(request, 'dashboard/payslip.html',{'query' : query})

@cache_control(no_cache=True, must_revalidate=True,no_store=True)
@login_required(login_url='/employeelogin/')
def docmedicalrecord(request):
        if request.user.is_superuser:
                return HttpResponse('')
                
        else:
                current_user = request.user
                us = current_user.username
                with connection.cursor() as cursor:
                        cursor.execute("select e.employeeID, firstname, lastname, designation, to_char(paymentdate, 'DD-MON-YYYY') as paymentdate, amount, deptid, paymentID from payslip p join employee e on p.employeeid = e.employeeid where e.employeeID = %s order by paymentdate",[us])
                        query = dictfetchall(cursor)
                        print(query)
                return render(request, 'dashboard/payslip.html',{'query' : query})



@cache_control(no_cache=True, must_revalidate=True,no_store=True)
@login_required(login_url='/employeelogin/')
def medical_record_view(request):
        # print(pform.instance.my_field)
        return render(request,'dashboard/docmedicalrecord.html') 

@cache_control(no_cache=True, must_revalidate=True,no_store=True)
@login_required(login_url='/employeelogin/') 
def medical_record_suc(request):
        print(request)
        if(request.method== 'POST'):
                diagnosis = request.POST["diagnosis"]
                knowndisease = request.POST['knowndisease']
                patientid = request.POST['patientid']
                print(diagnosis)
                print(knowndisease)
                current_user = request.user
                us = current_user.username
                with connection.cursor() as cursor:
                         date = datetime.datetime.now().date()
                         print(date)
                         query = "INSERT into medical_record (diagnosis,knowndisease,patientid,recorddate) values (%s,%s,%s,%s)"
                         cursor.execute(query, [diagnosis,knowndisease,patientid,date])
                return render(request, 'dashboard/medrecordsuccess.html')

@cache_control(no_cache=True, must_revalidate=True,no_store=True)
@login_required(login_url='/employeelogin/')            
def medrecordsearch(request):
        # print(pform.instance.my_field)
        return render(request,'dashboard/medrecordsearch.html') 


@cache_control(no_cache=True, must_revalidate=True,no_store=True)
@login_required(login_url='/employeelogin/')
def medrecordview(request):
        print(request)
        if(request.method== 'GET'):
                patientid = request.GET['patientid']
                current_user = request.user
                us = current_user.username
                with connection.cursor() as cursor:
                         date = datetime.datetime.now().date()
                         print(date)
                         cursor.execute("select p.patientID, firstname, lastname, age, gender, diagnosis, knowndisease from patient p join medical_record m on p.patientID = m.patientID where p.patientID = %s",[patientid])
                         query = dictfetchall(cursor)
                         cursor.execute("select firstname from patient p join medical_record m on p.patientID = m.patientID where p.patientID = %s",[patientid])
                         query2 = cursor.fetchone()

        return render(request, 'dashboard/medrecordview.html',{'query' : query,'query2':patientid})


def patientbillsearch(request):
    # print(pform.instance.my_field)
    return render(request,'dashboard/adminstats-patientbillsearch.html') 

def patientbillview(request):
    print(request)
    if(request.method== 'GET'):
        patientid = request.GET['patientid']
        current_user = request.user
        us = current_user.username
        with connection.cursor() as cursor:
             date = datetime.datetime.now().date()
             print(date)
             cursor.execute("with due_bill as ( select patientID, sum(pbamount) as Bill_Due from Patient_bill where PBstatus = 'Pending' group by patientID having sum(pbamount) > %s) select p.PatientID, firstname, lastname, age, gender, phoneno, Bill_Due from patient p join due_bill d on p.patientId = d.patientID order by Bill_Due desc",[patientid])
             query = dictfetchall(cursor)

        return render(request, 'dashboard/adminstats-patientbill.html',{'query' : query,'query2':patientid})

def equipment(request):
    # print(pform.instance.my_field)
    return render(request,'dashboard/adminstats-equipmentsearch.html') 

def equipmentview(request):
    print(request)
    if(request.method== 'GET'):
        patientid = request.GET['patientid']
        current_user = request.user
        us = current_user.username
        with connection.cursor() as cursor:
             date = datetime.datetime.now().date()
             print(date)
             cursor.execute("select vendorname, equipname, to_char(manufacturingdate, 'DD-MON-YYYY') as appdate, quantity, unitprice, (quantity*unitprice) as Pending_Order_Amount, status from PRODUCT_ORDER_DETAILS d join product p on d.prodid = p.prodid join equipment e on p.prodid = e.prodid join vendor v on d.vendorid = v.vendorid where status in ('Shipped', 'Packed') and prodtype = 'EQUIPMENT' and (quantity*unitprice) > %s order by Pending_Order_Amount desc",[patientid])
             query = dictfetchall(cursor)

        return render(request, 'dashboard/adminstats-equipment.html',{'query' : query,'query2':patientid})


 


def doctorappointments(request):
        current_user = request.user
        us = current_user.username
        with connection.cursor() as cursor:
                cursor.execute("select a.appid, firstname, lastname, age, gender, phoneno,  meetinglink, to_char(appointment_date, 'DD-MON-YYYY') as appdate, appointment_time from appointment a join patient p on a.patientid = p.patientid join online_appointment oa on a.appid = oa.appid WHERE employeeid = %s",[us])
                query = dictfetchall(cursor)
                cursor.execute("select a.appid, firstname, lastname, age, gender, phoneno,cabinno, to_char(appointment_date, 'DD-MON-YYYY') as appdate, appointment_time from appointment a join patient p on a.patientid = p.patientid join offline_appointment oa on a.appid = oa.appid WHERE employeeid  = %s",[us])
                offquery = dictfetchall(cursor)
                print(offquery)
        return render(request, 'dashboard/doctorappointments.html',{'query' : query,'offquery':offquery})

@cache_control(no_cache=True, must_revalidate=True,no_store=True)
@login_required(login_url='/employeelogin/')
def adminstats(request):
        if request.user.is_superuser:
                with connection.cursor() as cursor:
                        cursor.execute("with due_bill as ( select patientID, sum(pbamount) as Bill_Due from Patient_bill where PBstatus = 'Pending' group by patientID having sum(pbamount) > 5000 ) select p.PatientID, firstname, lastname, age, gender, phoneno, Bill_Due from patient p join due_bill d on p.patientId = d.patientID order by Bill_Due desc fetch first 5 rows only")
                        offquery = dictfetchall(cursor)
                        cursor.execute("select deptname, e.firstname as employee_firstname, e.lastname as employee_lastname, a.appid as appointmentId, patientid, appointment_date, appointment_time from appointment a join employee e on a.employeeid = e.employeeid join department d on e.deptid = d.deptid order by deptname, appointment_date, appointment_time, appointmentID")
                        offquery1 = dictfetchall(cursor)
                        cursor.execute("select EmployeeID, e.deptID, DeptName as Department_Name ,firstname , lastname , Age, Gender, Designation, salary, row_number() over (partition by e.deptID order by salary desc) orderbysalary from employee e join department d on e.deptid = d.deptid")
                        offquery2 = dictfetchall(cursor)
                return render(request, 'dashboard/adminstats.html',{'query' : offquery,'query1' : offquery1,'query2' : offquery2})
                
        if request.user.is_staff:
                 return HttpResponse('')
                
        else:
                return HttpResponse('')
            

# with due_bill as ( select patientID, sum(pbamount) as Bill_Due from Patient_bill where PBstatus = 'Pending' group by patientID having sum(pbamount) > 5000 ) select p.PatientID, firstname, lastname, age, gender, phoneno, Bill_Due from patient p join due_bill d on p.patientId = d.patientID order by Bill_Due desc fetch first 5 rows only
# ;

#select deptname, e.firstname as employee_firstname, e.lastname as employee_lastname, a.appid as appointmentId, patientid, appointment_date, appointment_time from appointment a join employee e on a.employeeid = e.employeeid join department d on e.deptid = d.deptid order by deptname, appointment_date, appointment_time, appointmentID  ;

#select EmployeeID, e.deptID, DeptName as Department_Name ,firstname as "Employee First Name", lastname as "Employee Last Name", Age, Gender, Designation, salary, row_number() over (partition by e.deptID order by salary desc) orderbysalary from employee e join department d on e.deptid = d.deptid
