from typing import Union

from flask import render_template, url_for
from werkzeug.utils import redirect

from app import db
from app.main import bp
from app.main.forms import SearchForm
from app.models import Bookmark, Post, User


@bp.route('/')
def feed():
    posts: Post = Post.query

    bookmarks_count: int = Bookmark.query.count()

    search_form: SearchForm = SearchForm(csrf_enabled=False)

    return render_template(
        'index.html',
        posts=posts,
        bookmarks_count=bookmarks_count,
        search_form=search_form,
    )


@bp.route('/posts/<post_id>')
def post(post_id: int):
    post: Post = Post.query.filter_by(id=post_id).first_or_404()

    return render_template(
        'post.html',
        post=post,
        title='post',
    )


@bp.route('/search')
def search():
    search_form: SearchForm = SearchForm(csrf_enabled=False)

    posts: Union[list, Post] = []

    if search_form.validate():
        posts = Post.query.filter(db.func.lower(Post.content).like(db.func.lower(f'%{search_form.s.data}%'))).limit(10)

    return render_template(
        'search.html',
        posts=posts,
        search_form=search_form,
        title='search',
    )


@bp.route('/user/<username>')
def user_feed(username: str):
    user: User = User.query.filter_by(username=username).first_or_404()

    return render_template(
        'user-feed.html',
        user=user,
        title='user feed',
    )


@bp.route('/tag/<tag_name>')
def tag_feed(tag_name: str):
    return render_template('tag.html')


@bp.route('/bookmarks/add/<post_id>', methods=['POST'])
def add_post_to_bookmarks(post_id: int):
    return redirect(url_for('/'), code=302)


@bp.route('/bookmarks')
def bookmarks():
    return render_template('bookmarks.html')
