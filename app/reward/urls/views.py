from django.urls import path
from .. import views

urlpatterns = [
    path('', views.reward_list, name='reward-list'),

]
