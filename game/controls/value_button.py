from .button import Button
from .input_box import InputBox


class ValueButton(Button):
    """
    Button with input box inside.
    Button clicked - call method with default value.
    Box clicked - select and type new value.
    Always send saves new value to VauleButton's value.
    Button clicked - call method with new value.

    Button -creates-with-default->   InputBox
    Button <-typing-saves-kwargs- InputBox
    Button -LPM-> execute method with kwargs
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.value = None
        self.first_key = None
        self.input_box = self.create_input_box()

    def create_input_box(self):
        # get first key-value from kwargs to input box default value
        text = ''
        for k, v in self.method_kwargs.items():
            self.first_key = k
            text = str(v)
            break

        box = InputBox(text=text,
                       send_to_callable=self.save_new_value,
                       always_send=True,
                       game=self.game,
                       groups=[self.game.sprite_group],
                       min_width=10,
                       **self.locate_in_button())
        return box

    def locate_in_button(self):
        box_w = self.rect.width // 5
        box_h = self.rect.height // 3
        box_x = self.rect.x + (self.rect.width // 5) * 3
        box_y = self.rect.y + box_h
        return {'x': box_x, 'y': box_y, 'width': box_w, 'height': box_h}

    def save_new_value(self, text_value):
        self.method_kwargs[self.first_key] = text_value
        print(self.method_kwargs)

    def adapt_to_new_size(self):
        super().adapt_to_new_size()
        location = self.locate_in_button()
        self.input_box.rect.x = location['x']
        self.input_box.rect.y = location['y']
        self.input_box.rect.width = location['width']
        self.input_box.rect.height = location['height']
        self.input_box.adapt_to_new_size()

    def kill(self) -> None:
        self.input_box.kill()
        return super().kill()

    def left_upclick(self, **kwargs):
        """
        If clicked - trigger mapped instance method.
        """
        print(self.method_kwargs)
        self.method(**self.method_kwargs)
        if self.parent:
            self.parent.kill()
        self.kill()

    def update(self) -> None:
        super().update()
        self.draw_text(self.title, x=self.rect.x, y=self.rect.y)
        self.input_box.update()
