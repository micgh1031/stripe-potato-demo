import logging

from django.shortcuts import redirect

from django.views import generic


class HomePageView(generic.TemplateView):
    """"""
    template_name = 'main/home.html'

home = HomePageView.as_view()


class LandingPageView(generic.TemplateView):
    """"""
    template_name = 'main/landing.html'

    def get(self, request, *args, **kwargs):
        """"""
        if request.user and request.user.is_authenticated():
            return redirect('home')
        return super(LandingPageView, self).get(request, *args, **kwargs)

landing = LandingPageView.as_view()
