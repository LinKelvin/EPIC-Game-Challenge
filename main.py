#main.py

''' 
This is the main loop for the program.
TODO: Implement game
'''

import pygame
import random
import graphics
import wordProcessing

#Colours

WHITE = (255, 255, 255)
YELLOW = (219, 219, 0) #(255, 251, 0)
ORANGE = (255, 132, 0)
GREEN = (0, 140, 12)
BLUE = (0, 0, 255)
PURPLE = (92, 0, 204)
RED = (255, 0, 0)
BROWN = (115, 85, 2)
BLACK = (0, 0, 0)
colour = [WHITE, YELLOW, ORANGE, GREEN, BLUE, PURPLE, RED, BROWN, BLACK]
lightColours = [WHITE, YELLOW]
                
#Game States
MAIN_MENU = 0
LESSON = 1
TRIVIA = 2
LESSON_LEVEL_SELECTION = 3
TRIVIA_LEVEL_SELECTION = 4

#User Defined Events
TIMER = 25

#Variable used to control the flow of the story

#Used for dialog
lineNumber = 0 
selection = 0
score = 0
timer = 0

#Used for start menu
state = MAIN_MENU
beltIndex = 1

#Whether or not to end the game
quit = False


class StartMenu():
    
    def __init__(self, screen, bg_colour = BLACK):
        self.screen = screen
        self.bg_colour = bg_colour
        self.clock = pygame.time.Clock()
        self.lessonButton = graphics.Button(screen, 560, 240, 967, 390, LESSON_LEVEL_SELECTION)
        self.quizButton = graphics.Button(screen, 206, 406, 543, 543, TRIVIA_LEVEL_SELECTION)
        self.soundObj = pygame.mixer.Sound("BabySteps.wav")
        self.soundObj.play(-1, fade_ms=2000)         
        self.pushSound = pygame.mixer.Sound("Woosh.wav")
        self.mouseIsDown = False
        
    def gameLoop(self):
        done = False
        clock = pygame.time.Clock()
        while not done:
            self.updateScreen()
            done = self.processEvents()
            clock.tick(60)
            
    #Processes user inputs
    def processEvents(self):
        global state, quit           
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit = True
                return True
            if event.type == pygame.MOUSEBUTTONDOWN :
                self.mouseIsDown = True
                if self.lessonButton.isPressed():
                    self.pushSound.play()
                    self.soundObj.fadeout(3000)
                    state = self.lessonButton.getState()
                elif self.quizButton.isPressed():                     
                    self.pushSound.play()
                    self.soundObj.fadeout(3000)
                    state = self.quizButton.getState()
            else:
                self.mouseIsDown = False
                    
        return state != MAIN_MENU
    
    
    #Updates the screen
    def updateScreen(self):
        self.screen.fill(BLACK)
        graphics.setBackground(self.screen, "Menu.png")
        
        if self.quizButton.isPressed():
            if self.mouseIsDown:
                pressed = pygame.image.load("TriviaButton_Pressed.png").convert()
                self.screen.blit(pressed, [self.quizButton.getX()[0]-2,self.quizButton.getY()[0]-2])    
            else:
                hover = pygame.image.load("TriviaButton_Hover.png").convert()
                self.screen.blit(hover, [self.quizButton.getX()[0]-2,self.quizButton.getY()[0]-2])         
        elif self.lessonButton.isPressed():
            if self.mouseIsDown:
                pressed = pygame.image.load("StoryButton_Pressed.png").convert()
                self.screen.blit(pressed, [self.lessonButton.getX()[0],self.lessonButton.getY()[0]])    
            else:
                hover = pygame.image.load("StoryButton_Hover.png").convert()
                self.screen.blit(hover, [self.lessonButton.getX()[0],self.lessonButton.getY()[0]])             
            
        pygame.display.flip()
        
