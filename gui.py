# gui.py
from browser import document, svg, timer
from core import Resource,Converter
import loader
# import svg, panel, document from main

class Node:
    radius = 20
    color = "red"

    def __init__(self, converter, pos):
        self.converter = converter
        self.position = pos

    def draw(self, panel):
        x,y = self.position
        circle = svg.circle(cx=x, cy=y+self.radius+10, r=self.radius,stroke="black",stroke_width="2",fill=self.color)
        title = svg.text(self.converter.name, x=x, y=y, font_size=15,text_anchor="middle")
        panel <= circle
        panel <= title

nodes = []
X,Y=200,200
for conv in Converter.converters.values():
    node = Node(conv,(X,Y))
    nodes.append(node)
    X += 50

def draw_nodes():
    panel = document['panel']
    for node in nodes:
        node.draw(panel)
