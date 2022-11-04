#A Level Programming Project by  Mayur Shankar

import pygame #--Importing all the required modules
import csv
import time
import sys
import os
import matplotlib.pyplot as plt
import random
import numpy as np
from numpy.polynomial.polynomial import polyfit
pygame.init() #--Initialises pygame

#--Setting up the Tkinter window
from tkinter import*
window = Tk()
window.title("Physics Practical Animation and Quiz")#--Name of the window
window.geometry("1000x700") #--Sets the height and width of the Tkinter window
window.configure(bg="SkyBlue2") #--Sets the background colour of the window
window.resizable(False, False) #--Tkinter window is not resizable

loginTries = 0

class Format:#--Class for all the formatting that will be used throughout the program
  def __init__(self, white, black, blue, background, red, quizred, grey, green,font, bd, fontSizeLarge, fontSizeLargeQuiz, fontSizeMedium, fontSizeSmall):
    self.white = white      
    self.black = black
    self.blue = blue
    self.background = background
    self.red = red
    self.quizred = quizred
    self.grey = grey
    self.green = green
    self.font = font
    self.bd = bd
    self.fontSizeLarge = fontSizeLarge
    self.fontSizeLargeQuiz = fontSizeLargeQuiz
    self.fontSizeMedium = fontSizeMedium
    self.fontSizeSmall = fontSizeSmall

form = Format("white", "black", "medium blue", "SkyBlue2", "firebrick1", "IndianRed2" ,"grey40", "seagreen3", "Arial", 1, 20, 17,15, 13)
#--This will be expanded as needed

class Login:#--Initialising the first class that will be used for the login screen
  def __init__(self):#--Key attributes labelled
    self.credentialsList = [] #--List of all the student details to be used later
    #--Tkinter widgets
    self.welcomeText = Label(window, text="Welcome, to get started please log in", fg=form.black,bg=form.white,font=(form.font, form.fontSizeLarge))
    self.accountText = Label(window, text="Don't have an account? Create one!", fg=form.grey,bg=form.white,font=(form.font, form.fontSizeSmall))
    self.username = Label(text="Username:", fg=form.red, bg=form.white, font=(form.font, form.fontSizeMedium))
    self.password = Label(text="Password:", fg=form.blue, bg=form.white, font=(form.font, form.fontSizeMedium))
    self.entryUsername = Entry(window, bd = form.bd, font=(form.font, form.fontSizeSmall))
    self.entryPassword = Entry(window, bd = form.bd, font=(form.font, form.fontSizeSmall), show='*') #--This is where the user will enter their details
    self.submit = Button(window, text="Submit", fg=form.black, bg=form.white,font=(form.font, form.fontSizeMedium), command=self.checkCredentials)
    #--Checks the entered credentials by using the checkCredentials method
    self.createButton = Button(window, text="Create a new account", bd = form.bd, fg = form.black, bg=form.white, font=(form.font, form.fontSizeMedium),
                                                                                                                            command=self.createAccount)
    #--Program will move onto the createAccount method

    #--Widgets used for creating a new account
    self.welcomeText.grid()
    self.createText = Label(text="Please create a new account",fg=form.black,bg=form.white,font=(form.font, form.fontSizeLarge))
    self.newUsername = Label(text="New Username:", fg=form.red, bg=form.white, font=(form.font, form.fontSizeMedium))
    self.newPassword = Label(text="New Password:", fg=form.blue, bg=form.white, font=(form.font, form.fontSizeMedium))
    #---This is where the user will enter their new username and password
    self.entryNewUsername = Entry(window, bd = form.bd, font=(form.font, form.fontSizeSmall)) 
    self.entryNewPassword = Entry(window, bd = form.bd, font=(form.font, form.fontSizeSmall), show='*')
    self.submitNew = Button(window, text="Submit", fg=form.black, font=(form.font, form.fontSizeMedium), command=self.addCredentials)

    #--Text that will be displayed to cope with erroneous inputs
    self.enterText = Label(window, text="Please enter a valid username/password", fg=form.grey,bg=form.white,font=(form.font, form.fontSizeSmall))
    self.attemptText = Label(window, text="You have attempted more than 5 tries, please wait 30 seconds",
                             fg=form.grey,bg=form.white,font=(form.font, form.fontSizeSmall))
    self.retryText = Label(window, text="Wrong credentials, please try again", fg=form.grey,bg=form.white,font=(form.font, form.fontSizeSmall))

    #--Widget Positioning
    self.welcomeText.grid(row=1, columnspan=9, pady = 100, padx = 280) #--Main widget in the window
    self.accountText.grid(row=5, column=4, pady = 50)
    self.username.grid(row=3, column=3, sticky = E) #--Sticky determines which side the widget will bind to
    self.password.grid(row=4, column=3, sticky = E)
    self.entryUsername.grid(row=3, column=4) 
    self.entryPassword.grid(row=4, column=4)
    self.submit.grid(row=4, column = 5, sticky = W)
    self.createButton.grid(row=6, column = 4)

  def createAccount(self): #--Method to create a new user account
    self.accountText.grid_forget() #--Removing widgets that are no longer needed
    self.createButton.grid_forget()
    self.retryText.grid_forget()
    self.welcomeText.grid_forget()
    
    #--Positioning of widgets as per my screen designs
    self.createText.grid(row=1, columnspan=9, pady = 130, padx = 330)
    self.newUsername.grid(row=3, column=3, sticky = E)
    self.newPassword.grid(row=4, column=3, sticky = E)
    self.entryNewUsername.grid(row=3, column=4)
    self.entryNewPassword.grid(row=4, column=4)
    self.submitNew.grid(row=4, column = 5, sticky = W)
    
  def addCredentials(self): #--Appending entered credentials to a CSV file
    #--Part of validation where at least one character has to be entered to be saved
    if len(self.entryNewUsername.get()) == 0 or len(self.entryNewPassword.get()) == 0:
      self.enterText.grid(row=2, column = 4)
      self.entryNewUsername.delete(0, 'end') #--Deletes content in widgets
      self.entryNewPassword.delete(0, 'end')
      command = self.addCredentials #--Repeats Method
    else:
      rows = [[self.entryNewUsername.get(),self.entryNewPassword.get()]] #--Items that will be added
      #--Appending to the file as I want the original contents to be stored
      with open('studentCredentials.csv','a', newline='') as studentCredentials:
        writer = csv.writer(studentCredentials)
        writer.writerows(rows) #--Rows written
        self.newUsername.grid_forget()
        self.newPassword.grid_forget()
        self.enterText.grid_forget()
        self.createText.grid_forget()
        self.retryText.grid_forget()
        self.accountText.grid_forget()
        self.username.grid_forget()
        self.password.grid_forget()
        self.entryUsername.grid_forget()
        self.entryPassword.grid_forget()
        self.welcomeText.grid_forget()
        self.createButton.grid_forget()
        self.submit.grid_forget()
        self.entryNewUsername.grid_forget()
        self.entryNewPassword.grid_forget()
        self.submitNew.grid_forget()
        command = Login() #--Taking user back to main login screen
            
  def checkCredentials(self): #--Method to check the inputted details
    global loginTries #--Global variable which keeps track of how many attempts the user has had
    if loginTries > 4: #--Giving the user 5 attempts as per my success criteria
      self.retryText.grid_forget()
      self.attemptText.grid(row=2, column=4)
      second=StringVar()
      second.set("30")
      #--Timer that will be displayed
      timeEntryLabel = Label(window, text="30", width=3, bg = form.white, font=(form.font, form.fontSizeLarge,""),textvariable=second)
      timeEntryLabel.grid(row = 1, column = 3)
      self.entryUsername.delete(0, 'end') #--Deletes content in widgets
      self.entryPassword.delete(0, 'end')
      loop = 30 #--Sets the total time in seconds
      while loop >-1: #--Loop allows timer to iterate
        mins,secs = divmod(loop,60)
        second.set("{0:2d}".format(secs))
        window.update() #--Updates window as time changes
        time.sleep(1)
        if (loop == 0): 
          timeEntryLabel.grid_forget()
          self.enterText.grid_forget()
          self.attemptText.grid_forget()
          loginTries = 0 #--Resets variable so user can enter their details again
          command = self.removeWidgets #--Sends user back to the login screen
        loop -= 1

    #--Makes sure usernames and passwords with no characters cannot be entered
    if len(self.entryUsername.get()) == 0 or len(self.entryPassword.get()) == 0:
        self.retryText.grid_forget()
        self.enterText.grid(row=2, column = 4) 
            
    else:
      self.correct = False #--Attribute to determine whether access is given
      with open('studentCredentials.csv', 'r') as studentCredentials:
        reader = csv.reader(studentCredentials)
        for row in reader: #--File contents are appended as a 2d array
          self.credentialsList.append(row)

        for x in self.credentialsList: #--Goes through each array in the 2d array
          if self.entryUsername.get() in x and self.entryPassword.get() in x:
            self.accountText.grid_forget()
            self.username.grid_forget()
            self.password.grid_forget()
            self.entryUsername.grid_forget()
            self.entryPassword.grid_forget()
            self.entryNewUsername.grid_forget()
            self.entryNewPassword.grid_forget()
            self.welcomeText.grid_forget()
            self.createButton.grid_forget()
            self.submit.grid_forget()
            self.retryText.grid_forget()
            self.enterText.grid_forget()
            self.correct = True #--Sets attribute to true so access is granted
            command = ChoosePractical()
        
        if self.correct !=True:
          loginTries += 1 #--Adds one to the loginTries count
          self.credentialsList.clear()
          self.entryUsername.delete(0, 'end') #--Deletes content in widgets
          self.entryPassword.delete(0, 'end')
          self.enterText.grid_forget()
          self.retryText.grid(row = 2, column = 4)
          command = self.removeWidgets #--Sends user back to the login screen

  #--Method which removes widgets from the window when user enters wrong details
  def removeWidgets(self):
    self.retryText.grid_forget()
    self.enterText.grid_forget()
    command = Login() #--Takes user back to the login screen

class ChoosePractical:
  def __init__(self):
    #---Main heading in the window
    self.headingText = Label(window, text="Please choose a practical to view",fg=form.black,bg=form.white,font=(form.font, form.fontSizeLarge))
    self.confirm_Button2 = Button(text="Confirm?",fg=form.black, font=(form.font, form.fontSizeMedium), command = self.practical)
    #--List of options in the drop-down menu
    self.OptionList = ["Click to choose Practical:", "Determination of 'g' by a freefall method"] 
    self.menu = StringVar(window) #--Sets up a Tkinter variable
    self.menu.set(self.OptionList[0]) #--First option will be 'Choose Practical'
    self.dropDown = OptionMenu(window, self.menu, *self.OptionList)
    #--Formats and positions the drop-down menu
    self.dropDown.config(width=32, font=(form.font, form.fontSizeMedium)) 
    self.dropDown.grid(row=3, column=2)
    self.headingText.grid(row=1, columnspan=9, pady = 120, padx = 250)
    
    def change_dropdown(*args): #--Function which runs when the user clicks an option
      if self.menu.get() == "Determination of 'g' by a freefall method":
        #--Calls 'confirmButton' method
        command = self.confirmButton()
      elif self.menu.get() == "Click to choose Practical:":
        self.confirm_Button2.grid_forget()
    self.menu.trace("w", change_dropdown) #--Allows the function to be run
    
  def confirmButton(self): #--Allows the user to confirm that they want to view the practical
    self.confirm_Button2.grid(row=3, column=4)

  def practical(self): #--Instantiates the 'PracticalAnimation' class which creates a new window
    window.destroy() #--Destroys old Tkinter window
    command = PracticalAnimation()

class PracticalAttributes: #--Main class to store attributes
  def __init__(self, WHITE, GREY, BLACK, BLUE, ORANGE, PURPLE, RED, fontObj, fontObj_medium, fontObj_mediumsmall, fontObj_small):
    self.WHITE = WHITE #--Examples of colours
    self.GREY = GREY
    self.BLACK = BLACK
    self.BLUE = BLUE
    self.ORANGE = ORANGE
    self.PURPLE = PURPLE
    self.RED = RED
    self.fontObj = fontObj #--Used to set a font
    self.fontObj_medium = fontObj_medium
    self.fontObj_mediumsmall = fontObj_mediumsmall
    self.fontObj_small = fontObj_small
    self.width = 100 #--Values to set the size of shapes
    self.height = 50
    self.x_beginText = 315 #--Coordinates needed to position objects in the window
    self.y_beginText = 305
    self.x_heading = 100
    self.y_heading = 150
    self.x_beginButton = 310
    self.y_beginButton = 300
    self.m = 1000
    self.m2 = 1000
    self.condition = True #--Allows future loops to be run and broken
    self.condition2 = True
    self.condition_lightgatebutton = True
    self.condition_lightgatebutton2 = True
pract = PracticalAttributes((255,255,255),(220,220,220),(0,0,0),(57,100,240), #--Class is instantiated
                            (255,181,127),(240,0,250),(255,0,0),pygame.font.SysFont('arial', 34), pygame.font.SysFont('arial', 26),
                            pygame.font.SysFont('arial', 21),pygame.font.SysFont('arial', 20))

