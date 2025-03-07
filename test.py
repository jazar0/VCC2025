import cv2 
import numpy as np

roi = None
initialH, initialS, initialV = None, None, None

def display():  # this function displays multiple windows and handles/returns the ROI
    global roi

    # init and display HSV/BGR frames
    ret, frame = cap.read()
    hsvFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    #cv2.imshow("HSV", hsvFrame)
    #cv2.imshow("BGR", frame)

    # roi 
    x = cv2.getTrackbarPos('X', 'Trackbars') 
    y = cv2.getTrackbarPos('Y', 'Trackbars') 
    scale = cv2.getTrackbarPos('Scale', 'Trackbars')  #assign variables handled by trackbar

    hsvroirec = hsvFrame.copy() # copy so dont ruin the OG HSV image with rectangle
    cv2.imshow("HSV ROI Rectangle", cv2.rectangle(hsvroirec, (x, y), (x + scale, y + scale), (255, 255, 255), 1)) #draw rectangle on OG hsv to track roi pos
    
    roi = hsvFrame[y:y + scale, x:x + scale] # crop roi from hsvFrame
    cv2.imshow("ROI", roi)
    return roi
    
def hsvGetInitial(roi): # grabs initial HSV (DOES NOT RUN ONCE. RUNS EVERY TIME TRACKBAR IS UPDATED.) for future comparison
    global initialH, initialS, initialV
    avgH = np.round(np.mean(roi[:, :, 0]), 2)
    avgS = np.round(np.mean(roi[:, :, 1]), 2)     # splits hsv channels, takes indivudual avgs, and rounds to 2 decimal places 
    avgV = np.round(np.mean(roi[:, :, 2]), 2)
    print("Initial HSV:(", avgH, ",", avgS, ",", avgV, ")")

    initialH, initialS, initialV = avgH, avgS, avgV

def onTrackbarChange(x):
    global roi  
    if roi is not None:
        hsvGetInitial(roi)
    return

def trackbarsInit(): #create trackbars (for ROI)
    ret, frame = cap.read()
    cv2.namedWindow("Trackbars")
    cv2.createTrackbar("X", "Trackbars", 0, frame.shape[1], onTrackbarChange) # sets max value as the width of image, this value controls the x value of the square for roi
    cv2.createTrackbar("Y", "Trackbars", 0, frame.shape[0], onTrackbarChange) # sets max value as height of image, this value controls the y value of the square for roi     
    cv2.createTrackbar("Scale", "Trackbars", 100, frame.shape[0], onTrackbarChange) #min value is 100 pix, max is the height, this value controls the scale value of the square for roi
    # most of these will be changed to constants once we get definite camera resolution

def compare(initialH, initialS, initialV, roi):

    currentH = np.round(np.mean(roi[:, :, 0]), 2)
    currentS = np.round(np.mean(roi[:, :, 1]), 2)
    currentV = np.round(np.mean(roi[:, :, 2]), 2)

    print("Current HSV:(", currentH, ",", currentS, ",", currentV, ")")
    #Include the Comparing code here.
    #TODO: Figure out which changes in H/S/V compared to original correspond to a red, blue, green, or yellow marble
    #Once above is known, simply implement the comparing logic by comparing values


#initialization
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_AUTO_WB, 0.0) # Disable automatic white balance
cap.set(cv2.CAP_PROP_WB_TEMPERATURE, 4200) # Set manual white balance temperature to 4200K
cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0) 
cap.set(cv2.CAP_PROP_EXPOSURE, -7) 
trackbarsInit()

while True:
    display()
    compare(initialH, initialS, initialV, roi) # feed the 3 global variables for the initial HSV (which is updated upon trackbar moving) and the current roi and compares them
    if cv2.waitKey(1) & 0xFF == ord('q'):
            break
