# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from project.server_util import empty_embed_vec, obj2pickled

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    pref_vec = models.TextField(default= obj2pickled(empty_embed_vec()))
    img_count = models.IntegerField(default=0)

    def __str__(self):
        return ' user: {} | preference vector: {}'.format(self.user,self.pref_vec)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class Image(models.Model):
    path = models.FilePathField(null=True,max_length=150)         # path to img file
    label = models.IntegerField(null=True)       # id of the image in simvec.np
    txt_vec = models.TextField(null=True)

    def __str__(self):
        return 'path: {} | label: {} | txt_vec: {}'.format(self.path,self.label,self.txt_vec)

class LikedImages(models.Model):
    user = models.ForeignKey('auth.User',default=None, related_name='likedImage',on_delete=models.CASCADE)
    img  = models.ForeignKey(Image, on_delete=models.DO_NOTHING)

    def __str__(self):
        return 'user : {} | img: {} '.format(self.user,self.img)
