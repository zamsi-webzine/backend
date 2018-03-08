from django.http import HttpResponse
from rest_framework.views import APIView


class Login(APIView):
    def get(self, request):
        return HttpResponse('<h1>Hello</h1>')