# gui.py
from browser import document, svg, html, timer
from browser.local_storage import storage
from core.resource import Resource
from core.converter import Converter
from gui.node import Node
import gui.hud as hud
from gui.info_panel import InfoPanel
from gui.menu_panel import *
from gui.navigation import Navigation
from gui.connections import *


# Init nodes
nodes = []

sX, sY = 100,100
deltaY = 0
deltaX = 200
maxCol = 5
actCol = 0
X = sX
Y = sY
for conv in Converter.converters:
    node = Node(conv,(X,Y))
    nodes.append(node)
    X += deltaX
    actCol += 1
    Y += 40
    if actCol == maxCol:
        sX += 10
        X = sX
        Y += deltaY
        actCol = 0


### Init connections ###
# Init connection structures
refreshAllConnections(nodes)


# Drawings
def draw_connections():
    for node in nodes:
        for connection in node.connections:
            connection.drawConnection()


def draw_nodes():
    for node in nodes:
        node.try_unhide_node()
        node.draw()

def draw_resources():
    info_panel.draw()



def drawing():
    draw_nodes()
    draw_connections()
    draw_resources()
    update_menu_panel() # menu panel update (eg.: playtime)
    hud.Hud.refresh_buy_icon() # update the buy icon in the HUD


# Init resource texts
info_panel = InfoPanel(resources=Resource.resources, nodes=nodes)

# Init GUI
drawing()

# Init HUD
hud.Hud.clear_hud()
document["hud"].bind('click', hud.Hud.hud_clicked)
# HUD clear event
def panel_click(event):
    hud.Hud.active = False
    hud.Hud.clear_hud()
document["play_area"].bind('click',panel_click)

# Create navigation
Navigation(svg_item=document['play_area'])

# Initialize drawing thread
timer.set_interval(drawing, 100)

# Version
from core.app_version import version_label
document['content'] <= html.DIV(version_label, id="version")

### MENU BAR ###
# How to button
howTo = HowToMenuItem(document["menu_btns"])
# Hard reset button connection
def hard_reset(event):
    for r in Resource.resources:
        r.amount = 0
    for c in Converter.converters:
        c.running = False
    storage['state'] = "" # full reset
document["reset"].bind("click", hard_reset)
# Save button
def save_state(event):
    fullString = version_label + "|"
    for resource in Resource.resources:
        fullString += f'{resource.name}:{resource.amount}|'
    storage['state'] = fullString
document["save"].bind("click", save_state)

def load_last_save(event):
    try:
        fullString = storage['state']
        print(fullString, fullString.startswith(version_label))
        resources = fullString.split("|")
        # Version check
        for idx, resource in enumerate(Resource.resources):
            name, amount = resources[idx+1].split(":") # +1 the version
            if resource.name != name:
                return
            else:
                resource.amount = float(amount)
    except:
        pass # local save not exists yet
load_last_save(None) # Try to load local file


