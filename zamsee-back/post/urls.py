from django.urls import path

from . import apis

app_name = 'post'

urlpatterns = [
    path('<int:author_pk>/', apis.PostCreateList.as_view(), name='create_list'),
]
