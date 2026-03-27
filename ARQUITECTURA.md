🏗️ ARQUITECTURA DE DOMICILIOS APP
==================================

## Diagrama General de la Arquitectura

```
┌─────────────────────────────────────────────────────────────┐
│                      USUARIO (Navegador)                     │
│                                                               │
│              http://localhost:8000 (Frontend)                │
└────────────────────────┬────────────────────────────────────┘
                         │
                         │ HTTP/JSON
                         │
        ┌────────────────▼────────────────┐
        │                                  │
        │  FRONTEND (HTML/CSS/JavaScript)  │
        │                                  │
        │  ├─ index.html                   │
        │  ├─ styles.css                   │
        │  └─ script.js                    │
        │                                  │
        │  Funcionalidades:                │
        │  ├─ Login/Registro               │
        │  ├─ Ver comercios y productos    │
        │  ├─ Carrito de compras           │
        │  ├─ Crear órdenes                │
        │  ├─ Ver órdenes                  │
        │  ├─ Panel de usuario             │
        │  └─ Panel de admin               │
        │                                  │
        └────────────────┬────────────────┘
                         │
                         │ Peticiones REST API
                         │
        ┌────────────────▼──────────────────────────────────┐
        │                                                    │
        │    BACKEND (Flask + Python)                       │
        │    http://127.0.0.1:5000/api                      │
        │                                                    │
        │  ┌──────────────────────────────────────────┐    │
        │  │ API Routes (Endpoints)                   │    │
        │  │                                          │    │
        │  │ /auth              - Autenticación      │    │  
        │  │ /usuarios          - Perfil de usuario  │    │
        │  │ /comercios         - Gestión comercios  │    │
        │  │ /productos         - Gestión productos  │    │
        │  │ /ordenes           - Gestión órdenes    │    │
        │  │ /admin             - Panel admin        │    │
        │  └──────────────────────────────────────────┘    │
        │                         │                         │
        │  ┌──────────────────────▼─────────────────────┐  │
        │  │ Models (Modelos de Datos)                 │  │
        │  │                                            │  │
        │  │ ├─ Usuario                                 │  │
        │  │ ├─ Comercio                                │  │
        │  │ ├─ Producto                                │  │
        │  │ ├─ Orden                                   │  │
        │  │ └─ ItemOrden                               │  │
        │  └──────────────────────┬─────────────────────┘  │
        │                         │                         │
        └─────────────────────────┼──────────────────────────┘
                                  │
                                  │ SQL
                                  │
                  ┌───────────────▼───────────────┐
                  │                               │
                  │   SQLite Database             │
                  │                               │
                  │   domicilios.db               │
                  │                               │
                  │   - usuarios tabla            │
                  │   - comercios tabla           │
                  │   - productos tabla           │
                  │   - ordenes tabla             │
                  │   - items_orden tabla         │
                  │                               │
                  └───────────────────────────────┘
```

---

## 📊 Diagrama de Entidades (BD)

```
┌─────────────────┐
│   USUARIOS      │
├─────────────────┤
│ id (PK)         │
│ nombre          │
│ email (UNIQUE)  │
│ telefono        │
│ password_hash   │
│ rol             │ ──┬──────────────┐
│ direccion       │  │ (CLIENTE,     │
│ ciudad          │  │  COMERCIO,    │
│ codigo_postal   │  │  ADMIN,       │
│ activo          │  │  REPARTIDOR) ─┘
│ fecha_creacion  │
└────────┬────────┘
         │ (1:1 relación con COMERCIOS)
         │
    ┌────▼──────────────────┐
    │                       │
┌───▼─────────────────┐    │
│   COMERCIOS         │◄───┘
├─────────────────────┤
│ id (PK)             │
│ nombre              │
│ descripcion         │
│ propietario_id (FK) │
│ telefono            │
│ email               │
│ direccion           │
│ ciudad              │
│ codigo_postal       │
│ horario_apertura    │
│ horario_cierre      │
│ activo              │
│ logo_url            │
│ categoria           │
│ calificacion        │
│ fecha_creacion      │
└────────┬────────────┘
         │ (1:N con PRODUCTOS)
         │
    ┌────▼──────────────────┐
    │                       │
┌───▼─────────────────┐    │
│   PRODUCTOS         │◄───┘
├─────────────────────┤
│ id (PK)             │
│ nombre              │
│ descripcion         │
│ precio              │
│ comercio_id (FK)    │
│ categoria           │
│ imagen_url          │
│ disponible          │
│ stock               │
│ fecha_creacion      │
└─────────────────────┘
         ▲
         │ (relación N:N a través de ITEMS_ORDEN)
         │
    ┌────┴──────────────────┐
    │                       │
┌───▼─────────────────┐    │
│   ITEMS_ORDEN       │────┘
├─────────────────────┤
│ id (PK)             │
│ orden_id (FK)       │
│ producto_id (FK)    │
│ cantidad            │
│ precio_unitario     │
│ subtotal            │
└─────────────────────┘
         ▲
         │
    ┌────┴──────────────────┐
    │                       │
┌───▼─────────────────┐    │
│   ORDENES           │────┘
├─────────────────────┤
│ id (PK)             │
│ numero_orden        │
│ cliente_id (FK)     │
│ comercio_id (FK)    │
│ estado              │
│ monto_total         │
│ direccion_entrega   │
│ notas               │
│ fecha_creacion      │
│ fecha_entrega       │
└─────────────────────┘

Estados de orden:
- pendiente
- confirmada
- en_preparacion
- en_ruta
- entregada
- cancelada
```

