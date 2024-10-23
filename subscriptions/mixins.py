# Import necessary modules for response and redirection
from django.http import HttpResponseForbidden  # For forbidden access responses
from django.shortcuts import redirect  # To redirect users to login page if not authenticated

# Mixin to check if the user has a Bronze subscription
class BronzeSubscriptionRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        # Check if user is authenticated
        if request.user.is_authenticated:
            # Check if user has a subscription and if the status is 'bronze'
            if hasattr(request.user, 'subscription') and request.user.subscription.status == 'bronze':
                return super().dispatch(request, *args, **kwargs)  # Allow access to the view
            else:
                return HttpResponseForbidden("You do not have the required subscription status.")  # Deny access
        else:
            return redirect('login')  # Redirect to login if not authenticated


# Mixin to check if the user has a Silver subscription
class SilverSubscriptionRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        # Check if user is authenticated
        if request.user.is_authenticated:
            # Check if user has a subscription and if the status is 'silver'
            if hasattr(request.user, 'subscription') and request.user.subscription.status == 'silver':
                return super().dispatch(request, *args, **kwargs)  # Allow access to the view
            else:
                return HttpResponseForbidden("You do not have the required subscription status.")  # Deny access
        else:
            return redirect('login')  # Redirect to login if not authenticated


# Mixin to check if the user has a Gold subscription
class GoldSubscriptionRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        # Check if user is authenticated
        if request.user.is_authenticated:
            # Check if user has a subscription and if the status is 'gold'
            if hasattr(request.user, 'subscription') and request.user.subscription.status == 'gold':
                return super().dispatch(request, *args, **kwargs)  # Allow access to the view
            else:
                return HttpResponseForbidden("You do not have the required subscription status.")  # Deny access
        else:
            return redirect('login')  # Redirect to login if not authenticated
