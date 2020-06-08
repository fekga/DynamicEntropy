# gui.py

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
        circle = svg.circle(cx=x, cy=y, r=self.radius,stroke="black",stroke_width="2",fill=self.color)
        title = svg.text(converter.name, x=x, y=y, font_size=8,text_anchor="middle")
        panel <= circle
        panel <= title

nodes = []
x,y=0,0
for conv in Converter.converters.values():
    node = Node(conv,(x,y))
    nodes.append(node)
    x += 50

print(nodes)

def draw_nodes():
    panel = document['panel']
    # for node in nodes:
        # node.draw(panel)
