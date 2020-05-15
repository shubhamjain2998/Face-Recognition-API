from django.contrib import admin
from attendance.models import Employee
# Register your models here.
class EmployeeAdmin(admin.ModelAdmin):
    pass

admin.site.register(Employee, EmployeeAdmin)