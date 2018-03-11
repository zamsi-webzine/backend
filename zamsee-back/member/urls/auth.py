from django.urls import path

from .. import apis

urlpatterns = [
    path('obtain_token/', apis.ObtainToken.as_view(), name='login'),
]