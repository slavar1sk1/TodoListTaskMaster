from django.urls import path
from .views import *
from .views import buy_silver

urlpatterns = [
    path('', home, name='home'),
    path('login/', LoginUserView.as_view(), name='login'),
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('subscriptions/', subscriptions, name='subscriptions'),
    path('profile/', profile, name='profile'),
    path('buy_silver/', buy_silver, name='buy_silver'),
    path('buy_gold/', buy_gold, name='buy_gold'),
    path('statistic', StatisticsView.as_view(), name='statistic')
]
