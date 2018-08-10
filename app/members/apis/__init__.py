from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from rest_framework.compat import authenticate
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics

from ..serializer import UserSerializer

User = get_user_model()


class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class AuthToken(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)

        if user:
            token, __ = Token.objects.get_or_create(user=user)

            data = {
                'token': token.key,
            }
            return Response(data)
        raise AuthenticationFailed('인증정보가 올바르지 않습니다')
