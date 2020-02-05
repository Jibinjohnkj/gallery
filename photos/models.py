from django.db import models
from django.contrib.auth.models import User

class Image(models.Model):
    """A model of a Image."""
    caption = models.TextField()
    media = models.ImageField(upload_to='uploads/%Y/%m/%d/')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # if published_on is null, this is a draft
    published_on = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.caption
