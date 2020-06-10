# gui.py
from browser import document, svg, timer
from core import Resource,Converter
import loader
# import svg, panel, document from main

class Node:
    radius = 20
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
        # cx += 1
        self.circle.attrs["cx"] = cx
        self.circle.attrs["cy"] = cy
        self.title.attrs["x"] = cx
        self.title.attrs["y"] = cy
        self.position = cx, cy

# Init nodes
nodes = []
panel = document['panel']
X,Y=20,20
for conv in Converter.converters.values():
    node = Node(conv,(X,Y))
    nodes.append(node)
    X += 100
    Y = (Y*1.25+270)%600

# Init connections
connections = []
for resource in Resource.resources.values():
    for node in nodes:
        for out_recipe in  node.converter.out_recipes:
            for node_other in nodes:
                for in_recipe in node_other.converter.in_recipes:
                    if out_recipe.resource == in_recipe.resource:
                        d="M 100 350 c 100 -200 200 500 300 0"
                        line = svg.path(d=d)
                        panel <= line
                        connections.append((node, node_other, line))

# Init node graphic
for node in nodes:
    panel <= node.circle
    panel <= node.title

# Init resource texts
resources=[]
X,Y = 800,100
for res in Resource.resources.values():
    text = svg.text(str(res), x=X, y=Y, font_size=20,text_anchor="middle")
    panel <= text
    resources.append((res,text))
    Y += 50

def draw_connections():
    for node_out, node_in, line in connections:
        x1, y1 = map(int,node_out.position)
        x2, y2 = map(int,node_in.position)

        mx1,my1 = int((x1+x2)/2),int(y1)
        mx2,my2 = int((x1+x2)/2),int(y2)
        d = f'M {x1} {y1} C {mx1} {my1} {mx2} {my2} {x2} {y2}'

        line.attrs["d"] = d


def draw_nodes():
    for node in nodes:
        node.draw()

def draw_resources():
    for res,text in resources:
        text.text = res


def drawing():
    draw_nodes()
    draw_connections()
    draw_resources()

# Init GUI
drawing()