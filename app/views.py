# Create your views here.

# Common imports
from django.shortcuts import render
from django.views.generic import TemplateView
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView

# Models and serialiezrs
from app.serializers import UnlikedImageSerializer, LikedImageSerializer
from django.contrib.auth.models import User
from app.models import Image, LikedImages, Profile
from app.serializers import ImageSerializer

from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from app.serializers import ProfileSerializer

# Task specific imports
# TODO move these to a seperate module
import pickle as pckl
import numpy as np
import codecs
from project.project_config import GALLERY_IMG_NUM

def obj2pickled(obj):
    return codecs.encode(pckl.dumps(obj), "base64").decode()

def pickled2obj(pickled):
    return pckl.loads(codecs.decode(pickled.encode(), "base64"))

class ImageViewSet(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    authentication_classes = (JSONWebTokenAuthentication,SessionAuthentication,BasicAuthentication)

class RandomImageViewSet(viewsets.ModelViewSet):
    serializer_class = UnlikedImageSerializer
    authentication_classes = (JSONWebTokenAuthentication,SessionAuthentication,BasicAuthentication)

    def get_queryset(self):
        user = self.request.user
        return Image.objects.exclude(id__in = LikedImages.objects.filter(user=user).values_list('img', flat=True))

class LikedImageViewSet(viewsets.ModelViewSet):
    serializer_class = LikedImageSerializer
    authentication_classes = (JSONWebTokenAuthentication,SessionAuthentication,BasicAuthentication)

    def get_queryset(self):
        user = self.request.user
        return Image.objects.filter(id__in = LikedImages.objects.filter(user=user).values_list('img', flat=True))

class RecommendedImageViewSet(viewsets.ModelViewSet):
    serializer_class = UnlikedImageSerializer
    authentication_classes = (JSONWebTokenAuthentication,SessionAuthentication,BasicAuthentication)

    def get_queryset(self):
        user = self.request.user
        images = Image.objects.all().exclude(id__in=LikedImages.objects.filter(user=user).values_list('img', flat=True))
        if len(images) == 0:
            return images

        profile = Profile.objects.filter(user_id=user.id).first()

        pref_vec = pickled2obj(profile.pref_vec)
        sim = []
        for img in images:
            img_vec = pickled2obj(img.txt_vec)
            similarity = np.arccos(np.dot(img_vec, pref_vec) / (np.linalg.norm(img_vec) * np.linalg.norm(pref_vec)))
            sim.append((img.id, similarity))

        sim.sort(key=lambda tup: tup[1])
        indices = map(lambda rec: rec[0], sim[:GALLERY_IMG_NUM])

        return Image.objects.filter(id__in = indices)

class ProfileViewSet(viewsets.ReadOnlyModelViewSet):
    # TODO restrict user acces with permissions
    queryset = User.objects.all()
    serializer_class = ProfileSerializer
    authentication_classes = (JSONWebTokenAuthentication,SessionAuthentication,BasicAuthentication)

class UserRegister(APIView):

    def post(self, request, format=None):
        if 'username' in request.data and 'email' in request.data and 'password' in request.data :
            user = User.objects.create_user(username=request.data['username'],
                                            email=request.data['email'],
                                            password=request.data['password'])
            return Response({'message':'User created.'}, status=status.HTTP_201_CREATED)
        return Response({'message':'Missing data. Provide "username", "email" and "password".'}, status=status.HTTP_400_BAD_REQUEST)

class ImageLike(APIView):
    authentication_classes = (JSONWebTokenAuthentication,SessionAuthentication,BasicAuthentication)

    def post(self, request, format=None):

        if 'like' in request.data and 'id' in request.data:
            like = request.data['like']
            img_id = request.data['id']
            user = request.user

            query_res = LikedImages.objects.filter(user=user.id, img=img_id)
            if like:
                # Add the image to list if it's not there yet
                if len(query_res) is 0:
                    image = Image.objects.filter(id=img_id).first()

                    # update user preferences
                    profile = Profile.objects.filter(user_id=user.id).first()
                    profile_vec = pickled2obj(profile.pref_vec)
                    img_vec     = pickled2obj(image.txt_vec)

                    profile_vec = ((profile_vec * profile.img_count) + img_vec) / (profile.img_count + 1 )
                    profile.img_count += 1
                    profile.pref_vec = obj2pickled(profile_vec)
                    profile.save()

                    # save like
                    li = LikedImages(user=user, img=image)
                    li.save()

            else:
                if len(query_res) is 1:
                    result = query_res.first()

                    # update user preferences
                    profile = Profile.objects.filter(user_id=user.id).first()
                    profile_vec = pickled2obj(profile.pref_vec)
                    img_vec = pickled2obj(result.img.txt_vec)

                    profile_vec = ((profile_vec * profile.img_count) - img_vec)
                    profile_vec = profile_vec if profile.img_count == 1 else profile_vec / (profile.img_count - 1)
                    profile.img_count -= 1
                    profile.pref_vec = obj2pickled(profile_vec)
                    profile.save()

                    result.delete()

            return Response({'message':'Like recorded successfuly.'}, status=status.HTTP_201_CREATED)
        return Response({'message':'Missing data. Provide "like" flag and image "id".'}, status=status.HTTP_400_BAD_REQUEST)

class HomePageView(TemplateView):
    def get(self, request, **kwargs):
        return render(request, 'index.html', context=None)





