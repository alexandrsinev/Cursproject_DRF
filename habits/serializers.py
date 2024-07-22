from rest_framework import serializers

from habits.models import Habits
from habits.validators import (
    EliminationChoiceValidator,
    TimeDurationValidator,
    CombinationValidator,
    AbsenceValidator,
    PeriodicityValidator,
)
from users.serializer import UserSerializer


class HabitsSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Habits
        fields = "__all__"
        validators = [
            EliminationChoiceValidator("associated_habit", "reward"),
            TimeDurationValidator("duration"),
            CombinationValidator("associated_habit", "pleasant_habit"),
            AbsenceValidator("reward", "associated_habit", "pleasant_habit"),
            PeriodicityValidator("periodicity"),
        ]
