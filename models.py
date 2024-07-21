import datetime
import os
import random
import re
from urllib.parse import unquote_plus

from PIL import Image, ImageDraw, ImageFont
from fontTools.ttLib import TTFont


def parse_text_into_params(text):
    text = unquote_plus(text).strip()
    text = text[:-1] if text[-1] == ";" else text
    params = text.split(";")

    title = params.pop(0).strip() if params else "Default Title"
    subtitle = params.pop(0).strip() if params else "Default Subtitle"
    author = params.pop(0).strip() if params else "Default Author"
    image_code = params.pop(0).strip() if params else str(random.randrange(1, 41))
    theme = params.pop(0).strip() if params else str(random.randrange(0, 17))

    return title, subtitle, author, image_code, theme


def load_fonts(base_dir):
    font_paths = {
        'italic': os.path.join(base_dir, 'fonts', 'Garamond LightItalic.ttf'),
        'regular': os.path.join(base_dir, 'fonts', 'Garamond Light.ttf'),
        'helvetica': os.path.join(base_dir, 'fonts', 'HelveticaNeue-Medium.otf'),
        'helvetica_bold': os.path.join(base_dir, 'fonts', 'Helvetica Bold.ttf')
    }

    fonts = {
        'top': ImageFont.truetype(font_paths['italic'], 20),
        'subtitle': ImageFont.truetype(font_paths['italic'], 34),
        'author': ImageFont.truetype(font_paths['italic'], 24),
        'title': ImageFont.truetype(font_paths['regular'], 62),
        'orielly': ImageFont.truetype(font_paths['helvetica'], 28),
        'question_mark': ImageFont.truetype(font_paths['helvetica_bold'], 16)
    }
    return fonts, font_paths


def draw_top_text(draw, text, width, font):
    text = sanitize_unicode(text, font.path)
    text_width = draw.textlength(text, font)
    text_position_x = (width / 2) - (text_width / 2)

    draw.text((text_position_x, 10), text, fill='black', font=font)


def draw_title(draw, title, width, theme_color, font_paths):
    title_font, new_title = clamp_title_text(sanitize_unicode(title, font_paths['regular']), width - 80)
    if new_title is None:
        raise ValueError('Title too long')

    text_width, text_height = draw.multiline_textsize(new_title, title_font)
    draw.rectangle([(20, 400), (width - 20, 400 + text_height + 40)], fill=theme_color)
    draw.multiline_text((40, 420), new_title, fill='white', font=title_font)
    return text_height


def draw_subtitle(draw, subtitle, title_text_height, width, font, guide_text_placement):
    subtitle = sanitize_unicode(subtitle, font.path)

    text_width, text_height = textsize(subtitle, font)
    if guide_text_placement == 'top_left':
        text_position_x = 20
        text_position_y = 400 - text_height - 2
    elif guide_text_placement == 'top_right':
        text_position_x = width - 20 - text_width
        text_position_y = 400 - text_height - 2
    elif guide_text_placement == 'bottom_left':
        text_position_y = 400 + title_text_height + 40
        text_position_x = 20
    else:  # bottom_right is default
        text_position_y = 400 + title_text_height + 40
        text_position_x = width - 20 - text_width

    draw.text((text_position_x, text_position_y), subtitle, fill='black', font=font)


def draw_orielly(draw, height, font_text, font_question_mark, theme_color):
    oreilly_text = "O RLY"
    text_width = draw.textlength(oreilly_text, font_text)
    text_height = font_text.size * 1
    text_position_x = 20
    text_position_y = height - text_height - 20
    draw.text((text_position_x, text_position_y), oreilly_text, fill='black', font=font_text)

    draw.text((text_position_x + text_width, text_position_y - 1), "?", fill=theme_color, font=font_question_mark)


def draw_author(draw, text, width, height, font):
    text = sanitize_unicode(text, font.path)
    text_width = draw.textlength(text, font)
    text_height = font.size * 1
    text_position_x = width - text_width - 20
    text_position_y = height - text_height - 20
    draw.text((text_position_x, text_position_y), text, fill='black', font=font)


def generate_image(title, top_text, author, image_code, theme, guide_text_placement, guide_text):
    theme_colors = {
        "0": (85, 19, 93, 255), "1": (113, 112, 110, 255), "2": (128, 27, 42, 255), "3": (184, 7, 33, 255),
        "4": (101, 22, 28, 255), "5": (80, 61, 189, 255), "6": (225, 17, 5, 255), "7": (6, 123, 176, 255),
        "8": (247, 181, 0, 255), "9": (0, 15, 118, 255), "10": (168, 0, 155, 255), "11": (0, 132, 69, 255),
        "12": (0, 153, 157, 255), "13": (1, 66, 132, 255), "14": (177, 0, 52, 255), "15": (55, 142, 25, 255),
        "16": (133, 152, 0, 255)
    }
    theme_color = theme_colors.get(theme, (255, 255, 255, 255))

    width, height = 500, 700
    im = Image.new('RGBA', (width, height), "white")
    base_dir = os.path.dirname(os.path.realpath(__file__))
    fonts, font_paths = load_fonts(base_dir)

    draw = ImageDraw.Draw(im)
    draw.rectangle(((20, 0), (width - 20, 10)), fill=theme_color)

    draw_top_text(draw, top_text, width, fonts['top'])
    title_text_height = draw_title(draw, title, width, theme_color, font_paths)
    draw_subtitle(draw, guide_text, title_text_height, width, fonts['subtitle'], guide_text_placement)
    draw_orielly(draw, height, fonts['orielly'], fonts['question_mark'], theme_color)
    draw_author(draw, author, width, height, fonts['author'])

    animal_image_path = os.path.join(base_dir, 'images', f'{image_code}.png')
    animal_image = Image.open(animal_image_path).convert('RGBA')
    im.paste(animal_image, (80, 40), animal_image)

    final_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ('%s.png' % datetime.datetime.now())))
    im.save(final_path)
    im.close()

    return final_path


def sanitize_unicode(string, font_file_path):
    sanitized_string = ''
    font = TTFont(font_file_path)
    cmap = font['cmap'].getcmap(3, 1).cmap
    for char in string:
        if ord(char) in cmap:
            sanitized_string += char
    return sanitized_string


def clamp_title_text(title, width):
    im = Image.new('RGBA', (500, 500), "white")
    dr = ImageDraw.Draw(im)

    font_path_italic = os.path.abspath(os.path.join(os.path.dirname(__file__), 'fonts', 'Garamond Light.ttf'))
    start_font_size, end_font_size = 80, 61

    for font_size in range(start_font_size, end_font_size, -1):
        font = ImageFont.truetype(font_path_italic, font_size)
        w, h = textsize(title, font)
        if w < width:
            return font, title

    start_font_size, end_font_size = 80, 34
    for font_size in range(start_font_size, end_font_size, -1):
        font = ImageFont.truetype(font_path_italic, font_size)
        for match in re.finditer(r'\s', title):
            new_title = title[:match.start()] + '\n' + title[match.start() + 1:]
            substring_width, h = dr.multiline_textsize(new_title, font)
            if substring_width < width:
                return font, new_title

    im.close()
    return None, None


def textsize(text, font):
    im = Image.new(mode="P", size=(0, 0))
    draw = ImageDraw.Draw(im)
    _, _, width, height = draw.textbbox((0, 0), text=text, font=font)
    return width, height
