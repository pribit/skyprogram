import re
from typing import Optional

from flask import url_for

from app import db


def add_links_to_hash_tags(text: str):
    hash_tag_regexp = re.compile('\\B(#(?:\\w|\\d)+\\b)')
    hash_tags = re.findall(hash_tag_regexp, text)

    for hash_tag in hash_tags:
        text = text.replace(
            hash_tag,
            f'<a class="item__tag" href="{url_for("main.tag_feed", tag_name=hash_tag)}">{hash_tag}</a>',
            1
        )

    return text


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(63), index=True, unique=True)
    avatar = db.Column(db.String, nullable=True)

    posts = db.relationship('Post', backref='author', lazy='dynamic')
    comments = db.relationship('Comment', backref='author', lazy='dynamic')


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    content = db.Column(db.Text)
    likes_count = db.Column(db.Integer)
    views_count = db.Column(db.Integer)
    pic = db.Column(db.String)

    comments = db.relationship('Comment', backref='post', lazy='dynamic')

    @staticmethod
    def search_by_like(looking_for: str, limit: Optional[int]):
        posts: Post = Post.query.filter(db.func.lower(Post.content).like(db.func.lower(f'%{looking_for}%')))

        if limit:
            posts = posts.limit(limit)

        return posts

    def get_content(self, minify: bool = False):
        content = add_links_to_hash_tags(self.content)

        if minify:
            if len(content) <= 50:
                return content

            return f'{content[:50]}...'

        return content

    def get_comment_count_string(self) -> str:
        comments_count: int = self.comments.count()

        if comments_count == 0:
            return 'Нет комментариев'
        else:
            if 2 <= comments_count % 10 <= 4 and not 12 <= comments_count % 100 <= 14:
                return f'{comments_count} комментария'
            elif comments_count % 10 == 1 and comments_count % 100 != 11:
                return f'{comments_count} комментарий'
            else:
                return f'{comments_count} комментариев'

    def __repr__(self):
        return f'<Post id={self.id}, user_id={self.user_id}, ' + \
               f'content={self.content if len(self.content) <= 39 else f"{self.content[:39]}..."}'


db.Index('post_lower_content_idx', db.func.lower(Post.__table__.c.content))


class Bookmark(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))

    post = db.relationship('Post', backref=db.backref('bookmark', uselist=False))

    def __repr__(self):
        return f'<Bookmark id={self.id}, post_id={self.post_id}>'


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    comment = db.Column(db.Text)

    def get_comment(self):
        return add_links_to_hash_tags(self.comment)

    def __repr__(self):
        return f'<Comment id={self.id}, post_id={self.post_id}> ' + \
               f'commenter_name={self.commenter_name}, comment={self.comment}'