class LevelSelectionMenu():
    def __init__(self, screen, typeOfMenu, nextState, bg_colour = BLACK):
        self.screen = screen
        self.bg_colour = bg_colour
        self.clock = pygame.time.Clock()
        self.typeOfMenu = typeOfMenu
        self.soundObj = pygame.mixer.Sound("BabySteps.wav")
        self.soundObj.play(-1, fade_ms=2000)         
        self.mouseIsDown = False
        
        #Implement using for loop(?)
        self.level = []
        self.level.append(graphics.Button(screen, 57, 267, 340, 329, nextState))
        self.level.append(graphics.Button(screen, 57, 371, 340, 432, nextState))
        self.level.append(graphics.Button(screen, 57, 474, 340, 534, nextState))
        self.level.append(graphics.Button(screen, 57, 577, 340, 639, nextState))
        self.level.append(graphics.Button(screen, 376, 265, 660, 329, nextState))
        self.level.append(graphics.Button(screen, 376, 369, 660, 432, nextState))
        self.level.append(graphics.Button(screen, 376, 472, 660, 534, nextState))
        self.level.append(graphics.Button(screen, 697, 265, 980, 329, nextState))
        self.level.append(graphics.Button(screen, 697, 369, 980, 432, nextState))
        
        
    
    def gameLoop(self):
        done = False
        clock = pygame.time.Clock()
        while not done:
            self.updateScreen()
            done = self.processEvents()
            clock.tick(60)
            
    #Processes user inputs
    def processEvents(self):
        global state, quit, beltIndex
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit = True
                return True
            if event.type == pygame.MOUSEBUTTONDOWN :
                self.mouseIsDown = True
                for i in range(9):
                    if self.level[i].isPressed():
                        pushSound = pygame.mixer.Sound("Woosh.wav")
                        pushSound.play()                        
                        self.soundObj.fadeout(3000)
                        state = self.level[i].getState()
                        beltIndex = i+1
            else:
                self.mouseIsDown = False
        return state != self.typeOfMenu
    
    
    #Updates the screen
    def updateScreen(self):
        self.screen.fill(BLACK)
        graphics.setBackground(self.screen, "Level_Menu.png")
        
        #event = pygame.event.poll()
        for i in range(len(self.level)):
            if self.level[i].isPressed():
                if self.mouseIsDown:
                    pressed = pygame.image.load(str(i+1) + "_Pressed.png").convert()
                    self.screen.blit(pressed, [self.level[i].getX()[0],self.level[i].getY()[0]])    
                else:
                    hover = pygame.image.load(str(i+1) + "_Hover.png").convert()
                    self.screen.blit(hover, [self.level[i].getX()[0]-2,self.level[i].getY()[0]-2])             
        
        pygame.display.flip()
        
        
        
