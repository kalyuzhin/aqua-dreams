from django.urls import path
from .views import CategoryListView, CategoryDetailView, ProductDetailView, ProductSearchView

urlpatterns = [
    path('', CategoryListView.as_view(), name='category-list'),
    path('<slug:slug>/', CategoryDetailView.as_view(), name='category-detail'),
    path('search/', ProductSearchView.as_view(), name='product-list'),  # Новый эндпоинт для списка продуктов с поиском и сортировкой
    path('<slug:category_slug>/<slug:product_slug>/', ProductDetailView.as_view(), name='product-detail'),
]
