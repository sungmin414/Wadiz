from rest_framework import serializers

from reward.models import Product, Reward


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product

        fields = (
            'pk',
            'product_name',
            'product_type',
            'product_company_name',
            'product_img',
            'product_interested_count',
            'product_start_time',
            'product_end_time',
            'product_cur_amount',
            'product_total_amount',
        )


class RewardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reward

        fields = (
            'reward_name',
            'reward_price',
            'reward_shipping_charge',
            'reward_expecting_departure_date',
            'reward_total_count',
            'reward_sold_count',
            'reward_on_sale',
            'product',
        )
