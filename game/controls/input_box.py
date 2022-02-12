import pygame
from game.clickable import Clickable


COLOR_INACTIVE = pygame.Color('lightskyblue3')
COLOR_ACTIVE = pygame.Color('dodgerblue2')


class InputBox(Clickable):

    def __init__(self, text='', **kwargs):
        super().__init__(**kwargs)
        self.text = text
        self.font = pygame.font.Font(None, 32)
        self.image = self.font.render(text, True, self.color)
        self.keyboard = self.game.keyboard
        self.adapt_to_new_size()

    def left_upclick(self, mouse_event: pygame.event.Event, **kwargs):
        """
        When clicked - connect to keyboard.
        """
        self.keyboard.connect(self)

    def keyboard_input(self, event):
        if event.key == pygame.K_RETURN:
            print(self.text)
            self.text = ''
        elif event.key == pygame.K_BACKSPACE:
            self.text = self.text[:-1]
        else:
            self.text += event.unicode
        # Re-render the text.
        self.image = self.font.render(self.text, True, self.color)

        # Resize the box if the text is too long.
        width = max(200, self.image.get_width()+10)
        self.rect.w = width
        self.adapt_to_new_size()

    def kill(self) -> None:
        self.keyboard.disconnect()
        return super().kill()

    def update(self) -> None:
        super().update()
        self.draw_text(self.text)
