from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.db.models import Count


# Custom User model inheriting from Django's AbstractUser.
class User(AbstractUser):
    pass  # No additional fields added to the default User model for now.


# Model to store profile information for each user.
class UserProfile(models.Model):
    # Subscription tiers for users.
    BRONZE = 'bronze'
    SILVER = 'silver'
    GOLD = 'gold'

    # Choices for subscription status.
    STATUS_CHOICES = [
        (BRONZE, 'Bronze'),
        (SILVER, 'Silver'),
        (GOLD, 'Gold'),
    ]

    # User profile is linked to a User object with a one-to-one relationship.
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # User's subscription status (bronze by default).
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=BRONZE)
    # Tracks the number of completed tasks by the user.
    tasks_completed = models.IntegerField(default=0)

    # Method to count the number of completed tasks.
    def completed_tasks_count(self):
        return self.tasks.filter(status=True).count()

    # Method to count the total number of tasks.
    def total_tasks_count(self):
        return self.tasks.count()

    # Method to calculate the percentage of completed tasks.
    def completion_percentage(self):
        total_tasks = self.total_tasks_count()
        completed_tasks = self.completed_tasks_count()
        if total_tasks > 0:
            return (completed_tasks / total_tasks) * 100
        return 0

    # Calculates how many consecutive days the user has been active (since last login).
    def consecutive_days_active(self):
        today = timezone.now().date()
        last_active_date = self.user.last_login.date() if self.user.last_login else None
        if last_active_date:
            consecutive_days = (today - last_active_date).days
            return max(consecutive_days, 0)
        return 0

    # Average time per task (if time tracking is implemented).
    def average_time_per_task(self):
        if self.tasks_completed > 0:
            average_time = self.tasks_completed_time / self.tasks_completed
            return f"{average_time:.1f} seconds"
        return "0.0 seconds"

    # Determines which day of the week the user was most active (completed the most tasks).
    def most_active_day_of_week(self):
        completed_tasks = self.tasks.filter(status=True)

        if not completed_tasks.exists():
            return None

        # Annotates tasks with their day of the week and counts how many were completed on each day.
        day_counts = (completed_tasks
                      .annotate(day_of_week=models.functions.ExtractWeekDay('created_at'))
                      .values('day_of_week')
                      .annotate(count=Count('id'))
                      .order_by('-count'))

        if day_counts:
            # Get the most active day of the week and adjust for Django's weekday numbering.
            max_day = day_counts[0]['day_of_week']
            max_day_corrected = max_day % 7 or 7
            today = timezone.now().date()
            today_day_of_week = today.weekday()
            days_difference = max_day_corrected - (today_day_of_week + 1)

            return today + timezone.timedelta(days=days_difference)

        return None


# Model to represent tasks associated with a user profile.
class TaskModel(models.Model):
    # Predefined categories for tasks.
    CATEGORY_CHOICES = [
        ('sport', 'Sport'),
        ('work', 'Work'),
        ('study', 'Study'),
        ('leisure', 'Leisure'),
        ('other', 'Other'),
    ]

    task = models.TextField()  # The task's description.
    status = models.BooleanField(default=False)  # Task completion status (True for completed).
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES)  # Task category.
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp when task was created.
    updated_at = models.DateTimeField(auto_now=True)  # Timestamp when task was last updated.
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='tasks')  # Task linked to user profile.


# Model representing categories (not used in the TaskModel).
class Category(models.Model):
    category = models.BooleanField(max_length=30)  # Unclear purpose, likely needs revision.
