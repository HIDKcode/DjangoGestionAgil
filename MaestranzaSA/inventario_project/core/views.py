from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from datetime import date, timedelta
from .decorators import rol_requerido
from .models import Piezas, Usuarios, MovimientoInventario, Proyecto, AsignacionPieza
from .forms import PiezasForm
from django.db.models import F
from django.db import models

def login_view(request):
    if request.method == 'POST':
        usuario = request.POST.get('usuario')
        clave = request.POST.get('clave')
        user = authenticate(request, usuario=usuario, clave=clave)
        if user is not None:
            if user.bloqueado:
                return render(request, 'login.html', {'error': 'Tu cuenta está bloqueada. Contacta al administrador.'})
            login(request, user)
            return redirect('inventario')  
        else:
            return render(request, 'login.html', {'error': 'Credenciales inválidas'})
    else:
        return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def inventario_view(request):
    categoria = request.GET.get('categoria')
    piezas = Piezas.objects.select_related('proveedor')

    if categoria:
        piezas = piezas.filter(categoria=categoria)

    categorias = Piezas.objects.values_list('categoria', flat=True).distinct()

    return render(request, 'inventario.html', {
        'piezas': piezas,
        'categorias': categorias,
        'categoria_actual': categoria,
    })

@login_required
def pieza_crear(request):
    if request.method == 'POST':
        form = PiezasForm(request.POST)
        if form.is_valid():
            pieza = form.save()
            MovimientoInventario.objects.create(
                pieza=pieza,
                accion='CREADO',
                usuario=request.user,
                observacion='Pieza registrada en el sistema.'
            )
            return redirect('inventario')
    else:
        form = PiezasForm()
    return render(request, 'piezas/pieza_form.html', {'form': form, 'accion': 'Crear'})

@login_required
def pieza_editar(request, pieza_id):
    pieza = get_object_or_404(Piezas, id=pieza_id)
    if request.method == 'POST':
        form = PiezasForm(request.POST, instance=pieza)
        if form.is_valid():
            form.save()
            MovimientoInventario.objects.create(
                pieza=pieza,
                accion='EDITADO',
                usuario=request.user,
                observacion='Datos de la pieza actualizados.'
            )
            return redirect('inventario')
    else:
        form = PiezasForm(instance=pieza)
    return render(request, 'piezas/pieza_form.html', {'form': form, 'accion': 'Editar'})

@login_required(login_url='login')
def admin_view(request):
    if request.user.rol != 'admin':
        return redirect('login') 
    return render(request, 'admin.html')

 #accesible solo a admin y gerente
@login_required(login_url='login')
@rol_requerido(['admin', 'gerente'])
def home(request):
    return render(request, 'login.html')

@login_required(login_url='login')
@rol_requerido(['admin'])
def administrar_view(request):
    return render(request, 'admin.html')

@login_required(login_url='login')
@rol_requerido(['comprador', 'admin', 'gerente'])
def compras_view(request):
    return render(request, 'compras.html')


@login_required(login_url='login')
@rol_requerido(['logistica', 'admin', 'gerente'])
def logistica_view(request):
    return render(request, 'logistica.html')

# seccion proyectos

@login_required
@rol_requerido(['produccion', 'admin', 'gerente'])
def lista_proyectos(request):
    proyectos = Proyecto.objects.all()
    piezas = Piezas.objects.all()
    return render(request, 'produccion.html', {
        'proyectos': proyectos,
        'piezas': piezas,
    })

