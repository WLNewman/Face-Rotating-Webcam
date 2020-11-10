from gpiozero import OutputDevice as stepper
from gpiozero.pins.pigpio import PiGPIOFactory
import face_recognition as fr
import pigpio
import cv2

#THIS IS AN OLDER VERSION THAT IS VERY, VERY SLOW. SEE OTHER TWO
#INCLUDED FILES FOR THE REAL STUFF AND README FOR INSTRUCTION

pi = pigpio.pi('PI IP ADDRESS', 8888)
if not pi.connected:
	print('Could not connect to Pi.')
factory = PiGPIOFactory('PI IP ADDRESS')

FRAME_THICKNESS = 3

encodings = []
locations = []

#set () to 1 so it would use external webcam
video_capture = cv2.VideoCapture(1)

#horizontal motor
step1_1 = stepper(12, pin_factory = factory)
step1_2 = stepper(16, pin_factory = factory)
step1_3 = stepper(20, pin_factory = factory)
step1_4 = stepper(21, pin_factory = factory)
step1 = (step1_1, step1_2, step1_3, step1_4)

stepping =  [[1,1,0,0],
             [0,1,1,0],
             [0,0,1,1],
             [1,0,0,1]]


def rotate(num):
	#rotates motor; positive for counterclockwise
	loopCtrl = 20
	stepCounter= 0
	stepPins = step1
	
	while loopCtrl > 0:
		for pin in range(0,4):
		    thisPin = stepPins[pin]         
		    if stepping[stepCounter][pin] != 0:
		    	thisPin.on()
		    else:
		    	thisPin.off()
		stepCounter += num
		if (stepCounter >= len(stepping) - 1):
			stepCounter = 0
		if (stepCounter < 0):
			stepCounter = len(stepping) + num
		loopCtrl -= 1

pseudoFrameCount = 0

while True:
	ret, frame = video_capture.read()     

	if pseudoFrameCount % 50 == 0:

		locations = fr.face_locations(frame, model='hog')
		#set hog to cnn if your computer is beefy
		encodings = fr.face_encodings(frame, locations)


		for encoding in range(len(encodings)):
			#find all faces
			if locations[encoding][3] < 200:
				rotate(-1)
			elif locations[encoding][1] > 500:
				rotate(1)

			center = ((locations[encoding][3]  + locations[encoding][1] )//2, (locations[encoding][0]  + locations[encoding][2] )//2)
			color = [0, 255, 0]
			cv2.circle(frame, center, 50, color, FRAME_THICKNESS)

	cv2.imshow('Video', frame)			
	if cv2.waitKey(1) & 0xFF == ord('q'):
		breakq

	pseudoFrameCount += 1


video_capture.release()
cv2.destroyAllWindows()
