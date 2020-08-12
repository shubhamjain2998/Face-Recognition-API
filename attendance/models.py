from django.db import models
from django.contrib.auth import get_user_model
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import AbstractUser
from rest_framework.reverse import reverse as api_reverse

# Create your models here.
class User(AbstractUser):
    username = models.CharField(blank=True, null=True, max_length=50)
    email = models.EmailField(unique=True)
    
    USERNAME_FIELD  = 'email'
    REQUIRED_FIELDS = ['username',]

    def __str__(self):
        return self.email



class MediaFileSystemStorage(FileSystemStorage):
    def get_available_name(self,name,max_length=None):
        if max_length and len(name) > max_length:
            raise (Exception("name length is greater than max_length"))
        return name
    
    def _save(self,name,content):
        if self.exists(name):
            return name
        
        return super(MediaFileSystemStorage,self)._save(name,content)
    
class Department(models.Model):
    depId       = models.IntegerField(unique=True)
    DeptName    = models.CharField(max_length=60)
    Description = models.TextField()

    def __str__(self):
        return self.DeptName

class Organization(models.Model):
    # OrgId = models.IntegerField(primary_key=True)
    Name = models.CharField(max_length=100)
    orgType = models.CharField(max_length=100)
    # emailId = models.EmailField()
    # passwd = models.CharField(max_length=20)
    contact = models.CharField(max_length=12)
    staffcount = models.IntegerField()
    logo = models.ImageField(upload_to='companyLogo//',storage=MediaFileSystemStorage(),blank=True,null=True)

    def get_api_url(self, request=None):
        return api_reverse("api-attendance:Org-Detail", kwargs={'pk': self.pk}, request=request)
    
    def __str__(self):
        return self.Name
    

class Account(models.Model):
    empId           = models.IntegerField(unique=True)
    # emailId         = models.EmailField(verbose_name='emailId',max_length=60, unique=True)
    emailId         = models.ForeignKey(get_user_model(),to_field='email',on_delete=models.CASCADE)
    username        = models.CharField(max_length=100,unique=True)
    firstName       = models.CharField(max_length=100)
    lastName        = models.CharField(max_length=100)
    # password        = models.CharField(max_length=30)
    gender          = models.CharField(max_length=100,choices=(('Male','Male'),('Female','Female')))
    phone           = models.CharField(max_length=100)
    readEmp         = models.BooleanField(default=False)
    addEmp          = models.BooleanField(default=False)
    readAtt         = models.BooleanField(default=False)
    addAtt          = models.BooleanField(default=False)
    readDept        = models.BooleanField(default=False)
    addDept         = models.BooleanField(default=False)

    idType          = models.CharField(max_length=100,choices=(
        ('Adhaar Card','Adhaar Card'),
        ('PAN Card','PAN Card'),
        ('Passport','Passport'),
        ('Driving License','Driving License')
    ))
    idProof         = models.CharField(max_length=100, unique=True)
    profileImg      = models.ImageField(upload_to='profilePics//',storage=MediaFileSystemStorage(),blank=True,null=True)
    orgId           = models.ForeignKey(Organization,on_delete=models.CASCADE)
    deptId          = models.ForeignKey(Department,on_delete=models.CASCADE)
    role            = models.CharField(max_length=100)

    def __str__(self):
        return self.firstName + self.lastName

    def get_api_url(self, request=None):
        return api_reverse("api-attendance:account-detail", kwargs={'empId': self.empId}, request=request)


class Attendance(models.Model): 
    empId       = models.ForeignKey(Account, to_field='empId', on_delete=models.CASCADE)
    check_in    = models.TimeField(null=True,blank=True)
    check_out   = models.TimeField(null=True,blank=True)
    date        = models.DateField()
    leave       = models.BooleanField(default=False)

    def __str__(self):
        return str(self.empId)

class Payments(models.Model):
    payId       = models.CharField(max_length=20)
    amount      = models.IntegerField()
    currency    = models.CharField(max_length=5)
    method      = models.CharField(max_length=20)
    captured    = models.BooleanField(default=False)
    description = models.TextField(max_length=100)
    email       = models.EmailField()
    contact     = models.IntegerField()
    fee         = models.IntegerField()
    tax         = models.IntegerField()
    createdAt   = models.TimeField(auto_now_add=True)

    def __str__(self):
        return str(self.payId)

class Cards(models.Model):
    cardId          = models.CharField(max_length=20)
    name            = models.CharField(max_length=20)
    last4           = models.CharField(max_length=4)
    network         = models.CharField(max_length=20)
    typeOfCard      = models.CharField(max_length=10)
    issuer          = models.CharField(max_length=20)
    international   = models.BooleanField(default=False)
    emi             = models.BooleanField(default=False)

    def __str__(self):
        return str(self.cardId)



class Attendance_Config(models.Model):
    orgId           = models.ForeignKey(Organization, on_delete = models.CASCADE)
    check_in_start  = models.TimeField()
    check_in_end    = models.TimeField()
    check_out_start = models.TimeField()
    check_out_end   = models.TimeField()
