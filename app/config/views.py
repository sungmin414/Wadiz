from django.shortcuts import render

from reward.models import Reward


def index(request):
    # TEMPLATE 설정 app/template 추

    reward = Reward.objects.all()

    context = {
        'rewards': reward
    }

    # if Reward.objects.count() < 10:
    #     WadizCrawler.get_item_list()

    return render(request, 'production/product-list.html', context)

    # return render(request, 'index.html')
