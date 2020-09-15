# Face-Rotating-Webcam
A webcam which uses a Raspberry Pi to rotate when your face moves to the peripherals

Okay, if you want to make this yourself (especially if you're using Windows), here's some tips

-face_recognition would never pip install for me. I can't find it again but there's
 a conda page where a guy made a version for Windows. Command was something like
 'conda install [person's name] face_recognition'

-we're going to be interfacing with a raspberry pi wirelessly. To do this, you have
 to enable remote GPIO on your Pi and initialize a communication daemon. Look below for tips
  >https://gpiozero.readthedocs.io/en/stable/remote_gpio.html
  >https://gist.github.com/bennuttall/572789b0aa5fc2e7c05c7ada1bdc813e (this is how I connected on Windows)
  
-face_recognition has several models. 'cnn' is better performing, but only if you have a GPU. I don't,
 so I've set my code example to the 'hog' model. Feel free to do what you like.
