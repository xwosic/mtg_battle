import pygame


class Keyboard:
    def __init__(self, game) -> None:
        self.game = game
        self.output = None

    def connect(self, output):
        self.output = output

    def disconnect(self):
        self.output = None

    def keyboard_clicked(self, event: pygame.event.Event):
        print(event)
        if self.output:
            self.output.keyboard_input(event)