class PlayQuiz():    
    
    def __init__(self, screen, bg_colour = BLACK):
        self.screen = screen
        self.bg_colour = bg_colour
        self.questionList, self.selectionList, self.answerList, self.scoreList, self.timeList = wordProcessing.getTriviaScript("Quiz"+str(beltIndex)+".txt")        
        self.questionSequence = wordProcessing.getQuestionSequence(len(self.questionList))
        self.clock = pygame.time.Clock()
        self.emotion = "Happy"
        self.oldMousePos = pygame.mouse.get_pos()        
        pygame.mixer.init()
        self.bgMusic = ["Bomberguy.wav", "LittleTraveller.wav", "CactusLand.wav", "PinballTwo.wav", "PuzzleKid.wav"]
        self.soundObj = pygame.mixer.Sound(self.bgMusic[random.randrange(0,5)])
        self.soundObj.set_volume(0.7)
        self.soundObj.play(-1, fade_ms = 1500)
        self.correctSound = pygame.mixer.Sound("ElevatorDing.wav")
        self.incorrectSound = pygame.mixer.Sound("DoorBuzzer.wav")
        
        self.selectionButtons = []
        self.selectionButtons.append(graphics.Button(screen, 10, 534, 1040, 556, 0))
        self.selectionButtons.append(graphics.Button(screen, 10, 557, 1040, 574, 1))
        self.selectionButtons.append(graphics.Button(screen, 10, 575, 1040, 596, 2))
        self.selectionButtons.append(graphics.Button(screen, 10, 597, 1040, 614, 3))
        
    #The game loop runs while the game is not over
    def gameLoop(self):
        done = False
        clock = pygame.time.Clock()
        pygame.time.set_timer(TIMER, 1000)
        while not done:
            self.rolloverUpdate()
            done = self.processEvents()
            self.updateScreen()
            clock.tick(60)    
            
    def rolloverUpdate(self):
        global selection
        newMousePos = pygame.mouse.get_pos()
        if newMousePos != self.oldMousePos: 
            for i in range(4):        
                if self.selectionButtons[i].isPressed():
                    selection = self.selectionButtons[i].getState()
            self.oldMousePos = newMousePos
    
    #Processes user inputs
    def processEvents(self):
        global lineNumber, selection, score, timer, quit, state
        done = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
                quit = True
                return done
            
            #Processes Mouse Down events
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if lineNumber < len(self.questionList):
                    for i in range(4):
                        if self.selectionButtons[i].isPressed():
                            if selection+1 == int(self.answerList[self.questionSequence[lineNumber]]):
                                self.correctSound.play()
                                score += int(self.scoreList[self.questionSequence[lineNumber]])
                            else:
                                self.incorrectSound.play()
                            lineNumber += 1
                            timer = 0  
                else:
                    lineNumber = 0
                    score = 0
                    self.soundObj.fadeout(1000)
                    state = MAIN_MENU
                    done = True                            
                            
            
            #Processes Keyboard input
            elif event.type == pygame.KEYUP:
                #If there are still lines remaining 
                if lineNumber < len(self.questionList):
                    #Process input if there the dialog is a selection
                    if event.key == pygame.K_UP:
                        selection = max(0, selection-1)
                    elif event.key == pygame.K_DOWN:
                        selection = min(3, selection +1)
                    elif event.key == pygame.K_SPACE:
                        if selection+1 == int(self.answerList[self.questionSequence[lineNumber]]): 
                            self.correctSound.play()
                            score += int(self.scoreList[self.questionSequence[lineNumber]])
                        else:
                            self.incorrectSound.play()
                        lineNumber += 1
                        timer = 0
                else:
                    if event.key == pygame.K_SPACE:
                        lineNumber = 0
                        score = 0
                        self.soundObj.fadeout(1000)
                        state = MAIN_MENU
                        done = True
   
            #Starts trivia timer when doing a quiz
            elif event.type == TIMER:
                    timer += 1
        
        return done
    
    #Updates the screen
    def updateScreen(self):
        global lineNumber, timer
        
        self.screen.fill(WHITE)
        graphics.setBackground(self.screen, "Blackboard.jpg")
        graphics.setCharacter(self.screen, "Girl_" + self.emotion + ".png", int(((self.screen.get_width())/1.75)), 100)
        graphics.drawDialogBox(self.screen, colour[beltIndex-1], 0.65)
        
        
        #Display dialog while there is still script
        if lineNumber < len(self.questionList):
            #text = "".join(wordProcessing.processSelection(self.selectionList[lineNumber]))
            graphics.displayDialog(self.screen, self.questionList[self.questionSequence[lineNumber]], self.selectionList[self.questionSequence[lineNumber]], True, colour[beltIndex - 1], lightColours)
            
            if selection == 0:
                graphics.drawSelection(self.screen, 0)
            elif selection == 1:
                graphics.drawSelection(self.screen, 1)
            elif selection == 2:
                graphics.drawSelection(self.screen, 2)
            elif selection == 3:
                graphics.drawSelection(self.screen, 3)
            
            #Draws the timer, and updates the line number if the user fails
            self.emotion = graphics.drawTimer(self.screen, timer, int(self.timeList[self.questionSequence[lineNumber]]))

            if timer >= int(self.timeList[self.questionSequence[lineNumber]]):
                lineNumber += 1
                timer = 0
    
        else:
            graphics.displayDialog(self.screen, "The End.", "Congratulations! You have reached the end of this chapter!", False, colour[beltIndex -1], lightColours)  #Denotes the end of a chapter
        graphics.printScore(self.screen, score)
        pygame.display.flip()    
        
        
