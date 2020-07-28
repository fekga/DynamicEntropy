from browser import document, svg, timer
# Visible content
document["loading"].attrs["style"] = "display:none"
document["content"].attrs["style"] = "display:block"

from core.data import *
from core.time_measurement import *
from gui.gui import *

TICK_REFRESH_RATE = 500

class App:
    def tick():
        for c in Converter.converters:
            c.update()
        for r in Resource.resources:
            r.update()
    
    def dev_tick(event):
        timer.clear_interval(App.tick_caller)
        if event.target.checked:
            App.tick_caller = timer.set_interval(App.tick, 50)
        else:
            App.tick_caller = timer.set_interval(App.tick, TICK_REFRESH_RATE)
    

App.tick_caller = timer.set_interval(App.tick, TICK_REFRESH_RATE)
# Dev tick checkbox connection
dev_tick_check_box = document["dev_tick_checkbox"]
dev_tick_check_box.bind("click", App.dev_tick)
