from django.urls import path
from .views import *


urlpatterns = [
    #path('',Get_Api_Key.as_view(),name="people_code"),
    path('',People.as_view(),name="people"),
    path('searchfriends/',FindPeople.as_view(),name="findpeople"),
    path('sendrequest/',FriendRequest.as_view(),name="friendrequest"),
    path('usersrequests/',UsersRequests.as_view(),name="usersrequests"),
    path('userfriends/',UserFriends.as_view(),name="getuserfriends"),
    
]