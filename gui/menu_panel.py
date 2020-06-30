# menu_panel.py
from browser import svg, document
from core.time_measurement import TimeMeasurment

def update_menu_panel():
    document['timer'].text = "Playtime: " + TimeMeasurment.printElapsedTime()