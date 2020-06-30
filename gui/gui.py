# gui.py
from browser import document, svg, html, timer
from core.resource import Resource
from core.converter import Converter
from gui.node import Node
import gui.hud as hud
from gui.info_panel import InfoPanelItem
from gui.menu_panel import *
from gui.navigation import Navigation
from main import tick, tick_caller


# Init nodes
nodes = []
panel = document['panel']
sX, sY = 100,100
deltaY = 0
deltaX = 100
maxCol = 5
actCol = 0
X = sX
Y = sY
for conv in Converter.converters:
    node = Node(conv,(X,Y))
    nodes.append(node)
    X += deltaX
    actCol += 1
    Y += 20
    if actCol == maxCol:
        X = sX
        Y += deltaY
        actCol = 0


# Init connections
for node_out in nodes:
    for out_recipe in node_out.converter.makes:
        for node_in in nodes:
            for in_recipe in node_in.converter.needs:
                if out_recipe.resource == in_recipe.resource:
                    d="M 100 350 c 100 -200 200 500 300 0"
                    line = svg.path(d=d)
                    panel <= line
                    node_out.connections.append((line, node_in))

# Init node graphic
for node in nodes:
    panel <= node.circle
    panel <= node.title

# Drawings
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
            if node_out.converter.state == Converter.OK and not node_in.hidden:
                line.attrs["visibility"] = "visible"
            else:
                line.attrs["visibility"] = "hidden"


def draw_nodes():
    for node in nodes:
        node.try_unhide_node()
        node.draw()

def draw_resources():
    for info_panel_item in info_panel_items:
        info_panel_item.draw()


def drawing():
    draw_nodes()
    draw_connections()
    draw_resources()
    update_menu_panel() # menu panel update (eg.: playtime)

# Init resource texts
info_panel_items=[]
for idx, res in enumerate(Resource.resources):
    info_panel_items.append(InfoPanelItem(res, idx))

# Init GUI
drawing()

# Init HUD
hud.Hud.clear_hud()
panel <= svg.use(href="#hud")
document["hud"].bind('click',hud.Hud.hud_clicked)
# HUD clear event
def panel_click(event):
    hud.Hud.active = False
    hud.Hud.clear_hud()
document["play_area"].bind('click',panel_click)

# Create navigation
Navigation(graphic_item=document['panel'], event_item=document['play_area'])

# Initialize drawing thread
timer.set_interval(drawing, 100)

# Hard reset button connection
def hard_reset(event):
    for r in Resource.resources:
        r.amount = 0
    for c in Converter.converters:
        c.running = False
document["reset"].bind("click", hard_reset)

# Dev tick checkbox connection
dev_tick_check_box = document["dev_tick_checkbox"]
def dev_tick(event):
    global tick_caller
    timer.clear_interval(tick_caller)
    if event.target.checked:
        tick_caller = timer.set_interval(tick, 50)
    else:
        tick_caller = timer.set_interval(tick, 500)
dev_tick_check_box.bind("click", dev_tick)