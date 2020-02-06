from easy_thumbnails.files import get_thumbnailer

from .models import Image
from rest_framework import serializers

class ImageSerializer(serializers.ModelSerializer):
    thumbnail_url = serializers.SerializerMethodField('get_thumbnail_url')

    def get_thumbnail_url(self, obj):
        return get_thumbnailer(obj.media)['thumbnail'].url

    class Meta:

        model = Image
        fields = ['caption', 'media', 'thumbnail_url', 'user', 'published_on']

