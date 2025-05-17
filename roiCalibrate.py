import cv2

drawing = False
ix, iy = -1, -1
current_roi = 1
rois = {1: None, 2: None}

def draw_square(event, x, y, flags, param):
    global ix, iy, drawing, rois, current_roi, img_copy

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix, iy = x, y

    elif event == cv2.EVENT_MOUSEMOVE and drawing:
        img_copy = img.copy()
        side = min(abs(x - ix), abs(y - iy))
        x_end = ix + side if x > ix else ix - side
        y_end = iy + side if y > iy else iy - side
        cv2.rectangle(img_copy, (ix, iy), (x_end, y_end), (0, 255, 0), 2)
        cv2.imshow("Draw ROI", img_copy)

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        side = min(abs(x - ix), abs(y - iy))
        x_start = min(ix, ix + side if x > ix else ix - side)
        y_start = min(iy, iy + side if y > iy else iy - side)
        rois[current_roi] = (x_start, y_start, side)
        print(f"ROI {current_roi} set to: {rois[current_roi]}")
        redraw_rois()

def redraw_rois():
    global img_copy
    img_copy = img.copy()
    for i in [1, 2]:
        if rois[i]:
            x, y, s = rois[i]
            color = (0, 255, 0) if i == 1 else (255, 0, 0)
            cv2.rectangle(img_copy, (x, y), (x + s, y + s), color, 2)
    cv2.imshow("Draw ROI", img_copy)

# Grab a single frame from the webcam
cap = cv2.VideoCapture(1)
cv2.waitKey(5000) # Wait for the camera to warm up
ret, img = cap.read()
cap.release()

if not ret:
    print("Failed to grab frame from camera.")
    exit()

img_copy = img.copy()
cv2.namedWindow("Draw ROI")
cv2.setMouseCallback("Draw ROI", draw_square)

print("Instructions:")
print(" - Click and drag to draw a square ROI")
print(" - Press '1' or '2' to select which ROI")
print(" - Press 's' to save to rois.txt")
print(" - Press 'q' to quit without saving")

while True:
    cv2.imshow("Draw ROI", img_copy)
    key = cv2.waitKey(1) & 0xFF

    if key == ord('1'):
        current_roi = 1
        print("Editing ROI 1")
    elif key == ord('2'):
        current_roi = 2
        print("Editing ROI 2")
    elif key == ord('s'):
        with open("rois.txt", "w") as f:
            for i in [1, 2]:
                if rois[i]:
                    x, y, s = rois[i]
                    f.write(f"ROI{i}: {x},{y},{s}\n")
        print("ROIs saved to rois.txt")
        break
    elif key == ord('q'):
        print("Quit without saving.")
        break

cv2.destroyAllWindows()