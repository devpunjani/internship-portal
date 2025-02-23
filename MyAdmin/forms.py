from django import forms
from .models import IndustryModel

#Industry Form
class IndustryForm(forms.ModelForm):
    class Meta:
        model = IndustryModel
        fields = [
            "name",
        ]