import serial # add Serial library for Serial communication
import time


Arduino_Serial = serial.Serial('com3',9600) #Create Serial port object called arduinoSerialData
#print Arduino_Serial.readline() #read the serial data and print it as line
def motorForward():
    Arduino_Serial.write(str.encode('y'))
    print("Turn motor forwards")

def motorBackward():
    Arduino_Serial.write(str.encode('n'))
    print("Turn motor backwards")

def motorStop():
    Arduino_Serial.write(str.encode('s'))
    print("Turn motor off")

motorForward()
movingForward = True
while (True):

    # Capture frame-by-frame
    ret, frame = cap.read()
  
    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    avg_brightness = np.mean(gray)
    print(avg_brightness)
    if (avg_brightness >= threshold):
        if (movingForward):
            movingForward = False
            motorStop()
    elif (movingForward == False):
        movingForward = True
        motorForward()

    #motorForward()
    #time.sleep(2)
    #motorBackward()
    #time.sleep(1/30)