from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.forms import ModelForm

from apps.product.models import Product


class ProductForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'  # this line sets your form's method to post
        self.helper.form_action = "."  # this line sets the form action
        self.helper.add_input(Submit('submit', 'Add', css_class="btn btn-dark is-uppercase")
                              )

    class Meta:
        model = Product
        fields = ['category', 'image', 'title', 'description', 'quantity', 'price']
