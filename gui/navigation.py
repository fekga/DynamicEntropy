# navigation.py
from browser import document

class Navigation:
    def __init__(self, graphic_item, event_item = None):
        self.graphic_item = graphic_item
        if event_item is None:
            event_item = graphic_item
        self.event_item = event_item
        self.init_translate = 0,0
        self.scale = 1
        self.started = False
        # Binds
        self.event_item.bind('mousedown', lambda ev: self.move_from(ev))
        self.event_item.bind('mouseup', lambda ev: self.move_to(ev))
        self.event_item.bind('mousewheel', lambda ev: self.zoom(ev))

    def update_graphic(self, translate=None, scale=None):
        if translate is None:
            translate = self.init_translate
        if scale is None:
            scale = self.scale
        posX, posY = translate
        self.graphic_item.attrs["transform"] = f'translate({posX},{posY}),scale({scale})'

    def move_from(self, event):
        self.started = True
        self.start_pos = event.pageX, event.pageY
        self.event_item.bind('mousemove', lambda ev: self.moving(ev))


    def calc_current_pos(self, init_pos, start_pos, current_pos):
        ix, iy = init_pos
        cx, cy = current_pos
        sx, sy = start_pos
        deltaX = cx - sx
        deltaY = cy - sy
        posX = deltaX + ix
        posY = deltaY + iy
        # Constraints
        # TODO
        return posX, posY

    def moving(self, event):
        if not self.started:
            return
        cx = event.pageX
        cy = event.pageY
        self.update_graphic(translate=self.calc_current_pos(self.init_translate, self.start_pos, (cx, cy)))

    def move_to(self,event):
        if not self.started:
            return
        self.event_item.unbind('mousemove')
        cx = event.pageX
        cy = event.pageY
        self.init_translate = self.calc_current_pos(self.init_translate, self.start_pos, (cx, cy))
        self.update_graphic()
        self.started = False

    def zoom(self,event):
        delta = 0.9
        if event.wheelDelta < 0:
            self.scale *= delta
        else:
            self.scale /= delta
        self.update_graphic()
        event.stopPropagation()
        event.preventDefault()