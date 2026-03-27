# 🚚 Plataforma de Domicilios - DOMICILIOS APP

Una plataforma web completa para pedidos de domicilios con front-end, back-end, base de datos SQLite y estilos modernos.

## 📋 Características

- ✅ **Autenticación y Registro** - Usuarios con roles: Cliente, Comercio, Repartidor, Admin
- ✅ **Gestión de Comercios** - Crear, editar y listar comercios
- ✅ **Catálogo de Productos** - Productos con precios, descripción e imágenes
- ✅ **Carrito de Compras** - Agregar productos y crear órdenes
- ✅ **Sistema de Órdenes** - Crear, rastrear y actualizar estado
- ✅ **Panel de Administración** - Estadísticas y gestión de usuarios
- ✅ **Perfil de Usuario** - Actualizar datos personales
- ✅ **Responsive Design** - Funciona en móviles y escritorio

## 🛠️ Tecnologías Utilizadas

### Backend
- **Python 3.8+**
- **Flask** - Framework web
- **Flask-SQLAlchemy** - ORM para base de datos
- **Flask-JWT-Extended** - Autenticación con JWT
- **Flask-CORS** - Soporte para CORS
- **SQLite** - Base de datos

### Frontend
- **HTML5** - Estructura
- **CSS3** - Estilos modernos y responsive
- **JavaScript Vanilla** - Lógica del cliente
- **LocalStorage** - Almacenamiento local de carrito y sesión

## 📦 Instalación

### 1. Clonar o descargar el proyecto

```bash
cd "c:\Users\NICOA\Nicolas\Vs Code\DOMICILIOS APP"
```

### 2. Configurar el Backend

#### Crear un entorno virtual (opcional pero recomendado)
```bash
python -m venv venv
# En Windows
venv\Scripts\activate
# En Linux/Mac
source venv/bin/activate
```

#### Instalar dependencias
```bash
cd backend
pip install -r requirements.txt
```

#### Crear archivo .env (opcional)
```bash
# Crear archivo .env en la carpeta backend
echo FLASK_ENV=development > .env
echo FLASK_DEBUG=True >> .env
```

### 3. Ejecutar el Backend

```bash
# Desde la carpeta backend
python main.py
```

El servidor estará disponible en: `http://127.0.0.1:5000`

### 4. Servir el Frontend

Opción 1: Usar Python (recomendado)
```bash
cd frontend
python -m http.server 8000
```

Opción 2: Usar VS Code Live Server
- Click derecho en `index.html` → "Open with Live Server"

Opción 3: Usar Node.js (si está instalado)
```bash
cd frontend
npx http-server
```

El frontend estará disponible en: `http://localhost:8000`

## 🚀 Uso de la Plataforma

### Como Cliente
1. Registrarse con roles "Cliente"
2. Ver comercios disponibles
3. Seleccionar un comercio para ver productos
4. Agregar productos al carrito
5. Confirmar orden
6. Ver mis órdenes

### Como Comercio
1. Registrarse con rol "Comercio"
2. Crear/editar información del comercio en "Mi Cuenta"
3. Agregar productos desde el panel
4. Ver órdenes recibidas
5. Actualizar estado de órdenes

### Como Administrador
1. Acceso con usuario admin (ver base de datos)
2. Ver estadísticas
3. Gestionar usuarios
4. Ver todas las órdenes

## 📁 Estructura del Proyecto

```
DOMICILIOS APP/
├── backend/
│   ├── app/
│   │   ├── __init__.py       # Inicialización de Flask
│   │   ├── models.py         # Modelos de BD (Usuario, Comercio, Producto, Orden)
│   │   └── routes.py         # Rutas API (Auth, Comercios, Productos, Órdenes, Admin)
│   ├── config.py             # Configuración de la aplicación
│   ├── main.py               # Punto de entrada
│   ├── requirements.txt       # Dependencias Python
│   └── domicilios.db         # Base de datos SQLite (se crea automáticamente)
│
└── frontend/
    ├── index.html            # Página principal
    ├── styles.css            # Estilos CSS
    └── script.js             # Lógica JavaScript
```

## 🔌 API Endpoints

### Autenticación
- `POST /api/auth/registro` - Registrar usuario
- `POST /api/auth/login` - Iniciar sesión

### Usuarios
- `GET /api/usuarios/perfil` - Obtener perfil
- `PUT /api/usuarios/perfil` - Actualizar perfil

### Comercios
- `GET /api/comercios` - Listar comercios
- `GET /api/comercios/<id>` - Obtener comercio
- `POST /api/comercios` - Crear comercio
- `PUT /api/comercios/<id>` - Actualizar comercio

### Productos
- `GET /api/productos` - Listar productos
- `GET /api/productos/<id>` - Obtener producto
- `POST /api/productos` - Crear producto
- `PUT /api/productos/<id>` - Actualizar producto

### Órdenes
- `POST /api/ordenes` - Crear orden
- `GET /api/ordenes` - Listar órdenes
- `GET /api/ordenes/<id>` - Obtener orden
- `PUT /api/ordenes/<id>/estado` - Actualizar estado

### Admin
- `GET /api/admin/usuarios` - Listar usuarios
- `GET /api/admin/estadisticas` - Obtener estadísticas

## 🔐 Seguridad

- Contraseñas hasheadas con Werkzeug
- Autenticación JWT
- CORS habilitado
- Validación de permisos en rutas protegidas

## 📝 Datos de Prueba

Para probar la aplicación, registra usuarios con estos roles:

1. **Cliente** - Para comprar productos
2. **Comercio** - Para vender productos
3. **Admin** - Para administración (requiere actualización manual en BD)

## 🐛 Solución de Problemas

### El backend no inicia
- Verificar que Python esté instalado: `python --version`
- Instalar dependencias: `pip install -r requirements.txt`
- Puerto 5000 en uso: cambiar puerto en `main.py`

### CORS error en el frontend
- Verificar que Flask-CORS esté instalado
- Revisar que `CORS(app)` esté en `app/__init__.py`

### Base de datos vacía
- La base de datos se crea automáticamente al iniciar
- Si hay error, eliminar `domicilios.db` y reiniciar

## 📞 Soporte

Para reportar errores o sugerencias, contacta al desarrollador.

## 📄 Licencia

Este proyecto está disponible bajo licencia libre.

---

**¡Feliz uso de la plataforma de domicilios!** 🚀
