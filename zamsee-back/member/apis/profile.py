import json

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

User = get_user_model()

# 캐시 만료 시간 설정
CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


class Dashboard(APIView):
    # 인증 클래스
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    # 캐시 적용을 위한 데코레이터
    @method_decorator(cache_page(CACHE_TTL))
    def get(self, request, *args, **kwargs):
        # JWT와 함께 user pk를 필요로 한다
        user_pk = kwargs['pk']

        if cache.get('user_query') is not None:
            queryset = cache.get('user_query')
        else:
            queryset = User.objects.all()
            cache.set('user_query', queryset, CACHE_TTL)

        user = queryset.get(pk=user_pk)
        data = {
            'email': user.email,
            'nickname': user.nickname
        }

        return HttpResponse(json.dumps(data),
                            content_type='application/json; charset=utf-8',
                            status=status.HTTP_200_OK)
