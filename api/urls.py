from django.urls import path, include
from rest_framework.routers import DefaultRouter
from FAQS.views import FAQViewSet

router = DefaultRouter()
router.register(r'faqs', FAQViewSet, basename='faqs')  

urlpatterns = [
    path('', include(router.urls)),
]
