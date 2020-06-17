# node.py
from browser import svg
from core.converter import Converter
import gui.hud as hud

class Node:
    radius = 20

    def __init__(self, converter, pos):
        self.converter = converter
        self.position = pos
        self.circle = svg.circle(cx=0, cy=0, r=self.radius,stroke="black",stroke_width="2",fill="green")
        self.circle.attrs["id"] = self.converter.name
        self.title = svg.text(self.converter.name, x=0, y=self.radius+15, z=10, font_size=15,text_anchor="middle")
        x,y = self.position
        self.circle.bind("click", self.clicked)
        self.circle.bind("contextmenu", self.right_clicked)
        self.circle.bind("mouseover", self.mouse_over)
        self.circle.bind("mouseout", self.mouse_out)
        self.connections = []
        self.hide_all()

    def clicked(self, event):
        hud.Hud.active = True
        hud.Hud.show_info(self)
        event.stopPropagation()

    def right_clicked(self, event):
        if self.converter.is_stopped():
            self.converter.start()
        else:
            self.converter.stop()

    def mouse_over(self, event):
        if not hud.Hud.active:
            hud.Hud.show_info(self)
        if not self.converter.unstoppable:
            self.circle.attrs['stroke'] = 'orange'
        # for line,node in self.connections:
            # line.attrs['stroke'] = 'green'

    def mouse_out(self, event):
        if not hud.Hud.active:
            hud.Hud.clear_hud()
        self.circle.attrs['stroke'] = 'black'
        # for line,node in self.connections:
        #     line.attrs['stroke'] = 'black'

    def try_unhide_node(self):
        if self.hidden:
            self.hidden = self.converter.stay_hidden()

    def draw(self):
        if not self.hidden:
            self.unhide_all()
            # Update
            cx, cy = self.position
            self.circle.attrs["cx"] = cx
            self.circle.attrs["cy"] = cy
            self.title.attrs["x"] = cx
            self.title.attrs["y"] = cy - self.radius - 15
            self.position = cx, cy
            state = self.converter.state
            if state == Converter.OK:
                color = "green"
            elif state == Converter.STOPPED:
                color = "gray"
            elif state == Converter.NO_INPUT:
                color = "yellow"
            elif state == Converter.MAX_OUTPUT:
                color = "darkgreen"
            else:
                color = "blue" # error
            self.circle.attrs["fill"] = color

    def hide_all(self):
        self.hidden = True
        # self.circle.attrs["fill"] = "white"
        self.circle.attrs["visibility"] = "hidden"
        self.title.attrs["visibility"] = "hidden"
    def unhide_all(self):
        self.hidden = False
        self.circle.attrs["visibility"] = "visible"
        self.title.attrs["visibility"] = "visible"