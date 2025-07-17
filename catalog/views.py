from rest_framework import generics, filters
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer


class CategoryListView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'

    def get(self, request, *args, **kwargs):
        category = self.get_object()
        search_query = request.query_params.get('search', '').strip()

        products = category.products.all()

        if search_query:
            words = search_query.split()
            for word in words:
                products = products.filter(name__icontains=word)

        # Можно добавить сортировку по параметру ordering
        ordering = request.query_params.get('ordering')
        allowed_ordering = ['popularity', '-popularity', 'name', '-name']
        if ordering in allowed_ordering:
            products = products.order_by(ordering)
        else:
            products = products.order_by('popularity', 'name')

        products_serializer = ProductSerializer(products, many=True, context={'request': request})
        category_serializer = self.get_serializer(category)

        data = category_serializer.data
        data['products'] = products_serializer.data
        return Response(data)


class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProductSerializer
    lookup_field = 'slug'         # по какому полю ищем продукт
    lookup_url_kwarg = 'product_slug'  # параметр из URL

    def get_object(self):
        category_slug = self.kwargs['category_slug']
        product_slug = self.kwargs['product_slug']

        return get_object_or_404(
            Product,
            category__slug=category_slug,
            slug=product_slug
        )

    def get_queryset(self):
        category_slug = self.kwargs.get('category_slug')
        category = get_object_or_404(Category, slug=category_slug)
        return Product.objects.filter(category=category)


class ProductSearchView(generics.ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        query = self.request.query_params.get('search', '')
        qs = Product.objects.all()

        if not query:
            return qs  # Можно возвращать все продукты, или none() — по желанию

        words = query.split()
        for word in words:
            qs = qs.filter(name__icontains=word)

        # Добавим сортировку по параметру ordering из query params
        ordering = self.request.query_params.get('ordering', '')
        allowed_ordering = ['popularity', '-popularity', 'name', '-name']

        if ordering in allowed_ordering:
            qs = qs.order_by(ordering)
        else:
            # дефолтная сортировка
            qs = qs.order_by('popularity', 'name')

        return qs