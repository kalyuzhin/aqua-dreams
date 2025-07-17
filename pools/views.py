from rest_framework import generics
from .models import Pool
from .serializers import PoolListSerializer, PoolDetailSerializer

class PoolListView(generics.ListCreateAPIView):
    queryset = Pool.objects.all().prefetch_related('description_obj', 'images')
    serializer_class = PoolListSerializer

class PoolDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Pool.objects.all().prefetch_related('description_obj', 'images')
    serializer_class = PoolDetailSerializer
    lookup_field = 'slug'
