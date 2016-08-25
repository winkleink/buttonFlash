import RPi.GPIO as GPIO
from lib_nrf24 import NRF24
import time
import spidev
from random import randint
import pygame 
import os


# get current working directory
curDir= os.getcwd() +"/"


# Change these to change the game
pause = 10 # how long to wait for a button to be pressed
numberOfNodes =2 # number of buttons
sayNumbers = 0
gamelen = 20 # number of button presses in a game

ready = "readysteadygoeffect.ogg"
countdown = ["one.ogg", "two.ogg", "three.ogg", "four.ogg", "five.ogg", "six.ogg", "seven.ogg", "eight.ogg", "nine.ogg", "ten.ogg"]

pygame.init()
pygame.font.init()
pygame.mixer.init()
pygame.mixer.get_init


window = pygame.display.set_mode((600, 400),)
pygame.display.set_caption("Button Flash")

# print(pygame.font.get_fonts())

#textfont = pygame.font.SysFont("moonspace",100)
textfont = pygame.font.SysFont("videophreak",75)
window.fill((255,255,255))
pygame.display.update()


# print("playing sound")
soundPlay = pygame.mixer.Sound(curDir+"readysteadygoeffect.ogg")
soundPlay.set_volume(1)
# soundPlay.play()

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

pipes = [[0xE8, 0xE8, 0xF0, 0xF0, 0xE1], [0xF0, 0xF0, 0xF0, 0xF0, 0xE1]]

nodes = ["1P", "2P", "3P", "4P", "5P", "6P", "7P", "8P", "9P", "10P"]
radio = NRF24(GPIO, spidev.SpiDev())
radio.begin (0, 17)  # CE0 value 0 is GPIO 8  CE Value - GPIO 17

radio.setPayloadSize(32)
radio.setChannel(0x76)
radio.setDataRate(NRF24.BR_1MBPS)
radio.setPALevel(NRF24.PA_MAX)

radio.setAutoAck(True)
radio.enableDynamicPayloads()
radio.enableAckPayload()

radio.openWritingPipe(pipes[0])
radio.openReadingPipe(1,pipes[1])
radio.printDetails()
#radio.startListening()
time.sleep(1)

# message = list("3P")
# while len(message) <32:
#     message.append(0)



nodeNumber = 0 # which node to turn on
do = 0 # wait for a button to be pressed to decided if test or play
play = 0 # actually play the game (either test or game)
gamestartime = 0 # start of game in seconds
gameendtime = 0 # end of game in seconds
highscore = 0.0
score = 0.0

while True:
    pygame.event.clear

    highscoretext = textfont.render("High Score: ", 1, (255,0,0))
    highscoreresult = textfont.render(str(highscore), 1, (255,0,0))    
    scoretext = textfont.render("Your Score: ", 1, (0,0,0))
    scoreresult = textfont.render(str(score), 1, (0,0,0))    

    window.fill((255,255,255))
    window.blit(highscoretext, (20,10))
    window.blit(highscoreresult, (20,90))

    window.blit(scoretext, (20,200))
    window.blit(scoreresult, (20,280))
    pygame.display.update()
    
    print ("t for test \n\r[return] to play\n\r")
    while  (do == 0):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_t:
                    do = 1
                    play = 2
                    steps = 1
                    print("Test Mode")
                    message = list("TEST")
                    soundPlay = pygame.mixer.Sound(curDir+"testmode.ogg")
                    soundPlay.play()
                    
                    
                if event.key == pygame.K_p:
                    print("Say Numbers")
                    sayNumbers = 1
                if event.key == pygame.K_s:
                    print("Do Not Say Number")
                    sayNumbers = 0
                    
                if event.key == pygame.K_RETURN:
                    do = 1
                    play = 1
                    steps = gamelen
                    print("Starting Game")
                    soundPlay = pygame.mixer.Sound(curDir+"readysteadygoeffect.ogg")
                    soundPlay.play()
                    time.sleep(5)

                    
    pygame.event.clear
    gamestartime = time.time()
    print ("gamestarttime is "+str(gamestartime))
    if play == 1:
        playtext = textfont.render("PLAY !", 1, (0,0,192)) 
    else:
        playtext = textfont.render("TEST !", 1, (0,0,192)) 

    window.fill((255,255,255))
    window.blit(playtext, (200,150))
    pygame.display.update()


    
    
    
    
    for x in range(0,steps):
        print("Round "+str(x+1))
        
        if play == 1:
            newnodeNumber=randint(0,numberOfNodes-1)
            while (newnodeNumber == nodeNumber):
                newnodeNumber=randint(0,numberOfNodes-1)
                print("boo picked the same one again nodenumber"+str(nodeNumber)+" | newnodenumber "+str(newnodeNumber)+"\n\r")
            nodeNumber = newnodeNumber
            message = list(nodes[nodeNumber])
            if sayNumbers == 1:
                soundPlay = pygame.mixer.Sound(curDir+countdown[nodeNumber])
                soundPlay.play()


        print(message)
        while len(message) <32:
            message.append(0)
    
        start = time.time()
        radio.write(message)
        print("sent the message: {}".format(message))
        radio.startListening()


        while not radio.available(0):
            time.sleep(1/100)
            if time.time() - start > pause:
                print("Timed out.")
                break

        receivedMessage = []
        radio.read(receivedMessage, radio.getDynamicPayloadSize())
        print ("Received: {}".format(receivedMessage))

        print("Translating our received message into unicode characters...")
        string = ""

        for n in receivedMessage:
            if (n >=32 and n <= 126):
                string += chr(n)
        print("Our received message decodes to: {}".format(string))

        radio.stopListening()
        time.sleep(0.5)
        if (do == 2):
            time.sleep(3)
            
        if play == 1:
            playtext = textfont.render("PLAY ! " + str(x+1), 1, (0,0,192)) 
        else:
            playtext = textfont.render("TEST !", 1, (0,0,192)) 

        window.fill((255,255,255))
        window.blit(playtext, (150,150))
        pygame.display.update()

                   
                                   
    gameendtime = time.time()
    print ("raw score: " + str(gameendtime-gamestartime))
    score = (int((gameendtime-gamestartime)*100)/100)+0.0
    
    print ("\r\nYour score is: "+ str(score)+"\r\n")
    if play ==1:
        soundPlay = pygame.mixer.Sound("/home/pi/buttonFlash/gameover.ogg")
        soundPlay.play()
        time.sleep(2)
        if score < highscore or highscore == 0:
            soundPlay = pygame.mixer.Sound("/home/pi/buttonFlash/newhighscore.ogg")
            soundPlay.play()
            time.sleep(2)
            highscore = score
    
        highscoretext = textfont.render("High Score: ", 1, (255,0,0))
        highscoreresult = textfont.render(str(highscore), 1, (255,0,0))    
        scoretext = textfont.render("Your Score: ", 1, (0,0,0))
        scoreresult = textfont.render(str(score), 1, (0,0,0))    

        window.fill((255,255,255))
        window.blit(highscoretext, (20,10))
        window.blit(highscoreresult, (20,90))

        window.blit(scoretext, (20,200))
        window.blit(scoreresult, (20,280))
        pygame.display.update()
    else:
        score = 0
	
    do = 0
    play = 0
    

