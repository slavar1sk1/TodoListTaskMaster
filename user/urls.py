from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('login/', LoginUserView.as_view(), name='login'),
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('subscriptions/', subscriptions, name='subscriptions'),
    path('profile/', profile, name='profile')
]
