from datetime import timedelta

from rest_framework.exceptions import ValidationError


class EliminationChoiceValidator:
    """Валидатор, исключающий выбор связанной привычки
    и награды одновременно"""

    def __init__(self, associated_habit, reward):
        self.associated_habit = associated_habit
        self.reward = reward

    def __call__(self, habit):
        if habit.get(self.associated_habit) and habit.get(self.reward):
            raise ValidationError(
                "Выберите либо связанную привычку, либо вознаграждение."
            )


class TimeDurationValidator:
    """Валидатор, который проверяет, находится ли время на выполнение привычки в интервале 120 секунд"""

    def __init__(self, duration):
        self.duration = duration

    def __call__(self, habit):
        max_duration = timedelta(seconds=120)
        if (habit.get(self.duration)
                and habit.get(self.duration) > max_duration):
            raise ValidationError(
                f"Длительность выполнения привычки "
                f"не может превышать {max_duration}."
            )


class CombinationValidator:
    """Валидатор, который проверяет что, только привычка с признаком
    приятной привычки может попасть в связанные привычки"""

    def __init__(self, associated_habit, pleasant_habit):
        self.associated_habit = associated_habit
        self.pleasant_habit = pleasant_habit

    def __call__(self, habit):
        if (habit.get(self.associated_habit)
                and habit.get(self.pleasant_habit)):
            raise ValidationError(
                "В связанные привычки могут попадать только "
                "привычки с признаком приятной привычки."
            )


class PeriodicityValidator:
    """Проверка на выполнение привычки не реже чем раз в 7 дней"""

    def __init__(self, periodicity):
        self.periodicity = periodicity

    def __call__(self, habit):
        if habit.get(self.periodicity) and habit.get(self.periodicity) > 7:
            raise ValidationError("Нельзя выполнять привычку реже, "
                                  "чем 1 раз в 7 дней.")


class AbsenceValidator:
    """Валидатор указывает на то что, приятная привычка не может иметь вознаграждение или связанную привычку"""

    def __init__(self, reward, associated_habit, pleasant_habit):
        self.reward = reward
        self.associated_habit = associated_habit
        self.pleasant_habit = pleasant_habit

    def __call__(self, habit):
        if habit.get(self.pleasant_habit) and (
            habit.get(self.reward) or habit.get(self.associated_habit)
        ):
            raise ValidationError(
                "Приятная привычка не может иметь вознаграждение "
                "или связанную привычку."
            )
