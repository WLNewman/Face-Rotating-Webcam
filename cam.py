from gpiozero import OutputDevice as stepper
import face_recognition as fr
import pigpio
import cv2
import os

os.environ["PIGPIO_ADDR"] = "INSERT YOUR PI'S IP ADDRESS HERE"                            
os.environ["GPIOZERO_PIN_FACTORY"] = "pigpio"

FRAME_THICKNESS = 3

me = fr.load_image_file("myFace5.jpg") #THIS FILE WILL BE YOUR FACE
known = [fr.face_encodings(me)[0]]
encodings = []
locations = []
#set () to 1 so it would use external webcam
video_capture = cv2.VideoCapture(1)

#horizontal motor     REMEMBER THESE ARE THE BCM NUMBERING SYSTEM
step1_1 = stepper(12)
step1_2 = stepper(16)
step1_3 = stepper(20)
step1_4 = stepper(21)
step1 = (step1_1, step1_2, step1_3, step1_4)

#vertical motor
step2_1 = stepper(5)
step2_2 = stepper(6)
step2_3 = stepper(13)
step2_4 = stepper(19)
step2 = (step2_1, step2_2, step2_3, step2_4)

stepping =  [[1,0,0,1],
             [1,0,0,0], 
             [1,1,0,0],
             [0,1,0,0],
             [0,1,1,0],
             [0,0,1,0],
             [0,0,1,1],
             [0,0,0,1]]


def rotate(num, vert=False):
	#swivel left and right (up and down if vert) +num for forwards
	loopCtrl = 20
	stepCounter= 0
	if vert:
		stepPins = step2
	else:
		stepPins = step1
	
	while loopCtrl > 0:
		for pin in range(0,4):
		    thisPin = stepPins[pin]         
		    if stepping[stepCounter][pin] != 0:
		      thisPin.on()
		stepCounter += num
		if (stepCounter >= len(stepping) - 1):
			stepCounter = 0
		if (stepCounter < 0):
			stepCounter = len(stepping) + num
		loopCtrl -= 1


while True:
	ret, frame = video_capture.read()     

	locations = fr.face_locations(frame, model='hog')
	#set hog to cnn if your computer is beefy
	encodings = fr.face_encodings(frame, locations)

	for encoding in range(len(encodings)):
		#find all faces
		result = fr.compare_faces(known, encodings[encoding], tolerance=0.1)
		if result:
			if locations[encoding][0] < 50:
				rotate(-1, True)
				print('up')
			elif locations[encoding][2] > 440:
				rotate(1, True)
				print('down')
			if locations[encoding][3] < 100:
				rotate(-1)
				print('left')
			elif locations[encoding][1] > 570:
				rotate(1)
				print('right')
			
			center = ((locations[encoding][3]  + locations[encoding][1] )//2, (locations[encoding][0]  + locations[encoding][2] )//2)
			color = [0, 255, 0]
			cv2.circle(frame, center, 50, color, FRAME_THICKNESS)
	
	cv2.imshow('Video', frame)			
	
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

video_capture.release()
cv2.destroyAllWindows()
