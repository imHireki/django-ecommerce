from django.urls import path
from . import views


app_name = 'pedido'

urlpatterns = [
    path('salvarpedido/', views.SalvarPedido.as_view(), name='salvarpedido')
]