class Apparatus: #--Class which stores attributes for the apparatus part of the practical
  def __init__(self):
    self.time_delay = 2000 #--Time delays that will be used
    self.time_delay2 = 4000
    self.time_delay3 = 6000
    self.time_delay4 = 8000
    self.time_delay5 = 11000
    #--List of text to be rendered and displayed onscreen using attributes from the 'PracticalAttributes' class
    self.equipment_text = pract.fontObj_medium.render("This is the equipment you will need:", True, pract.BLACK, pract.WHITE) 
    self.clampStand_text = pract.fontObj_medium.render("Stand and Clamp", True, pract.BLACK, pract.WHITE)
    self.magnet_text = pract.fontObj_medium.render("Electromagnet", True, pract.BLACK, pract.WHITE)
    self.bearings_text = pract.fontObj_medium.render("Steel ball bearings", True, pract.BLACK, pract.WHITE)
    self.gates_text = pract.fontObj_medium.render("Light Gates", True, pract.BLACK, pract.WHITE)
    self.stopwatch_text = pract.fontObj_medium.render("Stopwatch", True, pract.BLACK, pract.WHITE)
    #--List of images to be projected, saved as jpg files
    self.img_clamp = pygame.image.load('Clamp Stand.jpg')
    self.img_magnet = pygame.image.load('Electromagnet.jpeg')
    self.img_bearings = pygame.image.load('Ball bearings.jpg')
    self.img_gates = pygame.image.load('Light Gates.jpg')
    self.img_stopwatch = pygame.image.load('Stopwatch.jpg')
    #--Setting the overall size of each image
    self.img_clamp = pygame.transform.scale(self.img_clamp, (150,150))
    self.img_magnet = pygame.transform.scale(self.img_magnet, (150,150))
    self.img_bearings = pygame.transform.scale(self.img_bearings, (150,150))
    self.img_gates = pygame.transform.scale(self.img_gates, (150,150))
    self.img_stopwatch = pygame.transform.scale(self.img_stopwatch, (150,150))
    #--Coordinates of the text and images that will be displayed
    self.x_apparatusHeading = 10
    self.y_apparatusHeading = 10
    self.x_apparatusText = 10
    self.x_apparatusPicture = 190
    self.x2_apparatusText = 380
    self.x2_apparatusPicture = 510
    self.y_apparatusRow1 = 60
    self.y_apparatusRow2 = 230
    self.y_apparatusRow3 = 400
apparatus = Apparatus() #--Class is instantiated

class MovingAnimation: #--Class for all the attributes needed to create the animation
  def __init__(self):
    self.x_stand = 70 #--These attributes are for the x and y coordinate of every object in the screen
    self.y_stand = 50
    self.x_base = 10
    self.y_base = 530
    self.x_clamp = 70
    self.y_clamp = 50
    self.x_pad = 150
    self.y_pad = 515
    self.x_counterweight = 15
    self.y_counterweight = 500
    self.x_electromagnet = 175
    self.y_electromagnet = 62
    self.x_ball = 192
    self.y_ball = 96
    self.x_lightgate = 60
    self.y_lightgate = 150
    self.x_lightgate2 = 60
    self.y_lightgate2 = 450
    self.x_lightray = 120
    self.y_lightray = 156
    self.x_lightray2 = 120
    self.y_lightray2 = 456
    self.y_lightgate2_075m = 375
    self.y_lightray2_075m = 381
    self.y_lightgate2_050m = 300
    self.y_lightray2_050m = 306
    self.y_lightgate2_025m = 225
    self.y_lightray2_025m = 231
    self.x_graphButton = 320
    self.y_graphButton = 300
    self.x_slider = 420
    self.y_slider = 400

    #--Since many of my objects are rectangles, I have included a height and width.
    self.width_stand = 12
    self.height_stand = 480
    self.width_base = 250
    self.height_base = 12
    self.width_clamp = 140
    self.height_clamp = 12
    self.width_pad = 80
    self.height_pad = 16
    self.width_counterweight = 40
    self.height_counterweight = 30
    self.width_electromagnet = 35
    self.height_electromagnet = 20
    self.radius_ball = 15
    self.width_lightgate = 50
    self.height_lightgate = 12
    self.width_lightgate2 = 50
    self.height_lightgate2 = 12
    self.width_lightray = 150 
    self.height_lightray = 1
    self.width_lightray2  = 150
    self.height_lightray2 = 1
    self.width_graphButton = 150
    self.height_graphButton = 150
    self.width_slider = 150
    self.height_slider = 150

    #--Labels for objects in the screen
    self.clampStand_label = pract.fontObj_small.render("Clamp Stand", True, pract.BLACK, pract.WHITE)
    self.counterweight_label = pract.fontObj_small.render("Counterweight", True, pract.BLACK, pract.WHITE)
    self.lightgates_label = pract.fontObj_small.render("Light gate", True, pract.BLACK, pract.WHITE)
    self.magnet_label = pract.fontObj_small.render("Electromagnet connected to low voltage DC supply", True, pract.BLACK, pract.WHITE)
    self.bearings_label = pract.fontObj_small.render("Ball bearing", True, pract.BLACK, pract.WHITE)
    self.press_spacebar_label = pract.fontObj_mediumsmall.render("Press the spacebar to drop the ball.", True, pract.BLACK, pract.WHITE)
    self.repeat_spacebar_label = pract.fontObj_mediumsmall.render("Press the spacebar again to repeat.", True, pract.BLACK, pract.WHITE)
    
    #--X and Y coordinates for every label
    self.x_clampStandlabel = 30
    self.y_clampStandlabel = 300
    self.y_clampStandlabel_075m = 230
    self.x_counterweightlabel = 15
    self.y_counterweightlabel = 550
    self.x_lightgateslabel = 50
    self.y_lightgateslabel = 120
    self.x_lightgateslabel2 = 50
    self.y_lightgateslabel2 = 420
    self.y_lightgateslabel2_075m = 345
    self.y_lightgateslabel2_050m = 270
    self.y_lightgateslabel2_025m = 190
    self.x_magnetlabel = 165
    self.y_magnetlabel = 20
    self.x_bearingslabel = 210
    self.y_bearingslabel = 86
    self.x_press_spacebarlabel = 400
    self.y_press_spacebarlabel = 550
    self.x_displaytimer = 390
    self.y_displaytimer = 430
    self.x_timerresult = 460
    self.y_timerresult = 470

    #--Attributes for the motion of the ball
    self.pressed = False
    self.intial_motion = 0
    self.acceleration = 0
    self.acceleration2 = 1

    #--Attributes for the buttons to change the coordinates of the light gates
    self.height_05_text = pract.fontObj_mediumsmall.render("0.5 metres", True, pract.BLACK, pract.GREY)
    self.chooseheight = 0
    self.x_height_1m_text = 556
    self.y_height_1m_text = 140
    self.x_height_075m_text = 545
    self.y_height_075m_text = 140
    self.x_height_050m_text = 545
    self.y_height_050m_text = 140
    self.x_height_025m_text = 545
    self.y_height_025m_text = 140
    self.coordinates_upbutton = ((560,120),(590,90), (620,120))
    self.coordinates_downbutton = ((560,180),(590,210), (620,180))

    #--Attributes for displaying the graph
    self.graphTime = []
    self.graphHeight = []
    self.height_05_text = pract.fontObj_mediumsmall.render("0.5 metres", True, pract.BLACK, pract.GREY)
    self.x_graphButton = 555
    self.y_graphButton = 243
    self.x_graphButtonText = 565
    self.y_graphButtonText = 250
    self.width_graphButton = 110
    self.height_graphButton = 40
    self.graphButtonText = pract.fontObj_mediumsmall.render("View Graph", True, pract.BLACK, pract.WHITE)
    self.countRepeats = 0
    self.repeatText = pract.fontObj_mediumsmall.render(" Repeat the experiment with different heights! ", True, pract.BLACK, pract.WHITE)
    self.x_repeatText = 330
    self.y_repeatText = 370

    #--So the user can exit the Pygame window
    self.x_exitButton = 555
    self.y_exitButton = 300
    self.x_exitButtonText = 595
    self.y_exitButtonText = 307
    self.width_exitButton = 110
    self.height_exitButton = 40
    self.exitButtonText = pract.fontObj_mediumsmall.render("Exit", True, pract.BLACK, pract.WHITE)
#--Class is instantiated
mov = MovingAnimation()

