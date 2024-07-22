from django.contrib import admin

from habits.models import Habits


@admin.register(Habits)
class HabitsAdmin(admin.ModelAdmin):
    list_display = ('id', 'habit_title', 'location', 'action', 'is_published')
