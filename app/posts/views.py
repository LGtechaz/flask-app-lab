from . import post_bp
from flask import render_template, abort, flash, redirect, url_for, session
from .forms import PostForm
import json
from app.models import Post
from app import db

posts = [
    {"id": 1, 'title': 'My First Post', 'content': 'This is the content of my first post.', 'author': 'John Doe'},
    {"id": 2, 'title': 'Another Day', 'content': 'Today I learned about Flask macros.', 'author': 'Jane Smith'},
    {"id": 3, 'title': 'Flask and Jinja2', 'content': 'Jinja2 is powerful for templating.', 'author': 'Mike Lee'}
] 

@post_bp.route('/')
def get_posts():
   
    posts = Post.query.all()
    return render_template("posts.html", posts=posts)

@post_bp.route('/post/<int:post_id>', methods=['GET'])
def detail_post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('detail_post.html', post=post)

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
        db.session.add(new_post)  #
        db.session.commit()  
        flash('Post added successfully!', 'success')
        return redirect(url_for('posts.get_posts'))  
    return render_template('add_post.html', form=form)
