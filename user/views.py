from django.http import HttpResponseForbidden

from .forms import LoginForm, RegistrationForm
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.views import LoginView
from .models import User, UserProfile
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from subscriptions.mixins import GoldSubscriptionRequiredMixin

__all__ = ['RegistrationView', 'LoginUserView', 'home', 'subscriptions', 'profile', 'StatisticsView', 'buy_gold']


# View for Registration
class RegistrationView(CreateView):
    model = User
    template_name = 'registration.html'
    form_class = RegistrationForm
    
    success_url = '/task_list'

    def form_valid(self, form):
        response = super().form_valid(form)
        # Создание профиля пользователя
        UserProfile.objects.create(user=self.object, status=UserProfile.BRONZE)
        # Автоматический вход пользователя после регистрации
        login(self.request, self.object)
        return response


# View for Login
class LoginUserView(LoginView):
    model = User
    template_name = 'login.html'
    form_class = LoginForm
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return '/task_list'


# Create a home page
def home(request):
    return render(request, 'home.html')


# Create Subscriptions page (just how much cost the subscriptions)
def subscriptions(request):
    return render(request, 'subscriptions.html')


def login_redirect(request):
    if request.user.is_authenticated:
        return redirect('/task_list')
    else:
        return redirect('/login') 
    

def profile(request):
    user_profile = get_object_or_404(UserProfile, user=request.user)
    return render(request, 'profil.html', {'user_profile': user_profile})


def buy_silver(request):
    user_profile = request.user
    user = UserProfile.objects.filter(user=user_profile).first()
    if user.tasks_completed >= 100:
        user.status = 'silver'
        user.tasks_completed -= 100
        user.save()
        return redirect('/task_list')
    else:
        return HttpResponseForbidden("you don't have 100 rubies for a silver")


def buy_gold(request):
    user_profile = request.user
    user = UserProfile.objects.filter(user=user_profile).first()
    if user.tasks_completed >= 300:
        user.status = 'gold'
        user.tasks_completed -= 300
        user.save()
        print(user.status)
        print(user.tasks_completed)
        return redirect('/task_list')
    else:
        return HttpResponseForbidden("you don't have 300 rubies for a gold")


class StatisticsView(LoginRequiredMixin, View, GoldSubscriptionRequiredMixin):
    def get(self, request):
        user_profile = request.user.userprofile

        # Получаем статистику из модели
        status = user_profile.status
        total_tasks = user_profile.total_tasks_count()
        completed_tasks = user_profile.completed_tasks_count()
        consecutive_days = user_profile.consecutive_days_active()
        completion_percentage = user_profile.completion_percentage()
        most_active_day = user_profile.most_active_day_of_week()

        return render(request, 'statistic.html', {
            'status': status,
            'total_tasks': total_tasks,
            'completed_tasks': completed_tasks,
            'consecutive_days': consecutive_days,
            'completion_percentage': completion_percentage,
            'most_active_day': most_active_day,
        })