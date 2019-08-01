from django.urls import path, include, re_path
from .views import ValidatePhoneSendOTP,ValidateOTP,Register,LoginView,UserDetailView, FileUploadView
from knox.views import LogoutView as Logout
urlpatterns = [
    re_path(r'^validate/',ValidatePhoneSendOTP.as_view()),
    re_path(r'^verify_otp/',ValidateOTP.as_view()),
    re_path(r'^register/',Register.as_view()),
    re_path(r'^login/$',LoginView.as_view()),
    re_path(r'^logout/$',Logout.as_view()),
    re_path(r'^profile/$',UserDetailView.as_view()),
    re_path(r'^pic/$',FileUploadView.as_view())
]