from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

def login_view(request):
    if request.method == 'POST':
        usuario = request.POST.get('usuario')
        clave = request.POST.get('clave')

        if usuario == 'admin' and clave == 'admin':
            request.session['auth'] = True
            request.session['usuario'] = usuario
            request.session['rol'] = 'admin'
            return redirect('inventario')  # usa el nombre correcto aquí

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
    return redirect('/login')

def inventario_view(request):
    if not request.session.get('auth'):
        return redirect('login')
    return render(request, 'inventario.html')

def admin_view(request):
    usuario_actual = request.session.get('usuario_id')
    if not usuario_actual:
        return redirect('login')

    from .models import Usuarios
    try:
        usuario = Usuarios.objects.get(id=usuario_actual)
    except Usuarios.DoesNotExist:
        return redirect('login')

    if usuario.rol != 'admin':
        return redirect('no_acceso')

    usuarios = Usuarios.objects.all()
    return render(request, 'admin.html', {'usuarios': usuarios})