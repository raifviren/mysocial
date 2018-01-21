from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'input-text'}), label='username', max_length=150)
    password = forms.CharField(widget=forms.TextInput(attrs={'class': 'input-text'}))
