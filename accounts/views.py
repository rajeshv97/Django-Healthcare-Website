from django.shortcuts import render,redirect
from .forms import PatientRegisterForm,PatientProfileUpdateForm
from .forms import PatientRegisterForm,EmployeeProfileUpdateForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import connection
from django import forms
import json
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control

# Create your views here.


def index(request):
    return render(request, 'accounts/index.html')

def registerpatient(request):
	if(request.method == 'POST'):
		form = PatientRegisterForm(request.POST)
		if form.is_valid():
			form.save()
			messages.success(request,f'Account Created.')
			return redirect('login')

	else:
		form = PatientRegisterForm()
	return render(request, 'accounts/patient_registration.html',{'form':form})

@cache_control(no_cache=True, must_revalidate=True,no_store=True)
@login_required(login_url='/login/')
def patientprofile(request):
    # print(pform.instance.my_field)
    
    if(request.method== 'POST'):
        pform = PatientProfileUpdateForm(request.POST)
        
        if pform.is_valid():
            firstname = request.POST.get('firstname')
            lastname = request.POST.get('lastname')
            age = request.POST.get('age')
            gender = request.POST.get('gender')
            phoneno= request.POST.get('phoneno')
            streetname=request.POST.get('streetname')
            areaname= request.POST.get('areaname')
            city= request.POST.get('city')
            state= request.POST.get('state')
            pincode= request.POST.get('pincode')
            with connection.cursor() as cursor:
                current_user = request.user
                us = current_user.username
                print(current_user.username)
                #cursor.execute("UP INTO patient (patientid,firstname) VALUES (8573,'firstnamel');")
                #cursor.execute("UPDATE patient set firstname='praveen',lastname=%s where patientid=%s",[firstname,lastname,current_user.username])
                #cursor.execute("UPDATE patient set firstname='praveen' where age=19")
                #cursor.execute("UPDATE patient set firstname=%s,lastname=%s,age=%(age)s where patientid=%s",[firstname,lastname,us])
                #cursor.execute("UPDATE patient set age=%(age)s where age=19")     
                query = "UPDATE patient set firstname=%s,lastname=%s,age=%s,gender=%s,phoneno=%s,streetname=%s,areaname=%s,city=%s,state=%s,pincode=%s where patientid=%s"
                cursor.execute(query, [firstname,lastname,age,gender,phoneno, streetname, areaname,city,state,pincode, us])                  
                return redirect('patientprofile')

    with connection.cursor() as cursor:
        current_user = request.user
        us = current_user.username
        cursor.execute("select * from patient where patientid=%s",[us])
        res = cursor.fetchone()
        #print(res[1])
        initial_data = {
            'firstname':res[1],
            'lastname':res[2],
            'age':res[3],
            'gender':res[4],
            'phoneno':res[5],
            'streetname':res[6],
            'areaname':res[7],
            'city':res[8],
            'state':res[9],
            'pincode':res[10]}
        
    pform = PatientProfileUpdateForm(initial = initial_data)
    return render(request, 'accounts/patient_profile.html',{'pform':pform})
            




        

# def fetchData(request):
#     current_user = request.user
#     print (current_user.id)
#     qry = 'select * from patient'
#     with connection.cursor() as cursor:
#         cursor.execute("select * from patient")
#         res = cursor.fetchall()
#         for row in res:
#             print(row)

# def fetchData(request):
#     json_str = False
#     current_user = request.user
#     print (current_user.username)
#     with connection.cursor() as cursor:
#         cursor.execute("select * from patient where patientid= %s",[current_user.username])
#         res = cursor.fetchone()
#         if json_str:
#             print(json.dumps( [dict(ix) for ix in res] )) #CREATE JSON
#     #for row in res:
#             #print(row)    

# def fetchData(request):
#     json_str = False
#     current_user = request.user
#     print (current_user.username)
#     with connection.cursor() as cursor:
#         cursor.execute("select * from patient where patientid='P002'")
#         res = cursor.fetchone()
#         print(res[1])
        # for row in res:
        #    print(row)
        # if json_str:
        #     print(json.dumps( [dict(ix) for ix in res] )) #CREATE JSON
        # for row in res:
        #     print(row)    


# if(request.method == 'POST'):
# 		pform = PatientProfileUpdateForm(request.POST)
# 		if pform.is_valid():
# 			with connection.cursor() as cursor:
# 				cursor.execute("INSERT INTO patient (patientid,firstname) VALUES (8573,'firstnamel');")
# 		return redirect('patientprofile')
# 	else:
# 		pform = PatientProfileUpdateForm()
# 	return render(request, 'accounts/patient_profile.html',{'pform':pform})
	
        

	       
@cache_control(no_cache=True, must_revalidate=True,no_store=True)
@login_required(login_url='/employeelogin/')
def employeeprofile(request):
    # print(pform.instance.my_field)
    
    if(request.method== 'POST'):
        pform = EmployeeProfileUpdateForm(request.POST)
        
        if pform.is_valid():
            firstname = request.POST.get('firstname')
            lastname = request.POST.get('lastname')
            email = request.POST.get('email')
            ssn = request.POST.get('ssn')
            with connection.cursor() as cursor:
                current_user = request.user
                us = current_user.username
                print(current_user.username)
                #cursor.execute("UP INTO patient (patientid,firstname) VALUES (8573,'firstnamel');")
                #cursor.execute("UPDATE patient set firstname='praveen',lastname=%s where patientid=%s",[firstname,lastname,current_user.username])
                #cursor.execute("UPDATE patient set firstname='praveen' where age=19")
                #cursor.execute("UPDATE patient set firstname=%s,lastname=%s,age=%(age)s where patientid=%s",[firstname,lastname,us])
                #cursor.execute("UPDATE patient set age=%(age)s where age=19")     
                
                query = "UPDATE employee set firstname=%s,lastname=%s,email=%s,ssn=%s where employeeid=%s"
                cursor.execute(query, [firstname,lastname,email,ssn, us])                  
                return redirect('employeeprofile')

    with connection.cursor() as cursor:
        current_user = request.user
        us = current_user.username
        cursor.execute("select * from employee where employeeid=%s",[us])
        res = cursor.fetchone()
        print(res)

        initial_data = {
            'firstname':res[1],
            'lastname':res[2],
            'email':res[9],
            'ssn':res[13]}
        
    pform = EmployeeProfileUpdateForm(initial = initial_data)
    return render(request, 'accounts/employee_profile.html',{'pform':pform})


            
