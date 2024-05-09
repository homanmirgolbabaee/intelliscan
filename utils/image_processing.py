import os
from PIL import Image, ImageDraw
from config import IMAGE_DIRECTORY

def load_images():
    images = []
    for file in os.listdir(IMAGE_DIRECTORY):
        if file.endswith(('.png', '.jpg', '.jpeg')):
            images.append(os.path.join(IMAGE_DIRECTORY, file))
    return images

def draw_boxes(image_path, boxes):
    with Image.open(image_path) as im:
        draw = ImageDraw.Draw(im)
        for box in boxes:
            xmin, ymin, xmax, ymax = box
            draw.rectangle(((xmin, ymin), (xmax, ymax)), outline="red", width=3)
        im.show()
