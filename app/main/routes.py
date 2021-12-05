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


@bp.route('/posts/<int:post_id>')
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
        posts = Post.search_by_like(search_form.s.data, limit=10)

    return render_template(
        'search.html',
        posts=posts,
        search_form=search_form,
        title='search',
    )


@bp.route('/user/<string:username>')
def user_feed(username: str):
    user: User = User.query.filter_by(username=username).first_or_404()

    return render_template(
        'user-feed.html',
        user=user,
        title='user feed',
    )


@bp.route('/tag/<string:tag_name>')
def tag_feed(tag_name: str):
    posts: Post = Post.search_by_like(tag_name, limit=None)

    return render_template(
        'tag-feed.html',
        tag_name=tag_name,
        posts=posts,
        title='tag'
    )


@bp.route('/bookmarks/add/<int:post_id>')
def add_post_to_bookmarks(post_id: int):
    bookmark: Bookmark = Bookmark.query.filter_by(post_id=post_id).first()

    if bookmark:
        return redirect(url_for('main.feed'), code=302)

    post: Post = Post.query.filter_by(id=post_id).first_or_404()

    db.session.add(Bookmark(post_id=post.id))
    db.session.commit()

    return redirect(url_for('main.feed'), code=302)


@bp.route('/bookmarks/remove/<int:bookmark_id>')
def remove_post_from_bookmarks(bookmark_id: int):
    bookmark: Bookmark = Bookmark.query.filter_by(id=bookmark_id).first_or_404()

    db.session.delete(bookmark)
    db.session.commit()

    return redirect(url_for('main.feed'), code=302)


@bp.route('/bookmarks')
def bookmarks():
    bookmarks: Bookmark = Bookmark.query

    return render_template(
        'bookmarks.html',
        bookmarks=bookmarks
    )


@bp.route('/raise_500')
def raise_500():
    raise Exception
