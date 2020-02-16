import requests
from flakon import SwaggerBlueprint
from flask import render_template, request, redirect, url_for, session
from flask_login import login_required, current_user

from APIGateway.forms import StoryForm
from APIGateway.tasks import reaction_task
from APIGateway.urls import *

storiesapi = SwaggerBlueprint('stories', '__name__', swagger_spec=os.path.join(YML_PATH, 'stories-api.yaml'))


# Renders the Stories page (stories.html), where ALL the published stories are seen
@storiesapi.operation('getAll')
def _get_all_stories():
    try:
        x = requests.get(STORY_URL + '/stories')
    except requests.exceptions.ConnectionError:
        return service_not_up()

    stories = []

    if check_service_up(x):
        stories = x.json()

    return render_template("stories.html", stories=stories, home_url=GATEWAY_URL)


# Renders the Stories page (stories.html) with only the last published story for each registered user
@storiesapi.operation('getLatest')
def _get_latest():
    try:
        x = requests.get(STORY_URL + '/stories/latest')
    except requests.exceptions.ConnectionError:
        return service_not_up()
    stories = []

    if check_service_up(x):
        stories = x.json()

    return render_template("stories.html", stories=stories, home_url=GATEWAY_URL)


# Renders the Stories page (stories.html) with only the stories published in a specified period
@storiesapi.operation('getRange')
def _get_range():
    # Get the begin and end date to put it into the query
    begin = request.args.get('begin')
    end = request.args.get('end')
    try:
        x = requests.get(STORY_URL + '/stories/range?begin={}&end={}'.format(begin, end))
    except requests.exceptions.ConnectionError:
        return service_not_up()
    if check_service_up(x):
        body = x.json()

        if x.status_code < 300:
            return render_template("stories.html", stories=body, home_url=GATEWAY_URL)

        else:
            flash(body['description'])
            return redirect(url_for('stories._get_all_stories'))
    else:
        return redirect(url_for('gateway._home'))


# Renders the Drafts page (drafts.html) with al the drafts of the logged user
@storiesapi.operation('getDrafts')
@login_required
def _get_drafts():
    try:
        s = requests.get(STORY_URL + '/stories/drafts?user_id={}'.format(current_user.id))
    except requests.exceptions.ConnectionError:
        return service_not_up()
    stories = []
    if s.status_code < 300:
        stories = s.json()

    return render_template("drafts.html", drafts=stories, home_url=GATEWAY_URL)


# Renders the Story page (story.html) with the specified story
@storiesapi.operation('getStory')
def _get_story(id_story):
    try:
        x = requests.get(STORY_URL + '/stories/{}'.format(id_story))
    except requests.exceptions.ConnectionError:
        return service_not_up()

    if check_service_up(x):
        body = x.json()
        return render_story(body)
    else:
        return redirect(url_for('gateway._home'))


# The operation to delete a previously published story
@storiesapi.operation('deleteStory')
def _delete_story(id_story):
    try:
        x = requests.delete(STORY_URL + '/stories/{}'.format(id_story), json={'user_id': current_user.id})
    except requests.exceptions.ConnectionError:
        return service_not_up()

    if check_service_up(x):
        body = x.json()
        flash(body['description'])

    return redirect(url_for('gateway._home'))


# Renders the Write page (write_story.html) where it's possible to publish a story (or save it as draft)
@storiesapi.operation('getWritePage')
@login_required
def _get_write_page():
    form = StoryForm()
    # If the user gets here in an unexpected way, redirect to home
    if 'figures' not in session:
        flash("You need to set a story before", 'error')
        redirect(url_for('gateway._home'))

    return render_template("write_story.html", form=form, id_draft=None, words=session['figures'], home_url=GATEWAY_URL)


# The operation to actually publish (or save as draft) a story
@storiesapi.operation('writeNew')
@login_required
def _write_new():
    form = request.form
    # Get the needed data from the form, then post it to the Stories service
    figures = '#' + '#'.join(session['figures']) + '#'
    data = {"as_draft": bool(int(form['as_draft'])), "text": form['text'],
            "user_id": current_user.id, "figures": figures}
    try:
        x = requests.post(STORY_URL + '/stories', json=data)
    except requests.exceptions.ConnectionError:
        return service_not_up()

    if check_service_up(x):
        body = x.json()

        # If everything's fine, remove from the session the loaded data and redirect to the page with all the stories
        if x.status_code < 300:
            session.pop('figures')
            session.pop('id_set')
            session.pop('name_set')
            session.pop('dice_number')
            return redirect(url_for('stories._get_all_stories'))
        # Else reload the page with the specified error
        else:
            new_form = StoryForm()
            new_form.text.data = form['text']
            return render_template("write_story.html", message=body['description'], id_draft=None,
                                   form=new_form, words=session['figures'], home_url=GATEWAY_URL)
    else:
        return redirect(url_for('gateway._home'))


