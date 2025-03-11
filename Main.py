import cv2 
import numpy as np

roi = None
roi2 = None
initialH, initialS, initialV = None, None, None
initialH2, initialS2, initialV2 = None, None, None


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
    
def hsvGetInitial(roi, roi2): # grabs initial HSV (DOES NOT RUN ONCE. RUNS EVERY TIME TRACKBAR IS UPDATED.) for future comparison
    global initialH, initialS, initialV, initialH2, initialS2, initialV2 
    avgH = np.round(np.mean(roi[:, :, 0]), 2)
    avgS = np.round(np.mean(roi[:, :, 1]), 2)     # splits hsv channels, takes indivudual avgs, and rounds to 2 decimal places 
    avgV = np.round(np.mean(roi2[:, :, 2]), 2)
    
    avgH2 = np.round(np.mean(roi2[:, :, 0]), 2)
    avgS2 = np.round(np.mean(roi2[:, :, 1]), 2)     # splits hsv channels, takes indivudual avgs, and rounds to 2 decimal places 
    avgV2 = np.round(np.mean(roi2[:, :, 2]), 2)
    
    print("Initial HSV:(", avgH, ",", avgS, ",", avgV, ")")
    print("Initial HSV2:(", avgH2, ",", avgS2, ",", avgV2, ")")

    initialH, initialS, initialV = avgH, avgS, avgV
    initialH2, initialS2, initialV2 = avgH2, avgS2, avgV2


def onTrackbarChange(x):
    global roi, roi2
    if roi is not None:
        hsvGetInitial(roi, roi2)
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

def compare(initialH, initialS, initialV, roi):
    currentH = np.round(np.mean(roi[:, :, 0]), 2)
    #currentS = np.round(np.mean(roi[:, :, 1]), 2)
    #currentV = np.round(np.mean(roi[:, :, 2]), 2)  # S and V unneeded for now, Hue is the main deciding factor in color

    diffH = abs(currentH - initialH)
    #print(diffH)
    color_thresholds = { #thresholds. the differences in initial/ current hue that correspond to each color
        "Red": [(20,34)], # random values, will be changed
        "Yellow": [(17, 21)],
        "Green": [(6, 15)],
        "Blue": [(50, 70)]   
    }

    for color, ranges in color_thresholds.items():
        for (low, high) in ranges:
            if low <= diffH <= high:
                return color
    return "Unknown"
            
    #TODO: Figure out which changes in H/S/V compared to original correspond to a red, blue, green, or yellow marble


#initialization
cap = cv2.VideoCapture(1)
cap.set(cv2.CAP_PROP_AUTO_WB, 0.0) # Disable automatic white balance
cap.set(cv2.CAP_PROP_WB_TEMPERATURE, 4200) # Set manual white balance temperature to 4200K
cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0) 
cap.set(cv2.CAP_PROP_EXPOSURE, -7) 
trackbarsInit()

while True:
    display()
    if initialH is not None:
        print(compare(initialH, initialS, initialV, roi)) # feed the 3 global variables for the initial HSV (which is updated upon trackbar moving) and the current roi and compares them
        #print("CURRENT COLOR FOR ROI 2", compare(initialH2, initialS2, initialV2, roi2)) # feed the 3 global variables for the initial HSV (which is updated upon trackbar moving) and the current roi and compares them
    if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()