import random
from checkio.signals import ON_CONNECT
from checkio import api
from multi_score import CheckiORefereeMultiScore
from checkio.referees import cover_codes
from checkio.referees import checkers

from tests import TESTS

from figures import FIGURES

WIDTH = 10
HEIGHT = 10

EXTRA_HEIGHT = 15

ACTIONS = "RLAC"

def init(data, rseed=None):
    if rseed:
        random.seed(rseed)
    grid = [[0 for _ in range(WIDTH)] for _ in range(EXTRA_HEIGHT)]
    current = random.choice(FIGURES[0])
    next_figure = random.choice(FIGURES[0])
    return {
        "grid": grid,
        "score": 0,
        "level": 0,
        "figures": FIGURES[0],
        "current_figure": current,
        "next_figure": next_figure,
        "input": [grid, current, next_figure, 0]
    }

def process(data, user):
    if not isinstance(user, str) or not all(x in ACTIONS for x in user):
        data.update({"result": False, "result_text": "You should return a string with actions."})
        return data
    figure = data["current"]




cover = """def cover(f, data):
    to_tuple = lambda x: tuple(tuple(row) for row in x)
    return f(to_tuple(data[0]), to_tuple(data[1]), to_tuple(data[2]), data[3])
"""


api.add_listener(
    ON_CONNECT,
    CheckiORefereeMultiScore(
        tests=TESTS,
        cover_code={
            'python-27': cover,
            'python-3': cover
        },
        initial_referee=init,
        # checker=None,  # checkers.float.comparison(2)
        # add_allowed_modules=[],
        # add_close_builtins=[],
        # remove_allowed_modules=[]
    ).on_ready)
