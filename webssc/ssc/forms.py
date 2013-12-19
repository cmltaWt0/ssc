from django import forms


class SSCForm(forms.Form):
    """
    Form for login_name
    """
    login_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'style':'width:20em',
                                                                              'placeholder':'LOGIN_NAME'}))