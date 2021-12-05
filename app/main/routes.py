from flask import render_template, request, url_for
from werkzeug.utils import redirect

from app.main import bp
from app.models import Bookmark, Post


@bp.route('/')
def feed():
    posts = Post.query
    bookmarks_count: int = Bookmark.query.count()
    return render_template(
        'index.html',
        posts=posts,
        bookmarks_count=bookmarks_count
    )



@bp.route('/', methods=['GET'])
@bp.route('/index', methods=['GET'])
def index():
    return 'It\'s works'
