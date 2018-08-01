from django.shortcuts import render

import os
from bs4 import BeautifulSoup
from selenium import webdriver
import re
import time
import requests

from reward.models import Reward


def reward_list(request):

    # Reward.objects.all().delete()

    if Reward.objects.count() < 10:
        WadizCrawler.create_detail_html()
        WadizCrawler.get_item_list()

    reward = Reward.objects.all()

    context = {
        'rewards': reward
    }

    return render(request, 'production/product-list.html', context)


class WadizCrawler:
    detail_info_list = []

    reward_dict = {
        'product_name': '',
        'product_type': '',
        'company_name': '',
        'product_img': '',
        'start_time': '',
        'total_amount': '',
        'end_time': '',
    }

    temp = []

    @classmethod
    def start(cls):

        url = 'https://www.wadiz.kr/web/campaign/detail/21408'

        file_path = 'data/wadiz_reward_list.html'

        driver = webdriver.Chrome('driver/chromedriver')

        driver.get(url)

        time.sleep(2)

        if not os.path.exists(file_path):

            html = driver.page_source

            open(file_path, 'wt').write(html)

        else:
            open(file_path, 'rt').read()

        driver.close()

    @classmethod
    def get_item_list(cls):
        file_path = 'reward/data/wadiz_reward_list.html'

        html = open(file_path, 'rt').read()

        soup = BeautifulSoup(html, 'lxml')

        ul_contents = soup.select("ul._34FDqXUubQC345dbhWBh3o li")

        for detail in cls.detail_info_list:

            soup = BeautifulSoup(detail, 'lxml')

            detail_infos = soup.select('div.wd-ui-cont')

            for item in detail_infos:
                amount, period = re.findall('금액(\S*)펀딩기간(\S*)',
                                            item.select_one('div.social-info + br + div p:nth-of-type(1)').get_text(
                                                strip=True))[0]
                total_amount = ''.join(re.findall(r'(\d)', amount))
                start_time, end_time = re.findall('(\S*)-(\S*)', period)[0]

                cls.reward_dict['start_time'] = start_time
                cls.reward_dict['end_time'] = end_time
                cls.reward_dict['total_amount'] = total_amount

            for content in ul_contents:
                product_name = content.select_one('a > h4').get_text(strip=True)

                product_type = content.select_one('a > span').get_text(strip=True)

                company_name = content.select_one('button > span').get_text(strip=True)

                total_amount = ''.join(
                    re.findall(r'(\d)', content.select_one('span:nth-of-type(5)').get_text(strip=True)))

                product_img = ''.join(
                    re.findall(r'url\("(\S*)"\)', content.select_one('div._3gmVBJTXNxBdKgoA_xSK3R').get('style')))

                cls.reward_dict['product_name'] = product_name
                cls.reward_dict['product_type'] = product_type
                cls.reward_dict['company_name'] = company_name
                cls.reward_dict['total_amount'] = total_amount
                cls.reward_dict['product_img'] = product_img

                Reward.objects.create(**cls.reward_dict)

    @classmethod
    def create_detail_html(cls):
        detail_url = 'https://www.wadiz.kr/web/campaign/detail/'
        detail_file_path = 'reward/data/detail/'
        file_path = 'reward/data/wadiz_reward_list.html'

        html = open(file_path, 'rt').read()
        soup = BeautifulSoup(html, 'lxml')

        detail_page = soup.select('ul._34FDqXUubQC345dbhWBh3o li')

        detail_list = []

        for page_num in detail_page:
            detail_page_id = ''.join(re.findall('detail/(\d*)', page_num.select_one('a').get('href')))
            detail_list.append(detail_page_id)

            if os.path.exists(f'{detail_file_path}{detail_page_id}.html'):
                html = open(f'{detail_file_path}{detail_page_id}.html', 'rt').read()
                cls.detail_info_list.append(html)

            else:
                response = requests.get(f'{detail_url}{detail_page_id}')
                html = response.text
                open(f'{detail_file_path}{detail_page_id}.html', 'wt').write(html)

    def __str__(self):
        return f'이름: {self.product_name} / 종류:{self.product_type} / 회사: {self.company_name} /' \
               f'이미지: {self.product_img} / 총금액:{self.total_amount} / 시작시간: {self.start_time} / 종료시간:{self.end_time}'
