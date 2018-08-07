from rest_framework import generics

from ..models import Product
from ..serializer import ProductSerializer


class ProductList(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
