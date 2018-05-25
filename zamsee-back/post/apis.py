from django.contrib.auth import get_user_model
from rest_framework.generics import ListCreateAPIView
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
