# import time and pygame and initalize pygame
import time 
import pygame, sys
from pygame.locals import * 
pygame.init()

# set the screen size
screen = pygame.display.set_mode((800, 640))

# define image variable 
background_img = pygame.image.load("city_background.jpg")
hospital_img = pygame.image.load("hospital.png")
icon_img = pygame.image.load("virus.png")
sick_man_img = pygame.image.load("sick_man.png")
# initialize coordinates for the start pos for sick_man_img
sick_man_xpos = -64
sick_man_ypos = 435
doctor_img = pygame.image.load("64_doctor.png")
hospital_bed_img = pygame.image.load("64_hospital_bed.png")
money_img = pygame.image.load("64_money.png")
happy_person_img = pygame.image.load("happy.png")
# initalize coordinated for the start pos for happy_person_img
happy_person_xpos = 240
happy_person_ypos = 435

# change caption of screen 
pygame.display.set_caption("Virus Idle")
# change icon of screen 
pygame.display.set_icon(icon_img)

# draw text function that allows you to insert text on the screen 
def draw_text(text, font_size, color, surface, x,y):
    font = pygame.font.SysFont(None, font_size)
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

# create a button class
class button():
    def __init__(self, color, x, y, width, height, text = ""):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
    # create draw function
    def draw(self, screen, outline = None):
        if outline:
            pygame.draw.rect(screen, outline, (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 0)
            
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height), 0)
        
        if self.text != "":
            font = pygame.font.SysFont("Comicsans", 30)
            text = font.render(self.text, 1, (0, 0, 0))
            screen.blit(text, (self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2)))
            
    # create function that checks to see if the mouse pointer is over the button 
    def isOver(self, pos):
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True
        return False 

# initalize buttons
upgrade_doctors = button((255, 255, 255), 400, 550, 145, 45, "Doctors")
upgrade_hospital_beds = button((255, 255, 255), 600, 550, 145, 45, "Hospital Beds")
start_button = button((255, 255, 255), 75, 550, 145, 45, "Start Game")
rules_button = button((255, 255, 255), 325, 550, 145, 45, "How to Play")
info_button = button((255, 255, 255), 575, 550, 145, 45, "COVID-19 INFO")

##### MAIN MENU FUNCTION #####
# initialize click to false
click = False
def main_menu():
    # create while loop to run main menu 
    while True:
        # draw the background for te main menu 
        screen.blit(background_img, (0, 0))
        screen.blit(hospital_img, (220, 241))
        # type title for the main menu 
        draw_text("Virus Idle", 50, (0, 0, 0), screen, 300, 20)
        
        
        ##### DRAW OUT THE SELECTION BUTTONS #####
        start_button.draw(screen, (0, 0, 0))
        rules_button.draw(screen, (0, 0, 0))
        info_button.draw(screen, (0, 0, 0))
        
        click = False
        # create an event loop for the main menu
        # when you enter "esc" on keyboard code will end 
        for event in pygame.event.get():
            # track mouse position
            pos = pygame.mouse.get_pos()
            
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit
            
            # if user clicks on one of the selection buttons
            if event.type == MOUSEBUTTONDOWN:
                # game button
                if start_button.isOver(pos):
                    # call game function
                    game()
                if rules_button.isOver(pos):
                    # call rules functon
                    game_rules()
                if info_button.isOver(pos):
                    # call info function
                    covid_info()
                    
             # if user hovers over the selection buttons
            if event.type == pygame.MOUSEMOTION:
                # game button
                if start_button.isOver(pos):
                    start_button.color = (0, 255, 0)
                else:
                    start_button.color = (255, 255, 255)
                # rules button 
                if rules_button.isOver(pos):
                    rules_button.color = (0, 255, 0)
                else:
                    rules_button.color = (255, 255, 255)
                # info button
                if info_button.isOver(pos):
                    info_button.color = (0, 255, 0)
                else:
                    info_button.color = (255, 255, 255)
            
                    
        pygame.display.update()

