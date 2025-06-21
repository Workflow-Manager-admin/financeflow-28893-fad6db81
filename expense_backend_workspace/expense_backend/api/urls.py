from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    health,
    register,
    login_view,
    logout_view,
    ExpenseViewSet,
    CategoryViewSet,
    monthly_statistics,
)

router = DefaultRouter()
router.register(r'expenses', ExpenseViewSet, basename='expense')
router.register(r'categories', CategoryViewSet, basename='category')

urlpatterns = [
    path('health/', health, name='Health'),
    path('auth/register/', register, name='auth-register'),
    path('auth/login/', login_view, name='auth-login'),
    path('auth/logout/', logout_view, name='auth-logout'),
    path('statistics/monthly/', monthly_statistics, name='monthly-statistics'),
    path('', include(router.urls)),
]
