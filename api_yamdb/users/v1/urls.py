from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register('users', views.UserModelViewSet, basename='users')
router.register('users/me', views.ProfileModelViewSet, basename='profile')
