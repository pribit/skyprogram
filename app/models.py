from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(63), index=True, unique=True)
    avatar = db.Column(db.String, nullable=True)

    posts = db.relationship('Post', backref='author', lazy='dynamic')
    comments = db.relationship('Comment', backref='author', lazy='dynamic')


class Post(db.Model):
    __searchable__ = ['content']

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    content = db.Column(db.Text)
    likes_count = db.Column(db.Integer)
    views_count = db.Column(db.Integer)
    pic = db.Column(db.String)

    comments = db.relationship('Comment', backref='post', lazy='dynamic')

    def get_content(self):
        if len(self.content) <= 50:
            return self.content
        else:
            return f'{self.content[:50]}...'

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

    def __repr__(self):
        return f'<Bookmark id={self.id}, post_id={self.post_id}>'


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    comment = db.Column(db.Text)

    def __repr__(self):
        return f'<Comment id={self.id}, post_id={self.post_id}> ' + \
               f'commenter_name={self.commenter_name}, comment={self.comment}'
