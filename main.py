from browser import document, svg, timer

from core import *
import data
from gui import *


def tick():
    for c in Converter.converters.values():
        c.update()
    for r in Resource.resources.values():
        r.update()
        # print(r)
    # print()

timer.set_interval(tick, 100)
timer.set_interval(drawing, 100)


# for dev
def hard_reset(event):
    for r in Resource.resources.values():
        r.amount = 0
    for c in Converter.converters.values():
        c.running = False
document["reset"].bind("click", hard_reset)
