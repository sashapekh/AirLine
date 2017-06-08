# -*- coding: utf-8 -*-

u"""Forms for creating and updating user data."""

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField


class UserCreationForm(forms.ModelForm):
    u"""
    Form for creation new user.
    If passwords is equal, create new record, else throw error.
    """

    password1 = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput
    )
    password2 = forms.CharField(
        label='Подтвердить пароль',
        widget=forms.PasswordInput
    )

    def clean_password2(self):
        # Check password1 and password2 to equal.
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Passwords is not equal!')
        return password2

    def save(self, commit=True):
        """
        Create new record in DB. For password hashing used default Django
        function."""
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user

    class Meta:
        model = get_user_model()
        fields = ('email', 'firstname', 'lastname', 'middlename', 'date_of_birth', 'citizen_city')


class UserChangeForm(forms.ModelForm):
    u"""
    Form for updating user data.
    If password is defined in data, call default Django function for setting
    him.
    """
    password = ReadOnlyPasswordHashField(
        widget=forms.PasswordInput,
        required=False
    )

    # def clean_password(self):
    #     # Return 'password' value from data
    #     return self.initial['password']

    def save(self, commit=True):
        u"""
        If password is defined, call set_password.method before commiting.
        """
        user = super(UserChangeForm, self).save(commit=False)
        password = self.cleaned_data['password']
        if password:
            user.set_password(password)
        if commit:
            user.save()
        return user

    class Meta:
        model = get_user_model()
        fields = ['password']


class LoginForm(forms.Form):
    u"""Form for authorization with admin panel."""
    username = forms.CharField()
    password = forms.CharField()
