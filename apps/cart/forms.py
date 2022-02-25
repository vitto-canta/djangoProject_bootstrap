import re

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from django.core.exceptions import ValidationError

from apps.order.models import Order


def only_number(value):
    if not re.match('^[0-9 ]+$', value):
        raise ValidationError('It should contains only digits')


class CheckoutForm(forms.ModelForm):
    postcode = forms.CharField(min_length=4, max_length=6, validators=[only_number])
    phone_number = forms.CharField(min_length=6, max_length=15, validators=[only_number])

    # Payment
    credit_card = forms.CharField(min_length=10, max_length=20, validators=[only_number])
    cvv = forms.CharField(min_length=3, max_length=3, validators=[only_number])

    class Meta:
        model = Order
        fields = [
            'name',
            'surname',
            'email',
            'phone_number',
            'country',
            'town_city',
            'postcode',
            'address_line_1',
            'address_line_2',
        ]

    field_order = Meta.fields + ['credit_card', 'cvv']

    def __init__(self, *args, **kwargs):
        super(CheckoutForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_action = "."
        self.helper.add_input(Submit('submit', 'Confirm and pay', css_class="btn btn-dark is-uppercase"))
