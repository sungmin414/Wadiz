from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueValidator

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    password = serializers.SlugField(max_length=12, min_length=1, allow_blank=False, write_only=True)
    username = serializers.EmailField(validators=[UniqueValidator(queryset=User.objects.all())])
    nickname = serializers.CharField(max_length=10, validators=[UniqueValidator(queryset=User.objects.all())])

    class Meta:
        model = User

        fields = (
            'pk',
            'username',
            'password',
            'nickname',
            'img_profile',
        )

    def validate_password(self, value):
        if value == self.initial_data.get('password1'):
            return value
        raise ValidationError('비밀번호 불일치')