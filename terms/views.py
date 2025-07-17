from rest_framework import generics
from .models import TermsPool
from .serializers import TermsPoolListSerializer, TermsPoolDetailSerializer


class TermsPoolListView(generics.ListCreateAPIView):
    queryset = TermsPool.objects.all().prefetch_related('description_obj', 'images')
    serializer_class = TermsPoolListSerializer


class TermsPoolDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = TermsPool.objects.all().prefetch_related('description_obj', 'images')
    serializer_class = TermsPoolDetailSerializer
    lookup_field = 'slug'
