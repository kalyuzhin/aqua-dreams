from django.urls import path
from .views import TermsPoolListView, TermsPoolDetailView

urlpatterns = [
    path('', TermsPoolListView.as_view(), name='terms-pool-list'),
    path('<slug:slug>/', TermsPoolDetailView.as_view(), name='terms-pool-detail'),
]
