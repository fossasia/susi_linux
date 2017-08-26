import math
import cairo
import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib


class Animator(Gtk.DrawingArea):
    def __init__(self, **properties):
        super().__init__(**properties)
        self.set_size_request(200, 80)
        self.connect("draw", self.do_drawing)
        GLib.timeout_add(1, self.tick)

    def tick(self):
        self.queue_draw()
        return True

    def do_drawing(self, widget, cr):
        self.draw(cr, self.get_allocated_width(), self.get_allocated_height())

    def draw(self, cr, width, height):
        pass


class ListeningAnimator(Animator):
    def __init__(self, window, **properties):
        super().__init__(**properties)
        self.window = window
        self.tc = 0

    def draw(self, ctx: cairo.Context, w, h):

        self.tc += 0.07
        self.tc %= 2 * math.pi

        sin_rot = math.sin(self.tc)
        cos_rot = math.cos(self.tc)

        for i in range(-4, 5):
            ctx.set_source_rgb(0.2, 0.5, 1)
            ctx.set_line_width(6)
            ctx.set_line_cap(cairo.LINE_CAP_ROUND)
            if i % 2 == 0:
                ctx.move_to(w / 2 + i * 10, h / 2 + 3 - 8 * sin_rot)
                ctx.line_to(w / 2 + i * 10, h / 2 - 3 + 8 * sin_rot)
            else:
                ctx.set_source_rgb(0.2, 0.7, 1)
                ctx.move_to(w / 2 + i * 10, h / 2 + 3 - 8 * cos_rot)
                ctx.line_to(w / 2 + i * 10, h / 2 - 3 + 8 * cos_rot)
            ctx.stroke()


class ThinkingAnimator(Animator):
    def __init__(self, window, **properties):
        super().__init__(**properties)
        self.window = window
        self.rot = 0
        self.x, self.y = 0, 0
        self.rad = 20

    def draw(self, ctx: cairo.Context, w, h):
        self.x, self.y = w / 2, h / 2
        self.rot += 0.1
        self.rot %= 2 * math.pi

        for i in range(-2, 2):
            ctx.set_source_rgb(0.2, 0.7, 1)
            ctx.arc(self.x + i * 20, self.y, 8 * math.cos(self.rot - i/2), 0, 360)
            ctx.fill()
