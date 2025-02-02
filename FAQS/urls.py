from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FAQViewSet,FAQSViews,FaqsEditViews

router = DefaultRouter()
router.register(r'faqs', FAQViewSet, basename='faqs')  

urlpatterns = [
    path('',FAQSViews),
    path('edit/',FaqsEditViews,name='faq-edit'),
    path('api/', include(router.urls)),
]
