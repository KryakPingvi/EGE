from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.metrics import dp

class ScrollableLabel(Label):
    def __init__(self, **kwargs):
        text = kwargs.pop('text', '')
        halign = kwargs.pop('halign', 'left')
        valign = kwargs.pop('valign', 'top')
        markup = kwargs.pop('markup', False)
        height = kwargs.pop('height', '200dp')
        
        super().__init__(
            text=text,
            halign=halign,
            valign=valign,
            markup=markup,
            size_hint_y=None,  
            height=height,     
        )
        
        self.bind(size=self._update_text_size)
        self._update_text_size()
        
        self.text_size = (None, None)  
        self.bind(width=lambda *x: setattr(self, 'text_size', (self.width, None)))
        self.bind(texture_size=lambda *x: setattr(self, 'height', max(self.texture_size[1], dp(200))))

    def _update_text_size(self, *args):
        self.text_size = (self.width, None)

def create_button(text, disabled=False, on_press=None):
    button = Button(
        text=text,
        size_hint_y=None,
        height='48dp',
        disabled=disabled,
        text_size=(None, None),
        halign='center',
        valign='middle'
    )
    if on_press:
        button.bind(on_press=on_press)
    button.bind(size=lambda *args: setattr(button, 'text_size', button.size))
    return button

def create_text_input(hint_text='', disabled=False):
    return TextInput(
        hint_text=hint_text,
        multiline=False,
        size_hint_y=None,
        height='48dp',
        disabled=disabled
    )
