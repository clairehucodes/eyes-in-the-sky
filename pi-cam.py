#make needed imports
#from picamera import PiCamera
from time import sleep
from twilio.rest import Client
import cv2
import numpy as np


# #STEP 1: CAPTURE PHOTO
# camera = PiCamera()

# #open cam and give 30 sec intervals between capture
# camera.start_preview()
# sleep(30)

# #replace file path
# camera.capture('/home/pi/Desktop/image.jpg')
# camera.stop_preview()

# #STEP 2: DETECT SKY CONTOURS & SAVE AS ISOLATED IMAGE
# def isolate_sky(image):
#   # Load the image and convert it to grayscale
#   img = cv2.imread(image)
#   gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

#   # Invert the grayscale image
#   gray = cv2.bitwise_not(gray)

#   # Threshold the image to create a binary image
#   _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

#   # Find the contours in the image
#   contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

#   # Find the contour with the largest area --> ask user to position camera where sky takes us majority of frame
#   contour = max(contours, key=cv2.contourArea)

#   # Create a mask image with the same size as the original image
#   mask = np.zeros(img.shape[:2], np.uint8)

#   # Fill the mask with the contour
#   cv2.drawContours(mask, [contour], -1, (255, 255, 255), -1)

#   # Use the mask to isolate the sky in the original image
#   isolated_sky = cv2.bitwise_and(img, img, mask=mask)

#   return isolated_sky

# #test path
# path = r'/Users/clairehu/Documents/GitHub/eyes-in-the-sky/sunset-photo.png'
# image_before = cv2.imread(path)
# cv2.imshow('image before mask', image_before)


# isolated_sky = isolate_sky(path)
# cv2.imwrite('isolated_sky.jpg', isolated_sky)
# image_after = cv2.imread('isolated_sky.jpg')
# cv2.imshow('image after mask', image_after)


#STEP 3: LOOP AND FIND NUM OF PRETTY COLORS
# Read the image file
# resize image here????
#uncomment later to use isolated sky

#image = cv2.imread('isolated_sky.jpg'), CHANGE image_before to say image_after after we figure out step 2
# Convert the image to HSV color space
hsv = cv2.cvtColor(image_before, cv2.COLOR_BGR2HSV)
cv2.imshow('image before mask', image_before)
print(image_before.shape)

# Extract the H, S, and V channels
h, s, v = cv2.split(hsv)

# Set the lower and upper bounds for the colors we want to detect
lower_yellow = np.array([0, 65, 205])
upper_yellow = np.array([60, 255, 255])
yellow_mask = cv2.inRange(hsv, lower_yellow, upper_yellow)

lower_magenta = np.array([135, 65, 205])
upper_magenta = np.array([360, 255, 255])
magenta_mask = cv2.inRange(hsv, lower_magenta, upper_magenta)

# Count the number of pixels for each color
yellow_pixels = cv2.countNonZero(yellow_mask)
magenta_pixels = cv2.countNonZero(magenta_mask)

print("Yellow pixels:", yellow_pixels)
print("Magenta pixels:", magenta_pixels)

#IF ABOVE THRESHOLD, SEND A TEXT VIA TWILIO API
# replace placeholder # of 100 with something else
# Check if the number of red pixels exceeds the threshold
trigger_colors = yellow_pixels + magenta_pixels
if trigger_colors > 1000:
    print('lots of  colors')
    # Set up the Twilio API client
    account_sid = 'AC90d2aec1b48d86aadca0ac3b5e4175b1'
    auth_token = '529a30cd7d3c052ddc809f9eb939baa8'
    client = Client(account_sid, auth_token)

    # Send the text message
    message = client.messages \
                    .create(
                         body='There are more than 100 red, yellow, or magenta pixels in the image! WAKE UP RIGHT NOW!',
                         from_='+13862603449',
                         to='+15135387028'
                     )
    print(f'Sent message: {message.sid}')
else:
    print(f'No action needed')