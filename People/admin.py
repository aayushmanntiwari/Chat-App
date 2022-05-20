from django.contrib import admin
from .models import Friends,FriendRequestList

class FriendsAdmin(admin.ModelAdmin):
    list_display = ['user']
    search_fields = ['user__username']
    list_filter = ['user']
    readonly_field = ['user']
class FriendRequestAdmin(admin.ModelAdmin):
    list_display = ['sender','receiver']
    search_fields = ['sender__username','receiver__username']
    readonly_field = ['sender','receiver']

# Register your models here.
admin.site.register(Friends,FriendsAdmin)
admin.site.register(FriendRequestList,FriendRequestAdmin)