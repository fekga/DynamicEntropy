# hud.py
from browser import document, svg, html
from functools import partial

# Add g to the hud
class Hud:
    panel = svg.g(id='hud')
    document['panel'] <= panel
    rect = panel.parent.getBoundingClientRect()
    width,height = rect.width,rect.height
    hud_info = svg.text("", x=0, y=0, font_size=20,text_anchor="start")
    hud_bounding = svg.rect(x=0, y=0, width=100, height=100, stroke="black", fill="white")
    # add to panel manually later
    active = False
    border = 10
    upgrade_button_size = 10

    def create_tspan(text,x,dy='1em'):
        return svg.tspan(text,x=x,dy=dy)

    def hud_clicked(event):
        event.stopPropagation()

    def clear_hud():
        Hud.panel.clear()
        Hud.hud_info.clear()
        Hud.panel.attrs["visibility"] = "hidden"
        Hud.hud_info = svg.text("", x=0, y=0, font_size=20,text_anchor="start")
        Hud.hud_bounding = svg.rect(x=0, y=0, width=100, height=100, stroke="black", fill="white")
        Hud.panel <= Hud.hud_bounding
        Hud.panel <= Hud.hud_info

    def hud_size():
        brect = Hud.hud_info.getBBox()
        return brect.width, brect.height

    # HACK: Upgrade can not send, idx travel through html element
    def hud_upgrade_buy(event, upgrade, node):
        if upgrade.buy():
            Hud.show_info(node)
        event.stopPropagation()

    def create_converter_elements(title,elements):
        if elements:
            Hud.hud_info <= Hud.create_tspan(title,x=Hud.border+10,dy=25)
            for element in elements:
                text = repr(element)
                Hud.hud_info <= Hud.create_tspan(text,x=Hud.border+20)

    def create_hud_content(node):
        # As 0,0 is the start position
        name = node.converter.name
        if node.converter.unstoppable:
            name += " - [UNSTOPPABLE]"
        Hud.hud_info <= Hud.create_tspan(name,x=Hud.border,dy=Hud.border)
        Hud.create_converter_elements('Needs:',node.converter.needs)
        Hud.create_converter_elements('Produces:',node.converter.makes)
        # Hud.create_converter_elements('Upgrades:',node.converter.upgrades)
        
        if node.converter.upgrades:
            Hud.hud_info <= Hud.create_tspan('Upgrades:',x=Hud.border+10,dy=25)
            for idx, upgrade in enumerate(node.converter.upgrades):
                if upgrade.bought:
                    continue
                text = repr(upgrade)
                Hud.hud_info <= Hud.create_tspan(text,x=Hud.border+20)
                
                button = svg.rect(x=0, y=0, width=Hud.upgrade_button_size, height=Hud.upgrade_button_size)
                hsx, hsy = Hud.hud_size()
                button.attrs['x'] = Hud.border
                button.attrs['y'] = hsy - Hud.upgrade_button_size
                func = lambda ev, upgrade=upgrade: Hud.hud_upgrade_buy(ev,upgrade,node)
                button.bind("click", func)
                Hud.panel <= button

    def show_info(node):
        Hud.clear_hud() # clear
        Hud.create_hud_content(node)
        # Create bounding rect
        hsx, hsy = Hud.hud_size()
        Hud.hud_bounding.attrs["width"] = hsx + Hud.border*2
        Hud.hud_bounding.attrs["height"] = hsy + Hud.border*2
        # Set text start
        Hud.hud_info.attrs["y"] = 0
        # Translate all element
        tx = node.position[0] + node.radius + 5
        ty = node.position[1] - node.radius
        Hud.panel.attrs["transform"] = f'translate({tx},{ty})'
        # Visibility
        Hud.panel.attrs["visibility"] = "visible"

