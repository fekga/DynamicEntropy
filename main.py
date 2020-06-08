from browser import document, svg, timer

from core import *
from gui import draw_nodes


def main_update():
    for c in Converter.converters.values():
        c.update()

    for r in Resource.resources.values():
        r.update()
        # print(r)

    # draw_nodes()

    print("update")

    # print()
    # time.sleep(.1)
    # timer.sleep(.1)
    # time(.1)

timer.set_interval(main_update(), 1000)
