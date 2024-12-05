from rest_framework.routers import SimpleRouter
from django.urls import include, path

from . import views

router_v1 = SimpleRouter()
router_v1.register('users', views.UserModelViewSet, basename='users')
router_v1.register('categories', views.CategoryViewSet, basename='categories')
router_v1.register('genres', views.GenreViewSet, basename='genres')
router_v1.register('titles', views.TitleViewSet, basename='titles')
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    views.CommentViewSet, basename='comments',
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    views.ReviewViewSet, basename='reviews',
)

app_name = 'api'
urlpatterns = [
    path('v1/', include([
        path('', include(router_v1.urls)),
        path('auth/', include([
            path('token/', views.get_token_api_view, name='token'),
            path('signup/', views.signup_api_view, name='signup'),
        ])),
    ])),
]