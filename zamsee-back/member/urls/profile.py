from django.urls import path

from member import apis

app_name = 'member'

urlpatterns = [
    path('<int:pk>/', apis.Dashboard.as_view(), name='dashboard'),
    path('<int:pk>/thumbnail/', apis.ThumbnailUpdate.as_view(), name='thumbnail'),
]
