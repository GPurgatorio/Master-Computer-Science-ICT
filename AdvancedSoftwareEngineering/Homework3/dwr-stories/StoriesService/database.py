# encoding: utf8
import datetime as dt
from builtins import isinstance, getattr, super

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Story(db.Model):
    __tablename__ = 'story'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    text = db.Column(db.Text(1000))  # around 200 (English) words
    date = db.Column(db.DateTime)
    figures = db.Column(db.Unicode(128))
    # define foreign key
    author_id = db.Column(db.Integer)
    is_draft = db.Column(db.Boolean, default=True)

    def __init__(self, *args, **kw):
        super(Story, self).__init__(*args, **kw)
        date_format = "%Y %m %d %H:%M"
        self.date = dt.datetime.strptime(dt.datetime.now().strftime(date_format), date_format)

    def to_json(self):
        json = {}
        for attr in ('id', 'text', 'date', 'figures',
                     'author_id', 'is_draft'):
            value = getattr(self, attr)
            json[attr] = value
        return json

