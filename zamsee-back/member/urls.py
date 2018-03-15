from django.urls import path

from . import apis

app_name = 'member'

urlpatterns = [
    path('obtain_token/', apis.ObtainToken.as_view(), name='login'),
    path('signup/', apis.Signup.as_view(), name='signup'),
    path('activate/<path:token>/', apis.Activate.as_view(), name='activate'),
]

urlpatterns += [
    path('profile/<int:pk>/', apis.Dashboard.as_view(), name='dashboard'),
]
