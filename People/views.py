import secrets
from django.db.models import Q
from django.http import JsonResponse
from rest_framework import status
from rest_framework.renderers import TemplateHTMLRenderer,JSONRenderer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from Register.models import UserProfile
from django.contrib.auth.models import User
from django.forms.models import model_to_dict
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import FriendRequestList,Friends
from .serializers import FriendsSerializer,FriendRequestListSerializer,UserProfileSerializer
from rest_framework.pagination import PageNumberPagination

# Create your views here.
class Get_Api_Key(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    renderer_classes = [TemplateHTMLRenderer,JSONRenderer]
    def get(self, request):
        userprofile = UserProfile.objects.get(user = User.objects.get(username = request.user))
        userprofile.api_key = secrets.token_urlsafe()
        userprofile.save()
        return JsonResponse(data={'code':userprofile.api_key},status = status.HTTP_200_OK)


class People(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    renderer_classes = [TemplateHTMLRenderer,JSONRenderer]
    def get(self, request,code=None, *args, **kwargs):
        #print(User.objects.get(id = request.user.id))
        userprofile = UserProfile.objects.get(user = User.objects.get(id = request.user.id))
        return JsonResponse(data={'username':request.user.username,
                'first_name':request.user.first_name,
                'last_name':request.user.last_name,
                'phone_number':userprofile.phone_number,
                'middle_name':userprofile.middle_name,
        },status=status.HTTP_200_OK)

class FindPeople(APIView,PageNumberPagination):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    renderer_classes = [TemplateHTMLRenderer,JSONRenderer]
    def get_paginated_response(self, data, page, page_num):
        d= {}
        d['results'] = data
        d['count'] = self.page.paginator.count
        d['current'] = page
        d['next'] = self.get_next_link()
        d['previous'] = self.get_previous_link()
        d['page_size'] = page_num
        return d

    def get_queryset(self,request,users_list):
        return self.paginate_queryset(users_list, self.request)

    def post(self, request):

        '''Check if any match user is found or not else show no result found'''
        try:
            users_list = UserProfile.objects.filter(Q(user__username__icontains = request.POST.get('searchvalue')) & ~Q(user__is_staff = True) & ~Q(user__username__iexact = request.user.username))
        except:
            users_list = UserProfile.objects.filter(~Q(user__is_stuff = True) & ~Q(user__username__iexact = request.user.username))

        '''Get the current logged in user friends list'''
        friends = Friends.objects.get(user__username__iexact = request.user.username)
        if bool(friends.friends.all()):
            friendserializer = FriendsSerializer(friends)
            have_friends = friendserializer.data #many=True is not passed as friends holds single object
        else:
            have_friends = False
        
        '''Get friendrequestlist for the current logged in user'''
        friendrequestlists = FriendRequestList.objects.filter(sender = User.objects.get(username__iexact = request.user.username))
        if friendrequestlists:
            friendrequestserializer = FriendRequestListSerializer(friendrequestlists,many=True)
            friendrequests = friendrequestserializer.data #passing many=True means friendrequestlists holds mutliple objects 
        else:
            friendrequests = False

        #Pagination
        page = self.request.POST.get('page', 1) 
        page_size = self.request.POST.get('page_size', 2) #Items per page
        users = self.get_queryset(request,users_list)
        userprofileserializer = UserProfileSerializer(users,many=True)
        p = self.get_paginated_response(userprofileserializer.data, page, page_size)

        return JsonResponse(data={
            'have_friends':have_friends,
            'friendrequests':friendrequests,
            'users':p['results'],
            'users_found':bool(users_list),
            'count':p['count'],
            'current':p['current'],
            'next':p['next'],
            'previous':p['previous'],
            'page_size':p['page_size'],
            'sender':request.user.username,
            'anyfriendrequests':bool(friendrequests)

        },status=status.HTTP_200_OK,safe=False)
        

class FriendRequest(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    renderer_classes = [TemplateHTMLRenderer,JSONRenderer]
    def post(self, request):
        action = request.POST.get('action')
        sender_name = request.POST.get('sender_name')
        receiver_name = request.POST.get('receiver_name')
        receiverprofile = UserProfile.objects.get(user = User.objects.get(username__iexact = receiver_name ))
        if action == "add-friend":
            friendrequestlist,created = FriendRequestList.objects.get_or_create(sender = User.objects.get(username__iexact = sender_name),receiver =  User.objects.get(username__iexact = receiver_name))
            if created:
               #print(1)
               friendrequestlist.save()
               return JsonResponse(data = {'message':'Request Sent','sender_name':sender_name,'receiver_name':receiver_name,'action':action,'first_name':receiverprofile.user.first_name,'last_name':receiverprofile.user.last_name,'middle_name':receiverprofile.middle_name},status=status.HTTP_200_OK)
            if bool(friendrequestlist):
                #print(2)
                friendrequestlist.status = True
                friendrequestlist.save()
                return JsonResponse(data = {'message':'Request Sent','sender_name':sender_name,'receiver_name':receiver_name,'action':action,'first_name':receiverprofile.user.first_name,'last_name':receiverprofile.user.last_name,'middle_name':receiverprofile.middle_name},status=status.HTTP_200_OK)
            return JsonResponse(data = {'message':'Bad Request'},status=status.HTTP_400_BAD_REQUEST)
        if action == 'cancel-friend-request':
            friendrequestlist = FriendRequestList.objects.get(sender = User.objects.get(username__iexact = sender_name),receiver =  User.objects.get(username__iexact = receiver_name))
            if bool(friendrequestlist):
                friendrequestlist.cancel()
                return JsonResponse(data = {'message':'Request Cancelled','receiver_name':receiver_name,'sender_name':sender_name,'action':action,'first_name':receiverprofile.user.first_name,'last_name':receiverprofile.user.last_name,'middle_name':receiverprofile.middle_name},status=status.HTTP_200_OK)
            return JsonResponse(data = {'message':'Bad Request'},status=status.HTTP_400_BAD_REQUEST)
        if action == 'un-friend':
            friends = Friends.objects.get(user = User.objects.get(username__iexact = sender_name))
            rec_obj = Friends.objects.get(user = User.objects.get(username__iexact = receiver_name))
            if bool(friends):
                friends.friends.remove(User.objects.get(username__iexact = receiver_name))
                friends.save()
                rec_obj.friends.remove(User.objects.get(username__iexact = sender_name))
                rec_obj.save()
                return JsonResponse(data = {'message':'Friend Remove','receiver_name':receiver_name,'sender_name':sender_name,'action':action,'first_name':receiverprofile.user.first_name,'last_name':receiverprofile.user.last_name,'middle_name':receiverprofile.middle_name},status=status.HTTP_200_OK)
            return JsonResponse(data = {'message':'Bad Request'},status=status.HTTP_400_BAD_REQUEST)  
        if action == 'accpet-request':
            friend1 = Friends.objects.get(user = User.objects.get(username__iexact = sender_name))
            valid_frnd_1 = friend1.add_friend(User.objects.get(username__iexact = receiver_name))
            friend2 = Friends.objects.get(user = User.objects.get(username__iexact = receiver_name))
            valid_frnd_2 = friend2.add_friend(User.objects.get(username__iexact = sender_name))
            if valid_frnd_1 and valid_frnd_2:
                friendrequestlist = FriendRequestList.objects.get(sender = User.objects.get(username__iexact = sender_name),receiver =  User.objects.get(username__iexact = receiver_name))
                friendrequestlist.delete()
                usersrequests = FriendRequestList.objects.filter(receiver = User.objects.get(username__iexact = receiver_name))
                usersrequestsserializer = FriendRequestListSerializer(usersrequests,many=True)
                return JsonResponse(data = {'message':'Friends added','usersrequests':usersrequestsserializer.data,'action':action,'anyrequests':bool(usersrequests)},status=status.HTTP_200_OK)
            return JsonResponse(data = {'message':'Bad Request'},status=status.HTTP_400_BAD_REQUEST)
        if action == 'delete-request':
            friendrequestlist = FriendRequestList.objects.get(sender = User.objects.get(username__iexact = sender_name),receiver =  User.objects.get(username__iexact = receiver_name))
            if bool(friendrequestlist):
                friendrequestlist.delete()
                usersrequests = FriendRequestList.objects.filter(receiver = User.objects.get(username__iexact = receiver_name))
                usersrequestsserializer = FriendRequestListSerializer(usersrequests,many=True)
                return JsonResponse(data = {'message':'Friends added','usersrequests':usersrequestsserializer.data,'action':action,'anyrequests':bool(usersrequests)},status=status.HTTP_200_OK)
            return JsonResponse(data = {'message':'Bad Request'},status=status.HTTP_400_BAD_REQUEST)

class UsersRequests(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    renderer_classes = [TemplateHTMLRenderer,JSONRenderer]
    def post(self,request):
        usersrequests = FriendRequestList.objects.filter(receiver = User.objects.get(username__iexact = request.user.username))
        if bool(usersrequests):
            usersrequestsserializer = FriendRequestListSerializer(usersrequests,many=True)
            return JsonResponse(data = {'usersrequests':usersrequestsserializer.data,'anyrequests':bool(usersrequests)},status=status.HTTP_200_OK) 
        return JsonResponse(data = {'message':'No friend Requests','anyrequests':bool(usersrequests)},status=status.HTTP_200_OK)


class UserFriends(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    renderer_classes = [TemplateHTMLRenderer,JSONRenderer] 
    def get(self,request):
        user_friends = Friends.objects.get(user = User.objects.get(username__iexact = request.user.username))
        if bool(user_friends):
            user_friend_serializer = FriendsSerializer(user_friends)
            return JsonResponse(data = {'usersrequests':user_friend_serializer.data,'havefriends':bool(user_friends.friends.all())},status=status.HTTP_200_OK)
        return JsonResponse(data = {'message':'No Friends!','havefriends':bool(user_friends.friends.all())},status=status.HTTP_200_OK)