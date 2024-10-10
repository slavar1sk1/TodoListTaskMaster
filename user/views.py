from .forms import LoginForm, RegistrationForm
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.views import LoginView
from .models import User, UserProfile
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.shortcuts import render, get_object_or_404

__all__ = ['RegistrationView', 'LoginUserView', 'home', 'subscriptions', 'profile']


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