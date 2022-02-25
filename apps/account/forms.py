from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from django.contrib.auth.password_validation import validate_password

from .models import Account


class RegistrationForm(forms.ModelForm):
    CHOICES = [('', '---'),
               ('1', 'Yes'),
               ('0', 'Not now, maybe later'),
               ]
    is_vendor = forms.TypedChoiceField(
        label="I'd like to sell items",
        choices=CHOICES,
        coerce=lambda x: bool(int(x)),
        required=True,
        help_text='Required')
    is_costumer = forms.TypedChoiceField(
        label="I'd like to buy items",
        choices=CHOICES,
        coerce=lambda x: bool(int(x)),
        required=True,
        help_text='Required')

    username = forms.CharField(
        label='Username', min_length=4, max_length=50, help_text='Required', error_messages={
            'required': 'Sorry, you will need a valid username'})
    email = forms.EmailField(max_length=100, help_text='Required', error_messages={
        'required': 'Sorry, you will need a valid email'})
    password = forms.CharField(label='Password', widget=forms.PasswordInput, help_text='Required',
                               validators=[validate_password])
    password2 = forms.CharField(
        label='Repeat password', widget=forms.PasswordInput, help_text='Required', validators=[validate_password])
    is_active = True

    class Meta:
        model = Account
        fields = ('username',
                  'email',
                  'phone_number',
                  'is_vendor',
                  'is_costumer',
                  'name',
                  'surname',
                  'country',
                  'town_city',
                  'postcode',
                  'address_line_1',
                  'address_line_2',
                  )

    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        r = Account.objects.filter(username=username)
        if r.count():
            raise forms.ValidationError("username already exists")
        return username

    def clean_password2(self):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')

        if password != password2:
            raise forms.ValidationError("Your passwords do not match", code="pw_not_match")
        return password2

    def clean_email(self):
        email = self.cleaned_data['email']
        if Account.objects.filter(email=email).exists():
            raise forms.ValidationError(
                'Please use another Email, that is already taken')
        return email

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'Enter username'})
        self.fields['email'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'Enter e-mail', 'name': 'email', 'id': 'id_email'})
        self.fields['password'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'Enter password'})
        self.fields['password2'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Repeat Password'})

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_action = "."
        self.helper.add_input(Submit('submit', 'Sign in', css_class="btn btn-dark is-uppercase"))


class DataForm(forms.ModelForm):
    username = forms.CharField()
    email = forms.EmailField(max_length=100)

    class Meta:
        model = Account
        fields = [
            'username',
            'email',
            'name',
            'surname',
            'phone_number',
            'country',
            'town_city',
            'postcode',
            'address_line_1',
            'address_line_2',

        ]

    field_order = ['username', 'email'] + Meta.fields

    def __init__(self, *args, **kwargs):
        super(DataForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['readonly'] = 'readonly'
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_action = "."
        self.helper.add_input(Submit('submit', 'Save changes', css_class="btn btn-dark is-uppercase"))