---

## 🔄 Flujo de Autenticación

```
1. Usuario entra a la app
   │
   ├─ ¿Token en localStorage?
   │  │
   │  ├─ Sí → Usuario autenticado (mostrar opciones de usuario)
   │  │
   │  └─ No → Mostrar botón de Login
   │
2. Usuario hace click en "Iniciar Sesión"
   │
3. Envía POST /api/auth/login
   │
4. Backend valida credenciales
   │
5. Si válidas:
   ├─ Genera JWT token
   ├─ Devuelve token + datos usuario
   │
6. Frontend:
   ├─ Guarda token en localStorage
   ├─ Guarda usuario en localStorage
   ├─ Actualiza UI (muestra opciones de usuario)
   │
7. En futuras peticiones:
   └─ Incluye header: Authorization: Bearer {token}
```

---

## 🛒 Flujo de Compra

```
Cliente
   │
   ├─ Ver Comercios
   │  └─ GET /api/comercios
   │
   ├─ Selecciona Comercio
   │  └─ GET /api/productos?comercio_id=1
   │
   ├─ Agrega productos al Carrito
   │  └─ Guardado en localStorage (sin servidor)
   │
   ├─ Ve el Carrito
   │  └─ Desde localStorage
   │
   ├─ Confirma Orden
   │  └─ POST /api/ordenes
   │     {
   │       comercio_id: 1,
   │       items: [{producto_id: 1, cantidad: 2}, ...],
   │       direccion_entrega: "...",
   │       notas: "..."
   │     }
   │
   ├─ Backend crea orden en BD
   │  ├─ Validar productos existan
   │  ├─ Calcular monto_total
   │  ├─ Crear registro Orden
   │  └─ Crear registros ItemOrden
   │
   └─ Frontend
      ├─ Vacía carrito
      ├─ Muestra confirmación
      └─ Redirige a "Mis Órdenes"
```

---

## 🔐 Seguridad

```
Autenticación:
├─ JWT (JSON Web Token)
├─ Token en Authorization header
└─ Expira en 30 días

Hashing:
├─ Contraseñas con Werkzeug
└─ Salt automático

Permisos:
├─ Cliente: Ver comercios, hacer órdenes
├─ Comercio: Crear/editar su comercio y productos
├─ Admin: Acceso total
└─ Validación en cada ruta
```

---

## 📦 Stack Tecnológico Resumido

```
Frontend:
- HTML5 (estructura)
- CSS3 (diseño y responsividad)
- JavaScript vanilla (lógica)
- LocalStorage (almacenamiento local)
- REST API (comunicación)

Backend:
- Python 3.8+
- Flask (framework web)
- SQLAlchemy (ORM)
- SQLite (base de datos)
- JWT (autenticación)
- CORS (cross-origin)
```

---

## 🚀 Despliegue (Futuro)

Para llevar a producción:

```
Frontend:
├─ Usar Webpack o Vite
├─ Minificar CSS/JS
├─ Desplegar en Netlify/Vercel
└─ HTTPS obligatorio

Backend:
├─ Usar Gunicorn/uWSGI
├─ Nginx como reverse proxy
├─ Base de datos PostgreSQL
├─ Variables de entorno (.env)
└─ Dominio personalizado
```

---

¡Arquitectura lista para crecer! 🏗️
