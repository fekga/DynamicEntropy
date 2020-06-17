# hud.py
from browser import document, svg, html

def create_tspan(text,x,dy='1em'):
    tspan = svg.tspan(text,x=x,dy=dy)
    Hud.tspans.append(tspan)
    return tspan

# Upgrade button
def get_upgrade_btn(idx):
    r = svg.rect(x=0, y=0, width=10, height=10, id="upgrade_rect")
    r.attrs["class"] = idx
    return r

# Add g to the hud
document['panel'] <= svg.g(id='hud')
class Hud:
    panel = document['hud']
    rect = panel.parent.getBoundingClientRect()
    width,height = rect.width,rect.height
    hud_info = svg.text("", x=0, y=0, font_size=20,text_anchor="start")
    hud_bounding = svg.rect(x=0, y=0, width=100, height=100, stroke="black", fill="white")
    # add to panel manually later
    active = False
    tspans = []
    upgrade_btn_created = False

    def hud_clicked(event):
        event.stopPropagation()

    def clear_hud():
        Hud.hud_info.text = ''
        if Hud.upgrade_btn_created:
            while "upgrade_rect" in document:
                del document["upgrade_rect"]
        Hud.upgrade_btn_created = False
        Hud.tspans.clear()
        Hud.panel.attrs["visibility"] = "hidden"

    def hud_size():
        brect = Hud.hud_info.getBBox()
        return brect.width, brect.height

    # HACK: Upgrade can not send, idx travel through html element
    def hud_upgrade_buy(event, idx, node):
        upgrade = node.converter.upgrades[int(idx)]
        if upgrade.buy():
            Hud.show_info(node)
        event.stopPropagation()

    def create_hud_content(node):
        # As 0,0 is the start position
        Hud.hud_info.text = node.converter.name
        if node.converter.unstoppable:
            Hud.hud_info.text += " - [UNSTOPPABLE]"
        if node.converter.needs:
            Hud.hud_info <= create_tspan('Needs:',x=10,dy=25)
            for in_recipe in node.converter.needs:
                text = repr(in_recipe)
                Hud.hud_info <= create_tspan(text,x=20)
        if node.converter.makes:
            Hud.hud_info <= create_tspan('Produces:',x=10,dy=25)
            for out_recipe in node.converter.makes:
                text = repr(out_recipe)
                Hud.hud_info <= create_tspan(text,x=20)
        if node.converter.upgrades:
            Hud.hud_info <= create_tspan('Upgrades:', x=10, dy=25)
            for idx, upgrade in enumerate(node.converter.upgrades):
                if upgrade.bought:
                    continue
                text = repr(upgrade)
                tspan = create_tspan(text,x=20)
                Hud.hud_info <= tspan
                btn_instance = get_upgrade_btn(idx)
                btn_instance.attrs["nodeID"] = node.converter.name
                hsx, hsy = Hud.hud_size()
                btn_instance.attrs['x'] = hsx
                btn_instance.attrs['y'] = hsy - 25/2
                btn_instance.bind("click", lambda ev : Hud.hud_upgrade_buy(ev, ev.target.attrs["class"], node))
                Hud.panel <= btn_instance
                Hud.upgrade_btn_created = True

    def calc_container_width(name, spans):
        container_width = Hud.string2width(name)
        for sp in spans:
            container_width = max(container_width, Hud.tspan_width(sp))
        return container_width

    def show_info(node):
        Hud.clear_hud() # clear
        Hud.create_hud_content(node)
        # Create bounding rect
        hsx, hsy = Hud.hud_size()
        Hud.hud_bounding.attrs["width"] = hsx + 20 # plus upgrade icon
        Hud.hud_bounding.attrs["height"] = hsy
        # Set text start
        Hud.hud_info.attrs["y"] = 20
        # Translate all element
        tx = node.position[0] + node.radius + 5
        ty = node.position[1] - node.radius
        Hud.panel.attrs["transform"] = f'translate({tx},{ty})'
        # Visibility
        Hud.panel.attrs["visibility"] = "visible"

