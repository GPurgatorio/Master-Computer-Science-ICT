# encoding: utf8
from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class ReactionCatalogue(db.Model):
    __tablename__ = 'reaction_catalogue'

    reaction_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    reaction_caption = db.Column(db.Text(20))


class Reaction(db.Model):
    __tablename__ = 'reaction'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    reactor_id = db.Column(db.Integer, nullable=False)

    story_id = db.Column(db.Integer, nullable=False)

    reaction_type_id = db.Column(db.Integer, db.ForeignKey('reaction_catalogue.reaction_id'))
    reaction_type = relationship('ReactionCatalogue', foreign_keys='Reaction.reaction_type_id')

    marked = db.Column(db.Integer, default=0)  # True iff it has been counted in Story.likes

    def to_json(self):
        json = {}
        for attr in ('id', 'reactor_id', 'story_id', 'reaction_type_id',
                     'marked'):
            value = getattr(self, attr)
            json[attr] = value
        return json


class Counter(db.Model):
    __tablename__ = 'counter'

    reaction_type_id = db.Column(db.Integer, db.ForeignKey('reaction_catalogue.reaction_id'), primary_key=True)
    reaction_type = relationship('ReactionCatalogue', foreign_keys='Counter.reaction_type_id')

    story_id = db.Column(db.Integer, primary_key=True, nullable=False)

    counter = db.Column(db.Integer, default=0)

    def to_json(self):
        json = {}
        for attr in ('reaction_type_id', 'story_id', 'counter'):
            value = getattr(self, attr)
            json[attr] = value
        return json








