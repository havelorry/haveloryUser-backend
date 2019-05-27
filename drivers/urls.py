from .views import SignIn
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns=[
    path('login/',SignIn.as_view()),

]
urlpatterns = format_suffix_patterns(urlpatterns)
