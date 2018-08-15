from rest_framework import generics, mixins, filters
from ..models import Product, Reward
from ..serializer import ProductSerializer, RewardSerializer, ProductDetailSerializer, ProductFundingSerializer
from utils.paginations import ProductListPagination
from django.db.models import Q


class ProductList(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = ProductListPagination


class ProductCategoryList(generics.ListAPIView):
    serializer_class = ProductSerializer
    pagination_class = ProductListPagination

    def get_queryset(self):
        category = self.request.query_params.get('category', None)
        product_name = self.request.query_params.get('product_name', None)
        # ordering = self.
        return Product.objects.filter(product_type__contains=category, product_name__contains=product_name)


class ProductFundingList(mixins.RetrieveModelMixin, generics.GenericAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductFundingSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class RewardList(generics.ListAPIView):
    queryset = Reward.objects.all()
    serializer_class = RewardSerializer


# 쿼리 매개 변수에 대한 필터링
class ProductFilterList(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('product_name',)


# 오름차순 내림차순 필터링
class ProductOrderingList(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = (filters.OrderingFilter,)
    ordering_fields = ('product_interested_count', 'product_cur_amount', 'product_end_time')


class ProductDetail(mixins.RetrieveModelMixin, generics.GenericAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
