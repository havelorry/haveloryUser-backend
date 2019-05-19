from django.contrib import admin
# Register your models here.
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


from .forms import UserAdminCreationForm, UserAdminChangeForm
from .models import User,OTP
admin.site.register(User)
admin.site.register(OTP)