import logging

from django.conf import settings
from django.shortcuts import redirect

from django.core.exceptions import ObjectDoesNotExist

from django.views.decorators.http import require_POST

from django.contrib import messages
from django.contrib.auth.decorators import login_required

from django.views import generic

import stripe

from payments.models import Customer


from django.http import HttpResponse
from django.utils import simplejson


class JSONResponse(HttpResponse):
    """
        JSON response
    """
    def __init__(self, content, mimetype='application/json', status=None, content_type=None):
        super(JSONResponse, self).__init__(
            content=simplejson.dumps(content),
            mimetype=mimetype,
            status=status,
            content_type=content_type,
        )


def wrap_stripe_error(ajax_view):
    """Return a JSONResponse with status 500 if any stripe calls fail for some reason."""
    def wrapper(request):
        try:
            return ajax_view(request)
        except stripe.StripeError as e:
            logging.error('Stripe Error')
            logging.error(e)
            if request.method == "POST":
                logging.error(request.POST)
            return JSONResponse(content=u"%s" % e, status=500)
    return wrapper


@require_POST
@login_required
@wrap_stripe_error
def subscribe_ajax(request):
    """"""
    stripe_token = request.POST.get("stripe_token")
    plan_id = request.POST.get("plan_id", None)

    try:
        customer = request.user.customer
    except ObjectDoesNotExist:
        customer = Customer.create(request.user)

    customer.update_card(stripe_token)
    customer.subscribe(plan_id)
    messages.success(request, 'Your subscription is now active.')
    return JSONResponse({'message': 'Subscription successful'})


@require_POST
@login_required
@wrap_stripe_error
def change_plan_ajax(request):
    """"""
    plan_id = request.POST.get("plan_id", None)
    request.user.customer.subscribe(plan_id)
    messages.info(request, 'Subscription plan changed to: %s' % settings.PAYMENTS_PLANS[plan_id]['name'])
    return JSONResponse({'message': 'Subscription changed.'})


@require_POST
@login_required
@wrap_stripe_error
def change_card_ajax(request):
    """"""
    if request.POST.get("stripe_token"):
        customer = request.user.customer
        send_invoice = customer.card_fingerprint == ""
        customer.update_card(
            request.POST.get("stripe_token")
        )
        if send_invoice:
            customer.send_invoice()
        customer.retry_unpaid_invoices()
        messages.success(request, 'Card information was changed successfully.')
        return JSONResponse({'message': 'Card was updated.'})
    else:
        raise stripe.StripeError('Invalid Stripe token')


@require_POST
@login_required
@wrap_stripe_error
def cancel_ajax(request):
    """"""
    request.user.customer.cancel(at_period_end=False)
    messages.info(request, "You have unsubscribed successfully.")
    return JSONResponse({'message': 'Cancellation successful.'})


class BaseStripeTemplateView(generic.TemplateView):
    """"""

    def get_context_data(self, **kwargs):
        """"""
        ctx = super(BaseStripeTemplateView, self).get_context_data(**kwargs)
        ctx.update({
            "STRIPE_PUBLIC_KEY": settings.STRIPE_PUBLIC_KEY,
            "plans": settings.PAYMENTS_PLANS,
        })
        return ctx


class BaseSubscribeView(BaseStripeTemplateView):
    """Vanilla Checkout.js example"""
    def get(self, request, *args, **kwargs):
        """Redirect user to home if he already has an active subscription"""
        try:
            if self.request.user.customer.current_subscription.status == 'active':
                messages.warning(request, "You already have an active paid subscription.")
                return redirect('home')
        except ObjectDoesNotExist:
            pass

        return super(BaseSubscribeView, self).get(request, *args, **kwargs)


class VanillaSubscribeView(BaseSubscribeView):
    """"""
    template_name = "main/payment/subscribe_vanilla.html"


class ModalSubscribeView(BaseSubscribeView):
    """"""
    template_name = "main/payment/subscribe_modal.html"


class CancelSubscriptionView(generic.TemplateView):
    """Confirmation view for cancelling current subscription"""
    template_name = 'main/payment/cancel.html'


class ChangeSubscriptionView(generic.TemplateView):
    """"""
    template_name = 'main/payment/change.html'

    def get_context_data(self, **kwargs):
        """"""
        return {
            'plans': [settings.PAYMENTS_PLANS[k] for k in sorted(settings.PAYMENTS_PLANS.keys())]
        }


class ChangeCardView(generic.TemplateView):
    """"""
    template_name = "main/payment/card.html"

    def get_context_data(self, **kwargs):
        """"""
        return {
            "STRIPE_PUBLIC_KEY": settings.STRIPE_PUBLIC_KEY,
        }


subscribe_vanilla = VanillaSubscribeView.as_view()
subscribe_modal = ModalSubscribeView.as_view()
change = ChangeSubscriptionView.as_view()
change_card = ChangeCardView.as_view()
cancel = CancelSubscriptionView.as_view()
