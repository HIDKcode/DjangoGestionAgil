from django.urls import path
from . import views

urlpatterns = [
    path('login/',            views.login_view,     name='login'),
    path('logout/',           views.logout_view,    name='logout'),
    path('',                  views.home,           name='home'),
    path('inventario/',       views.inventario_view,name='inventario'),
    path('piezas/crear/', views.pieza_crear, name='pieza_crear'),
    path('piezas/<int:pieza_id>/editar/', views.pieza_editar, name='pieza_editar'),
    path('compras/',          views.compras_view,   name='compras'),
    path('logistica/',        views.logistica_view, name='logistica'),
    
    path('auditoria/',        views.auditoria_view, name='auditoria'),
    path('planta/',           views.planta_view,    name='planta'),
    path('administrar/',      views.administrar_view, name='administrar'),
    path('alertas/',          views.alertas_view,   name='alertas'),
    path('usuarios/',         views.usuarios_list,  name='usuarios_list'),
    path('usuarios/crear/',   views.usuarios_crear, name='usuarios_crear'),
    path('produccion/', views.lista_proyectos, name='lista_proyectos'),
    path('proyecto/<int:proyecto_id>/asignar_pieza/', views.asignar_piezas_proyecto, name='asignar_piezas_proyecto'),
    path('proyectos/crear/', views.crear_proyecto, name='crear_proyecto'),
    path('notfound/',         views.notfound,       name='notfound'),
]