from rest_framework import serializers

from reward.models import Reward


class RewardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reward

        fields = (
            'pk',
            'product_name',
            'product_type',
            'company_name',
            'product_img',
            'start_time',
            'end_time',
            'total_amount',
        )
