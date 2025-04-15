import cv2
import numpy as np

def nothing(x): pass

# Define color names
colors = ['Red1', 'Red2', 'Yellow', 'Green', 'Blue']
selected_color_index = 0  # starts on Red1

cv2.namedWindow("Trackbars")
cv2.namedWindow("View")

cv2.createTrackbar("Color", "Trackbars", 0, len(colors) - 1, nothing) # trackbar for colors

for ch in ['H_low', 'S_low', 'V_low', 'H_high', 'S_high', 'V_high']:  # trackbar for hsv range
    cv2.createTrackbar(ch, "Trackbars", 0, 179 if 'H' in ch else 255, nothing)

cv2.setTrackbarPos("H_low", "Trackbars", 0) # defaults
cv2.setTrackbarPos("S_low", "Trackbars", 0)
cv2.setTrackbarPos("V_low", "Trackbars", 0)
cv2.setTrackbarPos("H_high", "Trackbars", 255)
cv2.setTrackbarPos("S_high", "Trackbars", 255)
cv2.setTrackbarPos("V_high", "Trackbars", 255) 

cap = cv2.VideoCapture(1)

saved_thresholds = {}

while True:
    ret, frame = cap.read()
    if not ret:
        break

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    current_color = colors[cv2.getTrackbarPos("Color", "Trackbars")]

    # Get current slider values
    low = (
        cv2.getTrackbarPos("H_low", "Trackbars"),
        cv2.getTrackbarPos("S_low", "Trackbars"),
        cv2.getTrackbarPos("V_low", "Trackbars")
    )
    high = (
        cv2.getTrackbarPos("H_high", "Trackbars"),
        cv2.getTrackbarPos("S_high", "Trackbars"),
        cv2.getTrackbarPos("V_high", "Trackbars")
    )

    mask = cv2.inRange(hsv, np.array(low), np.array(high))  # create mask and apply to frame/display it
    result = cv2.bitwise_and(frame, frame, mask=mask)

    combined = np.hstack([frame, result])
    cv2.putText(combined, f"Current: {current_color}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)
    cv2.imshow("View", combined)

    key = cv2.waitKey(1)

    if key == ord('s'): # saves threshold for current color
        saved_thresholds[current_color] = (*low, *high)
        print(f"Saved: {current_color} -> {saved_thresholds[current_color]}")

    elif key == ord('w'): # writes all saved thresholds to a file
        with open("thresholds.txt", "w") as f:
            for color, values in saved_thresholds.items():
                f.write(f"{color}:{','.join(map(str, values))}\n")
        print("saved to thresholds.txt")

    elif key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
