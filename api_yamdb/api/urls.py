from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    CategoryViewSet,
    GenreViewSet,
    TitleViewSet,
)

CURRENT_API_VERSION = 'v1'

v1_router = DefaultRouter()
v1_router.register('titles', TitleViewSet, basename='title')
v1_router.register('genres', GenreViewSet, basename='genre')
v1_router.register('categories', CategoryViewSet, basename='category')

urlpatterns = [
    path(f'{CURRENT_API_VERSION}/', include(v1_router.urls)),
]
