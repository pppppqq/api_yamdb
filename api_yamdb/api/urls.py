from rest_framework.routers import DefaultRouter
from django.urls import include, path

from .views import CommentViewSet, ReviewViewSet

router_v1 = DefaultRouter()
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet, basename='review'
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comment'
)
urlpatterns = [
    path('', include(router_v1.urls)),
]
from rest_framework.routers import DefaultRouter
from django.urls import include, path

from jwt_auth.views import SignUpView, TokenByCodeView
from users.views import UserViewSet


app_name = 'api'

v1_router = DefaultRouter()
v1_router.register('users', UserViewSet, basename='user')

urlpatterns = [
    path('v1/auth/signup/', SignUpView.as_view(), name='signup'),
    path('v1/auth/token/', TokenByCodeView.as_view(), name='token'),
    path('v1/', include(v1_router.urls))
]
