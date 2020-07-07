# connections.py
from browser import svg, document
from core.converter import Converter

class Connection:
    def __init__(self, node_make, node_need, resource):
        self.node_make = node_make
        self.node_need = node_need
        self.resource = resource
        self.lineCreation()
        self.manual_property_set = False

    def __del__(self):
        self.line.remove()
        self.defs.remove()

    def lineCreation(self):
        # SVG path calculation
        x1, y1 = map(int, self.node_make.position)
        x2, y2 = map(int, self.node_need.position)
        dx = abs(int((x1 - x2)))
        dy = abs(int((y1 - y2)))
        if dx > dy:
            mx1, my1 = int((x1 + x2) / 2), y1
            mx2, my2 = int((x1 + x2) / 2), y2
        else:
            mx1, my1 = x1, int((y1 + y2) / 2)
            mx2, my2 = x2, int((y1 + y2) / 2)
        if x1 == x2:
            mx1 += 1
            mx2 += 1
        if y1 == y2:
            my1 += 1
            my2 += 1
        d = f'M {x1} {y1} C {mx1} {my1} {mx2} {my2} {x2} {y2}'
        self.line = svg.path(d=d)

        # SVG lineGradient calculation
        lineGradID = f'lineGrad_{id(self)}'
        x1, y1 = self.node_make.position
        x2, y2 = self.node_need.position
        dx = abs(int((x1 - x2)))
        dy = abs(int((y1 - y2)))
        if dx > dy:
            x1_ = 0.4
            x2_ = 0.6
            y1_ = y2_ = 0
            inv = x2 < x1
        else:
            x1_ = x2_ = 0
            y1_ = 0.4
            y2_ = 0.6
            inv = y2 < y1
        self.defs = svg.defs()
        lg = svg.linearGradient(id=lineGradID, x1=x1_, y1=y1_, x2=x2_, y2=y2_)
        s1 = svg.stop(offset="0%")
        c1 = "rgb(0,255,0)"
        c2 = "rgb(255,0,0)"
        s1.attrs["style"] = f'stop-color:{c1 if not inv else c2};'
        lg <= s1
        s2 = svg.stop(offset="100%")
        s2.attrs["style"] = f'stop-color:{c2 if not inv else c1};'
        lg <= s2
        self.defs <= lg
        self.line.attrs['stroke'] = f'url(#{lineGradID})'
        document['connections'] <= self.defs
        document['connections'] <= self.line

    def drawConnection(self):
        if self.node_make.hidden or self.node_need.hidden:
            self.line.attrs["visibility"] = "hidden"
        else:
            self.line.attrs["visibility"] = "visible"
            if self.node_make.converter.state == Converter.OK:
                self.drawConnectionAsActive()
            else:
                self.drawConnectionAsInactive()

    def drawConnectionAsActive(self, forced=False):
        if not self.manual_property_set or forced:
            self.line.attrs["opacity"] = "1.0"

    def drawConnectionAsInactive(self, forced=False):
        if not self.manual_property_set or forced:
            self.line.attrs["opacity"] = "0.2"

    def createConnection(node_out, node_in):
        if node_out is not node_in:
            for make in node_out.converter.makes:
                for need in node_in.converter.needs:
                    if make.resource == need.resource:
                        return True, make.resource
        return False, None

def refreshAllConnections(nodes):
    for node in nodes:
        refreshConnections(node, nodes)

def refreshConnections(node, nodes):
    node.connections.clear()  # reset
    for node_need in nodes:
        create, resource = Connection.createConnection(node, node_need)
        if create:
            connection = Connection(node, node_need, resource)
            node.connections.append(connection)


    # for connect_out in node.connections:

