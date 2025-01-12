from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=100,
        label='Kullanıcı Adı',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Kullanıcı Adı'})
    )
    password = forms.CharField(
        max_length=100,
        label='Parola',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Parola'})
    )

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError('Kullanıcı adı veya parola yanlış.')
        return cleaned_data

class RegisterForm(forms.ModelForm):
    password1 = forms.CharField(
        max_length=100,
        label='Parola',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Parola'})
    )
    password2 = forms.CharField(
        max_length=100,
        label='Parolayı Doğrula',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Parolayı Doğrula'})
    )

    class Meta:
        model = User
        fields = ['username']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Kullanıcı Adı'}),
        }

    def clean_password2(self):
        cleaned_data = self.cleaned_data
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Parolalar uyuşmuyor.')
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user
