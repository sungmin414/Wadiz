from django.urls import path

from .. import apis

urlpatterns = [
    path('', apis.ProductList.as_view()),
    path('search/', apis.ProductCategoryList.as_view()),
    path('<int:pk>/', apis.ProductDetail.as_view()),
<<<<<<< HEAD
    path('<int:pk>/funding/', apis.ProductFundingList.as_view()),
    # path('item/', apis.RewardList.as_view()),
    # path('search/', apis.ProductFilterList.as_view()),
    # path('search/product/', apis.ProductOrderingList.as_view()),
=======

    path('item/', apis.RewardList.as_view()),
    path('search/', apis.ProductFilterList.as_view()),




>>>>>>> filter 수정
]
