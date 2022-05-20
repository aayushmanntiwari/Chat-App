from email import message
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import logout
from rest_framework import status
from django.contrib.sessions.models import Session

# Create your views here.
class SignOut(APIView):
    def post(self,request):
        try:
            '''s = Session.objects.get(pk=request.POST.get('session_id'))
            get_refresh = s.get_decoded()['refresh']
            token_obj = RefreshToken(get_refresh)
            token_obj.blacklist()
            s.delete()'''
            logout(request)
            return Response({'message': 'User logged out sucessfully!'},status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'message':e},status=status.HTTP_400_BAD_REQUEST)