class PracticalAnimation:
  def __init__(self):
    win = pygame.display.set_mode((700, 600)) #--Sets the size of the Pygame window
    pygame.display.set_caption('Practical Animation') #--Gives the window a name
    win.fill(pract.ORANGE) #--Allows a background colour to be set
    #--First heading in the window
    heading_text = pract.fontObj.render(" Determination of 'g' by a freefall method ", True, pract.BLACK, pract.WHITE)
    begin_text = pract.fontObj.render(' Begin ', True, pract.BLACK)
    #--Allows the user to start the animation
    beginButton = pygame.draw.rect(win, pract.WHITE, (pract.x_beginButton, pract.y_beginButton, pract.width, pract.height))
    #--Draws the text onscreen
    win.blit(heading_text, (pract.x_heading, pract.y_heading))
    win.blit(begin_text, (pract.x_beginText, pract.y_beginText))
    #--Draws border around the text
    beginButton_border = pygame.draw.rect(win, pract.BLACK, (pract.x_beginButton, pract.y_beginButton, pract.width, pract.height),1)

    #--Starts a while loop which repeatedly checks the user's mouse position
    while pract.condition == True:
      pos = pygame.mouse.get_pos()
      #--Boundaries the user's mouse position has to be in for the button to be pressed
      if pos[0] > 310 and pos[0]< 390 and pos[1] > 300 and pos[1]< 350:
        event = pygame.event.poll()
        if event.type == pygame.MOUSEBUTTONDOWN:
          pract.condition = False #--Breaks the while loop
          win.fill(pract.ORANGE) #--New backgroud which replaces everything onscreen
          previous_time = pygame.time.get_ticks() #--Measures current time
          while pract.condition2 == True: #--Starts another while loop
            win.fill(pract.ORANGE)
            #--Draws the first set of text and images onscreen
            win.blit(apparatus.equipment_text, (apparatus.x_apparatusHeading, apparatus.y_apparatusHeading))
            win.blit(apparatus.clampStand_text, (apparatus.x_apparatusText, apparatus.y_apparatusRow1))
            win.blit(apparatus.img_clamp, (apparatus.x_apparatusPicture, apparatus.y_apparatusRow1))
            clampStand_rect = pygame.draw.rect(win, pract.BLACK, (apparatus.x_apparatusPicture, apparatus.y_apparatusRow1, 150,150),1)
            current_time = pygame.time.get_ticks() #--Measures the current time relative to the previous time
            if current_time - previous_time > apparatus.time_delay: #--Decides when the next batch of text and images should be displayed
              #--Next batch of text and images are displayed when the if statement is fulfilled
              win.blit(apparatus.equipment_text, (apparatus.x_apparatusHeading, apparatus.y_apparatusHeading))
              win.blit(apparatus.magnet_text, (apparatus.x_apparatusText, apparatus.y_apparatusRow2))
              win.blit(apparatus.img_magnet, (apparatus.x_apparatusPicture, apparatus.y_apparatusRow2))
              magnet_rect = pygame.draw.rect(win, pract.BLACK, (apparatus.x_apparatusPicture, apparatus.y_apparatusRow2, 150,150),1)
              current_time = pygame.time.get_ticks() #--Measures the current time relative to the previous time
              #--Larger time gap means a larger time delay is used
              if current_time - previous_time > apparatus.time_delay2:
                win.blit(apparatus.equipment_text, (apparatus.x_apparatusHeading, apparatus.y_apparatusHeading))
                win.blit(apparatus.bearings_text, (apparatus.x_apparatusText, apparatus.y_apparatusRow3))
                win.blit(apparatus.img_bearings, (apparatus.x_apparatusPicture, apparatus.y_apparatusRow3))
                bearings_rect = pygame.draw.rect(win, pract.BLACK, (apparatus.x_apparatusPicture, apparatus.y_apparatusRow3, 150,150),1)
                current_time = pygame.time.get_ticks()
                #--Process iterates
                if current_time - previous_time > apparatus.time_delay3:
                  win.blit(apparatus.equipment_text, (apparatus.x_apparatusHeading, apparatus.y_apparatusHeading))
                  win.blit(apparatus.gates_text, (apparatus.x2_apparatusText, apparatus.y_apparatusRow1))
                  win.blit(apparatus.img_gates, (apparatus.x2_apparatusPicture, apparatus.y_apparatusRow1))
                  gates_rect = pygame.draw.rect(win, pract.BLACK, (apparatus.x2_apparatusPicture, apparatus.y_apparatusRow1, 150,150),1)
                  current_time = pygame.time.get_ticks()
                  if current_time - previous_time > apparatus.time_delay4:
                    win.blit(apparatus.equipment_text, (apparatus.x_apparatusHeading, apparatus.y_apparatusHeading))
                    win.blit(apparatus.stopwatch_text, (apparatus.x2_apparatusText, apparatus.y_apparatusRow2))
                    win.blit(apparatus.img_stopwatch, (apparatus.x2_apparatusPicture, apparatus.y_apparatusRow2))
                    stopwatch_rect = pygame.draw.rect(win, pract.BLACK, (apparatus.x2_apparatusPicture, apparatus.y_apparatusRow2, 150,150),1)
                    current_time = pygame.time.get_ticks()
                    #--Waits some time before transitioning the screen
                    if current_time - previous_time > apparatus.time_delay5:
                      command = self.AnimationInteraction() #--Calls the next method

            #--While the program is running, checks whether the user is quitting the window
            for event in pygame.event.get(): 
              if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            pygame.display.update() #--Updates the display
      #--Since there are two while loops, there needs to be two lots of this code
      for event in pygame.event.get():
          if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
      pygame.display.update() #--Updates the display

  def AnimationInteraction(self):
    win = pygame.display.set_mode((700, 600))
    win.fill(pract.ORANGE)
    while pract.condition == False:
      keys = pygame.key.get_pressed() #--Detects user's key inputs
      if not (mov.pressed): #--Only runs when mov.pressed is False
        if keys[pygame.K_SPACE]:
          mov.pressed = True #--If true, on the next loop, the program won't check whether the space key is being pressed
        else:
          win.fill(pract.ORANGE)
          stand = pygame.draw.rect(win, pract.GREY,(mov.x_stand, mov.y_stand, mov.width_stand, mov.height_stand))
          #--An identical rectangle is created for the border
          stand = pygame.draw.rect(win, pract.BLACK,(mov.x_stand, mov.y_stand, mov.width_stand, mov.height_stand), 1)
          #--Rectangles for the base of the stand
          base = pygame.draw.rect(win, pract.GREY,(mov.x_base, mov.y_base, mov.width_base, mov.height_base))
          base = pygame.draw.rect(win, pract.BLACK,(mov.x_base, mov.y_base, mov.width_base, mov.height_base), 1)
          #--Rectangles for the top of the screen
          clamp = pygame.draw.rect(win, pract.GREY,(mov.x_clamp, mov.y_clamp, mov.width_clamp, mov.height_clamp))
          clamp = pygame.draw.rect(win, pract.BLACK,(mov.x_clamp, mov.y_clamp, mov.width_clamp, mov.height_clamp), 1)
          #--Rectangles for the pad and counterweight
          pad = pygame.draw.rect(win, pract.GREY,(mov.x_pad, mov.y_pad, mov.width_pad, mov.height_pad))
          pad = pygame.draw.rect(win, pract.BLACK,(mov.x_pad, mov.y_pad, mov.width_pad, mov.height_pad), 1)
          counterweight = pygame.draw.rect(win, pract.GREY,(mov.x_counterweight, mov.y_counterweight, mov.width_counterweight, mov.height_counterweight))
          counterweight = pygame.draw.rect(win, pract.BLACK,(mov.x_counterweight, mov.y_counterweight, mov.width_counterweight, mov.height_counterweight), 1)
          #--Drawing light gates as rectangles
          lightgate = pygame.draw.rect(win, pract.GREY,(mov.x_lightgate, mov.y_lightgate, mov.width_lightgate, mov.height_lightgate))
          lightgate = pygame.draw.rect(win, pract.BLACK,(mov.x_lightgate, mov.y_lightgate, mov.width_lightgate, mov.height_lightgate), 1)
          lightgate2 = pygame.draw.rect(win, pract.GREY,(mov.x_lightgate2, mov.y_lightgate2, mov.width_lightgate2, mov.height_lightgate2))
          lightgate2 = pygame.draw.rect(win, pract.BLACK,(mov.x_lightgate2, mov.y_lightgate2, mov.width_lightgate2, mov.height_lightgate2),1)
          #--Treating these as rectangles but with very small heights
          lightray = pygame.draw.rect(win, pract.RED,(mov.x_lightray, mov.y_lightray, mov.width_lightray, mov.height_lightray))
          lightray2 = pygame.draw.rect(win, pract.RED,(mov.x_lightray2, mov.y_lightray2, mov.width_lightray2, mov.height_lightray2))
          #--Drawing electromagnets as rectangles
          electromagnet = pygame.draw.rect(win, pract.GREY,(mov.x_electromagnet, mov.y_electromagnet, mov.width_electromagnet,mov.height_electromagnet))
          electromagnet = pygame.draw.rect(win, pract.BLACK,(mov.x_electromagnet, mov.y_electromagnet, mov.width_electromagnet,mov.height_electromagnet), 1)

          #--Drawing to the screen the various labels at the specified x and y coordinates
          win.blit(mov.clampStand_label, (mov.x_clampStandlabel, mov.y_clampStandlabel))
          win.blit(mov.counterweight_label, (mov.x_counterweightlabel, mov.y_counterweightlabel))
          win.blit(mov.lightgates_label, (mov.x_lightgateslabel, mov.y_lightgateslabel))
          win.blit(mov.lightgates_label, (mov.x_lightgateslabel2, mov.y_lightgateslabel2))
          win.blit(mov.magnet_label, (mov.x_magnetlabel, mov.y_magnetlabel))
          win.blit(mov.bearings_label, (mov.x_bearingslabel, mov.y_bearingslabel))
          win.blit(mov.press_spacebar_label, (mov.x_press_spacebarlabel, mov.y_press_spacebarlabel))
          
          #--Will be drawn as a circle
          ball_bearing = pygame.draw.circle(win, pract.GREY,(mov.x_ball, mov.y_ball), mov.radius_ball)
          ball_bearing = pygame.draw.circle(win, pract.BLACK,(mov.x_ball, mov.y_ball), mov.radius_ball,1)

          #--Buttons the user can press to change the position of the light gates
          increaseheightbutton = pygame.draw.polygon(win, pract.RED, mov.coordinates_upbutton,2)
          decreaseheightbutton = pygame.draw.polygon(win, pract.RED, mov.coordinates_downbutton,2)
          height_1m_text = pract.fontObj_mediumsmall.render(' 1 Metre ', True, pract.BLACK, pract.WHITE)
          win.blit(height_1m_text, (mov.x_height_1m_text, mov.y_height_1m_text))
          
          #--Detects whether this button has been pressed
          while pract.condition_lightgatebutton == True:
            keys = pygame.key.get_pressed() #--Receives any key press
            pos = pygame.mouse.get_pos() #--Receives any mouse press
            #--Boundaries the user's mouse position has to be in for the bottom button to be pressed
            if pos[0] > 560 and pos[0]< 620  and pos[1] > 160 and pos[1]< 230: 
              event = pygame.event.poll()
              #--The mouse button has to also be pressed
              if event.type == pygame.MOUSEBUTTONDOWN:
                mov.chooseheight -=1
                #--Protects against repeated clicking of the button
                if mov.chooseheight < -3:
                  mov.chooseheight = -3
                #--If the button is pressed once, the diagram for a height of 0.75m will be displayed.
                if mov.chooseheight == -1:
                  win.fill(pract.ORANGE)
                  stand = pygame.draw.rect(win, pract.GREY,(mov.x_stand, mov.y_stand, mov.width_stand, mov.height_stand))
                  #--An identical rectangle is created for the border
                  stand = pygame.draw.rect(win, pract.BLACK,(mov.x_stand, mov.y_stand, mov.width_stand, mov.height_stand), 1)
                  #--Rectangles for the base of the stand
                  base = pygame.draw.rect(win, pract.GREY,(mov.x_base, mov.y_base, mov.width_base, mov.height_base))
                  base = pygame.draw.rect(win, pract.BLACK,(mov.x_base, mov.y_base, mov.width_base, mov.height_base), 1)
                  #--Rectangles for the top of the screen
                  clamp = pygame.draw.rect(win, pract.GREY,(mov.x_clamp, mov.y_clamp, mov.width_clamp, mov.height_clamp))
                  clamp = pygame.draw.rect(win, pract.BLACK,(mov.x_clamp, mov.y_clamp, mov.width_clamp, mov.height_clamp), 1)
                  #--Rectangles for the pad and counterweight
                  pad = pygame.draw.rect(win, pract.GREY,(mov.x_pad, mov.y_pad, mov.width_pad, mov.height_pad))
                  pad = pygame.draw.rect(win, pract.BLACK,(mov.x_pad, mov.y_pad, mov.width_pad, mov.height_pad), 1)
                  counterweight = pygame.draw.rect(win, pract.GREY,(mov.x_counterweight, mov.y_counterweight, mov.width_counterweight, mov.height_counterweight))
                  counterweight = pygame.draw.rect(win, pract.BLACK,(mov.x_counterweight, mov.y_counterweight, mov.width_counterweight, mov.height_counterweight), 1)
                  #--Drawing electromagnets as rectangles
                  electromagnet = pygame.draw.rect(win, pract.GREY,(mov.x_electromagnet, mov.y_electromagnet, mov.width_electromagnet,mov.height_electromagnet))
                  electromagnet = pygame.draw.rect(win, pract.BLACK,(mov.x_electromagnet, mov.y_electromagnet, mov.width_electromagnet,mov.height_electromagnet), 1)
                  #--Will be drawn as a circle
                  ball_bearing = pygame.draw.circle(win, pract.GREY,(mov.x_ball, mov.y_ball), mov.radius_ball)
                  ball_bearing = pygame.draw.circle(win, pract.BLACK,(mov.x_ball, mov.y_ball), mov.radius_ball,1)

                  #--Drawing to the screen the various labels at the specified x and y coordinates
                  win.blit(mov.counterweight_label, (mov.x_counterweightlabel, mov.y_counterweightlabel))
                  win.blit(mov.lightgates_label, (mov.x_lightgateslabel, mov.y_lightgateslabel))
                  win.blit(mov.lightgates_label, (mov.x_lightgateslabel2, mov.y_lightgateslabel2_075m))
                  win.blit(mov.magnet_label, (mov.x_magnetlabel, mov.y_magnetlabel))
                  win.blit(mov.bearings_label, (mov.x_bearingslabel, mov.y_bearingslabel))
                  win.blit(mov.press_spacebar_label, (mov.x_press_spacebarlabel, mov.y_press_spacebarlabel))

                  #--Drawing light gates as rectangles
                  lightgate = pygame.draw.rect(win, pract.GREY,(mov.x_lightgate, mov.y_lightgate, mov.width_lightgate, mov.height_lightgate))
                  lightgate = pygame.draw.rect(win, pract.BLACK,(mov.x_lightgate, mov.y_lightgate, mov.width_lightgate, mov.height_lightgate), 1)
                  lightgate2_075m = pygame.draw.rect(win, pract.GREY,(mov.x_lightgate2, mov.y_lightgate2_075m, mov.width_lightgate2, mov.height_lightgate2))
                  lightgate2_075m= pygame.draw.rect(win, pract.BLACK,(mov.x_lightgate2, mov.y_lightgate2_075m, mov.width_lightgate2, mov.height_lightgate2), 1)
                  
                  #--Treating these as rectangles but with very small heights
                  lightray = pygame.draw.rect(win, pract.RED,(mov.x_lightray, mov.y_lightray, mov.width_lightray, mov.height_lightray))
                  lightray2_075m = pygame.draw.rect(win, pract.RED,(mov.x_lightray2, mov.y_lightray2_075m, mov.width_lightray2, mov.height_lightray2))

                  #--Buttons the user can press to change the position of the light gates
                  increaseheightbutton = pygame.draw.polygon(win, pract.RED, mov.coordinates_upbutton,2)
                  decreaseheightbutton = pygame.draw.polygon(win, pract.RED, mov.coordinates_downbutton,2)
                  height_075m_text = pract.fontObj_mediumsmall.render(' 0.75 Metres ', True, pract.BLACK, pract.WHITE)
                  win.blit(height_075m_text, (mov.x_height_075m_text, mov.y_height_075m_text))

                #--If the button is pressed twice, the diagram for a height of 0.50m will be displayed.
                if mov.chooseheight == -2:
                  win.fill(pract.ORANGE)
                  stand = pygame.draw.rect(win, pract.GREY,(mov.x_stand, mov.y_stand, mov.width_stand, mov.height_stand))
                  #--An identical rectangle is created for the border
                  stand = pygame.draw.rect(win, pract.BLACK,(mov.x_stand, mov.y_stand, mov.width_stand, mov.height_stand), 1)
                  #--Rectangles for the base of the stand
                  base = pygame.draw.rect(win, pract.GREY,(mov.x_base, mov.y_base, mov.width_base, mov.height_base))
                  base = pygame.draw.rect(win, pract.BLACK,(mov.x_base, mov.y_base, mov.width_base, mov.height_base), 1)
                  #--Rectangles for the top of the screen
                  clamp = pygame.draw.rect(win, pract.GREY,(mov.x_clamp, mov.y_clamp, mov.width_clamp, mov.height_clamp))
                  clamp = pygame.draw.rect(win, pract.BLACK,(mov.x_clamp, mov.y_clamp, mov.width_clamp, mov.height_clamp), 1)
                  #--Rectangles for the pad and counterweight
                  pad = pygame.draw.rect(win, pract.GREY,(mov.x_pad, mov.y_pad, mov.width_pad, mov.height_pad))
                  pad = pygame.draw.rect(win, pract.BLACK,(mov.x_pad, mov.y_pad, mov.width_pad, mov.height_pad), 1)
                  counterweight = pygame.draw.rect(win, pract.GREY,(mov.x_counterweight, mov.y_counterweight, mov.width_counterweight, mov.height_counterweight))
                  counterweight = pygame.draw.rect(win, pract.BLACK,(mov.x_counterweight, mov.y_counterweight, mov.width_counterweight, mov.height_counterweight), 1)
                  #--Drawing electromagnets as rectangles
                  electromagnet = pygame.draw.rect(win, pract.GREY,(mov.x_electromagnet, mov.y_electromagnet, mov.width_electromagnet,mov.height_electromagnet))
                  electromagnet = pygame.draw.rect(win, pract.BLACK,(mov.x_electromagnet, mov.y_electromagnet, mov.width_electromagnet,mov.height_electromagnet), 1)
                  #--Will be drawn as a circle
                  ball_bearing = pygame.draw.circle(win, pract.GREY,(mov.x_ball, mov.y_ball), mov.radius_ball)
                  ball_bearing = pygame.draw.circle(win, pract.BLACK,(mov.x_ball, mov.y_ball), mov.radius_ball,1)
                  #--Drawing to the screen the various labels at the specified x and y coordinates
                  win.blit(mov.counterweight_label, (mov.x_counterweightlabel, mov.y_counterweightlabel))
                  win.blit(mov.lightgates_label, (mov.x_lightgateslabel, mov.y_lightgateslabel))
                  #--New position of the light gate label
                  win.blit(mov.lightgates_label, (mov.x_lightgateslabel2, mov.y_lightgateslabel2_050m))
                  win.blit(mov.magnet_label, (mov.x_magnetlabel, mov.y_magnetlabel))
                  win.blit(mov.bearings_label, (mov.x_bearingslabel, mov.y_bearingslabel))
                  win.blit(mov.press_spacebar_label, (mov.x_press_spacebarlabel, mov.y_press_spacebarlabel))
                  
                  lightgate = pygame.draw.rect(win, pract.GREY,(mov.x_lightgate, mov.y_lightgate, mov.width_lightgate, mov.height_lightgate))
                  lightgate = pygame.draw.rect(win, pract.BLACK,(mov.x_lightgate, mov.y_lightgate, mov.width_lightgate, mov.height_lightgate), 1)
                  #--New coordinates for the light gates
                  lightgate2_050m = pygame.draw.rect(win, pract.GREY,(mov.x_lightgate2, mov.y_lightgate2_050m, mov.width_lightgate2, mov.height_lightgate2))
                  lightgate2_050m= pygame.draw.rect(win, pract.BLACK,(mov.x_lightgate2, mov.y_lightgate2_050m, mov.width_lightgate2, mov.height_lightgate2), 1)
                  
                  #--Treating these as rectangles but with very small heights
                  lightray = pygame.draw.rect(win, pract.RED,(mov.x_lightray, mov.y_lightray, mov.width_lightray, mov.height_lightray))
                  lightray2_050m = pygame.draw.rect(win, pract.RED,(mov.x_lightray2, mov.y_lightray2_050m, mov.width_lightray2, mov.height_lightray2))

                  #--Buttons the user can press to change the position of the light gates
                  increaseheightbutton = pygame.draw.polygon(win, pract.RED, mov.coordinates_upbutton,2)
                  decreaseheightbutton = pygame.draw.polygon(win, pract.RED, mov.coordinates_downbutton,2)
                  #--New label for the height of 0.5 metres
                  height_050m_text = pract.fontObj_mediumsmall.render(' 0.5 Metres ', True, pract.BLACK, pract.WHITE)
                  win.blit(height_050m_text, (mov.x_height_050m_text, mov.y_height_050m_text))

                #--If the button is pressed thrice, the diagram for a height of 0.25m will be displayed.
                if mov.chooseheight == -3:
                  win.fill(pract.ORANGE)
                  stand = pygame.draw.rect(win, pract.GREY,(mov.x_stand, mov.y_stand, mov.width_stand, mov.height_stand))
                  #--An identical rectangle is created for the border
                  stand = pygame.draw.rect(win, pract.BLACK,(mov.x_stand, mov.y_stand, mov.width_stand, mov.height_stand), 1)
                  #--Rectangles for the base of the stand
                  base = pygame.draw.rect(win, pract.GREY,(mov.x_base, mov.y_base, mov.width_base, mov.height_base))
                  base = pygame.draw.rect(win, pract.BLACK,(mov.x_base, mov.y_base, mov.width_base, mov.height_base), 1)
                  #--Rectangles for the top of the screen
                  clamp = pygame.draw.rect(win, pract.GREY,(mov.x_clamp, mov.y_clamp, mov.width_clamp, mov.height_clamp))
                  clamp = pygame.draw.rect(win, pract.BLACK,(mov.x_clamp, mov.y_clamp, mov.width_clamp, mov.height_clamp), 1)
                  #--Rectangles for the pad and counterweight
                  pad = pygame.draw.rect(win, pract.GREY,(mov.x_pad, mov.y_pad, mov.width_pad, mov.height_pad))
                  pad = pygame.draw.rect(win, pract.BLACK,(mov.x_pad, mov.y_pad, mov.width_pad, mov.height_pad), 1)
                  counterweight = pygame.draw.rect(win, pract.GREY,(mov.x_counterweight, mov.y_counterweight, mov.width_counterweight, mov.height_counterweight))
                  counterweight = pygame.draw.rect(win, pract.BLACK,(mov.x_counterweight, mov.y_counterweight, mov.width_counterweight, mov.height_counterweight), 1)
                  #--Drawing electromagnets as rectangles
                  electromagnet = pygame.draw.rect(win, pract.GREY,(mov.x_electromagnet, mov.y_electromagnet, mov.width_electromagnet,mov.height_electromagnet))
                  electromagnet = pygame.draw.rect(win, pract.BLACK,(mov.x_electromagnet, mov.y_electromagnet, mov.width_electromagnet,mov.height_electromagnet), 1)
                  #--Will be drawn as a circle
                  ball_bearing = pygame.draw.circle(win, pract.GREY,(mov.x_ball, mov.y_ball), mov.radius_ball)
                  ball_bearing = pygame.draw.circle(win, pract.BLACK,(mov.x_ball, mov.y_ball), mov.radius_ball,1)
                  #--Drawing to the screen the various labels at the specified x and y coordinates
                  win.blit(mov.counterweight_label, (mov.x_counterweightlabel, mov.y_counterweightlabel))
                  win.blit(mov.lightgates_label, (mov.x_lightgateslabel, mov.y_lightgateslabel))
                  #--New position of the light gate label
                  win.blit(mov.lightgates_label, (mov.x_lightgateslabel2, mov.y_lightgateslabel2_025m))
                  win.blit(mov.magnet_label, (mov.x_magnetlabel, mov.y_magnetlabel))
                  win.blit(mov.bearings_label, (mov.x_bearingslabel, mov.y_bearingslabel))
                  win.blit(mov.press_spacebar_label, (mov.x_press_spacebarlabel, mov.y_press_spacebarlabel))
                  
                  lightgate = pygame.draw.rect(win, pract.GREY,(mov.x_lightgate, mov.y_lightgate, mov.width_lightgate, mov.height_lightgate))
                  lightgate = pygame.draw.rect(win, pract.BLACK,(mov.x_lightgate, mov.y_lightgate, mov.width_lightgate, mov.height_lightgate), 1)
                  #--New coordinates for the light gate
                  lightgate2_025m = pygame.draw.rect(win, pract.GREY,(mov.x_lightgate2, mov.y_lightgate2_025m, mov.width_lightgate2, mov.height_lightgate2))
                  lightgate2_025m= pygame.draw.rect(win, pract.BLACK,(mov.x_lightgate2, mov.y_lightgate2_025m, mov.width_lightgate2, mov.height_lightgate2), 1)
                  #--Treating these as rectangles but with very small heights
                  lightray = pygame.draw.rect(win, pract.RED,(mov.x_lightray, mov.y_lightray, mov.width_lightray, mov.height_lightray))
                  lightray2_025m = pygame.draw.rect(win, pract.RED,(mov.x_lightray2, mov.y_lightray2_025m, mov.width_lightray2, mov.height_lightray2))

                  #--Buttons the user can press to change the position of the light gates
                  increaseheightbutton = pygame.draw.polygon(win, pract.RED, mov.coordinates_upbutton,2)
                  decreaseheightbutton = pygame.draw.polygon(win, pract.RED, mov.coordinates_downbutton,2)
                  #--New label for the height of 0.25 metres
                  height_025m_text = pract.fontObj_mediumsmall.render(' 0.25 Metres ', True, pract.BLACK, pract.WHITE)
                  win.blit(height_025m_text, (mov.x_height_025m_text, mov.y_height_025m_text))
                
            if pos[0] > 560 and pos[0]< 620  and pos[1] > 70 and pos[1]< 140: #--Boundaries for the up button
              event = pygame.event.poll()
              #--The mouse button has to also be pressed
              if event.type == pygame.MOUSEBUTTONDOWN:
                mov.chooseheight += 1 #--Will increment this attribute by 1
                if mov.chooseheight > 0:
                  mov.chooseheight = 0 #--Protects against repeated clicking of the up button
                else:
                  mov.chooseheight = 0 
                  #--Displays window with new objects
                  win.fill(pract.ORANGE)
                  stand = pygame.draw.rect(win, pract.GREY,(mov.x_stand, mov.y_stand, mov.width_stand, mov.height_stand))
                  #--An identical rectangle is created for the border
                  stand = pygame.draw.rect(win, pract.BLACK,(mov.x_stand, mov.y_stand, mov.width_stand, mov.height_stand), 1)
                  #--Rectangles for the base of the stand
                  base = pygame.draw.rect(win, pract.GREY,(mov.x_base, mov.y_base, mov.width_base, mov.height_base))
                  base = pygame.draw.rect(win, pract.BLACK,(mov.x_base, mov.y_base, mov.width_base, mov.height_base), 1)
                  #--Rectangles for the top of the screen
                  clamp = pygame.draw.rect(win, pract.GREY,(mov.x_clamp, mov.y_clamp, mov.width_clamp, mov.height_clamp))
                  clamp = pygame.draw.rect(win, pract.BLACK,(mov.x_clamp, mov.y_clamp, mov.width_clamp, mov.height_clamp), 1)
                  #--Rectangles for the pad and counterweight
                  pad = pygame.draw.rect(win, pract.GREY,(mov.x_pad, mov.y_pad, mov.width_pad, mov.height_pad))
                  pad = pygame.draw.rect(win, pract.BLACK,(mov.x_pad, mov.y_pad, mov.width_pad, mov.height_pad), 1)
                  counterweight = pygame.draw.rect(win, pract.GREY,(mov.x_counterweight, mov.y_counterweight, mov.width_counterweight, mov.height_counterweight))
                  counterweight = pygame.draw.rect(win, pract.BLACK,(mov.x_counterweight, mov.y_counterweight, mov.width_counterweight, mov.height_counterweight), 1)
                  #--Drawing light gates as rectangles
                  lightgate = pygame.draw.rect(win, pract.GREY,(mov.x_lightgate, mov.y_lightgate, mov.width_lightgate, mov.height_lightgate))
                  lightgate = pygame.draw.rect(win, pract.BLACK,(mov.x_lightgate, mov.y_lightgate, mov.width_lightgate, mov.height_lightgate), 1)
                  lightgate2 = pygame.draw.rect(win, pract.GREY,(mov.x_lightgate2, mov.y_lightgate2, mov.width_lightgate2, mov.height_lightgate2))
                  lightgate2 = pygame.draw.rect(win, pract.BLACK,(mov.x_lightgate2, mov.y_lightgate2, mov.width_lightgate2, mov.height_lightgate2),1)
                  #--Treating these as rectangles but with very small heights
                  lightray = pygame.draw.rect(win, pract.RED,(mov.x_lightray, mov.y_lightray, mov.width_lightray, mov.height_lightray))
                  lightray2 = pygame.draw.rect(win, pract.RED,(mov.x_lightray2, mov.y_lightray2, mov.width_lightray2, mov.height_lightray2))
                  #--Drawing electromagnets as rectangles
                  electromagnet = pygame.draw.rect(win, pract.GREY,(mov.x_electromagnet, mov.y_electromagnet, mov.width_electromagnet,mov.height_electromagnet))
                  electromagnet = pygame.draw.rect(win, pract.BLACK,(mov.x_electromagnet, mov.y_electromagnet, mov.width_electromagnet,mov.height_electromagnet), 1)

                  #--Drawing to the screen the various labels at the specified x and y coordinates
                  win.blit(mov.clampStand_label, (mov.x_clampStandlabel, mov.y_clampStandlabel))
                  win.blit(mov.counterweight_label, (mov.x_counterweightlabel, mov.y_counterweightlabel))
                  win.blit(mov.lightgates_label, (mov.x_lightgateslabel, mov.y_lightgateslabel))
                  win.blit(mov.lightgates_label, (mov.x_lightgateslabel2, mov.y_lightgateslabel2))
                  win.blit(mov.magnet_label, (mov.x_magnetlabel, mov.y_magnetlabel))
                  win.blit(mov.bearings_label, (mov.x_bearingslabel, mov.y_bearingslabel))
                  win.blit(mov.press_spacebar_label, (mov.x_press_spacebarlabel, mov.y_press_spacebarlabel))
                  
                  #--Will be drawn as a circle
                  ball_bearing = pygame.draw.circle(win, pract.GREY,(mov.x_ball, mov.y_ball), mov.radius_ball)
                  ball_bearing = pygame.draw.circle(win, pract.BLACK,(mov.x_ball, mov.y_ball), mov.radius_ball,1)

                  #--Buttons the user can press to change the position of the light gates
                  increaseheightbutton = pygame.draw.polygon(win, pract.RED, mov.coordinates_upbutton,2)
                  decreaseheightbutton = pygame.draw.polygon(win, pract.RED, mov.coordinates_downbutton,2)
                  height_1m_text = pract.fontObj_mediumsmall.render(' 1 Metre ', True, pract.BLACK, pract.WHITE)
                  win.blit(height_1m_text, (mov.x_height_1m_text, mov.y_height_1m_text))

            if keys[pygame.K_SPACE]: #--Checks whether the space bar has been pressed
              pract.condition_lightgatebutton = False #--If so, this while loop will be ended
                
            #--While the program is running, checks whether the user is quitting the window
            for event in pygame.event.get(): 
              if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            pygame.display.update() #--Updates the display
            
      else: #--Previous if not statement is bypassed
        win.fill(pract.ORANGE)
        #--Practical diagram is redrawn
        stand = pygame.draw.rect(win, pract.GREY,(mov.x_stand, mov.y_stand, mov.width_stand, mov.height_stand))
        #--An identical rectangle is created for the border
        stand = pygame.draw.rect(win, pract.BLACK,(mov.x_stand, mov.y_stand, mov.width_stand, mov.height_stand), 1)
        #--Rectangles for the base of the stand
        base = pygame.draw.rect(win, pract.GREY,(mov.x_base, mov.y_base, mov.width_base, mov.height_base))
        base = pygame.draw.rect(win, pract.BLACK,(mov.x_base, mov.y_base, mov.width_base, mov.height_base), 1)
        #--Rectangles for the top of the stand
        clamp = pygame.draw.rect(win, pract.GREY,(mov.x_clamp, mov.y_clamp, mov.width_clamp, mov.height_clamp))
        clamp = pygame.draw.rect(win, pract.BLACK,(mov.x_clamp, mov.y_clamp, mov.width_clamp, mov.height_clamp), 1)
        #--Rectangles for the pad and counterweight
        pad = pygame.draw.rect(win, pract.GREY,(mov.x_pad, mov.y_pad, mov.width_pad, mov.height_pad))
        pad = pygame.draw.rect(win, pract.BLACK,(mov.x_pad, mov.y_pad, mov.width_pad, mov.height_pad), 1)
        counterweight = pygame.draw.rect(win, pract.GREY,(mov.x_counterweight, mov.y_counterweight, mov.width_counterweight, mov.height_counterweight))
        counterweight = pygame.draw.rect(win, pract.BLACK,(mov.x_counterweight, mov.y_counterweight, mov.width_counterweight, mov.height_counterweight), 1)

        if mov.chooseheight == 0: #--When the up or down button is not pressed
          #--Drawing the original light gates
          lightgate = pygame.draw.rect(win, pract.GREY,(mov.x_lightgate, mov.y_lightgate, mov.width_lightgate, mov.height_lightgate))
          lightgate = pygame.draw.rect(win, pract.BLACK,(mov.x_lightgate, mov.y_lightgate, mov.width_lightgate, mov.height_lightgate), 1)
          lightgate2 = pygame.draw.rect(win, pract.GREY,(mov.x_lightgate2, mov.y_lightgate2, mov.width_lightgate2, mov.height_lightgate2))
          lightgate2 = pygame.draw.rect(win, pract.BLACK,(mov.x_lightgate2, mov.y_lightgate2, mov.width_lightgate2, mov.height_lightgate2),1)
          #--Treating these as rectangles but with very small heights
          lightray = pygame.draw.rect(win, pract.RED,(mov.x_lightray, mov.y_lightray, mov.width_lightray, mov.height_lightray))
          lightray2 = pygame.draw.rect(win, pract.RED,(mov.x_lightray2, mov.y_lightray2, mov.width_lightray2, mov.height_lightray2))
          #--Drawing light gate label
          win.blit(mov.lightgates_label, (mov.x_lightgateslabel2, mov.y_lightgateslabel2))
          #--Drawing clamp stand label
          win.blit(mov.clampStand_label, (mov.x_clampStandlabel, mov.y_clampStandlabel))

        if mov.chooseheight == -1: #--When the down button is pressed once
          #--Drawing the new light gates corresponding to a height of 0.75 metres
          lightgate = pygame.draw.rect(win, pract.GREY,(mov.x_lightgate, mov.y_lightgate, mov.width_lightgate, mov.height_lightgate))
          lightgate = pygame.draw.rect(win, pract.BLACK,(mov.x_lightgate, mov.y_lightgate, mov.width_lightgate, mov.height_lightgate), 1)
          lightgate2_075m = pygame.draw.rect(win, pract.GREY,(mov.x_lightgate2, mov.y_lightgate2_075m, mov.width_lightgate2, mov.height_lightgate2))
          lightgate2_075m = pygame.draw.rect(win, pract.BLACK,(mov.x_lightgate2, mov.y_lightgate2_075m, mov.width_lightgate2, mov.height_lightgate2), 1)
          #--Treating these as rectangles but with very small heights
          lightray = pygame.draw.rect(win, pract.RED,(mov.x_lightray, mov.y_lightray, mov.width_lightray, mov.height_lightray))
          lightray2_075m = pygame.draw.rect(win, pract.RED,(mov.x_lightray2, mov.y_lightray2_075m, mov.width_lightray2, mov.height_lightray2))
          #--Drawing light gate label
          win.blit(mov.lightgates_label, (mov.x_lightgateslabel2, mov.y_lightgateslabel2_075m))

        if mov.chooseheight == -2: #--When the down button is pressed twice
          #--Drawing the new light gates corresponding to a height of 0.5 metres
          lightgate = pygame.draw.rect(win, pract.GREY,(mov.x_lightgate, mov.y_lightgate, mov.width_lightgate, mov.height_lightgate))
          lightgate = pygame.draw.rect(win, pract.BLACK,(mov.x_lightgate, mov.y_lightgate, mov.width_lightgate, mov.height_lightgate), 1)
          lightgate2_050m = pygame.draw.rect(win, pract.GREY,(mov.x_lightgate2, mov.y_lightgate2_050m, mov.width_lightgate2, mov.height_lightgate2))
          lightgate2_050m = pygame.draw.rect(win, pract.BLACK,(mov.x_lightgate2, mov.y_lightgate2_050m, mov.width_lightgate2, mov.height_lightgate2), 1)
          #--Treating these as rectangles but with very small heights
          lightray = pygame.draw.rect(win, pract.RED,(mov.x_lightray, mov.y_lightray, mov.width_lightray, mov.height_lightray))
          lightray2_050m = pygame.draw.rect(win, pract.RED,(mov.x_lightray2, mov.y_lightray2_050m, mov.width_lightray2, mov.height_lightray2))
          #--Drawing light gate label
          win.blit(mov.lightgates_label, (mov.x_lightgateslabel2, mov.y_lightgateslabel2_050m))

        if mov.chooseheight == -3: #--When the down button is pressed thrice
          #--Drawing the new light gates corresponding to a height of 0.25 metres
          lightgate = pygame.draw.rect(win, pract.GREY,(mov.x_lightgate, mov.y_lightgate, mov.width_lightgate, mov.height_lightgate))
          lightgate = pygame.draw.rect(win, pract.BLACK,(mov.x_lightgate, mov.y_lightgate, mov.width_lightgate, mov.height_lightgate), 1)
          lightgate2_025m = pygame.draw.rect(win, pract.GREY,(mov.x_lightgate2, mov.y_lightgate2_025m, mov.width_lightgate2, mov.height_lightgate2))
          lightgate2_025m = pygame.draw.rect(win, pract.BLACK,(mov.x_lightgate2, mov.y_lightgate2_025m, mov.width_lightgate2, mov.height_lightgate2), 1)
          #--Treating these as rectangles but with very small heights
          lightray = pygame.draw.rect(win, pract.RED,(mov.x_lightray, mov.y_lightray, mov.width_lightray, mov.height_lightray))
          lightray2_025m = pygame.draw.rect(win, pract.RED,(mov.x_lightray2, mov.y_lightray2_025m, mov.width_lightray2, mov.height_lightray2))
          #--Drawing light gate label
          win.blit(mov.lightgates_label, (mov.x_lightgateslabel2, mov.y_lightgateslabel2_025m))
          
        #--Drawing electromagnets as rectangles
        electromagnet = pygame.draw.rect(win, pract.GREY,(mov.x_electromagnet, mov.y_electromagnet, mov.width_electromagnet,mov.height_electromagnet))
        electromagnet = pygame.draw.rect(win, pract.BLACK,(mov.x_electromagnet, mov.y_electromagnet, mov.width_electromagnet,mov.height_electromagnet), 1)
        #--Will be drawn as a circle
        ball_bearing = pygame.draw.circle(win, pract.GREY,(mov.x_ball, int(mov.y_ball)), mov.radius_ball)
        ball_bearing = pygame.draw.circle(win, pract.BLACK,(mov.x_ball, int(mov.y_ball)), mov.radius_ball,1)

        #--Drawing to the screen the various labels at the specified x and y coordinates
        win.blit(mov.counterweight_label, (mov.x_counterweightlabel, mov.y_counterweightlabel))
        win.blit(mov.lightgates_label, (mov.x_lightgateslabel, mov.y_lightgateslabel))
        win.blit(mov.magnet_label, (mov.x_magnetlabel, mov.y_magnetlabel))
        win.blit(mov.bearings_label, (mov.x_bearingslabel, mov.y_bearingslabel))
        win.blit(mov.press_spacebar_label, (mov.x_press_spacebarlabel, mov.y_press_spacebarlabel))

        if mov.chooseheight == 0: #--If the light gates are in their original positions
          if mov.y_ball > mov.y_lightray - 1 and mov.y_ball < mov.y_lightray + 1: #--When ball passes the first light gate
            self.lightgate_detect = pygame.time.get_ticks() #--Will record time
            
          if mov.y_ball > mov.y_lightray2 - 1 and mov.y_ball < mov.y_lightray2 + 1: #--When ball passes the second light gate
            self.lightgate2_detect = pygame.time.get_ticks()
            self.result_time = self.lightgate2_detect - self.lightgate_detect #--Stores the calculated time
            #--Appending time and height to lists
            mov.graphTime.append(((self.result_time)**2)/1000**2)
            mov.graphHeight.append(1)
            
        if mov.chooseheight == -1: #--If the light gates are separated by a distance of 0.75 metres
          if mov.y_ball > mov.y_lightray - 1 and mov.y_ball < mov.y_lightray + 1: #--When ball passes the first light gate
            self.lightgate_detect = pygame.time.get_ticks() #--Will record time

          if mov.y_ball > mov.y_lightray2_075m - 1 and mov.y_ball < mov.y_lightray2_075m + 1: #--When ball passes the second light gate
            self.lightgate2_detect = pygame.time.get_ticks()
            self.result_time = self.lightgate2_detect - self.lightgate_detect #--Stores the calculated time
            #--Appending time and height to lists
            mov.graphTime.append(((self.result_time)**2)/1000**2)
            mov.graphHeight.append(0.75)

        if mov.chooseheight == -2: #--If the light gates are separated by a distance of 0.5 metres
          if mov.y_ball > mov.y_lightray - 1 and mov.y_ball < mov.y_lightray + 1: #--When ball passes the first light gate
            self.lightgate_detect = pygame.time.get_ticks() #--Will record time

          if mov.y_ball > mov.y_lightray2_050m - 1 and mov.y_ball < mov.y_lightray2_050m + 1: #--When ball passes the second light gate
            self.lightgate2_detect = pygame.time.get_ticks()
            self.result_time = self.lightgate2_detect - self.lightgate_detect #--Stores the calculated time
            #--Appending time and height to lists
            mov.graphTime.append(((self.result_time)**2)/1000**2)
            mov.graphHeight.append(0.5)

        if mov.chooseheight == -3: #--If the light gates are separated by a distance of 0.25 metres
          if mov.y_ball > mov.y_lightray - 1 and mov.y_ball < mov.y_lightray + 1: #--When ball passes the first light gate
            self.lightgate_detect = pygame.time.get_ticks() #--Will record time

          if mov.y_ball > mov.y_lightray2_025m - 1 and mov.y_ball < mov.y_lightray2_025m + 1: #--When ball passes the second light gate
            self.lightgate2_detect = pygame.time.get_ticks()
            self.result_time = self.lightgate2_detect - self.lightgate_detect #--Stores the calculated time
            #--Appending time and height to lists
            mov.graphTime.append(((self.result_time)**2)/1000**2)
            mov.graphHeight.append(0.25)
  
        if mov.y_ball >= 500: #--If the ball goes past the pad, the while loop will be broken
          #--Displays the time taken for the ball to fall
          self.display_timer = pract.fontObj_mediumsmall.render((f'Time taken to fall between light gates:'), True, pract.BLACK, pract.WHITE)
          self.time_result = pract.fontObj_medium.render(str(f'{self.result_time} milliseconds'), True, pract.BLACK, pract.WHITE)
          win.blit(self.display_timer, (mov.x_displaytimer,mov.y_displaytimer))
          win.blit(self.time_result, (mov.x_timerresult,mov.y_timerresult))
          #--Prompts the user to repeat the practical
          win.blit(mov.repeat_spacebar_label, (mov.x_press_spacebarlabel, mov.y_press_spacebarlabel))
          #--So the user can change the height of the light gates once the ball has fallen
          increaseheightbutton = pygame.draw.polygon(win, pract.RED, mov.coordinates_upbutton,2)
          decreaseheightbutton = pygame.draw.polygon(win, pract.RED, mov.coordinates_downbutton,2)
          #--So the user can open a graph of results
          graphButton = pygame.draw.rect(win, pract.WHITE, (mov.x_graphButton, mov.y_graphButton, mov.width_graphButton, mov.height_graphButton))
          graphButton = pygame.draw.rect(win, pract.RED, (mov.x_graphButton, mov.y_graphButton, mov.width_graphButton, mov.height_graphButton),1)
          win.blit(mov.graphButtonText,(mov.x_graphButtonText, mov.y_graphButtonText))

          #--Allows the user to exit the Pygame window
          exitButton = pygame.draw.rect(win, pract.WHITE, (mov.x_exitButton, mov.y_exitButton, mov.width_exitButton, mov.height_exitButton))
          exitButton = pygame.draw.rect(win, pract.RED, (mov.x_exitButton, mov.y_exitButton, mov.width_exitButton, mov.height_exitButton),1)
          win.blit(mov.exitButtonText,(mov.x_exitButtonText, mov.y_exitButtonText))

          #--Makes sure enough data points are plotted on the graph
          mov.countRepeats += 1
          
          #--Displays the current height between the light gates
          if mov.chooseheight == 0:
            height_1m_text = pract.fontObj_mediumsmall.render(' 1 Metre ', True, pract.BLACK, pract.WHITE)
            win.blit(height_1m_text, (mov.x_height_1m_text, mov.y_height_1m_text))
          elif mov.chooseheight == -1:
            height_075m_text = pract.fontObj_mediumsmall.render(' 0.75 Metres ', True, pract.BLACK, pract.WHITE)
            win.blit(height_075m_text, (mov.x_height_075m_text, mov.y_height_075m_text))
          elif mov.chooseheight == -2:
            height_050m_text = pract.fontObj_mediumsmall.render(' 0.5 Metres ', True, pract.BLACK, pract.WHITE)
            win.blit(height_050m_text, (mov.x_height_050m_text, mov.y_height_050m_text))
          elif mov.chooseheight == -3:
            height_050m_text = pract.fontObj_mediumsmall.render(' 0.25 Metres ', True, pract.BLACK, pract.WHITE)
            win.blit(height_050m_text, (mov.x_height_025m_text, mov.y_height_025m_text))

          #--Sets this condition to true so the while loop can always run
          pract.condition_lightgatebutton2 = True
          #--Detects whether the up or down button has been pressed
          while pract.condition_lightgatebutton2 == True:
            keys = pygame.key.get_pressed() #--Receives any key press
            pos = pygame.mouse.get_pos() #--Receives any mouse press
            #--Boundaries the user's mouse position has to be in for the bottom button to be pressed
            if pos[0] > 560 and pos[0]< 620  and pos[1] > 160 and pos[1]< 230: 
              event = pygame.event.poll()
              #--The mouse button has to be pressed
              if event.type == pygame.MOUSEBUTTONDOWN:
                mov.chooseheight -=1
                if mov.chooseheight < -3:
                  mov.chooseheight = -3 #--Protects against repeated clicking of the down button
                if mov.chooseheight == -1: #--Displaying the buttons and text for a height of 0.75 metres
                  increaseheightbutton = pygame.draw.polygon(win, pract.RED, mov.coordinates_upbutton,2)
                  decreaseheightbutton = pygame.draw.polygon(win, pract.RED, mov.coordinates_downbutton,2)
                  height_075m_text = pract.fontObj_mediumsmall.render(' 0.75 Metres ', True, pract.BLACK, pract.WHITE)
                  win.blit(height_075m_text, (mov.x_height_075m_text, mov.y_height_075m_text))

                if mov.chooseheight == -2: #--Displaying the buttons and text for a height of 0.5 metres
                  increaseheightbutton = pygame.draw.polygon(win, pract.RED, mov.coordinates_upbutton,2)
                  decreaseheightbutton = pygame.draw.polygon(win, pract.RED, mov.coordinates_downbutton,2)
                  height_050m_text = pract.fontObj_mediumsmall.render(' 0.5 Metres   ', True, pract.BLACK, pract.WHITE)
                  win.blit(height_050m_text, (mov.x_height_050m_text, mov.y_height_050m_text))

                if mov.chooseheight == -3: #--Displaying the buttons and text for a height of 0.25 metres
                  increaseheightbutton = pygame.draw.polygon(win, pract.RED, mov.coordinates_upbutton,2)
                  decreaseheightbutton = pygame.draw.polygon(win, pract.RED, mov.coordinates_downbutton,2)
                  height_025m_text = pract.fontObj_mediumsmall.render(' 0.25 Metres   ', True, pract.BLACK, pract.WHITE)
                  win.blit(height_025m_text, (mov.x_height_025m_text, mov.y_height_025m_text))
                  
            if pos[0] > 560 and pos[0]< 620  and pos[1] > 70 and pos[1]< 140: #--Boundaries for the up button
              event = pygame.event.poll()
              #--The mouse button has to be pressed
              if event.type == pygame.MOUSEBUTTONDOWN:
                mov.chooseheight += 1 #--Will increment this attribute by 1
                if mov.chooseheight > 0:
                  mov.chooseheight = 0 #--Protects against repeated clicking of the up button
                else:
                  mov.chooseheight = 0
                  win.fill(pract.ORANGE)
                  stand = pygame.draw.rect(win, pract.GREY,(mov.x_stand, mov.y_stand, mov.width_stand, mov.height_stand))
                  #--An identical rectangle is created for the border
                  stand = pygame.draw.rect(win, pract.BLACK,(mov.x_stand, mov.y_stand, mov.width_stand, mov.height_stand), 1)
                  #--Rectangles for the base of the stand
                  base = pygame.draw.rect(win, pract.GREY,(mov.x_base, mov.y_base, mov.width_base, mov.height_base))
                  base = pygame.draw.rect(win, pract.BLACK,(mov.x_base, mov.y_base, mov.width_base, mov.height_base), 1)
                  #--Rectangles for the top of the screen
                  clamp = pygame.draw.rect(win, pract.GREY,(mov.x_clamp, mov.y_clamp, mov.width_clamp, mov.height_clamp))
                  clamp = pygame.draw.rect(win, pract.BLACK,(mov.x_clamp, mov.y_clamp, mov.width_clamp, mov.height_clamp), 1)
                  #--Rectangles for the pad and counterweight
                  pad = pygame.draw.rect(win, pract.GREY,(mov.x_pad, mov.y_pad, mov.width_pad, mov.height_pad))
                  pad = pygame.draw.rect(win, pract.BLACK,(mov.x_pad, mov.y_pad, mov.width_pad, mov.height_pad), 1)
                  counterweight = pygame.draw.rect(win, pract.GREY,(mov.x_counterweight, mov.y_counterweight, mov.width_counterweight, mov.height_counterweight))
                  counterweight = pygame.draw.rect(win, pract.BLACK,(mov.x_counterweight, mov.y_counterweight, mov.width_counterweight, mov.height_counterweight), 1)
                  #--Drawing light gates as rectangles
                  lightgate = pygame.draw.rect(win, pract.GREY,(mov.x_lightgate, mov.y_lightgate, mov.width_lightgate, mov.height_lightgate))
                  lightgate = pygame.draw.rect(win, pract.BLACK,(mov.x_lightgate, mov.y_lightgate, mov.width_lightgate, mov.height_lightgate), 1)
                  lightgate2 = pygame.draw.rect(win, pract.GREY,(mov.x_lightgate2, mov.y_lightgate2, mov.width_lightgate2, mov.height_lightgate2))
                  lightgate2 = pygame.draw.rect(win, pract.BLACK,(mov.x_lightgate2, mov.y_lightgate2, mov.width_lightgate2, mov.height_lightgate2),1)
                  #--Treating these as rectangles but with very small heights
                  lightray = pygame.draw.rect(win, pract.RED,(mov.x_lightray, mov.y_lightray, mov.width_lightray, mov.height_lightray))
                  lightray2 = pygame.draw.rect(win, pract.RED,(mov.x_lightray2, mov.y_lightray2, mov.width_lightray2, mov.height_lightray2))
                  #--Drawing electromagnets as rectangles
                  electromagnet = pygame.draw.rect(win, pract.GREY,(mov.x_electromagnet, mov.y_electromagnet, mov.width_electromagnet,mov.height_electromagnet))
                  electromagnet = pygame.draw.rect(win, pract.BLACK,(mov.x_electromagnet, mov.y_electromagnet, mov.width_electromagnet,mov.height_electromagnet), 1)
                  #--Drawing to the screen the various labels at the specified x and y coordinates
                  win.blit(mov.clampStand_label, (mov.x_clampStandlabel, mov.y_clampStandlabel))
                  win.blit(mov.counterweight_label, (mov.x_counterweightlabel, mov.y_counterweightlabel))
                  win.blit(mov.lightgates_label, (mov.x_lightgateslabel, mov.y_lightgateslabel))
                  win.blit(mov.lightgates_label, (mov.x_lightgateslabel2, mov.y_lightgateslabel2))
                  win.blit(mov.magnet_label, (mov.x_magnetlabel, mov.y_magnetlabel))
                  win.blit(mov.bearings_label, (mov.x_bearingslabel, mov.y_bearingslabel))
                  win.blit(mov.press_spacebar_label, (mov.x_press_spacebarlabel, mov.y_press_spacebarlabel))
                  win.blit(self.display_timer, (mov.x_displaytimer,mov.y_displaytimer))
                  win.blit(self.time_result, (mov.x_timerresult,mov.y_timerresult))
                  #--Prompts the user to repeat the practical
                  win.blit(mov.repeat_spacebar_label, (mov.x_press_spacebarlabel, mov.y_press_spacebarlabel))
                  #--Draws the ball bearing onscreen again
                  ball_bearing = pygame.draw.circle(win, pract.GREY,(mov.x_ball, int(mov.y_ball)), mov.radius_ball)
                  ball_bearing = pygame.draw.circle(win, pract.BLACK,(mov.x_ball, int(mov.y_ball)), mov.radius_ball,1)
                  
                  #--Displaying the buttons and text again
                  increaseheightbutton = pygame.draw.polygon(win, pract.RED, mov.coordinates_upbutton,2)
                  decreaseheightbutton = pygame.draw.polygon(win, pract.RED, mov.coordinates_downbutton,2)
                  height_1m_text = pract.fontObj_mediumsmall.render(' 1 Metre ', True, pract.BLACK, pract.WHITE)
                  win.blit(height_1m_text, (mov.x_height_1m_text, mov.y_height_1m_text))

            #--Boundaries for the graph button
            if pos[0] > 555 and pos[0]< 665 and pos[1] > 243 and pos[1]< 283:
              event = pygame.event.poll()
              #--The mouse button has to be pressed
              if event.type == pygame.MOUSEBUTTONDOWN:
                #--So enough data points are plotted on the graph
                if mov.countRepeats > 3:
                  #--Plots graph
                  plt.scatter(mov.graphTime,mov.graphHeight)
                  plt.title('Spot the anomalies and work out the gradient!')
                  plt.xlabel('Time Squared (s)^2')
                  plt.ylabel('Height (m)')
                  plt.grid(True)
                  #--Line of best fit
                  plt.plot(np.unique(mov.graphTime), np.poly1d(np.polyfit(mov.graphTime, mov.graphHeight, 1))
                                                                                   (np.unique(mov.graphTime)))
                  plt.show()
                else:
                  #--Prompts the user to repeat the practical
                  win.blit(mov.repeatText,(mov.x_repeatText,mov.y_repeatText))

            #--Boundaries for the exit button
            if pos[0] > 555 and pos[0]< 665 and pos[1] > 300 and pos[1]< 340:
              event = pygame.event.poll()
              if event.type == pygame.MOUSEBUTTONDOWN:
                #--Exits the window
                command = Quiz()
                pygame.quit()
                sys.exit()
                   
            if keys[pygame.K_SPACE]: #--Checks whether the space bar has been pressed
              pract.condition_lightgatebutton2 = False #--If so, this while loop will be ended
              mov.acceleration = 0 #--Resets acceleration and position of the ball
              mov.y_ball = 96

            for event in pygame.event.get(): 
              if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            pygame.display.update() #--Updates the display
            
          if keys[pygame.K_SPACE]: #--Checks whether the space bar has been pressed (only when the up or down button has not been pressed)
            pract.condition_lightgatebutton2 = False #--If so, this while loop will be ended
            mov.acceleration = 0 #--Resets acceleration and position of the ball
            mov.y_ball = 96
        
        else:
          mov.y_ball += mov.acceleration#--Moves the ball downwards
          mov.acceleration += 0.00161 #--Allows the acceleration of the ball to increase
          #--Displays the ball bearing again but with new coordinates
          ball_bearing = pygame.draw.circle(win, pract.GREY,(mov.x_ball, int(mov.y_ball)), mov.radius_ball)
          ball_bearing = pygame.draw.circle(win, pract.BLACK,(mov.x_ball, int(mov.y_ball)), mov.radius_ball,1)

        for event in pygame.event.get(): 
          if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        pygame.display.update() #--Updates the display

      for event in pygame.event.get(): 
        if event.type == pygame.QUIT:
          pygame.quit()
          sys.exit()
      pygame.display.update() #--Updates the display

