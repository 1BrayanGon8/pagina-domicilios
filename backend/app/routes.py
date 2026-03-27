from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.models import db, Usuario, Comercio, Producto, Orden, ItemOrden, RoleEnum, EstadoOrdenEnum
from datetime import datetime
from functools import wraps

# Helpers
def get_current_user():
    identity = get_jwt_identity()
    print(f"DEBUG: Identity from token: {identity}, type: {type(identity)}")
    try:
        identity_int = int(identity)
    except (ValueError, TypeError):
        return None, {'mensaje': 'JWT inválido: subject no numérico'}, 401
    usuario = Usuario.query.get(identity_int)
    print(f"DEBUG: Usuario found: {usuario}")
    if not usuario:
        return None, {'mensaje': 'Usuario no encontrado'}, 404
    return usuario, None, None

# Blueprints
auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')
usuarios_bp = Blueprint('usuarios', __name__, url_prefix='/api/usuarios')
comercios_bp = Blueprint('comercios', __name__, url_prefix='/api/comercios')
productos_bp = Blueprint('productos', __name__, url_prefix='/api/productos')
ordenes_bp = Blueprint('ordenes', __name__, url_prefix='/api/ordenes')
admin_bp = Blueprint('admin', __name__, url_prefix='/api/admin')

# Decoradores de autorización
def admin_required(fn):
    @wraps(fn)
    @jwt_required()
    def wrapper(*args, **kwargs):
        identity = get_jwt_identity()
        try:
            identity_int = int(identity)
        except (ValueError, TypeError):
            return {'mensaje': 'JWT inválido: subject no numérico'}, 401
        usuario = Usuario.query.get(identity_int)
        if not usuario or usuario.rol != RoleEnum.ADMIN:
            return {'mensaje': 'Acceso denegado. Se requiere rol de administrador'}, 403
        return fn(*args, **kwargs)
    return wrapper

def comercio_required(fn):
    @wraps(fn)
    @jwt_required()
    def wrapper(*args, **kwargs):
        identity = get_jwt_identity()
        try:
            identity_int = int(identity)
        except (ValueError, TypeError):
            return {'mensaje': 'JWT inválido: subject no numérico'}, 401
        usuario = Usuario.query.get(identity_int)
        if not usuario or usuario.rol not in [RoleEnum.COMERCIO, RoleEnum.ADMIN]:
            return {'mensaje': 'Acceso denegado. Se requiere rol de comercio'}, 403
        return fn(*args, **kwargs)
    return wrapper

def cliente_required(fn):
    @wraps(fn)
    @jwt_required()
    def wrapper(*args, **kwargs):
        identity = get_jwt_identity()
        try:
            identity_int = int(identity)
        except (ValueError, TypeError):
            return {'mensaje': 'JWT inválido: subject no numérico'}, 401
        usuario = Usuario.query.get(identity_int)
        if not usuario or usuario.rol != RoleEnum.CLIENTE:
            return {'mensaje': 'Acceso denegado. Se requiere rol de cliente'}, 403
        return fn(*args, **kwargs)
    return wrapper

# ============= AUTENTICACIÓN =============
@auth_bp.route('/registro', methods=['POST'])
def registro():
    """Registrar nuevo usuario"""
    data = request.get_json()
    
    # Validar datos requeridos
    if not data or not data.get('email') or not data.get('password') or not data.get('nombre'):
        return {'mensaje': 'Email, contraseña y nombre son requeridos'}, 400
    
    # Verificar si el usuario ya existe
    if Usuario.query.filter_by(email=data['email']).first():
        return {'mensaje': 'El email ya está registrado'}, 400
    
    # Crear nuevo usuario
    usuario = Usuario(
        nombre=data['nombre'],
        email=data['email'],
        telefono=data.get('telefono'),
        rol=RoleEnum(data.get('rol', 'cliente')),
        direccion=data.get('direccion'),
        ciudad=data.get('ciudad'),
        codigo_postal=data.get('codigo_postal')
    )
    usuario.set_password(data['password'])
    
    db.session.add(usuario)
    db.session.commit()
    
    # Generar token
    access_token = create_access_token(identity=usuario.id)
    
    return {
        'mensaje': 'Usuario registrado exitosamente',
        'usuario': usuario.to_dict(),
        'access_token': access_token
    }, 201

