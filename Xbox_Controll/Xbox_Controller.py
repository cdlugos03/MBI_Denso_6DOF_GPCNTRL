"""
                                                                                                                                               
     .*...............................................,,,,,,,,,,,....*(#(       
   .                                                                     %(     
                  .(##(##/*                                              .#.    
 .              #(        .##*####(*                                      #.    
 ,             #,           /#       .*(###(/,                           .#.    
 .            /#.            #                 ,/####(,                  .#.    
 .            (##           #(                    /##/. . .#(            .#.    
 .            /#,##,     ,(#,                   .#.           (          .#.    
 .             #,   ,*/###(**                  .#.           .#*.        .#.    
 ,             (#            , .*###/,         .#.           ,#,#        .#.    
 ,              #/                       ,(##(, .#(         /#.(*        .#.    
 .               #*                               .###(((##( ,#,         .#.    
 ,               ,#,                                                     .#.    
 (                ,#            ,.                                       .#.    
 #                 *#            ,.                                      .#.    
 (                  (#            /                                       #.    
 (                   #*            #.                                     #.    
 (                   .#    .*//*   .#                                     #.    
 #                    #*##.      .#((                                     #.    
 #                    ##            #.                                    #.    
 #                    #,            #(                                    #.    
 #                   *##           ,##.                                   #.    
 #                   (,*#/       .##.((                                   #.    
 #.                  #    *#####(,   .*                                   #.    
 #.                 *#                                                    #.    
 #.                  (#((((((##(((,..                                    .#.    
 #.                    /(##########(/                                     #.    
 ,/                  ,               .#*                                 *#     
  .%/              .                  /#                               /#/      
      .,****,*,,,,,,,,,,,,,****,,,*,,,**,*******,***,****************.          
                                                                            


MBI AUTOMATION R&D
Author: Cooper Dlugos

Libraries
______________________________________________
PyGame: Controlling robot using controller     
bcapclient: Communication with RC8 controller
______________________________________________
"""
#import necessary Libraries
import bcapclient
#communication with Robot

import numpy as np
#used for organizing cordinates
import sys
#system for controlling program paths
import time
#used for timing inputs
import pygame
#Used to connect with xbox controller
from pygame.locals import *

"""NOTES
•THINGS I CAN ADD: IDLE FUNCTION, ROBOT MOVES IN A PREDETERMINED PATH
UNTIL INPUT IS SENSED. AFTER 10 SECONDS OF NO INPUT THE ROBOT GOES BACK TO
IDLE STATE

•EOAT: How Can I use EOAT and would I have to write a program in the
controller to engage/disengage it?

•TOGGLE: How can I toggle between cartesian movements and joint movements


"""


def main():
    running = True

    bcapconnect() # establish connection between PC and RC8 Controller
    jstckinit() #establish connection between connection 
    motor_on() #turns robot motors on and releases brakes
    speedset(20,10,10,5)  # Set the speed of movement for robot
    pygminit()  # Initialize Pygame 

    while running:
        pos = getpos() # get current position of robot
        #Constant loop waiting for input from controller until A is pressed to
        #To stop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.JOYBUTTONDOWN:
                if event.button == 0:
                    pygame.quit()
                    motor_off()
                    sys.exit()

        checkz(HRobot, pos, event)  # Pass the event parameter to the checkpos function
        check_y(HRobot, pos, event)
        check_x(HRobot, pos, event)
        check_neg_y(HRobot,pos,event)

        #prints the current position of the robot
        curpos = getpos()
        print(f"\rCurrent position: {[round(x, 1) for x in curpos[0:3]]}", end='', flush=True)



        #This ensures your program can internally 
        # interact with the rest of the operating system.
        pygame.event.pump()

        #maps axis movements to their respective input
        x_axis = joystick.get_axis(0)
        y_axis = joystick.get_axis(1)
        z_axis = joystick.get_axis(3)
        Look = joystick.get_axis(2)

        #Declared Deadzone where stick drift will not be read
        if (
            abs(x_axis) > 0.3
            or abs(y_axis) > 0.1
            or abs(z_axis) > 0.1
            or abs(Look) > .1
        ):
            move_robot(HRobot, x_axis, y_axis, z_axis, Look)

