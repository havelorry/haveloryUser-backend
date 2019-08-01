
from django.contrib.auth import get_user_model, authenticate
from rolepermissions.roles import assign_role 
from rolepermissions.permissions import grant_permission,revoke_permission
from rest_framework import serializers
from .roles import VIEW_RIDE_HISTORY,CREATE_RIDE
User = get_user_model()
from accounts.models import Profile

def format_message(message):
    return {
        'status':False,
        'message':message
    }


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('phone','first_login','language')

class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('phone','password')
        extra_kwargs = {
            'password':{
                'write_only':True
            }
        }

    def create(self,validated_data):
        user = User.objects.create_user(**validated_data)
        assign_role(user,'customer')
        grant_permission(user,CREATE_RIDE)
        grant_permission(user,VIEW_RIDE_HISTORY)
        return user



class LoginSerializer(serializers.Serializer):
    phone = serializers.CharField()

    def validate(self,data):
        print(data)
        phone = data.get('phone') 
        password = data.get('password') or "soludents@123#"
        if phone and password:
            if User.objects.filter(phone = phone):
                data['user'] = authenticate(request=self.context.get('request'),phone=phone,password=password)
            else:
                raise serializers.ValidationError(format_message('Phone number not found'),code='authorization')
        
        if not phone:
            raise serializers.ValidationError(format_message('Please provide phone number'),code='authorization')

        
        if not password:
            raise serializers.ValidationError(format_message('password cannot be blank'),code='authorization')

        return data



class ProfileSerializer(serializers.ModelSerializer):
    
    user = UserSerializer()
    depth = 1
    class Meta:
        model = Profile
        fields = (
            'firstName',
            'lastName',
            'profilePic',
            'user'
        ) 


        
