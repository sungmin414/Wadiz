from django.shortcuts import render
import os
from bs4 import BeautifulSoup
from selenium import webdriver
import re
import time
import requests

from reward.models import Reward, Product

__all__ = (
    'reward_list',
)


def reward_list(request):
    # Product.objects.all().delete()

    print('리워드 실행')
    #
    if Product.objects.count() < 10:
        WadizCrawler.get_product_list()
        WadizCrawler.get_reward_list()

    product = Product.objects.all()

    context = {
        'products': product
    }

    return render(request, 'production/product-list.html', context)


class WadizCrawler:
    product_dict = {
        'product_name': '',
        'product_type': '',
        'product_company_name': '',
        'product_img': '',
        'product_start_time': '',
        'product_end_time': '',
        'product_cur_amount': 0,
        'product_total_amount': 0,
        'product_interested_count': 0,
        'product_description': '',
    }

    product_list = []

    product_no = []

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
    def get_product_list(cls):
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

            # detail 페이지 안의 description 내부의 html 내용을 담음
            description = soup.select_one('div.wd-ui-cont div.inner-contents')

            # 목표금액, 기간정보를 가진 div 선택
            detail_info = soup.select_one('div.social-info + br + div p:nth-of-type(1)').get_text(strip=True)

            amount, period = re.findall('금액(\S*)펀딩기간(\S*)', detail_info)[0]
            total_amount = ''.join(re.findall(r'(\d)', amount))
            start_time, end_time = re.findall('(\S*)-(\S*)', period)[0]

            # 현재까지 펀딩된 금액
            cur_amount = ''.join(re.findall(r'(\d)', soup.select_one('p.total-amount > strong').get_text(strip=True)))

            # 현재까지 좋아요를 받은 개수
            interested_count = soup.select_one('em.cnt-like').get_text(strip=True)

            cls.product_dict['product_name'] = product_name
            cls.product_dict['product_type'] = product_type
            cls.product_dict['product_company_name'] = company_name
            cls.product_dict['product_img'] = product_img
            cls.product_dict['product_start_time'] = start_time
            cls.product_dict['product_end_time'] = end_time
            cls.product_dict['product_cur_amount'] = int(cur_amount)
            cls.product_dict['product_total_amount'] = int(total_amount)
            cls.product_dict['product_interested_count'] = int(interested_count)
            cls.product_dict['product_description'] = str(description)
            cls.product_no.append(detail_page_id)
            cls.product_list.append(Product.objects.create(**cls.product_dict))

    @classmethod
    def get_reward_list(cls):

        detail_file_path = 'reward/data/detail/'

        # 각 product html 을 순회

        for i, product in enumerate(cls.product_list):
            detail_html = open(f'{detail_file_path}{cls.product_no[i]}.html', 'rt').read()

            soup = BeautifulSoup(detail_html, 'lxml')

            rewards = soup.select('div.wd-ui-gift button')

            for reward in rewards:

                reward_on_sale = True
                reward_price = ''.join(re.findall('(\d)', reward.select_one('dt').get_text(strip=True)))
                reward_name = reward.select_one('p.reward-name').get_text(strip=True)
                reward_option = reward.select_one('dd p:nth-of-type(2)').get_text(strip=True)
                reward_shipping_charge = ''.join(
                    re.findall('(\d)', reward.select_one('li.shipping em').get_text(strip=True)))
                reward_expecting_departure_date = reward.select_one('li.date em').get_text(strip=True)
                # 크롤링 데이터에서 수량이 매진되어 현재 개수와 총 개수를 파악 하기 어려울때, soldout 클래스 여부에따라 변수 할당결정
                reward_check = reward.select_one('p.reward-qty').get('class')
                reward_total_count = ''
                reward_sold_count = reward.select_one('p.reward-soldcount strong').get_text(strip=True)

                if 'soldout' in reward_check:
                    reward_on_sale = False
                    # 만약 다팔렸다면 팔린 개수와 총개수는 동일함
                    reward_total_count = reward_sold_count

                if reward_on_sale:
                    reward_total_count = reward.select_one('p.reward-qty strong').get_text(strip=True)

                Reward.objects.create(
                    reward_name=reward_name,
                    reward_option=reward_option,
                    reward_price=int(reward_price),
                    reward_shipping_charge=int(reward_shipping_charge),
                    reward_expecting_departure_date=reward_expecting_departure_date,
                    reward_total_count=int(reward_total_count),
                    reward_sold_count=int(reward_sold_count),
                    reward_on_sale=reward_on_sale,
                    product=product,
                )

                # print('가격: ', reward_price)
                # print('상품이름: ', reward_name)
                # print('배송비: ', reward_shipping_charge)
                # print('리워드 배송일: ', reward_expecting_departure_date)
                # print('총 개수:', reward_total)
                # print('펀딩된 수량: ', reward_sold_count)
                # print('펀딩 가능 여부: ', reward_on_sale)
                #
                # print('')

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