class PlayStory():
    def __init__(self, screen, bg_colour = BLACK):
        self.screen = screen
        self.bg_colour = bg_colour
        self.backgroundPictureList, self.foregroundPictureList, self.speakerProfilePictureList, self.speakerList, self.dialogList = wordProcessing.getLessonScript("Lesson"+str(beltIndex)+".txt")  
        
        self.bgMusic = ["ShinyDay.wav", "PuzzleKid.wav", "LiveTogether.wav", "AutumnAvenue.wav", "MorningRush.wav"]
        self.soundObj = pygame.mixer.Sound(self.bgMusic[random.randrange(0,5)])
        self.soundObj.play(-1, fade_ms = 1500)                
        
        self.clock = pygame.time.Clock()
        
    #The game loop runs while the game is not over
    def gameLoop(self):
        done = False
        clock = pygame.time.Clock()
        pygame.time.set_timer(TIMER, 1000)
        while not done:
            done = self.processEvents()
            self.updateScreen()
            clock.tick(60)
            
    
    #Processes user inputs
    def processEvents(self):
        global lineNumber, selection, score, timer, quit, state
        done = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
                quit = True
                return done
            
            #Processes mouse input
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if lineNumber < len(self.backgroundPictureList):
                    lineNumber += 1
                else:
                    lineNumber = 0
                    self.soundObj.fadeout(1000)
                    state = MAIN_MENU
                    done = True                    
            
            #Processes Keyboard input
            elif event.type == pygame.KEYUP:
                #If there are still lines remaining 
                if lineNumber < len(self.backgroundPictureList):
                    #Process input if there the dialog is a selection
                    if event.key == pygame.K_SPACE:
                        lineNumber+= 1
                    elif event.key == pygame.K_LEFT:
                        lineNumber -= 1
                    elif event.key == pygame.K_RIGHT:
                        lineNumber += 1
                else:
                    if event.key == pygame.K_SPACE:
                        lineNumber = 0
                        self.soundObj.fadeout(1000)
                        state = MAIN_MENU
                        done = True
   
        return done
    
    
    #Updates the screen
    def updateScreen(self):
        global lineNumber, timer
        
        self.screen.fill(WHITE)
        #Display dialog while there is still script
        if lineNumber < len(self.backgroundPictureList):
            graphics.setBackground(self.screen, self.backgroundPictureList[lineNumber])
            graphics.setCharacter(self.screen, self.foregroundPictureList[lineNumber],int(((self.screen.get_width())/3.5)), 100)
            graphics.drawDialogBox(self.screen, colour[beltIndex-1], 0.65)            
            graphics.displayDialog(self.screen, self.speakerList[lineNumber], self.dialogList[lineNumber], False, colour[beltIndex-1], lightColours)
    
        else:
            graphics.setBackground(self.screen, self.backgroundPictureList[lineNumber-1])
            graphics.setCharacter(self.screen, self.foregroundPictureList[lineNumber-1], int(((self.screen.get_width())/3.5)), 100)
            graphics.drawDialogBox(self.screen, colour[beltIndex], 0.65)            
            graphics.displayDialog(self.screen, "The End.", "Congratulations! You have reached the end of this chapter!", False, colour[beltIndex], lightColours)  #Denotes the end of a chapter
        #graphics.printScore(self.screen, score)
        pygame.display.flip()    
        

#The main loop
def main():
    screen = initializeGame()
    while not quit:
        if state == MAIN_MENU:
            menu = StartMenu(screen)
            menu.gameLoop()
        elif state == LESSON_LEVEL_SELECTION:
            selection = LevelSelectionMenu(screen, LESSON_LEVEL_SELECTION, LESSON)
            selection.gameLoop()
        elif state == TRIVIA_LEVEL_SELECTION:
            selection = LevelSelectionMenu(screen, TRIVIA_LEVEL_SELECTION, TRIVIA)
            selection.gameLoop()
        elif state == TRIVIA:
            triviaGame = PlayQuiz(screen)
            triviaGame.gameLoop()
        elif state == LESSON:
            lessonGame = PlayStory(screen)
            lessonGame.gameLoop()
    pygame.quit()
    print "Done"

#Initializes pyGame, and returns a screen for the game
def initializeGame():
    pygame.init()
    size = (1050, 750)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("For i in Python")
    return screen

main() #Runs the game