import os

class Config(object):
    ENVIRONMENT = 'Production'
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    SECRET_KEY = os.getenv('SECRET_KEY')
    FLASK_APP = os.environ.get("FLASK_APP")

    PROPAGATE_EXCEPTIONS = True
    DEBUG = False

    SQLALCHEMY_ECHO = False
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = bool(os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS'))
    SQLALCHEMY_ENGINE_OPTIONS = {'pool_recycle': 280, 'pool_timeout': 100,  'pool_pre_ping': True}
    
    CKEDITOR_SERVE_LOCAL = True
    CKEDITOR_PKG_TYPE = 'full'
    CKEDITOR_LANGUAGE = 'en'
    CKEDITOR_ENABLE_CSRF = True
    CKEDITOR_FILE_UPLOADER = '/static/uploads/'

    CKEDITOR_ENABLE_CODESNIPPET = True
    CKEDITOR_CODE_THEME = 'monokai_sublime'


class Development(Config):
    ENVIRONMENT = 'Development'
    DEBUG = True
    TESTING = False
    MAIL_DEBUG = True
   
class Testing (Config):
    ENVIRONMENT = 'Staging'
    DEBUG = False
    TESTING = True
    MAIL_DEBUG = False
    SQLALCHEMY_ENGINE_OPTIONS = {}

    
class Production(Config):
    ENVIRONMENT = 'Production'
    DEBUG = False
    TESTING = False
    MAIL_DEBUG = False
