from rest_framework import generics

from ..models import Reward
from ..serializer import RewardSerializer


class RewardList(generics.ListAPIView):
    queryset = Reward.objects.all()
    serializer_class = RewardSerializer
