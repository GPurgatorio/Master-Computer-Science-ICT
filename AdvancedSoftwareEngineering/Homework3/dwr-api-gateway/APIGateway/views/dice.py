import requests
from flakon import SwaggerBlueprint
from flask import url_for, redirect, render_template, request, session
from flask_login import login_required
from werkzeug.exceptions import BadRequestKeyError

from APIGateway.urls import *

diceapi = SwaggerBlueprint('dice', '__name__', swagger_spec=os.path.join(YML_PATH, 'dice-api.yaml'))


# Renders the Setting page (settings.html), where the set and number of dice can be chosen.
@diceapi.operation('getSettingsPage')
@login_required
def _get_settings_page():
    try:
        x = requests.get(DICE_URL + '/sets')
    except requests.exceptions.ConnectionError:
        return service_not_up()

    if check_service_up(x):
        # No dice sets are loaded into the dice microservice
        if x.status_code == 204:
            flash("No dice set found. Please contact Jacopo Massa")
            redirect(url_for('gateway._home'))
        else:  # status_code < 300 ?
            sets = x.json()
            return render_template("settings.html", sets=sets, home_url=GATEWAY_URL)
    else:
        return redirect(url_for('gateway._home'))


# Renders the Roll page (roll_dice.html) with the rolled dice (set and num of dice previously chosen).
@diceapi.operation('getRollPage')
@login_required
def _get_roll_page():
    # Tries to get the dice_number from the request and set it into session
    try:
        dice_number = int(request.form['dice_number'])
        session['dice_number'] = dice_number
    # If it fails, set the dice_number with the one in session
    except BadRequestKeyError:
        dice_number = session['dice_number']

    # Tries to get the set id and name, which are in the form of "ID_NAME"
    try:
        s = request.form['dice_img_set'].split('_', 1)
        id_set = s[0]
        name_set = s[1]
        session['id_set'] = id_set
        session['name_set'] = name_set
    # If it fails, set the set's id and name with the ones in session
    except BadRequestKeyError:
        id_set = session['id_set']
        name_set = session['name_set']

    # Actually roll the dice
    data = {'dice_number': dice_number}
    try:
        x = requests.post(DICE_URL + '/sets/{}/roll'.format(id_set), json=data)
    except requests.exceptions.ConnectionError:
        return service_not_up()

    if check_service_up(x):
        body = x.json()

        # If everything's fine, show the rolled dice and save references
        if x.status_code < 300:
            words = []
            dice_indexes = []
            for n, fig in body.items():
                dice_indexes.append(int(n) - 1)
                words.append(fig)
            session['figures'] = words

            context_vars = {"dice_number": dice_number, "dice_img_set": name_set,
                            "words": words, "dice_indexes": dice_indexes, "home_url": GATEWAY_URL}
            return render_template("roll_dice.html", **context_vars)

        # Else flash the error and redirect to the first page (settings.html) to restart
        else:
            flash(body['description'], 'error')
            return redirect(url_for('dice._get_settings_page'))
    else:
        return redirect(url_for('gateway._home'))
