import cv2
import pytesseract

pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe'


# DETECTING CHARACTERS
def detectChar(img):
    print('Detecting Characters...')
    hImg, wImg, _ = img.shape
    boxes = pytesseract.image_to_boxes(img)
    # This prints the coordinates of every character
    print(boxes)
    for b in boxes.splitlines():
        print(b)
        b = b.split(' ')
        x, y, w, h = int(b[1]), int(b[2]), int(b[3]), int(b[4])
        cv2.rectangle(img, (x, hImg - y), (w, hImg - h), (0, 0, 255), 2)
        cv2.putText(img, b[0], (x, hImg - y + 35), cv2.FONT_HERSHEY_COMPLEX, 1, (50, 50, 255), 2)

    return img


# DETECTING WORDS
def detectWords(img):
    print('Detecting Words in the right side...')
    hImg, wImg, _ = img.shape
    # print('Image Height: ', hImg)
    # print('Image Width: ', wImg)
    conf = "r'--oem 2 --psm 1 -l eng/esp'"
    boxes = pytesseract.image_to_data(img, config=conf)
# This prints the information of every string
#     print(boxes)
    for x, b in enumerate(boxes.splitlines()):
        if x != 0:
            b = b.split()
            if len(b) == 12:
                print(b)
                x, y, w, h = int(b[6]), int(b[7]), int(b[8]), int(b[9])
                cv2.rectangle(img, (x, y), (w+x, h+y), (0, 0, 255), 2)
                cv2.putText(img, b[11], (x, y), cv2.FONT_HERSHEY_COMPLEX, 1, (50, 50, 255), 2)
    return img


# DETECTING WORDS
def detectWordsF(img):
    print('Detecting Words in the Front side...')
    hImg, wImg, _ = img.shape
    # print('Image Height: ', hImg)
    # print('Image Width: ', wImg)
    conf = "r'--oem 2 --psm 1 -l eng/esp'"
    wordsAsString = pytesseract.image_to_string(img, config=conf)
    boxes = pytesseract.image_to_data(img, config=conf)
# This prints the information of every string
    print(wordsAsString)
    for x, b in enumerate(boxes.splitlines()):
        if x != 0:
            b = b.split()
            if len(b) == 12:
                # print(b)
                x, y, w, h = int(b[6]), int(b[7]), int(b[8]), int(b[9])
                cv2.rectangle(img, (x, y), (w+x, h+y), (0, 0, 255), 2)
                cv2.putText(img, b[11], (x, y), cv2.FONT_HERSHEY_COMPLEX, 1, (50, 50, 255), 2)
    return img


def detectWordsLeft(img):
    print('Detecting Words in the left side...')
    hImg, wImg, _ = img.shape
    # print('Image Height: ', hImg)
    # print('Image Width: ', wImg)
    conf = "r'--oem 2 --psm 1 -l eng/esp'"
    wordsAsStrings = pytesseract.image_to_string(img, config=conf)
    boxes = pytesseract.image_to_data(img, config=conf)
# This prints the information of every string
    print(wordsAsStrings)
    for x, b in enumerate(boxes.splitlines()):
        if x != 0:
            b = b.split()
            if len(b) == 12:
                # print(b)
                x, y, w, h = int(b[6]), int(b[7]), int(b[8]), int(b[9])
                cv2.rectangle(img, (x, y), (w+x, h+y), (0, 0, 255), 2)
                cv2.putText(img, b[11], (x, y), cv2.FONT_HERSHEY_COMPLEX, 1, (50, 50, 255), 2)
    return img


# DETECTING NUMBERS
def detectNumbers(img):
    print('Detecting Numbers...')
    hImg, wImg= img.shape
    print('Image Height: ', hImg)
    print('Image Width: ', wImg)
    cong = r'--oem 0 --psm 6 outputbase digits'
    boxes = pytesseract.image_to_data(img, config=cong)
# This prints the information of every string
# print(boxes)
    for x, b in enumerate(boxes.splitlines()):
        if x != 0:
            b = b.split()
            if len(b) == 12:
                # print(b)
                x, y, w, h = int(b[6]), int(b[7]), int(b[8]), int(b[9])
                cv2.rectangle(img, (x, y), (w+x, h+y), (0, 0, 255), 2)
                cv2.putText(img, b[11], (x, y), cv2.FONT_HERSHEY_COMPLEX, 1, (50, 50, 255), 2)
    return img





