from asyncore import read
from requests import request
from rest_framework import serializers, status
from .models import *
from Register.models import UserProfile



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')


class FriendsSerializer(serializers.ModelSerializer):
    friends = UserSerializer(many=True, read_only=True) #Pasing many=True shows friends holds multiple objects 
    user = UserSerializer()
    class Meta:
        model = Friends
        fields = ('user', 'friends',)


class FriendRequestListSerializer(serializers.ModelSerializer):
    sender = UserSerializer()
    receiver = UserSerializer()
    class Meta:
        model = FriendRequestList
        fields = ('sender', 'receiver','status')


class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = UserProfile
        fields = ('middle_name', 'user',)