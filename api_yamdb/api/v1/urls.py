from rest_framework.routers import SimpleRouter
from django.urls import path, include

from .views import ReviewViewSet, CommentViewSet

router_v1 = SimpleRouter()
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comments',
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet, basename='reviews',
)

urlpatterns = [
    path('v1/', include(router_v1.urls)),
]
