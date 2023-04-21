from django.contrib import admin
from .models import Patient
from .models import Department
from .models import Employee

admin.site.register(Patient)
admin.site.register(Department)
admin.site.register(Employee)