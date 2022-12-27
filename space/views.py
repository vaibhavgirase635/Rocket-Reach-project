from rest_framework import generics, permissions,viewsets
from rest_framework.response import Response
from knox.models import AuthToken
from django.contrib.auth import login
from rest_framework.views import APIView
from knox.views import LoginView as KnoxLoginView
from .serializers import *
from .models import *
from rest_framework.generics import ListCreateAPIView
from rest_framework.filters import OrderingFilter,SearchFilter
import pandas as pd
import csv
import codecs
from rest_framework.decorators import action
from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from itertools import islice

fs = FileSystemStorage(location='tmp/')

# Register API
class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
        "user": UserSerializer(user, context=self.get_serializer_context()).data,
        "token": AuthToken.objects.create(user)[1]
        })

class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user'] 
        login(request, user)
        return super(LoginAPI, self).post(request, format=None)

class UserProfileView(ListCreateAPIView):
    #permission_classes=[IsAuthenticated]
    permission_classes = (permissions.AllowAny,)
    queryset = User_Profile.objects.all()
    serializer_class = ProfileSerializer
    filter_backends = [SearchFilter]
    search_fields = ['id','full_name','stream','school','job_title','company','email','linkdin','Twitter','github','location']

class ContactView(viewsets.ModelViewSet):
    
    queryset = Contacts.objects.all()
    serializer_class = ContactSerializer
    
    @action(detail=False, methods=['POST'])
    def upload_data(self, request):
        """Upload data from CSV"""
        file = request.FILES["file"]

        content = file.read()  # these are bytes
        file_content = ContentFile(content)
        file_name = fs.save("_tmp.csv", file_content)
        tmp_file = fs.path(file_name)
        csv_file = open(tmp_file, errors="ignore")
        reader = csv.reader(csv_file)
        print(reader)
        data = list(reader) 
        print(data)
        contact_list=[]
        
        for row in data:
          
            print(row)
            for i in row:
                print(i)
            
            
                obj = list(User_Profile.objects.filter(full_name=i).values())
                print(obj)
                for j in obj:
                    contact_list.append(
                        Contacts(
                            full_name=j['full_name'],
                            stream=j['stream'],
                            school=j['school'],
                            degree=j['degree'],
                            job_title=j['job_title'],
                            skills=j['skills'],
                            experiance=j['experiance'],
                            company=j['company'],
                            phone=j['phone'],
                            email=j['email'],
                            linkdin=j['linkdin'],
                            Twitter=j['Twitter'],
                            alt_phone=j['alt_phone'],
                            gender=j['gender'],
                            DOB=j['DOB'],
                            profile_photo=j['profile_photo'],
                            location=j['location'],
                            created_at=j['created_at'],
                            updated_at=j['updated_at']
                            )
                        )
            obj1=list(Contacts.objects.bulk_create(contact_list))
            
            return JsonResponse(obj,safe=False)
            