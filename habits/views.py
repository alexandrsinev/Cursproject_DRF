from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from habits.models import Habits
from habits.paginators import HabitPagination
from habits.serializers import HabitsSerializer
from users.permissoins import IsOwner


class HabitsViewSet(viewsets.ModelViewSet):
    queryset = Habits.objects.all()
    serializer_class = HabitsSerializer
    pagination_class = HabitPagination
    permission_classes = [IsAuthenticated, IsOwner]

    def perform_create(self, serializer):
        habit = serializer.save()
        habit.user = self.request.user
        habit.save()

    def get_queryset(self):
        """Отображает список привычек созданных пользователем"""
        user = self.request.user
        return Habits.objects.filter(user=user)

    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = [IsAuthenticated]
        if self.action in ['update', 'partial_update', 'retrieve', 'destroy']:
            self.permission_classes = [IsAuthenticated, IsOwner]
        return super().get_permissions()


class HabitPublishedListAPIView(ListAPIView):
    serializer_class = HabitsSerializer
    pagination_class = HabitPagination

    def get_queryset(self):
        """Отображает список опубликованных привычек"""
        return Habits.objects.filter(is_published=True)
