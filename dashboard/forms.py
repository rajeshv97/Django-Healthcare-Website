from django import forms
from . models import Patient
from . models import MedicalRecord
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class MedicalRecordForm(forms.ModelForm) :
	
	class Meta:
		model = MedicalRecord
		fields = ['recordid','recorddate','diagnosis','knowndisease','patientid']

