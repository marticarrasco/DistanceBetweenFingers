from HandTrackingModule import HandDetector
import cv2
import serial

cap = cv2.VideoCapture(0)
detector = HandDetector(detectionCon=0.8, maxHands=1)

arduino = serial.Serial(port='/dev/cu.usbmodem14101', baudrate=9600, timeout=.1)

while True:
    success, img = cap.read()
    hands, img = detector.findHands(img) 
   

    if hands:
        hand1 = hands[0]
        lmList1 = hand1["lmList"]  
        bbox1 = hand1["bbox"]  
        centerPoint1 = hand1['center']
        handType1 = hand1["type"]

        fingers1 = detector.fingersUp(hand1)

        length, info, img = detector.findDistance(lmList1[4], lmList1[8], img)  

        if ((length - 20) < 0):
            length = 0
        else:
            length = (length - 20) * (255/180)

        if (length > 255):
            length = 255

        dataToSend = "$" + str(length)
        print(dataToSend)
        arduino.write(bytes(dataToSend, 'utf-8'))
    
    cv2.imshow("Image", img)
    
    if cv2.waitKey(1) & 0xFF == 27:
            break

cap.release()
cv2.destroyAllWindows()
exit()
