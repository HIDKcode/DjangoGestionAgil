from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from datetime import date, timedelta
from .decorators import rol_requerido
from .models import Piezas
from .forms import PiezasForm
from .models import Usuarios
from django.db.models import F

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


@login_required(login_url='login')
def inventario_view(request):
    piezas = Piezas.objects.select_related('proveedor').all()
    return render(request, 'inventario.html', {
        'piezas': piezas
    })

@login_required
def pieza_crear(request):
    if request.method == 'POST':
        form = PiezasForm(request.POST)
        if form.is_valid():
            form.save()
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
            return redirect('inventario')
    else:
        form = PiezasForm(instance=pieza)
    return render(request, 'piezas/pieza_form.html', {'form': form, 'accion': 'Editar'})

@login_required
def pieza_eliminar(request, pieza_id):
    pieza = get_object_or_404(Piezas, id=pieza_id)
    if request.method == 'POST':
        pieza.delete()
        return redirect('inventario')
    return render(request, 'piezas/pieza_confirmar_eliminar.html', {'pieza': pieza})

@login_required(login_url='login')
def admin_view(request):
    if request.user.rol != 'admin':
        return redirect('login') 
    return render(request, 'admin.html')

 #accesible solo a admin y gerente
@login_required(login_url='login')
@rol_requerido(['admin', 'gerente'])
def home(request):
    return render(request, 'home.html')

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


@login_required(login_url='login')
@rol_requerido(['produccion', 'admin', 'gerente'])
def produccion_view(request):
    return render(request, 'produccion.html')


@login_required(login_url='login')
@rol_requerido(['auditor', 'admin', 'gerente'])
def auditoria_view(request):
    return render(request, 'auditoria.html')


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