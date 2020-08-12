from rest_framework import serializers
# from django.contrib.auth import get_user_model
from .models import Account,Organization,Department,Attendance,Attendance_Config, Payments, Cards
from django.contrib.auth import get_user_model

class UserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)

    def create(self, validated_data):

        user = get_user_model().objects.create(
            email=validated_data['email'],
            is_staff=validated_data['is_staff']
            # username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        # user.is_staff(False)
        user.save()

        return user

    class Meta:
        model = get_user_model()
        # fields = [
        #     'pk',
        #     'first_name',
        #     'last_name',
        #     'username',
        #     'email',
        #     'password',
        # ]
        fields = '__all__'


class UserDetailsSerializer(serializers.ModelSerializer):
    """
    User model w/o password
    """
    class Meta:
        model = get_user_model()
        fields = '__all__'
        read_only_fields = ('email', )


class AccountSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Account
        fields = (
            'url',
            'pk',
            'empId',
            'emailId',
            'username',
            'firstName',
            'lastName',
            'gender',
            'phone',
            'readEmp',
            'addEmp',
            'readAtt',
            'addAtt',
            'readDept',
            'addDept',
            'idType' ,
            'idProof' ,
            'profileImg',
            'orgId',
            'deptId',
            'role',   
        )

    def get_url(self, obj):
        request = self.context.get("request")
        return obj.get_api_url(request=request)

class OrganizationSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Organization
        fields = (
            'url',
            'pk',
            'Name',
            'orgType',
            # emailId = models.EmailField()
            # passwd = models.CharField(max_length=20)
            'contact',
            'staffcount',
            'logo',
        )
    def get_url(self, obj):
        request = self.context.get("request")
        return obj.get_api_url(request=request)

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'   
    
class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = "__all__"

class Attendance_ConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Attendance_Config
        fields = "__all__"

class PaymentsSerializer(serializers.ModelSerializer):
    class Meta:
        model   = Payments
        fields  = '__all__' 

class CardsSerializer(serializers.ModelSerializer):
    class Meta:
        model   = Cards
        fields  = '__all__'