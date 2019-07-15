# This Python file uses the following encoding: utf-8
import argparse
import os
import codecs
import glob

from shutil import copyfile
from PIL import Image
from PIL import ImageFont
from PIL import ImageFile
from PIL import ImageDraw


ImageFile.LOAD_TRUNCATED_IMAGES = True

DEFAULT_LIST_FILE_NAME = r'list.txt'
DEFAULT_MOCK_UP_FILE_NAME = r'mock_up.jpg'
DEFAULT_FONT_NAME = "l_10646.ttf"
DEFAULT_TEXT_MARGIN_LEFT = 0.5
DEFAULT_TEXT_MARGIN_TOP = 0.125
DEFAULT_FACE_MARGIN_LEFT = 0.1
DEFAULT_FACE_MARGIN_TOP = 0.1
FONTS_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'fonts')


def read_names_from_file(dir_path, file_name):
    people = []
    with codecs.open(os.path.join(dir_path, file_name), encoding='utf-8') as f:
        for line in f:
            if len(line) > 2:
                line = line.strip()
                line = line.split('. ', 1)[-1]
                people.append(line)
    return people


def create_badges(dir_path, mock_up_name, list_file_name):
    people = read_names_from_file(dir_path, list_file_name)
    faces = glob.glob(os.path.join(dir_path,"[0-9]*.jpg"))
    if len(faces) != len(people):
        print "INCORRECT INPUT"
        print people
        print faces
        return
    for i in range(len(people)):
        lines = people[i].split(' ')
        create_one_badge(dir_path, mock_up_name, faces[i], lines[1], lines[0])


def put_photo_on_badge(img, face_img, margin_left, margin_right):
    img.paste(face_img, (margin_left, margin_right))


def create_one_badge(dir_path, mock_up_name, face_pic, name, surname):
    mock_up = os.path.join(dir_path, mock_up_name)
    badge_path = os.path.join(dir_path, name + " " + surname)
    face_path = os.path.join(dir_path, face_pic)
    copyfile(mock_up, badge_path)

    img = Image.open(badge_path)
    width, height = img.size

    face_img = Image.open(face_path)
    face_img = face_img.resize((int(width / 3), int(height / 1.5)))
    face_margin = int(height * DEFAULT_FACE_MARGIN_LEFT)
    put_photo_on_badge(img, face_img,
                       margin_left=face_margin,
                       margin_right=face_margin)

    name_font_size = (int(width / 1.5)) / len(name)
    surname_font_size = (int(width / 1.5)) / len(surname)

    if name_font_size > int(width / 10):
        name_font_size = int(width / 10)

    if surname_font_size > int(width / 10):
        surname_font_size = int(width / 10)

    print_name_on_badge(img, name, surname, name_font_size, surname_font_size,
                        margin_left=int(width * DEFAULT_TEXT_MARGIN_LEFT),
                        margin_top=int(height * DEFAULT_TEXT_MARGIN_TOP))
    img.save(badge_path + '.jpg')


def print_name_on_badge(img, name, surname,
                        name_font_size, surname_font_size,
                        margin_left, margin_top):
    draw = ImageDraw.Draw(img)

    font = ImageFont.truetype(os.path.join(FONTS_PATH, DEFAULT_FONT_NAME), name_font_size)
    draw.text((margin_left, margin_top), name, fill=(255, 69, 0), font=font)

    font = ImageFont.truetype(os.path.join(FONTS_PATH, DEFAULT_FONT_NAME), surname_font_size)
    draw.text((margin_left, margin_top + name_font_size), surname, fill=(255, 69, 0), font=font)

    #img.show()


parser = argparse.ArgumentParser()
parser.add_argument("--path_to_squad_dir", required=True)
parser.add_argument("--mock_up_name", default=DEFAULT_MOCK_UP_FILE_NAME)
parser.add_argument("--list_file_name", default=DEFAULT_LIST_FILE_NAME)
parser.add_argument("--face_margin_from_top", default=DEFAULT_FACE_MARGIN_TOP, type=float)
parser.add_argument("--face_margin_from_left", default=DEFAULT_FACE_MARGIN_LEFT, type=float)
parser.add_argument("--name_margin_from_top", default=DEFAULT_TEXT_MARGIN_TOP, type=float)
parser.add_argument("--name_margin_from_left", default=DEFAULT_TEXT_MARGIN_LEFT, type=float)

args = parser.parse_args()


create_badges(args.path_to_squad_dir, args.mock_up_name, args.list_file_name)
#read_names_from_file(args.path_to_squad_dir, args.list_file_name)
#create_one_badge(args.path_to_squad_dir, r'mock_up.jpg',
#                 '1.jpg', u"Егор Янышев")
