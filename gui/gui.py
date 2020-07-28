# gui.py
from typing import List

from browser import document, svg, html, timer
from core.resource import *
from gui.node import Node
import gui.hud as hud
from gui.info_panel import InfoPanel
from gui.menu_panel import *
from gui.navigation import Navigation
from gui.connections import *
from core.app_version import version_label
from core.save_load_game import SaveLoadGame


# Init nodes
nodes: List[Node] = []

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
document['content'] <= html.DIV(version_label, id="version")

### Save/load game
save_load_game = SaveLoadGame(converters=Converter.converters, resources=Resource.resources)

### MENU BAR ###
# How to button
howTo = HowToMenuItem(document["menu_btns"])
# Reset button
document["reset"].bind("click", lambda e: save_load_game.reset_game())
# Save button
document["save"].bind("click", lambda e: save_load_game.save_game())
save_load_game.load_game() # Try to load local file

