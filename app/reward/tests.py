from rest_framework import status
from rest_framework.test import APITestCase
import json

from reward.models import Reward


def get_dummy_reward():
    notebook_list = ['맥북', '그램', '맥북프로', '레노버']

    return [Reward.objects.create(
        product_name=f'{notebook}',
        product_type='노트북',
        company_name='와디즈주식회사',
        product_img='노트북.jpg',
        interested_count='100',
        start_time='2018-08-15',
        end_time='2018-08-20',
        total_amount=2000000
    ) for notebook in notebook_list]


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
