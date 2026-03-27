📡 EJEMPLOS DE USO DE API - DOMICILIOS APP
==========================================

## 🔑 Autenticación

### Registro de nuevo usuario
```
POST http://127.0.0.1:5000/api/auth/registro
Content-Type: application/json

{
  "nombre": "Carlos López",
  "email": "carlos@example.com",
  "password": "password123",
  "telefono": "3001234567",
  "direccion": "Calle 10 #5-50",
  "ciudad": "Bogotá",
  "codigo_postal": "110111",
  "rol": "cliente"
}

Respuesta (201):
{
  "mensaje": "Usuario registrado exitosamente",
  "usuario": {
    "id": 5,
    "nombre": "Carlos López",
    "email": "carlos@example.com",
    "telefono": "3001234567",
    "rol": "cliente",
    "direccion": "Calle 10 #5-50",
    "ciudad": "Bogotá",
    "codigo_postal": "110111",
    "activo": true,
    "fecha_creacion": "2024-03-27T10:30:00"
  },
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

### Login
```
POST http://127.0.0.1:5000/api/auth/login
Content-Type: application/json

{
  "email": "cliente1@example.com",
  "password": "cliente123"
}

Respuesta (200):
{
  "mensaje": "Sesión iniciada exitosamente",
  "usuario": {
    "id": 2,
    "nombre": "Juan Pérez",
    "email": "cliente1@example.com",
    "telefono": "3001234567",
    "rol": "cliente",
    "ciudad": "Bogotá",
    "activo": true
  },
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

---

## 👤 Usuarios

### Obtener perfil
```
GET http://127.0.0.1:5000/api/usuarios/perfil
Authorization: Bearer {access_token}

Respuesta (200):
{
  "id": 2,
  "nombre": "Juan Pérez",
  "email": "cliente1@example.com",
  "telefono": "3001234567",
  "rol": "cliente",
  "direccion": "Calle 10 #5-50",
  "ciudad": "Bogotá",
  "codigo_postal": "110111",
  "activo": true,
  "fecha_creacion": "2024-03-27T10:00:00"
}
```

### Actualizar perfil
```
PUT http://127.0.0.1:5000/api/usuarios/perfil
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "nombre": "Juan Pedro Pérez",
  "telefono": "3009876543",
  "direccion": "Carrera 7 #100-50",
  "ciudad": "Medellín"
}

Respuesta (200):
{
  "mensaje": "Perfil actualizado",
  "usuario": { ... }
}
```

---

## 🏪 Comercios

### Listar comercios
```
GET http://127.0.0.1:5000/api/comercios

Respuesta (200):
[
  {
    "id": 1,
    "nombre": "Pizza Italia",
    "descripcion": "Deliciosas pizzas artesanales",
    "telefono": "3105555555",
    "email": "pizzeria@example.com",
    "direccion": "Calle 80 #19-50, Bogotá",
    "ciudad": "Bogotá",
    "horario_apertura": "11:00",
    "horario_cierre": "23:00",
    "activo": true,
    "categoria": "Comida",
    "calificacion": 4.8,
    "fecha_creacion": "2024-03-27T10:00:00"
  },
  ...
]
```

### Obtener detalle de comercio
```
GET http://127.0.0.1:5000/api/comercios/1

Respuesta (200):
{
  "id": 1,
  "nombre": "Pizza Italia",
  ...
}
```

### Crear comercio (Como usuario autenticado)
```
POST http://127.0.0.1:5000/api/comercios
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "nombre": "Burger King Local",
  "descripcion": "Las mejores hamburguesas",
  "telefono": "3107777777",
  "email": "burgers@example.com",
  "direccion": "Calle 50 #10-20",
  "ciudad": "Bogotá",
  "codigo_postal": "110221",
  "horario_apertura": "10:00",
  "horario_cierre": "22:00",
  "categoria": "Comida Rápida"
}

Respuesta (201):
{
  "mensaje": "Comercio creado exitosamente",
  "comercio": { ... }
}
```

### Actualizar comercio
```
PUT http://127.0.0.1:5000/api/comercios/1
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "descripcion": "Deliciosas pizzas artesanales con ingredientes premium",
  "telefono": "3105555556"
}

Respuesta (200):
{
  "mensaje": "Comercio actualizado",
  "comercio": { ... }
}
```

---

## 📦 Productos

### Listar productos
```
GET http://127.0.0.1:5000/api/productos
GET http://127.0.0.1:5000/api/productos?comercio_id=1

Respuesta (200):
[
  {
    "id": 1,
    "nombre": "Pizza Margherita",
    "descripcion": "Tomate, mozzarella y albahaca",
    "precio": 18.99,
    "comercio_id": 1,
    "categoria": "Pizza",
    "disponible": true,
    "stock": 50,
    "fecha_creacion": "2024-03-27T10:00:00"
  },
  ...
]
```

### Obtener producto
```
GET http://127.0.0.1:5000/api/productos/1

Respuesta (200):
{
  "id": 1,
  "nombre": "Pizza Margherita",
  ...
}
```

### Crear producto (Como comerciante)
```
POST http://127.0.0.1:5000/api/productos
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "nombre": "Pizza Especial Vegetariana",
  "descripcion": "Con vegetales frescos de la estación",
  "precio": 22.99,
  "categoria": "Pizza",
  "stock": 30,
  "imagen_url": "https://example.com/pizza.jpg"
}

Respuesta (201):
{
  "mensaje": "Producto creado exitosamente",
  "producto": { ... }
}
```

### Actualizar producto
```
PUT http://127.0.0.1:5000/api/productos/1
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "precio": 25.99,
  "stock": 45,
  "disponible": true
}

Respuesta (200):
{
  "mensaje": "Producto actualizado",
  "producto": { ... }
}
```

---

## 🛒 Órdenes

### Crear orden (Como cliente)
```
POST http://127.0.0.1:5000/api/ordenes
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "comercio_id": 1,
  "items": [
    {
      "producto_id": 1,
      "cantidad": 2
    },
    {
      "producto_id": 2,
      "cantidad": 1
    }
  ],
  "direccion_entrega": "Calle 10 #5-50, Apartamento 302",
  "notas": "Sin cebolla por favor"
}

Respuesta (201):
{
  "mensaje": "Orden creada exitosamente",
  "orden": {
    "id": 1,
    "numero_orden": "ORD-20240327103000-2",
    "cliente_id": 2,
    "comercio_id": 1,
    "estado": "pendiente",
    "monto_total": 56.97,
    "direccion_entrega": "Calle 10 #5-50, Apartamento 302",
    "notas": "Sin cebolla por favor",
    "fecha_creacion": "2024-03-27T10:30:00",
    "items": [
      {
        "id": 1,
        "orden_id": 1,
        "producto_id": 1,
        "producto_nombre": "Pizza Margherita",
        "cantidad": 2,
        "precio_unitario": 18.99,
        "subtotal": 37.98
      },
      ...
    ]
  }
}
```

### Obtener orden
```
GET http://127.0.0.1:5000/api/ordenes/1
Authorization: Bearer {access_token}

Respuesta (200):
{
  "id": 1,
  "numero_orden": "ORD-20240327103000-2",
  ...
}
```

### Listar mis órdenes
```
GET http://127.0.0.1:5000/api/ordenes
Authorization: Bearer {access_token}

Respuesta (200):
[
  {
    "id": 1,
    "numero_orden": "ORD-20240327103000-2",
    ...
  }
]
```

### Actualizar estado de orden (Como comercio)
```
PUT http://127.0.0.1:5000/api/ordenes/1/estado
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "estado": "en_preparacion"
}

Estados válidos:
- pendiente
- confirmada
- en_preparacion
- en_ruta
- entregada
- cancelada

Respuesta (200):
{
  "mensaje": "Estado actualizado",
  "orden": { ... }
}
```

---

## 🔒 Admin

### Obtener estadísticas
```
GET http://127.0.0.1:5000/api/admin/estadisticas
Authorization: Bearer {access_token_admin}

Respuesta (200):
{
  "total_usuarios": 5,
  "total_comercios": 2,
  "total_productos": 10,
  "total_ordenes": 3,
  "monto_total": 156.97
}
```

### Listar todos los usuarios
```
GET http://127.0.0.1:5000/api/admin/usuarios
Authorization: Bearer {access_token_admin}

Respuesta (200):
[
  {
    "id": 1,
    "nombre": "Administrador",
    "email": "admin@domicilios.com",
    "rol": "admin",
    ...
  },
  ...
]
```

---

## 🧪 Pruebas con cURL

### Login
```powershell
$body = @{
    email = "cliente1@example.com"
    password = "cliente123"
} | ConvertTo-Json

Invoke-WebRequest -Uri "http://127.0.0.1:5000/api/auth/login" `
  -Method POST `
  -Headers @{"Content-Type" = "application/json"} `
  -Body $body
```

### Listar comercios
```powershell
Invoke-WebRequest -Uri "http://127.0.0.1:5000/api/comercios" `
  -Method GET
```

### Obtener perfil (requiere token)
```powershell
$token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."

Invoke-WebRequest -Uri "http://127.0.0.1:5000/api/usuarios/perfil" `
  -Method GET `
  -Headers @{"Authorization" = "Bearer $token"}
```

---

## ⚠️ Códigos HTTP Esperados

- **200** - OK
- **201** - Created
- **400** - Bad Request
- **401** - Unauthorized
- **403** - Forbidden
- **404** - Not Found
- **500** - Server Error

---

¡Ahora puedes usar la API! 🚀
