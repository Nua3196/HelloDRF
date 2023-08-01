from rest_framework import viewsets, permissions, generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404 # get_object_or_404 불러오기
from .models import Book # 모델 불러오기
from .serializers import BookSerializer # 시리얼라이저 불러오기

# Create your views here.

# @api_view
# 데코레이터 <- 함수의 성격을 표시
# request 객체
# 요청을 효과적으로 처리하고 인증 기능을 구현할 때 편리함을 제공
# 요청 타입, 함께 보낸 데이터 등 해당 요청에 대한 정보를 담고 있음
# 이런 정보에 접근할 때 request를 사용
# ex)  요청 타입 request.method, 데이터 request.data로 접근
# Response 클래스
# DRF의 결과 반환 방식
# request와 마찬가지로 응답에 대한 정보를 담고 있음
# ex) 응답에 포함되는 데이터 response.data, 응답에 대한 상태 response.status
@api_view(['GET'])
def HelloAPI(request):
    return Response("hello world!")

@api_view(['GET', 'POST'])  # GET/POST 요청을 처리하게 만들어주는 데코레이터
def booksAPI(request):  # /book/
    if request.method == 'GET': # GET 요청 (도서 전체 정보)
        books = Book.objects.all()  # Book 모델로부터 전체 데이터 가져오기
        # 시리얼라이저에 전체 데이터를 한번에 집어넣기(직렬화, many=True)
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK) # return Response!
    elif request.method == 'POST':  
        # POST 요청으로 들어온 데이터를 시리얼라이저에 넣기
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():   # 유효한 데이터라면
            # 시리얼라이저의 역직렬화를 통해 save(), 모델시리얼라이저의 기본 create() 함수가 동작
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)    # 201 메시지를 보내며 성공!
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) # 400 잘못된 요청!
    
@api_view(['GET'])
def bookAPI(request, bid):  # /book/bid/
    book = get_object_or_404(Book, bid=bid) # bid = id 인 데이터를 Book에서 가져오고, 없으면 404 에러
    serializer = BookSerializer(book)   # 시리얼라이저에 데이터를 집어넣기(직렬화)
    return Response(serializer.data, status=status.HTTP_200_OK) # return Response!

class BooksAPI(APIView):
    def get(self, request):
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    def post(self, request):
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class BookAPI(APIView):
    def get(self, request, bid):
        book = get_object_or_404(Book, bid=bid)
        serializer = BookSerializer(book)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
from rest_framework import generics
from rest_framework import mixins

class BooksAPIMixins(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class BookAPIMixins(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    lookup_field = 'bid'

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
    

class BooksAPIGenerics(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class BookAPIGenerics(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    lookup_field = 'bid'

from rest_framework import viewsets

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer