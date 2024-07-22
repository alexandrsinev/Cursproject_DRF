from django.urls import path
from rest_framework.routers import DefaultRouter

from habits.apps import HabitsConfig
from habits.views import HabitsViewSet, HabitPublishedListAPIView

app_name = HabitsConfig.name

router = DefaultRouter()
router.register(r'habits', HabitsViewSet, basename='habits')


urlpatterns = [path(
        "habits_published/", HabitPublishedListAPIView.as_view(), name="habits_published",)
] + router.urls
