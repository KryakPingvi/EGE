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
    
    def build(self):
        Window.clearcolor = (1, 1, 1, 1)
        root = BoxLayout(orientation='vertical', padding=[20, 10], spacing=15)
        
        # Add top controls
        top_controls = BoxLayout(size_hint_y=None, height='48dp', spacing=10)
        top_controls.add_widget(self.subject_spinner)
        top_controls.add_widget(self.topic_spinner)
        root.add_widget(top_controls)
        # Add get problem button
        self.get_problem_button.background_color = (1, 1, 1, 1)
        self.get_problem_button.color = (0, 0, 0, 1)
        root.add_widget(self.get_problem_button)
        
        # Add center scroll view
        center_scroll = ScrollView()
        center_layout = BoxLayout(orientation='vertical', size_hint_y=None, spacing=5)
        center_layout.bind(minimum_height=center_layout.setter('height'))
        
        self.problem_text.background_color = (1, 1, 1, 1)
        self.problem_text.color = (0, 0, 0, 1)
        center_layout.add_widget(self.problem_text)
        center_layout.add_widget(self.svg_widget)
        
        center_scroll.add_widget(center_layout)
        root.add_widget(center_scroll)
        
        # Add bottom controls
        bottom_controls = BoxLayout(orientation='vertical', size_hint_y=None, height='150dp', spacing=10)
        bottom_controls.add_widget(self.answer_input)
        self.answer_input.background_color = (1, 1, 1, 1)
        self.answer_input.foreground_color = (0, 0, 0, 1)
        bottom_controls.add_widget(self.check_answer_button)
        self.check_answer_button.background_color = (0.9, 0.9, 0.9, 1)
        self.check_answer_button.color = (0, 0, 0, 1)
        bottom_controls.add_widget(self.result_label)
        self.result_label.background_color = (1, 1, 1, 1)
        self.result_label.color = (0, 0, 0, 1)
        root.add_widget(bottom_controls)
        
        return root
    def on_subject_change(self, spinner, text):
        self.problem_text.text = ''
        self.result_label.text = ''
        
        if text not in ['Выберите предмет', 'Загрузка предметов...', 'Ошибка загрузки']:
            self.topic_spinner.disabled = False
            self.topic_spinner.text = 'Загрузка тем...'
            self.topic_spinner.values = []
            
            subject_code = self.subject_spinner.subject_codes[text]
            
            if subject_code not in self.subject_catalogs:
                self.subject_catalogs[subject_code] = self.sdamgia.get_catalog(subject_code)
            
            catalog = self.subject_catalogs[subject_code]
            
            categories = set()
            self.topic_spinner.category_ids = {}
            
            for topic in catalog:
                if isinstance(topic, dict) and 'topic_name' in topic:
                    topic_name = topic['topic_name']
                    
                    if is_first_part_topic(topic_name, subject_code):
                        if topic_name not in categories:
                            categories.add(topic_name)
                            self.topic_spinner.category_ids[topic_name] = topic.get('topic_id')
            
            self.topic_spinner.values = sorted(categories)
            self.topic_spinner.text = 'Выберите тему'
            
        else:
            self.topic_spinner.disabled = True
            self.topic_spinner.text = 'Выберите тему'
    def on_topic_select(self, spinner, text):
        self.problem_text.text = ''
        self.result_label.text = ''
        
        if text not in ['Выберите тему', 'Загрузка тем...', 'Ошибка загрузки тем']:
            topic_id = self.topic_spinner.category_ids.get(text)
            if topic_id:
                self.get_problem_button.disabled = False
                self.current_topic_id = topic_id
                self.current_topic_name = text
    def get_random_problem(self, instance=None):
        subject_code = self.subject_spinner.subject_codes[self.subject_spinner.text]
        self.current_problem = get_random_problem(
            self.sdamgia,
            subject_code,
            self.current_topic_name,
            self.problem_text,
            self.svg_widget,
            self.loading_label,
            self.answer_input,
            self.check_answer_button,
            self.result_label
        )
    def check_answer(self, instance):
        check_answer(
            self.current_problem,
            self.answer_input.text,
            self.result_label
        )
