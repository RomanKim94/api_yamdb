from django.urls import include, path
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register('users', views.UserModelViewSet, basename='users')
router.register('users/me', views.ProfileModelViewSet, basename='profile')


urlpatterns = [
    path('', include(router.urls)),
    path('auth/token/', views.TokenApiView.as_view(), name='token'),
    path('auth/signup/', views.SignUpApiView.as_view(), name='signup'),
]
