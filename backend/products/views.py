from rest_framework import generics, mixins, permissions, authentication
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404


from .models import Product
from .serializers import ProductSerializer
from .permissions import IsStaffEditorPermission


class ProductListCreateAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    authenticated_classes = [authentication.SessionAuthentication,
                             authentication.TokenAuthentication]
    permission_classes = [permissions.IsAdminUser, IsStaffEditorPermission]

    def perform_create(self, serializer):
        title = serializer.validated_data.get('title')
        content = serializer.validated_data.get('content')
        if content is None:
            content = title
        serializer.save(content=content)


class ProductMixinView(mixins.ListModelMixin, mixins.RetrieveModelMixin,
                       mixins.CreateModelMixin, generics.GenericAPIView):

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'

    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        if pk:
            return self.retrieve(request, *args, **kwargs)
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        content = serializer.validated_data.get('content')
        if content == None:
            content = "My Name Is Ahmed Lotfe"
        serializer.save(content=content)


class ProductListAPIView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductDetailAPIView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductUpdateAPIView(generics.UpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def perform_update(self, serializer):
        instance = serializer.save()
        if instance.content is None:
            instance.content = instance.title


class ProductDeleteAPIView(generics.DestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def perform_destroy(self, instance):
        super().perform_destroy(instance)


@api_view(['GET', 'POST'])
def product_alt_view(request, pk=None, *args, **kwargs):
    method = request.method
    if method == 'GET':
        if pk:
            # get detail view
            obj = get_object_or_404(Product, pk=pk)
            data = ProductSerializer(obj, many=False).data
            return Response(data)
        # get list view
        queryset = Product.objects.all()
        data = ProductSerializer(queryset, many=True).data
        return Response(data)

    elif method == 'POST':
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            title = serializer.validated_data.get('title')
            content = serializer.validated_data.get('content')
            if content is None:
                content = title
            serializer.save(content=content)
            return Response(serializer.data)
        return Response({"Invalid": "Not good data"}, status=400)
