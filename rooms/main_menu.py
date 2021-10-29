import pygame
import pygame.locals as pl
import os
import gettext

import display
import gui
import resources
import fonts as f
import colors as c
from room import Layout, LayoutParams, Gravity, Background

from rooms.map_menu import MapMenu


class MainMenu(gui.LinearLayout):
    def __init__(self):
        super().__init__(allowed_events=[pl.MOUSEMOTION, pl.MOUSEBUTTONDOWN, pl.KEYDOWN],
                         background=Background(color=c.BLACK, image=resources.load_image('Ice Emblem.png')),
                         layout=Layout(width=LayoutParams.FILL_PARENT, height=LayoutParams.FILL_PARENT), spacing=50)
        self.click_to_start = gui.Label(_("Click to Start"), f.MAIN_MENU, padding=10,
                                        txt_color=c.ICE, layout=Layout(gravity=Gravity.BOTTOM), die_when_done=False)
        self.hmenu = gui.HorizontalMenu([(_("License"), self.show_license), (_("Settings"), self.settings_menu)],
                                        f.SMALL, die_when_done=False, layout=Layout(gravity=Gravity.BOTTOMRIGHT))
        self.add_children(self.click_to_start, self.hmenu)
        self.bind_keys((pl.K_RETURN, pl.K_SPACE), self.show_map_menu)
        self.bind_click((1,), self.show_map_menu, self.hmenu.rect, False)

    def show_map_menu(self, *_):
        self.next = MapMenu(self.background)
        self.done = True

    def show_license(self, *_):
        self.next = License()
        self.done = True
        self.next.next = self

    def settings_menu(self, *_):
        self.next = SettingsMenu()
        self.done = True
        self.next.next = self


class License(gui.Image):
    def __init__(self):
        super().__init__(resources.load_image('GNU GPL.jpg'), layout=Layout(gravity=Gravity.FILL),
                         allowed_events=[pl.MOUSEBUTTONDOWN, pl.KEYDOWN], die_when_done=True)


class SettingsMenu(gui.LinearLayout):

    def __init__(self):
        super().__init__(padding=30, layout=Layout(gravity=Gravity.FILL),
                         background=gui.NinePatch(resources.load_image('WindowBorder.png'), (70, 70)))
        self.back_btn = gui.Button(_("Go Back"), f.MAIN, callback=lambda *_: setattr(self, 'done', True),
                                   layout=Layout(gravity=Gravity.BOTTOMRIGHT))
        self.title = gui.Label(_("Settings"), f.MAIN)
        self.display_label = gui.Label(_("Display"), f.SMALL)

        # use a set comprehension to filter duplicates and too small resolutions
        # However sets are not guaranteed to be ordered in every python
        # implementation, so use sorted to switch back to an ordered list
        resolutions = {res for res in pygame.display.list_modes()
                       if res[0] >= display.min_resolution[0] and res[1] >= display.min_resolution[1]}
        resolutions = sorted(resolutions, reverse=True)

        def toggle_fullscreen(*_):
            display.set_resolution(resolutions[0])
            display.toggle_fullscreen()

        self.fullscreen_btn = gui.CheckBox(_("Toggle Fullscreen"), f.SMALLER, callback=toggle_fullscreen)

        def res_setter(res):
            return lambda *_: display.set_resolution(res)

        entries = [("{0[0]}x{0[1]}".format(res), res_setter(res)) for res in resolutions]
        self.resolutions_menu = gui.Menu(entries, f.SMALLER, die_when_done=False)



        self.add_children(self.back_btn, self.title, self.display_label, self.fullscreen_btn, self.resolutions_menu)

    def handle_keydown(self, event: pygame.event.Event):
        if event.key == pl.K_ESCAPE:
            self.done = True

    def handle_mousebuttondown(self, event: pygame.event.Event):
        if event.button == pl.BUTTON_RIGHT:
            self.done = True
