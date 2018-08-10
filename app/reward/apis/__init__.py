
import django_filters.rest_framework
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, mixins, filters

from rest_framework import generics, mixins
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView


from ..models import Product, Reward
from ..serializer import ProductSerializer, RewardSerializer, ProductDetailSerializer
from utils.paginations import ProductListPagination


class ProductList(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = ProductListPagination


class ProductCategoryList(generics.ListAPIView):
    serializer_class = ProductSerializer
    pagination_class = ProductListPagination

    def get_queryset(self):
        category = self.request.query_params.get('category', None)
        return Product.objects.filter(product_type__contains=category)


class RewardList(generics.ListAPIView):
    queryset = Reward.objects.all()
    serializer_class = RewardSerializer


# 쿼리 매개 변수에 대한 필터링
class ProductFilterList(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('product_name', )


# 오름차순 내림차순 필터링
class ProductOrderingList(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = (filters.OrderingFilter, )
    ordering_fields = ('product_interested_count', 'product_cur_amount', 'product_end_time')







class ProductDetail(mixins.RetrieveModelMixin, generics.GenericAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