@auth_bp.route('/login', methods=['POST'])
def login():
    """Iniciar sesión"""
    data = request.get_json()
    
    if not data or not data.get('email') or not data.get('password'):
        return {'mensaje': 'Email y contraseña son requeridos'}, 400
    
    usuario = Usuario.query.filter_by(email=data['email']).first()
    
    if not usuario or not usuario.check_password(data['password']):
        return {'mensaje': 'Email o contraseña incorrectos'}, 401
    
    if not usuario.activo:
        return {'mensaje': 'Usuario desactivado'}, 403
    
    # JWT en Flask-JWT-Extended espera un sub (subject) serializable en JWT, preferible string
    access_token = create_access_token(identity=str(usuario.id))
    
    return {
        'mensaje': 'Sesión iniciada exitosamente',
        'usuario': usuario.to_dict(),
        'access_token': access_token
    }, 200

@auth_bp.route('/login', methods=['GET'])
def login_get():
    """Método GET no permitido para login"""
    return {'mensaje': 'Método no permitido. Use POST para iniciar sesión'}, 405

# ============= USUARIOS =============
@usuarios_bp.route('/perfil', methods=['GET'])
@jwt_required()
def get_perfil():
    """Obtener perfil del usuario autenticado"""
    usuario, error, status = get_current_user()
    if error:
        return error, status
    return usuario.to_dict(), 200

@usuarios_bp.route('/perfil', methods=['PUT'])
@jwt_required()
def update_perfil():
    """Actualizar perfil del usuario"""
    usuario, error, status = get_current_user()
    if error:
        return error, status
    
    data = request.get_json()
    
    # Actualizar campos
    if 'nombre' in data:
        usuario.nombre = data['nombre']
    if 'telefono' in data:
        usuario.telefono = data['telefono']
    if 'direccion' in data:
        usuario.direccion = data['direccion']
    if 'ciudad' in data:
        usuario.ciudad = data['ciudad']
    if 'codigo_postal' in data:
        usuario.codigo_postal = data['codigo_postal']
    
    usuario.fecha_actualizacion = datetime.utcnow()
    db.session.commit()
    
    return {'mensaje': 'Perfil actualizado', 'usuario': usuario.to_dict()}, 200

# ============= COMERCIOS =============
@comercios_bp.route('', methods=['GET'])
def get_comercios():
    """Obtener todos los comercios activos"""
    comercios = Comercio.query.filter_by(activo=True).all()
    return [comercio.to_dict() for comercio in comercios], 200

@comercios_bp.route('/<int:id>', methods=['GET'])
def get_comercio(id):
    """Obtener un comercio específico"""
    comercio = Comercio.query.get(id)
    
    if not comercio:
        return {'mensaje': 'Comercio no encontrado'}, 404
    
    return comercio.to_dict(), 200

@comercios_bp.route('', methods=['POST'])
@admin_required
def crear_comercio():
    """Crear nuevo comercio"""
    identity = get_jwt_identity()
    usuario = Usuario.query.get(identity)
    
    if not usuario:
        return {'mensaje': 'Usuario no encontrado'}, 404
    
    data = request.get_json()
    
    if not data or not data.get('nombre') or not data.get('direccion'):
        return {'mensaje': 'Nombre y dirección son requeridos'}, 400
    
    # Verificar si ya tiene un comercio
    if usuario.comercio:
        return {'mensaje': 'El usuario ya tiene un comercio registrado'}, 400
    
    comercio = Comercio(
        nombre=data['nombre'],
        descripcion=data.get('descripcion'),
        propietario_id=usuario.id,
        telefono=data.get('telefono'),
        email=data.get('email'),
        direccion=data['direccion'],
        ciudad=data.get('ciudad'),
        codigo_postal=data.get('codigo_postal'),
        horario_apertura=data.get('horario_apertura'),
        horario_cierre=data.get('horario_cierre'),
        categoria=data.get('categoria')
    )
    
    db.session.add(comercio)
    
    # Cambiar rol a comercio
    usuario.rol = RoleEnum.COMERCIO
    
    db.session.commit()
    
    return {'mensaje': 'Comercio creado exitosamente', 'comercio': comercio.to_dict()}, 201

