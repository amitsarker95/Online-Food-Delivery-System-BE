from rest_framework import serializers
from .models import Restaurant, MenuItem, Order, OrderItem

class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = ['id', 'name', 'description', 'price', 'is_available']

class RestaurantSerializer(serializers.ModelSerializer):
    menu_items = MenuItemSerializer(many=True, read_only=True)
    
    class Meta:
        model = Restaurant
        fields = ['id', 'name', 'description', 'address', 'phone_number', 'is_active', 'menu_items']
        read_only_fields = ['owner']

    def create(self, validated_data):
        validated_data['owner'] = self.context['request'].user
        return super().create(validated_data)

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id', 'menu_item', 'quantity', 'price']

class OrderCreateSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'restaurant', 'delivery_address', 'items']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        # Calculate total amount
        total_amount = sum(
            item['menu_item'].price * item['quantity']
            for item in items_data
        )
        
        # Create order
        order = Order.objects.create(
            customer=self.context['request'].user,
            total_amount=total_amount,
            **validated_data
        )

        # Create order items
        for item_data in items_data:
            OrderItem.objects.create(
                order=order,
                price=item_data['menu_item'].price,
                **item_data
            )

        return order

class OrderDetailSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    
    class Meta:
        model = Order
        fields = ['id', 'restaurant', 'status', 'total_amount', 'delivery_address', 
                 'items', 'created_at', 'updated_at']