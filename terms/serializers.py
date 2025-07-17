from rest_framework import serializers
from .models import TermsPool, TermsPoolImage, TermsPoolDescription


class TermsPoolImageSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = TermsPoolImage
        fields = ['id', 'image_url']

    def get_image_url(self, obj):
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
        return None


class TermsPoolListSerializer(serializers.ModelSerializer):
    main_image_url = serializers.SerializerMethodField()

    class Meta:
        model = TermsPool
        fields = ['id', 'name', 'description_short', 'main_image_url', 'slug']

    def get_main_image_url(self, obj):
        if obj.main_image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.main_image.url)
        return None


class TermsPoolDetailSerializer(serializers.ModelSerializer):
    images = TermsPoolImageSerializer(many=True, read_only=True)
    description = serializers.SerializerMethodField()
    main_image_url = serializers.SerializerMethodField()

    class Meta:
        model = TermsPool
        fields = [
            'id', 'name', 'description_short', 'description',
            'slug', 'main_image_url', 'images'
        ]

    def get_description(self, obj):
        if hasattr(obj, 'description_obj'):
            return obj.description_obj.description
        return None

    def get_main_image_url(self, obj):
        if obj.main_image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.main_image.url)
        return None
