import pygame # importing pygame
import random # importing random
from time import sleep
import webbrowser
import sys  
pygame.mixer.init()
pygame.init() # stat pygame 
font = pygame.font.SysFont(None,80) # set the font for the victory screen
SCREEN_WIDTH = 800 # constant for the screen width 
SCREEN_HEIGHT = 800 # constant fo the screen height 

screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT)) # set the screen to display game

pygame.display.set_caption("Battleships") # window name

screen_rect = screen.get_rect() # get the screen window

run = True # variable for the game loop

black = (0, 0, 0)
white = (250, 250, 250)
red = (250, 0, 0)
green = (0, 250, 0)
blue = (0, 0, 250)
settingsBlue = (10, 80, 120)
skyBlue = (100, 210, 255)
colours = [black, white, red, green, blue, settingsBlue, skyBlue]  


# This line will probably be rewritten a lot so it's better as a subroutine
def imageLoader(pic):
    loadedPic = pygame.image.load(pic).convert_alpha()  # Load PNG file
    return loadedPic  # Assigns PNG to a variable

# Changes size of the PNG according to provided scale factors
def imageScaler(size, pic):
    # Obtain dimensions of PNG, multiply by factor for new width and height values
    width = int(pic.get_width() * size)
    height = int(pic.get_height() * size)
    # Transform the image using the new values
    scaledPic = pygame.transform.scale(pic, (width, height))
    return scaledPic  # Assigns PNG to a variable

# Instead of repeating subroutines I make one that runs both in one line
def imageModifier(pic, size=1):
    loadedPic = imageLoader(pic)  # Takes PNG and returns it loaded
    modifiedPic = imageScaler(
        size, loadedPic
    )  # Takes PNG and returns it scaled
    return modifiedPic

def intuitiveExit(image, imgPos, events):
  exited = False
  compareRect = image.get_rect(topleft = imgPos)
  position = pygame.mouse.get_pos()
  for event in events:
    if event.type == pygame.MOUSEBUTTONDOWN:
      if event.button == 1:  
        if not compareRect.collidepoint(event.pos):
          goBackSfx.play()
          exited = True
          return exited
# This was repeated in the button and slider class so I made it into a subroutine
# It checks for whether a button or slider knob is being pressed and returns T/F
""" Takes in a mouseState T/F private var that is outside of the method so that
the action isn't returned as True every frame but only once. Also takkes in
the PNG which iwe compare for the overlap. Finally a conditional for
whether the button should have a hold function in a case like a slider"""

class AI:
    def __init__(self):
        
       self.guessed_grid = set()

    def basic_random_guess(self):
            while True:
              # generating a random row between 0 and 9 (since board is 10x10)
              y = random.randint(0,9)
              # generating a random column between 0 and 9
              x = random.randint(0,9)
              # combining them into one coordinate
              # this represents the square the ai wants to shoot at
              guess_cordinate = y,x
              # checking if this square has already been guessed before
              # this prevents the ai from cheating or repeating moves
              if guess_cordinate not in self.guessed_grid:
                  # using recursion to try again if its already been guessed
                 # return self.basic_random_guess()
                  # return is important here otherwise the new value wont go back properly
                self.guessed_grid.add(guess_cordinate)
                return y,x

            
            # if it has not been guessed before, now we check if it is a ship
            
            return y,x

    def moderate_guess(self):
        # this is a slightly smarter ai than the easy mode
        # it still uses random numbers but increases probability
        # where ships actually exist to simulate better prediction
        self.heuristic_matrix = []  # resetting the probability board
        # generating a 10x10 matrix filled with random probability values
        for row in range(10):
            list2 = []
            for column in range(10):
                # rounding to 2 decimal places just to keep the matrix readable
                list2.append(round(random.uniform(0,10)))
            self.heuristic_matrix.append(list2)
        # increasing probability where ships are located
        # this is the heuristic element of the ai
        for row in range(10):
            for column in range(10):
               if final_boardpos[row][column] == 1:
                  self.heuristic_matrix[row][column] *= 1.1 # boosting the probability slightly (10 percent increase)
        # searching the matrix to find the highest probability value
        guess_cordinate = None
        highest_value = -1
        for row in range(10):
            for column in range(10):
                # if a larger value is found we update the guess
                if self.heuristic_matrix[row][column] > highest_value and (row,column) not in self.guessed_grid:
                    guess_cordinate = row,column
                    highest_value = self.heuristic_matrix[row][column]
        # checking if this coordinate has already been guessed
        if guess_cordinate in self.guessed_grid:
            print('already guessed that square')  # feedback for testing
            # using recursion to generate a new guess
            # return is important otherwise the new guess would not propagate back
            return self.moderate_guess()
        # if it has not been guessed before we now check if it hits a ship
        #elif guess_cordinate in self.ships_array:
            print('hit')  # indicates the ai successfully found a ship
       #
       #  else:
            # if the coordinate is not in ships_array then it must be a miss
            print('miss')
        # storing the guess so the ai cannot guess the same square again
        self.guessed_grid.add(guess_cordinate)
        # printing guessed grid helps verify behaviour during testing
       # print(self.guessed_grid)
        # returning the coordinate so other parts of the program
        # (game logic, gui, scoring etc) can use the ai's guess
        return guess_cordinate
    def hard_guess(self):
        # this is a slightly smarter ai than the easy mode
        # it still uses random numbers but increases probability
        # where ships actually exist to simulate better prediction
        heuristic_matrix = []  # resetting the probability board
        # generating a 10x10 matrix filled with random probability values
        for row in range(10):
            list1 = []
            for column in range(10):
                # rounding to 2 decimal places just to keep the matrix readable
                list1.append(round(random.uniform(0,10)))
            heuristic_matrix.append(list1)
        # increasing probability where ships are located
        # this is the heuristic element of the ai
        for row in range(10):
            for column in range(10):
               if final_boardpos[row][column] == 1:
                  heuristic_matrix[row][column] *= 1.2 # boosting the probability slightly (10 percent increase)
        # searching the matrix to find the highest probability value
        guess_cordinate = None
        highest_value = -1
        for row in range(10):
            for column in range(10):
                # if a larger value is found we update the guess
                if heuristic_matrix[row][column] > highest_value and (row,column) not in self.guessed_grid:
                    guess_cordinate = row,column
                    highest_value = heuristic_matrix[row][column]
        # checking if this coordinate has already been guessed
        if guess_cordinate in self.guessed_grid:
            print('already guessed that square')  # feedback for testing
            # using recursion to generate a new guess
            # return is important otherwise the new guess would not propagate back
            return self.moderate_guess()
        # if it has not been guessed before we now check if it hits a ship
        #elif guess_cordinate in self.ships_array:
            print('hit')  # indicates the ai successfully found a ship
       #
       #  else:
            # if the coordinate is not in ships_array then it must be a miss
            print('miss')
        # storing the guess so the ai cannot guess the same square again
        self.guessed_grid.add(guess_cordinate)
        # printing guessed grid helps verify behaviour during testing
       # print(self.guessed_grid)
        # returning the coordinate so other parts of the program
        # (game logic, gui, scoring etc) can use the ai's guess
        return guess_cordinate

