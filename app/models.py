from app import db
from datetime import datetime

class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=True)
    posted = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)  # Нове поле: активний чи ні
    category = db.Column(db.String(50), nullable=True)  # Нове поле: категорія поста
    author = db.Column(db.String(20), nullable=True)  # Нове поле: автор поста

    def __repr__(self):
        return f"<Post(title='{self.title}', category='{self.category}')>"
