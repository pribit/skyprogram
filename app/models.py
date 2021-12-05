from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(63), index=True, unique=True)
    avatar = db.Column(db.String, nullable=True)


class Post(db.Model):
    __searchable__ = ['content']

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    content = db.Column(db.Text)
    likes_count = db.Column(db.Integer)
    views_count = db.Column(db.Integer)
    pic = db.Column(db.String)

    def __repr__(self):
        return f'<Post id={self.id}, user_id={self.user_id}, ' + \
               f'content={self.content if len(self.content) <= 39 else f"{self.content[:39]}..."}'


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
