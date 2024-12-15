from kivy.uix.label import Label
from kivy.clock import Clock

class LoadingLabel(Label):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.dots = 0
        self.base_text = "Загрузка"
        self.schedule = None

    def start(self):
        self.opacity = 1
        if not self.schedule:
            self.schedule = Clock.schedule_interval(self.update_dots, 0.5)

    def stop(self):
        if self.schedule:
            self.schedule.cancel()
            self.schedule = None
        self.opacity = 0

    def update_dots(self, dt):
        self.dots = (self.dots + 1) % 4
        self.text = self.base_text + "." * self.dots
