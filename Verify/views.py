import requests
import base64
from django.http import JsonResponse
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.renderers import TemplateHTMLRenderer,JSONRenderer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from Register.models import UserProfile
from django.contrib.auth.models import User

# Create your views here.
class Verify(generics.RetrieveAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    renderer_classes = [TemplateHTMLRenderer,JSONRenderer]
    
    def post(self,request):
        return JsonResponse(data={'message':'NOT Allowed'},status=status.HTTP_405_METHOD_NOT_ALLOWED)
        
    def get(self,request):
        url = f"https://2factor.in/API/V1/e34eead4-75fa-11ec-b710-0200cd936042/SMS/{request.GET.get('number','')}/AUTOGEN/"
        response = requests.get(url)
        json_data = response.json()
        #print(json_data['Status'])
        if json_data['Status'] == 'Success':
            return JsonResponse(data = {'authorize':json_data['Status'],'mobile_number':request.GET.get('number'),'session_id':json_data['Details']},status=status.HTTP_200_OK)
        return JsonResponse(data = {'phone_number':json_data['Details']},status=status.HTTP_400_BAD_REQUEST)


class OtpSend(generics.RetrieveAPIView):
    renderer_classes = [TemplateHTMLRenderer,JSONRenderer]
    def post(self,request):
        if len(str(base64.b64decode(request.POST.get('session_id','')).decode("utf-8")).split('-')) == 5:
            url = f"https://2factor.in/API/V1/e34eead4-75fa-11ec-b710-0200cd936042/SMS/VERIFY/{base64.b64decode(request.POST.get('session_id','')).decode('utf-8')}/{request.POST.get('otp_input','')}"
            response = requests.get(url)
            json_data = response.json()
            if json_data['Status'] == 'Success':
                userprofile = UserProfile.objects.get(phone_number = request.POST.get('mobile_number',''))
                if userprofile is not None:
                    userprofile.phone_number_verified = True
                    userprofile.save()
                    return JsonResponse(data = {'authorize':json_data['Status']},status=status.HTTP_200_OK)
                return JsonResponse(data = {'message':'User is not valid'},status=status.HTTP_400_BAD_REQUEST)
            return JsonResponse(data = {'message':f"{json_data['Details']} or Resent OTP"},status=status.HTTP_400_BAD_REQUEST)
        else:
            return JsonResponse(data = {'message':"Bad Request"},status=status.HTTP_400_BAD_REQUEST)
    def get(self,request):
        if base64.b64decode(request.GET.get('authorize','')).decode("utf-8")  == 'Success' and len(str(base64.b64decode(request.GET.get('session_id','')).decode("utf-8")).split('-')) == 5:
            return Response(data = {'mobile_number':base64.b64decode(request.GET.get('mobile_number','')).decode("utf-8"),'session_id':request.GET.get('session_id','')},template_name='mobile_otp.html',status=status.HTTP_200_OK)
        else:
            return JsonResponse(data={'message':'NOT VALID'},status=status.HTTP_400_BAD_REQUEST)
         