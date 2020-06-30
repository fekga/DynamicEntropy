from browser import document, svg, timer
# Visible content
document["loading"].attrs["style"] = "display:none"
document["content"].attrs["style"] = "display:block"

from core.converter import Converter
from core.resource import Resource
from core.upgrade import Upgrade
from core.data import *
from core.time_measurement import *
from gui.gui import *


def tick():
    for c in Converter.converters:
        c.update()
    for r in Resource.resources:
        r.update()
        # print(r)
    # print()

tick_caller = timer.set_interval(tick, 500)


