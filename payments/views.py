from django.shortcuts import render
import stripe
from django.conf import settings
from django.views.generic.base import TemplateView

stripe.api_key = settings.STRIPE_SECRET_KEY # new


class HomePageView(TemplateView):
    template_name = 'payment/payment.html'

    def get_context_data(self, **kwargs):  # new
        context = super().get_context_data(**kwargs)
        context['key'] = settings.STRIPE_PUBLISHABLE_KEY
        return context


def charge(request):  # new
    if request.method == 'POST':
        charge = stripe.Charge.create(
            amount=500,
            currency='usd',
            description='A Django charge',
            source=request.POST['stripeToken']
        )
        return render(request, 'payment/charge.html')