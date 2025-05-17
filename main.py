import cv2 
import numpy as np
import serial
import math
import time

Arduino_Serial = serial.Serial('com4', 9600) # Create Serial port object 

roi = None
roi2 = None

# Constants
distance = 17.5
radius = 13

# ------------- FUNCTIONS -------------
def load_thresholds(path='thresholds.txt'): # Loads threshold values from a text file
    thresholds = {}
    with open(path, 'r') as f:
        for line in f:
            name, values = line.strip().split(':')
            vals = list(map(int, values.split(',')))
            thresholds[name] = {
                'low': np.array(vals[0:3]),
                'high': np.array(vals[3:6])
            }
    return thresholds

def load_rois(path='rois.txt'):
    rois = {}
    with open(path, 'r') as f:
        for line in f:
            name, values = line.strip().split(':')
            x, y, scale = map(int, values.split(','))
            rois[name.strip()] = {'x': x, 'y': y, 'scale': scale}
    return rois

def display():  # This function displays multiple windows and handles/returns the ROI
    global roi, roi2
    
    # Initialize BGR/HSV 
    ret, frame = cap.read()
    hsvFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Set ROI bounds via trackbars
    x = cv2.getTrackbarPos('X', 'Trackbars') 
    y = cv2.getTrackbarPos('Y', 'Trackbars') 
    scale = cv2.getTrackbarPos('Scale', 'Trackbars')  

    x2 = cv2.getTrackbarPos('X2', 'Trackbars') 
    y2 = cv2.getTrackbarPos('Y2', 'Trackbars') 
    scale2 = cv2.getTrackbarPos('Scale2', 'Trackbars') 

    hsvroirec = hsvFrame.copy() # Copy old frame and display rectanges on top
    cv2.rectangle(hsvroirec, (x2, y2), (x2 + scale2, y2 + scale2), (255, 255, 255), 1)
    cv2.rectangle(hsvroirec, (x, y), (x + scale, y + scale), (255, 255, 255), 1)
    cv2.imshow("HSV ROI Rectangle", hsvroirec) 
    
    roi = hsvFrame[y:y + scale, x:x + scale] # Crop the ROI from full frams and display them
    roi2 = hsvFrame[y2:y2 + scale2, x2:x2 + scale2] 
    cv2.imshow("ROI", roi)
    cv2.imshow("ROI2", roi2)
    return roi, roi2
    
def onTrackbarChange(x):
    return

def trackbarsInit(): 
    # Load the calibrated ROI values
    rois = load_rois()

    roi1 = rois['ROI1']
    roi2 = rois['ROI2']

    # Initialize Trackbars with default positions from rois.txt
    ret, frame = cap.read()
    cv2.namedWindow("Trackbars")
    cv2.createTrackbar("X", "Trackbars", roi1['x'], frame.shape[1], onTrackbarChange)  # Set default to ROI1's x position
    cv2.createTrackbar("Y", "Trackbars", roi1['y'], frame.shape[0], onTrackbarChange)  # Set default to ROI1's y position
    cv2.createTrackbar("Scale", "Trackbars", roi1['scale'], frame.shape[0], onTrackbarChange)  # Set to ROI1's scale

    # Trackbars for second ROI (ROI2)
    cv2.createTrackbar("X2", "Trackbars", roi2['x'], frame.shape[1], onTrackbarChange)  # Set to ROI2's x position
    cv2.createTrackbar("Y2", "Trackbars", roi2['y'], frame.shape[0], onTrackbarChange)  # Set to ROI2's y position
    cv2.createTrackbar("Scale2", "Trackbars", roi2['scale'], frame.shape[0], onTrackbarChange)  # Set to ROI2's scale

def compare(thresholds, roi): # Function that compares the ROI with thresholds
    max_match_count = 0
    detected_color = "Unknown"
    
    for color, thresh in thresholds.items():
        mask = cv2.inRange(roi, thresh['low'], thresh['high'])
        match_count = cv2.countNonZero(mask)
        
        if match_count > max_match_count and match_count > 35:  # min matches need to be 50 px, it selects the color with most matching pixels
            max_match_count = match_count
            detected_color = color

    return detected_color

def getAngle(d, r): # Get the angle needed with bar distance d and lever arm r
    return 360*math.asin(d/(2*r))/math.pi

def goToPosition(pos): # Go to a certain position based on the current position and constant distance and radius
    print('Going to: ', pos)
    global currentPosition, distance, radius
    angle = getAngle(distance, radius)
    print('Angle: ', angle)
    if (pos == 0):
        Arduino_Serial.write(str.encode('0f'))
    if (pos == 1):
        Arduino_Serial.write(str.encode(str(-1 * angle) + 'f'))
    if (pos == 2):
        Arduino_Serial.write(str.encode('180f'))
    if (pos == 3):
        Arduino_Serial.write(str.encode(str(180-angle) + 'f'))
    if (pos == 4):
        Arduino_Serial.write(str.encode(str(90-(angle/2)) + 'f'))
    
    currentPosition = pos
# ------------- INITIALIZATION -------------
cap = cv2.VideoCapture(1)
cap.set(cv2.CAP_PROP_AUTO_WB, 0.0) # Disable automatic white balance
cap.set(cv2.CAP_PROP_WB_TEMPERATURE, 4200) # Set manual white balance temperature to 4200K
cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0) 
cap.set(cv2.CAP_PROP_EXPOSURE, -7) 
trackbarsInit()

# -- Variables --
start = False # Prevents it from immediately detecting colors
thresholds = load_thresholds()
prev_color_lane1 = None
prev_color_lane2 = None

laneOfInterest = None # last detected lane. L = left lane, R = right lane 
colorOfInterest = None # last detected color

currentPosition = 0     # Positions:
                        #0 = Yellow in Lane R/Default
                        #1 = Yellow in Lane L
                        #2 = Blue in Lane R
                        #3 = Blue in Lane L
                        #4 = Horizontal 

# ------------- MAIN LOOP -------------
while True:
    display()
    if cv2.waitKey(1) & 0xFF == ord('s'):
        start = True
        print("Program Start!")
        
    if roi is not None and roi2 is not None and start == True:
        color_lane1 = compare(thresholds, roi)
        color_lane2 = compare(thresholds, roi2)

        if color_lane1 != prev_color_lane1:
            print(f"Detected in lane 1: {color_lane1}")
            prev_color_lane1 = color_lane1
            laneOfInterest = "L"
            colorOfInterest = color_lane1
            
        if color_lane2 != prev_color_lane2:
            print(f"Detected in lane 2: {color_lane2}")
            prev_color_lane2 = color_lane2
            laneOfInterest = "R"
            colorOfInterest = color_lane2

        if colorOfInterest in ["Red", "Green"] and currentPosition != 4:
            goToPosition(4)
            print(4)

        elif colorOfInterest == "Yellow":
            if laneOfInterest == "R":
                if currentPosition != 0:
                    goToPosition(0)
            else:
                if currentPosition != 1:
                    goToPosition(1)

        elif colorOfInterest == "Blue":
            if laneOfInterest == "R":
                if currentPosition != 2:
                    goToPosition(2)

            else:
                if currentPosition != 3:
                    goToPosition(3)

    if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
