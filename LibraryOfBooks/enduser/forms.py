from django import forms


class FilterForm(forms.Form):
    title = forms.CharField(required=False)
    author = forms.CharField(required=False)
