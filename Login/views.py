from os import access
from django.contrib.auth.models import User
from django.shortcuts import render,redirect
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from django.contrib import messages
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import authenticate,login
from Register.models import UserProfile
from django.db.models import Q
from rest_framework_simplejwt.tokens import AccessToken,RefreshToken
from rest_framework.renderers import TemplateHTMLRenderer,JSONRenderer


# Create your views here.
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        token['first_name'] = user.first_name
        token['last_name'] = user.last_name
        token['id'] = user.id
        token['email'] = user.email
        # ...

        return token

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class SignIn(APIView):
    renderer_classes = [TemplateHTMLRenderer,JSONRenderer]
    def post(self,request):
        user_m_e = request.POST.get("user_m_e").replace(" ", "")
        password = request.POST.get('password').replace(" ", "")
        if  user_m_e is not None and password is not None:
            #userprofile = UserProfile.objects.get(Q(phone_number__iexact=user_m_e) | Q(user__username__iexact=user_m_e))
            #user_obj = authenticate(username=userprofile, password=password)
            #access = AccessToken.for_user(user_obj)
            #print(access)
            try:
                userprofile = UserProfile.objects.get(Q(phone_number__iexact=user_m_e) | Q(user__username__iexact=user_m_e))
                user_obj = authenticate(username=userprofile, password=password)
                if user_obj is not None:
                    if userprofile.phone_number_verified:
                        #access = AccessToken.for_user(user_obj)
                        #print(access)
                        #print(request.session['access'])
                        refresh = RefreshToken.for_user(user_obj)
                        '''s = SessionStore()
                        s['refresh'] =  str(refresh)
                        s['access'] =  str(refresh.access_token)
                        s['has_token'] = True
                        s.create()'''
                        login(request,user_obj)
                        return Response({'message': 'User Logged In','refresh': str(refresh),
                                'access': str(refresh.access_token)}, status=status.HTTP_202_ACCEPTED)
                    else:
                        return redirect('verify')
                else:
                    return Response({'message': 'Wrong credentials'}, status=status.HTTP_401_UNAUTHORIZED)
            except:
                return Response({'message': 'User is not registered!'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'message': 'Fields Cannot be Blank!'}, status=status.HTTP_400_BAD_REQUEST)

    def get(self,request):
        return Response(template_name='login.html')


'''@api_view(['POST'])
def signin(request):
    user_m_e = request.POST.get("user_m_e").replace(" ", "")
    password = request.POST.get('password').replace(" ", "")
    print(user_m_e)
    print(password)
    if  user_m_e is not None and password is not None:
        try:
            userprofile = UserProfile.objects.get(Q(phone_number__icontains=user_m_e) | Q(user__username=user_m_e) | Q(user__email=user_m_e))
            print(userprofile)
        except:
            return Response({'message': 'User is not registered!'}, status=status.HTTP_404_NOT_FOUND)
            print(userprofile)
            if userprofile is not None:
                print(userprofile.user)
                if userprofile.user.is_active:
                    user_obj = authenticate(username=userprofile.user.username, password=password)
                    if user_obj is not None:
                        login(request,user_obj)
                    else:
                        return Response({'message': 'wrong credentials'}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    pass
            else:
                return Response({'message': 'User is not registered!'}, status=status.HTTP_404_NOT_FOUND)
        except:
            return Response({'message': 'User is not registered!'}, status=status.HTTP_404_NOT_FOUND)

    else:
        return Response({'message': 'Fields Cannot be Blank!'}, status=status.HTTP_400_BAD_REQUEST)'''

