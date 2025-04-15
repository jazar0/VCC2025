import cv2 
import numpy as np

roi = None
roi2 = None

def load_thresholds(path='thresholds.txt'):
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

def display():  # this function displays multiple windows and handles/returns the ROI
    global roi, roi2
    # init and display HSV/BGR frames
    ret, frame = cap.read()
    hsvFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    #cv2.imshow("HSV", hsvFrame)
    #cv2.imshow("BGR", frame)

    # roi 
    x = cv2.getTrackbarPos('X', 'Trackbars') 
    y = cv2.getTrackbarPos('Y', 'Trackbars') 
    scale = cv2.getTrackbarPos('Scale', 'Trackbars')  #assign variables handled by trackbar

    # roi 2
    x2 = cv2.getTrackbarPos('X2', 'Trackbars') 
    y2 = cv2.getTrackbarPos('Y2', 'Trackbars') 
    scale2 = cv2.getTrackbarPos('Scale2', 'Trackbars')  #assign variables handled by trackbar

    hsvroirec = hsvFrame.copy() # copy so dont ruin the OG HSV image with rectangle
    cv2.rectangle(hsvroirec, (x2, y2), (x2 + scale2, y2 + scale2), (255, 255, 255), 1)
    cv2.rectangle(hsvroirec, (x, y), (x + scale, y + scale), (255, 255, 255), 1)
    cv2.imshow("HSV ROI Rectangle", hsvroirec) #draw rectangle on OG hsv to track roi 1/2 pos
    
    roi = hsvFrame[y:y + scale, x:x + scale] # crop roi from hsvFrame
    roi2 = hsvFrame[y2:y2 + scale2, x2:x2 + scale2] 
    cv2.imshow("ROI", roi)
    cv2.imshow("ROI2", roi2)
    return roi, roi2
    
def onTrackbarChange(x):
    return

def trackbarsInit(): #create trackbars (for ROI)
    ret, frame = cap.read()
    cv2.namedWindow("Trackbars")
    cv2.createTrackbar("X", "Trackbars", 0, frame.shape[1], onTrackbarChange) # sets max value as the width of image, this value controls the x value of the square for roi
    cv2.createTrackbar("Y", "Trackbars", 0, frame.shape[0], onTrackbarChange) # sets max value as height of image, this value controls the y value of the square for roi     
    cv2.createTrackbar("Scale", "Trackbars", 100, frame.shape[0], onTrackbarChange) #min value is 100 pix, max is the height, this value controls the scale value of the square for roi

    #trackbars for second ROI
    cv2.createTrackbar("X2", "Trackbars", 0, frame.shape[1], onTrackbarChange) # sets max value as the width of image, this value controls the x value of the square for roi
    cv2.createTrackbar("Y2", "Trackbars", 0, frame.shape[0], onTrackbarChange) # sets max value as height of image, this value controls the y value of the square for roi     
    cv2.createTrackbar("Scale2", "Trackbars", 100, frame.shape[0], onTrackbarChange) #min value is 100 pix, max is the height, this value controls the scale value of the square for roi
    # most of these will be changed to constants once we get definite camera resolution

def compare(thresholds, roi):
    max_match_count = 0
    detected_color = "Unknown"
    
    for color, thresh in thresholds.items():
        mask = cv2.inRange(roi, thresh['low'], thresh['high'])
        match_count = cv2.countNonZero(mask)
        
        if match_count > max_match_count and match_count > 50:  # min matches need to be 50 px, it selects the color with most matching pixels
            max_match_count = match_count
            detected_color = color

    return detected_color

#initialization
cap = cv2.VideoCapture(1)
cap.set(cv2.CAP_PROP_AUTO_WB, 0.0) # Disable automatic white balance
cap.set(cv2.CAP_PROP_WB_TEMPERATURE, 4200) # Set manual white balance temperature to 4200K
cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0) 
cap.set(cv2.CAP_PROP_EXPOSURE, -7) 
trackbarsInit()
thresholds = load_thresholds()

prev_color_lane1 = None
prev_color_lane2 = None

while True:
    display()
    if roi is not None and roi2 is not None:
        color_lane1 = compare(thresholds, roi)
        color_lane2 = compare(thresholds, roi2)

        if color_lane1 != prev_color_lane1:
            print(f"Lane 1: {color_lane1}")
            prev_color_lane1 = color_lane1

        if color_lane2 != prev_color_lane2:
            print(f"Lane 2: {color_lane2}")
            prev_color_lane2 = color_lane2

    if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
