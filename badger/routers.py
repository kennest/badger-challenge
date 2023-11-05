from .serializers import *
from rest_framework import viewsets, routers
from .models import User, Badge, UserBadge


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
