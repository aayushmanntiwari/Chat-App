'''@receiver(post_save, sender=User,dispatch_uid=User.id)
def create_user_profile(sender,instance, created,**kwargs):
    if created:
        print('signal called')
        print(created)
        print(instance)
        print("middle name: ",kwargs.get('middle'))
        UserProfile.objects.create(
            user = instance
        )
        print('profile created')
    else:
        print('user delete because of error!')
        instance.delete()
'''
'''@receiver(create_user_profile)
def create_user_profile(**kwargs):
    userprofileserializer = UserProfileSerializer(data = {'middle_name':kwargs['middle_name'],
    'phone_number':kwargs['phone_number'],'birthday':kwargs['birthday'],'country':kwargs['country'],'user':kwargs['user']})
    if userprofileserializer.is_valid():
        userprofileserializer.save()
        refresh = RefreshToken.for_user(kwargs['user'])
        return JsonResponse({'message': 'User registered sucessfully!',
                                'mobile_number': "+" + countryDictionary[kwargs['country']] + str(kwargs['phone_number']),
                                'access_token':str(refresh.access_token),
                                'refresh_token':str(refresh),
                            },status=status.HTTP_201_CREATED)
    else:
        print('something went wrong: ',kwargs['user'])
        kwargs['user'].delete()
        return JsonResponse(userprofileserializer._errors, status=status.HTTP_400_BAD_REQUEST)'''
            





