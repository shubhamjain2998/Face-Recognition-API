from django.contrib import admin
from attendance.models import Account,Organization,Department,Attendance,User

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    pass

class AccountAdmin(admin.ModelAdmin):
    pass

class OrganizationAdmin(admin.ModelAdmin):
    pass

class DepartmentAdmin(admin.ModelAdmin):
    pass

class AttendanceAdmin(admin.ModelAdmin):
    pass

admin.site.register(User,UserAdmin)
admin.site.register(Account, AccountAdmin)
admin.site.register(Organization,OrganizationAdmin)
admin.site.register(Department,DepartmentAdmin)
admin.site.register(Attendance,AttendanceAdmin)