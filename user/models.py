''' Create Model for Users'''

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.db.models import Count


class User(AbstractUser):
    pass


class UserProfile(models.Model):
    BRONZE = 'bronze'
    SILVER = 'silver'
    GOLD = 'gold'

    STATUS_CHOICES = [
        (BRONZE, 'Bronze'),
        (SILVER, 'Silver'),
        (GOLD, 'Gold'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=BRONZE)
    tasks_completed = models.IntegerField(default=0)

    def completed_tasks_count(self):
        print(self.tasks.filter(status=True).count())
        return self.tasks.filter(status=True).count()

    def total_tasks_count(self):
        return self.tasks.count()

    def completion_percentage(self):
        total_tasks = self.total_tasks_count()
        completed_tasks = self.completed_tasks_count()
        if total_tasks > 0:
            return (completed_tasks / total_tasks) * 100
        return 0

    def consecutive_days_active(self):
        today = timezone.now().date()
        last_active_date = self.user.last_login.date() if self.user.last_login else None
        if last_active_date:
            consecutive_days = (today - last_active_date).days
            return max(consecutive_days, 0)
        return 0

    def average_time_per_task(self):
        if self.tasks_completed > 0:
            average_time = self.tasks_completed_time / self.tasks_completed
            return f"{average_time:.1f} seconds"  # Форматирование времени
        return "0.0 seconds"

    def most_active_day_of_week(self):
        # Получаем все завершенные задачи
        completed_tasks = self.tasks.filter(status=True)

        if not completed_tasks.exists():
            return None

        # Группируем задачи по дню недели и считаем количество задач
        day_counts = (completed_tasks
                      .annotate(day_of_week=models.functions.ExtractWeekDay('created_at'))
                      .values('day_of_week')
                      .annotate(count=Count('id'))
                      .order_by('-count'))

        if day_counts:
            # Получаем номер дня недели с максимальным количеством задач
            max_day = day_counts[0]['day_of_week']
            # Преобразуем номер дня недели (1 = воскресенье, 7 = суббота) в дату
            # Поскольку ExtractWeekDay возвращает 1 для воскресенья, а 7 для субботы, нужно скорректировать
            max_day_corrected = max_day % 7 or 7  # 0 становится 7 для воскресенья

            # Находим текущую дату и получаем номер текущего дня
            today = timezone.now().date()
            today_day_of_week = today.weekday()  # 0 = понедельник, 6 = воскресенье

            # Находим дату для максимального дня активности
            days_difference = max_day_corrected - (today_day_of_week + 1)  # +1, чтобы совместить с ExtractWeekDay

            return today + timezone.timedelta(days=days_difference)

        return None


class TaskModel(models.Model):
    CATEGORY_CHOICES = [
        ('sport', 'Sport'),
        ('work', 'Work'),
        ('study', 'Study'),
        ('leisure', 'Leisure'),
        ('other', 'Other'),
    ]

    task = models.TextField()
    status = models.BooleanField(default=False)
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  # Добавлено
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='tasks')



class Category(models.Model):

    category = models.BooleanField(max_length=30)