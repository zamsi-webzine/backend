from django.contrib.auth import get_user_model
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView, RetrieveAPIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated, AllowAny

from .models import Post
from .pagination import PostPagination, ClientPostPagination
from .serializers import PostSerializer

User = get_user_model()


class PostCreateList(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    pagination_class = PostPagination
    parser_classes = (MultiPartParser, FormParser,)
    serializer_class = PostSerializer

    def get_queryset(self):
        return Post.objects.filter(author_id=self.kwargs['author_pk'])

    def perform_create(self, serializer):
        user = User.objects.get(pk=self.kwargs['author_pk'])
        return serializer.save(author=user)


class PostRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = PostSerializer
    parser_classes = (MultiPartParser, FormParser,)
    lookup_url_kwarg = 'post_pk'

    def get_queryset(self):
        queryset = Post.objects.all()
        return queryset.filter(author_id=self.kwargs['author_pk'])


class PostClientList(ListAPIView):
    permission_classes = (AllowAny,)
    pagination_class = ClientPostPagination
    parser_classes = (MultiPartParser, FormParser,)
    serializer_class = PostSerializer
    queryset = Post.objects.filter(is_published=True)


class PostClientRetrieve(RetrieveAPIView):
    permission_classes = (AllowAny,)
    parser_classes = (MultiPartParser, FormParser,)
    serializer_class = PostSerializer
    queryset = Post.objects.filter(is_published=True)
    lookup_field = 'id'
    lookup_url_kwarg = 'post_pk'


class PostClientListReView(ListAPIView):
    permission_classes = (AllowAny,)
    pagination_class = PostPagination
    parser_classes = (MultiPartParser, FormParser,)
    serializer_class = PostSerializer
    queryset = Post.objects.filter(is_published=True).filter(category='R')


class PostClientListEnterView(ListAPIView):
    permission_classes = (AllowAny,)
    pagination_class = PostPagination
    parser_classes = (MultiPartParser, FormParser,)
    serializer_class = PostSerializer
    queryset = Post.objects.filter(is_published=True).filter(category='E')


class PostClientListOverView(ListAPIView):
    permission_classes = (AllowAny,)
    pagination_class = PostPagination
    parser_classes = (MultiPartParser, FormParser,)
    serializer_class = PostSerializer
    queryset = Post.objects.filter(is_published=True).filter(category='O')
