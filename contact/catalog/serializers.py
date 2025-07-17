from django.utils.text import slugify
from rest_framework import serializers
from django.core.exceptions import ValidationError
from PIL import Image
import os
from .models import Category, Product, ProductImage, Specification


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug']
        read_only_fields = ['slug']

    def validate_name(self, value):
        if not value.strip():
            raise serializers.ValidationError("Category name cannot be empty.")
        return value.strip()

    def validate(self, data):
        # Автоматически создаём slug из имени, если его нет
        if 'name' in data and not data.get('slug'):
            data['slug'] = slugify(data['name'])

        # Проверяем уникальность slug
        if 'slug' in data:
            queryset = Category.objects.filter(slug=data['slug'])
            if self.instance:
                queryset = queryset.exclude(pk=self.instance.pk)
            if queryset.exists():
                raise serializers.ValidationError({'slug': 'Category with this slug already exists.'})

        return data


class SpecificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specification
        fields = ['id', 'key', 'value']

    def validate_key(self, value):
        if not value.strip():
            raise serializers.ValidationError("Key cannot be empty.")
        return value.strip()

    def validate_value(self, value):
        if not value.strip():
            raise serializers.ValidationError("Value cannot be empty.")
        return value.strip()


class ProductImageSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'image_url']

    def get_image_url(self, obj):
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
        return None

    def validate_image(self, value):
        if not value:
            raise serializers.ValidationError("Image file is required.")

        valid_extensions = ['.jpg', '.jpeg', '.png', '.webp']
        ext = os.path.splitext(value.name)[1].lower()
        if ext not in valid_extensions:
            raise serializers.ValidationError(
                f"Unsupported file extension. Supported extensions: {', '.join(valid_extensions)}"
            )

        try:
            img = Image.open(value)
            img.verify()
            value.seek(0)
        except Exception:
            raise serializers.ValidationError("Invalid image file. Please upload a valid image.")

        return value


class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, required=False)
    specifications = SpecificationSerializer(many=True, required=False)
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    image_url = serializers.SerializerMethodField()
    image_second_url = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id', 'category', 'name', 'slug', 'image', 'image_second', 'image_url', 'image_second_url', 'popularity',
            'reliability_text', 'special_notes', 'images', 'specifications'
        ]
        read_only_fields = ['slug', 'image_url', 'image_second_url']
        extra_kwargs = {
            'image': {'required': True},
            'image_second': {'required': False},
            'category': {'required': True}
        }

    def get_image_url(self, obj):
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
        return None

    def get_image_second_url(self, obj):
        if obj.image_second:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image_second.url)
        return None

    def validate_name(self, value):
        if not value.strip():
            raise serializers.ValidationError("Product name cannot be empty.")
        return value.strip()

    def validate_popularity(self, value):
        valid_choices = [0, 1, 2]
        if value not in valid_choices:
            raise serializers.ValidationError(f"Popularity must be one of {valid_choices}.")
        return value

    def validate(self, data):
        # Автоматически создаём slug из имени, если его нет
        if 'name' in data and not data.get('slug'):
            data['slug'] = slugify(data['name'])

        # Проверяем уникальность slug в рамках категории
        if 'slug' in data and 'category' in data:
            queryset = Product.objects.filter(slug=data['slug'], category=data['category'])
            if self.instance:
                queryset = queryset.exclude(pk=self.instance.pk)
            if queryset.exists():
                raise serializers.ValidationError({
                    'slug': 'Product with this slug already exists in this category.'
                })

        return data

    def create(self, validated_data):
        images_data = validated_data.pop('images', [])
        specs_data = validated_data.pop('specifications', [])
        product = Product.objects.create(**validated_data)

        for image_data in images_data:
            ProductImage.objects.create(product=product, **image_data)

        for spec_data in specs_data:
            Specification.objects.create(product=product, **spec_data)

        return product

    def update(self, instance, validated_data):
        images_data = validated_data.pop('images', None)
        specs_data = validated_data.pop('specifications', None)

        instance = super().update(instance, validated_data)

        if images_data is not None:
            instance.images.all().delete()
            for image_data in images_data:
                ProductImage.objects.create(product=instance, **image_data)

        if specs_data is not None:
            instance.specifications.all().delete()
            for spec_data in specs_data:
                Specification.objects.create(product=instance, **spec_data)

        return instance
