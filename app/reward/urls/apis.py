from django.urls import path

from .. import apis

urlpatterns = [
    path('', apis.ProductList.as_view()),
    path('<int:pk>/', apis.ProductDetail.as_view()),
    path('item/', apis.RewardList.as_view()),

]