class Quiz(): #--New class which will be used for the quiz
  def __init__(self):
    #--Creating a new window which will be identical to the old one
    self.window2 = Tk()
    self.window2.title("Physics Practical Animation and Quiz")#--Name of the window
    self.window2.geometry("1000x700") #--Sets the height and width of the tkinter window
    self.window2.configure(bg="SkyBlue2") #--Sets the background colour of the window
    self.window2.resizable(False, False) #-Tkinter window is not resizable
    
    #--Initial screen which will allow the user to click a button to begin the practical
    self.quizMaintext = Label(self.window2, text="Quiz: Determination of 'g' by a free-fall method",
                              fg=form.black,bg=form.white,font=(form.font, form.fontSizeLarge))
    self.startText = Label(self.window2, text="You will now answer 13 multiple choice questions",
                              fg=form.black,bg=form.white,font=(form.font, form.fontSizeMedium))
    self.startButton = Button(self.window2, text="Click to begin!", fg=form.black,bg=form.white,
                              font=(form.font, form.fontSizeMedium), command = self.LoadQuestions)
    
    self.quizMaintext.grid(row=0, columnspan=9, pady = 100, padx = 220) #--Main widget in the window
    self.startText.grid(row=1, column=2, columnspan = 5,pady = 80)
    self.startButton.grid(row=2, column=4)

    self.quizArray = [] #--Array of questions and answers that will be used
    self.score = 0 #--Sets score to 0
    self.repeatAnswer = 0
    
  def LoadQuestions(self):
    with open('Quiz_Questions&Answers.csv', 'r') as Quiz_QA:
        reader = csv.reader(Quiz_QA)
        for row in reader: #--File contents are appended as a 2d array
          self.quizArray.append(row)
    print(self.quizArray)
    self.x = 1
    self.repeatAnswer +=1
    command = self.DisplayQuiz() #--Allows the quiz to run

  def DisplayQuiz(self):
    #--Removes widgets in the window
    self.quizMaintext.grid_forget()
    self.startText.grid_forget()
    self.startButton.grid_forget()
    #--Repaints the background
    self.window2.configure(bg="SkyBlue2")
    #--Questions
    self.QuestionNumber = Label(text=f' Question {self.quizArray[self.x][0]}: ', fg=form.black,bg=form.white,font=(form.font, form.fontSizeLarge))
    self.Question = Label(text=f' {self.quizArray[self.x][1]} ', fg=form.black,bg=form.white,font=(form.font, form.fontSizeLargeQuiz))
    #--Correct answer for the first question
    if self.x == 1:
      self.CorrectAnswer = Button(text=f'  {self.quizArray[self.x][2]}  ', fg=form.black,bg=form.white,font=(form.font, form.fontSizeMedium),
                                                                                                            command = self.CorrectAnswer)
    #--This solves my problem where the I couldn't click the correct answers when repeating the quiz
    if self.repeatAnswer > 1 and self.x == 1:
      self.CorrectAnswer = Button(text=f'  {self.quizArray[self.x][2]}  ', fg=form.black,bg=form.white,font=(form.font, form.fontSizeMedium),
                                                                                                           command = self.CorrectAnswer2)
    #--Correct answer for the second question
    if self.x == 2:
      self.CorrectAnswer = Button(text=f'  {self.quizArray[self.x][2]}  ', fg=form.black,bg=form.white,font=(form.font, form.fontSizeMedium),
                                                                                                           command = self.CorrectAnswer2)
    #--Correct answer for the third question
    if self.x == 3:
      self.CorrectAnswer = Button(text=f'  {self.quizArray[self.x][2]}  ', fg=form.black,bg=form.white,font=(form.font, form.fontSizeMedium),
                                                                                                           command = self.CorrectAnswer3)
    #--Correct answer for the fourth question
    if self.x == 4:
      self.CorrectAnswer = Button(text=f'  {self.quizArray[self.x][2]}  ', fg=form.black,bg=form.white,font=(form.font, form.fontSizeMedium),
                                                                                                           command = self.CorrectAnswer4)
    #--Correct answer for the fifth question
    if self.x == 5:
      self.CorrectAnswer = Button(text=f'  {self.quizArray[self.x][2]}  ', fg=form.black,bg=form.white,font=(form.font, form.fontSizeMedium),
                                                                                                           command = self.CorrectAnswer5)
    #--Correct answer for the sixth question
    if self.x == 6:
      self.CorrectAnswer = Button(text=f'  {self.quizArray[self.x][2]}  ', fg=form.black,bg=form.white,font=(form.font, form.fontSizeMedium),
                                                                                                           command = self.CorrectAnswer6)
    #--Correct answer for the seventh question
    if self.x == 7:
      self.CorrectAnswer = Button(text=f'  {self.quizArray[self.x][2]}  ', fg=form.black,bg=form.white,font=(form.font, form.fontSizeMedium),
                                                                                                           command = self.CorrectAnswer7)
    #--Correct answer for the eighth question
    if self.x == 8:
      self.CorrectAnswer = Button(text=f'  {self.quizArray[self.x][2]}  ', fg=form.black,bg=form.white,font=(form.font, form.fontSizeMedium),
                                                                                                           command = self.CorrectAnswer8)
    #--Correct answer for the ninth question
    if self.x == 9:
      self.CorrectAnswer = Button(text=f'  {self.quizArray[self.x][2]}  ', fg=form.black,bg=form.white,font=(form.font, form.fontSizeMedium),
                                                                                                           command = self.CorrectAnswer9)
    #--Correct answer for the tenth question
    if self.x == 10:
      self.CorrectAnswer = Button(text=f'  {self.quizArray[self.x][2]}  ', fg=form.black,bg=form.white,font=(form.font, form.fontSizeMedium),
                                                                                                           command = self.CorrectAnswer10)
    #--Correct answer for the eleventh question
    if self.x == 11:
      self.CorrectAnswer = Button(text=f'  {self.quizArray[self.x][2]}  ', fg=form.black,bg=form.white,font=(form.font, form.fontSizeMedium),
                                                                                                           command = self.CorrectAnswer11)
    #--Correct answer for the twelfth question
    if self.x == 12:
      self.CorrectAnswer = Button(text=f'  {self.quizArray[self.x][2]}  ', fg=form.black,bg=form.white,font=(form.font, form.fontSizeMedium),
                                                                                                           command = self.CorrectAnswer12)
    #--Correct answer for the thirteenth question
    if self.x == 13:
      self.CorrectAnswer = Button(text=f'  {self.quizArray[self.x][2]}  ', fg=form.black,bg=form.white,font=(form.font, form.fontSizeMedium),
                                                                                                           command = self.CorrectAnswer13)
    #--Incorrect Answers
    self.IncorrectAnswer1 = Button(text=f'  {self.quizArray[self.x][3]}  ', fg=form.black,bg=form.white,font=(form.font, form.fontSizeMedium),
                                                                                                           command = self.IncorrectAnswer)
    self.IncorrectAnswer2 = Button(text=f'  {self.quizArray[self.x][4]}  ', fg=form.black,bg=form.white,font=(form.font, form.fontSizeMedium),
                                                                                                           command = self.IncorrectAnswer)
    self.IncorrectAnswer3 = Button(text=f'  {self.quizArray[self.x][5]}  ', fg=form.black,bg=form.white,font=(form.font, form.fontSizeMedium),
                                                                                                           command = self.IncorrectAnswer)
    #--Randomises the order of the displayed answers
    rowchoice = [3,4,5,6]
    row1 = random.choice(rowchoice)
    #--Removing items from the list so the same coordinates cannot be used twice
    rowchoice.remove(row1)
    row2 = random.choice(rowchoice)
    rowchoice.remove(row2)
    row3 = random.choice(rowchoice)
    rowchoice.remove(row3)
    row4 = random.choice(rowchoice)
    rowchoice.remove(row4)
    
    #--Determines positioning of widgets
    self.QuestionNumber.grid(row = 1, column = 1, columnspan = 1,padx = 400, pady = 50)
    self.Question.grid(row = 2, column = 1, columnspan = 1,pady = 70)
    self.CorrectAnswer.grid(row = row1, column = 1, padx = 100,pady = 20)
    self.IncorrectAnswer1.grid(row = row2, column = 1, padx = 100,pady = 20)
    self.IncorrectAnswer2.grid(row = row3, column = 1, pady = 20)
    self.IncorrectAnswer3.grid(row = row4, column = 1, pady = 20)
    
  #--If the first question is answered correctly
  def CorrectAnswer(self):
    #--Removes all widgets in the window
    self.QuestionNumber.grid_forget()
    self.Question.grid_forget()
    self.CorrectAnswer.grid_forget()
    self.IncorrectAnswer1.grid_forget()
    self.IncorrectAnswer2.grid_forget()
    self.IncorrectAnswer3.grid_forget()
    #--Paints the background green
    self.window2.configure(bg=form.green)
    #--Prints text
    self.correctAnswerText = Label(text=f' Correct! You have gained a mark. ', fg=form.black,bg=form.white,font=(form.font, form.fontSizeLarge))
    self.correctAnswerText.grid(padx = 300, pady = 300)

    #--Increases the score by 1
    self.score += 1
    #--Allows the next question to be displayed
    self.x +=1
    #--Displays this window for 2 seconds before displaying the next question
    self.window2.after(2000, lambda: self.DisplayQuiz())
    #--Removes this text widget so the next lot of questions and answers can be displayed
    self.window2.after(2000, lambda: self.correctAnswerText.grid_forget())
    
  #--If the second question is answered correctly
  def CorrectAnswer2(self):
    #--Removes all widgets in the window
    self.QuestionNumber.grid_forget()
    self.Question.grid_forget()
    self.CorrectAnswer.grid_forget()
    self.IncorrectAnswer1.grid_forget()
    self.IncorrectAnswer2.grid_forget()
    self.IncorrectAnswer3.grid_forget()
    #--Paints the background green
    self.window2.configure(bg=form.green)
    #--Prints text
    self.correctAnswerText = Label(text=f' Correct! You have gained a mark. ', fg=form.black,bg=form.white,font=(form.font, form.fontSizeLarge))
    self.correctAnswerText.grid(padx = 300, pady = 300)
    #--Increases the score by 1
    self.score += 1
    #--Allows the next question to be displayed
    self.x +=1
    #--Displays this window for 2 seconds before displaying the next question
    self.window2.after(2000, lambda: self.DisplayQuiz())
    #--Removes this text widget so the next lot of questions and answers can be displayed
    self.window2.after(2000, lambda: self.correctAnswerText.grid_forget())

  #--If the third question is answered correctly
  def CorrectAnswer3(self):
    #--Removes all widgets in the window
    self.QuestionNumber.grid_forget()
    self.Question.grid_forget()
    self.CorrectAnswer.grid_forget()
    self.IncorrectAnswer1.grid_forget()
    self.IncorrectAnswer2.grid_forget()
    self.IncorrectAnswer3.grid_forget()
    #--Paints the background green
    self.window2.configure(bg=form.green)
    #--Prints text
    self.correctAnswerText = Label(text=f' Correct! You have gained a mark. ', fg=form.black,bg=form.white,font=(form.font, form.fontSizeLarge))
    self.correctAnswerText.grid(padx = 300, pady = 300)
    #--Increases the score by 1
    self.score += 1
    #--Allows the next question to be displayed
    self.x +=1
    #--Displays this window for 2 seconds before displaying the next question
    self.window2.after(2000, lambda: self.DisplayQuiz())
    #--Removes this text widget so the next lot of questions and answers can be displayed
    self.window2.after(2000, lambda: self.correctAnswerText.grid_forget())

  #--If the fourth question is answered correctly
  def CorrectAnswer4(self):
    #--Removes all widgets in the window
    self.QuestionNumber.grid_forget()
    self.Question.grid_forget()
    self.CorrectAnswer.grid_forget()
    self.IncorrectAnswer1.grid_forget()
    self.IncorrectAnswer2.grid_forget()
    self.IncorrectAnswer3.grid_forget()
    #--Paints the background green
    self.window2.configure(bg=form.green)
    #--Prints text
    self.correctAnswerText = Label(text=f' Correct! You have gained a mark. ', fg=form.black,bg=form.white,font=(form.font, form.fontSizeLarge))
    self.correctAnswerText.grid(padx = 300, pady = 300)
    #--Increases the score by 1
    self.score += 1
    #--Allows the next question to be displayed
    self.x +=1
    #--Displays this window for 2 seconds before displaying the next question
    self.window2.after(2000, lambda: self.DisplayQuiz())
    #--Removes this text widget so the next lot of questions and answers can be displayed
    self.window2.after(2000, lambda: self.correctAnswerText.grid_forget())

  #--If the fifth question is answered correctly
  def CorrectAnswer5(self):
    #--Removes all widgets in the window
    self.QuestionNumber.grid_forget()
    self.Question.grid_forget()
    self.CorrectAnswer.grid_forget()
    self.IncorrectAnswer1.grid_forget()
    self.IncorrectAnswer2.grid_forget()
    self.IncorrectAnswer3.grid_forget()
    #--Paints the background green
    self.window2.configure(bg=form.green)
    #--Prints text
    self.correctAnswerText = Label(text=f' Correct! You have gained a mark. ', fg=form.black,bg=form.white,font=(form.font, form.fontSizeLarge))
    self.correctAnswerText.grid(padx = 300, pady = 300)
    #--Increases the score by 1
    self.score += 1
    #--Allows the next question to be displayed
    self.x +=1
    #--Displays this window for 2 seconds before displaying the next question
    self.window2.after(2000, lambda: self.DisplayQuiz())
    #--Removes this text widget so the next lot of questions and answers can be displayed
    self.window2.after(2000, lambda: self.correctAnswerText.grid_forget())

  #--If the sixth question is answered correctly
  def CorrectAnswer6(self):
    #--Removes all widgets in the window
    self.QuestionNumber.grid_forget()
    self.Question.grid_forget()
    self.CorrectAnswer.grid_forget()
    self.IncorrectAnswer1.grid_forget()
    self.IncorrectAnswer2.grid_forget()
    self.IncorrectAnswer3.grid_forget()
    #--Paints the background green
    self.window2.configure(bg=form.green)
    #--Prints text
    self.correctAnswerText = Label(text=f' Correct! You have gained a mark. ', fg=form.black,bg=form.white,font=(form.font, form.fontSizeLarge))
    self.correctAnswerText.grid(padx = 300, pady = 300)
    #--Increases the score by 1
    self.score += 1
    #--Allows the next question to be displayed
    self.x +=1
    #--Displays this window for 2 seconds before displaying the next question
    self.window2.after(2000, lambda: self.DisplayQuiz())
    #--Removes this text widget so the next lot of questions and answers can be displayed
    self.window2.after(2000, lambda: self.correctAnswerText.grid_forget())
    
  #--If the seventh question is answered correctly
  def CorrectAnswer7(self):
    #--Removes all widgets in the window
    self.QuestionNumber.grid_forget()
    self.Question.grid_forget()
    self.CorrectAnswer.grid_forget()
    self.IncorrectAnswer1.grid_forget()
    self.IncorrectAnswer2.grid_forget()
    self.IncorrectAnswer3.grid_forget()
    #--Paints the background green
    self.window2.configure(bg=form.green)
    #--Prints text
    self.correctAnswerText = Label(text=f' Correct! You have gained a mark. ', fg=form.black,bg=form.white,font=(form.font, form.fontSizeLarge))
    self.correctAnswerText.grid(padx = 300, pady = 300)
    #--Increases the score by 1
    self.score += 1
    #--Allows the next question to be displayed
    self.x +=1
    #--Displays this window for 2 seconds before displaying the next question
    self.window2.after(2000, lambda: self.DisplayQuiz())
    #--Removes this text widget so the next lot of questions and answers can be displayed
    self.window2.after(2000, lambda: self.correctAnswerText.grid_forget())
    
  #--If the eighth question is answered correctly
  def CorrectAnswer8(self):
    #--Removes all widgets in the window
    self.QuestionNumber.grid_forget()
    self.Question.grid_forget()
    self.CorrectAnswer.grid_forget()
    self.IncorrectAnswer1.grid_forget()
    self.IncorrectAnswer2.grid_forget()
    self.IncorrectAnswer3.grid_forget()
    #--Paints the background green
    self.window2.configure(bg=form.green)
    #--Prints text
    self.correctAnswerText = Label(text=f' Correct! You have gained a mark. ', fg=form.black,bg=form.white,font=(form.font, form.fontSizeLarge))
    self.correctAnswerText.grid(padx = 300, pady = 300)
    #--Increases the score by 1
    self.score += 1
    #--Allows the next question to be displayed
    self.x +=1
    #--Displays this window for 2 seconds before displaying the next question
    self.window2.after(2000, lambda: self.DisplayQuiz())
    #--Removes this text widget so the next lot of questions and answers can be displayed
    self.window2.after(2000, lambda: self.correctAnswerText.grid_forget())

  #--If the ninth question is answered correctly
  def CorrectAnswer9(self):
    #--Removes all widgets in the window
    self.QuestionNumber.grid_forget()
    self.Question.grid_forget()
    self.CorrectAnswer.grid_forget()
    self.IncorrectAnswer1.grid_forget()
    self.IncorrectAnswer2.grid_forget()
    self.IncorrectAnswer3.grid_forget()
    #--Paints the background green
    self.window2.configure(bg=form.green)
    #--Prints text
    self.correctAnswerText = Label(text=f' Correct! You have gained a mark. ', fg=form.black,bg=form.white,font=(form.font, form.fontSizeLarge))
    self.correctAnswerText.grid(padx = 300, pady = 300)
    #--Increases the score by 1
    self.score += 1
    #--Allows the next question to be displayed
    self.x +=1
    #--Displays this window for 2 seconds before displaying the next question
    self.window2.after(2000, lambda: self.DisplayQuiz())
    #--Removes this text widget so the next lot of questions and answers can be displayed
    self.window2.after(2000, lambda: self.correctAnswerText.grid_forget())

  #--If the tenth question is answered correctly
  def CorrectAnswer10(self):
    #--Removes all widgets in the window
    self.QuestionNumber.grid_forget()
    self.Question.grid_forget()
    self.CorrectAnswer.grid_forget()
    self.IncorrectAnswer1.grid_forget()
    self.IncorrectAnswer2.grid_forget()
    self.IncorrectAnswer3.grid_forget()
    #--Paints the background green
    self.window2.configure(bg=form.green)
    #--Prints text
    self.correctAnswerText = Label(text=f' Correct! You have gained a mark. ', fg=form.black,bg=form.white,font=(form.font, form.fontSizeLarge))
    self.correctAnswerText.grid(padx = 300, pady = 300)
    #--Increases the score by 1
    self.score += 1
    #--Allows the next question to be displayed
    self.x +=1
    #--Displays this window for 2 seconds before displaying the next question
    self.window2.after(2000, lambda: self.DisplayQuiz())
    #--Removes this text widget so the next lot of questions and answers can be displayed
    self.window2.after(2000, lambda: self.correctAnswerText.grid_forget())

  #--If the eleventh question is answered correctly
  def CorrectAnswer11(self):
    #--Removes all widgets in the window
    self.QuestionNumber.grid_forget()
    self.Question.grid_forget()
    self.CorrectAnswer.grid_forget()
    self.IncorrectAnswer1.grid_forget()
    self.IncorrectAnswer2.grid_forget()
    self.IncorrectAnswer3.grid_forget()
    #--Paints the background green
    self.window2.configure(bg=form.green)
    #--Prints text
    self.correctAnswerText = Label(text=f' Correct! You have gained a mark. ', fg=form.black,bg=form.white,font=(form.font, form.fontSizeLarge))
    self.correctAnswerText.grid(padx = 300, pady = 300)
    #--Increases the score by 1
    self.score += 1
    #--Allows the next question to be displayed
    self.x +=1
    #--Displays this window for 2 seconds before displaying the next question
    self.window2.after(2000, lambda: self.DisplayQuiz())
    #--Removes this text widget so the next lot of questions and answers can be displayed
    self.window2.after(2000, lambda: self.correctAnswerText.grid_forget())

  #--If the twelfth question is answered correctly
  def CorrectAnswer12(self):
    #--Removes all widgets in the window
    self.QuestionNumber.grid_forget()
    self.Question.grid_forget()
    self.CorrectAnswer.grid_forget()
    self.IncorrectAnswer1.grid_forget()
    self.IncorrectAnswer2.grid_forget()
    self.IncorrectAnswer3.grid_forget()
    #--Paints the background green
    self.window2.configure(bg=form.green)
    #--Prints text
    self.correctAnswerText = Label(text=f' Correct! You have gained a mark. ', fg=form.black,bg=form.white,font=(form.font, form.fontSizeLarge))
    self.correctAnswerText.grid(padx = 300, pady = 300)
    #--Increases the score by 1
    self.score += 1
    #--Allows the next question to be displayed
    self.x +=1
    #--Displays this window for 2 seconds before displaying the next question
    self.window2.after(2000, lambda: self.DisplayQuiz())
    #--Removes this text widget so the next lot of questions and answers can be displayed
    self.window2.after(2000, lambda: self.correctAnswerText.grid_forget())

  #--If the thirteenth question is answered correctly
  def CorrectAnswer13(self):
    #--Removes all widgets in the window
    self.QuestionNumber.grid_forget()
    self.Question.grid_forget()
    self.CorrectAnswer.grid_forget()
    self.IncorrectAnswer1.grid_forget()
    self.IncorrectAnswer2.grid_forget()
    self.IncorrectAnswer3.grid_forget()
    #--Paints the background green
    self.window2.configure(bg=form.green)
    #--Prints text
    self.correctAnswerText = Label(text=f' Correct! You have gained a mark. ', fg=form.black,bg=form.white,font=(form.font, form.fontSizeLarge))
    self.correctAnswerText.grid(padx = 300, pady = 300)
    #--Increases the score by 1
    self.score += 1
    #--Displays this window for 2 seconds before finishing the quiz
    self.window2.after(2000, lambda: self.EndQuiz())
    #--Removes this text widget so the next screen can be displayed
    self.window2.after(2000, lambda: self.correctAnswerText.grid_forget())
  
  #--If the user answers the question incorrectly
  def IncorrectAnswer(self):
    #--Removes all widgets in the window
    self.QuestionNumber.grid_forget()
    self.Question.grid_forget()
    self.CorrectAnswer.grid_forget()
    self.IncorrectAnswer1.grid_forget()
    self.IncorrectAnswer2.grid_forget()
    self.IncorrectAnswer3.grid_forget()
    #--Paints the background red
    self.window2.configure(bg=form.quizred)
    #--Prints the correct answer
    self.incorrectAnswerText = Label(text=f' Incorrect. The correct answer was: ', fg=form.black,bg=form.white,font=(form.font, form.fontSizeLarge))
    self.correctAnswer = Label(text=f' {self.quizArray[self.x][2]}', fg=form.black,bg=form.white,font=(form.font, form.fontSizeLarge))
    self.incorrectAnswerText.grid(row = 1, column = 2, padx = 300, pady = 150)
    self.correctAnswer.grid(row = 2, column = 2)
    #--If the user is on the final question
    if self.x == 13:
      #--Displays this window for 3 seconds before finishing the quiz
      self.window2.after(3000, lambda: self.EndQuiz())
    #--Allows the next question to be displayed
    self.x +=1
    #--Displays this window for 3 seconds before moving onto the next question
    self.window2.after(3000, lambda: self.DisplayQuiz())
    #--Removes these text widgets so the next screen can be displayed
    self.window2.after(3000, lambda: self.incorrectAnswerText.grid_forget())
    self.window2.after(3000, lambda: self.correctAnswer.grid_forget())
  
  #--Will run when the user answers the last question
  def EndQuiz(self):
    #--Repaints the window
    self.window2.configure(bg="SkyBlue2")
    #--Displays the user's score
    self.scoreText = Label(text=f' Your score was: ', fg=form.black,bg=form.white,font=(form.font, form.fontSizeLarge))
    self.scoreInteger = Label(text=f' {self.score}/13  ', fg=form.black,bg=form.white,font=(form.font, form.fontSizeLarge))
    #--Positions widgets
    self.scoreText.grid(row = 1, column = 2, padx = 400, pady = 70)
    self.scoreInteger.grid(row = 2, column = 2, pady = 60)
    
    #--Buttons that the user can press
    self.repeatQuiz = Button(text=f' Repeat Quiz ', fg=form.black,bg=form.white,font=(form.font, form.fontSizeMedium), command = self.RepeatQuiz)
    self.exitQuiz = Button(text=f' Exit Quiz ', fg=form.black,bg=form.white,font=(form.font, form.fontSizeMedium), command = self.ExitQuiz)
    self.graphProgress = Button(text=f' View Progress ', fg=form.black,bg=form.white,font=(form.font, form.fontSizeMedium), command = self.GraphProgress)
    #--Positions widgets
    self.repeatQuiz.grid(row = 4, column = 2, pady = 0)
    self.exitQuiz.grid(row = 5, column = 2, pady = 50)
    self.graphProgress.grid(row = 6, column = 2)
  
  #--Allows the user to repeat the quiz
  def RepeatQuiz(self):
    #--Removes widgets from the display
    self.repeatQuiz.grid_forget()
    self.exitQuiz.grid_forget()
    self.graphProgress.grid_forget()
    self.scoreText.grid_forget()
    self.scoreInteger.grid_forget()
    #--Clears the contents of the array so the quiz can be repeated
    self.quizArray.clear()
    #--Resets the score
    self.score = 0
    #--Repeats the quiz
    command = self.LoadQuestions()

  #--Will exit the program
  def ExitQuiz(self):
    self.window2.destroy()
    print("Program exited")
    #--Deletes this file so each student has their own progress chart
    os.remove('ScoreProgress.csv')

  #--Allows the user to view their progress over time
  def GraphProgress(self):
    #--Allows program to record the current time
    import datetime
    from datetime import date
    #--Records the current time
    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)
    #--List of times and scores
    self.progressList = []
    
    #--Appends the current time and user's score to a CSV file
    rows = [[current_time, self.score]]
    with open('ScoreProgress.csv','a', newline='') as ScoreProgress:
            writer = csv.writer(ScoreProgress)
            writer.writerows(rows) #--Rows written

    #--Writes contents of this file to a list
    with open('ScoreProgress.csv','r', newline='') as ScoreProgress:
            reader = csv.reader(ScoreProgress)
            for row in reader: #--File contents are appended as a 2d array
              self.progressList.append(row)

    del self.progressList[0] #--Deletes first item in list since this will be blank
    self.length = len(self.progressList)
    command = self.DisplayGraph()

  def DisplayGraph(self):
    #--Additional lists that data will be appended to
    Time_Scores = []
    Scores = []
    #--These variables will allow me to iterate through lists
    x = 0
    u = 0
    z = 0

    for z in range(self.length+1):
      #--Appends all the times to a list
      Time_Scores.append(self.progressList[u][0])
      #--Appends all the scores to a list
      Scores.append(self.progressList[u][1])
      #--Iterates through list
      u+=1
      if len(Time_Scores) == len(self.progressList):
        #--Converts the list of scores from strings to integers
        Scores = list(map(int, Scores))
        #--Orders the two lists so they can be plotted
        Time_Scores, Scores = zip(*sorted(zip(Time_Scores, Scores)))

        #--Graph is plotted
        plt.plot(Time_Scores, Scores, color='#444444', marker = '.', linestyle= '-')
        plt.xlabel(f"Time")
        plt.ylabel(f"Score")
        plt.title(f"Your progress:")
        plt.grid(True)
        plt.show()
        
        print("Graph drawn")
        #--For loop is broken
        break

login = Login() #--Instantiates the main class
window.mainloop()
