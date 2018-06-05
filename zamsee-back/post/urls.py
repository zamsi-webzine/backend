from django.urls import path

from . import apis

app_name = 'post'

urlpatterns = [
    path('<int:author_pk>/', apis.PostCreateList.as_view(), name='create_list'),
    path('<int:author_pk>/<int:post_pk>/', apis.PostRetrieveUpdateDestroy.as_view(), name='detail'),
    path('all/', apis.PostClientList.as_view(), name='all'),
]
