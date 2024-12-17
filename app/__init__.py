from flask import Flask

# Ініціалізація додатку
app = Flask(__name__)
app.config.from_pyfile('../config.py')

# Імпорт views
from . import views

# Імпорт та реєстрація Blueprints
from .posts import post_bp
from .users import bp as user_bp

# Реєстрація Blueprints
app.register_blueprint(post_bp)
app.register_blueprint(user_bp, url_prefix="/users")