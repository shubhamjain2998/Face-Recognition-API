from django.conf.urls import url
from django.urls import path
from attendance import views
from django.urls.conf import include
from attendance.views import(
    OrganizationList,
    OrganizationDetail,
    DepartmentList,
    DepartmentDetail,
    AccountList,
    AccountDetail,
    AccountRegister,
    AccountFilter,
    CreateUserView,
    AttendanceList,
    AttendanceDetail,
    AttendanceFilter,
    report_att,
    daily_report,
    report_download,
)

app_name = "api-attendance"

urlpatterns = [
    url('^detect/$', views.detect, name='detect'),
    url('^train_dataset/$', views.train_dataset, name='train_dataset'),
    
    path('auth/', include('rest_auth.urls')),

    path('api/user/register',CreateUserView.as_view(),name='User-Register'),
    path('api/accounts', AccountList.as_view(), name='accounts'),
    path('api/accounts/filter', AccountFilter.as_view(), name='Acc-Filter'),
    path('api/accounts/register', AccountRegister.as_view(), name='Acc-Register'),
    path('api/accounts/<int:empId>/', AccountDetail.as_view(), name='account-detail'),

    path('api/org', OrganizationList.as_view(), ),
    path('api/org/<int:pk>/',OrganizationDetail.as_view(),name='Org-Detail'),

    path('api/attendance', AttendanceList.as_view(), name='Attendance-List'),
    path('api/attendance/<int:pk>', AttendanceList.as_view(), name='Attendance-Detail'),
    path('api/attendance/filter', AttendanceFilter.as_view(), name='Attendance-Filter'),

    path('api/dept', DepartmentList.as_view(), name='Dept-List'),
    path('api/dept/<int:pk>/',DepartmentDetail.as_view()),
    
    path('api/report',report_att),
    path('api/daily_report',daily_report),
    path('api/report_download',report_download),
    url('^$',views.home)   
]

# url('^addEmp/$', views.addEmployee, name='addEmployee'),
# url('^addDept/$', views.addDepartment, name='addDepartment'),
# url('^addOrg/$', views.addOrganization, name='addOrganization')