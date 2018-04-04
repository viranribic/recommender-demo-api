from django.contrib.auth.models import User
from rest_framework import serializers
from app.models import Image

class UserSerializer(serializers.ModelSerializer):
    snippets = serializers.HyperlinkedRelatedField(many=True, view_name='snippet-detail', read_only=True)

    class Meta:
        model = User
        fields = ('url','id', 'username', 'snippets')

class ProfileSerializer(serializers.ModelSerializer):
    pref_vec = serializers.CharField(source='user.pref_vec') # works for TextField as well
    img_count = serializers.CharField(source='user.img_count') # works for TextField as well

    class Meta:
        model = User
        fields = ('id', 'username', 'pref_vec', 'img_count')

class ImageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Image
        fields = ('id','path','label')
        ordering = ('id',)

class LikedImageSerializer(serializers.HyperlinkedModelSerializer):
    liked = serializers.SerializerMethodField('liked_init')

    @staticmethod
    def liked_init(obj):
        return True

    class Meta:
        model = Image
        fields = ('id', 'path', 'label', 'liked')
        ordering = ('id',)

class UnlikedImageSerializer(serializers.HyperlinkedModelSerializer):
    liked = serializers.SerializerMethodField('liked_init')

    @staticmethod
    def liked_init(obj):
        return False

    class Meta:
        model = Image
        fields = ('id', 'path', 'label', 'liked')
        ordering = ('-id',)
