# Import the required modules
import dlib
import cv2
import argparse as ap
import darknet

net = darknet.load_net("yolov3.cfg", "yolov3.weights", 0)
meta = darknet.load_meta("coco.data")
points = []
fourcc = cv2.VideoWriter_fourcc(*'mp4v') # Be sure to use lower case
#ret, frame = vs.read()	
out = cv2.VideoWriter('output_videos/result.mp4', fourcc, 20.0, (1280, 720))

def run(source=0, dispLoc=True):
	# Create the VideoCapture object
	cam = cv2.VideoCapture(source)

	# If Camera Device is not opened, exit the program
	if not cam.isOpened():
		print "Video device or file couldn't be opened"
		exit()

	ret, frame = cam.read()
	points = darknet.detect(net,meta,frame)
	#points = [(int(points[0][2][0]), int(points[0][2][1]), int(points[0][2][2]), int(points[0][2][3]))] 
	new_points = []
	if(len(points)!=0):
		i = 0
		for p in points:
			if(i == 4):
				break
			else:
				i+=1
			x = p[2][0]
			y = p[2][1]
			w = p[2][2]
			h = p[2][3]
			new_points.append((int(x-0.5*w),int(y-0.5*h),int(x+0.5*w),int(y+0.5*h)))
			
	while not new_points:
		#print 'Yes'
		# Retrieve an image and Display it.
		for i in range(5):
			ret, frame = cam.read()
			if not ret:
				print "Cannot capture frame device"
				exit()
		r = darknet.detect(net,meta,frame)
		if(len(r)!=0):
			j = 0
			for p in r:
				if(j == 3):
					break
				else:
					j+=1
				x = p[2][0]
				y = p[2][1]
				w = p[2][2]
				h = p[2][3]
				new_points.append((int(x-0.5*w),int(y-0.5*h),int(x+0.5*w),int(y+0.5*h)))

	#print 'P: ', new_points
	#print len(new_points)
	tracker = [dlib.correlation_tracker() for _ in xrange(len(new_points))]
	# Provide the tracker the initial position of the object
	[tracker[i].start_track(frame, dlib.rectangle(*rect)) for i, rect in enumerate(new_points)]

	while True:
		# Read frame from device or file
		ret, img = cam.read()
		
		if not ret:
			print "Cannot capture frame | CODE TERMINATION :( "
			exit()

		height, width = img.shape[:2]

		for i in xrange(len(tracker)):
			tracker[i].update(img)

			rect = tracker[i].get_position()
			pt1 = (int(rect.left()), int(rect.top()))
			pt2 = (int(rect.right()), int(rect.bottom()))

			if pt1[0]>1000:
				continue
			if pt1[0]<0 or pt1[1]<0 or pt2[0]>width or pt2[1]>height:
				continue

			cv2.rectangle(img, pt1, pt2, (0, 0, 255), 3)
			print "Object {} tracked at [{}, {}] \r".format(i, pt1, pt2),
			if dispLoc:
				loc = (int(rect.left()), int(rect.top()-20))
			txt = "Object tracked at [{}, {}]".format(pt1, pt2)
			cv2.putText(img, txt, loc , cv2.FONT_HERSHEY_SIMPLEX, .5, (255,255,255), 1)
		cv2.namedWindow("Image", cv2.WINDOW_NORMAL)
		cv2.imshow("Image", img)
		out.write(img) # Write out frame to video
		# Continue until the user presses ESC key
		if cv2.waitKey(1) == 27:
			break

	# Relase the VideoCapture object
	cam.release()
	out.release()

if __name__ == "__main__":
	# Parse command line arguments
	parser = ap.ArgumentParser()
	group = parser.add_mutually_exclusive_group(required=True)
	group.add_argument('-d', "--deviceID", help="Device ID")
	group.add_argument('-v', "--videoFile", help="Path to Video File")
	parser.add_argument('-l', "--dispLoc", dest="dispLoc", action="store_true")
	args = vars(parser.parse_args())

	# Get the source of video
	if args["videoFile"]:
		source = args["videoFile"]
	else:
		source = int(args["deviceID"])
	run(source, args["dispLoc"])
