import cv2
import imutils
import util.textDetector as detector
from skimage.filters import threshold_local

from util.transform import four_point_transform, rotate_bound

# # construct the argument parser
# ap = argparse.ArgumentParser()
# ap.add_argument("-i", "--image", required=True, help="Path to the image to be scanned")
# args = vars(ap.parse_args())


# load the image and compute the ratio of the old height
# to the new height, clone it, and resize it
# image = cv2.imread("resources/dui.jpg")
# ratio = image.shape[0] / 500.0
# orig = image.copy()
# image = imutils.resize(image, height=500)

# convert the image to grayscale, blur it, and find edges
# in the image
# gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# gray = cv2.GaussianBlur(gray, (5, 5), 0)
# edged = cv2.Canny(gray, 75, 200)

# Repeat the process for the front part of the DUI
imagef = cv2.imread("resources/dui-front3.jpg")
ratiof = imagef.shape[0] / 500.0
origf = imagef.copy()
imagef = imutils.resize(imagef, height=500)
grayf = cv2.cvtColor(imagef, cv2.COLOR_BGR2GRAY)
grayf = cv2.GaussianBlur(grayf, (5, 5), 0)
edgedf = cv2.Canny(grayf, 75, 200)

# show the original image and the edge detected image
print("STEP 1: Edge Detection")
# cv2.imshow("Image", image)
# cv2.imshow("Edged", edged)

# find the contours in the edged image, keeping only the
# largest ones, and initialize the screen contour
# cnts = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
# cnts = imutils.grab_contours(cnts)
# cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:5]
# loop over the contours
# for c in cnts:
    # approximate the contour
    # peri = cv2.arcLength(c, True)
    # approx = cv2.approxPolyDP(c, 0.02 * peri, True)
    # if our approximated contour has four points, then we
    # can assume that we have found our screen
    # if len(approx) == 4:
    #     screenCnt = approx
    #     break

# Repeat the process for the front part of the DUI
cntsf = cv2.findContours(edgedf.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
cntsf = imutils.grab_contours(cntsf)
cntsf = sorted(cntsf, key=cv2.contourArea, reverse=True)[:5]
# loop over the contours
for c in cntsf:
    # approximate the contour
    perif = cv2.arcLength(c, True)
    approxf = cv2.approxPolyDP(c, 0.02 * perif, True)
    # if our approximated contour has four points, then we
    # can assume that we have found our screen
    if len(approxf) == 4:
        screenCntf = approxf
        break

# show the contour (outline) of the piece of paper
print("STEP 2: Find contours of paper")
# cv2.drawContours(image, [screenCnt], -1, (0, 255, 0), 2)
# cv2.imshow("Outline", image)

# apply the four point transform to obtain a top-down
# view of the original image
# print(screenCnt.reshape(4, 2) * ratio)
# warped = four_point_transform(orig, screenCnt.reshape(4, 2) * ratio)

# convert the warped image to grayscale, then threshold it
# to give it that 'black and white' paper effect
# warped = cv2.cvtColor(warped, cv2.COLOR_BGR2BGRA)
# T = threshold_local(warped, 11, offset = 10, method = "gaussian")
# warped = warped.astype("uint8") * 255

# Repeat for the front
cv2.drawContours(imagef, [screenCntf], -1, (0, 255, 0), 2)
warpedf = four_point_transform(origf, screenCntf.reshape(4, 2) * ratiof)
warpedf = warpedf.astype("uint8") * 255

# show the original and scanned images
print("STEP 3: Apply perspective transform")
# cv2.imshow("Original", imutils.resize(orig, height = 650))
# cv2.imshow("Scanned", imutils.resize(warped, height = 650))


# Cropping the image into 2 separate images.
print("STEP 4: Crop image and create each side separately")
# resizedImg = imutils.resize(warped, height = 650)
# hImg, wImg, _= resizedImg.shape
#
# leftImg = resizedImg[185:hImg-190, 5:670]
# rightImg = resizedImg[167:hImg - 220, 665: wImg -40]
# cv2.imshow("Left", leftImg)
# cv2.imshow("Right", rightImg)

# Process for the front
resizedFront = imutils.resize(warpedf, height=650)
resizedFront = rotate_bound(resizedFront, -90)
hImg, wImg, _ = resizedFront.shape

resizedFront = resizedFront[90: hImg-90, 0: wImg]

# Obtaining words
# leftWords = detector.detectWordsLeft(imutils.resize(leftImg, height = 450))
# rightWords = detector.detectWords(imutils.resize(rightImg, height = 650))
# cv2.imshow("Left Words", leftWords)
# cv2.imshow("Right Words", rightWords)
frontWords = detector.detectWords(imutils.resize(resizedFront, height = 650))
cv2.imshow("Front Words", frontWords)
cv2.waitKey(0)

