# 🔍 DIAGNÓSTICO - DOMICILIOS APP

## Paso 1: Abre la Consola del Navegador

**Presiona F12** en tu navegador donde está abierta la aplicación.

Deberías ver una consola con mensajes como:
```
Script JavaScript cargado correctamente
API_URL: http://127.0.0.1:5000/api
Token: No
DOM cargado - ejecutando inicialización
Actualizando UI...
Cargando comercios...
```

---

## Paso 2: ¿Hay Errores en la Consola?

### Si ves errores rojos:
1. Copia el error completo
2. Publica el error
3. Lo investigamos juntos

### Errores comunes:

**Error: "Cannot read property of undefined"**
→ Significa que falta un elemento HTML

**Error: "Failed to fetch"**
→ El backend no está respondiendo

**Error: "CORS error"**
→ Problema de comunicación backend-frontend

---

## Paso 3: Verifica el Backend

Abre PowerShell y ejecuta:

```powershell
cd "c:\Users\NICOA\Nicolas\Vs Code\DOMICILIOS APP\backend"

# Verifica si el backend está corriendo
curl -UseBasicParsing http://127.0.0.1:5000/api/health
```

Deberías ver:
```json
{ "status": "OK", "message": "API de Domicilios está funcionando" }
```

---

## Paso 4: Prueba Manual en Consola

En la **consola del navegador (F12)**, ejecuta:

```javascript
// Prueba 1: Verificar API
console.log('API_URL:', API_URL);

// Prueba 2: Cargar comercios
fetch('http://127.0.0.1:5000/api/comercios')
  .then(r => r.json())
  .then(data => console.log('Comercios:', data))
  .catch(e => console.error('Error:', e));

// Prueba 3: Verificar función
console.log('mostrarPagina:', typeof mostrarPagina);
console.log('cargarComercios:', typeof cargarComercios);
```

---

## Paso 5: Soluciones Rápidas

### Solución 1: Limpiar Caché
```
Presiona: Ctrl + Shift + R
```

### Solución 2: Recargar Backend
En PowerShell donde corre el backend:
```
Presiona: Ctrl + C
Luego: python main.py
```

### Solución 3: Limpiar LocalStorage
En la consola del navegador:
```javascript
localStorage.clear();
location.reload();
```

### Solución 4: Verificar Base de Datos
```powershell
cd backend
python init_db.py
```

---

## Paso 6: Reporta el Problema

Cuando tengas el error, comparte:

```
1. El error exacto de la consola (F12)
2. La respuesta de: curl http://127.0.0.1:5000/api/health
3. Lo que ves en pantalla
4. Qué botón presionaste cuando falló
```

---

## Checklist Rápido

- [ ] Backend corre (http://127.0.0.1:5000 responde)
- [ ] Frontend carga (http://localhost:8000 se abre)
- [ ] Consola sin errores críticos (F12)
- [ ] script.js se cargó ("Script JavaScript cargado...") 
- [ ] Se ejecutó inicialización ("Actualizando UI...")
- [ ] Se intentó cargar comercios ("Cargando comercios...")

---

## 📝 Formulario de Reporte

Si nada funciona, usa este formato:

```
BACKEND:
- ¿Corre python main.py? Sí / No
- ¿Responde /api/health? Sí / No
- ¿Hay errores en la consola de Python? Sí / No (cuál?)

FRONTEND:  
- ¿Se abre http://localhost:8000? Sí / No
- ¿Ves la página de bienvenida? Sí / No
- ¿Hay errores en F12 Console? Sí / No (cuál?)
- ¿Los botones hacen algo? Sí / No

ERROR:
- Mensaje exacto:
- Dónde escribo ese mensaje (busca "error" en consola F12):
```

---

**¡Envíame tu diagnóstico y lo arreglamos! 🔧**
