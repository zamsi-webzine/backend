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

    def get(self, request, *args, **kwargs):
        # 쿼리셋 호출
        queryset = User.objects.all()

        # frontend에서 동적으로 매핑된 user_id 값을 pk 값으로 가져온다
        user_pk = kwargs['pk']

        user = queryset.get(pk=user_pk)
        data = {
            'email': user.email,
            'nickname': user.nickname
        }

        return HttpResponse(json.dumps(data),
                            content_type='application/json; charset=utf-8',
                            status=status.HTTP_200_OK)

    def patch(self, request, *args, **kwargs):
        # 데이터 유효성 검증 함수
        def validate_user(user_info, query):
            # 검증 1: 빈 값이 들어왔는가? (닉네임과 패스워드 1이 함께 비어있는가?)
            payload_list = list(user_info.values())
            if payload_list[0] and payload_list[1] and payload_list[2] is '':
                msg = {
                    'message': 'Please fill out all of data'
                }

                return msg

            # 검증 2: 닉네임이 이미 존재하는가?
            elif query.filter(nickname=payload_list[0]).exists():
                msg = {
                    'message': 'This nickname is already exists'
                }

                return msg

            # 검증 3: 패스워드1, 2가 일치하는가? (빈 값이어도 상관 없음)
            elif payload_list[1] != payload_list[2]:
                msg = {
                    'message': 'Password confirmation is not correct'
                }

                return msg

            # 모든 검증을 마치면 빈 값을 지운다
            elif '' in payload_list:
                payload_list.remove('')

            return tuple(payload_list)

        # 데이터 디코딩
        body_unicode = request.body.decode('utf-8')
        payload = json.loads(body_unicode)

        # 쿼리셋 호출 및 유저 추적
        queryset = User.objects.all()
        user_pk = kwargs['pk']
        user = queryset.get(pk=user_pk)

        # 데이터 유효성 검증
        is_validated = validate_user(payload, queryset)

        # 검증 여부에 따른 리턴 값 결정
        if type(is_validated) is dict:
            return HttpResponse(json.dumps(is_validated),
                                content_type='application/json; charset=utf-8',
                                status=status.HTTP_400_BAD_REQUEST)
        # 요소가 3개일 경우: 닉네임, 패스워드 모두 변경
        elif len(is_validated) is 3:
            user.nickname = is_validated[0]
            user.set_password(is_validated[-1])
            user.save()
        # 요소가 2개일 경우: 닉네임이 지워졌다고 판단, 패스워드 설정
        elif len(is_validated) is 2:
            user.set_password(is_validated[-1])
            user.save()
        # 요소가 1개일 경우: 패스워드가 지워졌다고 판단, 닉네임 설정
        elif len(is_validated) is 1:
            user.nickname = is_validated[0]
            user.save()

        result = {
            'message': 'User information is modified successfully'
        }

        return HttpResponse(json.dumps(result),
                            content_type='application/json; charset=utf-8',
                            status=status.HTTP_206_PARTIAL_CONTENT)
