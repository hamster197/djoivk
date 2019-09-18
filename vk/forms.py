from django import forms

class LoginForm(forms.Form):
    lgn = forms.CharField(label='Введите логин VC:', max_length=20, required=True, help_text='email или телефон')
    psw = forms.CharField(label='Пароль VC', max_length=200, widget=forms.PasswordInput, required=True)