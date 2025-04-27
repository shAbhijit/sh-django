"""
URLS from the organizations app.
"""
from django.urls import (
    path,
    include
)
from rest_framework.routers import DefaultRouter
from organizations import views


router = DefaultRouter()
router.register('', views.OrganizationViewSet, basename='organization')

app_name = 'organizations'

urlpatterns = [
    path('', include(router.urls)),
]
