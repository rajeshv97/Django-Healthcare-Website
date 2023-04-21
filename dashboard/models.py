from django.db import models
from django.db import connections
# Create your models here
class MedicalRecord(models.Model):
    recordid = models.CharField(primary_key=True, max_length=4)
    recorddate = models.DateField(blank=True, null=True)
    diagnosis = models.CharField(max_length=100, blank=True, null=True)
    knowndisease = models.CharField(max_length=100, blank=True, null=True)
    patientid = models.ForeignKey('Patient', models.DO_NOTHING, db_column='patientid', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'medical_record'
        
class Patient(models.Model):
    patientid = models.CharField(primary_key=True, max_length=4)
    firstname = models.CharField(max_length=20, blank=True, null=True)
    lastname = models.CharField(max_length=20, blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    gender = models.CharField(max_length=6, blank=True, null=True)
    phoneno = models.IntegerField(blank=True, null=True)
    streetname = models.CharField(max_length=10, blank=True, null=True)
    areaname = models.CharField(max_length=10, blank=True, null=True)
    city = models.CharField(max_length=10, blank=True, null=True)
    state = models.CharField(max_length=10, blank=True, null=True)
    pincode = models.IntegerField(blank=True, null=True)
    
    class Meta:
        managed = False
        db_table = 'PATIENT'