from PIL import Image, ImageDraw, ImageFont
import math

class GraphicsTools:
    def __init__(self, filename):
        self.image = Image.open(filename)
        self.draw = ImageDraw.Draw(self.image)
        self.image_name = filename

    def add_grid(self):
        image_width, image_height = self.image.size
        self.create_columns(image_width, image_height)
        self.create_rows(image_width, image_height)
        self.save_image("grid_" + self.image_name)
        
    def create_columns(self, image_width, image_height):
        total_columns = math.floor(image_width/100)
        for i in range(1, total_columns + 1):
            if i % 2 == 0:
                text = str(i*100) + "px"
                self.insert_text(text , i*100 - 50, 50)
                color = 'red'
                line_width = 4
            else:
                color = 'blue'
                line_width = 2

            self.add_line((i*100, 0),(i*100, image_height), line_width=line_width, line_color=color)

    def create_rows(self, image_width, image_height):
        total_rows = math.floor(image_width/100)
        for i in range(1, total_rows + 1):
            if i % 2 == 0:
                text = str(i*100) + "px"
                self.insert_text(text, 50, i*100 - 50)
                color = 'red'
                line_width = 4
            else:
                color = 'blue'
                line_width = 2

            self.add_line((0, i*100),(image_width, i*100), line_width=line_width, line_color=color)

    def add_line(self, start_point, end_point, line_color='red', line_width=2):
        self.draw.line(start_point + end_point, fill=line_color, width=line_width)

    def insert_text(self, text, x, y, font_size=30, font_color='red'):
        font = ImageFont.truetype("cantarell.ttf", font_size)
        self.draw.text((x, y), text, fill=font_color, font=font)

    def insert_mouse_cursor(self, x, y):
        cursor_image = Image.open("assets/icons/mouse_cursor.png")
        cursor_width, cursor_height = cursor_image.size
        if x > self.image.width - cursor_width:
            # Mirror the image
            cursor_image = cursor_image.transpose(Image.FLIP_LEFT_RIGHT)
            x = x - cursor_width
            
        if y > self.image.height - cursor_height:
            # Mirror the image
            cursor_image = cursor_image.transpose(Image.FLIP_TOP_BOTTOM)
            y = y - cursor_height

        self.image.paste(cursor_image, (x, y), cursor_image)
        self.save_image("cursor_" + self.image_name)

    def save_image(self, filename):
        self.image.save(filename)

    def __delete_image(self, filename):
        os.remove(self.image_name)

    def delete_all_images(self):
        try:
            os.remove("grid_" + self.image_name)
            os.remove("cursor_" + self.image_name)
            os.remove(self.image_name)
        except:
            pass
