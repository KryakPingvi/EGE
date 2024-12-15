from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from sdamgia import SdamGIA

from spinners import SubjectSpinner, TopicSpinner
from widgets import ScrollableLabel, create_button, create_text_input
from loading_label import LoadingLabel
from image_processing import SvgWidget
from problem_handler import get_random_problem, check_answer, is_first_part_topic

class EgeApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Initialize spinners
        self.subject_spinner = SubjectSpinner(size_hint_y=None, height='48dp')
        self.topic_spinner = TopicSpinner(size_hint_y=None, height='48dp')
        self.topic_spinner.disabled = True
        
        # Bind spinner events
        self.subject_spinner.bind(text=self.on_subject_change)
        self.topic_spinner.bind(text=self.on_topic_select)
        
        # Create buttons
        self.get_problem_button = create_button(
            'Получить случайное задание',
            disabled=True,
            on_press=self.get_random_problem
        )
        
        # Create loading label
        self.loading_label = LoadingLabel(size_hint_y=None, height='48dp')
        
        # Create problem text widget
        self.problem_text = ScrollableLabel(
            text='',
            halign='left',
            valign='top',
            markup=True,
            size_hint_y=None,  
            height='200dp'     
        )
        
        # Create SVG widget
        self.svg_widget = SvgWidget()
        
        # Create answer input
        self.answer_input = create_text_input(
            hint_text='Введите ответ',
            disabled=True
        )
        
        # Create check answer button
        self.check_answer_button = create_button(
            'Проверить ответ',
            disabled=True,
            on_press=self.check_answer
        )
        
        # Create result label
        self.result_label = ScrollableLabel(
            text='',
            markup=True,
            size_hint_y=None,
            height='48dp'
        )
        
        # Initialize other components
        self.sdamgia = SdamGIA()
        self.subject_catalogs = {}
        self.current_problem = None
