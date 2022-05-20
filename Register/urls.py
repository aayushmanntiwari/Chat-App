from django.urls import path
from .views import *


urlpatterns = [
    
    path('',SignUp.as_view(),name="create_acoount")
]