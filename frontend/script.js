// Configuración
const API_URL = 'http://127.0.0.1:5000/api';
let token = localStorage.getItem('token');
let usuarioActual = token ? JSON.parse(localStorage.getItem('usuario') || '{}') : null;
let carrito = JSON.parse(localStorage.getItem('carrito') || '[]');
let comercioActual = null;

console.log('Script JavaScript cargado correctamente');
console.log('API_URL:', API_URL);
console.log('Token:', token ? 'Sí' : 'No');

// ========== INICIALIZACIÓN ==========
document.addEventListener('DOMContentLoaded', function () {
    console.log('DOM cargado - ejecutando inicialización');
    try {
        actualizarUI();
        cargarComercios();
    } catch (error) {
        console.error('Error durante la inicialización:', error);
    }
});

// ========== GESTIÓN DE PÁGINAS ==========
function mostrarPagina(nombrePagina) {
    console.log('Mostrando página:', nombrePagina);
    
    // Prevenir comportamiento por defecto
    if (event && event.preventDefault) {
        event.preventDefault();
    }
    
    // Ocultar todas las páginas
    document.querySelectorAll('.pagina').forEach(p => p.classList.remove('activa'));

    // Mostrar la página seleccionada
    const pagina = document.getElementById(`pagina-${nombrePagina}`);
    if (pagina) {
        pagina.classList.add('activa');
        console.log('Página mostrada:', nombrePagina);

        // Cargar datos específicos
        if (nombrePagina === 'comercios') {
            cargarComercios();
        } else if (nombrePagina === 'ordenes') {
            cargarMisOrdenes();
        } else if (nombrePagina === 'miCuenta') {
            cargarPerfil();
        } else if (nombrePagina === 'admin') {
            cargarAdmin();
        }
    } else {
        console.error('Página no encontrada:', `pagina-${nombrePagina}`);
    }
}

function cambiarTab(tab) {
    console.log('Cambiando tab a:', tab);
    
    document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('activo'));
    document.querySelectorAll('.tab-content').forEach(content => content.classList.remove('activo'));

    // Encontrar y activar el botón correcto
    const btns = document.querySelectorAll('.tab-btn');
    btns.forEach(btn => {
        if (btn.textContent.toLowerCase().includes(tab === 'login' ? 'iniciar' : 'registr')) {
            btn.classList.add('activo');
        }
    });
    
    const formulario = document.getElementById(`${tab}Form`);
    if (formulario) {
        formulario.classList.add('activo');
        console.log('Tab activado:', tab);
    } else {
        console.error('Formulario no encontrado:', `${tab}Form`);
    }
}

