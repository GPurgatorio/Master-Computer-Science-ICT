import os
from flask import Flask
from monolith.database import db, User, Story
from monolith.views import blueprints
from monolith.auth import login_manager
import datetime


def create_app():
    app = Flask(__name__)
    app.config['WTF_CSRF_SECRET_KEY'] = 'A SECRET KEY'
    app.config['SECRET_KEY'] = 'ANOTHER ONE'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///storytellers.db'

    for bp in blueprints:
        app.register_blueprint(bp)
        bp.app = app

    db.init_app(app)
    login_manager.init_app(app)
    db.create_all(app=app)

    # create a first admin user
    with app.app_context():
        q = db.session.query(User).filter(User.email == 'example@example.com')
        user = q.first()
        if user is None:
            example = User()
            example.firstname = 'Admin'
            example.lastname = 'Admin'
            example.email = 'example@example.com'
            example.dateofbirth = datetime.datetime(2020, 10, 5)
            example.is_admin = True
            example.set_password('admin')
            db.session.add(example)
            db.session.commit()

        q = db.session.query(Story).filter(Story.id == 1)
        story = q.first()
        if story is None:
            example = Story()
            example.text = 'Trial story of example admin user :)'
            example.likes = 42
            example.author_id = 1
            example.figures = 'example#admin'
            print(example)
            db.session.add(example)
            db.session.commit()

        q = db.session.query(User).filter(User.email == 'ciao@ciao.com')
        user = q.first()
        if user is None:
            example = User()
            example.firstname = 'Ciao'
            example.lastname = 'Ciao'
            example.email = 'ciao@ciao.com'
            example.dateofbirth = datetime.datetime(2020, 10, 5)
            example.is_admin = False
            example.set_password('ciao')
            db.session.add(example)
            db.session.commit()

        q = db.session.query(Story).filter(Story.id == 2)
        story = q.first()
        if story is None:
            example = Story()
            example.text = 'First'
            example.likes = 40
            example.author_id = 2
            example.figures = 'example#ciao'
            print(example)
            db.session.add(example)
            db.session.commit()

        q = db.session.query(User).filter(User.email == 'nini@nini.com')
        user = q.first()
        if user is None:
            example = User()
            example.firstname = 'Nini'
            example.lastname = 'Nini'
            example.email = 'nini@nini.com'
            example.dateofbirth = datetime.datetime(2010, 8, 5)
            example.is_admin = False
            example.set_password('nini')
            db.session.add(example)
            db.session.commit()

        q = db.session.query(Story).filter(Story.id == 3)
        story = q.first()
        if story is None:
            example = Story()
            example.text = 'Ninininininiinininininini'
            example.likes = 3
            example.author_id = 3
            example.figures = 'example#nini'
            print(example)
            db.session.add(example)
            db.session.commit()

        q = db.session.query(Story).filter(Story.id == 4)
        story = q.first()
        if story is None:
            example = Story()
            example.text = 'This is the second one u should see this only and not First'
            example.likes = 5
            example.author_id = 2
            example.figures = 'example#ciao'
            print(example)
            db.session.add(example)
            db.session.commit()
    return app


if __name__ == '__main__':
    app = create_app()
    app.run()
