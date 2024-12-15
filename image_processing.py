from kivy.uix.image import Image
import os
import logging
import tempfile
import requests
import hashlib

class SvgWidget(Image):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (0.4, None)  
        self.height = '200dp'  
        self.allow_stretch = True
        self.keep_ratio = True
        self.pos_hint = {'center_x': 0.5}  

    def load_image(self, image_path):
        try:
            print(f"Попытка загрузки изображения: {image_path}")
            
            if not os.path.exists(image_path):
                print(f"Файл не найден: {image_path}")
                return
            
            file_size = os.path.getsize(image_path)
            print(f"Размер файла: {file_size} байт")
            
            if file_size == 0:
                print("Файл пуст!")
                return
            
            if image_path.lower().endswith('.svg'):
                png_path = convert_svg_to_png(image_path)
                if png_path != image_path:  
                    self.source = png_path
                else:
                    print("Ошибка конвертации SVG в PNG")
                    return
            else:
                self.source = image_path
            
            self.reload()
            
            print(f"Источник установлен: {self.source}")
            print(f"Текстура: {self.texture}")
        
        except Exception as e:
            print(f"Ошибка загрузки изображения: {e}")
            import traceback
            traceback.print_exc()

    def clear(self):
        """Очистить виджет, сбросив источник изображения и текстуру."""
        self.source = ''
        self.texture = None
        self.canvas.ask_update()

    def reset(self):
        """Сбросить виджет, удалив изображение и обновив холст."""
        self.source = ''
        self.texture = None
        self.canvas.ask_update()

def convert_svg_to_png(svg_path, png_path=None, size=None):
    try:
        import cairosvg
        from PIL import Image
        import os

        if png_path is None:
            png_path = os.path.splitext(svg_path)[0] + '.png'

        cairosvg.svg2png(url=svg_path, write_to=png_path)

        with Image.open(png_path) as img:
            img.load()

        return png_path

    except Exception as e:
        logging.error(f"SVG to PNG conversion error: {e}")
        return svg_path

def download_image(url):
    try:
        cache_dir = os.path.join(tempfile.gettempdir(), 'ege_image_cache')
        os.makedirs(cache_dir, exist_ok=True)

        filename = hashlib.md5(url.encode()).hexdigest()
        file_extension = os.path.splitext(url)[-1].lower() or '.svg'
        local_filepath = os.path.join(cache_dir, f"{filename}{file_extension}")

        if os.path.exists(local_filepath):
            return local_filepath

        response = requests.get(url, timeout=10)
        response.raise_for_status()

        with open(local_filepath, 'wb') as f:
            f.write(response.content)

        if file_extension == '.svg':
            try:
                png_path = convert_svg_to_png(local_filepath)
                return png_path
            except Exception as svg_error:
                logging.error(f"SVG conversion error: {svg_error}")
                return local_filepath

        return local_filepath

    except Exception as e:
        logging.error(f"Image download error: {e}")
        return ''
