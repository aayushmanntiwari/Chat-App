from multiprocessing import context
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from .serializers import UserSerializer,UserProfileSerializer
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
#from django.contrib.sessions.backends.db import SessionStore
from rest_framework.renderers import TemplateHTMLRenderer,JSONRenderer
from .country_code import countryDictionary



# Create your views here.


class SignUp(APIView):
    renderer_classes = [TemplateHTMLRenderer,JSONRenderer]
    def post(self,request):
        userserializer = UserSerializer(data = request.data)
        if userserializer.is_valid():
            userserializer.save()
            userprofileserializer = UserProfileSerializer(data = request.data,context={'user_id':userserializer.data['id']})
            get_user = User.objects.get( id = userserializer.data['id'])
            if userprofileserializer.is_valid():
                userprofileserializer.save()
                refresh = RefreshToken.for_user(get_user)
                '''s = SessionStore()
                s['refresh'] =  str(refresh)
                s['access'] =  str(refresh.access_token)
                s['has_token'] = True
                s.create()'''
                refresh.blacklist()
                return JsonResponse({'message': 'User registered sucessfully!',
                                'mobile_number': "+" + countryDictionary[request.data['country']] + str(request.data['phone_number']),
                                'access_token':str(refresh.access_token),
                                'refresh_token':str(refresh),
                            },status=status.HTTP_201_CREATED)
            else:
                if get_user is not None:
                    get_user.delete()
                return JsonResponse(userprofileserializer._errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return JsonResponse(userserializer._errors, status=status.HTTP_400_BAD_REQUEST)
    def get(self,request):
        return Response(template_name='register.html')
        
