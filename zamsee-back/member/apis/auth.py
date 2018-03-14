import json

from django.contrib.auth import authenticate, get_user_model
from django.http import HttpResponse
from rest_framework import status
from rest_framework_jwt.settings import api_settings
from rest_framework_jwt.views import JSONWebTokenAPIView

User = get_user_model()
jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


# JWToken 생성
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


# 회원가입
class Signup(JSONWebTokenAPIView):
    def post(self, request, *args, **kwargs):
        # 데이터 디코딩
        body_unicode = request.body.decode('utf-8')
        payload = json.loads(body_unicode)

        # 검증 1: 빈 값이 들어왔는가?
        if '' in list(payload.values()):
            data = {
                'message': 'Please fill out all of data'
            }

            return HttpResponse(json.dumps(data),
                                content_type='application/json; charset=utf-8',
                                status=status.HTTP_400_BAD_REQUEST)

        # payload에서 값 할당
        email = payload['email']
        nickname = payload['nickname']
        password1 = payload['password1']
        password2 = payload['password2']

        # queryset 호출
        queryset = User.objects.all()

        # 검증 2: 이메일이 이미 존재하는가?
        if queryset.filter(email=email).exists():
            data = {
                'message': 'This email is already exists'
            }

            return HttpResponse(json.dumps(data),
                                content_type='application/json; charset=utf-8',
                                status=status.HTTP_400_BAD_REQUEST)

        # 검증 3: 닉네임이 이미 존재하는가?
        elif queryset.filter(nickname=nickname).exists():
            data = {
                'message': 'This nickname is already exists'
            }

            return HttpResponse(json.dumps(data),
                                content_type='application/json; charset=utf-8',
                                status=status.HTTP_400_BAD_REQUEST)

        # 검증 4: 패스워드1, 2가 일치하는가?
        elif password1 != password2:
            data = {
                'message': 'Password confirmation is not correct'
            }

            return HttpResponse(json.dumps(data),
                                content_type='application/json; charset=utf-8',
                                status=status.HTTP_400_BAD_REQUEST)

        # 모든 검증을 통과하면 유저 생성
        else:
            user = User.objects.create_user(
                email=email,
                nickname=nickname,
                password=password2,
            )

            data = {
                'user': {
                    'email': user.email,
                    'nickname': user.nickname,
                    'is_active': user.is_active
                }
            }

            return HttpResponse(json.dumps(data),
                                content_type='application/json; charset=utf-8',
                                status=status.HTTP_200_OK)