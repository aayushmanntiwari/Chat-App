from django.urls import path
from django.urls.resolvers import URLPattern
from .views import *
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    path('',SignIn.as_view(),name="signin"),
    #path('api/token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    #path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]