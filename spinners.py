from kivy.uix.spinner import Spinner, SpinnerOption
from constants import SUBJECT_NAMES

class CustomSpinnerOption(SpinnerOption):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(size=self._update_text_size)
        self.halign = 'center'
        self.valign = 'middle'
        self._update_text_size()

    def _update_text_size(self, *args):
        self.text_size = self.size

class SubjectSpinner(Spinner):
    def __init__(self, **kwargs):
        kwargs['option_cls'] = CustomSpinnerOption
        kwargs['sync_height'] = True
        super().__init__(**kwargs)
        self.text = 'Выберите предмет'
        self.values = list(SUBJECT_NAMES.values())
        self.subject_codes = {v: k for k, v in SUBJECT_NAMES.items()}
        self.text_size = (None, None)
        self.halign = 'center'
        self.valign = 'middle'
        self.bind(size=self._update_text_size)
    
    def _update_text_size(self, *args):
        self.text_size = self.size

class TopicSpinner(Spinner):
    def __init__(self, **kwargs):
        kwargs['option_cls'] = CustomSpinnerOption
        kwargs['sync_height'] = True
        super().__init__(**kwargs)
        self.text = 'Выберите тему'
        self.values = []
        self.category_ids = {}
        self.text_size = (None, None)
        self.halign = 'center'
        self.valign = 'middle'
        self.bind(size=self._update_text_size)
    
    def _update_text_size(self, *args):
        self.text_size = self.size
