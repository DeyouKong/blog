from django import forms


class GeeForm(forms.Form):
    geetest_challenge = forms.CharField(min_length=1, max_length=40, required=True)
    geetest_validate = forms.CharField(min_length=1, max_length=40, required=True)
    geetest_seccode = forms.CharField(min_length=1, max_length=40, required=True)