#communicates with controller to pass along current positional
#Data in the form of a list
def getpos():
    Command = "CurPos"
    Param = ""
    tmp_cur_pos = m_bcapclient.robot_execute(HRobot, Command, Param)
    
    return tmp_cur_pos

#passed different movement axis' and moves them repsective to their input
def move_robot(HRobot, x_axis, y_axis, z_axis, Look):
    takearm()
    speedset(20,10,10,5)
    Param = ""
    cur_pos = getpos()
    cur_pos = np.array(cur_pos[0:7])

    org_list = cur_pos.tolist()

    # Adjust the robot's X, Y, Z, and joint 5 position based on the joystick's position
    temp_pos = org_list
    temp_pos[1] += x_axis * speed_factor
    temp_pos[0] += y_axis * speed_factor
    temp_pos[2] -= z_axis * speed_factor
    temp_pos[4] += Look * speed_factor
    temp_pos = [temp_pos, "P", "@P"]

    m_bcapclient.robot_move(HRobot, 1, temp_pos, Param)

#establishes connection between PC and the robot controller            
def bcapconnect():
    host = "192.168.0.1" #RC8 IP
    port = 5007 #RC8 Port
    timeout = 2000 #RC8 timeout determines how 
    #long the program will wait for a response 
    # from the RC8 device before timing out. (2000ms)

    global m_bcapclient 
    
    #Declare open connection with RC8
    m_bcapclient = bcapclient.BCAPClient(host, port, timeout)
    print("Open Connection")
    
    # command to start the b-CAP service on the controller. 
    m_bcapclient.service_start("")
    print("Send SERVICE_START packet")

    Name = ""
    Provider = "CaoProv.DENSO.VRC"
    Machine = "localhost"
    Option = ""

    #declare controller varible for GP control
    hCtrl = m_bcapclient.controller_connect(Name, Provider, Machine, Option)
    print("Connect RC8")

    #declare robot varible for GP control
    global HRobot
    HRobot = m_bcapclient.controller_getrobot(hCtrl, "Arm", "")
    print("AddRobot")

#motor on function: communicates with RC8 to turn motors on and
#disengage Brakes
def motor_on():
    Command = "Motor"
    Param = [1, 0]
    m_bcapclient.robot_execute(HRobot, Command, Param)
    print("Motor On")
    return

#motor off function: communicates with RC8 to turn motors off and
#Enable Brakes
def motor_off():
    Command = "Motor"
    Param = [0,0]
    m_bcapclient.robot_execute(HRobot,Command,Param)
    print("Motor Off")
    return

#initialize pygame: open and establishes use of pygame
#functionalitites 
def pygminit():
    pygame.init()
    

#initialize joystick: pygame functionality to establish a 
# communication between the Pc and the game controller
def jstckinit():
    pygame.joystick.init()
    global joystick 
    joystick = pygame.joystick.Joystick(0)
    joystick.init()

#Take Arm function: Prepares Robot arm to be controlled by program
def takearm():
    Command = "TakeArm"
    Param = [0, 0]
    m_bcapclient.robot_execute(HRobot, Command, Param)

#speed set function: used to declare acceleration, decceleration,
#speed and a speedfactor
def speedset(spd, acl, dcl,spdfctr):
    #set global variable for factoring speed
    global speed_factor

    speed_factor = spdfctr
    Command = "ExtSpeed"
    Speed = spd
    Accel = acl
    Decel = dcl
    Param = [Speed, Accel, Decel]

    m_bcapclient.robot_execute(HRobot, Command, Param)




