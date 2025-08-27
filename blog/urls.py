from django.urls import path, include
from rest_framework import routers
from .views import PostViewSet, RegisterAPIView, LoginAPIView

router = routers.DefaultRouter()
router.register(r'posts', PostViewSet, basename='post')

urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('login/', LoginAPIView.as_view(), name='login'),
]
