from django.shortcuts import redirect, render
from rest_framework.response import Response
from rest_framework.decorators import api_view,renderer_classes
from rest_framework import status
from rest_framework.renderers import TemplateHTMLRenderer,JSONRenderer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse

# Create your views here.

class Home(APIView):
    #authentication_classes = [JWTAuthentication]
    #permission_classes = [IsAuthenticated]
    renderer_classes = [TemplateHTMLRenderer,JSONRenderer]
    def post(self,request):
        return JsonResponse(data={'message':'NOT Allowed'},status=status.HTTP_405_METHOD_NOT_ALLOWED)
    def get(self,request):
        return Response(template_name='people.html',status=status.HTTP_200_OK)
