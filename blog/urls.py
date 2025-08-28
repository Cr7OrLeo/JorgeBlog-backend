from django.urls import path, include
from rest_framework import routers
from .views import PostViewSet, RegisterAPIView, LoginAPIView, check_login
from .views import verify_email

router = routers.DefaultRouter()
router.register(r'posts', PostViewSet, basename='post')

urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('check_login/', check_login),
    path('verify_email/', verify_email),
]
