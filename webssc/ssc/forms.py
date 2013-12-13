from django import forms


class SSCForm(forms.Form):
    """
    Form for login_name
    """
    login_name = forms.CharField(max_length=50)