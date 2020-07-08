# navigation.py
from browser import document

class Navigation:
    def __init__(self, svg_item, max_size=2000):
        self.svg_item = svg_item
        self.viewBox = 0, 0, 1000, 1000
        self.max_size = max_size
        self.update_graphic()
        # Binds
        self.svg_item.bind('mousedown', lambda ev: self.move_from(ev))
        self.svg_item.bind('mouseup', lambda ev: self.move_to(ev))
        self.svg_item.bind('mousewheel', lambda ev: self.zoom(ev))

    def update_graphic(self):
        vx, vy, bx, by = self.viewBox
        self.svg_item.attrs["viewBox"] = f'{vx} {vy} {bx} {by}'

    def move_from(self, event):
        self.svg_item.bind('mousemove', lambda ev: self.moving(ev))

    def moving(self, event):
        dx = event.movementX
        dy = event.movementY
        vx, vy, bx, by = self.viewBox
        vx -= dx
        vy -= dy
        self.viewBox = vx, vy, bx, by
        self.update_graphic()

    def move_to(self, event):
        self.svg_item.unbind('mousemove')

    def zoom(self, event):
        delta = 0.9
        if event.wheelDelta < 0:
            delta = (1./delta)

        w = self.svg_item.getBoundingClientRect().width
        h = self.svg_item.getBoundingClientRect().height
        px = event.offsetX
        py = event.offsetY
        ratio_x = px / w
        ratio_y = py / h

        vx, vy, bx, by = self.viewBox
        delta_x = (bx-vx) * (1. - delta)
        delta_y = (by-vy) * (1. - delta)

        dvx = delta_x * ratio_x
        vx += dvx
        dvy = delta_y * ratio_y
        vy += dvy
        bx -= delta_x * (1. - ratio_x) + dvx
        by -= delta_y * (1. - ratio_y) + dvy

        if self.max_size > max([abs(vx - bx), abs(vy - by)]):
            self.viewBox = vx, vy, bx, by
            self.update_graphic()
        event.stopPropagation()
        event.preventDefault()