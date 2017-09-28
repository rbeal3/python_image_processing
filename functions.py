
def draw_arrow(image, p, q, color=(200,50,50), arrow_magnitude=9, thickness=1, line_type=8, shift=0):

  # draw arrow tail
  print "attempting to draw a line from: ", p, "to: ", q
  cv.line(image, p, q, color, thickness, line_type, shift)
  # calc angle of the arrow 
  angle = np.arctan2(p[1]-q[1], p[0]-q[0])
  # starting point of first line of arrow head 
  p = (int(q[0] + arrow_magnitude * np.cos(angle + np.pi/4)),
  int(q[1] + arrow_magnitude * np.sin(angle + np.pi/4)))
  # draw first half of arrow head
  cv.line(image, p, q, color, thickness, line_type, shift)
  # starting point of second line of arrow head 
  p = (int(q[0] + arrow_magnitude * np.cos(angle - np.pi/4)),
  int(q[1] + arrow_magnitude * np.sin(angle - np.pi/4)))
  # draw second half of arrow head
  cv.line(image, p, q, color, thickness, line_type, shift)

"""
def car.setup(pinArray):
	#forward, reverse, left right
	

def car.find():
	#in carTracker

def car.orientation():
	move car forward, and return the orientation
	car.find()
	car.move_forward()
	car.find()

def car.move_to(x,y):

#send forward message to car
def car.move_forward(ms):
	#open socket
	pin[5]=1
	wait(ms)
	pin[5]=0


"""