def checkz(HRobot, cur_pos, event):
    if cur_pos[2] <= 70.0:
        motor_off()
        print("Motor Off")
        joystick.rumble(0, 1, 3000)
        print("You Are Exceeding Safety Range!")
        time.sleep(3)
        print("Press A To Reset From Safety Range!")

        # Wait until A button is pressed
        while True:
            pygame.event.pump()
            for event in pygame.event.get():
                if event.type == pygame.JOYBUTTONDOWN and event.button == 0:
                    ### TakeArm
                    takearm()
                    print("TakeArm")

                    ###Motor On
                    motor_on()
                    print("Motor On")

                    Param = ""                    
                    tmp_cur_pos =getpos()
                    # Adjust the robot's X, Y, Z, and joint 5 position based on the joystick's position
                    tmp_cur_pos[2] += 70
                    pos = [tmp_cur_pos, "P", "@P"]
                    m_bcapclient.robot_move(HRobot, 1, pos, Param)
                    joystick.init()
                    return  # Exit the function

def check_x(HRobot, cur_pos, event):
    if cur_pos[0] >= 340.0:
        motor_off()
        print("Motor Off")
        #joystick.rumble(0, 1, 3000) FIX THIS
        print("You Are Exceeding Safety Range!")
        time.sleep(3)
        print("Press A To Reset From Safety Range!")
        

        # Wait until A button is pressed
        while True:
            pygame.event.pump()
            for event in pygame.event.get():
                if event.type == pygame.JOYBUTTONDOWN and event.button == 0:
                    #TakeArm
                    takearm()
                    #Motor On
                    motor_on()
                    #Current Position
                    tmp_cur_pos = getpos()
                    #this is a manual Move so the robot will move 70 units
                    #Away in a perpendicular fashion from the obstruction
                    
                    Param = ""

                    tmp_cur_pos[0]  -= 70.0   # Set the position to the safety limit
                    pos = [tmp_cur_pos, "P", "@P"]
                    #move the determined distance away from the stopped pos
                    m_bcapclient.robot_move(HRobot, 1, pos, Param)
                    joystick.init() #reinitialize Joystick
                    return  # Exit the function
                
def check_y(HRobot, cur_pos, event):
    if cur_pos[1] >= 340:
        motor_off()
        print("Motor Off")
        #joystick.rumble(0, 1, 3000) FIX THIS
        print("You Are Exceeding Safety Range!")
        time.sleep(3)
        print("Press A To Reset From Safety Range!")
        

        # Wait until A button is pressed
        while True:
            pygame.event.pump()
            for event in pygame.event.get():
                if event.type == pygame.JOYBUTTONDOWN and event.button == 0:
                    #TakeArm
                    takearm()
                    #Motor On
                    motor_on()
                    #Current Position
                    tmp_cur_pos = getpos()
                    #this is a manual Move so the robot will move 70 units
                    #Away in a perpendicular fashion from the obstruction
                    
                    Param = ""

                    tmp_cur_pos[1]  -= 70.0   # Set the position to the safety limit
                    pos = [tmp_cur_pos, "P", "@P"]
                    #move the determined distance away from the stopped pos
                    m_bcapclient.robot_move(HRobot, 1, pos, Param)
                    joystick.init() #reinitialize Joystick
                    return  # Exit the function


def check_neg_y(HRobot, cur_pos, event):
    if cur_pos[1] <= -360.0:
        motor_off()
        print("Motor Off")
        #joystick.rumble(0, 1, 3000) FIX THIS
        print("You Are Exceeding Safety Range!")
        time.sleep(3)
        print("Press A To Reset From Safety Range!")
        

        # Wait until A button is pressed
        while True:
            pygame.event.pump()
            for event in pygame.event.get():
                if event.type == pygame.JOYBUTTONDOWN and event.button == 0:
                    #TakeArm
                    takearm()
                    #Motor On
                    motor_on()
                    #Current Position
                    tmp_cur_pos = getpos()
                    #this is a manual Move so the robot will move 70 units
                    #Away in a perpendicular fashion from the obstruction
                    
                    Param = ""

                    tmp_cur_pos[1]  += 70.0   # Set the position to the safety limit
                    pos = [tmp_cur_pos, "P", "@P"]
                    #move the determined distance away from the stopped pos
                    m_bcapclient.robot_move(HRobot, 1, pos, Param)
                    joystick.init() #reinitialize Joystick
                    return  # Exit the function
            





















if __name__ == "__main__":
    main()


