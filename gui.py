# gui.py
from browser import document, svg, timer
from core import Resource,Converter,ConverterState
# import loader
# import svg, panel, document from main

class Node:
    radius = 20

    def __init__(self, converter, pos):
        self.converter = converter
        self.position = pos
        self.circle = svg.circle(cx=0, cy=0, r=self.radius,stroke="black",stroke_width="2",fill="green")
        self.circle.attrs["id"] = self.converter.name
        self.title = svg.text(self.converter.name, x=0, y=-self.radius, z=10, font_size=15,text_anchor="middle")
        x,y = self.position
        self.circle.bind("click", self.clicked)
        self.circle.bind("contextmenu", self.right_clicked)
        self.connections = []

    def clicked(self, event):
        print(self.converter.name + " clicked")

    def right_clicked(self, event):
        if self.converter.state == ConverterState.STOPPED:
            self.converter.state = ConverterState.OK
        else:
            self.converter.state = ConverterState.STOPPED

    def draw(self):
        # Update
        cx, cy = self.position
        # cx += 1
        self.circle.attrs["cx"] = cx
        self.circle.attrs["cy"] = cy
        self.title.attrs["x"] = cx
        self.title.attrs["y"] = cy
        self.position = cx, cy
        if self.converter.state == ConverterState.OK:
            color = "green"
        elif self.converter.state == ConverterState.STOPPED:
            color = "gray"
        elif self.converter.state == ConverterState.NO_INPUT:
            color = "yellow"
        elif self.converter.state == ConverterState.MAX_OUTPUT:
            color = "red"
        else:
            color = "blue" # error
        self.circle.attrs["fill"] = color

# Init nodes
nodes = []
panel = document['panel']
sX,sY=100,100
deltaY = 0
deltaX = 100
maxCol = 5
actCol = 0
X = sX
Y = sY
for conv in Converter.converters.values():
    node = Node(conv,(X,Y))
    nodes.append(node)
    X += deltaX
    actCol += 1
    Y += 20 # hack
    if actCol == maxCol:
        X = sX
        Y += deltaY
        actCol = 0


# Init connections
for node_out in nodes:
    for out_recipe in  node_out.converter.out_recipes:
        for node_in in nodes:
            for in_recipe in node_in.converter.in_recipes:
                if out_recipe.resource == in_recipe.resource:
                    d="M 100 350 c 100 -200 200 500 300 0"
                    line = svg.path(d=d)
                    panel <= line
                    node_out.connections.append((line, node_in))

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
    for node_out in nodes:
        for connect_out in node_out.connections:
            line, node_in = connect_out
            x1, y1 = map(int,node_out.position)
            x2, y2 = map(int,node_in.position)

            mx1,my1 = int((x1+x2)/2),int(y1)
            mx2,my2 = int((x1+x2)/2),int(y2)
            d = f'M {x1} {y1} C {mx1} {my1} {mx2} {my2} {x2} {y2}'

            line.attrs["d"] = d
            if node_out.converter.state == ConverterState.OK:
                line.attrs["visibility"] = "visible"
            else:
                line.attrs["visibility"] = "hidden"


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


