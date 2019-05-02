import numpy as np
import cv2

def show_classification(cv2, frame):
    classes = ['Assault', 'Burglary', 'Shooting', 'Robbery', 'Normal']
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    font                   = cv2.FONT_HERSHEY_SIMPLEX
    bottomLeftCornerOfText = (0,20)
    fontScale              = 0.5
    fontColor              = (0,255,0)
    lineType               = 1
    ypos = 0
    for klass in classes:
        ypos += 20
        cv2.putText(frame, klass, 
            (0, ypos), 
            font, 
            fontScale,
            fontColor,
            lineType)
    return


VID_FILE = 'Shooting050_x264.mp4'
#cap = cv2.VideoCapture(VID_FILE)
cap = cv2.VideoCapture(0)
ret1, frame1 = cap.read()
optical_flow = cv2.DualTVL1OpticalFlow_create()
prvs = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
hsv = np.zeros_like(frame1)
hsv[...,1] = 255


while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    # show_classification(cv2, frame)
    # Our operations on the frame come here
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # if prvs is not None:
    #     flow = optical_flow.calc(prvs, frame, None)
    #     mag, ang = cv2.cartToPolar(flow[...,0], flow[...,1])
    #     hsv[...,0] = ang*180/np.pi/2
    #     hsv[...,2] = cv2.normalize(mag,None,0,255,cv2.NORM_MINMAX)
    #     bgr = cv2.cvtColor(hsv,cv2.COLOR_HSV2BGR)
    #     #cv.imshow('frame2',bgr)
    #     cv2.imshow('Video',bgr)
    # prvs = frame
    cv2.imshow('Video',frame)
    # Display the resulting frame
    # cv2.rectangle(frame, (0, 0), (100, 100), (0, 255, 0), 2)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
