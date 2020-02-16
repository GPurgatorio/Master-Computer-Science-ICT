import os

from flakon import SwaggerBlueprint
from flask import jsonify, abort, request

from dice_service.database import DiceSet, Die, db

YML = os.path.join(os.path.dirname(__file__), 'dice-api.yaml')
dice = SwaggerBlueprint('dice', '__name__', swagger_spec=YML)


@dice.operation('addSet')
def _new_set():

    # check correctness of request body
    if not request.is_json:
        abort(400, "Not valid request body")
    else:
        body = request.json
        if 'name' not in body or 'dice' not in body:
            abort(400, "Name or dice are missing")
        else:
            # must have 6 dice, with 6 figures each one
            new_dice = body['dice']
            if len(new_dice) != 6 or not all((len(d) == 6 for d in new_dice)):
                abort(400, "DiceSet must be formed by 6 dice of 6 figures each one")
            # check if the set already exists
            elif DiceSet.query.filter(DiceSet.name == body['name']).first() is not None:
                abort(409, "A DiceSet called {} already exists".format(body['name']))
            else:
                # add new DiceSet
                new_set = DiceSet()
                new_set.name = body['name'].lower()
                db.session.add(new_set)
                db.session.commit()

                # create new 6 dice
                number = 1
                for d in new_dice:
                    die = Die()
                    die.number = number
                    die.figures = "#{}#".format('#'.join(d).lower())
                    die.id_set = new_set.id
                    db.session.add(die)
                    db.session.commit()
                    number += 1

                return jsonify(id_set=new_set.id, description="DiceSet successfully added"), 201


@dice.operation('getSet')
def _set(id_set):
    asked_set = DiceSet.query.filter_by(id=id_set).first()

    if asked_set is None:
        abort(404, 'DiceSet not found')
    else:
        return jsonify(asked_set.to_json())


@dice.operation('deleteSet')
def _delete_set(id_set):
    asked_set = DiceSet.query.filter_by(id=id_set).first()

    if asked_set is None:
        abort(404, 'DiceSet not found')
    else:
        db.session.delete(asked_set)
        db.session.commit()
        return jsonify(description="DiceSet successfully deleted")


@dice.operation('getSets')
def _sets():
    all_sets = DiceSet.query.all()
    # return 200 if there is more than 1 set (2xx Success OK)
    # return 204 if there is no set (2xx Success No Content)
    code = 200 if len(all_sets) > 0 else 204
    return jsonify([s.to_json_light() for s in all_sets]), code


@dice.operation('rollSet')
def _roll_set(id_set):
    asked_set = DiceSet.query.filter_by(id=id_set).first()
    # check correctness of request body
    if asked_set is None:
        abort(404, 'DiceSet not found')
    if not request.is_json:
        abort(400, "Not valid request body")
    # check presence of 'dice_number' into request body
    elif "dice_number" not in request.json or request.json['dice_number'] is None:
        abort(400, "Specify number of dice you want to roll")
    # check validity of 'dice_number'
    elif int(request.json['dice_number']) not in range(2, 7):
        abort(400, "Number of dice to roll must be between 2 and 6")
    # check presence of requested set into the db
    else:
        return jsonify(asked_set.roll_set(int(request.json['dice_number'])))
