from django.urls import path, include

urlpatterns = [

    path('users/', include('members.urls.apis')),
    path('rewards/', include('reward.urls.apis')),
]
