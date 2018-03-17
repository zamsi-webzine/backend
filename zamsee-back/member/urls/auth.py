from django.urls import path

from member import apis

app_name = 'member'

urlpatterns = [
    path('signin/', apis.SignIn.as_view(), name='signin'),
    path('signup/', apis.Signup.as_view(), name='signup'),
    path('activate/<path:token>/', apis.Activate.as_view(), name='activate'),
    path('reset-password/', apis.ResetPassword.as_view(), name='reset_pwd'),
]
