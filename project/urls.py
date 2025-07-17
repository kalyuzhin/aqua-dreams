from rest_framework.routers import DefaultRouter
from .views import ProjectViewSet, ProjectCategoryViewSet, ProjectCategoryImagesViewSet

router = DefaultRouter()
router.register('projects', ProjectViewSet)
router.register(r'category', ProjectCategoryViewSet)
router.register(r'category-images', ProjectCategoryImagesViewSet)
urlpatterns = router.urls
