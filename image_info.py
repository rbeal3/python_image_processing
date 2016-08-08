import numpy as np
import cv2 as cv
import os
import sys

print "openCV version" + cv.__version__
print os.getcwd()


flags = [i for i in dir(cv) if 'max' in i or 'MAX' in i]
print flags

## main()
##locate_hsv_object()

#img = cv.imread('0.jpg',cv.IMREAD_COLOR)
#numbers = [ int(x) for x in numbers ]


#for each image
for file_num in [str(x) for x in range(0,7)]:
#cap = cv.VideoCapture(0)
#while(1):
		#_wtf, frame = cap.read()
    print "File:" + file_num + ".jpg"
    frame = cv.imread(file_num+'.jpg',cv.IMREAD_COLOR)

    #show just the red pixels

    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV) #Convert the captured frame from BGR to HSV
    lower_red = np.array([165,100,100])
    upper_red = np.array([180,255,255])
    # Threshold the HSV image to get only red colors
    mask = cv.inRange(hsv, lower_red, upper_red)

    kernel = np.ones((5,5),np.uint8)
    eroded_mask = cv.dilate(mask,kernel,iterations=3)
    #DEBUG#cv.imshow('eroded_mask', eroded_mask)
    
    #################################################

    x, y = frame.shape[:2]

    print "frame.shape="
    print frame.shape
    print x, y

    # Set tracking to start at center
    track_window = (0,0,x,y)
    print track_window

    # Bitwise-AND mask and original image
    #res = cv.bitwise_and(img,img, mask= mask)
    #cv.imshow('res',res)

    roi_hist = cv.calcHist([hsv],[0],mask,[180],[0,180])
    cv.normalize(roi_hist, roi_hist, 0, 255, cv.NORM_MINMAX)
    cv.imshow('histogram', roi_hist)

    # Setup the termination criteria, either 10 iteration or move by atleast 1 pt
    term_crit = ( cv.TERM_CRITERIA_EPS | cv.TERM_CRITERIA_COUNT, 1, 1 )

		#loop around Camshift until I am satisfied (esc) 
		#keys pressed other than escape will be the file's save name
    sys.stdout.flush()
    while(1):
    #for 10 iterations

        dst = cv.calcBackProject([hsv], [0], roi_hist, [0,180], 1)
        #dst = cv.calcBackProject([mask], [0], roi_hist,[0,180], 1)

        # apply meanshift to get the new location
        ret, track_window = cv.CamShift(dst, track_window, term_crit)
        tw= track_window
        
        cv.imshow('camshift Sees this:', dst[tw[1]:tw[1]+tw[3], tw[0]:tw[0]+tw[2]])
        # for averages we want x1+x2/2, = tw[1]+tw[1]+tw[3]/2 = 2*tw[1]+tw[3]/2 = tw1+tw3,
        print "track_window (x,w,y,h) = "
        print track_window
        print "ret= "
        print ret
        #print tw[0]=y2, tw[1]=x2, tw[2]=h, tw[3]=w

        # Draw it on image
        pts = cv.boxPoints(ret)
        pts = np.int0(pts)
        img2 = cv.polylines(frame, [pts], True, 255, 2)
        #cv.imshow('backProp_histogram', dst)
        #cv.imshow('track', track_window)
        cv.imshow('mask', mask[tw[1]:tw[1]+tw[3], tw[0]:tw[0]+tw[2]])

		#calculate vector
        average_center_object = [tw[1]+tw[3], tw[0]+tw[2]]


        sys.stdout.flush()
        k = cv.waitKey() 
        if k == 27:   # wait for ESC key to exit
            break
        else:
            #print k
            cv.imwrite(chr(k)+file_num+".jpg",img2)
cv.destroyAllWindows()
