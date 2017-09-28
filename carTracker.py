import numpy as np
import cv2 as cv
import os
import sys
import functions as f
"""
Author:
	Ryan Beal
Purpose:
	This code finds an object by color using a color mask and a camshift.

	It finds the center point of the mask
	and calculates the distance between the 
	current frame and the previous frame

	draws a line that represents magnitude of the movement in a direction (drawn from center of screen).

	draws a line at the center of the screen equal to the magnitude of the movement in that direction.

Arguments:
	color: you are looking for 
		default: racecar red
	pctErr: percent error of the estimated color
		default: 10%
	
"""
print "Python Version:" + sys.version
print "OpenCV Version" + cv.__version__
print os.getcwd()

def find_object_by_color(color= 172, pctErr=.1):
  aoLocList = [(0,0)] #average object location list
  
  #for each image
  for file_num in [str(x) for x in range(0,7)]:
  
  #cap = cv.VideoCapture(0)
  #while(1):
  		#_wtf, frame = cap.read()
      print "File:" + file_num + ".jpg"
      frame = cv.imread(file_num+'.jpg',cv.IMREAD_COLOR)
  
      print "frame.shape=", frame.shape
      frame_y, frame_x = frame.shape[:2]
  
  		#set the default first average object location to the middle of the screen
      aoLocList[0] = (frame_x/2,frame_y/2)
  
      hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV) #Convert the captured frame from BGR to HSV
  
      # Threshold the HSV image to get only red colors
      #lower_red = np.array([165,100,100]) #RGB
      #upper_red = np.array([180,255,255])
      # Threshold the HSV image to be within 10% of the requested 
      lower_red = np.array([color*(1-pctErr),100,100]) #RGB
      upper_red = np.array([color*(1+pctErr),255,255])
      mask = cv.inRange(hsv, lower_red, upper_red)
  
      kernel = np.ones((5,5),np.uint8)
      eroded_mask = cv.dilate(mask,kernel,iterations=3)
      #DEBUG#cv.imshow('eroded_mask', eroded_mask)
  
      # Set tracking to start with the full frame
      track_window = (0,0,frame_x,frame_y)
      print track_window
  
      # Bitwise-AND mask and original image
      #res = cv.bitwise_and(img,img, mask= mask)
      #cv.imshow('res',res)
  
      # Setup the termination criteria, either 10 iteration or move by atleast 1 pt
      term_crit = ( cv.TERM_CRITERIA_EPS | cv.TERM_CRITERIA_COUNT, 10, 1 )
  
      sys.stdout.flush()
      #Run camshift x times and draw the box
      # apply meanshift to get the new location
      # camshift returns tw[0]=y, tw[1]=x, tw[2]=h, tw[3]=w
      ret, track_window = cv.CamShift(mask, track_window, term_crit)
      tw= track_window
      
      # for averages we want x1+x2/2, = tw[1]+tw[1]+tw[3]/2 = 2*tw[1]+tw[3]/2 = tw1+tw3,
      #print "track_window (x,w,y,h) = ", track_window #DEBUG#
  
      # Draw it on image
      pts = cv.boxPoints(ret)
      pts = np.int0(pts)
      img = cv.polylines(frame, [pts], True, 255, 2)
      #cv.imshow('track', track_window)
  
  		#calculate vector for each frame after camshift
      #aoLocList.append ((tw[1]+tw[3]/2, tw[0]+tw[2]/2))
      aoLocList.append ((tw[0]+tw[2]/2, tw[1]+tw[3]/2))
      
      #object_vector = (aoLocList[-2][0] - aoLocList[-1][0], aoLocList[-2][1] - aoLocList[-1][1])
      object_loc = aoLocList[-1]
      prev_object_loc = aoLocList[-2] 
      object_vector = [object_loc[i] - prev_object_loc[i] for i in range(len(object_loc))]
  
      print "aoLocList", aoLocList
      print "object_vector", object_vector
      print frame_x, frame_y
  		#draw_arrow not working vector line
  		#draw arrow from middle representing magnitude and direction
      f.draw_arrow(img, (frame_x/2, frame_y/2) , (object_vector[0] - frame_x/2, object_vector[1] - frame_y/2))
  		#draw line from previous center to current center
      cv.line(img, (prev_object_loc), (object_loc), (200,10,40), 3)
      print "draw line at:", (frame_x/2, frame_y/2) , object_vector
      #img = cv.line(img, (x/2, y/2), object_vector, (60,20,200))
  
      #cv.imshow('frame', frame[tw[1]:tw[1]+tw[3], tw[0]:tw[0]+tw[2]])
      cv.imwrite(os.path.join('image_results',"t_camShift" + file_num + ".jpg"), img)
      cv.imwrite(os.path.join('image_results',"t_mask" + file_num + ".jpg"), eroded_mask)
  
    #I would love to learn more about this method and what I'm doing wrong 
    #roi_hist = cv.calcHist([hsv],[0],eroded_mask,[180],[10,160])
    #cv.normalize(roi_hist, roi_hist, 0, 255, cv.NORM_MINMAX)
    #dst = cv.calcBackProject([hsv], [0], roi_hist, [20,180], 1)
    #cv.imwrite(os.path.join('image_results',"t_BackProp" + file_num + ".jpg"), dst)
  
      print "image saved test_" + file_num + ".jpg"
  
      sys.stdout.flush()
      #pause 
      #k = cv.waitKey() 
      #if k == 27:   # wait for ESC key to exit any other key continues operation
      #    break
  cv.destroyAllWindows()
  
  #defined functions ################################################
