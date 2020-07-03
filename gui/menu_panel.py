# menu_panel.py
from browser import svg, document, html
from core.time_measurement import TimeMeasurment
from gui.front_page import create_front_blank_page

def update_menu_panel():
    document['timer'].text = "Playtime: " + TimeMeasurment.printElapsedTime()

class HowToMenuItem:
    def __init__(self, whereToPut):
        self.button = html.DIV("How to")
        self.show = False
        self.button.bind("click", lambda ev, self=self: self.toggle_howToInfo())
        self.content = None

        whereToPut <= self.button

    def show_howToInfo(self):
        if self.content is None:
            text = "<h1>How to play</h1>"
            text += "<h2>Dynamic Entropy</h2>"
            text += "<br>"
            text += "Right click nodes to start or stop them.<br>"
            text += "Left click nodes to show or hide the information panel.<br>"
            text += "Left click upgrades to buy them on the information panel of the nodes.<br>"
            text += "Upgrades can be only bought when you have the required resources<br>"
            text += "Hover over the resources on the side panel to highlight the nodes which need or create that resource.<br>"
            text += "Drag the play are with left click to move it around.<br>"
            text += "<br>"
            text += "Nodes can only function if they have enough input resource.<br>"
            text += "Nodes won't work if the output resource has reached it's maximum value.<br>"
            text += "<br>"
            text += "When nothing seems to work, try twiddling your thumbs to lose your Stamina and fall asleep.<br>"
            text += "<br>"
            text += "Good luck!<br>"
            self.content = create_front_blank_page(text) # already added to html
        self.show = True

    def hide_howToInfo(self):
        self.content.remove()
        self.content = None
        self.show = False

    def toggle_howToInfo(self):
        if self.show:
            self.hide_howToInfo()
        else:
            self.show_howToInfo()
