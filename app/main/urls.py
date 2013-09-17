from django.contrib.auth.decorators import login_required

from django.conf.urls import patterns, url

from main import views
from main.views import payment

urlpatterns = patterns(
    'main.views',
    url(r'^home$', login_required(views.home), name="home"),
    url(r'^$', views.landing, name="landing_page"),

    url(r'^subscribe-vanilla$', login_required(payment.subscribe_vanilla), name="subscribe_vanilla"),
    url(r'^subscribe-modal$', login_required(payment.subscribe_modal), name="subscribe_modal"),
    url(r'^change/plan/$', login_required(payment.change), name="change_subscription"),
    url(r'^change/card/$', login_required(payment.change_card), name="change_card"),
    url(r'^cancel$', login_required(payment.cancel), name="cancel_subscription"),

    url(r'^subscribe_ajax$', 'payment.subscribe_ajax', name="subscribe_ajax"),
    url(r'^cancel_ajax$', 'payment.cancel_ajax', name="cancel_ajax"),
    url(r'^change_plan_ajax$', 'payment.change_plan_ajax', name="change_plan_ajax"),
    url(r'^change_card_ajax$', 'payment.change_card_ajax', name="change_card_ajax"),


    url(r'^login$', 'auth.login', name='login'),
    url(r'^logout$', 'auth.logout', name='logout'),
    url(r'^signup$', 'auth.sign_up', name='signup',),
)
