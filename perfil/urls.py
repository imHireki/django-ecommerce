from django.urls import path
from . import views


app_name = 'perfil'

urlpatterns = [
    path('', views.CriarAtualizar.as_view(), name='criar'),
    # path('login/', views.Login.as_view(), name='login'),
    # path('logout/', views.Logout.as_view(), name='logout'),
]
