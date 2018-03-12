from django.urls import path

from .. import apis

app_name = 'member'
urlpatterns = [
    path('obtain_token/', apis.ObtainToken.as_view(), name='login'),
]
