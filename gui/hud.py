# hud.py
from browser import document, svg

def create_tspan(text,x,dy='1em'):
    tspan = svg.tspan(text,x=x,dy=dy)
    Hud.tspans.append(tspan)
    return tspan

class Hud:
    panel = document['panel']
    rect = panel.parent.getBoundingClientRect()
    width,height = rect.width,rect.height
    hud_info = svg.text("", x=0, y=0, font_size=20,text_anchor="start")
    hud_bounding = svg.rect(x=0, y=0, width=100, height=100, stroke="black", fill="white")
    # add to panel manually later
    active = False
    tspans = []

    def clear_hud():
        Hud.hud_info.text = ''
        for e in Hud.tspans:
            del e
        Hud.tspans.clear()
        Hud.hud_info.attrs["visibility"] = "hidden"
        Hud.hud_bounding.attrs["visibility"] = "hidden"

    def create_hud_content(node):
        # As 0,0 is the start position
        Hud.hud_info.text = node.converter.name
        if node.converter.needs:
            Hud.hud_info <= create_tspan('Needs:',x=10,dy=25)
            for in_recipe in node.converter.needs:
                text = f'{in_recipe.resource.name} [>={in_recipe.at_least}]: {in_recipe.amount:.2f}'
                Hud.hud_info <= create_tspan(text,x=20)
        if node.converter.makes:
            Hud.hud_info <= create_tspan('Produces:',x=10,dy=25)
            for out_recipe in node.converter.makes:
                text = f'{out_recipe.resource.name}: {out_recipe.amount:.2f}'
                Hud.hud_info <= create_tspan(text,x=20,)

    def calc_container_width(spans):
        container_width = 0
        for sp in spans:
            container_width = max(container_width, len(sp.text) * 11 + int(sp.attrs["x"]))
        return container_width

    def show_info(node):
        Hud.clear_hud() # clear
        Hud.create_hud_content(node)
        hud_bounding_width = Hud.calc_container_width(Hud.tspans)
        # Create bounding rect
        sx, sy = node.position
        Hud.hud_bounding.attrs["x"] = sx + node.radius + 5
        Hud.hud_bounding.attrs["y"] = sy - node.radius
        Hud.hud_bounding.attrs["width"] = hud_bounding_width
        Hud.hud_bounding.attrs["height"] = 25 + len(Hud.tspans)*25
        # Update text positions
        hud_info_sx = int(Hud.hud_bounding.attrs["x"])
        hud_info_sy = int(Hud.hud_bounding.attrs["y"]) + 20
        Hud.hud_info.attrs['x'] = hud_info_sx
        Hud.hud_info.attrs['y'] = hud_info_sy
        for e in Hud.tspans:
            e.attrs["x"] = int(e.attrs["x"]) + int(hud_info_sx)
        Hud.hud_info.attrs["visibility"] = "visible"
        Hud.hud_bounding.attrs["visibility"] = "visible"