// ========== AUTENTICACIÓN ==========
function handleLogin(event) {
    event.preventDefault();

    const email = document.getElementById('loginEmail').value;
    const password = document.getElementById('loginPassword').value;

    fetch(`${API_URL}/auth/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password })
    })
        .then(res => res.json())
        .then(data => {
            if (data.access_token) {
                token = data.access_token;
                usuarioActual = data.usuario;
                localStorage.setItem('token', token);
                localStorage.setItem('usuario', JSON.stringify(usuarioActual));
                actualizarUI();
                mostrarPagina('inicio');
                document.getElementById('loginForm').reset();
            } else {
                mostrarError('loginError', data.mensaje || 'Error en el login');
            }
        })
        .catch(error => mostrarError('loginError', 'Error de conexión'));
}

function handleRegistro(event) {
    event.preventDefault();

    const data = {
        nombre: document.getElementById('regNombre').value,
        email: document.getElementById('regEmail').value,
        password: document.getElementById('regPassword').value,
        telefono: document.getElementById('regTelefono').value,
        direccion: document.getElementById('regDireccion').value,
        ciudad: document.getElementById('regCiudad').value,
        rol: document.getElementById('regRol').value
    };

    fetch(`${API_URL}/auth/registro`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    })
        .then(res => res.json())
        .then(data => {
            if (data.access_token) {
                token = data.access_token;
                usuarioActual = data.usuario;
                localStorage.setItem('token', token);
                localStorage.setItem('usuario', JSON.stringify(usuarioActual));
                actualizarUI();
                mostrarPagina('inicio');
                document.getElementById('registroForm').reset();
            } else {
                mostrarError('registroError', data.mensaje || 'Error en el registro');
            }
        })
        .catch(error => mostrarError('registroError', 'Error de conexión'));
}

function logout() {
    token = null;
    usuarioActual = null;
    localStorage.removeItem('token');
    localStorage.removeItem('usuario');
    carrito = [];
    localStorage.removeItem('carrito');
    actualizarUI();
    mostrarPagina('inicio');
}

function actualizarUI() {
    console.log('Actualizando UI...');
    const loginNav = document.getElementById('loginNav');
    const logoutNav = document.getElementById('logoutNav');
    const misCuentaNav = document.getElementById('misCuentaNav');
    const misOrdenesNav = document.getElementById('misOrdenesNav');
    const adminNav = document.getElementById('adminNav');

    console.log('Elementos de navegación encontrados:', {
        loginNav: !!loginNav,
        logoutNav: !!logoutNav,
        misCuentaNav: !!misCuentaNav,
        misOrdenesNav: !!misOrdenesNav,
        adminNav: !!adminNav
    });

    if (token && usuarioActual) {
        loginNav.style.display = 'none';
        logoutNav.style.display = 'block';
        misCuentaNav.style.display = 'block';
        misOrdenesNav.style.display = 'block';

        if (usuarioActual.rol === 'admin') {
            adminNav.style.display = 'block';
        } else {
            adminNav.style.display = 'none';
        }
    } else {
        loginNav.style.display = 'block';
        logoutNav.style.display = 'none';
        misCuentaNav.style.display = 'none';
        misOrdenesNav.style.display = 'none';
        adminNav.style.display = 'none';
    }

    actualizarCarrito();
    console.log('UI actualizada');
}

// ========== COMERCIOS ==========
function cargarComercios() {
    console.log('Cargando comercios...');
    fetch(`${API_URL}/comercios`)
        .then(res => {
            console.log('Respuesta de comercios:', res.status);
            return res.json();
        })
        .then(comercios => {
            console.log('Comercios recibidos:', comercios);
            const container = document.getElementById('comerciosList');
            if (!container) {
                console.error('Contenedor comerciosList no encontrado');
                return;
            }
            container.innerHTML = '';

            comercios.forEach(comercio => {
                const card = document.createElement('div');
                card.className = 'comercio-card';
                card.onclick = () => verDetalleComercio(comercio.id);

                const emoji = ['🍔', '🏪', '⚕️', '🚬', '📚', '👕'][Math.floor(Math.random() * 6)];

                card.innerHTML = `
                    <div class="comercio-banner">${emoji}</div>
                    <div class="comercio-info">
                        <h3>${comercio.nombre}</h3>
                        <p>${comercio.descripcion || 'Sin descripción'}</p>
                        <span class="comercio-categoria">${comercio.categoria || 'General'}</span>
                        <div class="comercio-calificacion">⭐ ${comercio.calificacion.toFixed(1)}</div>
                    </div>
                `;

                container.appendChild(card);
            });
        })
        .catch(error => console.error('Error cargando comercios:', error));
}

function verDetalleComercio(comercioId) {
    fetch(`${API_URL}/comercios/${comercioId}`)
        .then(res => res.json())
        .then(comercio => {
            comercioActual = comercio;
            cargarProductosPorComercio(comercioId);
            mostrarPagina('comercio-detalle');
        })
        .catch(error => console.error('Error:', error));
}

function cargarProductosPorComercio(comercioId) {
    fetch(`${API_URL}/productos?comercio_id=${comercioId}`)
        .then(res => res.json())
        .then(productos => {
            const container = document.getElementById('comercioDetalleContainer');

            const html = `
                <div class="comercio-detalle">
                    <div class="comercio-header">
                        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); height: 200px; border-radius: 8px; display: flex; align-items: center; justify-content: center; color: white; font-size: 4rem;">
                            ${['🍔', '🏪', '⚕️', '🚬', '📚', '👕'][Math.floor(Math.random() * 6)]}
                        </div>
                        <div class="comercio-header-info">
                            <h2>${comercioActual.nombre}</h2>
                            <p><strong>Descripción:</strong> ${comercioActual.descripcion || 'N/A'}</p>
                            <p><strong>Dirección:</strong> ${comercioActual.direccion}</p>
                            <p><strong>Teléfono:</strong> ${comercioActual.telefono || 'N/A'}</p>
                            <p><strong>Horario:</strong> ${comercioActual.horario_apertura || '09:00'} - ${comercioActual.horario_cierre || '21:00'}</p>
                            <p><strong>Categoría:</strong> ${comercioActual.categoria || 'General'}</p>
                            <div class="comercio-calificacion">⭐ ${comercioActual.calificacion.toFixed(1)}</div>
                        </div>
                    </div>

                    <h3>Productos Disponibles</h3>
                    <div class="productos-list">
                        ${productos.map(producto => `
                            <div class="producto-card">
                                <div class="producto-imagen">📦</div>
                                <h4>${producto.nombre}</h4>
                                <p>${producto.descripcion || 'Sin descripción'}</p>
                                <div class="producto-precio">$${producto.precio.toFixed(2)}</div>
                                <p><small>${producto.stock > 0 ? `Stock: ${producto.stock}` : 'Sin stock'}</small></p>
                                <div class="producto-agregar">
                                    <input type="number" id="cant-${producto.id}" value="1" min="1" max="${producto.stock}">
                                    <button class="btn btn-primary" onclick="agregarAlCarrito(${producto.id}, '${producto.nombre}', ${producto.precio})">Agregar</button>
                                </div>
                            </div>
                        `).join('')}
                    </div>
                </div>
            `;

            container.innerHTML = html;
        })
        .catch(error => console.error('Error:', error));
}

// ========== CARRITO ==========
function agregarAlCarrito(productoId, nombre, precio) {
    const cantidad = parseInt(document.getElementById(`cant-${productoId}`).value);

    // Verificar si el comercio es el mismo
    if (comercioActual && (carrito.length === 0 || carrito[0].comercio_id === comercioActual.id)) {
        const itemExistente = carrito.find(item => item.producto_id === productoId);

        if (itemExistente) {
            itemExistente.cantidad += cantidad;
        } else {
            carrito.push({
                producto_id: productoId,
                nombre: nombre,
                precio: precio,
                cantidad: cantidad,
                comercio_id: comercioActual.id
            });
        }

        localStorage.setItem('carrito', JSON.stringify(carrito));
        actualizarCarrito();
        alert(`${nombre} agregado al carrito`);
    } else {
        alert('No puedes agregar productos de diferentes comercios. Vacía el carrito primero.');
    }
}

function actualizarCarrito() {
    const count = carrito.length;
    document.getElementById('carritoCount').textContent = count;

    const carritoVacio = document.getElementById('carritoVacio');
    const carritoLleno = document.getElementById('carritoLleno');

    if (carrito.length === 0) {
        carritoVacio.style.display = 'block';
        carritoLleno.style.display = 'none';
    } else {
        carritoVacio.style.display = 'none';
        carritoLleno.style.display = 'block';

        const tbody = document.getElementById('carritoBody');
        tbody.innerHTML = '';
        let total = 0;

        carrito.forEach((item, index) => {
            const subtotal = item.precio * item.cantidad;
            total += subtotal;

            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${item.nombre}</td>
                <td>$${item.precio.toFixed(2)}</td>
                <td><input type="number" value="${item.cantidad}" min="1" onchange="actualizarCantidad(${index}, this.value)"></td>
                <td>$${subtotal.toFixed(2)}</td>
                <td><button class="btn btn-danger" onclick="eliminarDelCarrito(${index})">Eliminar</button></td>
            `;
            tbody.appendChild(row);
        });

        document.getElementById('totalCarrito').textContent = total.toFixed(2);
    }
}

