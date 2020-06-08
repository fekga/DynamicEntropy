# main.py

from core import *
from gui import draw_nodes
import time

while True:
    for c in Converter.converters.values():
        c.update()

    for r in Resource.resources.values():
        r.update()
        # print(r)

    draw_nodes()

    # print()
    time.sleep(.1)
