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

#STEP 2: DETECT SKY CONTOURS
def isolate_sky(image):
  # Load the image and convert it to grayscale
  img = cv2.imread(image)
  gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

  # Invert the grayscale image
  gray = cv2.bitwise_not(gray)

  # Threshold the image to create a binary image
  _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

  # Find the contours in the image
  contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

  # Find the contour with the largest area --> ask user to position camera where sky takes us majority of frame
  contour = max(contours, key=cv2.contourArea)

  # Create a mask image with the same size as the original image
  mask = np.zeros(img.shape[:2], np.uint8)

  # Fill the mask with the contour
  cv2.drawContours(mask, [contour], -1, (255, 255, 255), -1)

  # Use the mask to isolate the sky in the original image
  isolated_sky = cv2.bitwise_and(img, img, mask=mask)

  return isolated_sky

#test path
path = r'/Users/clairehu/Documents/GitHub/eyes-in-the-sky/sunset-photo.png'
image_before = cv2.imread(path)
cv2.imshow('image before mask', image_before)


isolated_sky = isolate_sky(path)
cv2.imwrite('isolated_sky.jpg', isolated_sky)
image_after = cv2.imread('isolated_sky.jpg')
cv2.imshow('image after mask', image_after)


#STEP 3: LOOP AND FIND NUM OF PRETTY COLORS
# Read the image file


#resize image here????
#uncomment later to use isolated sky
#image = cv2.imread('isolated_sky.jpg')

# Convert the image to HSV color space
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# Extract the H, S, and V channels
h, s, v = cv2.split(hsv)

# Set the lower and upper bounds for the colors we want to detect
lower_red = np.array([0, 50, 70])
upper_red = np.array([10, 255, 255])
lower_yellow = np.array([20, 50, 70])
upper_yellow = np.array([30, 255, 255])
lower_magenta = np.array([300, 50, 30])
upper_magenta = np.array([360, 255, 255])

# Initialize counters for the number of red, yellow, and magenta pixels
red_count = 0
yellow_count = 0
magenta_count = 0

# Iterate over the image pixels
for i in range(image.shape[0]):
    for j in range(image.shape[1]):
        # Get the H, S, and V values for the current pixel
        h_val = h[i][j]
        s_val = s[i][j]
        v_val = v[i][j]
        
        # Check if the pixel is within the red range
        if lower_red[0] <= h_val <= upper_red[0] and lower_red[1] <= s_val <= upper_red[1] and lower_red[2] <= v_val <= upper_red[2]:
            red_count += 1
        # Check if the pixel is within the yellow range
        elif lower_yellow[0] <= h_val <= upper_yellow[0] and lower_yellow[1] <= s_val <= upper_yellow[1] and lower_yellow[2] <= v_val <= upper_yellow[2]:
            yellow_count += 1
        # Check if the pixel is within the magenta range
        elif lower_magenta[0] <= h_val <= upper_magenta[0] and lower_magenta[1] <= s_val <= upper_magenta[1] and lower_magenta[2] <= v_val <= upper_magenta[2]:
            magenta_count += 1

# Print the counts
print(f'Number of red pixels: {red_count}')
print(f'Number of yellow pixels: {yellow_count}')
print(f'Number of magenta pixels: {magenta_count}')

#IF ABOVE THRESHOLD, SEND A TEXT VIA TWILIO API
# replace placeholder # of 100 with something else
# Check if the number of red pixels exceeds the threshold
if red_count > 100 or yellow_count > 100 or magenta_count > 100:
#trigger_colors = red_count + yellow_count + magenta_count
#if trigger_colors > 1000:
    # Set up the Twilio API client
    account_sid = 'AC90d2aec1b48d86aadca0ac3b5e4175b1'
    auth_token = '755a80c9f33edb80adebedb3cae60d6e'
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