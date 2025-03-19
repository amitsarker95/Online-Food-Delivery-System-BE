from djoser.serializers import UserCreateSerializer, UserSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomUserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ('id', 'email', 'password', 'first_name', 'last_name', 'phone_number',
                 'address', 'date_of_birth', 'profile_picture', 'is_customer',
                 'is_restaurant', 'is_delivery_person')


class CustomUserSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'phone_number',
                 'address', 'date_of_birth', 'profile_picture', 'is_customer',
                 'is_restaurant', 'is_delivery_person')
        read_only_fields = ('id', 'email')