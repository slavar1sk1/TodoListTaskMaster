from django.http import HttpResponseForbidden
from .forms import LoginForm, RegistrationForm
from django.views.generic.edit import CreateView
from django.contrib.auth.views import LoginView
from .models import User, UserProfile
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from subscriptions.mixins import GoldSubscriptionRequiredMixin

# List of public views and classes that can be imported and used in other parts of the application.
__all__ = ['RegistrationView', 'LoginUserView', 'home', 'subscriptions', 'profile', 'StatisticsView', 'buy_gold']


class RegistrationView(CreateView):
    """
    This view handles the user registration process.
    - Uses the RegistrationForm to create a new user.
    - After creating the user, it also creates a UserProfile with the default subscription status of 'bronze'.
    - Automatically logs in the newly registered user and redirects them to the task list page.
    """
    model = User
    template_name = 'registration.html'  # Template for rendering the registration form.
    form_class = RegistrationForm
    success_url = '/task_list'  # Redirects the user to the task list after successful registration.

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        response = super().form_valid(form)
        # Create a UserProfile for the newly registered user with a 'bronze' status.
        UserProfile.objects.create(user=self.object, status=UserProfile.BRONZE)
        # Automatically log in the new user.
        login(self.request, self.object)
        return response


class LoginUserView(LoginView):
    """
    Handles user login using Django's built-in LoginView.
    - If the user is authenticated, they are redirected to the task list page.
    """
    model = User
    template_name = 'login.html'  # Template for rendering the login form.
    form_class = LoginForm
    redirect_authenticated_user = True  # Redirects already logged-in users to the success URL.

    def get_success_url(self):
        # Returns the URL to redirect to after a successful login.
        return '/task_list'


def home(request):
    """
    Simple view that renders the home page.
    """
    return render(request, 'home.html')


def subscriptions(request):
    """
    Renders the subscriptions page where users can view and purchase subscriptions.
    """
    return render(request, 'subscriptions.html')


def login_redirect(request):
    """
    Redirects authenticated users to the task list and unauthenticated users to the login page.
    """
    if request.user.is_authenticated:
        return redirect('/task_list')
    else:
        return redirect('/login')


def profile(request):
    """
    Renders the user's profile page.
    - Retrieves the profile of the logged-in user and displays it in the 'profil.html' template.
    """
    user_profile = get_object_or_404(UserProfile, user=request.user)
    return render(request, 'profil.html', {'user_profile': user_profile})


def buy_silver(request):
    """
    Allows a user to purchase a Silver subscription.
    - The user must have completed 100 tasks (rubies).
    - If the user has enough rubies, their status is upgraded to 'silver' and the rubies are deducted.
    """
    user_profile = request.user
    user = UserProfile.objects.filter(user=user_profile).first()
    if user.tasks_completed >= 100:
        user.status = 'silver'  # Upgrade the user to Silver status.
        user.tasks_completed -= 100  # Deduct 100 tasks (rubies).
        user.save()
        return redirect('/task_list')
    else:
        # If the user doesn't have enough rubies, forbid the request.
        return HttpResponseForbidden("you don't have 100 rubies for a silver")


def buy_gold(request):
    """
    Allows a user to purchase a Gold subscription.
    - The user must have completed 300 tasks (rubies).
    - If the user has enough rubies, their status is upgraded to 'gold' and the rubies are deducted.
    """
    user_profile = request.user
    user = UserProfile.objects.filter(user=user_profile).first()
    if user.tasks_completed >= 300:
        user.status = 'gold'  # Upgrade the user to Gold status.
        user.tasks_completed -= 300  # Deduct 300 tasks (rubies).
        user.save()
        return redirect('/task_list')
    else:
        # If the user doesn't have enough rubies, forbid the request.
        return HttpResponseForbidden("you don't have 300 rubies for a gold")


class StatisticsView(LoginRequiredMixin, View, GoldSubscriptionRequiredMixin):
    """
    View that displays user statistics.
    - Only available to users with a Gold subscription (handled by the GoldSubscriptionRequiredMixin).
    - Displays various statistics like total tasks, completed tasks, consecutive active days, etc.
    """
    def get(self, request):
        user_profile = request.user.userprofile
        status = user_profile.status  # Get the current subscription status.
        total_tasks = user_profile.total_tasks_count()  # Total number of tasks.
        completed_tasks = user_profile.completed_tasks_count()  # Number of completed tasks.
        consecutive_days = user_profile.consecutive_days_active()  # Number of consecutive active days.
        completion_percentage = user_profile.completion_percentage()  # Percentage of tasks completed.
        most_active_day = user_profile.most_active_day_of_week()  # The day of the week the user is most active.

        # Render the statistics page with the gathered data.
        return render(request, 'statistic.html', {
            'status': status,
            'total_tasks': total_tasks,
            'completed_tasks': completed_tasks,
            'consecutive_days': consecutive_days,
            'completion_percentage': completion_percentage,
            'most_active_day': most_active_day,
        })
