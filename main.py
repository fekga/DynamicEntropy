from browser import document, svg, timer
# Visible content
document["loading"].attrs["style"] = "display:none"
document["content"].attrs["style"] = "display:block"


from core.core import *
from core.data import *
from gui.gui import *


def tick():
    for c in Converter.converters:
        c.update()
    for r in Resource.resources:
        r.update()
        # print(r)
    # print()

tick_caller = timer.set_interval(tick, 500)
timer.set_interval(drawing, 100)


# for dev
def hard_reset(event):
    for r in Resource.resources:
        r.amount = 0
    for c in Converter.converters:
        c.running = False
document["reset"].bind("click", hard_reset)


def dev_tick(event):
    global tick_caller
    timer.clear_interval(tick_caller)
    if event.target.checked:
        tick_caller = timer.set_interval(tick, 50)
    else:
        tick_caller = timer.set_interval(tick, 500)
document["dev_tick"].bind("change", dev_tick)