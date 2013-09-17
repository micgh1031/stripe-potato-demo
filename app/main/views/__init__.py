import logging

from django.core.urlresolvers import reverse

from django.views import generic


class HomePageView(generic.TemplateView):
    """"""
    template_name = 'main/home.html'

home = HomePageView.as_view()


class LandingPageView(generic.RedirectView):
    """"""

    def get_redirect_url(self, **kwargs):
        """"""
        request = self.request
        if request.user and request.user.is_authenticated():
            return reverse('home')
        return reverse('signup')

landing = LandingPageView.as_view()
