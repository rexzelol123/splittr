from django.urls import path
from . import views


urlpatterns=[
    path('', views.index, name ='index'),                        
    path('create', views.create, name='create'),
    path('items', views.items, name='items'),
    path('compute2', views.compute2, name='compute2'),
    path('compute3', views.compute3, name='compute3'),
    path('compute4', views.compute4, name='compute4'),
    path('compute5', views.compute5, name='compute5'),
    path('compute6', views.compute6, name='compute6'),
    path('compute7', views.compute7, name='compute7'),
    path('compute8', views.compute8, name='compute8'),
    path('compute9', views.compute9, name='compute9'),
    path('compute10', views.compute10, name='compute10'),
    path('<str:participant_id>', views.display, name='display'),
]