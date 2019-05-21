from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)

from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self,phone,is_admin=False,is_active=True,is_staff=False,language='EN',password=None,commit=False):
        if not phone:
            raise ValueError("User must have a phone number")
        
        user_obj = self.model(phone=phone)

        if not password:
            user_obj.set_password(self.make_random_password())
        else:
            user_obj.set_password(password)

        user_obj.admin = is_admin
        user_obj.staff = is_staff
        user_obj.active = is_active
        user_obj.phone_verified = True
        user_obj.save(using=self._db)
        return user_obj

    def create_staffuser(self,phone,password):
        user = self.create_user(
            phone,
            password=password,
            is_staff=True
        )

        user.save(using=self._db)
        return user

    def create_superuser(self,phone,password):
        user = self.create_user(
            phone,
            password=password,
            is_staff=True,
            is_admin=True
        )

        user.save(using=self._db)
        return user



class User(AbstractBaseUser,PermissionsMixin):
    phone_regex =  RegexValidator(regex=r'^\+?1?\d{9,14}$',message='Phone number must be entered in following format')
    phone       =  models.CharField(max_length=15,validators=[phone_regex], unique=True)
    email       =  models.EmailField(blank=True,null=True)
    name        =  models.CharField(max_length=55,blank=True,null=True)
    active      =  models.BooleanField(default=True)
    admin       =  models.BooleanField(default=False)
    staff       =  models.BooleanField(default=False)
    first_login =  models.BooleanField(default=False)
    phone_verified = models.BooleanField(default=False)
    email_verified = models.BooleanField(default=False)
    language       = models.CharField(max_length=2,default='EN', blank=True,null=True)
    objects = UserManager()

    def __str__(self):
        return self.phone

    def get_full_name(self):
        if self.name:
            return self.name
        else:
            return self.phone

    def get_shortname(self):    
        if self.name:
            return self.name
        else:
            return self.phone

    def has_module_perms(self,app_label):
        return True

    def has_perm(self,perm, obj=None):
        return True

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_active(self):
        return self.active

    @property
    def is_admin(self):
        return self.admin


    @property
    def is_superuser(self):
        return self.admin

    @property
    def is_email_verified(self):
        return self.email_verified
    
    @property
    def is_phone_verified(self):
        return self.phone_verified


    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []


class OTP(models.Model):
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,14}$', message='phone number must be entered in folloeing format *********')
    phone = models.CharField(validators = [phone_regex],max_length=17)
    otp = models.CharField(max_length=10, blank=True, null=True)
    count = models.IntegerField(default=0,help_text='Number of otp sent')    
    validated = models.BooleanField(default=False,help_text='Only if it is verified')
    objects = models.Manager()
    
    def __str__(self):
        return str(self.phone)+" is sent "+ str(self.otp)


class Location(models.Model):
    lat = models.FloatField(max_length=20, default=0.0)
    lng = models.FloatField(max_length=20, default=0.0)

    def __str__(self):
        return f'({self.lat}, {self.lng})'


