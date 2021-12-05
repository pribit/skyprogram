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


@bp.route('/posts/<post_id>')
def post(post_id: int):
    post = Post.query.filter_by(id=post_id).first_or_404()

    return render_template(
        'post.html',
        post=post,
        title='post',
    )


@bp.route('/search')
def search():
    looking_for = request.args.get('s')
    return render_template('search.html')


@bp.route('/user/<username>')
def user_feed(username: str):
    return render_template('user-feed.html')


@bp.route('/tag/<tag_name>')
def tag_feed(tag_name: str):
    return render_template('tag.html')


@bp.route('/bookmarks/add/<post_id>', methods=['POST'])
def add_post_to_bookmarks(post_id: int):
    return redirect(url_for('/'), code=302)


@bp.route('/bookmarks')
def bookmarks():
    return render_template('bookmarks.html')
