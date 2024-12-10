from flask import Blueprint

post_bp = Blueprint("posts", 
                     "posts_bp",
                    __name__, 
                    url_prefix="/post",
                    template_folder="templates/posts"
                    )

from . import views