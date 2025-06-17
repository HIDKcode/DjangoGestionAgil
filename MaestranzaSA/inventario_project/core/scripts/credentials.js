function iniciarSesion(usuario, clave) {
    fetch('/api/login/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')  // CSRF obligatorio
        },
        body: JSON.stringify({
            username: usuario,
            password: clave
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            localStorage.setItem('auth', 'true');
            localStorage.setItem('usuario', data.username);
            localStorage.setItem('rol', data.rol);
            window.location.href = "/vistas/menu/inventario.html";
        } else {
            alert("Credenciales inválidas");
        }
    })
    .catch(error => {
        console.error("Error:", error);
        alert("Error en el servidor");
    });
}

// Utilidad para CSRF
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
