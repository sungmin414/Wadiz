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


class ProductDetail(mixins.RetrieveModelMixin, generics.GenericAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)