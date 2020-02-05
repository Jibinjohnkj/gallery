from django.urls import path

from .views import ImageList, ImageDetails

urlpatterns = [
    path('<int:pk>/', ImageDetails.as_view()),
    path('', ImageList.as_view())
]