class Button:
  def __init__(self, size, coord_x, coord_y, pic, sfxTypeBool):                 #Initialisation with scale factor and position(with separate coords as it is easier)
    self.image = imageModifier(pic, size)                          #Loaded and Scaled PNG
    self.rectangle = self.image.get_rect()                         #PNG made into a rectangle so it is easier to use
    self.rectangle.topleft = coord_x, coord_y                      #Assign the top left of the rectangles to a position, this one doesn't have to be
    self.mouseState = False                                        #centered as no math will be done to it. You can callibrate by eye
    self.sfxTypeBool = sfxTypeBool                                                               #Set a click indicator that wont be reset every iteration when using the methods
    
  def place(self, events):                                    #Method that places the button on the screen and returns feedback over interavtion (clicking)

    for event in events:
      if event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == 1:  
          if self.rectangle.collidepoint(event.pos):
            if self.sfxTypeBool == True:
              buttonSfx.play()
            else:
              goBackSfx.play()
            return True                                                

  def draw(self, screen):                                     #Displays Button on the screen
    screen.blit(self.image, (self.rectangle.x, self.rectangle.y ))

#------| Starts a Slider class |---------------------------------------------------------------------------------------------------------------------------------------------------------------------#

class Slider:
  def __init__(self, pos : tuple, size : tuple, initialVal : float, minVal : int, maxVal : int, pic,\
colours : list, containerColour : int, outlineColour : int): #Initialisation with pos(x, y), parameters(h, w),
                              #percent pos of knob on container, range bounds, PNG file, colours array, container colour index and outline colour index on list.             
    self.pos = pos                                        #The position on the screen, size of the container
    self.size = size                
    self.knob = pic                                       #The button that slides as an image (so I can use circles instead of rectangles)
    self.colours = colours                                #An array of identified colours so I don't need to input RGB values
    self.containerColourIndex = containerColour           #The idex of the colours I will use on the array of colours
    self.outlineColourIndex = outlineColour
    self.sfxValArr = [0.1, 0.2, 0.3, 0.4, 0.51, 0.6, 0.7, 0.8, 0.9]
    self.mouseState = False                               #A click vs unclicked indicator that resets each iteration that can help me with rect interaction
    
    self.sliderLeft = self.pos[0] - (self.size[0] // 2)   #Dimensions of the slider container (left, right, top)
    self.sliderRight = self.pos[0] + (self.size[0] // 2) 
    self.sliderTop = self.pos[1] - (self.size[1] // 2)    
    
    self.minVal = minVal                                  #Upper and lower bound of the slider outcome values eg. 0-100%
    self.maxVal = maxVal
    
    self.initialVal = (self.sliderRight - self.sliderLeft) * initialVal                                   #Using the percent initial value to figure out the value in terms of poition
    self.containerRect = pygame.Rect(self.sliderLeft, self.sliderTop, self.size[0], self.size[1])         #Creating the container of the slider as a rect using the private values assigned earlier
    self.knobRect = self.knob.get_rect()                                                                  #Turning the loaded circle png file into a rectangle so that it is interactable
    self.knobRect.center = ((self.sliderLeft + self.initialVal)), ((self.sliderTop + self.size[1] // 2))  #Assigning the default position of the circle

  def moveSlider(self):                                                     #Method to move the knob along the container
    #Check if the user is clicking on/trying to drag the knob
    mouseState = checkCollision(self.mouseState, self.containerRect, False)      #Check if the user is clicking on/trying to drag the knob
    if mouseState == True:                                                       #If the mouse is being clicked
        self.knobRect.centerx = pygame.mouse.get_pos()[0]                        #Set the x coords of the center of the knob to that of the mouse                                                                        

  def draw(self, smoothConditional):            #Method to place the rectangles of the container and of the knob on the screen with option to round the edges swich looks better on some themes
    pygame.draw.rect(screen, self.colours[self.containerColourIndex], self.containerRect)               #Draw the container
    if smoothConditional == True:                                                                       #If the conditional was true, draws two circles at the edges of the container
      pygame.draw.circle(screen, self.colours[self.containerColourIndex], (self.sliderLeft, self.pos[1]), self.size[1]//2)
      pygame.draw.circle(screen, self.colours[self.containerColourIndex], (self.sliderRight, self.pos[1]), self.size[1]//2)
    screen.blit(self.knob, (self.knobRect.x, self.knobRect.y)) #Draw the knob

  def fetchVal(self, lastVal):                                #Method to get the multiplier of the slider as a percentage float
    valRange = self.sliderRight - self.sliderLeft          #Work out range of possible x coords
    knobVal = self.sliderRight - self.knobRect.centerx     #Work out distance from left of the container to the moddle of the knob
    val = (valRange - knobVal) / valRange                  #Calculation for multiplier
    if val in self.sfxValArr and val != lastVal:
      sliderTickSfx.play()
    return val                                            #Return said multiplier

  def setCoords(self, valFraction):
    valRange = self.sliderRight - self.sliderLeft         
    self.knobRect.centerx = valRange * valFraction + self.sliderLeft

#------| Starts a MainMenu screen class |------------------------------------------------------------------------------------------------------------------------------------------------------------#

class MainMenu:
  def __init__(self):
    BG_unloaded = "skyBG.png"
    self.BG = imageModifier(BG_unloaded, 0.4)
    Title_unloaded = "Title.png"
    self.Title = imageModifier(Title_unloaded, 0.4)

    self.singlePlayerButton = Button(0.3, 250, 350, "SinglePlayer.png", True) 
    self.multiPlayerButton = Button(0.3, 250, 400, "MultiPlayer.png", True)
    self.settingsButton = Button(0.3, 250, 450, "Settings.png", True)
    self.quitButton = Button(0.3, 265, 500, "QuitButton.png", False)
    self.helpButton = Button(0.3, 700, 700, "Help.png", True)

  def draw(self, screen):
    screen.blit(self.BG, (0, 0))
    screen.blit(self.Title, (177, 60))
    self.singlePlayerButton.draw(screen)
    self.multiPlayerButton.draw(screen)
    self.settingsButton.draw(screen)
    self.quitButton.draw(screen)
    self.helpButton.draw(screen)

  def place(self, events):
    if self.singlePlayerButton.place(events): 
      return singlePlayer
    if self.multiPlayerButton.place(events): 
      return multiPlayer
    if self.settingsButton.place(events):
      return settings
    if self.quitButton.place(events):
      return QuitScreen()
    if self.helpButton.place(events):
      webbrowser.open('https://sites.google.com/view/group-d-battleships/home?authuser=0')
      return None
    return None

#------| Starts a SinglePlayer tab class |-----------------------------------------------------------------------------------------------------------------------------------------------------------#

class SinglePlayer():
  def __init__(self):
    
    SinglePlayerTab_unloaded = "PlayerTab.png"
    self.singlePlayerTab = imageModifier(SinglePlayerTab_unloaded, 0.4)
    SinglePlayerTitle_unloaded = "SinglePlayerTitle.png"
    self.singlePlayerTitle = imageModifier(SinglePlayerTitle_unloaded, 0.4)

    ChoiceTab_unloaded = "ChosingTab.png"
    self.choiceTab = imageModifier(ChoiceTab_unloaded, 0.4)
    DiffDropOptions_unloaded = "DiffDropOptions.png"
    self.diffOptions = imageModifier(DiffDropOptions_unloaded, 0.4)
    TurnDropOptions_unloaded = "TurnDropOptions.png"
    self.turnOptions = imageModifier(TurnDropOptions_unloaded, 0.4)
    Checkmark_unloaded = "Check1.png"
    self.checkDiff = imageModifier(Checkmark_unloaded, 0.1)
    self.checkTurn = imageModifier(Checkmark_unloaded, 0.1)
    
    self.botDifficulty = Button(0.4, 270, 350, "BotDifficulty.png", True)
    self.firstTurn = Button(0.4, 270, 400, "FirstTurn.png", True)
    self.returnToMenu = Button(0.4, 285, 450, "ReturnToMenu.png", False)
    self.playButton = Button(0.4, 510, 490, "PlayButton.png", True)

    self.checkButtonDiff1 = Button(0.4, 510, 415, "DropCheck1.png", True)
    self.checkButtonDiff2 = Button(0.4, 510, 433, "DropCheck2.png", True)
    self.checkButtonDiff3 = Button(0.4, 510, 451, "DropCheck1.png", True)
    self.checkButtonDiff4 = Button(0.4, 510, 469, "DropCheck2.png", True)

    self.checkButtonTurn1 = Button(0.4, 510, 470, "DropCheck1.png", True)
    self.checkButtonTurn2 = Button(0.4, 510, 493, "DropCheck2.png", True)
    self.checkButtonTurn3 = Button(0.4, 510, 516, "DropCheck1.png", True)
    
    self.showBotdiff = False
    self.showTurns = False
    self.difficulty = "M"
    self.turn = "P"
    

  def draw(self, screen):
    screen.blit(self.singlePlayerTab, (0, 0))
    screen.blit(self.singlePlayerTitle, (300, 260))
    self.botDifficulty.draw(screen)
    self.firstTurn.draw(screen)
    self.returnToMenu.draw(screen)
    self.playButton.draw(screen)

    if self.showBotdiff:
      screen.blit(self.choiceTab, (370, 400))
      screen.blit(self.diffOptions, (380, 410))
      self.checkButtonDiff1.draw(screen)
      self.checkButtonDiff2.draw(screen)
      self.checkButtonDiff3.draw(screen)
      self.checkButtonDiff4.draw(screen)

      if self.difficulty == "E":
        screen.blit(self.checkDiff, (512, 417))
      if self.difficulty == "M":
        screen.blit(self.checkDiff, (512, 435))
      if self.difficulty == "H":
        screen.blit(self.checkDiff, (512, 453))
      if self.difficulty == "I":
        screen.blit(self.checkDiff, (512, 471))

    if self.showTurns:
      screen.blit(self.choiceTab, (370, 455))
      screen.blit(self.turnOptions, (380, 465))
      self.checkButtonTurn1.draw(screen)
      self.checkButtonTurn2.draw(screen)
      self.checkButtonTurn3.draw(screen)

      if self.turn == "P":
        screen.blit(self.checkTurn, (513, 472))
      if self.turn == "B":
        screen.blit(self.checkTurn, (513, 495))
      if self.turn == "R":
        screen.blit(self.checkTurn, (513, 518))
      
      
  def place(self, events):
    if self.showBotdiff == False and self.showTurns == False:
      if self.returnToMenu.place(events):
        self.showBotdiff = False
        return mainMenu
      if self.botDifficulty.place(events):
        self.showBotdiff = True
      if self.firstTurn.place(events):
        self.showTurns = True
      if self.playButton.place(events):
        global ai_difficulty, current_turn
        difficulty_map = {"E": "easy", "M": "medium", "H": "hard", "I": "impossible"}
        ai_difficulty = difficulty_map.get(self.difficulty, "easy")
        current_turn_map = {"P" : "Player", "B" :"AI", "R" : "Random"}
        current_turn = current_turn_map.get(self.turn,"Player")
        return placementScreen

    elif self.showBotdiff == True and self.showTurns == False:
      if self.checkButtonDiff1.place(events):
        self.difficulty = "E"
      if self.checkButtonDiff2.place(events):
        self.difficulty = "M"
      if self.checkButtonDiff3.place(events):
        self.difficulty = "H" 
      if self.checkButtonDiff4.place(events):
        self.difficulty = "I"
      if intuitiveExit(self.choiceTab, (370, 400), events):
        self.showBotdiff = False


    elif self.showBotdiff == False and self.showTurns == True:
      if self.checkButtonTurn1.place(events):
        self.turn = "P"
      if self.checkButtonTurn2.place(events):
        self.turn = "B"
      if self.checkButtonTurn3.place(events):
        self.turn = "R" 
      if intuitiveExit(self.choiceTab, (370, 455), events):
        self.showTurns = False

    return None

#------| Starts a MultiPlayer tab class |------------------------------------------------------------------------------------------------------------------------------------------------------------#
  
class MultiPlayer():
  def __init__(self):
    pass

  def draw(self, screen):
    pass

  def place(self, screen):
    return mainMenu

#------| Starts a Settings tab class |---------------------------------------------------------------------------------------------------------------------------------------------------------------#

class Settings():
  def __init__(self):
    SettingsTab_unloaded = "SettingsTab.png"
    self.SettingsTab = imageModifier(SettingsTab_unloaded, 0.4)
    Knob_unloaded = "SliderCircle.png"
    self.knob = imageModifier(Knob_unloaded, 0.2)
    Checkmark_unloaded = "Check1.png"
    self.checkANIM = imageModifier(Checkmark_unloaded, 0.2)
    Unmute_unloaded = "SoundIcon.png"
    self.soundIcon = imageModifier(Unmute_unloaded, 0.4)
    Mute_unloaded = "MutedIcon.png"
    self.muteIcon = imageModifier(Mute_unloaded, 0.4)

    self.bgmVol = 0.5
    self.bgmVolTemp = 0.5
    self.sfxVol = 0.5
    self.sfxVolTemp = 0.5
    self.lastValBgm = 0.5
    self.lastValSfx = 0.5
    self.animVar = False
    self.animVarTemp = False

    self.bgmSlider = Slider((500, 385), (200, 15), self.bgmVol, 0, 100, self.knob, colours, 1, 0)
    self.sfxSlider = Slider((500, 422), (200, 15), self.sfxVol, 0, 100, self.knob, colours, 1, 0)
    self.animBox = Button(0.8, 320, 520, "DropCheck1.png", True)
    self.leave = Button(0.4, 600, 200, "BigX.png", False)
    self.apply = Button(0.4, 550, 570, "SettingsApply.png", True)
    
  def draw(self, screen):
    screen.blit(self.SettingsTab, (0,0))

    self.apply.draw(screen)
    self.leave.draw(screen)
    self.animBox.draw(screen)
    self.bgmSlider.draw(True)
    self.sfxSlider.draw(True)
    
    if self.bgmVolTemp == 0:
      screen.blit(self.muteIcon, (320, 370))
    elif self.bgmVolTemp > 0:
      screen.blit(self.soundIcon, (320, 370))

    if self.sfxVolTemp == 0:
      screen.blit(self.muteIcon, (320, 407))
    elif self.sfxVolTemp > 0:
      screen.blit(self.soundIcon, (320, 407))

    if self.animVarTemp == True:
      screen.blit(self.checkANIM, (328, 525))

  def place(self, events):
    if self.animBox.place(events):
      if self.animVarTemp == True:
        self.animVarTemp = False
      else:
        self.animVarTemp = True

    self.bgmSlider.moveSlider()
    self.bgmVolTemp = self.bgmSlider.fetchVal(self.lastValBgm)
    self.lastValBgm = self.bgmVolTemp
    pygame.mixer.music.set_volume(self.bgmVolTemp)

    self.sfxSlider.moveSlider()
    self.sfxVolTemp = self.sfxSlider.fetchVal(self.lastValSfx)
    self.lastValSfx = self.sfxVolTemp
    for sfx in sfxArr:
      sfx.set_volume(self.sfxVolTemp)
    
    if self.leave.place(events):
      self.bgmVolTemp = self.bgmVol
      self.lastValBgm = self.bgmVol
      self.bgmSlider.setCoords(self.bgmVol)
      self.sfxVolTemp = self.sfxVol
      self.lastValSfx = self.sfxVol
      self.sfxSlider.setCoords(self.sfxVol)
      pygame.mixer.music.set_volume(self.bgmVolTemp)
      self.animVarTemp = self.animVar
      for sfx in sfxArr:
        sfx.set_volume(self.sfxVolTemp)
      return mainMenu

    if self.apply.place(events):
      self.bgmVol = self.bgmVolTemp
      self.sfxVol = self.sfxVolTemp
      self.animVar = self.animVarTemp
      return mainMenu


#------| Starts a QuitScreen tab class |-------------------------------------------------------------------------------------------------------------------------------------------------------------#

class QuitScreen():
  def __init__(self):
    QuitTab_unloaded = "QuitTab.png"
    self.QuitTab = imageModifier(QuitTab_unloaded, 0.4)

    self.quitYes = Button(0.4, 232, 447, "QuitYes.png", False)
    self.quitNo = Button(0.4, 502, 447, "QuitNo.png", True)

  def draw(self, screen):
    screen.blit(self.QuitTab, (0, 0))
    self.quitYes.draw(screen)
    self.quitNo.draw(screen)

  def place(self, events):
    if self.quitYes.place(events):
      sleep(0.3)
      pygame.quit()
      sys.exit()
    if self.quitNo.place(events):
      return mainMenu


class PlacementScreen:

    def __init__(self):
        self.activeship = None # activeship is none
        self.old_pos = (0,0) # original pos of ships

    def place(self, events): # place the grids and ships

        global final_boardpos
        global ai_board, current_turn, game_over, selected_cell, currentScreen, mainMenu

        for event in events:
            if event.type == pygame.KEYDOWN:  # if tab is pressed reset the game
             if event.key == pygame.K_TAB:
                reset_game()
                return mainMenu
            # pick up ship
            if event.type == pygame.MOUSEBUTTONDOWN: # click the mouse
                if event.button == 1: # left click

                    for ship in ship_List: # check which ship mouse collide with
                        if ship.current_Ship().collidepoint(event.pos):

                            self.activeship = ship # set to activeship the ship the mouse clicks on
                            self.old_pos = ship.current_Ship().topleft

            # move ship
            if event.type == pygame.MOUSEMOTION: # if motion when ship is held
                if self.activeship:

                    mx,my = pygame.mouse.get_pos()
                    self.activeship.current_Ship().center = (mx,my) # get coordinates of the ship when dropped

            # drop ship
            if event.type == pygame.MOUSEBUTTONUP: # mouse unclicked

                if event.button == 1 and self.activeship:

                    snap_pos = grid.snap(self.activeship.current_Ship()) # use snap function to place ship there

                    if snap_pos:

                        self.activeship.snap(snap_pos)
                        self.activeship.placed = True # ship should now have a variable called placed = true
                        shipSnapSfx.play() # placed sound
                        if collisions(self.activeship,ship_List): # check for collisions
                            self.activeship.snap(self.old_pos) # if collisions snap to last valid position

                    else:
                        self.activeship.snap(self.old_pos)
                        
                    self.activeship = None # no ship is active


            # rotate
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_r and self.activeship: # rotation checking
                    self.activeship.rotate() # if r is pressed when ship is held rotate and play rotation shound
                    shipRotateSfx.play()
                # start battle
                if event.key == pygame.K_RETURN: # if enter is pressed and all ships are placed 

                    if placed(ship_List): # check if all ships are placed

                        final_boardpos = grid.board1(ship_List) # pos of all ships on gthe grid

                        place_ai_ships(aiship_List,ai_grid) # place all ai ships

                        ai_board = ai_grid.board1(aiship_List) # pos of all ai ships on grid

                        return gameScreen # move to game screen

        return None


    def draw(self,screen):

        screen.blit(background,(0,0))

        grid.draw(screen)

        for ship in ship_List:
            ship.draw(screen)

class GameScreen:

    def draw(self, screen): # draw grids
        global current_turn, selected_cell
        screen.blit(background,(0,0))

        grid.draw(screen) # draw player grid
        ai_grid.draw(screen) # draw ai grid

        if selected_cell: # if cell is selected to shot
          row,col = selected_cell
          x = ai_grid.x + col * ai_grid.cell_size # calc to get coordinates on the screen
          y = ai_grid.y+ row * ai_grid.cell_size
          rect = pygame.Rect(x,y,ai_grid.cell_size,ai_grid.cell_size) # draw rectangle for the cell
          pygame.draw.rect(screen,(0,255,0),rect,3)

        for ship in ship_List: # place my ships on screen
            ship.draw(screen)

        hit_miss(ai_grid,player_shots,(255,0,0),(0,0,255)) # hit miss markers
        hit_miss(grid,ai_shots,(255,0,0),(0,0,255))
        draw_sunkship(aiship_List,screen)
        draw_sunkship(ship_List,screen)
        
        if text:
           win = font.render(text,True,(255,255,255))
           screen.blit(win,(250,100))
        if current_turn == "Random":
           turn = ["Player", "AI"]
           current_turn = random.choice(turn)
    def place(self, events):

        global current_turn
        global text
        global selected_cell, game_over, currentScreen, mainMenu
        for event in events:
          if event.type == pygame.KEYDOWN: # if tab is pressed reset the game
             if event.key == pygame.K_TAB:
                reset_game()
                return mainMenu
             
          if current_turn == "Player" and not game_over: # and turn is player

            if event.type == pygame.MOUSEBUTTONDOWN: # if tile clicked
                    if ai_grid.rect.collidepoint(event.pos): # calculation of the grid position

                        mousex,mousey = event.pos

                        col = (mousex - ai_grid.x) // ai_grid.cell_size
                        row = (mousey - ai_grid.y) // ai_grid.cell_size

                        selected_cell = (row,col) # store  the tile
            if event.type == pygame.KEYDOWN:
              if event.key == pygame.K_SPACE and selected_cell: # if space is pressed and a tile is selected
                  row,col = selected_cell
                  result = player_shot(row,col) # shoot the tile
                  if result is None:
                      return None
                  selected_cell = None 
                  if all_sunk(aiship_List): # check if all the ships are sunk 
                      text = "PLAYER WINS"
                      game_over = True
                  if result == "MISS":
                      current_turn = "AI"

        if current_turn == "AI" and not game_over: # ai turn

            pygame.time.wait(500) # pause
            
            if ai_difficulty == "easy":
               row,col = ai_player.basic_random_guess() # a
            elif ai_difficulty == "medium":
               row,col = ai_player.moderate_guess()
            elif ai_difficulty == "hard":
              row,col = ai_player.hard_guess()
            else:
               row,col = ai_player.basic_random_guess()

            result = ai_shot(row,col)
            if result is None:
               return None
            if all_sunk(ship_List):
                text = "AI WINS"
                game_over = True
            if result == "MISS":
                current_turn = "Player"

        return None

class Ship: #initialize the ship class
    def __init__(self, image, position,grid,length): # attribute are image and position
        self.length = length # this identifies the length of the ship
        self.grid = grid # this is the grid
        actual_image = image.get_bounding_rect() # get the actual image pixels
        unscaledimage = image.subsurface(actual_image)# remove the backgrfound surface
        cell = grid.cell_size# scaling the image
        height = cell * self.length
        width = cell
        self.image = pygame.transform.smoothscale(unscaledimage,(width,height)) # scaled image
        self.rect = self.image.get_rect(topleft=position) # get the rectangle of the image and set its top left position
        self.rotated_Image = pygame.transform.rotate(self.image, 90) # rotate the image by 90 
        self.rotated_Rect = self.rotated_Image.get_rect(center=self.rect.center) # get the rectangle of the rotated image and set its center to the center of the original rectangle
        self.rotated = False # ship not initially rotated
        self.placed = False # placed on grid variable
        self.hits = 0 # hit detection variable

      
    def draw(self, screen): # method to draw the ship on the surface
        if self.rotated: # if ship is rotated
            screen.blit(self.rotated_Image, self.rotated_Rect) # draw rotated image on the screen
        else: # if ship not rotated
            screen.blit(self.image, self.rect) # draw normal image on the screen
   
    def move(self, rel): # move method
        if self.rotated: # check if the ship is rotated
            rect = self.rotated_Rect # ship to move is the rotated one
        else: # if the image is the normal one
            rect = self.rect # ship to move is the normal one
        rect.move_ip(rel) # move the image on the screen
        rect.clamp_ip(screen_rect) # keep the ship on the screen

    def snap(self, position): # snapping the image unto the grid
        if self.rotated: # check if the ship is rotated
            rect = self.rotated_Rect # ship to snap is the rotated one
        else: # if the image is the normal one
            rect = self.rect # ship to snap is the normal one
        rect.topleft = position # snapping postion
    
    def rotate(self): # rotate the image
        self.rotated = not self.rotated # change the image orientation
        if self.rotated: # if rotated
            self.rotated_Rect.center = self.rect.center # change center to normal image center
        else: # if normal
            self.rect.center = self.rotated_Rect.center # leave the center as normal

    def current_Ship(self): # get the current ship
        if self.rotated: # if rotated 
            return self.rotated_Rect # use rotated ship
        else: # if normal
            return self.rect # use normal ship
    
    def hit(self): # hit method
        self.hits+= 1 # when called increase hit
        if self.hits == self.length: # if the hit equal the lenght return true
            return True
        return False


class Grid: # initialize the grid class
    def __init__(self, x = 10, y =200, cell_size = 35, size = 10):
        self.x = x # size of cell
        self.y = y
        self.cell_size = cell_size # size of cell
        self.size = size # number of cells
        self.rect = pygame.Rect(self.x, self.y, self.size * self.cell_size,self.size* self.cell_size) # draw rectangle
    
    def board1(self,ship_List): # the board for tracking ship hit and miss
        board = [[0 for _ in range(self.size)] for _ in range(self.size)] # grid of 0s
        for ship in ship_List: # loop through the list of shiips and append their postions onto the board
            for row, col in self.getcells(ship):
                if 0 <= row < self.size and 0 <= col < self.size: # checks if the current cell is equal to zero and updates it to 1
                    board[row][col] = 1
        return board


    def getcells(self,ship): # get the cells of the ships to know its placement
        rect = ship.current_Ship() # current ship
        cell = self.cell_size
        col = (rect.x - self.x) // cell # calc row and column
        row = (rect.y - self.y) // cell 
        cells = [] # store cells
        if ship.rotated:
            for i in range(ship.length):
                cells.append((row , col + i))
        else:
            for i in range(ship.length):
                cells.append((row + i,col))

        return cells




    def draw(self,surface):
        white = (255,255,0)
        x_pos = self.x # starting postiong for the line
        for i in range(self.size + 1):
            pygame.draw.line(surface,white,(x_pos,self.y),(x_pos, self.y+self.size * self.cell_size))
            x_pos += self.cell_size # move to the next line

        y_pos = self.y # start of y on grid
        for i in range(self.size+1):
            pygame.draw.line(surface,white,(self.x,y_pos),(self.x + self.size * self.cell_size, y_pos))
            y_pos += self.cell_size

    def snap(self,ship_rect): # snapping method
        if not self.rect.collidepoint(ship_rect.topleft): # check if mouse clicks on image
            return None
          
        col = (ship_rect.x - self.x) // self.cell_size # math to get the rounded cell row and column
        row = (ship_rect.y - self.y) // self.cell_size

        snap_x = self.x + col * self.cell_size # using the coordinates find the position on the grid
        snap_y = self.y + row * self.cell_size

        if snap_x + ship_rect.width > self.x + (self.size * self.cell_size):
            return None # Too far right!
        if snap_y + ship_rect.height > self.y + (self.size * self.cell_size):
            return None # Too far down! 




        return (snap_x,snap_y) # return postion of cells


def collisions(ship, ship_List): # check for collisions
    current = ship.current_Ship()
    for other in ship_List: # loop through all the ship in the list
        if other == ship: 
            continue 
        if current.colliderect(other.current_Ship()): # check is 2 ships collide
            return True
    return False 


def placed(ship_List):
    for i in ship_List: # check is all ships are placed
        if i.placed == True :
            continue
        else:
            return False 
    return True


def place_ai_ships(ai_ships, ai_grid):
    for ship in ai_ships: # loops through ai ship list
        valid_position = False # set valid position to false

        while not valid_position:
            ship.rotated = random.choice([True, False]) # choose random orientation

            row = random.randint(0, ai_grid.size - 1) # random cell location
            col = random.randint(0, ai_grid.size - 1)

            x = ai_grid.x + col * ai_grid.cell_size # postion on the screen in pixels
            y = ai_grid.y + row * ai_grid.cell_size

            ship.snap((x, y)) # snap to the postion on screen

            valid_position = True # set vslid postion to true 

            # Check inside grid
            for r, c in ai_grid.getcells(ship): # place the ship on the board used for hit and miss
                if not (0 <= r < ai_grid.size and 0 <= c < ai_grid.size):
                    valid_position = False

            # Check collision with other AI ships
            if collisions(ship, ai_ships):
                valid_position = False


def player_shot(row,col):
    if player_shots[row][col] != 0: # check where the player hit if it is not hit before
        return None 
    if ai_board[row][col] == 1: # if ship is there register hit
        player_shots[row][col] = 2 # mark on the shots board the hit
        for ship in aiship_List:
            if (row,col) in ai_grid.getcells(ship):# find the ship in that position and call the ship hit method
                sunk = ship.hit()
                if sunk:
                    print("AI ship sunk")
        return "HIT"
    else:
        player_shots[row][col] = 3 # register miss
        return "MISS"
    
def ai_shot(row,col):
    while True:
        if ai_shots[row][col] != 0: # check if pos has been hit before
            return None
        if final_boardpos[row][col] == 1: # check if there is a ship there
            ai_shots[row][col] = 2 # change shots board to 2 for hit
            for ship in ship_List:
                if (row,col) in grid.getcells(ship):# find the ship in that position and call the ship hit method
                    sunk = ship.hit()
                    if sunk:
                        print("player ship sunk")
            
            return "HIT"
        else:
            ai_shots[row][col] = 3
            return "MISS" # register miss

def hit_miss(grid,shots,hit,miss):
    for r in range(grid.size): # loop through the grid
        for c in range(grid.size):
            if shots[r][c] == 0: # if 0 no ship
                continue
            x = grid.x + c * grid.cell_size # find x and y on screen in pixels
            y = grid.y + r * grid.cell_size

            rect = pygame.Rect(x,y,grid.cell_size,grid.cell_size) # variable to draw a rectangel for hit and miss

            if shots[r][c] == 2 : # if hit draw hit rectangle
                pygame.draw.rect(screen,hit,rect)

            if shots[r][c] == 3 : # if miss draw miss rectangle
                pygame.draw.rect(screen,miss,rect)

def all_sunk(ship_list): # check if all ships have been sunk
    for ship in ship_list:
        if ship.hits < ship.length:
            return False
    return True       


def checkCollision(mouseState, rectangle, unclickConditional = True):
    position = pygame.mouse.get_pos()
    action = False
    if rectangle.collidepoint(position):
        if pygame.mouse.get_pressed()[0] == 1 and mouseState == False:
            mouseState = True
            action = True
    if unclickConditional == True:
      if pygame.mouse.get_pressed()[0] == 0:
        mouseState = False
      return mouseState, action
    else:
        return mouseState    


def draw_sunkship(list,screen): # draw sunk ships
   
   for ship in list: # loop throught the list of ships
      if ship.hits == ship.length: # check if sunk
        if ship.rotated:# check orientation
           screen.blit(ship.rotated_Image,ship.rotated_Rect)
           rect = ship.rotated_Rect
        else:
           screen.blit(ship.image,ship.rect)
           rect = ship.rect

        overlay = pygame.Surface((rect.width,rect.height), pygame.SRCALPHA) # add overlay
        overlay.fill((0,0,0,150)) # make overlay dark
        screen.blit(overlay,rect.topleft) # blit onto screen


def reset_game():

    global ship_List, aiship_List
    global player_shots, ai_shots
    global selected_cell
    global placement_finish
    global current_turn
    global game_over
    global text

    # reset ships
    ship_List =[ # list of the ships
    Ship(image1, (500,200),grid,1),
    Ship(image1, (400,200),grid,1),
    Ship(image1, (700,200),grid,1),
    Ship(image1, (600,200),grid,1),
    Ship(image2, (550,300),grid,2),
    Ship(image2, (450,300),grid,2),
    Ship(image2, (650,300),grid,2),
    Ship(image3, (600,400),grid,3),
    Ship(image3, (500,400),grid,3),
    Ship(image4, (550,500),grid,4),  
]

    aiship_List =[ # list of the ships
    Ship(image1, (0,0),ai_grid,1),
    Ship(image1, (0,0),ai_grid,1),
    Ship(image1, (0,0),ai_grid,1),
    Ship(image1, (0,0),ai_grid,1),
    Ship(image2, (0,0),ai_grid,2),
    Ship(image2, (0,0),ai_grid,2),
    Ship(image2, (0,0),ai_grid,2),
    Ship(image3, (0,0),ai_grid,3),
    Ship(image3, (0,0),ai_grid,3),
    Ship(image4, (0,0),ai_grid,4),  
]

    # reset shot boards
    player_shots = [[0 for _ in range(ai_grid.size)] for _ in range(ai_grid.size)]
    ai_shots = [[0 for _ in range(grid.size)] for _ in range(grid.size)]

    # reset gameplay
    selected_cell = None
    placement_finish = False
    current_turn = "Player"
    game_over = False
    text = ""


background = pygame.image.load("GameplayBG.webp").convert()
background = pygame.transform.scale(background,(SCREEN_WIDTH,SCREEN_HEIGHT))

image1 = imageModifier("realship1.webp")
image2 = imageModifier("realship2.webp")
image3 = imageModifier("realship3.webp")
image4 = imageModifier("realship4.webp")


BG = imageModifier("skyBG.png").convert()
BG = pygame.transform.scale(BG,(SCREEN_WIDTH,SCREEN_HEIGHT))
Title = imageModifier("Title.png",0.7)

pygame.mixer.music.load("【東方・Bossa Nova 】Close to your Mind『ShibayanRecords』.mp3")
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.5)

#------| setting sfx |-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

buttonSfx = pygame.mixer.Sound("generic-button.ogg")
sliderTickSfx = pygame.mixer.Sound("slider-tick.ogg")
goBackSfx = pygame.mixer.Sound("undo.ogg")
shipSnapSfx = pygame.mixer.Sound("place-ship.ogg")
shipRotateSfx = pygame.mixer.Sound("place-ship.ogg")

sfxArr = [buttonSfx, sliderTickSfx, goBackSfx, shipSnapSfx, shipRotateSfx]

for sfx in sfxArr:
  sfx.set_volume(0.5)

grid = Grid() # player grid

ai_grid = Grid(400,200) # ai grid


ship_List =[ # list of the ships
    Ship(image1, (500,200),grid,1),
    Ship(image1, (400,200),grid,1),
    Ship(image1, (700,200),grid,1),
    Ship(image1, (600,200),grid,1),
    Ship(image2, (550,300),grid,2),
    Ship(image2, (450,300),grid,2),
    Ship(image2, (650,300),grid,2),
    Ship(image3, (600,400),grid,3),
    Ship(image3, (500,400),grid,3),
    Ship(image4, (550,500),grid,4),  
]


aiship_List =[ # list of the ships
    Ship(image1, (0,0),ai_grid,1),
    Ship(image1, (0,0),ai_grid,1),
    Ship(image1, (0,0),ai_grid,1),
    Ship(image1, (0,0),ai_grid,1),
    Ship(image2, (0,0),ai_grid,2),
    Ship(image2, (0,0),ai_grid,2),
    Ship(image2, (0,0),ai_grid,2),
    Ship(image3, (0,0),ai_grid,3),
    Ship(image3, (0,0),ai_grid,3),
    Ship(image4, (0,0),ai_grid,4),  
]

current_turn = None # current player turn

ai_shots = [[0 for _ in range(ai_grid.size)] for _ in range(ai_grid.size)] # ai shots at player board
player_shots = [[0 for _ in range(grid.size)] for _ in range(grid.size)] # player shots at ai board

placement_finish = False # variable holding placement mode
old_pos = (0,0) # old pos
activeship = None # current ship is set to none 
text = None # display text is set to none
clock = pygame.time.Clock()

mainMenu = MainMenu()
singlePlayer = SinglePlayer()
multiPlayer = MultiPlayer()
settings = Settings()
gameScreen = GameScreen()
placementScreen = PlacementScreen()
ai_difficulty = None
currentScreen = mainMenu
redirect = None
game_over = False
ai_player = AI()
selected_cell = None

while run:

    events = pygame.event.get()

    for event in events:
        if event.type == pygame.QUIT:
            run = False

    redirect = currentScreen.place(events)

    if redirect:
        currentScreen = redirect

    currentScreen.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()