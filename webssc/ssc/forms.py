from django import forms
import re

city = ['KHARKOV', 'ODESSA', 'DONETSK', 'KIEV', 'DNEPR', 'POLTAVA', 'MARIUPOL']
point = ['K0', 'K2', 'K01', 'K02', 'K03', 'K04', 'K05', 'K06', 'K08', 'K11',
         'K12', 'K13', 'K14', 'K45', 'K20', 'X00']


class LoginNameField(forms.CharField):
    def to_python(self, login_name):
        """
        correction(login_name: str) -> str
        """
        login_name = login_name.strip()
        login_name = re.sub(' +', ' ', login_name)
        login_name = login_name.upper()
        login_name = re.sub('ETH', 'eth', login_name)

        return login_name

    def validate(self, login_name):
        """
        Testing login_name
        """
        correct = True
        login_part = login_name.split(' ')

        if login_name == '' or len(login_part) != 3:
            correct = False
        else:
            last_part = re.sub('[/:.]', '*', login_part[2]).split('*')
            try:
                if (len(last_part) != 7 or
                    0 in map(int, last_part) or
                    login_part[0].split('-')[0] not in city or
                    login_part[0].split('-')[1] not in point or
                    (login_part[1] != 'PON' and login_part[1] != 'eth')):
                    correct = False
            except ValueError:
                    correct = False
        if login_name == 'QUIT':
            correct = True

        if not correct:
            raise forms.ValidationError('Error testing LOGIN_NAME.')


class SSCForm(forms.Form):
    """
    Form for login_name
    """
    login_name = LoginNameField(max_length=50, widget=forms.TextInput(attrs={'style':'width:20em',
                                                                             'placeholder':'LOGIN_NAME'}))