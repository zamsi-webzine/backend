import json
import random
import string

import jwt
from django.conf import settings
from django.contrib.auth import authenticate, get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse, HttpResponseRedirect
from django.template.loader import render_to_string
from rest_framework import status
from rest_framework_jwt.authentication import jwt_decode_handler
from rest_framework_jwt.settings import api_settings
from rest_framework_jwt.views import JSONWebTokenAPIView

from .. import tasks

User = get_user_model()
jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


# 로그인 / JWToken 생성
class SignIn(JSONWebTokenAPIView):
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


# 회원 가입
class Signup(JSONWebTokenAPIView):
    def post(self, request, *args, **kwargs):
        # 데이터 유효성 검증 함수
        def validate_user(user_info):
            payload_tuple = tuple(user_info.values())
            # 검증 1: 빈 값이 들어왔는가?
            if '' in payload_tuple:
                msg = {
                    'message': 'Please fill out all of data'
                }

                return msg

            # queryset 호출
            queryset = User.objects.all()

            # 검증 2: 이메일이 이미 존재하는가?
            if queryset.filter(email=payload_tuple[0]).exists():
                msg = {
                    'message': 'This email is already exists'
                }

                return msg

            # 검증 3: 닉네임이 이미 존재하는가?
            elif queryset.filter(nickname=payload_tuple[1]).exists():
                msg = {
                    'message': 'This nickname is already exists'
                }

                return msg

            # 검증 4: 패스워드1, 2가 일치하는가?
            elif payload_tuple[2] != payload_tuple[3]:
                msg = {
                    'message': 'Password confirmation is not correct'
                }

                return msg

            else:
                # 모든 검증을 통과하면 유저 생성
                user = User.objects.create_user(
                    email=payload_tuple[0],
                    nickname=payload_tuple[1],
                    password=payload_tuple[3],
                )

                return user

        # 데이터 이메일 전송 함수
        def sending_email(instance):
            # 토큰 생성
            auth_payload = jwt_payload_handler(instance)
            token = jwt_encode_handler(auth_payload)

            # 이메일 발송에 필요한 정보
            current_site = get_current_site(request)
            to_email = instance.email
            subject = '[Zamsee] 회원가입 인증 이메일'
            message = render_to_string('email/user_activate_email.html', {
                'domain': current_site.domain,
                'token': token
            })
            tasks.send_mail_task.delay(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                to_email,
            )

        # 데이터 디코딩
        body_unicode = request.body.decode('utf-8')
        payload = json.loads(body_unicode)

        # 유효성 검증
        result = validate_user(payload)

        # 유효성 검증 결과에 따른 결과
        if type(result) is not dict:
            sending_email(result)

            data = {
                'message': 'Please check your email to activate'
            }

            return HttpResponse(json.dumps(data),
                                content_type='application/json; charset=utf-8',
                                status=status.HTTP_201_CREATED)
        else:
            return HttpResponse(json.dumps(result),
                                content_type='application/json; charset=utf-8',
                                status=status.HTTP_400_BAD_REQUEST)


# 회원 활성화
class Activate(JSONWebTokenAPIView):
    def get(self, request, *args, **kwargs):
        # 토큰 유효성 검증 함수
        def validate_token(token):
            # Check payload valid (based off of JSONWebTokenAuthentication,
            # may want to refactor)
            try:
                payload = jwt_decode_handler(token)
            except jwt.ExpiredSignature:
                msg = {
                    'message': 'Signature has expired.'
                }
                return msg
            except jwt.DecodeError:
                msg = {
                    'message': 'Error decoding signature.'
                }
                return msg

            return payload

        result = validate_token(kwargs['token'])

        # 검증 결과 오류가 없다면 유저를 활성화시키고 메인 페이지로 리다이렉트
        if len(result) is not 1:
            queryset = User.objects.all()
            user = queryset.get(email=result['email'])
            user.is_active = True
            user.save()

            return HttpResponseRedirect('http://localhost:8080/profile/posts')

        else:
            return HttpResponse(json.dumps(result),
                                content_type='application/json; charset=utf-8',
                                status=status.HTTP_400_BAD_REQUEST)


# 비밀번호 재설정
class ResetPassword(JSONWebTokenAPIView):
    def post(self, request, *args, **kwargs):
        # 데이터 유효성 검증 함수
        def validate_user(user_info):
            # 검증 1: 빈 값이 들어왔는가?
            if '' in list(user_info.values()):
                msg = {
                    'message': 'Please fill out all of data'
                }

                return msg

            # payload에서 값 할당
            email = user_info['email']

            # queryset 호출
            queryset = User.objects.all()

            # 검증 2: 이메일이 이미 존재하는가?
            if not queryset.filter(email=email).exists():
                msg = {
                    'message': "This email is doesn't exist"
                }

                return msg

            else:
                # 모든 검증을 통과하면 유저 생성
                user = queryset.get(email=email)

                return user

        # 데이터 이메일 전송 함수
        def sending_email(instance):
            # 새 비밀번호 생성
            new_password = ''.join((random.choice(string.ascii_lowercase) for _ in range(8)))

            # 비밀번호 적용
            instance.set_password(new_password)
            instance.save()

            # 이메일 발송에 필요한 정보
            to_email = instance.email
            subject = '[Zamsee] 비밀번호 초기화 이메일'
            message = render_to_string('email/initalize_password.html', {
                'new_password': new_password
            })
            tasks.send_mail_task.delay(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                to_email,
            )

        # 데이터 디코딩
        body_unicode = request.body.decode('utf-8')
        payload = json.loads(body_unicode)

        result = validate_user(payload)

        # 유효성 검증 결과에 따른 결과
        if type(result) is not dict:
            sending_email(result)

            data = {
                'message': 'Please check your email to reset password'
            }

            return HttpResponse(json.dumps(data),
                                content_type='application/json; charset=utf-8',
                                status=status.HTTP_200_OK)
        else:
            return HttpResponse(json.dumps(result),
                                content_type='application/json; charset=utf-8',
                                status=status.HTTP_400_BAD_REQUEST)
