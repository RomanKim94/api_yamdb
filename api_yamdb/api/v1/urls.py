from django.urls import include, path

from users.v1.urls import router as users_router_v1


urlpatterns = [
    path('v1/', include(users_router_v1.urls)),
]
