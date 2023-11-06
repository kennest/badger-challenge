from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from crispy_forms.layout import Layout, Submit, Column, Div, Field, HTML
from crispy_forms.helper import FormHelper
from django import forms
from .models import *


class Model3DForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(Model3DForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Column(
                "name",
                "image",
                "description",
            ),
            Submit('submit', 'Charger', css_class='btn btn-primary'),
        )

    class Meta:
        model = Model3d
        fields = ["name", "description", "image"]
