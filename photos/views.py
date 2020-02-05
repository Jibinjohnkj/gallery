from .models import Image
from rest_framework import generics
from rest_framework.response import Response
from .serializers import ImageSerializer
from distutils.util import strtobool

class ImageList(generics.ListCreateAPIView):
    serializer_class = ImageSerializer

    def get_queryset(self):
        queryset = Image.objects.all()
        user_id = self.request.query_params.get('user_id', None)
        draft = self.request.query_params.get('draft', None)
        sort = self.request.query_params.get('sort', None)

        if user_id:
            queryset = queryset.filter(user__id=user_id)
        if draft:
            queryset = queryset.filter(published_on__isnull=strtobool(draft))
        if sort:
            queryset = queryset.order_by(sort)
        return queryset

    def list(self, request):
        queryset = self.get_queryset()
        serializer = ImageSerializer(queryset, many=True)
        return Response(serializer.data)


class ImageDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
