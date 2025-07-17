from django.shortcuts import render
from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Prefetch
from django_filters.rest_framework import DjangoFilterBackend

from .models import Project, ProjectCategory, ProjectCategoryImages
from .serializers import (
    ProjectSerializer,
    ProjectCategorySerializer,
    ProjectCategoryImageSerializer
)


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


class ProjectCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ProjectCategory.objects.all()
    serializer_class = ProjectCategorySerializer

    @action(detail=True, methods=['get'], url_path='images')
    def images(self, request, pk=None):
        images = ProjectCategoryImages.objects.filter(category_id=pk)
        serializer = ProjectCategoryImageSerializer(images, many=True, context={'request': request})
        return Response(serializer.data)


class ProjectCategoryImagesViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ProjectCategoryImages.objects.all()
    serializer_class = ProjectCategoryImageSerializer
