import pygame
from game.clickable import Clickable


class InputBox(Clickable):

    def __init__(self, text='', **kwargs):
        super().__init__(**kwargs)
        self.keyboard = self.game.keyboard
        self.text = text
        self.font = pygame.font.Font(None, 32)
        self.image = self.font.render(self.text, True, self.color)
        self.adapt_to_new_size()

    def left_upclick(self, **kwargs):
        """
        When clicked - connects/disconnects to keyboard.
        """
        if self.selected:
            self.keyboard.disconnect()
            self.selected = False
        else:
            self.selected = True
            self.keyboard.connect(self)

    def keyboard_input(self, event):
        """
        Gets key from event then:
        adds it to text (if it is text)
        or deletes (if it was backspace)
        or sends it (if it was enter).
        """
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
