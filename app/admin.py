from django.contrib import admin

# Register your models here.

from .models import *

admin.register(Profile)
admin.register(Image)
admin.register(LikedImages)
