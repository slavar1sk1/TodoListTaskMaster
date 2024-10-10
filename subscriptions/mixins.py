from django.http import HttpResponseForbidden
from django.shortcuts import redirect

class BronzeSubscriptionRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if hasattr(request.user, 'subscription') and request.user.subscription.status == 'bronze':
                return super().dispatch(request, *args, **kwargs)
            else:
                return HttpResponseForbidden("You do not have the required subscription status.")
        else:
            return redirect('login')



class SilverSubscriptionRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if hasattr(request.user, 'subscription') and request.user.subscription.status == 'silver':
                return super().dispatch(request, *args, **kwargs)
            else:
                return HttpResponseForbidden("You do not have the required subscription status.")

        else:
            return redirect('login')


class GoldSubscriptionRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if hasattr(request.user, 'subscription') and request.user.subscription.status == 'gold':
                return super().dispatch(request, *args, **kwargs)
            else:
                return HttpResponseForbidden("You do not have the required subscription status.")

        else:
            return redirect('login')