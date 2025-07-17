from django.urls import path
from .views import PoolListView, PoolDetailView

urlpatterns = [
    path('', PoolListView.as_view(), name='pool-list'),
    path('<slug:slug>/', PoolDetailView.as_view(), name='pool-detail'),
]