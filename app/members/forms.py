from django import forms

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()


class SignupForm(forms.Form):
    username = forms.EmailField(
        label='아이디',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'
            }
        )
    )

    nickname = forms.CharField(
        label='유저이름',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'
            }
        )
    )

    password = forms.CharField(
        label='비밀번호',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control'
            }
        )
    )

    password2 = forms.CharField(
        label='비밀번호확인',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control'
            }
        )
    )

    img_profile = forms.ImageField(
        required=False
    )

    def clean(self):
        super().clean()
        password = self.cleaned_data['password']
        password2 = self.cleaned_data['password2']

        if password != password2:
            self.add_error('password2', '비밀번호와 비밀번호 확인의 값이 일치하지 않습니다.')

        return self.cleaned_data

    def signup(self):
        fields = [
            'username',
            'password',
            'img_profile',
            'nickname'
        ]

        create_user_dict = dict(filter(lambda item: item[0] in fields, self.cleaned_data.items()))

        print(create_user_dict)

        user = User.objects.create_user(**create_user_dict)

        return user