function actualizarCantidad(index, cantidad) {
    cantidad = parseInt(cantidad);
    if (cantidad > 0) {
        carrito[index].cantidad = cantidad;
        localStorage.setItem('carrito', JSON.stringify(carrito));
        actualizarCarrito();
    }
}

function eliminarDelCarrito(index) {
    carrito.splice(index, 1);
    localStorage.setItem('carrito', JSON.stringify(carrito));
    actualizarCarrito();
}

function vaciarCarrito() {
    if (confirm('¿Deseas vaciar el carrito?')) {
        carrito = [];
        localStorage.removeItem('carrito');
        actualizarCarrito();
        mostrarPagina('comercios');
    }
}

function confirmarOrden() {
    if (!token || token === 'null') {
        alert('Debes iniciar sesión para confirmar la orden');
        mostrarPagina('login');
        return;
    }

    if (carrito.length === 0) {
        alert('El carrito está vacío');
        return;
    }

    if (!carrito[0].comercio_id) {
        alert('Error: No se pudo determinar el comercio');
        return;
    }

    const direccion = document.getElementById('direccionEntrega').value;
    const notas = document.getElementById('notasOrden').value;

    if (!direccion.trim()) {
        alert('Debes ingresar una dirección de entrega');
        return;
    }

    const items = carrito.map(item => ({
        producto_id: item.producto_id,
        cantidad: item.cantidad
    }));

    const ordenData = {
        comercio_id: carrito[0].comercio_id,
        items: items,
        direccion_entrega: direccion,
        notas: notas
    };

    console.log('Enviando orden:', ordenData);
    console.log('Token:', token);

    fetch(`${API_URL}/ordenes`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(ordenData)
    })
        .then(res => {
            if (!res.ok) {
                console.error('Error al crear orden:', res.status, res.statusText);
                if (res.status === 401 || res.status === 422) {
                    alert('Sesión inválida o expirada. Por favor, inicia sesión nuevamente.');
                    logout();
                    return;
                }
                return res.text().then(text => {
                    try {
                        const data = JSON.parse(text);
                        alert('Error: ' + (data.mensaje || 'Error al crear la orden'));
                    } catch {
                        alert(`Error ${res.status}: ${res.statusText}`);
                    }
                });
            }
            return res.json();
        })
        .then(data => {
            if (data && data.orden) {
                alert(`¡Orden confirmada!\nNúmero de orden: ${data.orden.numero_orden}`);
                carrito = [];
                localStorage.removeItem('carrito');
                actualizarCarrito();
                mostrarPagina('ordenes');
                cargarMisOrdenes();
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error al confirmar la orden');
        });
}

