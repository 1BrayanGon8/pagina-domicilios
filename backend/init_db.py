"""
Script para inicializar la base de datos con datos de prueba
Ejecutar: python init_db.py
"""

import os
import sys

# Añadir el directorio al path
sys.path.insert(0, os.path.dirname(__file__))

from app import create_app
from app.models import db, Usuario, Comercio, Producto, RoleEnum

def init_database():
    """Inicializar la base de datos con datos de prueba"""
    
    app = create_app('development')
    
    with app.app_context():
        # Eliminar tablas existentes (comentar si no se desea)
        # db.drop_all()
        
        # Crear tablas
        db.create_all()
        
        # Verificar si ya existen usuarios
        if Usuario.query.first():
            print("⚠️ La base de datos ya contiene datos. Saltando inicialización.")
            return
        
        print("🚀 Inicializando base de datos...")
        
        # Crear usuario admin
        admin = Usuario(
            nombre='Administrador',
            email='admin@domicilios.com',
            telefono='1234567890',
            rol=RoleEnum.ADMIN,
            ciudad='Bogotá'
        )
        admin.set_password('admin123')
        db.session.add(admin)
        print("✓ Usuario admin creado")
        
        # Crear usuarios clientes de prueba
        cliente1 = Usuario(
            nombre='Juan Pérez',
            email='cliente1@example.com',
            telefono='3001234567',
            rol=RoleEnum.CLIENTE,
            direccion='Calle 10 #5-50',
            ciudad='Bogotá',
            codigo_postal='110111'
        )
        cliente1.set_password('cliente123')
        db.session.add(cliente1)
        print("✓ Cliente 1 creado")
        
        cliente2 = Usuario(
            nombre='María García',
            email='cliente2@example.com',
            telefono='3009876543',
            rol=RoleEnum.CLIENTE,
            direccion='Carrera 7 #50-80',
            ciudad='Medellín',
            codigo_postal='050001'
        )
        cliente2.set_password('cliente123')
        db.session.add(cliente2)
        print("✓ Cliente 2 creado")
        
        # Crear usuarios comerciantes
        comerciante1 = Usuario(
            nombre='Pizza Italia',
            email='pizzeria@example.com',
            telefono='3105555555',
            rol=RoleEnum.COMERCIO,
            ciudad='Bogotá'
        )
        comerciante1.set_password('comercio123')
        db.session.add(comerciante1)
        print("✓ Comerciante 1 creado")
        
        comerciante2 = Usuario(
            nombre='Farmacia ExpresS',
            email='farmacia@example.com',
            telefono='3156666666',
            rol=RoleEnum.COMERCIO,
            ciudad='Bogotá'
        )
        comerciante2.set_password('comercio123')
        db.session.add(comerciante2)
        print("✓ Comerciante 2 creado")
        
        db.session.commit()
        
        # Crear comercios
        comercio1 = Comercio(
            nombre='Pizza Italia',
            descripcion='Deliciosas pizzas artesanales con ingredientes frescos',
            propietario_id=comerciante1.id,
            telefono='3105555555',
            email='pizzeria@example.com',
            direccion='Calle 80 #19-50, Bogotá',
            ciudad='Bogotá',
            codigo_postal='110221',
            horario_apertura='11:00',
            horario_cierre='23:00',
            categoria='Comida',
            calificacion=4.8
        )
        db.session.add(comercio1)
        print("✓ Comercio 1 creado")
        
        comercio2 = Comercio(
            nombre='Farmacia Express',
            descripcion='Medicinas, vitaminas y artículos de salud',
            propietario_id=comerciante2.id,
            telefono='3156666666',
            email='farmacia@example.com',
            direccion='Carrera 11 #90-40, Bogotá',
            ciudad='Bogotá',
            codigo_postal='110311',
            horario_apertura='08:00',
            horario_cierre='20:00',
            categoria='Farmacia',
            calificacion=4.5
        )
        db.session.add(comercio2)
        print("✓ Comercio 2 creado")
        
        db.session.commit()
        
        # Crear productos para Pizza Italia
        productos_pizza = [
            Producto(
                nombre='Pizza Margherita',
                descripcion='Tomate, mozzarella y albahaca',
                precio=18.99,
                comercio_id=comercio1.id,
                categoria='Pizza',
                stock=50
            ),
            Producto(
                nombre='Pizza Pepperoni',
                descripcion='Salsa de tomate, mozzarella y pepperoni',
                precio=19.99,
                comercio_id=comercio1.id,
                categoria='Pizza',
                stock=50
            ),
            Producto(
                nombre='Pizza Cuatro Quesos',
                descripcion='Mozzarella, parmesano, queso azul y queso de cabra',
                precio=21.99,
                comercio_id=comercio1.id,
                categoria='Pizza',
                stock=30
            ),
            Producto(
                nombre='Ensalada César',
                descripcion='Lechuga, crutones, parmesano y aderezo César',
                precio=9.99,
                comercio_id=comercio1.id,
                categoria='Ensalada',
                stock=40
            ),
            Producto(
                nombre='Pasta Carbonara',
                descripcion='Pasta, huevo, tocino y parmesano',
                precio=15.99,
                comercio_id=comercio1.id,
                categoria='Pasta',
                stock=35
            ),
        ]
        
        for producto in productos_pizza:
            db.session.add(producto)
        print("✓ 5 productos de Pizza Italia creados")
        
        # Crear productos para Farmacia Express
        productos_farmacia = [
            Producto(
                nombre='Vitamina C 500mg',
                descripcion='Suplemento vitamínico',
                precio=12.99,
                comercio_id=comercio2.id,
                categoria='Vitaminas',
                stock=100
            ),
            Producto(
                nombre='Paracetamol 500mg',
                descripcion='Analgésico y antifebril',
                precio=5.99,
                comercio_id=comercio2.id,
                categoria='Analgésicos',
                stock=150
            ),
            Producto(
                nombre='Ibuprofeno 200mg',
                descripcion='Antiinflamatorio',
                precio=7.99,
                comercio_id=comercio2.id,
                categoria='Antiinflamatorios',
                stock=120
            ),
            Producto(
                nombre='Multivitamínico Diario',
                descripcion='Complejo vitamínico completo',
                precio=18.99,
                comercio_id=comercio2.id,
                categoria='Vitaminas',
                stock=80
            ),
            Producto(
                nombre='Gel Antibacterial',
                descripcion='Gel desinfectante para manos',
                precio=4.99,
                comercio_id=comercio2.id,
                categoria='Higiene',
                stock=200
            ),
        ]
        
        for producto in productos_farmacia:
            db.session.add(producto)
        print("✓ 5 productos de Farmacia Express creados")
        
        db.session.commit()
        
        print("\n✅ Base de datos inicializada correctamente!\n")
        print("📝 Usuarios de prueba creados:")
        print("   Admin:")
        print("   - Email: admin@domicilios.com")
        print("   - Contraseña: admin123\n")
        print("   Cliente:")
        print("   - Email: cliente1@example.com")
        print("   - Contraseña: cliente123\n")
        print("   Comerciante:")
        print("   - Email: pizzeria@example.com")
        print("   - Contraseña: comercio123\n")

if __name__ == '__main__':
    init_database()
