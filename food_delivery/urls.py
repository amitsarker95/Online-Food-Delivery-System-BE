from rest_framework_nested import routers
from django.urls import path, include
from . import views

router = routers.DefaultRouter()
router.register(r'restaurants', views.RestaurantViewSet, basename='restaurant')
router.register(r'orders', views.OrderViewSet, basename='order')

restaurants_router = routers.NestedDefaultRouter(router, r'restaurants', lookup='restaurant')
restaurants_router.register(r'menu-items', views.MenuItemViewSet, basename='restaurant-menu-items')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(restaurants_router.urls)),
]