from django.contrib import admin
from .models import Image

class ImageAdmin(admin.ModelAdmin):
    search_fields = ('id','caption','published_on')
    list_display = ('id','caption','published_on')

admin.site.register(Image,ImageAdmin)