@comercios_bp.route('/<int:id>', methods=['PUT'])
@admin_required
def update_comercio(id):
    """Actualizar comercio"""
    identity = get_jwt_identity()
    usuario = Usuario.query.get(identity)
    
    comercio = Comercio.query.get(id)
    
    if not comercio:
        return {'mensaje': 'Comercio no encontrado'}, 404
    
    # Verificar que el usuario sea propietario
    if usuario.id != comercio.propietario_id and usuario.rol != RoleEnum.ADMIN:
        return {'mensaje': 'No tienes permiso para editar este comercio'}, 403
    
    data = request.get_json()
    
    if 'nombre' in data:
        comercio.nombre = data['nombre']
    if 'descripcion' in data:
        comercio.descripcion = data['descripcion']
    if 'telefono' in data:
        comercio.telefono = data['telefono']
    if 'email' in data:
        comercio.email = data['email']
    if 'direccion' in data:
        comercio.direccion = data['direccion']
    if 'ciudad' in data:
        comercio.ciudad = data['ciudad']
    if 'codigo_postal' in data:
        comercio.codigo_postal = data['codigo_postal']
    if 'horario_apertura' in data:
        comercio.horario_apertura = data['horario_apertura']
    if 'horario_cierre' in data:
        comercio.horario_cierre = data['horario_cierre']
    if 'categoria' in data:
        comercio.categoria = data['categoria']
    if 'activo' in data:
        comercio.activo = data['activo']
    
    db.session.commit()
    
    return {'mensaje': 'Comercio actualizado', 'comercio': comercio.to_dict()}, 200

# ============= PRODUCTOS =============
@productos_bp.route('', methods=['GET'])
def get_productos():
    """Obtener todos los productos (opcional filtro por comercio)"""
    comercio_id = request.args.get('comercio_id')
    
    if comercio_id:
        productos = Producto.query.filter_by(comercio_id=comercio_id, disponible=True).all()
    else:
        productos = Producto.query.filter_by(disponible=True).all()
    
    return [producto.to_dict() for producto in productos], 200

@productos_bp.route('/<int:id>', methods=['GET'])
def get_producto(id):
    """Obtener un producto específico"""
    producto = Producto.query.get(id)
    
    if not producto:
        return {'mensaje': 'Producto no encontrado'}, 404
    
    return producto.to_dict(), 200

@productos_bp.route('', methods=['POST'])
@comercio_required
def crear_producto():
    """Crear nuevo producto"""
    identity = get_jwt_identity()
    usuario = Usuario.query.get(identity)
    
    # Obtener el comercio del usuario
    if usuario.rol == RoleEnum.COMERCIO:
        comercio = usuario.comercio
        if not comercio:
            return {'mensaje': 'El usuario no tiene un comercio registrado'}, 400
        comercio_id = comercio.id
    else:
        return {'mensaje': 'Solo comercios pueden crear productos'}, 403
    
    data = request.get_json()
    
    if not data or not data.get('nombre') or data.get('precio') is None:
        return {'mensaje': 'Nombre y precio son requeridos'}, 400
    
    producto = Producto(
        nombre=data['nombre'],
        descripcion=data.get('descripcion'),
        precio=float(data['precio']),
        comercio_id=comercio_id,
        categoria=data.get('categoria'),
        imagen_url=data.get('imagen_url'),
        stock=int(data.get('stock', 0))
    )
    
    db.session.add(producto)
    db.session.commit()
    
    return {'mensaje': 'Producto creado exitosamente', 'producto': producto.to_dict()}, 201

@productos_bp.route('/<int:id>', methods=['PUT'])
@comercio_required
def update_producto(id):
    """Actualizar producto"""
    identity = get_jwt_identity()
    usuario = Usuario.query.get(identity)
    
    producto = Producto.query.get(id)
    
    if not producto:
        return {'mensaje': 'Producto no encontrado'}, 404
    
    # Verificar que el usuario sea dueño del comercio
    if usuario.rol == RoleEnum.COMERCIO and usuario.comercio.id != producto.comercio_id:
        return {'mensaje': 'No tienes permiso para editar este producto'}, 403
    
    data = request.get_json()
    
    if 'nombre' in data:
        producto.nombre = data['nombre']
    if 'descripcion' in data:
        producto.descripcion = data['descripcion']
    if 'precio' in data:
        producto.precio = float(data['precio'])
    if 'categoria' in data:
        producto.categoria = data['categoria']
    if 'imagen_url' in data:
        producto.imagen_url = data['imagen_url']
    if 'disponible' in data:
        producto.disponible = data['disponible']
    if 'stock' in data:
        producto.stock = int(data['stock'])
    
    db.session.commit()
    
    return {'mensaje': 'Producto actualizado', 'producto': producto.to_dict()}, 200

