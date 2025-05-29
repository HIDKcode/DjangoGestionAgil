from django.shortcuts import render, redirect
from .models import Usuarios

def login_view(request):
    if request.method == 'POST':
        usuario = request.POST.get('usuario')
        clave = request.POST.get('clave')

        if usuario == 'admin' and clave == 'admin':
            request.session['auth'] = True
            request.session['usuario'] = usuario
            request.session['rol'] = 'admin'
            return redirect('administrar') 

        elif usuario == 'trabajador' and clave == 'trabajador':
            request.session['auth'] = True
            request.session['usuario'] = usuario
            request.session['rol'] = 'trabajador'
            return redirect('inventario')

        else:
            return render(request, 'login.html', {'error': 'Credenciales inválidas'})

    return render(request, 'login.html')


def logout_view(request):
    request.session.flush()
    return redirect('login')


def inventario_view(request):
    if not request.session.get('auth'):
        return redirect('login')
    return render(request, 'inventario.html')


def admin_view(request):
    if not request.session.get('auth'):
        return redirect('login')

    if request.session.get('rol') != 'admin':
        return redirect('no_acceso')

    return render(request, 'admin.html')

def usuarios_crear(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        rut = request.POST.get('rut')
        contrasena = request.POST.get('contrasena')
        rol = request.POST.get('rol')

        if not (nombre and rut and contrasena and rol):
            return render(request, 'usuarios/crear.html', {'error': 'Todos los campos son obligatorios'})

        if Usuarios.objects.filter(rut=rut).exists():
            return render(request, 'usuarios/crear.html', {'error': 'El RUT ya está registrado'})

        Usuarios.objects.create(
            nombre=nombre,
            rut=rut,
            contrasena=contrasena,  # Luego hay que ver para que no sea visible
            rol=rol
        )
        return redirect('admin_view') 

    return render(request, 'usuarios/crear.html')