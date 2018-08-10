from rest_framework import generics, mixins

from ..models import Product, Reward
from ..serializer import ProductSerializer, RewardSerializer
from utils.paginations import ProductListPagination


class ProductList(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = ProductListPagination

    # def get_queryset(self):
    #     category = self.request.query_params.get('category', None)
    #     return Product.objects.filter(product_type__contains=category)


class ProductDetail(mixins.RetrieveModelMixin, generics.GenericAPIView):

    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class RewardList(generics.ListAPIView):
    queryset = Reward.objects.all()
    serializer_class = RewardSerializer


class RewardDetail(mixins.RetrieveModelMixin, generics.GenericAPIView):

    queryset = Reward.objects.all()
    serializer_class = RewardSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)