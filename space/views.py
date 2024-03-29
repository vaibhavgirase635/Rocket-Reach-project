from rest_framework import generics, permissions,viewsets,status
from rest_framework.response import Response
from knox.models import AuthToken
from django.contrib.auth import login
from rest_framework.views import APIView
from knox.views import LoginView as KnoxLoginView
from .serializers import *
from .models import *
from rest_framework.generics import ListCreateAPIView,CreateAPIView
from rest_framework.filters import OrderingFilter,SearchFilter
import pandas as pd
import csv
import codecs
from rest_framework.decorators import action
from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from itertools import islice
from rest_framework.permissions import AllowAny
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render,HttpResponse,redirect
from django.db.models import Q

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

    # def get(self, request, id, *args, **kwargs):
    #     self.object = self.get_object(id=id)
    #     return Response({'user': self.object}, template_name='profile.html')

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
        contact_dict=[]
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
                    contact_dict.append(j)
            obj1=(Contacts.objects.bulk_create(contact_list))
            
            return Response(contact_dict)

class ProductView(viewsets.ModelViewSet):
    
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    

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
        contact_dict=[]
        for row in data:
          
                print(row)
                Product.objects.create(
                    title=row[0],
                    selling_price=row[1],
                    discounted_price=row[2],
                    description=row[3],
                    brand=row[4],
                    specifications=row[5],           
                                
                    )
                return Response('Data stored')
                
                    
                
                
                
                    


class Profile_Retrieve_View(generics.RetrieveAPIView):
    queryset = Tokens.objects.all()
    serializer_class = TokenSerializer
    permission_classes = [AllowAny,]
    
    def retrieve(self, request, *args, **kwargs):
        
        if self.request.user:
            print(self.request.user.id)
            logged_in_user_query = Tokens.objects.get(id=self.request.user.id)  # (id=self.kwargs["id"])
            print(logged_in_user_query)
            print(logged_in_user_query.user)
            print(logged_in_user_query.tokens)
            if logged_in_user_query.tokens == 0:
                return redirect('http://127.0.0.1:8000/space/purchased_subcription_create/')
            elif logged_in_user_query.tokens > 0:
                logged_in_user_query.tokens = logged_in_user_query.tokens - 1  
                logged_in_user_query.save()
                try:
                    query = Tokens.objects.get(id=self.kwargs["id"])  # id=self.request.user.id
                    serializer = self.get_serializer(query)
                    #print(query)
                    return Response(serializer.data, status=status.HTTP_200_OK)
                except ObjectDoesNotExist:
                    return Response({"DOES_NOT_EXIST": "Does not exist"}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"NO_ACCESS": "Access Denied"}, status=status.HTTP_401_UNAUTHORIZED)

class Pricing_Plan_List(generics.ListAPIView):
    queryset = Pricing_Plan.objects.all()
    serializer_class = PricingSerializer
    permission_classes = [AllowAny,]

    def list(self, request, *args, **kwargs):
        if self.request.user:
            print(self.request.user)
            serializer = self.get_serializer(self.get_queryset(), many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"NO_ACCESS": "Access Denied"}, status=status.HTTP_401_UNAUTHORIZED)    
            
class Purchased_Subcription_View(generics.CreateAPIView):
    queryset = Purchased_Subcription.objects.all()
    serializer_class = Purchased_Subcription_Serializer

    def post(self, request, format=None):
        serializer = Purchased_Subcription_Serializer(data=request.data)
       
        if serializer.is_valid():
            serializer.save()
            subscription  = serializer.data['subscription']
            print(subscription)
            query = Pricing_Plan.objects.get(id=subscription)
            print(query.tokens) 
            obj1 = query.tokens
            
            user_name = serializer.data['user_name']
            print(user_name)
            query_user=Tokens.objects.get(id=user_name)
            print(query_user.tokens)
            print(query_user.user)
            query_user.tokens += obj1
            print(query_user.tokens)
            query_user.save()
         
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TokenView(CreateAPIView):
    permission_classes = (permissions.AllowAny,)
    queryset = Tokens.objects.all()
    serializer_class = TokenSerializer

def search(request):
    if request.method == 'GET':
        query = request.GET.get('q')
        print(query)
        submitbutton = request.GET.get('submit')
        #print(submitbutton)
        if query is not None:
            lookups = (Q(full_name__icontains=query) | Q(location__icontains=query) | Q(school__icontains=query) | Q(company__icontains=query) | Q(gender__icontains=query) | Q(email__icontains=query) | Q(linkdin__icontains=query) | Q(github__icontains=query) | Q(Twitter__icontains=query))
            data = User_Profile.objects.filter(lookups)
            #print(data)
            context={'data':data,
                    'submitbutton':submitbutton}
            print(context)
            return render(request,'profile.html',context)
        else:
            return render(request,'profile.html')
    else:
        return render(request,'profile.html')

def GetContact(request, id):
    profile = User_Profile.objects.get(id=id)
    print(profile)
    Contacts(
        full_name = profile.full_name,
        stream = profile.stream,
        school = profile.school,
        degree = profile.degree,
        job_title = profile.job_title,
        skills = profile.skills,
        experiance = profile.experiance,
        company = profile.company,
        phone = profile.phone,
        email = profile.email,
        linkdin = profile.linkdin,
        Twitter = profile.Twitter,
        github = profile.github,
        gender = profile.gender,
        DOB = profile.DOB,
        profile_photo = profile.profile_photo,
        location = profile.location,
        alt_phone = profile.alt_phone,
    )
    return render(request, 'contact.html', {'profile':profile})    

