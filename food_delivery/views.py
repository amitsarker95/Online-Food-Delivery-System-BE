from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Restaurant, MenuItem, Order
from .serializers import (
    RestaurantSerializer, MenuItemSerializer, 
    OrderCreateSerializer, OrderDetailSerializer
)
from .permissions import IsRestaurantOwner, IsCustomer
from base.permissions import IsOwnerOrReadOnly

class RestaurantViewSet(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsRestaurantOwner]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        if self.request.user.is_restaurant:
            return Restaurant.objects.filter(owner=self.request.user)
        return Restaurant.objects.filter(is_active=True)

class MenuItemViewSet(viewsets.ModelViewSet):
    serializer_class = MenuItemSerializer
    permission_classes = [IsRestaurantOwner]

    def get_queryset(self):
        return MenuItem.objects.filter(restaurant_id=self.kwargs['restaurant_pk'])

    def perform_create(self, serializer):
        restaurant = Restaurant.objects.get(id=self.kwargs['restaurant_pk'])
        if restaurant.owner != self.request.user:
            raise permissions.PermissionDenied("You don't own this restaurant to add menu items.")
        serializer.save(restaurant=restaurant)

class OrderViewSet(viewsets.ModelViewSet):
    def get_permissions(self):
        if self.action in ['create', 'list', 'retrieve']:
            permission_classes = [IsCustomer]
        else:
            permission_classes = [IsRestaurantOwner]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.action == 'create':
            return OrderCreateSerializer
        return OrderDetailSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_customer:
            return Order.objects.filter(customer=user)
        elif user.is_restaurant:
            return Order.objects.filter(restaurant__owner=user)
        return Order.objects.none()

    @action(detail=True, methods=['post'])
    def update_status(self, request, pk=None):
        order = self.get_object()
        new_status = request.data.get('status')
        if new_status not in dict(Order.STATUS_CHOICES):
            return Response(
                {'error': 'Invalid status choice.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        order.status = new_status
        order.save()