@login_required
@rol_requerido(['produccion', 'admin', 'gerente'])
def crear_proyecto(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        descripcion = request.POST.get('descripcion')

        if nombre:
            Proyecto.objects.create(nombre=nombre, descripcion=descripcion)
            return redirect('lista_proyectos')

    return render(request, 'crear_proyecto.html')

@login_required
@rol_requerido(['produccion', 'admin', 'gerente'])
def asignar_piezas_proyecto(request, proyecto_id):
    proyecto = get_object_or_404(Proyecto, id=proyecto_id)
    piezas = Piezas.objects.all()

    if request.method == 'POST':
        pieza_id = request.POST.get('pieza_id')
        cantidad = request.POST.get('cantidad')

        if pieza_id and cantidad:
            pieza = get_object_or_404(Piezas, id=pieza_id)
            cantidad = int(cantidad)

            asignacion, created = AsignacionPieza.objects.get_or_create(
                proyecto=proyecto,
                piezas=pieza,
                defaults={'cantidad': cantidad}
            )
            if not created:
                asignacion.cantidad = cantidad
                asignacion.save()

            messages.success(request, f'Pieza "{pieza.nombre}" asignada al proyecto "{proyecto.nombre}".')
            return redirect('lista_proyectos')

    return render(request, 'asignar_pieza.html', {
        'proyecto': proyecto,
        'piezas': piezas,
    })

@login_required
@rol_requerido(['produccion', 'admin', 'gerente'])
def crear_proyecto(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        descripcion = request.POST.get('descripcion')
        fecha_inicio = request.POST.get('fecha_inicio')
        fecha_fin = request.POST.get('fecha_fin')

        Proyecto.objects.create(
            nombre=nombre,
            descripcion=descripcion,
            fecha_inicio=fecha_inicio if fecha_inicio else None,
            fecha_fin=fecha_fin if fecha_fin else None,
        )
        return redirect('lista_proyectos')  # o la url que muestra la lista

    # Si quieres también manejar GET y mostrar formulario, devuelve render
    return render(request, 'crear_proyecto.html')
# fin seccion proyectos

@login_required(login_url='login')
@rol_requerido(['auditor', 'admin', 'gerente'])
def auditoria_view(request):
    historial = MovimientoInventario.objects.select_related('pieza', 'usuario').order_by('-fecha')[:50]
    return render(request, 'auditoria.html',{'historial': historial})


@login_required(login_url='login')
@rol_requerido(['planta', 'admin', 'gerente'])
def planta_view(request):
    return render(request, 'planta.html')

@login_required(login_url='login')
@rol_requerido(['inventario', 'admin', 'gerente'])
def alertas_view(request):
    # Stock bajo
    low_stock = Piezas.objects.filter(stock__lte=F('umbral_minimo'))

    # Vencimientos próximos (próximos 30 días)
    today = date.today()
    soon = today + timedelta(days=30)
    expiring_qs = Piezas.objects.filter(
        fecha_vencimiento__isnull=False,
        fecha_vencimiento__gte=today,
        fecha_vencimiento__lte=soon
    )

    # Preparamos lista con días restantes
    expiring_list = []
    for p in expiring_qs:
        days_left = (p.fecha_vencimiento - today).days
        expiring_list.append({
            'nombre': p.nombre,
            'fecha_vencimiento': p.fecha_vencimiento,
            'dias_restantes': days_left
        })

    return render(request, 'alertas.html', {
        'low_stock': low_stock,
        'expiring_list': expiring_list,
    })

@login_required(login_url='login')
@rol_requerido(['admin'])
def usuarios_list(request):
    usuarios = Usuarios.objects.all()
    return render(request, 'usuarios/lista.html', {'usuarios': usuarios})

@login_required(login_url='login')
@rol_requerido(['admin'])
def usuarios_crear(request):
    if request.method == 'POST':
        rut      = request.POST.get('rut')
        password = request.POST.get('password')
        rol      = request.POST.get('rol')
        bloqueado = True if request.POST.get('bloqueado') == 'on' else False
        intentos = int(request.POST.get('intentos') or 0)

        if Usuarios.objects.filter(rut=rut).exists():
            error = "Ya existe un usuario con ese RUT."
            return render(request, 'usuarios/crear.html', {'error': error})

        user = Usuarios.objects.create_user(
            rut=rut,
            password=password,
            rol=rol,
            bloqueado=bloqueado,
            intentos_fallidos=intentos
        )
        return redirect('usuarios_list')
    # GET
    return render(request, 'usuarios/crear.html', {
        'roles': Usuarios.ROLES
    })

def notfound(request):
    return render(request, 'notfound.html')