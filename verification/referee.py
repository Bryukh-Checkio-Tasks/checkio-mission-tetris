import random
# from checkio.signals import ON_CONNECT
# from checkio import api
# from multi_score import CheckiORefereeMultiScore
# from checkio.referees import cover_codes
# from checkio.referees import checkers

from tests import TESTS


from figures import FIGURES

WIDTH = 10
HEIGHT = 10

EXTRA_HEIGHT = 15

SHIFT = 4

ACTIONS = "RLAC"

LEFT = "L"
RIGHT = "R"
CLOCK = "C"
CONTER = "A"


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


def rotate_figure(f, nrotates):
    work = [row[:] for row in f]
    if nrotates == 1:
        return list(zip(*work[::-1]))
    elif nrotates == 2:
        return [row[::-1] for row in work[::-1]]
    elif nrotates == 3:
        return list(zip(*work))[::-1]
    else:
        return work


def process_figure(fig, action):
    rotates = (action.count(CLOCK) - action.count(CONTER)) % 4
    rfig = rotate_figure(fig, rotates)
    shift = min(max(action.count(RIGHT) - action.count(LEFT) + SHIFT, 0), WIDTH - len(rfig[0]))
    h = len(rfig)
    wf = len(rfig[0])
    rfig = list(zip(*rfig))
    import ipdb; ipdb.set_trace()
    res = [[0] * h for _ in range(shift)] + rfig + [[0] * h for _ in range(WIDTH - shift - wf)]
    return list(zip(*res))


def process(data, user):
    if not isinstance(user, str) or not all(x in ACTIONS for x in user):
        data.update({"result": False, "result_text": "You should return a string with actions."})
        return data
    figure = data["current_figure"]
    level = data["level"]
    available_figures = sum(FIGURES[:level+1], [])
    next_figure = data["next_figure"]

    data["next_figure"] = random.choice(available_figures)
    data["current_figure"] = next_figure
    full_up = process_figure(figure, user)


cover = """def cover(f, data):
    to_tuple = lambda x: tuple(tuple(row) for row in x)
    return f(to_tuple(data[0]), to_tuple(data[1]), to_tuple(data[2]), data[3])
"""


# api.add_listener(
#     ON_CONNECT,
#     CheckiORefereeMultiScore(
#         tests=TESTS,
#         cover_code={
#             'python-27': cover,
#             'python-3': cover
#         },
#         initial_referee=init,
#         process_referee=None,
#         is_win_referee=None
#         # checker=None,  # checkers.float.comparison(2)
#         # add_allowed_modules=[],
#         # add_close_builtins=[],
#         # remove_allowed_modules=[]
#     ).on_ready)







# ========================================== #
f = [[1, 0, 0], [1, 1, 1]]
result = process_figure(f, "CCALLLLLR")
for row in result:
    print(row)
