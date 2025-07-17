from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve  # Добавляем для продакшена
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView

schema_view = get_schema_view(
   openapi.Info(
      title="Aqua Dreams Documentation",
      default_version='v1',
      description="Описание API",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@myproject.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path(settings.ADMIN_URL, admin.site.urls),  
    
    path('api/project/', include('project.urls')),
    path('api/catalog/', include('catalog.urls')),
    path('api/pools/', include('pools.urls')),
    path('api/terms/', include('terms.urls')),
    path('api/contact/', include('contact.urls')),

    
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

if settings.DEBUG:
    print("DEBUG mode is ON")
    print("STATIC_URL:", settings.STATIC_URL)
    print("STATIC_ROOT:", settings.STATIC_ROOT)
    print("MEDIA_URL:", settings.MEDIA_URL)
    print("MEDIA_ROOT:", settings.MEDIA_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
else:
    print("DEBUG mode is OFF")
    print("Static files should be served by web server")
    print("STATIC_ROOT:", settings.STATIC_ROOT)
    print("STATIC_URL:", settings.STATIC_URL)
    print("Current urlpatterns:", urlpatterns)
    
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    print("Added static files handling")
    print("Updated urlpatterns:", urlpatterns)

    
    urlpatterns += [
        re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
        re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    ]
