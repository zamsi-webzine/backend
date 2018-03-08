from django.urls import path

from .. import apis

urlpatterns = [
    path('login/', apis.Login.as_view(), name='login'),
]