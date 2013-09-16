from django import forms

from django.utils.translation import ugettext as _

from django.contrib.auth import forms as auth_forms

from crispy_forms.layout import Layout, Submit, Fieldset
from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper


class CrispyFormMixin(object):

    def init_helper(self, form_tag=False):
        self.helper = FormHelper()
        self.helper.layout = self.get_layout()
        self.helper.form_tag = form_tag

    def get_layout(self):
        return Layout()


class AuthenticationForm(auth_forms.AuthenticationForm, CrispyFormMixin):
    """"""

    redirect_url = forms.CharField(widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):

        self.init_helper()
        super(AuthenticationForm, self).__init__(*args, **kwargs)

    def get_layout(self):
        return Layout(
            Fieldset(
                _('Please enter your credentials'),
                'username',
                'password',
                'redirect_url',
                css_class='text-center'
            ),
            FormActions(
                Submit('submit', _('Login'), css_class='button btn-large')
            )
        )


class UserCreationForm(auth_forms.UserCreationForm, CrispyFormMixin):

    username = forms.CharField(label='Username', required=True)
    password2 = forms.CharField(required=False, widget=forms.HiddenInput)

    def __init__(self, *args, **kwargs):
        self.init_helper()
        super(UserCreationForm, self).__init__(*args, **kwargs)

    def get_layout(self):
        return Layout(

            Fieldset(
                _('User Registration'),
                'username',
                'password1',
                'password2',
                css_class='text-center'
            ),


            FormActions(
                Submit('submit', _('Register'), css_class='button btn-large btn-danger')
            )
        )

    def clean_password2(self):
        """"""
        return self.cleaned_data.get('password1', None)
