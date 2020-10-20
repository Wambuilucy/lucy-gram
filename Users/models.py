# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    
    profile_path = models.ImageField(upload_to = 'media/',default='profile_pics/prof.jpg')
    bio = models.TextField()
    user = models.OneToOneField(User,on_delete=models.CASCADE, primary_key=True)
    followers = models.ManyToManyField('Profile',related_name="followers_profile",blank=True)
    following = models.ManyToManyField('Profile',related_name="following_profile",blank=True)
    
    def get_number_of_followers(self):
        print(self.followers.count())
        if self.followers.count():
            return self.followers.count()
        else:
            return 0

    def get_number_of_following(self):
        if self.following.count():
            return self.following.count()
        else:
            return 0

    def __str__(self):
        return f'{self.user.username} Profile'

    @property
    def image(self):
        if self.profile_path and hasattr(self.profile_path, 'url'):
            return self.profile_path.url

    @classmethod
    def search_by_username(cls,search_term):
        search_result = cls.objects.filter(user__username__icontains=search_term)
        return search_result

    def save_profile(self):
        self.save()


