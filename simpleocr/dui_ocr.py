from simpleocr.files import open_image
from pathlib import Path
import cv2 as cv
import time

#Setting variables with
pathDuiFront = "dui-front.jpg"
pathDuiReverse = "dui-reverse.jpg"

#Calling "open_image(path)" from files.py
duiFront = open_image(pathDuiFront)
duiReverse = open_image(pathDuiReverse)

#Checking emptiness
if duiFront is None:
    print("Front not working")
else:
    print("Front working")

if duiReverse is None:
    print("Reverse not working")
else:
    print("Reverse working")
