from rest_framework import permissions, viewsets
from rest_framework.permissions import SAFE_METHODS
from .permissions import IsAdminOrSuperuser


class ReadOnlyOrAdminPermissionMixin(viewsets.ModelViewSet):
    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return (permissions.AllowAny(),)
        return (permissions.IsAuthenticated(), IsAdminOrSuperuser(),)
