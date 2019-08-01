from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser,MultiPartParser
from rest_framework.response import Response
from django.contrib.auth import login
from knox.views import LoginView as KnoxLoginView
from knox.auth import TokenAuthentication
from rest_framework import views
from rest_framework.permissions import IsAuthenticated
from .models import User, OTP, Profile
from django.forms import model_to_dict
import random

from .permissions import APIPermission
from .serializers import CreateUserSerializer, LoginSerializer, ProfileSerializer
# Create your views here.

def send_otp(phone):
    if phone:
        key = random.randint(99999,999999)
        print(key)
        return key
    else:
        return False



class ValidatePhoneSendOTP(APIView):
    permission_classes = (APIPermission,)
    parser_classes = (JSONParser,)
    def post(self,request,*args, **kwargs):
        phone_number = request.data.get('phone')
        if phone_number:
            phone = str(phone_number)
            user = User.objects.filter(phone__iexact=phone)
            if user.exists():
                return Response({
                    'status':False,
                    'message':'Phone number already taken'
                })

            else:
                key = send_otp(phone)
                if key:
                    old = OTP.objects.filter(phone__iexact = phone)
                    if old.exists():
                        old = old.first()
                        count = old.count
                        if count > 10:
                            return Response(
                                {'status': False,
                                'message':'Sending OTP Error.. Limit Exceeds'}
                            )
                        old.count = count +1
                        old.save()

                    OTP.objects.create(
                        phone = phone,
                        otp = key
                    )

                    return Response({
                        'status':True,
                        'message':'OTP sent successfully'
                    })

                else:
                    return Response({
                        'status':False,
                        'message':'OTP sending Error'
                    })

        else:
            return Response({
                'status':False,
                'message':'phone number is not supplied'
            })




class ValidateOTP(APIView):
    
    permission_classes = (APIPermission,)
    parser_classes = (JSONParser,)

    def post(self,request,*args,**kwargs):
        phone = request.data.get('phone',False)
        otp_sent = request.data.get('otp',False)

        if phone and otp_sent:
            old = OTP.objects.filter(phone__iexact = phone)
            if old.exists():
                old =old.first()
                otp = old.otp
                if str(otp_sent) == str(otp):
                    old.validated = True
                    old.save()

                    return Response({
                        'status':True,
                        'message':'OTP verified.'
                    })
                else:
                    return Response({
                        'status':False,
                        'message':'OTP not verified.'
                    })
            else:
                return Response({
                    'status':False,    
                    'message':'First proceed by sending otp'
                })
        else:
            return Response({
                    'status':False,
                    'message':'Please provide required fields'
                })


class Register(APIView):
    
    permission_classes = (APIPermission,)
    parser_classes = (JSONParser,)
    
    def post(self,request,*args,**kwargs):
        phone = request.data.get('phone')
        
        if phone:
            old = OTP.objects.filter(phone__iexact=phone)
            if old.exists():
                old = old.first()
                validated = old.validated

                if validated:
                    temp_data = {
                        'phone':phone,
                        'password':'soludents@123#'
                    }

                    serializer =CreateUserSerializer(data = temp_data)
                    serializer.is_valid(raise_exception=True)
                    serializer.save()
                    old.delete()

                    return Response({
                        'status':True,
                        'message':'Account created successfully'
                    })

                else:
                    return Response({
                        'status':False,
                        'message':'OTP not verified'
                    })
        else:
            return Response({
                'status':False,
                'message':'Phone number is required . cannot be empty'
            })


class LoginView(KnoxLoginView):
    permission_classes = (APIPermission,)
    parser_classes = (JSONParser,)

    def post(self,request,format=None):
        
        temp_data = {
            'phone':request.data.get('phone'),
            'password':'soludents@123#',
        }

        print(temp_data)
        serializer = LoginSerializer(data=temp_data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super().post(request,format=None)


class UserDetailView(views.APIView):
    
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    parser_classes = (JSONParser,)

    def get(self,request,*args, **kwargs):
        user = request.user
        profile = Profile.objects.get_or_none(user=user)
        print(
            profile
        )
        ps = ProfileSerializer(instance=profile)



        return Response({
            'status':True,
            'data':ps.data
        })

    def post(self,request,*args,**kwargs):
        user = request.user
        request_data = {
            'user':model_to_dict(user),
            **request.data
        }

        
        profile = Profile.objects.get_or_none(user=user)
        if profile is None:
            ps = Profile()
            ps.user = user
            ps.firstName = request.data['firstName']
            ps.lastName = request.data['lastName']
            ps.profilePic = request.data['profilePic']
            ps.save()
            return Response({'data':ProfileSerializer(instance=ps).data, 'status':True})
        else:
            for key,value in request.data.items():
                setattr(profile,key,value)
            
            profile.save()
            return Response({'data':ProfileSerializer(instance=profile).data})


class FileUploadView(views.APIView):
    parser_classes = (MultiPartParser,JSONParser)

    def put(self, request, format=None):
        from django.core.files.storage import FileSystemStorage
        
        fs = FileSystemStorage()
        file_obj = request.FILES['file']
        filename = fs.save(f"profiles/{file_obj.name}", file_obj)

        return Response({
            'status':'ok',
            'file_url':fs.url(filename)
        })


