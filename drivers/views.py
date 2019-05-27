from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from django.contrib.auth import login
from knox.views import LoginView as KnoxLoginView
from knox.auth import TokenAuthentication
from rest_framework import views
from django.contrib.auth import authenticate
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
User = get_user_model()
class SignIn(APIView):
    def post(self,request,format=None):
        phone = request.data.get("username")
        password = request.data.get("password")
        if phone is None or password is None:
            return Response({'error': 'Please provide both username and password'},
                            status=status.HTTP_400_BAD_REQUEST)
        user=User.objects.filter(phone = phone,password=password)
        if user:
            #user = authenticate(phone=phone,password=password)
            
            return Response({'massge':"Login successfully"},
                                status=status.HTTP_200_OK)
                
        else:
            
            return Response({'error': 'Invalid Credentials'},
                            status=status.HTTP_404_NOT_FOUND)
                                  
        return Response("Something went wrong")
                    