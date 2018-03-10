from django.contrib.auth import authenticate
from django.http import HttpResponse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView


class Login(APIView):
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(
            email=email,
            password=password
        )
        if user:
            token, token_created = Token.objects.get_or_create(user=user)
            data = {
                'token': token.key
            }
            return Response(data, status=status.HTTP_200_OK)
        data = {
            'message': 'Invalid Credentials'
        }
        return Response(data, status=status.HTTP_401_UNAUTHORIZED)
