from rest_framework import status
from rest_framework.test import APITestCase
import json

from reward.models import Reward, Product


def get_dummy_reward():
    notebook_list = ['맥북', '그램', '맥북프로', '레노버']

    return [Product.objects.create(
        product_name=f'{notebook}',
        product_type='노트북',
        product_company_name='와디즈주식회사',
        product_img='노트북.jpg',
        product_interested_count='100',
        product_start_time='2018-08-15',
        product_end_time='2018-08-20',
        product_total_amount=2000000
    ) for notebook in notebook_list]


def get_dummy_product():

    products = []

    for product in get_dummy_reward():

        for num in range(3):
            reward = Reward.objects.create(
                reward_name=f'얼리버드{num}',
                reward_price=30000,
                reward_shipping_charge=2500,
                reward_expecting_departure_date='2018년 8월 8일',
                reward_total_count=100,
                reward_sold_count=5,
                product=product,
            )
            products.append(reward)
    return products


class RewardListTest(APITestCase):
    URL = '/api/rewards/'

    def test_reward_list_status_code(self):
        response = self.client.get(self.URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_reward_list_count(self):
        get_dummy_reward()
        response = self.client.get(self.URL)

        data = json.loads(response.content)

        self.assertEqual(len(data), Reward.objects.count())

    def test_product_list(self):

        for product in get_dummy_product():
            print(product)

