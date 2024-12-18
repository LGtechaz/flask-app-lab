from . import post_bp
from flask import render_template, abort, flash, redirect, url_for, session, request
from .forms import PostForm
from app.models import Post
from app import db

# Список постів (тестові дані, більше не використовуються, якщо є БД)
posts = [
    {"id": 1, 'title': 'My First Post', 'content': 'This is the content of my first post.', 'author': 'John Doe'},
    {"id": 2, 'title': 'Another Day', 'content': 'Today I learned about Flask macros.', 'author': 'Jane Smith'},
    {"id": 3, 'title': 'Flask and Jinja2', 'content': 'Jinja2 is powerful for templating.', 'author': 'Mike Lee'}
]

# Маршрут для відображення всіх постів
@post_bp.route('/')
def get_posts():
    posts = Post.query.all()
    return render_template("posts.html", posts=posts)

# Маршрут для відображення деталей конкретного поста
@post_bp.route('/post/<int:post_id>', methods=['GET'])
def detail_post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('detail_post.html', post=post)

# Маршрут для додавання нового поста
@post_bp.route('/add_post', methods=['GET', 'POST'])
def add_post():
    form = PostForm()
    if form.validate_on_submit():
        new_post = Post(
            title=form.title.data,
            content=form.content.data,
            category=form.category.data,
            is_active=form.is_active.data,
            posted=form.posted.data,
            author=session.get('username', 'Unknown')
        )
        db.session.add(new_post)
        db.session.commit()
        flash('Post added successfully!', 'success')
        return redirect(url_for('posts.get_posts'))
    return render_template('add_post.html', form=form)

# Маршрут для видалення поста
@post_bp.route('/delete_post/<int:post_id>', methods=['POST'])
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    flash('Post deleted successfully!', 'success')
    return redirect(url_for('posts.get_posts'))

# Маршрут для редагування поста
@post_bp.route('/edit/<int:post_id>', methods=['GET', 'POST'])
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)  # Отримуємо пост з БД або повертаємо 404
    form = PostForm(obj=post)  # Заповнюємо форму даними з об'єкта поста

    # Примусова ініціалізація дати публікації
    form.posted.data = post.posted

    if form.validate_on_submit():
        # Оновлюємо значення поста з даних форми
        post.title = form.title.data
        post.content = form.content.data
        post.category = form.category.data
        post.is_active = form.is_active.data
        post.posted = form.posted.data

        db.session.commit()  # Зберігаємо зміни у БД
        flash('Post updated successfully!', 'success')
        return redirect(url_for('posts.get_posts'))  # Перенаправлення до списку постів

    return render_template('add_post.html', form=form)
