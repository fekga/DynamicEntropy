# menu_panel.py
from browser import svg, document, html
from core.time_measurement import TimeMeasurment

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
            text += "This is how to write the tutorial. PLEASE WRITE ME.<br>"
            text += "You can make new line like <br> See?<br>"
            text += "Bold text like <strong>this</strong><br>"
            text += "Make list like this:<ul><li>One</li><li>Two</li><li>Three</li></ul><br>"
            self.content = html.DIV(style={
                'width':'80%', "height":"70%","border":"3px solid #000",
                'background':'white',
                'position':'absolute', 'top':'50px',
                'margin': "50px"
            })
            self.content <= html.DIV(text, style={
                'margin': "50px", 'font-size': '20px'
            })
            document['content'] <= self.content
        self.show = True

    def hide_howToInfo(self):
        self.content.remove()
        self.content = None
        self.show = False

    def toggle_howToInfo(self):
        if self.show:
            self.hide_howToInfo()
            print("hide")
        else:
            self.show_howToInfo()
            print("show")