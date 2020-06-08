# gui.py
from browser import document, svg, timer
from core import Resource,Converter
import loader
# import svg, panel, document from main

class Node:
    radius = 50
    color = "red"
    ID = 0

    def __init__(self, converter, pos):
        self.converter = converter
        self.position = pos
        self.ID_ = Node.ID+1
        Node.ID += 1
        self.circle = svg.circle(cx=0, cy=0, r=self.radius,stroke="black",stroke_width="2",fill=self.color)
        self.title = svg.text(self.converter.name, x=0, y=0, z=10, font_size=15,text_anchor="middle")
        x,y = self.position

    def draw(self):
        # Update
        cx, cy = self.position
        cx += 1
        self.circle.attrs["cx"] = cx
        self.circle.attrs["cy"] = cy
        self.title.attrs["x"] = cx
        self.title.attrs["y"] = cy
        self.position = cx, cy

# Init nodes
nodes = []
panel = document['panel']
X,Y=200,200
for conv in Converter.converters.values():
    node = Node(conv,(X,Y))
    nodes.append(node)
    X += 200

# Init connections
connections = []
for resource in Resource.resources.values():
    for node in nodes:
        for out_recipe in  node.converter.out_recipes:
            for node_other in nodes:
                for in_recipe in node_other.converter.in_recipes:
                    if out_recipe.resource == in_recipe.resource:
                        line = svg.line(x1=0,y1=0,x2=0,y2=0, stroke="black",stroke_width="2")
                        panel <= line
                        connections.append((node, node_other, line))

# Init node graphic
for node in nodes:
    panel <= node.circle
    panel <= node.title

def draw_connections():
    for node_out, node_in, line in connections:
        x1, y1 = node_out.position
        x2, y2 = node_in.position
        line.attrs["x1"] = x1
        line.attrs["y1"] = y1
        line.attrs["x2"] = x2
        line.attrs["y2"] = y2


def draw_nodes():
    draw_connections()
    for node in nodes:
        node.draw()


def drawing():
    draw_nodes()
    draw_connections()

# Init GUI
drawing()