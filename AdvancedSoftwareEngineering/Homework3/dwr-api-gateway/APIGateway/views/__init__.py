from .auth import authapi
from .users import usersapi
from .dice import diceapi
from .stories import storiesapi

blueprints = [authapi, usersapi, diceapi, storiesapi]
