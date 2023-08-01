from django.urls import path, include
from .views import HelloAPI, bookAPI, booksAPI, BookAPI, BooksAPI, BookAPIMixins, BooksAPIMixins

urlpatterns = [
    path("hello/", HelloAPI),
    path("fbv/books/", booksAPI),   # 함수형 뷰의 booksAPI 연결
    path("fbv/book/<int:bid>/", bookAPI),   # 함수형 뷰의 bookAPI 연결
    path("cbv/books/", BooksAPI.as_view()),
    path("cbv/book/<int:bid>/", BookAPI.as_view()),
    path("mixin/books/", BooksAPIMixins.as_view()),
    path("mixin/book/<int:bid>/", BookAPIMixins.as_view()),
]

from rest_framework import routers
from .views import BookViewSet

router = routers.SimpleRouter()
router.register('books', BookViewSet)
urlpatterns = router.urls