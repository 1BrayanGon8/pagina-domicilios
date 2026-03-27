import os
from datetime import timedelta

class Config:
    """Configuración base de la aplicación"""
    SQLALCHEMY_DATABASE_URI = 'sqlite:///domicilios.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = 'kA#7mN!s2Q6eR4fT8uY1pO3iL0zX5vB9'  # 32+ chars para seguridad
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=30)
    JSON_SORT_KEYS = False
    JSONIFY_PRETTYPRINT_REGULAR = True

class DevelopmentConfig(Config):
    """Configuración para desarrollo"""
    DEBUG = True
    TESTING = False

class ProductionConfig(Config):
    """Configuración para producción"""
    DEBUG = False
    TESTING = False

class TestingConfig(Config):
    """Configuración para pruebas"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
