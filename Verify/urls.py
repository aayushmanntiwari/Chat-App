from django.urls import path
from .views import *

urlpatterns = [
    path('',Verify.as_view(),name="verify"),
    path('otpsend/',OtpSend.as_view(),name="otp")
]