# Renders the Write page (write_story.html) with a previously created draft
@storiesapi.operation('getDraftPage')
@login_required
def _get_draft_page(id_story):
    form = StoryForm()
    try:
        x = requests.get(STORY_URL + '/stories/{}'.format(id_story))
    except requests.exceptions.ConnectionError:
        return service_not_up()

    if check_service_up(x):
        body = x.json()
        if x.status_code < 300:
            if body['author_id'] == current_user.id:
                form.text.data = body['text']
                session['figures'] = body['figures'].split('#')
            else:
                flash("You are not the author of the story", 'error')
                return redirect(url_for('gateway._home'))
        else:
            flash(body['description'], 'error')
            return redirect(url_for('gateway._home'))

        return render_template("write_story.html", form=form, id_draft=id_story, words=session['figures'][1:-1],
                               home_url=GATEWAY_URL)
    else:
        return redirect(url_for('gateway._home'))


# The operation to complete a draft, similar to the previous one
@storiesapi.operation('completeDraft')
@login_required
def _complete_draft(id_story):
    form = request.form
    figures = '#' + '#'.join(session['figures']) + '#'
    data = {"as_draft": bool(int(form['as_draft'])), "text": form['text'],
            "user_id": current_user.id, "figures": figures}

    try:
        x = requests.put(STORY_URL + '/stories/{}'.format(id_story), json=data)
    except requests.exceptions.ConnectionError:
        return service_not_up()

    if check_service_up(x):
        body = x.json()

        if x.status_code < 300:
            session.pop('figures')
            return redirect(url_for('stories._get_all_stories'))
        else:
            new_form = StoryForm()
            new_form.text.data = form['text']
            return render_template("write_story.html", message=body['description'],
                                   form=new_form, id_draft=id_story, words=session['figures'][1:-1],
                                   home_url=GATEWAY_URL)
    else:
        return redirect(url_for('gateway._home'))


# Renders the Story page (story.html) with a randomly chosen story from other authors
@storiesapi.operation('getRandom')
def _get_random():
    method = '/stories/random'
    # If there's a logged user, then we concatenate its id to not get his stories
    if current_user is not None and hasattr(current_user, 'id'):
        method += '?user_id={}'.format(current_user.id)

    try:
        x = requests.get(STORY_URL + method)
    except requests.exceptions.ConnectionError:
        return service_not_up()

    if check_service_up(x):
        body = x.json()

        if x.status_code < 300:
            return render_story(body)
        else:
            flash(body['description'], "error")

        return redirect(url_for("stories._get_all_stories"))
    else:
        return redirect(url_for('gateway._home'))


# The operation to react to a specific story
@storiesapi.operation('reactStory')
@login_required
def _react_story(id_story, reaction_caption):
    r_task = reaction_task.delay(id_story, reaction_caption, current_user.id)

    try:
        s = requests.get(STORY_URL + "/stories/{}".format(id_story))
    except requests.exceptions.ConnectionError:
        return service_not_up()

    if check_service_up(s):
        if s.status_code < 300:
            return redirect(url_for('stories._get_story', id_story=id_story))
        else:
            flash("Error retrieving story!", 'error')

    return redirect(url_for('gateway._home'))


#                   Useful functions

def render_story(story=None):
    context_vars = {"home_url": GATEWAY_URL, "react_url": GATEWAY_URL + 'stories/{}/react',
                    "exists": (story is not None)}
    if story:
        try:
            u = requests.get(USER_URL + "/users/{}".format(story['author_id']))
        except requests.exceptions.ConnectionError:
            return service_not_up()

        if u.status_code < 300:
            try:
                r = requests.get(REACTION_URL + '/reactions/stats/{}'.format(story['id']))
            except requests.exceptions.ConnectionError:
                return service_not_up()

            if r.status_code < 300:
                rolled_dice = story['figures'].split('#')
                rolled_dice = rolled_dice[1:-1]
                context_vars.update({"rolled_dice": rolled_dice, "story": story,
                                     "user": u.json(), "reactions": r.json()})

        else:
            flash("Can't find author of this story", "error")
            return redirect(url_for('stories._get_all_stories'))

    return render_template("story.html", **context_vars)
