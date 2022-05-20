from django.urls import path
from .views import *


urlpatterns = [
     path('',SignOut.as_view(),name="signout"),
]