from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('login/', views.login_view),
    path('logout/', views.logout_view, name='logout'),
    path('inventario/', views.inventario_view, name='inventario'),
    path('administrar/', views.admin_view, name='administrar'),
    
    path('usuarios/crear/', views.usuarios_crear, name='usuarios_crear'),
]