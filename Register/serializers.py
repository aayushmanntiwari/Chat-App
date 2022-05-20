import re
import datetime
import phonenumbers
from phonenumbers import carrier
from phonenumbers.phonenumberutil import number_type
from django.contrib.auth.models import User
from rest_framework import serializers
from .models import UserProfile
from .country_code import countryDictionary
from People.models import Friends


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('middle_name','phone_number','birthday','country')
    def validate(self, attrs):
        if bool(attrs['middle_name']) and not attrs['middle_name'].isalpha():
            raise serializers.ValidationError({'middle_name':'Middle name cannot contain any numeric value!'})
        if not bool(attrs['phone_number']):
            raise serializers.ValidationError({'phone_number':'This field is required!'})
        if  bool(attrs['phone_number']):
            try:
                carrier._is_mobile(number_type(phonenumbers.parse("+" + countryDictionary[attrs['country']] + str(attrs['phone_number']))))
            except Exception as e:    
                raise serializers.ValidationError({'phone_number':e})
        if  bool(attrs['phone_number']) and UserProfile.objects.filter(phone_number = "+" + countryDictionary[attrs['country']] + str(attrs['phone_number'])).exists():
            raise serializers.ValidationError({'phone_number':'A user with that phone number already exists.'})
        if not bool(attrs['birthday']):
            raise serializers.ValidationError({'birthday':'This field is required!'})
        return attrs
    
    def create(self, validated_data):
        profile, created = UserProfile.objects.get_or_create(
            middle_name = validated_data['middle_name'],
            birthday = datetime.datetime.strptime(str(validated_data['birthday']), '%Y-%m-%d').strftime('%Y-%m-%d'),
            country = validated_data['country'],
            phone_number = "+" + countryDictionary[validated_data['country']] + str(validated_data['phone_number']),
            user =  User.objects.get(id = self.context.get('user_id')),
        )
        if created:
            user_friends = Friends.objects.create(user =  User.objects.get(id = self.context.get('user_id')))
            user_friends.save()
            profile.save()
            return profile


    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','username','password','first_name','last_name')
        extra_kwargs = {'password': {'write_only': True}}
        read_only_fields = ('id',)

    def validate(self, attrs):
        if  bool(attrs['username']) and re.compile('[@_!#$%^&*()<>?/\|}{~:]').search(attrs['username']) is not None:
            raise serializers.ValidationError({'username':'username cannot contain any special character'})
        if not bool(attrs['first_name']):
            raise serializers.ValidationError({'first_name':'First name is required!'})
        if not bool(attrs['last_name']):
            raise serializers.ValidationError({'last_name':'Last name is required!'})
        if bool(attrs['first_name']) and not attrs['first_name'].isalpha():
            raise serializers.ValidationError({'first_name':'First name cannot contain any numeric value!'})
        if bool(attrs['last_name']) and not attrs['last_name'].isalpha():
            raise serializers.ValidationError({'last_name':'Last name cannot contain any numeric value!'})
        return attrs
    def create(self,validated_data):
        user, created = User.objects.get_or_create(
            username = validated_data['username'],
            first_name = validated_data['first_name'],
            last_name = validated_data['last_name'],
            is_active = True,
            is_superuser = False,
            is_staff = False,
        )
        if created:
            user.set_password(validated_data['password'])
            user.save()
            return user
        
       
        