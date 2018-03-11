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
        body_unicode = request.body.decode('utf-8')
        payload = json.loads(body_unicode)

        user = authenticate(
            email=payload['email'],
            password=payload['password']
        )

        if user:
            auth_payload = jwt_payload_handler(user)
            token = jwt_encode_handler(auth_payload)

            data = {
                'token': token,
                'user': {
                    'pk': user.pk,
                    'email': user.email,
                    'nickname': user.nickname
                }
            }

            return HttpResponse(json.dumps(data),
                                content_type='application/json; charset=utf-8',
                                status=status.HTTP_200_OK)

        data = {
            'message': 'Invalid Credentials'
        }

        return HttpResponse(json.dumps(data),
                            content_type='application/json; charset=utf-8',
                            status=status.HTTP_400_BAD_REQUEST)