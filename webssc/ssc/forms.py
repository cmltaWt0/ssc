from django import forms
import re


city = (
	('KHARKOV', 'KHARKOV'),
	('ODESSA', 'ODESSA'),
	('DONETSK', 'DONETSK'),
	('KIEV', 'KIEV'),
	('DNEPR', 'DNEPR'),
	('POLTAVA', 'POLTAVA'),
	('MARIUPOL', 'MARIUPOL'),
	)

point = (
	        ('K0', 'K0'),
	        ('K2', 'K2'),
	        ('K01', 'K01'),
	        ('K02', 'K02'),
	        ('K03', 'K03'),
	        ('K04', 'K04'),
	        ('K05', 'K05'),
	        ('K06', 'K06'),
	        ('K08', 'K08'),
	        ('K11', 'K11'),
    		('K12', 'K12'),
    		('K13', 'K13'),
    		('K14', 'K14'),
    		('K45', 'K45'),
    		('K20', 'K20'),
    		('X00', 'X00'),
         )


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

        if len(login_part) != 3:
            correct = False
        else:
            last_part = re.sub('[/:.]', '*', login_part[2]).split('*')
            try:
                if (len(last_part) != 7 or
                    0 in map(int, last_part) or
                    login_part[0].split('-')[0] not in [i[0] for i in city] or
                    login_part[0].split('-')[1] not in [i[0] for i in point] or
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
    Form for login_name.
    """
    login_name = LoginNameField(max_length=50, min_length=15, label='',
    	                        widget=forms.TextInput(attrs={'style':'width:20em',
                                                              'placeholder':'LOGIN_NAME'}))


class MASKForm(forms.Form):
	"""
	Mask form.
	"""
	city_field = forms.ChoiceField(choices=city, widget=forms.Select(attrs={'style':'width:8em'}))
	point_field = forms.ChoiceField(choices=point, widget=forms.Select(attrs={'style':'width:5em'}))
