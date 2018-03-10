from django.contrib.auth import authenticate
from django.http import HttpResponse
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
            context = {
                'nickname': user.nickname
            }
            return Response(context)