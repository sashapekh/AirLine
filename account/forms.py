from django import forms


class ChangePassword(forms.Form):
    password = forms.CharField(label='Новый пароль',
                               max_length=128,
                               min_length=5,
                               widget=forms.PasswordInput)
    confirm_password = forms.CharField(label='Подтверждение',
                                       max_length=128,
                                       min_length=5,
                                       widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super(ChangePassword, self).clean()

        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password and confirm_password:
            if password != confirm_password:
                raise forms.ValidationError('Два поля должны совпадать')
        return cleaned_data


