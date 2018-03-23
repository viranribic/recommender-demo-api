"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url,include
from rest_framework_jwt.views import obtain_jwt_token,verify_jwt_token
from django.conf import settings
from django.views.static import serve
from django.conf.urls.static import  static
from app import views

urlpatterns = [
    url(r'^$', views.HomePageView.as_view()),
    path('admin/', admin.site.urls),
    url(r'^api-auth/', include('rest_framework.urls')),
    url(r'^api-token-auth/', obtain_jwt_token),
    url(r'^api-token-verify/', verify_jwt_token),
    url(r'^api/', include('app.urls'))
]

# Access local media root during development only
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # # Use this if you need a filesys interface in browser. Otherwise just serve files like above.
    # urlpatterns += [
    #     url(r'^media/(?P<path>.*)$',
    #         serve,
    #         {
    #             'document_root': settings.MEDIA_ROOT,
    #             'show_indexes':True}
    #         )]
