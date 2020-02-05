from io import BytesIO
import sys

import PIL

from django.contrib.auth.models import User
from django.core.files.uploadedfile import InMemoryUploadedFile
from rest_framework.test import APITestCase
from django.conf import settings
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework.test import APIRequestFactory, force_authenticate

from .models import Image
from .views import ImageList, ImageDetails

def create_image(name, type=None):
    image = BytesIO()
    image.name = name
    PIL.Image.new('RGB', (100, 100)).save(image, 'PNG')
    image.seek(0)
    if type == 'InMemoryUploadedFile':
        image = InMemoryUploadedFile(image,
                                     'ImageField',
                                     name,
                                     'image/png',
                                     sys.getsizeof(image),
                                     None)
    return image

class ImageListTest(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create_user(
            username='jibin', email='jibin@gmail.com', password='jibin@123')
        self.image = Image.objects.create(
            caption='A beautiful tree',
            media=create_image('tree.jpg','InMemoryUploadedFile'),
            user=self.user)

    def get_token(self):
        'POST -d "username=jibin&password=jibin@123" http://localhost:8000/api-token-auth/'
        data = {
            "username": self.user.username,
            "password": "jibin@123",
            }
        request = self.factory.post('/api-token-auth/', data)
        request.user = self.user
        response = obtain_jwt_token(request)
        self.assertEqual(response.status_code, 200)
        self.token = response.data.get('token')

    def test_post(self):
        data = {
            "caption": "A beautiful mountain",
            "media": create_image('mountain.jpg'),
            "user": self.user.id
            }
        request = self.factory.post('/api/photos/', data)
        request.user = self.user
        response = ImageList.as_view()(request)
        self.assertEqual(response.status_code, 201)
        self.assertTrue(Image.objects.filter(caption="A beautiful mountain").exists())

    def test_get(self):
        request = self.factory.get('/api/photos/<int:pk>/', pk=self.image.id)
        request.user = self.user
        response = ImageDetails.as_view()(request, pk=self.image.id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['caption'], "A beautiful tree")

    def test_update(self):
        data = {
            "caption": "A wonderful tree"
            }
        request = self.factory.patch('/api/photos/<int:pk>/', data)
        request.user = self.user
        response = ImageDetails.as_view()(request, pk=self.image.id)
        self.assertEqual(response.status_code, 200)
        self.image.refresh_from_db()
        self.assertEqual(self.image.caption, "A wonderful tree")

    def test_delete(self):
        request = self.factory.delete('/api/photos/<int:pk>/')
        request.user = self.user
        response = ImageDetails.as_view()(request, pk=self.image.id)
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Image.objects.filter(id=self.image.id).exists())

    def test_list(self):
        request = self.factory.get('/api/photos/')
        request.user = self.user
        response = ImageList.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response)

    def test_jwt_authentication(self):
        self.get_token()
        request = self.factory.get('/api/photos/<int:pk>/', pk=self.image.id, HTTP_AUTHORIZATION='JWT {}'.format(self.token))
        force_authenticate(request)
        response = ImageDetails.as_view()(request, pk=self.image.id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['caption'], "A beautiful tree")

