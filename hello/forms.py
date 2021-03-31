from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=64)
    password = forms.CharField(label='Password', max_length=128, widget=forms.PasswordInput)


class RegistrationForm(forms.Form):
    username = forms.CharField(label='Username', max_length=32, widget=forms.TextInput(attrs={'class': 'form-field', 'size': '30'}))
    email = forms.EmailField(label='E-mail', max_length=64, widget=forms.TextInput(attrs={'class': 'form-field', 'size': '30'}))
    password = forms.CharField(label='Password', min_length=3, max_length=32,
                               widget=forms.PasswordInput(attrs={'class': 'form-field', 'size': '30'}))
    check_password = forms.CharField(label='Re-enter password', min_length=3, max_length=32,
                                     widget=forms.PasswordInput(attrs={'class': 'form-field', 'size': '30'}))