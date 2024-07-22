from datetime import datetime, timedelta

import pytz
from celery import shared_task

from config import settings
from habits.models import Habits
from habits.services import send_telegram_message
from users.models import User


@shared_task
def send_remainder():
    """Отправляет в телеграмм сообщение в какое время какие привычки надо выполнить"""
    habits = Habits.objects.all()
    users = User.objects.all()
    for user in users:
        if user.tg_chat_id:
            for habit in habits:
                habit_start_time = habit.time_perform.replace(second=0, microsecond=0)
                habit_time_now = datetime.now(
                    pytz.timezone(settings.TIME_ZONE)
                ).replace(second=0, microsecond=0)
                if habit_start_time == habit_time_now:
                    if habit.pleasant_habit:
                        send_telegram_message(
                            habit.user.tg_chat_id,
                            f"Сегодня ты хотел: {habit.action}, "
                            f"время выполнения: {habit.duration} минуты.",
                        )
                    if habit.associated_habit:
                        send_telegram_message(
                            habit.user.tg_chat_id,
                            f"Сегодня ты хотел: {habit.action}, "
                            f"время выполнения: {habit.duration} минуты, "
                            f"когда закончишь можешь: {habit.associated_habit}.",
                        )
                    if habit.reward:
                        send_telegram_message(
                            habit.user.tg_chat_id,
                            f"Сегодня ты хотел: {habit.action}, "
                            f"время выполнения: {habit.duration} минуты, "
                            f"когда закончишь наградой будет: {habit.reward}.",
                        )
                    habit.time_perform = datetime.now(
                        pytz.timezone(settings.TIME_ZONE)
                    ) + timedelta(days=habit.periodicity)
                    habit.save()
