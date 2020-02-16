import datetime as dt

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import CheckConstraint
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.Unicode(128), nullable=False)
    firstname = db.Column(db.Unicode(128))
    lastname = db.Column(db.Unicode(128))
    password = db.Column(db.Unicode(128))
    dateofbirth = db.Column(db.DateTime)

    follower_counter = db.Column(db.Integer, default=0, )

    is_active = db.Column(db.Boolean, default=True)
    is_admin = db.Column(db.Boolean, default=False)
    is_anonymous = False

    def __init__(self, *args, **kw):
        super(User, self).__init__(*args, **kw)
        self._authenticated = False

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def authenticate(self, password):
        checked = check_password_hash(self.password, password)
        self._authenticated = checked
        return self._authenticated

    def serialize(self):
        return {
            'id'            : self.id,
            'email'         : self.email,
            'firstname'     : self.firstname,
            'lastname'      : self.lastname
        }
    
    def serialize_all(self):
        return {
            'id'                : self.id,
            'email'             : self.email,
            'firstname'         : self.firstname,
            'lastname'          : self.lastname,
            'dateofbirth'       : dump_datetime(self.dateofbirth),
            'follower_counter'  : self.follower_counter,
            'is_admin'          : self.is_admin
        }

    __table_args__ = (CheckConstraint(follower_counter >= 0, name='follower_counter_positive'), {})


class Follower(db.Model):
    __tablename__ = 'follower'

    follower_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    follower = relationship('User', foreign_keys='Follower.follower_id')

    followed_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    followed = relationship('User', foreign_keys='Follower.followed_id')

    date_format = "%Y %m %d %H:%M"
    creation_date = db.Column(db.DateTime, default = dt.datetime.strptime(dt.datetime.now().strftime(date_format), date_format))

    __table_args__ = (CheckConstraint(followed_id != follower_id, name='check_follow_myself'), {})


def dump_datetime(value):
    return value.strftime('%d/%m/%Y')