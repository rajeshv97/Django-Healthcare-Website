# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


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

class Department(models.Model):
    deptid = models.CharField(primary_key=True, max_length=4)
    deptname = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Department'


class Employee(models.Model):
    employeeid = models.CharField(primary_key=True, max_length=4)
    firstname = models.CharField(max_length=20, blank=True, null=True)
    lastname = models.CharField(max_length=20, blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    gender = models.CharField(max_length=6, blank=True, null=True)
    designation = models.CharField(max_length=10, blank=True, null=True)
    experience = models.IntegerField(blank=True, null=True)
    salary = models.IntegerField(blank=True, null=True)
    deptid = models.CharField(max_length=4, blank=True, null=True)
    email = models.CharField(max_length=40, blank=True, null=True)
    type = models.CharField(max_length=50, blank=True, null=True)
    area = models.CharField(max_length=50, blank=True, null=True)
    dateofjoin = models.DateField(blank=True, null=True)
    ssn = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Employee'