# ============= ÓRDENES =============
@ordenes_bp.route('', methods=['POST'])
@cliente_required
def crear_orden():
    """Crear nueva orden"""
    usuario, error, status = get_current_user()
    if error:
        return error, status
    
    data = request.get_json()
    print(f"DEBUG: Request data: {data}")
    
    if not data or not data.get('comercio_id') or not data.get('items') or not data.get('direccion_entrega'):
        return {'mensaje': 'Se requiere comercio_id, items y dirección de entrega'}, 400
    
    comercio = Comercio.query.get(data['comercio_id'])
    if not comercio:
        return {'mensaje': 'Comercio no encontrado'}, 404
    
    # Crear orden
    numero_orden = f"ORD-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}-{usuario.id}"
    orden = Orden(
        numero_orden=numero_orden,
        cliente_id=usuario.id,
        comercio_id=data['comercio_id'],
        direccion_entrega=data['direccion_entrega'],
        notas=data.get('notas')
    )
    
    monto_total = 0.0
    
    # Agregar items
    for item_data in data['items']:
        producto = Producto.query.get(item_data['producto_id'])
        
        if not producto:
            return {'mensaje': f"Producto {item_data['producto_id']} no encontrado"}, 404
        
        if not producto.disponible:
            return {'mensaje': f"Producto {producto.nombre} no está disponible"}, 400
        
        cantidad = int(item_data['cantidad'])
        precio_unitario = producto.precio
        subtotal = cantidad * precio_unitario
        
        item = ItemOrden(
            producto_id=producto.id,
            cantidad=cantidad,
            precio_unitario=precio_unitario,
            subtotal=subtotal
        )
        
        orden.items.append(item)
        monto_total += subtotal
    
    orden.monto_total = monto_total
    
    db.session.add(orden)
    db.session.commit()
    
    return {'mensaje': 'Orden creada exitosamente', 'orden': orden.to_dict()}, 201

@ordenes_bp.route('/<int:id>', methods=['GET'])
@jwt_required()
def get_orden(id):
    """Obtener una orden específica"""
    usuario, error, status = get_current_user()
    if error:
        return error, status
    
    orden = Orden.query.get(id)
    
    if not orden:
        return {'mensaje': 'Orden no encontrada'}, 404
    
    # Verificar permisos
    if usuario.id != orden.cliente_id and usuario.rol != RoleEnum.ADMIN and (usuario.rol != RoleEnum.COMERCIO or usuario.comercio.id != orden.comercio_id):
        return {'mensaje': 'No tienes permiso para ver esta orden'}, 403
    
    return orden.to_dict(), 200

@ordenes_bp.route('', methods=['GET'])
@jwt_required()
def get_mis_ordenes():
    """Obtener las órdenes del usuario"""
    usuario, error, status = get_current_user()
    if error:
        return error, status
    
    if usuario.rol == RoleEnum.CLIENTE:
        ordenes = Orden.query.filter_by(cliente_id=usuario.id).all()
    elif usuario.rol == RoleEnum.COMERCIO:
        ordenes = Orden.query.filter_by(comercio_id=usuario.comercio.id).all()
    else:
        ordenes = Orden.query.all()
    
    return [orden.to_dict() for orden in ordenes], 200

@ordenes_bp.route('/<int:id>/estado', methods=['PUT'])
@jwt_required()
def update_estado_orden(id):
    """Actualizar estado de la orden"""
    usuario, error, status = get_current_user()
    if error:
        return error, status
    
    orden = Orden.query.get(id)
    
    if not orden:
        return {'mensaje': 'Orden no encontrada'}, 404
    
    # Solo comercio o admin puede cambiar estado
    if usuario.rol == RoleEnum.COMERCIO and usuario.comercio.id != orden.comercio_id:
        return {'mensaje': 'No tienes permiso para actualizar esta orden'}, 403
    
    data = request.get_json()
    
    if not data or not data.get('estado'):
        return {'mensaje': 'Estado es requerido'}, 400
    
    try:
        orden.estado = EstadoOrdenEnum(data['estado'])
        
        if data['estado'] == 'entregada':
            orden.fecha_entrega = datetime.utcnow()
        
        db.session.commit()
    except ValueError:
        return {'mensaje': 'Estado inválido'}, 400
    
    return {'mensaje': 'Estado actualizado', 'orden': orden.to_dict()}, 200

# ============= ADMIN =============
@admin_bp.route('/usuarios', methods=['GET'])
@admin_required
def admin_get_usuarios():
    """Obtener todos los usuarios (solo admin)"""
    usuarios = Usuario.query.all()
    return [usuario.to_dict() for usuario in usuarios], 200

@admin_bp.route('/estadisticas', methods=['GET'])
@admin_required
def admin_estadisticas():
    """Obtener estadísticas generales"""
    total_usuarios = Usuario.query.count()
    total_comercios = Comercio.query.count()
    total_productos = Producto.query.count()
    total_ordenes = Orden.query.count()
    monto_total = db.session.query(db.func.sum(Orden.monto_total)).scalar() or 0
    
    return {
        'total_usuarios': total_usuarios,
        'total_comercios': total_comercios,
        'total_productos': total_productos,
        'total_ordenes': total_ordenes,
        'monto_total': monto_total
    }, 200
