import os

from flask import Blueprint, jsonify, session, abort, render_template, request
from flask_login import login_required

from monolith.classes.DiceSet import DiceSet, Die

dice = Blueprint('dice', __name__)


@login_required
@dice.route('/stories/dice/roll', methods=['GET'])
def _roll_dice():

    dice_list = []
    for i in range(0, 6):
        try:
            dice_list.append(Die('monolith/resources/die' + str(i) + '.txt'))
        except FileNotFoundError:
            print("File die" + str(i) + ".txt not found")
    dice_set = DiceSet(dice_list)
    try:
        dice_set.throw_dice()
    except IndexError as e:
        abort(500, 'Error in throwing dice')
    session['figures'] = dice_set.pips
    return render_template('roll_dice.html', words=dice_set.pips, write_url="http://127.0.0.1:5000/stories/write")
