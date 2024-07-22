from datetime import timedelta

from django.db import models

from config import settings

NULLABLE = {'blank': True, 'null': True}


class Habits(models.Model):
    habit_title = models.CharField(max_length=100, verbose_name='Название привычки')
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Хозяин привычки', **NULLABLE)
    location = models.CharField(max_length=250, verbose_name='Место где выполняется привычка')
    time_perform = models.DateTimeField(verbose_name='Время выполнения привычки')
    action = models.CharField(max_length=300, verbose_name='Какие действия надо выполнить')
    pleasant_habit = models.BooleanField(verbose_name="Это приятная привычка", default=False, )
    associated_habit = models.ForeignKey("self", on_delete=models.CASCADE, verbose_name="Связанная привычка",
                                         **NULLABLE)
    reward = models.CharField(max_length=300, verbose_name='Вознаграждение', **NULLABLE)
    periodicity = models.SmallIntegerField(default=1, verbose_name="Периодичность выполнения привычки",
                                           help_text="Укажите периодичность от 1 до 7, "
                                                     "где 1 - один раз в неделю, а 7 - это каждый день.",
                                           )
    duration = models.DurationField(verbose_name='Время на выполнение привычки', default=timedelta(seconds=120))
    is_published = models.BooleanField(default=False, verbose_name='статус публикации')

    def __str__(self):
        return f'{self.habit_title}'

    class Meta:
        verbose_name = 'Привычка'
        verbose_name_plural = 'Привычки'
