from django.contrib.auth import get_user_model
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView
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
