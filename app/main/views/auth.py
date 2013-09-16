from django.conf import settings

from django.utils.translation import ugettext as _
from django.shortcuts import render, redirect

from django.contrib import messages
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required

from main import forms


def login(request, template_name='base_form.html'):
    """Allow a user to log in with either username/email and password."""

    if request.user.is_authenticated():
        message = _('You are already logged in as') + u' %s!' % request.user.email
        messages.info(request, message)
        return redirect('home')

    if request.method == 'POST':
        form = forms.AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)

            redirect_url = form.cleaned_data.get('redirect_url', 'home')
            return redirect(redirect_url)
    else:
        form = forms.AuthenticationForm(initial={'redirect_url': request.GET.get('next', '/home')})

    template_vars = {
        'form': form,
    }

    return render(request, template_name, template_vars)


@login_required
def logout(request):
    auth_logout(request)
    return redirect('landing_page')


def sign_up(request, template_name='base_form.html'):
    """Allow a user to log in with either username/email and password."""
    form = forms.UserCreationForm()

    if request.user.is_authenticated():
        messages.success(request, _('You are already logged in!'))
        return redirect('home')

    if request.method == 'POST':
        form = forms.UserCreationForm(request.POST)

        if form.is_valid():

            user = form.save(commit=False)
            user.email = user.username
            user.save()

            user.backend = settings.AUTHENTICATION_BACKENDS[0]
            auth_login(request, user)

            return redirect('home')

    template_vars = {
        'form': form,
    }

    return render(request, template_name, template_vars)
