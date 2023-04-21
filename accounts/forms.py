from django import forms
from . models import Patient
from . models import Employee
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class PatientRegisterForm(UserCreationForm) :
	
	
	class Meta:
		model = User
		fields = ['username','password1','password2']


class PatientProfileUpdateForm(forms.ModelForm) :
	
	class Meta:
		model = Patient
		fields = ['firstname','lastname','age','gender','phoneno','streetname','areaname','city','state','pincode']

class EmployeeProfileUpdateForm(forms.ModelForm) :

	class Meta:
		model = Employee
		fields = ['firstname','lastname','email','ssn']
