from browser import document, svg, timer

from core import *
from gui import draw_nodes


def main_update():
    for c in Converter.converters.values():
        c.update()
    for r in Resource.resources.values():
        r.update()
    draw_nodes()

timer.set_interval(main_update, 1000)
