from django.urls import path
from .views import *  # Import all views from the views module.
from .views import buy_silver  # Explicitly importing the `buy_silver` view.

# Define URL patterns for the application.
urlpatterns = [
    path('', home, name='home'),  # Home page, handled by the `home` view.
    path('login/', LoginUserView.as_view(), name='login'),  # Login page using the `LoginUserView` class-based view.
    path('registration/', RegistrationView.as_view(), name='registration'),  # Registration page using `RegistrationView`.
    path('subscriptions/', subscriptions, name='subscriptions'),  # Subscription plans page, rendered by `subscriptions` view.
    path('profile/', profile, name='profile'),  # Profile page, rendered by the `profile` view.
    path('buy_silver/', buy_silver, name='buy_silver'),  # Endpoint for buying Silver subscription, handled by `buy_silver`.
    path('buy_gold/', buy_gold, name='buy_gold'),  # Endpoint for buying Gold subscription, handled by `buy_gold`.
    path('statistic', StatisticsView.as_view(), name='statistic'),  # Statistics page, only available to Gold members, handled by `StatisticsView`.
]
