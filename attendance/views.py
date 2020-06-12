from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from attendance import recognize as rec, data_creator as dc, train_model
from attendance.models import Account,Organization, Department, Attendance
from django.contrib.auth import get_user_model

import django_filters.rest_framework
from rest_framework import generics,mixins,permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import FormParser, MultiPartParser, JSONParser
from rest_framework import status
# from rest_framework import status

from .serializers import DepartmentSerializer, OrganizationSerializer, AccountSerializer
from .serializers import AttendanceSerializer, UserSerializer

import numpy as np
import urllib
import json
import cv2

def home(request):
    return render(request, 'home.html')

# class AccountList(APIView):
#     def get(self, request, format=None):
#         emp = AccountSerializer(Account.objects.all(),many=True)
#         return Response(emp.data)

#     def post(self,request, format=None):
#         emp = AccountSerializer(data=request.data)
#         if emp.is_valid():
#             emp.save()
#             return Response(emp.data, status=status.HTTP_201_CREATED)
#         return Response(emp.errors, status=status.HTTP_400_BAD_REQUEST)

class CreateUserView(mixins.CreateModelMixin, generics.ListAPIView):
    model = get_user_model()
    permission_classes = [
        permissions.AllowAny  # Or anon users can't register
    ]
    serializer_class = UserSerializer

    def get_queryset(self):
        usermodel = get_user_model()
        return usermodel.objects.all()

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class AccountRegister(generics.CreateAPIView):
    queryset            = Account.objects.all()
    serializer_class    = AccountSerializer
    parser_classes = [FormParser, MultiPartParser, JSONParser]

    # filter_backends     = filter_backends = [filters.SearchFilter]
    # search_fields       = ['username', 'email', 'role']

class AccountList(generics.ListAPIView):
    lookup_field = 'empId'
    queryset            = Account.objects.all()
    serializer_class    = AccountSerializer
    # extra_kwargs = {
    #         'url': {'view_name': 'account', 'lookup_field': 'pk'},
    #     }

class AccountFilter(generics.ListAPIView):
    serializer_class = AccountSerializer
    def get_queryset(self):
        """
        This view should return a list of all the purchases for
        the user as determined by the username portion of the URL.
        """
        queryset = Account.objects.all()
        role     = self.request.query_params.get('role', None)
        orgId    = self.request.query_params.get('orgId', None) 
        emailId  = self.request.query_params.get('email', None) 

        if role is not None:
            queryset = queryset.filter(role__exact=role)
        if orgId is not None:
            queryset = queryset.filter(orgId__exact=orgId)
        if emailId is not None:
            queryset = queryset.filter(emailId__exact=emailId)
        return queryset
    
class AccountDetail(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'empId'
    queryset = Account.objects.all().order_by('empId')
    serializer_class = AccountSerializer

class OrganizationList(generics.ListCreateAPIView):
    lookup_field = 'pk'
    parser_classes = [FormParser, MultiPartParser]
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    

class OrganizationDetail(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'pk'
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer

class DepartmentList(generics.ListCreateAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer

class DepartmentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer

class AttendanceList(generics.ListCreateAPIView):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer

class AttendanceDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer

class AttendanceFilter(generics.ListAPIView):
    serializer_class = AttendanceSerializer
    def get_queryset(self):
        """
        This view should return a list of all the purchases for
        the user as determined by the username portion of the URL.
        """
        queryset = Attendance.objects.all().order_by('date')
        empId    = self.request.query_params.get('empId', None)
        if empId is not None:
            queryset = queryset.filter(empId__exact=empId)
        return queryset


@csrf_exempt
def detect(request):
    # initialize the data dictionary to be returned by the request
    data = {"success": False}
    id=None
    # check to see if this is a post request
    if request.method == "POST":
        # check to see if an image was uploaded
        if request.FILES.get("image", None) is not None:
            # grab the uploaded image
            image = _grab_image(stream=request.FILES["image"])
        # otherwise, assume that a URL was passed in
        else:
            # grab the URL from the request
            req = request.POST.get("id", None)
            # if the URL is None, then return an error
            if req is None:
                data["error"] = "No URL provided."
                return JsonResponse(data)
            id = request.POST["id"]
            print(id)
            # load the image and convert
            # image = _grab_image(url=url)
        if id is None:
            result = rec.predict_face(image)
            if result["error"] != '':
                data["success"] = False
                data["result"] = result
            else:
                # data.update({'result': result})
                data = fetch_details(result['name'],result['accuracy'])
        else:
            data = fetch_details(id)
        

    # return a JSON response
    return JsonResponse(data)

def fetch_details(id,acc=''):
    data = {}
    data["success"] = True
    account = Account.objects.all()
    account.order_by('empId')
    if int(id) not in range(int(account.first().empId),int(account.last().empId)):
        data['error'] = "Employee ID is not valid"
        data["success"] = "False"
        return data
    res = {}
    res['empId'] = id
    res['firstName'] = account.get(empId=int(id)).firstName
    res['lastName'] = account.get(empId=int(id)).lastName
    res['accuracy'] = acc
    data['result'] = res
    return data

def _grab_image(path=None, stream=None, url=None):
    # if the path is not None, then load the image from disk
    if path is not None:
        image = cv2.imread(path)
    # otherwise, the image does not reside on disk
    else:
        # if the URL is not None, then download the image
        if url is not None:
            resp = urllib.urlopen(url)
            data = resp.read()
        # if the stream is not None, then the image has been uploaded
        elif stream is not None:
            data = stream.read()
        # convert the image to a NumPy array and then read it into
        # OpenCV format
        image = np.asarray(bytearray(data), dtype="uint8")
        image = cv2.imdecode(image, cv2.IMREAD_COLOR)

    # return the image
    return image

@csrf_exempt
def train_dataset(request):
    name = request.POST['empId']
    # if request.FILES.get("image", None) is not None:
            # grab the uploaded image
            # image = _grab_image(stream=request.FILES["image"])
    images = dict((request.FILES).lists())['image']
    for i in images:
        image = _grab_image(stream=i)
    
        dc.create_dataset(name,image)


    train_model.create_model()
    return JsonResponse({"status":"success, dataset and model created successfully"})
