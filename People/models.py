
from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Friends(models.Model):
    friends = models.ManyToManyField(User,blank=True,related_name='friends')
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='user')

    def __str__(self) -> str:
        return self.user.username

    
    def add_friend(self,account):
        '''Add a new friend in the friends'''
        if account not in self.friends.all():
            self.friends.add(account)
            return True
        else:
            return False
    
    def remove_friend(self,account):
        '''Remove a friend in the friends'''
        if account in self.friends.all():
            self.friends.remove(account)

    def unfriend(self,removee):
        '''Can we initated by any of friend if both are friends'''
        self.remove_friend(removee)
        other = Friends.objects.get(user = removee)
        other.remove_friend(self.user)

class FriendRequestList(models.Model):
    sender = models.ForeignKey(User,on_delete=models.CASCADE,related_name='sender')
    receiver = models.ForeignKey(User,on_delete=models.CASCADE,related_name='reciver')
    status = models.BooleanField(default=True)
    date_time = models.DateTimeField(auto_now_add=True, blank=True)

    def accpet(self):
        '''when receiver accpeted the sender request'''
        for_receiver,create = Friends.objects.get(user = self.receiver)
        if for_receiver is not None:
            for_receiver.add_friend(self.sender)
            for_sender = Friends.objects.get(user = self.receiver)
            if for_sender:
                for_sender.add_friend(self.receiver)
                self.status = False
                self.save()

    def cancel(self):
        '''when sender want to cancel the sent request'''
        self.status = False
        self.save()

