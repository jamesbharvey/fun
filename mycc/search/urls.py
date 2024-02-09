from django.urls import path

from . import views

urlpatterns = [
    path('mongo', views.mongo, name='mongo'),
    path('elastic', views.elastic, name='elastic'),

]