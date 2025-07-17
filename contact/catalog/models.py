from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    POPULARITY_CHOICES = [
        (0, 'Низкая'),
        (1, 'Средняя'),
        (2, 'Высокая'),
    ]

    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    reliability_text = models.TextField()
    special_notes = models.TextField()
    image = models.ImageField(upload_to='products/')
    image_second = models.ImageField(upload_to='products/', blank=True, null=True)
    popularity = models.PositiveIntegerField(choices=POPULARITY_CHOICES, default=1)

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/')


class Specification(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='specifications')
    key = models.CharField(max_length=100)
    value = models.CharField(max_length=100)