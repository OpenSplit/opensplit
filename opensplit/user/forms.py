from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Field


class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    helper = FormHelper()
    helper.add_input(Submit("submit", "Create account", css_class="btn-primary"))
    helper.form_method = "POST"


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())

    helper = FormHelper()
    helper.add_input(Submit("submit", "Login", css_class="btn-primary"))
    helper.form_method = "POST"