##### GAME FUNCTION #####
# runs all code for the game
def game():
    ##### INITALIZE SET OF VARIABLES #####
    # display counters 
    num_patients = 0
    num_doctors = 0
    num_hospital_beds = 0
    current_money = 100
    # purchase cost
    cost_doctors = 50
    cost_hospital_beds = 35
    # time spent in hospital formula numbers 
    percent_decrease_doc = .714
    percent_decrease_bed = .306
    # varibales that update after every round 
    increase_money_by = 100
    round_num = 1
    num_iterations = 0
    people_per_round = 10
    sick_person_speed = 1
    # make a empty list, so when a sick person reaches the hospital they added to the list 
    patient_list = []
    
    running = True
    # create while loop to start game
    while running:
        # change background
        screen.blit(background_img, (0, 0))
        screen.blit(hospital_img, (220, 241))
        # display title for the game
        draw_text("Lets Play Virus Idle!", 50, (0, 0, 0), screen, 230, 20)
        
        ###### ROUND NUMBER #####
        # first round is going to be first 10 sick people
        # rounds are based on the number of times a sick person goes into a hospital
        # if num_iterations == the determined people per round 
        if num_iterations == people_per_round:
            # round number increases 
            round_num += 1
            # amount of money earned for healing someone increases 
            increase_money_by *= 1.1
            # number of people per round increases by 5
            people_per_round += 5
            # the speed of the sick person increases 
            sick_person_speed *= 1.1
            # change num iterations back to o so we can count up to 15 and so on
            num_iterations = 0
        
        # create a loop so that the sick person continues to move accross the screen until he gets to the hospital
        global sick_man_xpos
        if sick_man_xpos < 230:
            sick_man_xpos += sick_person_speed
        elif sick_man_xpos >= 230:
            num_patients += 1
            num_iterations += 1
            start_time = time.time()
            patient_list.append(start_time)
            sick_man_xpos = -64    
        
        # create formula that determines how long until a sick patient leaves
        # player has to buy atleast one doctor and one hospital bed until the patients can start being treated
        if num_doctors >= 1 and num_hospital_beds >= 1:
            time_spent_formula = 15.3 / (percent_decrease_doc + percent_decrease_bed)
        else: # If player has not bought both a hospital bed and doctor
            time_spent_formula = 100000
        
        # we are going to loop over every "patient" on the list
        # check how long they have been on the list by finding the current time 
        # compare it to the amount_of_time_in_hospital formula
        # and if that patient has been in the hospital for that x amount of time
        # we will remove them and update num_patients
        current_time = time.time()
        # if len patient_list >= 1:
        if len(patient_list) >= 1:
            for patient in range(len(patient_list) - 1):
                # checking each patient/time in list to see how long they have been in the list/hospital for
                time_spent_in_hospital = current_time - patient_list[patient]
                # if they have been in the list/hospital for the time it take to heal a patient
                if time_spent_in_hospital >= time_spent_formula:
                    # let the healed person leave the hospital 
                    # happy_person(50,50)
                    # they are removed from the list/hospital
                    patient_list.pop(patient)
                    # num_patients in hospital decreases
                    num_patients -= 1
                    # you earn x amount of money depending on which round player is on
                    current_money += increase_money_by
        
        ##### DISPLAY UPGRADE BUTTONS #####
        # display doctors button
        upgrade_doctors.draw(screen, (0, 0, 0))
        # display hospital beds button
        upgrade_hospital_beds.draw(screen, (0, 0, 0))
            
        # start event loop to play the game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # if user enters "esc" on keyborad you will be put back to main menu or if on main menu it will exit game
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                    
            # get mouse position
            pos = pygame.mouse.get_pos()
                    
            # if user clicks on a upgrade button
            if event.type == pygame.MOUSEBUTTONDOWN:
                # if user clicks on doctors button
                if upgrade_doctors.isOver(pos) and current_money >= cost_doctors:
                    # update num_doctors counter
                    num_doctors += 1
                    # decrease current_money by the cost to buy a doctor
                    current_money -= cost_doctors
                    # increase the cost to buy a docotr
                    cost_doctors *= 1.2
                    # round cost_doctor so its a 2 decimal number
                    cost_doctors = round(cost_doctors, 2)
                    # increase the amount of time doctors subrtact from the total time patients stay in hospital
                    percent_decrease_doc *= 1.03

                # if user clicks on hospital beds button 
                if upgrade_hospital_beds.isOver(pos) and current_money >= cost_hospital_beds:
                    # update num_hospital_beds 
                    num_hospital_beds += 1
                    # decrease amont of money player has by the cost to buy a hospital bed
                    current_money -= cost_hospital_beds
                    # increase the cost to buy a hospital bed
                    cost_hospital_beds *= 1.2
                    # round the cost of hospital beds so its a 2 decimal number
                    cost_hospital_beds = round(cost_hospital_beds, 2)
                    # increase the amount of time hospital beds subtract from the total time patients stay in hospital
                    percent_decrease_bed *= 1.03
                    
            # if user hovers over the button
            if event.type == pygame.MOUSEMOTION:
                # hovers over doctors button and player has enough money to buy
                if upgrade_doctors.isOver(pos) and current_money >= cost_doctors:
                    # button turns green
                    upgrade_doctors.color = (0, 255, 0)
                # hovers over doctors button but they do not have enough money
                elif upgrade_doctors.isOver(pos) and current_money < cost_doctors:
                    # button turns red 
                    upgrade_doctors.color = (255, 0, 0)
                else: # not hovering over button
                    # button is white
                    upgrade_doctors.color = (255, 255, 255)
                # hovers over hospital beds button and player has enough money to buy it
                if upgrade_hospital_beds.isOver(pos) and current_money >= cost_hospital_beds:
                    # button turns green
                    upgrade_hospital_beds.color = (0, 255, 0)
                # hovers over hospital beds button but player does not have enough money 
                elif upgrade_hospital_beds.isOver(pos) and current_money < cost_hospital_beds:
                    # button turns red
                    upgrade_hospital_beds.color = (255, 0, 0)
                else: # not hovering over button
                    # button is white
                    upgrade_hospital_beds.color = (255, 255, 255)
        
        # call sick_person function
        sick_person(sick_man_xpos, sick_man_ypos)
        
        ##### DISPLAY COUNTERS #####
        # make a display that shows the round number
        draw_text("Round: ", 45, (255, 255, 255), screen, 40, 555)
        draw_text(str(round_num), 40, (255, 255, 255), screen, 150, 555)
        # make a display that shows the number of patients in the hospital
        draw_text("Number of Patients: ", 30, (0, 0, 0), screen, 85, 75)
        draw_text(str(num_patients), 35, (0, 0, 0), screen, 295, 72)
        # make a display that shows the number of doctors your hospital has
        draw_text("Number of Doctors: ", 30, (0, 0, 0), screen, 85, 160)
        draw_text(str(num_doctors), 35, (0, 0, 0), screen, 295, 157)
        # make a display that shows the number of hospital beds
        draw_text("Number of Hospital Beds: ", 30, (0, 0, 0), screen, 425, 75)
        draw_text(str(num_hospital_beds), 35, (0, 0, 0), screen, 685, 72)
        # Make a dispaly that shows the amount of money user has
        draw_text("Money: $", 30, (0, 0, 0), screen, 425, 160)
        draw_text(str(round(current_money, 2)), 35, (0, 0, 0), screen, 515, 157)
        
        # make a display that shows the cost of doctors and hospital beds
        draw_text("Upgrades: ", 45, (255, 255, 255), screen, 230, 555)
        draw_text("Cost: $", 30, (255, 255, 255), screen, 400, 605)
        draw_text(str(cost_doctors), 30, (255, 255, 255), screen, 472, 605)
        draw_text("Cost: $", 30, (255, 255, 255), screen, 600, 605)
        draw_text(str(cost_hospital_beds), 30, (255, 255, 255), screen, 672, 605)
        
        ##### DISPLAY ICONS NEXT TO COUNTERS #####
        # Icon for number of patients 
        screen.blit(sick_man_img, (15, 50))
        # icon for number of hospital beds
        screen.blit(doctor_img, (15, 140))
        # icon for hospital beds
        screen.blit(hospital_bed_img, (351, 50))
        # icon for money
        screen.blit(money_img, (351, 140))
        
        pygame.display.update()
        
