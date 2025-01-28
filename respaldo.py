#Vista basa en funciones, las cuales nos permiten crear, actualizar, listar y eliminar informacion, mediante la implementacion de una API

@api_view(["GET"])
def ProductList(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)

@api_view(["GET"])
def ProductDetail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    serializer = ProductSerializer(product)
    return Response(serializer.data)


@api_view(["GET"])
def OrderList(request):
    orders = Order.objects.all()
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)



@api_view(['GET'])
def ProductsInfo(request):
    products = Product.objects.all()
    serializer = ProductInfoSerializer({
        'products': products,
        'count': len(products),
        'max_price': products.aggregate(max_price=Max('price'))['max_price']
    })
    return Response(serializer.data)


#Vistas basadas en clases.
class ProductListCreateAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.order_by('pk')
    serializer_class = ProductSerializer

    filterset_class = ProductFilter
    filter_backends = [
        DjangoFilterBackend, 
        filters.SearchFilter, 
        filters.OrderingFilter,
        #InStockFilterBackend

    ]

    search_fields = ['name', 'description']
    ordering_fields = ['name', 'price', 'stock']

    pagination_class = PageNumberPagination
    pagination_class.page_size = 9
    pagination_class.page_query_param = 'pagenum'
    pagination_class.page_size_query_param ='size'
    pagination_class.max_page_size =10

    def get_permissions(self):
        self.permission_classes = [AllowAny]
        if self.request.method == 'POST':
            self.permission_classes = [IsAuthenticated]
        elif self.request.method == 'GET':
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()


class ProductDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.filter(stock__gt=0)
    serializer_class = ProductSerializer


class OrderListAPIView(generics.ListAPIView):
    queryset = Order.objects.prefetch_related('items__product')
    serializer_class = OrderSerializer


class UserOrderListAPIView(generics.ListAPIView):
    queryset = Order.objects.prefetch_related('items__product')
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(user=self.request.user)


class ProductInfoAPIView(APIView):
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductInfoSerializer({
            'products': products,
            'count': len(products),
            'max_price': products.aggregate(max_price=Max('price'))['max_price']
        })
        return Response(serializer.data)




class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.order_by('pk')
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]
    
    filterset_class = ProductFilter
    filter_backends = [
        DjangoFilterBackend, 
        filters.SearchFilter, 
        filters.OrderingFilter,
        #filters,InStockFilterBackend

    ]

    search_fields = ['name', 'description']
    ordering_fields = ['name', 'price', 'stock']
    
    pagination_class = PageNumberPagination
    pagination_class.page_size = 9
    pagination_class.page_query_param = 'pagenum'
    pagination_class.page_size_query_param ='size'
    pagination_class.max_page_size = 10
    
    def get_permissions(self):
        self.permission_classes = [AllowAny]

        if self.request.method == 'POST':
            self.permission_classes = [IsAuthenticated]

        elif self.request.method in ['PUT', 'PATCH', 'DELETE']:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()



#Esto es un avance
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]

    @action(
        detail=False, 
        methods=['GET'], 
        url_path='product_list', 
        permission_classes = [IsAuthenticated]
    )
    def ProductList(self, request):
        pass

    def ProductDetail(self, request, pk):
        pass