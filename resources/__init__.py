from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager
from flask_ckeditor import CKEditor


csrf = CSRFProtect()
ckeditor = CKEditor()
login_manager = LoginManager()