##### GAME RULES FUNCTION #####
# runs all code for game rules 
def game_rules():
    running = True
    # create while loop for game rules
    while running:
        # change background
        screen.blit(background_img, (0, 0))
        screen.blit(hospital_img, (220, 241))
        # display title for the game
        draw_text("How To Play", 50, (0, 0, 0), screen, 300, 20)
        draw_text("You just got put in charge of a hospital and a deadly virus has appeared.", 33, (0, 0, 0), screen, 17, 70)
        draw_text("You will have $100 so first buy one doctor and one hospital bed.", 33, (0, 0, 0), screen, 17, 105)
        draw_text("You will earn money for treating your patients.", 33, (0, 0, 0), screen, 17, 140)
        draw_text("As the pandemic goes on, the faster sick people arrive at your hospital.", 33, (0, 0, 0), screen, 17, 175)
        draw_text("Buy more doctors and hospital beds in order to treat your patients quicker.", 33, (0, 0, 0), screen, 17, 210)
        
        # start event loop to play the game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # if user enters "esc" on keyborad you will be put back to main menu 
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                    
        pygame.display.update()
        
##### COVID-19 INFO #####
# runs all code for covid 19 info
def covid_info():
    running = True
    # create while loop to start game
    while running:
        # change background
        screen.fill((255, 255, 255))
        # display title for the game
        draw_text("COVID-19 INFO", 50, (0, 0, 0), screen, 280, 20)
        
        # display data point
        draw_text("United States COVID-19 Stats:", 45, (179, 0, 0), screen, 65, 120)
        draw_text("Cases: 16+ million", 40, (179, 0, 0), screen, 75, 160)
        draw_text("Deaths: 299,163", 40, (179, 0, 0), screen, 75, 200)
        
        # display tips
        draw_text("How to keep youself and other around you safe:", 45, (179, 0, 0), screen, 65, 260)
        draw_text("Make sure you wear a mask out in public.", 40, (179, 0, 0), screen, 75, 300)
        draw_text("Keep a distance of 6 feet.", 40, (179, 0, 0), screen, 75, 340)
        draw_text("Avoid public and crowded areas if you can", 40, (179, 0, 0), screen, 75, 380)
        
        # start event loop to play the game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # if user enters "esc" on keyborad you will be put back to main menu 
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                    
        pygame.display.update()

# create sick person function
def sick_person(x, y):
    screen.blit(sick_man_img, (x, y))

# create happy person function
def happy_person(x, y):
    screen.blit(happy_person_img, (x, y))

# call main menu function         
main_menu()