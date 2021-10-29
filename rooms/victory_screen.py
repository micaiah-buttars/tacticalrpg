import pygame
import pygame.locals as p

import room
import gui
import rooms
import state as s
import fonts as f
import colors as c
import display
import resources


class VictoryScreen(gui.LinearLayout):
    def __init__(self, **kwargs):
        super().__init__(allowed_events=[p.MOUSEBUTTONDOWN, p.KEYDOWN], clear_screen=False,
                         background=room.Background(color=c.TRANSPARENT, transparent=True), **kwargs)

    def begin(self):
        super().begin()
        print(_("%s wins") % s.winner.name)
        pygame.event.clear()
        transparent = room.Background(color=c.TRANSPARENT, transparent=True)
        self.victory = gui.Label(_("%s wins!") % s.winner.name, f.MAIN_MENU, txt_color=s.winner.color,
                                 background=transparent)
        self.thank_you = gui.Label(_("Thank you for playing!"), f.MAIN_MENU, txt_color=c.ICE,
                                   background=transparent)
        pygame.mixer.stop()
        resources.play_music('Fanfare.ogg', pos=1)
        self.add_children(self.victory, self.thank_you)

    def handle_keydown(self, event: pygame.event.Event):
        if event.key in [p.K_SPACE, p.K_RETURN]:
            self.done = True

    def handle_mousebuttondown(self, event: pygame.event.Event):
        if event.button == 1:
            self.done = True


if __name__ == '__main__':
    import logging
    import unit
    from gettext import gettext as _
    logging.basicConfig(level=0)
    display.initialize()
    img = resources.load_image('old-paper.jpg')
    display.window.blit(img, (0, 0))
    u = unit.RandomUnitFactory.make_unit()
    s.winner = unit.Team("Red mordace", (255, 0, 0), 0, [u], u, {})
    pygame.display.set_caption("Ice Emblem VictoryScreen Test")
    room.run(rooms.Fadeout(duration=1000, percent=0.7, next=VictoryScreen(next=rooms.Fadeout(duration=2000))))
