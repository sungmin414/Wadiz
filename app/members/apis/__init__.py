from django.contrib.auth import get_user_model

from ..serializer import UserSerializer
from rest_framework import generics

User = get_user_model()


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
