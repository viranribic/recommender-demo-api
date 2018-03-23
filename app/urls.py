from django.conf.urls import url
from rest_framework import renderers

from . import views
from rest_framework.urlpatterns import format_suffix_patterns
from app.views import ImageViewSet, LikedImageViewSet, RecommendedImageViewSet, RandomImageViewSet
from app.views import UserRegister,ImageLike

image_list = ImageViewSet.as_view({
    'get':'list',
})

random_image_list = RandomImageViewSet.as_view({
    'get':'list',
})


image_recommended_list = RecommendedImageViewSet.as_view({
    'get':'list',
})

image_liked_list = LikedImageViewSet.as_view({
    'get':'list',
})

urlpatterns =[
    url(r'^image/random/$', random_image_list, name='random-image-list'),
    url(r'^image/recommended/$', image_recommended_list,name='image-details'),
    url(r'^image/liked/$', image_liked_list, name='image-details'),
    url(r'^image/like/$', ImageLike.as_view(), name='like-action'),
    # TODO add email verification and finish signup
    #url(r'^register/$', UserRegister.as_view(), name='register'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
