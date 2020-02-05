from .models import Image
from rest_framework import serializers

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['caption', 'media', 'user', 'published_on']
