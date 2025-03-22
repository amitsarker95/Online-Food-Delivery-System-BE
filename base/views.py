from django.shortcuts import render
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .serializers import CustomUserSerializer, PublicUserSerializer
from .permissions import IsUserOrAdmin

User = get_user_model()

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsUserOrAdmin]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            user_id = int(self.kwargs['pk'])
            if user_id == self.request.user.id or self.request.user.is_staff:
                return CustomUserSerializer
            return PublicUserSerializer
        if self.action == 'list':
            return PublicUserSerializer
        return CustomUserSerializer

    def get_queryset(self):
        queryset = User.objects.all()
        if not self.request.user.is_staff:
            queryset = queryset.filter(is_staff=False)
        return queryset

    def destroy(self, request, *args, **kwargs):
        user = self.get_object()
        if user != request.user and not request.user.is_staff:
            return Response(
                {"detail": "You do not have permission to delete this user."},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().destroy(request, *args, **kwargs)