// ========== PERFIL Y COMERCIO ==========
function cargarPerfil() {
    if (!token || token === 'null') {
        mostrarPagina('login');
        return;
    }

    fetch(`${API_URL}/usuarios/perfil`, {
        headers: { 'Authorization': `Bearer ${token}` }
    })
        .then(res => {
            if (!res.ok) {
                console.error('Error al cargar perfil:', res.status, res.statusText);
                if (res.status === 401 || res.status === 422) {
                    alert('Sesión inválida o expirada. Por favor, inicia sesión nuevamente.');
                    logout();
                    return;
                }
                return res.json().then(data => {
                    alert('Error al cargar perfil: ' + (data.mensaje || res.statusText));
                });
            }
            return res.json();
        })
        .then(usuario => {
            if (!usuario || typeof usuario !== 'object') {
                console.error('Respuesta inválida para perfil:', usuario);
                return;
            }
            document.getElementById('perfil-nombre').value = usuario.nombre;
            document.getElementById('perfil-email').value = usuario.email;
            document.getElementById('perfil-telefono').value = usuario.telefono || '';
            document.getElementById('perfil-direccion').value = usuario.direccion || '';
            document.getElementById('perfil-ciudad').value = usuario.ciudad || '';
            document.getElementById('perfil-codigoPostal').value = usuario.codigo_postal || '';

            // Si es comercio, cargar datos del comercio
            if (usuario.rol === 'comercio') {
                cargarDatosComercio(usuario.id);
            }
        })
        .catch(error => console.error('Error:', error));
}

