# hud.py
from browser import document, svg, html
from functools import partial


class Hud:
    # Add g to the hud
    panel = svg.g(id='hud')
    document['panel'] <= panel
    rect = panel.parent.getBoundingClientRect()
    width,height = rect.width,rect.height
    hud_info = svg.text("", x=0, y=0, font_size=20,text_anchor="start")
    hud_bounding = svg.rect(x=0, y=0, width=100, height=100, stroke="black", fill="white")
    upgrades = []
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
        Hud.upgrades.clear()
        Hud.panel.attrs["visibility"] = "hidden"

    def hud_size():
        brect = Hud.hud_info.getBBox()
        return int(brect.width), int(brect.height)

    def hud_upgrade_buy(event, upgrade, node):
        if upgrade.buy():
            Hud.show_info(node)
        event.stopPropagation()

    def create_converter_elements(title,elements,offset=0):
        if elements:
            Hud.hud_info <= Hud.create_tspan(title,x=Hud.border+10+offset,dy=25)
            for element in elements:
                text = str(element)
                Hud.hud_info <= Hud.create_tspan(text,x=Hud.border+20+offset)

    def create_hud_content(node):
        # As 0,0 is the start position
        Hud.hud_bounding = svg.rect(x=0, y=0, width=100, height=100, stroke="black", fill="white")
        Hud.hud_info = svg.text("", x=0, y=0, font_size=20,text_anchor="start")
        Hud.panel <= Hud.hud_bounding
        Hud.panel <= Hud.hud_info

        name = node.converter.name
        if node.converter.unstoppable:
            name += " - [Unstoppable]"
        Hud.hud_info <= Hud.create_tspan(name,x=Hud.border,dy=Hud.border)
        Hud.create_converter_elements('Needs:',node.converter.needs)
        Hud.create_converter_elements('Produces:',node.converter.makes)
        # Hud.create_converter_elements('Upgrades:',node.converter.upgrades)

        hasUpgrade = False
        for u in node.converter.upgrades:
            if not u.bought:
                hasUpgrade = True
        if hasUpgrade:
            Hud.hud_info <= Hud.create_tspan('Upgrades:',x=Hud.border+10,dy=25)
            for upgrade in node.converter.upgrades:
                if upgrade.bought:
                    continue
                Hud.hud_info <= Hud.create_tspan(upgrade.name,x=Hud.border+30)

                button = svg.rect(x=0, y=0, width=Hud.upgrade_button_size, height=Hud.upgrade_button_size, stroke="black", fill="white")
                hsx, hsy = Hud.hud_size()
                button.attrs['x'] = int(Hud.border + 15)
                button.attrs['y'] = int(hsy - Hud.upgrade_button_size)
                func = lambda ev, upgrade=upgrade: Hud.hud_upgrade_buy(ev,upgrade,node)
                button.bind("click", func)

                buy_icon_appearance_func = lambda upgrade=upgrade, button=button: Hud.upgrade_button_appearance(upgrade, button)
                Hud.upgrade_button_appearance(upgrade, button) # init
                Hud.upgrades.append(buy_icon_appearance_func) # refresh icon updater

                Hud.panel <= button

                if upgrade.all_requirements_bought():
                    Hud.create_converter_elements('Costs:',upgrade.costs,offset=30)
                    Hud.create_converter_elements('Changes:',upgrade.changes,offset=30)
                else:
                    Hud.create_converter_elements('Requires:',upgrade.requires,offset=30)

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

    def upgrade_button_appearance(upgrade, button):
        color = "red"
        if upgrade.isBuyable():
            color = "LawnGreen"
        button.style["stroke"] = "black"
        button.style["fill"] = color

    def refresh_buy_icon():
        for fn in Hud.upgrades:
            fn()