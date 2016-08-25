# buttonFlash
Program by @winkleink
MIT Licence
Use as you wish. No gurantee you won't be disgusted by the code or it's performance.
Correction: chances are if you can code then you will be disgusted by the code.

Game where you press the buttons to turn off the ligts.  Do it in the fastest time possible.

Used NRF24L01 wireless communication between the Raspberry Pi which acts as the master and Arduino Nanos that are the slaves and control the buttons.

# To run the game: 
Make sure all files are in the same folder.
From the folder type 'sudo python3 buttonFlash.py'
I've used a font I downloaded from the internet called VideoPhreak. 
YOu can get it from http://www.1001freefonts.com/computer-fonts.php
Alternatively you can use any other font you wish.

# In game there are a couple of keyboard buttons for the Pi
[t] - run test mode where all buttons will flash 5 times
[return] - play the game
[p] - say the numbers during the game
[s] - stop saying the numbers during the game

Winner is the person with the lowest time to press the required number of buttons.

In the code there are a few variables that can be changed to modify the game.
I've tried to group these near the top of the code so it's easy to find then and change them

# Change these to change the game
pause = 10 # how long to wait for a button to be pressed - if bad signal the game will go onto the next random button 

numberOfNodes =2 # number of buttons in your game.  The code can handle up to 10 without modification but you don't have to have 10.

sayNumbers = 0 - This is the variable changed with [p] and [s]

gamelen = 5 # number of button presses in a game 

# Technical stuff

For my sanity and shortness I'm going to call each Arduino/Button a node.

The NRF24L01 is a wireless 2.4GHz transiever. That means it can transmit and receive signals.  It's is not wifi, but something else.
In this arrangement the Raspberry Pi controls the show and the Arduino are for the most part just responding.
Each node has a unique ID "1P", "2P", "3P"...  These could be anything but keeping them consistent in format makes it easier to understand and extend.

# TEST
In test mode all nodes recieve 'TEST' and flash their LEDs 5 times.
Node 1 is special as in Test mode it sends a message back to say the test is completed.
The Raspberry Pi received this and goes back to the menu mode where you can start a new game.

# GAME
All the nodes wait for their ID to be sent by the Raspberry Pi then they change from listening, lights it's button.
When the button is pressed it send back a message and changes back to listening mode. When the message is received by the Raspberry Pi it picks a new random node and sends it a message to start it all off again. 

There is more details on the wiring with pictures and a video on the blog post.
http://www.winkleink.com/2016/08/buttonflash-game-made-with-raspberry-pi.html


