import math
import cairo
import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib  # nopep8


class Animator(Gtk.DrawingArea):
    def __init__(self, **properties):
        super().__init__(**properties)
        self.set_size_request(200, 80)
        self.connect("draw", self.do_drawing)
        GLib.timeout_add(50, self.tick)

    def tick(self):
        self.queue_draw()
        return True

    def do_drawing(self, widget, cr):
        self.draw(cr, self.get_allocated_width(), self.get_allocated_height())

    def draw(self, ctx, width, height):
        pass


class ListeningAnimator(Animator):
    def __init__(self, window, **properties):
        super().__init__(**properties)
        self.window = window
        self.tc = 0

    def draw(self, ctx, width, height):

        self.tc += 0.2
        self.tc %= 2 * math.pi

        for i in range(-4, 5):
            ctx.set_source_rgb(0.2, 0.5, 1)
            ctx.set_line_width(6)
            ctx.set_line_cap(cairo.LINE_CAP_ROUND)
            if i % 2 == 0:
                ctx.move_to(width / 2 + i * 10, height / 2 + 3 - 8 * math.sin(self.tc + i))
                ctx.line_to(width / 2 + i * 10, height / 2 - 3 + 8 * math.sin(self.tc + i))
            else:
                ctx.set_source_rgb(0.2, 0.7, 1)
                ctx.move_to(width / 2 + i * 10, height / 2 + 3 - 8 * math.cos(self.tc - i))
                ctx.line_to(width / 2 + i * 10, height / 2 - 3 + 8 * math.cos(self.tc - i))
            ctx.stroke()


class ThinkingAnimator(Animator):
    def __init__(self, window, **properties):
        super().__init__(**properties)
        self.window = window
        self.rot = 0
        self.x, self.y = 0, 0
        self.rad = 20

    def draw(self, ctx, width, height):
        self.x, self.y = width / 2, height / 2
        self.rot += 0.2
        self.rot %= 2 * math.pi

        for i in range(-2, 2):
            ctx.set_source_rgb(0.2, 0.7, 1)
            ctx.arc(self.x + i * 20, self.y, 8 * math.cos(self.rot - i / 2), 0, 2 * math.pi)
            ctx.fill()
