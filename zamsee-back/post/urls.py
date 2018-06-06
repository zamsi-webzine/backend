from django.urls import path

from . import apis

app_name = 'post'

urlpatterns = [
    path('<int:author_pk>/', apis.PostCreateList.as_view(), name='create_list'),
    path('<int:author_pk>/<int:post_pk>/', apis.PostRetrieveUpdateDestroy.as_view(), name='detail'),
    path('all/', apis.PostClientList.as_view(), name='all'),
    path('re/', apis.PostClientListReView.as_view(), name='re_view'),
    path('enter/', apis.PostClientListEnterView.as_view(), name='enter_view'),
    path('over/', apis.PostClientListOverView.as_view(), name='over_view'),
    path('<int:post_pk>/detail/', apis.PostClientRetrieve.as_view(), name='client_detail'),
]
