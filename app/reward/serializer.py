from rest_framework import serializers

from reward.models import Product, Reward


class RewardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reward

        fields = (
            'pk',
            'reward_name',
            'reward_option',
            'reward_price',
            'reward_shipping_charge',
            'reward_expecting_departure_date',
            'reward_total_count',
            'reward_sold_count',
            'reward_on_sale',
            'product',
        )


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


class ProductDetailSerializer(ProductSerializer):
    rewards = RewardSerializer(many=True)

    class Meta(ProductSerializer.Meta):
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
            'product_description',
            'rewards',
        )


class ProductFundingSerializer(ProductSerializer):
    rewards = RewardSerializer(many=True)

    class Meta(ProductSerializer.Meta):
        fields = (
            'pk',
            'product_name',
            'rewards',
        )
