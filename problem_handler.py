from constants import MATH_TOPICS_TO_TASKS, RUS_TOPICS_TO_TASKS
import random
from image_processing import download_image

def get_random_problem(sdamgia, subject_code, topic_name, problem_text_widget, svg_widget, loading_label, answer_input, check_answer_button, result_label):
    try:
        loading_label.start()
        problems = sdamgia.search(subject_code, topic_name)
        
        if not problems:
            problem_text_widget.text = "Не удалось найти задачи по выбранной теме"
            return None
            
        problem_id = random.choice(problems)
        problem = sdamgia.get_problem_by_id(subject_code, str(problem_id))
        
        if subject_code == 'rus':
            problem_text = problem.get('solution', {}).get('text', '')
        else:  
            problem_text = (
                problem.get('condition', {}).get('text', '') or 
                problem.get('solution', {}).get('text', '')
            )
        
        formatted_problem_text = f"Задача №{problem_id}\n\n{problem_text}"
        problem_text_widget.text = formatted_problem_text
        
        result_label.text = ''
        answer_input.text = ''
        answer_input.disabled = False
        check_answer_button.disabled = False
            
        solution_images = problem.get('solution', {}).get('images', [])
        if solution_images:
            svg_url = solution_images[0]  
            image_path = download_image(svg_url)
            if image_path:
                svg_widget.load_image(image_path)
                
        return problem
    
    except Exception as e:
        problem_text_widget.text = f"Ошибка при загрузке задачи: {str(e)}"
        print(f"Detailed error: {e}")
        return None
    finally:
        loading_label.stop()

def check_answer(current_problem, user_answer, result_label):
    if current_problem:
        user_answer = user_answer.strip()
        correct_answer = str(current_problem.get('answer', '')).strip()
        
        if user_answer.lower() == correct_answer.lower():
            result_label.text = '[color=00ff00]Правильно![/color]'
        else:
            result_label.text = f'[color=ff0000]Неправильно. Правильный ответ: {correct_answer}[/color]'
    else:
        result_label.text = '[color=ff0000]Сначала выберите задачу[/color]'

def is_first_part_topic(topic_name, subject):
    if subject == 'math':
        return any(pattern.lower() in topic_name.lower() for pattern in MATH_TOPICS_TO_TASKS)
    elif subject == 'rus':
        return any(pattern.lower() in topic_name.lower() for pattern in RUS_TOPICS_TO_TASKS)
    return False
