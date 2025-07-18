# serializers.py
from rest_framework import serializers
from .models import Project, ProjectDetail, ProjectCategory, ProjectCategoryImages


class ProjectDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectDetail
        fields = ['text']


class ProjectSerializer(serializers.ModelSerializer):
    details = ProjectDetailSerializer(many=True, read_only=True)
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = ['id', 'title', 'address', 'description', 'image', 'image_url', 'is_flipped', 'details']

    def get_image_url(self, obj):
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
        return None


class ProjectCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectCategory
        fields = ['id', 'name', 'description', 'created_at', 'updated_at']


class ProjectCategoryImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectCategoryImages
        fields = ['id', 'image', 'category']
