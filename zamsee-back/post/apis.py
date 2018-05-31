from django.contrib.auth import get_user_model
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated

from .models import Post
from .pagination import PostPagination
from .serializers import PostSerializer

User = get_user_model()


class PostCreateList(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    pagination_class = PostPagination
    parser_classes = (MultiPartParser, FormParser,)
    serializer_class = PostSerializer
    queryset = Post.objects.all()

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