function cargarDatosComercio(userId) {
    fetch(`${API_URL}/comercios`)
        .then(res => res.json())
        .then(comercios => {
            const comercio = comercios.find(c => c.propietario_id === userId);
            if (comercio) {
                document.getElementById('com-nombre').value = comercio.nombre;
                document.getElementById('com-descripcion').value = comercio.descripcion || '';
                document.getElementById('com-telefono').value = comercio.telefono || '';
                document.getElementById('com-email').value = comercio.email || '';
                document.getElementById('com-direccion').value = comercio.direccion;
                document.getElementById('com-ciudad').value = comercio.ciudad || '';
                document.getElementById('com-codigoPostal').value = comercio.codigo_postal || '';
                document.getElementById('com-apertura').value = comercio.horario_apertura || '';
                document.getElementById('com-cierre').value = comercio.horario_cierre || '';
                document.getElementById('com-categoria').value = comercio.categoria || '';
            }
        })
        .catch(error => console.error('Error:', error));
}

function handleActualizarPerfil(event) {
    event.preventDefault();

    const datos = {
        nombre: document.getElementById('perfil-nombre').value,
        email: document.getElementById('perfil-email').value,
        telefono: document.getElementById('perfil-telefono').value,
        direccion: document.getElementById('perfil-direccion').value,
        ciudad: document.getElementById('perfil-ciudad').value,
        codigo_postal: document.getElementById('perfil-codigoPostal').value
    };

    fetch(`${API_URL}/usuarios/perfil`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(datos)
    })
        .then(res => res.json())
        .then(data => {
            if (data.usuario) {
                usuarioActual = data.usuario;
                localStorage.setItem('usuario', JSON.stringify(usuarioActual));
                mostrarExito('perfilSuccess', 'Perfil actualizado correctamente');
            } else {
                mostrarError('perfilError', data.mensaje || 'Error al actualizar');
            }
        })
        .catch(error => mostrarError('perfilError', 'Error de conexión'));
}

function handleGuardarComercio(event) {
    event.preventDefault();

    const datos = {
        nombre: document.getElementById('com-nombre').value,
        descripcion: document.getElementById('com-descripcion').value,
        telefono: document.getElementById('com-telefono').value,
        email: document.getElementById('com-email').value,
        direccion: document.getElementById('com-direccion').value,
        ciudad: document.getElementById('com-ciudad').value,
        codigo_postal: document.getElementById('com-codigoPostal').value,
        horario_apertura: document.getElementById('com-apertura').value,
        horario_cierre: document.getElementById('com-cierre').value,
        categoria: document.getElementById('com-categoria').value
    };

    // Determinar si es crear o actualizar
    const url = usuarioActual.rol === 'comercio'
        ? `${API_URL}/comercios/1`
        : `${API_URL}/comercios`;

    const metodo = usuarioActual.rol === 'comercio' ? 'PUT' : 'POST';

    fetch(url, {
        method: metodo,
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(datos)
    })
        .then(res => res.json())
        .then(data => {
            if (data.comercio || data.mensaje) {
                mostrarExito('comercioSuccess', 'Comercio guardado correctamente');
                if (!usuarioActual.rol === 'comercio') {
                    usuarioActual.rol = 'comercio';
                    localStorage.setItem('usuario', JSON.stringify(usuarioActual));
                    actualizarUI();
                }
            } else {
                mostrarError('comercioError', data.mensaje || 'Error al guardar');
            }
        })
        .catch(error => mostrarError('comercioError', 'Error de conexión'));
}

