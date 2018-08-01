from django.shortcuts import render
import os
from bs4 import BeautifulSoup
from selenium import webdriver
import re
import time
import requests

from reward.models import Reward

__all__ = (
    'reward_list',
)


def reward_list(request):

    if Reward.objects.count() < 10:
        WadizCrawler.get_reward_list()

    reward = Reward.objects.all()

    context = {
        'rewards': reward
    }

    return render(request, 'production/product-list.html', context)


class WadizCrawler:
    reward_dict = {
        'product_name': '',
        'product_type': '',
        'company_name': '',
        'product_img': '',
        'start_time': '',
        'end_time': '',
        'cur_amount': 0,
        'total_amount': 0,
        'interested_count': 0,
    }

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
    def get_reward_list(cls):
        file_path = 'reward/data/wadiz_reward_list.html'

        detail_file_path = 'reward/data/detail/'

        html = open(file_path, 'rt').read()

        soup = BeautifulSoup(html, 'lxml')

        ul_contents = soup.select("ul._34FDqXUubQC345dbhWBh3o li")

        # 메인페이지 html을 순회
        for content in ul_contents:
            product_name = content.select_one('a > h4').get_text(strip=True)

            product_type = content.select_one('a > span').get_text(strip=True)

            company_name = content.select_one('button > span').get_text(strip=True)

            product_img = ''.join(
                re.findall(r'url\("(\S*)"\)', content.select_one('div._3gmVBJTXNxBdKgoA_xSK3R').get('style')))

            # 메인페이지에서 해당 detail page의 id값을 추출
            detail_page_id = ''.join(re.findall('detail/(\d*)', content.select_one('a').get('href')))

            # 로컬에 저장된 detail(id).html을 참조하여 html을 읽음
            detail_html = open(f'{detail_file_path}{detail_page_id}.html', 'rt').read()

            # detail(id).html의 내용을 beautiful soup으로 파싱
            soup = BeautifulSoup(detail_html, 'lxml')

            # 목표금액, 기간정보를 가진 div 선택
            detail_info = soup.select_one('div.social-info + br + div p:nth-of-type(1)').get_text(strip=True)

            amount, period = re.findall('금액(\S*)펀딩기간(\S*)', detail_info)[0]
            total_amount = ''.join(re.findall(r'(\d)', amount))
            start_time, end_time = re.findall('(\S*)-(\S*)', period)[0]

            # 현재까지 펀딩된 금액
            cur_amount = ''.join(re.findall(r'(\d)', soup.select_one('p.total-amount > strong').get_text(strip=True)))

            # 현재까지 좋아요를 받은 개수
            interested_count = soup.select_one('em.cnt-like').get_text(strip=True)

            cls.reward_dict['product_name'] = product_name
            cls.reward_dict['product_type'] = product_type
            cls.reward_dict['company_name'] = company_name
            cls.reward_dict['product_img'] = product_img
            cls.reward_dict['start_time'] = start_time
            cls.reward_dict['end_time'] = end_time
            cls.reward_dict['cur_amount'] = int(cur_amount)
            cls.reward_dict['total_amount'] = int(total_amount)
            cls.reward_dict['interested_count'] = int(interested_count)

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
        return f'이름: {self.product_name} \n 종류:{self.product_type} \n 회사: {self.company_name} \n' \
               f'이미지: {self.product_img} \n 시작시간: {self.start_time} \n 종료시간:{self.end_time} \n' \
               f'펀딩된 금액: {self.cur_amount} \n 총금액:{self.total_amount} \n 좋아요개수: {self.interest_count}'
