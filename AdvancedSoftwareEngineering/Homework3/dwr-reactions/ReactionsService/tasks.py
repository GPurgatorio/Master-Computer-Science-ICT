from celery import Celery
from sqlalchemy import and_

from .app import create_app
from .database import *

_APP = None

BACKEND = BROKER = 'redis://localhost:6379'
celery = Celery(__name__, backend=BACKEND, broker=BROKER)

# Schedule for the Celery task about reactions' update
celery.conf.beat_schedule = {
    'react_task': {
        'task': 'ReactionsService.tasks.like_task',
        'schedule': 3.0
    },
}
celery.conf.timezone = 'UTC'


@celery.task
def like_task():
    global _APP
    # lazy init
    if _APP is None:
        print("App not yet initialized")
        _APP = create_app()
        db.init_app(_APP)

    with _APP.app_context():
        q = db.engine.execute(
            "SELECT story_id, reaction_type_id, reaction_caption, COUNT(*) AS count, marked "
            "FROM reaction r "
            "JOIN reaction_catalogue rc on r.reaction_type_id = rc.reaction_id "
            "WHERE marked=0 OR marked=2 "
            "GROUP BY story_id, reaction_type_id, marked "
            "ORDER BY story_id, reaction_type_id, marked").fetchall()

        print("Analyzing {} reactions: \n".format(len(q)))

        for r in q:
            print("Story {}: {} {}(s) marked to {}".format(r.story_id, r.count, r.reaction_caption, r.marked))
            counter_row = Counter.query.filter(and_(Counter.reaction_type_id == r.reaction_type_id,
                                                    Counter.story_id == r['story_id'])).first()
            if r.marked == 0:  # INCREASE COUNTER
                counter_row.counter = counter_row.counter + r.count
            else:  # DECREASE COUNTER
                counter_row.counter = counter_row.counter - r.count

            # Delete all the rows with marked = 2
            Reaction.query.filter(Reaction.marked == 2).delete()

            # Update all the rows with marked = 1
            Reaction.query.filter(Reaction.marked == 0).update({Reaction.marked: 1})
        db.session.commit()
