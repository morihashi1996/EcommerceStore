from django import forms
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm, SetPasswordForm

from .models import UserBase


class RegistrationForm(forms.ModelForm):
    full_name = forms.CharField(label='Enter Full name', min_length=4, max_length=50, help_text='Required')
    email = forms.EmailField(max_length=100, help_text='Required',
                             error_messages={'required': 'Sorry, you will need an email'})
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)

    class Meta:
        model = UserBase
        fields = ('email', 'full_name',)

    def clean_email(self):
        email = self.cleaned_data['email']
        if UserBase.objects.filter(email=email).exists():
            raise forms.ValidationError(
                'Please use another Email, that is already taken'
            )
        return email

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords do not match.')
        return cd['password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['full_name'].widget.attrs.update(
            {'class': 'name', 'id': 'name',})
        self.fields['email'].widget.attrs.update(
            {'class': 'email', 'id': 'email', })
        self.fields['password'].widget.attrs.update(
            {'class': 'pass', 'id': 'password', })
        self.fields['password2'].widget.attrs.update(
            {'class': 'passConfirm', 'id': 'passwordCon', })


class UserLoginForm(AuthenticationForm):
    email = forms.CharField(widget=forms.TextInput(
        attrs={'class': '',}
    ))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': '',}
    ))


class UserEditFrom(forms.ModelForm):
    full_name = forms.CharField(
        label='full name', min_length=4, max_length=50, widget=forms.TextInput(
            attrs={'class': {}, 'placeholder': 'full name'}
        ))
    email = forms.EmailField(
        label='Email(can not be changed', max_length=150, widget=forms.TextInput(
            attrs={'class': '', 'placeholder': 'email', 'readonly': 'readonly'}
        ))

    class Meta:
        model = UserBase
        fields = ('full_name',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['full_name'].required = True


class PwdResetForm(PasswordResetForm):
    email = forms.EmailField(max_length=254, widget=forms.TextInput(
        attrs={'class': '', 'placeholder': 'Email'}))

    def clean_email(self):
        email = self.cleaned_data['email']
        u = UserBase.objects.filter(email=email)
        if not u:
            raise forms.ValidationError(
                'unfortunatly we can not find thet email address'
            )
        return email


class PwdResetConfirmForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label='New Password', widget=forms.PasswordInput(
            attrs={'class': '', 'placeholder': 'New Password'}
        ))
    new_password2 = forms.CharField(
        label='Repeat New Password', widget=forms.PasswordInput(
            attrs={'class': '', 'placeholder': 'Repeat New Password'}
        ))
