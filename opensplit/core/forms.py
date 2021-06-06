from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

class ExpenseForm(forms.Form):
    description = forms.CharField()
    amount = forms.DecimalField(min_value=0)
    paid_by = forms.ModelChoiceField(queryset=User.objects.all())
    participants = forms.ModelMultipleChoiceField(queryset=User.objects.all())

    def __init__(self, *args, **kwargs):
        org = kwargs.pop('org', None)
        super().__init__(*args, **kwargs)
        if org:
            self.fields['paid_by'].queryset = org.member
            self.fields['participants'].queryset = org.member

class NewOrgForm(forms.Form):
    name = forms.CharField()

class PaymentForm(forms.Form):
    description = forms.CharField(initial="Schuldenausgleich")
    amount = forms.DecimalField(min_value=0)
    sender = forms.ModelChoiceField(queryset=User.objects.all())
    receiver = forms.ModelChoiceField(queryset=User.objects.all())

    def __init__(self, *args, **kwargs):
        org = kwargs.pop('org', None)
        super().__init__(*args, **kwargs)
        if org:
            self.fields['sender'].queryset = org.member
            self.fields['receiver'].queryset = org.member
