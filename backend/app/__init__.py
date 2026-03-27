from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import config
from app.models import db

def create_app(config_name='development'):
    """Factory para crear la aplicación Flask"""
    app = Flask(__name__)
    
    # Cargar configuración
    app.config.from_object(config[config_name])
    print(f"DEBUG: JWT_SECRET_KEY = {app.config.get('JWT_SECRET_KEY')}")
    
    # Inicializar extensiones
    db.init_app(app)
    jwt = JWTManager(app)
    CORS(app)
    
    # Handlers JWT para entender 422/401 y mensajes
    @jwt.unauthorized_loader
    def unauthorized_response(callback):
        print(f"DEBUG: JWT unauthorized loader: {callback}")
        return jsonify({'mensaje': 'Necesitas autorización (token faltante o inválido).'}), 401

    @jwt.invalid_token_loader
    def invalid_token_response(callback):
        print(f"DEBUG: JWT invalid token loader: {callback}")
        return jsonify({'mensaje': 'Token inválido.'}), 401

    @jwt.expired_token_loader
    def expired_token_response(jwt_header, jwt_payload):
        print('DEBUG: JWT expired token')
        return jsonify({'mensaje': 'Token expirado, inicia sesión de nuevo.'}), 401

    @jwt.revoked_token_loader
    def revoked_token_response(jwt_header, jwt_payload):
        print('DEBUG: JWT revoked token')
        return jsonify({'mensaje': 'Token revocado.'}), 401

    # Crear tablas
    with app.app_context():
        db.create_all()
    
    # Registrar blueprints
    from app.routes import auth_bp, comercios_bp, productos_bp, ordenes_bp, usuarios_bp, admin_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(comercios_bp)
    app.register_blueprint(productos_bp)
    app.register_blueprint(ordenes_bp)
    app.register_blueprint(usuarios_bp)
    app.register_blueprint(admin_bp)
    
    # Ruta de prueba
    @app.route('/api/health', methods=['GET'])
    def health():
        return {'status': 'OK', 'message': 'API de Domicilios está funcionando'}, 200
    
    return app
