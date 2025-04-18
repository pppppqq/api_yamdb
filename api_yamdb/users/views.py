from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser

from .serializers import BaseUserSerializer

User = get_user_model()


class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = BaseUserSerializer
    permission_classes = (IsAdminUser,)
    lookup_field = 'username'
