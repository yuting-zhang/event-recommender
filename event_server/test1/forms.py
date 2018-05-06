from django import forms

class CheckboxForm(forms.Form):
    ai = forms.BooleanField(required=False, initial=False, label='Artificial Intelligence')
