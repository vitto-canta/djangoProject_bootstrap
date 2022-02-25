from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.forms import ModelForm

from apps.review.models import Review


class ReviewForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(ReviewForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_action = "."
        self.fields['rate'].widget.attrs.update({'min': 0, 'max': 5})
        self.helper.add_input(Submit('submit', 'Confirm review', css_class="btn btn-dark is-uppercase"))

    class Meta:
        model = Review
        fields = ['comment', 'rate']
