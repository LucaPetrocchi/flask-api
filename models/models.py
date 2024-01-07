from extensions import db
from sqlalchemy import ForeignKey
from datetime import datetime

class CRUD(object):
    
    def save(self, commit=True):
        db.session.add(self)
        if commit:
            db.session.commit()
        return self

    @classmethod
    def create(cls, **kwargs):
        instance = cls(**kwargs)
        return instance.save()
    
    def update(self, commit=True, **kwargs):
        print(kwargs)
        for attr, value in kwargs.items():
            if value is not None:
                setattr(self, attr, value)
        if commit:
            db.session.commit()
        return self
    
    def delete(self, commit=True):
        db.session.delete(self)
        if commit:
            return db.session.commit()
        
class Model(CRUD, db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key = True)

    @classmethod
    def get_by_id(cls, id):
        return cls.query.get(int(id))

class User(Model):
    __tablename__ = 'user'
    name = db.Column(db.String(100), nullable = False)
    email = db.Column(db.String(100), nullable = True, unique = True)
    password = db.Column(db.String(500), nullable = False)
    is_admin = db.Column(db.Boolean, default = False)
    date_created = db.Column(db.DateTime, 
                      nullable = False, 
                      default = datetime.utcnow)
    posts = db.relationship('Post', cascade = 'all, delete')

    def __repr__(self):
        return f'<User({self.name!r})>'

post_tags = db.Table('post_tags',
    db.Column(
        'post_id',
        db.Integer,
        ForeignKey('post.id'),
        primary_key=True,
    ),
    db.Column(
        'tag_id',
        db.Integer,
        ForeignKey('tag.id'),
        primary_key=True,
    )
)

class Post(Model):
    __tablename__ = 'post'
    title = db.Column(db.String(100), nullable = False)
    content = db.Column(db.String(100), nullable = False)
    date = db.Column(db.DateTime, 
                      nullable = False, 
                      default = datetime.utcnow)
    user_id = db.Column(db.Integer,
                        ForeignKey('user.id'),
                        nullable = False)
    user_obj = db.relationship('User', viewonly=True)
    tags = db.relationship('Tag',
                           secondary = post_tags,
                           cascade = 'all, delete')
    replies = db.relationship('Reply', cascade = 'all, delete')

    def __repr__(self):
        return f'<Reply({self.title!r})'


class Tag(Model):
    __tablename__ = 'tag'
    name =  db.Column(db.String(100), nullable = False, unique = True)
    
    def __repr__(self):
        return f'<Tag({self.name!r})'
    
class Reply(Model):
    __tablename__ = 'reply'
    post_id = db.Column(db.Integer,
                        ForeignKey('post.id'),
                        nullable = False)
    content = db.Column(db.String(100), nullable = False)
    date = db.Column(db.DateTime, 
                      nullable = False, 
                      default = datetime.utcnow)
    user_id = db.Column(db.Integer,
                        ForeignKey('user.id'),
                        nullable = False)
    user_obj = db.relationship('User', viewonly=True)

    def __repr__(self):
        return f'<Reply({self.id!r})'
