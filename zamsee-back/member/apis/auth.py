import json

from django.contrib.auth import authenticate
from django.http import HttpResponse
from rest_framework import status
from rest_framework_jwt.settings import api_settings
from rest_framework_jwt.views import JSONWebTokenAPIView

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


class ObtainToken(JSONWebTokenAPIView):
    def post(self, request, *args, **kwargs):
        # frontend에서 날아온 bytecode를 utf-8로 디코딩
        body_unicode = request.body.decode('utf-8')
        # 문자열을 json으로 불러옴
        payload = json.loads(body_unicode)

        # payload 값으로 유저 인증
        user = authenticate(
            email=payload['email'],
            password=payload['password']
        )

        # user가 인증 되면
        if user:
            # JWT 토큰 생성
            auth_payload = jwt_payload_handler(user)
            token = jwt_encode_handler(auth_payload)

            # frontend로 전송할 json 형식 만들기
            data = {
                'token': token,
                'user': {
                    'pk': user.pk,
                    'email': user.email,
                    'nickname': user.nickname
                }
            }

            # data를 json으로 압축해 전송
            return HttpResponse(json.dumps(data),
                                content_type='application/json; charset=utf-8',
                                status=status.HTTP_200_OK)

        # 그 외 정상적인 요청이 들어오지 않은 모든 경우
        data = {
            'message': 'Invalid Credentials'
        }

        return HttpResponse(json.dumps(data),
                            content_type='application/json; charset=utf-8',
                            status=status.HTTP_400_BAD_REQUEST)
