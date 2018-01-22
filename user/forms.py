from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'input100',
                                      'placeholder': 'Type your username',
                                      'type': 'text',}), label='username', max_length=150)
    password = forms.CharField(widget=forms.TextInput(attrs={'class': 'input100',
                                      'placeholder': 'Type your password',
                                      'type': 'password',}))
