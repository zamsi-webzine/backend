from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.utils.translation import ugettext_lazy as _

from member.models import ZSUser


# 유저 생성 폼
class UserCreationForm(forms.ModelForm):
    email = forms.EmailField(
        label=_('Email address'),
        widget=forms.EmailInput(
            attrs={
                'class': 'form_control',
                'required': 'True',
            }
        )
    )
    nickname = forms.CharField(
        label=_('Nickname'),
        widget=forms.TextInput(
            attrs={
                'class': 'form_control',
                'required': 'True',
            }
        )
    )
    password1 = forms.CharField(
        label=_('Password'),
        widget=forms.PasswordInput(
            attrs={
                'class': 'form_control',
                'placeholder': _('Password'),
                'required': 'True',
            }
        )
    )
    password2 = forms.CharField(
        label=_('Password confirmation'),
        widget=forms.PasswordInput(
            attrs={
                'class': 'form_control',
                'placeholder': _('Password confirmation'),
                'required': 'True',
            }
        )
    )

    class Meta:
        model = ZSUser
        fields = (
            'email',
            'nickname',
        )

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(_("Passwords don't match"))

        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


# 유저 수정 폼
class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(
        label=_('Password')
    )

    class Meta:
        model = ZSUser
        fields = (
            'email',
            'nickname',
            'is_active',
            'is_superuser',
        )

    def clean_password(self):
        return self.initial['password']
