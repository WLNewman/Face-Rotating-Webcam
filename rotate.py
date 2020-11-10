from gpiozero import OutputDevice as stepper
import time

#horizontal motor
step1_1 = stepper(12)
step1_2 = stepper(16)
step1_3 = stepper(20)
step1_4 = stepper(21)
step1 = (step1_1, step1_2, step1_3, step1_4)

stepping =  [[1,1,0,0],
             [0,1,1,0],
             [0,0,1,1],
             [1,0,0,1]]

busy = False

def rotate(num):
        #rotates motor; positive for counterclockwise
        busy = True
        loopCtrl = 200
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
                if (stepCounter >= len(stepping)):
                        stepCounter = 0
                if (stepCounter < 0):
                        stepCounter = len(stepping) + num
                loopCtrl -= 1
                time.sleep(0.01)
        busy = False

def checkState(num):
        #checks if Pi is already rotating
        if busy:
                pass
        else:
                rotate(num)


checkState(1)



