from django.shortcuts import render

import os
from bs4 import BeautifulSoup
from selenium import webdriver
import re
import time

from reward.models import Reward


def reward_list(request):

    if Reward.objects.count() < 10:
        WadizCrawler.get_item_list()

    reward = Reward.objects.all()

    context = {
        'rewards': reward
    }

    return render(request, 'production/product-list.html', context)


class WadizCrawler:

    def __init__(self, product_name, product_type, company_name, product_img, total_amount, period):
        self.product_name = product_name
        self.product_type = product_type
        self.company_name = company_name
        self.product_img = product_img
        self.total_amount = total_amount
        self.period = period

    @classmethod
    def start(cls):

        # requeset로 목록을 요청하여 html파일에 담고 저장
        url = 'https://www.wadiz.kr/web/campaign/detail/21408'

        file_path = 'data/wadiz_reward_list.html'

        # detail_path = 'data/wadiz_detail.html'

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

        wadiz_list = []

        ul_contents = soup.select("ul._34FDqXUubQC345dbhWBh3o li")

        for content in ul_contents:
            product_name = content.select_one('a > h4').get_text(strip=True)

            product_type = content.select_one('a > span').get_text(strip=True)

            company_name = content.select_one('button > span').get_text(strip=True)

            total_amount = ''.join(re.findall(r'(\d)', content.select_one('span:nth-of-type(5)').get_text(strip=True)))

            # date = content.select_one('span:nth-of-type(7)').get_text(strip=True)

            product_img = ''.join(
                re.findall(r'url\("(\S*)"\)', content.select_one('div._3gmVBJTXNxBdKgoA_xSK3R').get('style')))

            Reward.objects.create(
                product_name=product_name,
                product_type=product_type,
                company_name=company_name,
                product_img=product_img,
                total_amount=int(total_amount),
            )

        for item in wadiz_list:
            print(item)

    def __str__(self):
        return f'이름: {self.title} / 타입:{self.type1} / 타입2: {self.type2} / 가격: {self.cost} / 남은시간:{self.remain} '

# WadizCrawler.start()
# WadizCrawler.get_item_list()
