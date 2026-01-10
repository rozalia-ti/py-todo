import os
from flask import Flask
from extensions import db, migrate, login

def create_app():
    app = Flask(__name__)
    
    # Конфигурация
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'dev-key-very-secret'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///notes.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Инициализация расширений
    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    login.login_view = 'main.login'
    login.login_message = "Пожалуйста, войдите, чтобы увидеть эту страницу."
    login.login_message_category = "info"

    # Регистрация Blueprint
    from routes import main
    app.register_blueprint(main)

    return app

app = create_app()

@login.user_loader
def load_user(user_id):
    from models import User
    return db.session.get(User, int(user_id))

if __name__ == '__main__':
    app.run(debug=True)