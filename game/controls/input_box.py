import pygame
from game.game_objects import Clickable


class InputBox(Clickable):
    def __init__(self, text='', send_to_callable=None, always_send=False, send_call_result_to=None, **kwargs):
        super().__init__(**kwargs)
        self.keyboard = self.game.keyboard
        self.send_to_callable = send_to_callable
        self.send_call_result_to = send_call_result_to
        self.always_send = always_send
        self.text = text
        self.font = pygame.font.Font(None, 32)
        self.image = self.font.render(self.text, True, self.color)
        self.game.sprite_group.add(self)
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
            self.send()
            self.text = ''
        elif event.key == pygame.K_BACKSPACE:
            self.text = self.text[:-1]
            if self.always_send:
                self.send()
        else:
            self.text += event.unicode
            if self.always_send:
                self.send()
        # Re-render the text.
        self.image = self.font.render(self.text, True, self.color)

        # Resize the box if the text is too long.
        width = max(200, self.image.get_width()+10)
        self.rect.w = width
        self.adapt_to_new_size()

    def kill(self) -> None:
        self.keyboard.disconnect()
        return super().kill()

    def send(self):
        """
        Sends text to mapped Callable. Result of called function
        can be returned to send_call_result_to Callable.
        If always_send flag is set - text will be send each
        time keyboard is pressed.
        """
        if self.send_to_callable:
            result = self.send_to_callable(self.text)
            if self.send_call_result_to:
                self.send_call_result_to(result)

        else:
            print(self.text)

    def update(self) -> None:
        super().update()
        self.draw_text(self.text)
