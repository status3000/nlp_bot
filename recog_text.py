import cv2
import os
import pytesseract
import re

def img_loader(img_path):
    exists = os.path.isfile(img_path)
    if exists:
        img = cv2.imread(img_path)
        print("Success! The image exists")
        custom_config = r'-l rus+eng+bel --psm 6'
        result = pytesseract.image_to_string(img, config=custom_config)
        return result


def find_amounts(text):
    amounts = re.findall(r'\d+\.\d{2}\b', text)
    floats = [float(amount) for amount in amounts]
    unique = list(dict.fromkeys(floats))
    return unique

def check_sum():
    return max(find_amounts(img_loader()))

def check_detect(img_path):
    text = img_loader(img_path)
    amount = find_amounts(text)
    res = max(amount)
    return res
