from django.urls import path

from .. import apis

urlpatterns = [
    path('', apis.UserList.as_view()),
    path('login-auth-token/', apis.AuthToken.as_view()),
    path('detail/<int:pk>/', apis.UserDetail.as_view()),
    path('sign-up/', apis.UserList.as_view()),
    path('activate/', apis.UserActivate.as_view()),

    path('createtest/', apis.CreateTest.as_view()),
]
