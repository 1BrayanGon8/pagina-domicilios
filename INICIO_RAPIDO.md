📚 GUÍA RÁPIDA DE INICIO - DOMICILIOS APP
=========================================

## 🎯 PASO 1: Preparar el Backend (5 minutos)

1. Abre PowerShell o CMD en la carpeta `backend`:
   ```
   cd "c:\Users\NICOA\Nicolas\Vs Code\DOMICILIOS APP\backend"
   ```

2. Crea un entorno virtual (recomendado):
   ```
   python -m venv venv
   venv\Scripts\activate
   ```

3. Instala las dependencias:
   ```
   pip install -r requirements.txt
   ```

4. Inicializa la base de datos con datos de prueba:
   ```
   python init_db.py
   ```
   ✅ Verás un mensaje diciendo que la BD fue inicializada

---

## 🚀 PASO 2: Ejecutar el Backend (2 minutos)

1. Desde la carpeta `backend` (con el entorno virtual activo), ejecuta:
   ```
   python main.py
   ```

2. Deberías ver algo como:
   ```
   * Running on http://127.0.0.1:5000
   ```

3. ✅ El backend está listo. DEJA ESTA CONSOLA ABIERTA

---

## 🎨 PASO 3: Ejecutar el Frontend (2 minutos)

1. Abre otra consola/PowerShell en la carpeta `frontend`:
   ```
   cd "..\frontend"
   ```

2. Inicia un servidor HTTP:
   ```
   python -m http.server 8000
   ```

3. O si prefieres usar Node.js:
   ```
   npx http-server
   ```

4. ✅ El frontend está listo

---

## 🌐 PASO 4: Acceder a la Aplicación

1. Abre tu navegador web (Chrome, Firefox, Edge, etc.)
2. Ve a: **http://localhost:8000**
3. ✅ ¡La aplicación está lista para usar!

---

## 🧪 PASO 5: Probar la Aplicación

### Opción A: Iniciar Sesión (Datos de prueba)

Haz click en "Iniciar Sesión" y usa:

**Como Admin:**
- Email: admin@domicilios.com
- Contraseña: admin123

**Como Cliente:**
- Email: cliente1@example.com
- Contraseña: cliente123

**Como Comercio:**
- Email: pizzeria@example.com
- Contraseña: comercio123

### Opción B: Crear nueva cuenta
Haz click en "Registrarse" y crea una cuenta nueva con rol Cliente o Comercio

---

## 📋 Flujos de Prueba Recomendados

### 1️⃣ Comprar productos (Cliente)
1. Inicia sesión como cliente
2. Ve a "Comercios"
3. Selecciona "Pizza Italia"
4. Agrega productos al carrito
5. Ve al carrito (botón flotante)
6. Confirma tu orden
7. Ve a "Mis Órdenes" para ver tu pedido

### 2️⃣ Vender productos (Comercio)
1. Inicia sesión como comerciante
2. Ve a "Mi Cuenta"
3. Edita/crea tu comercio
4. Agrega productos
5. Ve a "Mis Órdenes" para ver pedidos

### 3️⃣ Administración (Admin)
1. Inicia sesión como admin
2. Ve a "Admin"
3. Visualiza estadísticas
4. Ve lista de usuarios

---

## 🆘 Solución de Problemas

### ❌ "ModuleNotFoundError: No module named 'flask'"
**Solución:** 
```
pip install -r requirements.txt
```

### ❌ "Port 5000 is already in use"
**Solución:** Cambia el puerto en `main.py` línea final:
```python
app.run(debug=True, host='127.0.0.1', port=5001)  # Usa 5001 en lugar de 5000
```

### ❌ CORS error en el navegador
**Solución:** Verifica que el backend esté ejecutándose en http://127.0.0.1:5000

### ❌ "Database is locked" 
**Solución:** Cierra el backend, borra `domicilios.db` y vuelve a iniciar

### ❌ Cambios en el frontend no se ven
**Solución:** Presiona Ctrl+Shift+R para vaciar caché del navegador

---

## 📁 Estructura de archivos importantes

```
backend/
├── main.py              ← Ejecutar para iniciar servidor
├── init_db.py           ← Ejecutar para cargar datos de prueba
├── requirements.txt     ← Dependencias a instalar
├── config.py            ← Configuración
└── app/
    ├── models.py        ← Base de datos
    └── routes.py        ← API endpoints

frontend/
├── index.html           ← Página web
├── styles.css           ← Estilos
└── script.js            ← Lógica JavaScript
```

---

## 🎓 Próximos Pasos

- [ ] Explorar la interfaz de usuario
- [ ] Hacer pruebas como cliente
- [ ] Hacer pruebas como comerciante  
- [ ] Ver el panel de administración
- [ ] Revisar el código de los endpoints
- [ ] Agregar nuevos productos
- [ ] Personalizar estilos
- [ ] Agregar más comercios

---

## 📞 Contacto y Soporte

Si tienes dudas o problemas, revisa:
1. El README.md (documentación completa)
2. Los comentarios en el código
3. La consola del navegador (F12) para ver errores

---

**¡Listo para disfrutar de DOMICILIOS APP! 🚀🚚**
