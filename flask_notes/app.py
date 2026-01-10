import os
from flask import Flask
from extensions import db, login_manager
from routes import main
from models import User, Note

def create_app():
    # Создаем экземпляр приложения Flask
    app = Flask(__name__)

    # --- КОНФИГУРАЦИЯ ---
    # Секретный ключ для защиты сессий (куки)
    app.config['SECRET_KEY'] = 'dev-key-12345'
    
    # Настройка базы данных SQLite
    # База будет создана в папке 'instance' или корне проекта
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'notes.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # --- ИНИЦИАЛИЗАЦИЯ РАСШИРЕНИЙ ---
    db.init_app(app)
    login_manager.init_app(app)

    # Куда перенаправлять пользователя, если он не авторизован
    login_manager.login_view = 'main.login'
    login_manager.login_message = "Пожалуйста, войдите в систему."
    login_manager.login_message_category = "info"

    # Регистрация маршрутов (Blueprint)
    app.register_blueprint(main)

    # --- ЗАГРУЗЧИК ПОЛЬЗОВАТЕЛЯ ---
    @login_manager.user_loader
    def load_user(user_id):
        # Flask-Login использует это, чтобы получить объект пользователя из БД по его ID
        return User.query.get(int(user_id))

    # --- СОЗДАНИЕ ТАБЛИЦ ---
    with app.app_context():
        # Эта команда создает файл notes.db и все таблицы, если их еще нет
        db.create_all()

    return app

if __name__ == '__main__':
    app = create_app()
    # Запуск сервера. debug=True позволяет видеть ошибки прямо в браузере
    app.run(debug=True)