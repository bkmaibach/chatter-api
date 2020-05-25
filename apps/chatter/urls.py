# chatter/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r'rooms', views.RoomViewSet)

app_name = 'chatter'

urlpatterns = [
    path('', include(router.urls)),
]