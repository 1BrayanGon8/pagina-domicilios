from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import enum

db = SQLAlchemy()

class RoleEnum(enum.Enum):
    CLIENTE = 'cliente'
    COMERCIO = 'comercio'
    ADMIN = 'admin'
    REPARTIDOR = 'repartidor'

class EstadoOrdenEnum(enum.Enum):
    PENDIENTE = 'pendiente'
    CONFIRMADA = 'confirmada'
    EN_PREPARACION = 'en_preparacion'
    EN_RUTA = 'en_ruta'
    ENTREGADA = 'entregada'
    CANCELADA = 'cancelada'

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    telefono = db.Column(db.String(20))
    password_hash = db.Column(db.String(255), nullable=False)
    rol = db.Column(db.Enum(RoleEnum), default=RoleEnum.CLIENTE, nullable=False)
    direccion = db.Column(db.String(255))
    ciudad = db.Column(db.String(100))
    codigo_postal = db.Column(db.String(20))
    activo = db.Column(db.Boolean, default=True)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_actualizacion = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relaciones
    ordenes = db.relationship('Orden', backref='cliente', lazy=True, foreign_keys='Orden.cliente_id')
    comercio = db.relationship('Comercio', backref='propietario_rel', lazy=True, uselist=False, foreign_keys='Comercio.propietario_id')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self, include_password=False):
        data = {
            'id': self.id,
            'nombre': self.nombre,
            'email': self.email,
            'telefono': self.telefono,
            'rol': self.rol.value,
            'direccion': self.direccion,
            'ciudad': self.ciudad,
            'codigo_postal': self.codigo_postal,
            'activo': self.activo,
            'fecha_creacion': self.fecha_creacion.isoformat()
        }
        if include_password:
            data['password_hash'] = self.password_hash
        return data

class Comercio(db.Model):
    __tablename__ = 'comercios'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(120), nullable=False, unique=True)
    descripcion = db.Column(db.Text)
    propietario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    telefono = db.Column(db.String(20))
    email = db.Column(db.String(120))
    direccion = db.Column(db.String(255), nullable=False)
    ciudad = db.Column(db.String(100))
    codigo_postal = db.Column(db.String(20))
    horario_apertura = db.Column(db.String(50))
    horario_cierre = db.Column(db.String(50))
    activo = db.Column(db.Boolean, default=True)
    logo_url = db.Column(db.String(255))
    categoria = db.Column(db.String(100))
    calificacion = db.Column(db.Float, default=0.0)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relaciones
    productos = db.relationship('Producto', backref='comercio', lazy=True, cascade='all, delete-orphan')
    ordenes = db.relationship('Orden', backref='comercio', lazy=True, foreign_keys='Orden.comercio_id')
    
    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'descripcion': self.descripcion,
            'telefono': self.telefono,
            'email': self.email,
            'direccion': self.direccion,
            'ciudad': self.ciudad,
            'codigo_postal': self.codigo_postal,
            'horario_apertura': self.horario_apertura,
            'horario_cierre': self.horario_cierre,
            'activo': self.activo,
            'logo_url': self.logo_url,
            'categoria': self.categoria,
            'calificacion': self.calificacion,
            'fecha_creacion': self.fecha_creacion.isoformat()
        }

class Producto(db.Model):
    __tablename__ = 'productos'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(120), nullable=False)
    descripcion = db.Column(db.Text)
    precio = db.Column(db.Float, nullable=False)
    comercio_id = db.Column(db.Integer, db.ForeignKey('comercios.id'), nullable=False)
    categoria = db.Column(db.String(100))
    imagen_url = db.Column(db.String(255))
    disponible = db.Column(db.Boolean, default=True)
    stock = db.Column(db.Integer, default=0)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relaciones
    items_orden = db.relationship('ItemOrden', backref='producto', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'descripcion': self.descripcion,
            'precio': self.precio,
            'comercio_id': self.comercio_id,
            'categoria': self.categoria,
            'imagen_url': self.imagen_url,
            'disponible': self.disponible,
            'stock': self.stock,
            'fecha_creacion': self.fecha_creacion.isoformat()
        }

class Orden(db.Model):
    __tablename__ = 'ordenes'
    
    id = db.Column(db.Integer, primary_key=True)
    numero_orden = db.Column(db.String(20), unique=True, nullable=False)
    cliente_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    comercio_id = db.Column(db.Integer, db.ForeignKey('comercios.id'), nullable=False)
    estado = db.Column(db.Enum(EstadoOrdenEnum), default=EstadoOrdenEnum.PENDIENTE, nullable=False)
    monto_total = db.Column(db.Float, nullable=False, default=0.0)
    direccion_entrega = db.Column(db.String(255), nullable=False)
    notas = db.Column(db.Text)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_entrega = db.Column(db.DateTime)
    
    # Relaciones
    items = db.relationship('ItemOrden', backref='orden', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'numero_orden': self.numero_orden,
            'cliente_id': self.cliente_id,
            'comercio_id': self.comercio_id,
            'estado': self.estado.value,
            'monto_total': self.monto_total,
            'direccion_entrega': self.direccion_entrega,
            'notas': self.notas,
            'fecha_creacion': self.fecha_creacion.isoformat(),
            'items': [item.to_dict() for item in self.items]
        }

class ItemOrden(db.Model):
    __tablename__ = 'items_orden'
    
    id = db.Column(db.Integer, primary_key=True)
    orden_id = db.Column(db.Integer, db.ForeignKey('ordenes.id'), nullable=False)
    producto_id = db.Column(db.Integer, db.ForeignKey('productos.id'), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    precio_unitario = db.Column(db.Float, nullable=False)
    subtotal = db.Column(db.Float, nullable=False)
    
    def to_dict(self):
        return {
            'id': self.id,
            'orden_id': self.orden_id,
            'producto_id': self.producto_id,
            'producto_nombre': self.producto.nombre if self.producto else None,
            'cantidad': self.cantidad,
            'precio_unitario': self.precio_unitario,
            'subtotal': self.subtotal
        }
