from app import app
from extensions import db
from models import User, Note # Импортируем, чтобы SQLAlchemy их увидел

with app.app_context():
    db.create_all()
    print("База данных создана успешно!")