// ========== ÓRDENES ==========
function cargarMisOrdenes() {
    if (!token || token === 'null') {
        mostrarPagina('login');
        return;
    }

    fetch(`${API_URL}/ordenes`, {
        headers: { 'Authorization': `Bearer ${token}` }
    })
        .then(res => {
            if (!res.ok) {
                console.error('Error al cargar órdenes:', res.status, res.statusText);
                if (res.status === 401 || res.status === 422) {
                    alert('Sesión inválida o expirada. Por favor, inicia sesión nuevamente.');
                    logout();
                    return;
                }
                return res.json().then(data => {
                    alert('Error al cargar órdenes: ' + (data.mensaje || res.statusText));
                });
            }
            return res.json();
        })
        .then(ordenes => {
            if (!ordenes || !Array.isArray(ordenes)) {
                console.error('Respuesta inválida para órdenes:', ordenes);
                return;
            }
            const container = document.getElementById('ordenesList');
            container.innerHTML = '';

            if (ordenes.length === 0) {
                container.innerHTML = '<p>No tienes órdenes aún</p>';
                return;
            }

            ordenes.forEach(orden => {
                const card = document.createElement('div');
                card.className = 'orden-card';

                const estadoClass = `estado-${orden.estado}`;

                card.innerHTML = `
                    <div class="orden-header">
                        <span class="orden-numero">${orden.numero_orden}</span>
                        <span class="orden-estado ${estadoClass}">${orden.estado.toUpperCase()}</span>
                    </div>
                    <div class="orden-info">
                        <p><strong>Monto:</strong> $${orden.monto_total.toFixed(2)}</p>
                        <p><strong>Entrega:</strong> ${orden.direccion_entrega}</p>
                        <p><strong>Fecha:</strong> ${new Date(orden.fecha_creacion).toLocaleString()}</p>
                    </div>
                    <div class="orden-items">
                        <h5>Artículos:</h5>
                        <ul>
                            ${orden.items.map(item => `
                                <li>${item.producto_nombre} x${item.cantidad} = $${item.subtotal.toFixed(2)}</li>
                            `).join('')}
                        </ul>
                    </div>
                    ${orden.notas ? `<p><strong>Notas:</strong> ${orden.notas}</p>` : ''}
                `;

                container.appendChild(card);
            });
        })
        .catch(error => console.error('Error:', error));
}

// ========== ADMIN ==========
function cargarAdmin() {
    if (!token || usuarioActual.rol !== 'admin') {
        mostrarPagina('inicio');
        return;
    }

    // Cargar estadísticas
    fetch(`${API_URL}/admin/estadisticas`, {
        headers: { 'Authorization': `Bearer ${token}` }
    })
        .then(res => res.json())
        .then(stats => {
            const container = document.getElementById('estadisticas');
            container.innerHTML = `
                <div class="stat-card">
                    <h3>Total Usuarios</h3>
                    <div class="number">${stats.total_usuarios}</div>
                </div>
                <div class="stat-card">
                    <h3>Total Comercios</h3>
                    <div class="number">${stats.total_comercios}</div>
                </div>
                <div class="stat-card">
                    <h3>Total Productos</h3>
                    <div class="number">${stats.total_productos}</div>
                </div>
                <div class="stat-card">
                    <h3>Total Órdenes</h3>
                    <div class="number">${stats.total_ordenes}</div>
                </div>
                <div class="stat-card">
                    <h3>Monto Total</h3>
                    <div class="number">$${stats.monto_total.toFixed(2)}</div>
                </div>
            `;
        })
        .catch(error => console.error('Error:', error));

    // Cargar usuarios
    fetch(`${API_URL}/admin/usuarios`, {
        headers: { 'Authorization': `Bearer ${token}` }
    })
        .then(res => res.json())
        .then(usuarios => {
            const container = document.getElementById('usuariosList');
            const html = `
                <table class="usuarios-table">
                    <thead>
                        <tr>
                            <th>Nombre</th>
                            <th>Email</th>
                            <th>Rol</th>
                            <th>Teléfono</th>
                            <th>Activo</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${usuarios.map(u => `
                            <tr>
                                <td>${u.nombre}</td>
                                <td>${u.email}</td>
                                <td>${u.rol}</td>
                                <td>${u.telefono || '-'}</td>
                                <td>${u.activo ? 'Sí' : 'No'}</td>
                            </tr>
                        `).join('')}
                    </tbody>
                </table>
            `;
            container.innerHTML = html;
        })
        .catch(error => console.error('Error:', error));
}

// ========== FUNCIONES AUXILIARES ==========
function mostrarError(elementId, mensaje) {
    const element = document.getElementById(elementId);
    element.textContent = mensaje;
    element.classList.add('show');
    setTimeout(() => {
        element.classList.remove('show');
    }, 5000);
}

function mostrarExito(elementId, mensaje) {
    const element = document.getElementById(elementId);
    element.textContent = mensaje;
    element.classList.add('show');
    setTimeout(() => {
        element.classList.remove('show');
    }, 5000);
}
