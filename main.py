from browser import document, svg, timer

from core import *
from gui import *


def main_update():
    for c in Converter.converters.values():
        c.update()
    for r in Resource.resources.values():
        r.update()
        print(r)
    print()

    drawing()

# timer.set_interval(main_update, 0)
