"""
                                                                                                                                               
                                                                                                                                                                                                    
                                                                                                                                                                                                        
                                                                                                                                                                                                        
                                                                                                                                                                                                        
           . ..     ....,,,,,********/((((((((((((((((((((((((((((*.                                                                                                                                    
    ,.                                                              *#(                                                                                 .....,,,,,..                                    
                                                                      *#          /%%%%%%%%%%%&                      (%%%%%%%%%%%(        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%&            %%%%%%%%%%%%%%  
                .##.   /###%/.                                         %.         /%%%%%%%%%%%%&                    &%%%%%%%%%%%%/        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%&%%%%%          %%%%%%%%%%&%%%  
 .            .#          *#.  ./(#(((,                                #.             #%%%%%%%%%%*                .&%%&%%%%%%%                &%%%%%                   .&%%%%%%             %%%%%&      
 .            #(            #           .,(#(#(/.                      #.             %%%%%%%%%%%%/              ,%%%%%%%%%%%%                &%%%%%                    ,%%%%%&             %%%%%%      
 .            ##           ,#                     #(#(##/              #.             %%%%%% &%%%%%&            &%%%%%& %%%%%%                &%%%%%                   *%%%%%%.             %%%%%%      
 .            ###,        ##                   /#,        ,#           #.             %%%%%%  #%%%%%%          %%%%%%&  %%%%%%                &%%%%%%%%%%%%%%%%%%%%%%%%%%%%%#               %%%%%%      
 .            ##  (###(##,.                   #(           ,,          #.             %%%%%%    %%%%%%.       %%%%%%.   %%%%%%                &%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%#              %%%%%%      
 ,            *#           .(###*.            (/           ,# /        #.             %%%%%%     &%%%%%%    #%%%%%&     %%%%%%                &%%%%%................*(&%%%%%%%&             %%%%%%      
 ,             ((           .        ,###/    ((          *# #         #.             %%%%%%      &%%%%%%  #%%%%%&      %%%%%%                &%%%%%                     &%%%%%&            %%%%%%      
 .              #(           .                  ###,. .,#####(         #.             %%%%%%       ,%%%%%%%%%%%%/       %%%%%%                &%%%%%                     (%%%%%&            %%%%%%      
 ,               #.           /                                        #.             %%%%%%         &%%%%%%%%&,        %%%%%%                &%%%%%                    %%%%%%%.            %%%%%%      
 /                #,           (                                       #.         *%%%%%%%%%%&&&%     %%%%%%%%     #&&%&%%%%%%&%%/        %%&%%%%%%%&&&&&&&&&&&&&&&&&%%%%%%%%%          &%%%%%%%&%%%%%  
 #                *#            %                                      #.         /%%%%%%%%%%%%%%      (%%%&%      #%%%%%%%%%%%%%(        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%&%            %%%%%%%%%%%%%%  
 (                 .%            #                                     #.         ,//////////////       *((/       */////////////,        ///(((((##################(*.                 */////////////. 
 (                  #%            #                                    #.                                                                                                                               
 (                   #    ,(##,.  #*                                   #.                                                                                                                               
 #                   #/#/       ,#(#                                   #.                                                                                                                               
 #                   /#           ,#                                   #.                                                                                                                               
 #                   (,           ,#                                   #.                                                                                                                               
 #                  ,##.          ###                                  #.                                                                                                                               
 #                  ## (#/     ,##  #,                                 #.                                                                                                                               
 #                  #,     ...       /                                 #.                                                                                                                               
 #                  (               .                                  #.                                                                                                                               
 #                                                                     #.                                                                                                                               
 (                  .(........    .(#.                                 #                                                                                                                                
  #.                                 #                                ##                                                                                                    .                           
    (#(*,,,*****************/////////#/((((((((((((##################.                       


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
    mainrunning = True
    while mainrunning:
        running = True
        bcapconnect() # establish connection between PC and RC8 Controller
        pygminit()  # Initialize Pygame
        jstckinit() #establish connection between connection 
        motor_on()
        speedset(10,10,10,5)  # Set the speed of movement for robot
        IOHandl = 0
        IOHandl = m_bcapclient.controller_getvariable(hCtrl, "IO128", "")
        HTask = 0
        HTask = m_bcapclient.controller_gettask(hCtrl,"Pro1","")
        mode = 1
        m_bcapclient.variable_putvalue(IOHandl, False)
        m_bcapclient.task_start(HTask,mode,"")

        

        flg = True
        while flg:
            TaskStatus = m_bcapclient.task_execute(HTask,"GetStatus")
            for event in pygame.event.get():
                if event.type == pygame.JOYBUTTONDOWN and event.button == 0:
                        print("LEFT D-PAD Pressed")
                        m_bcapclient.variable_putvalue(IOHandl, True)
                        print("Write Variable :newval = %s" % True)
                    
                        #m_bcapclient.task_stop(HTask,1,"")
                        print("task stop")

                        print(TaskStatus)
                        if(TaskStatus == 2):
                            
                            m_bcapclient.task_release(HTask)
                            print("Release Pro1")
                            flg = False
                            
            
        m_bcapclient.variable_putvalue(IOHandl, False)            
                    
        running = True
        
        global last_input_time 
        last_input_time = time.time()
        while running:
            
            pos = getpos() # get current position of robot
            #Constant loop waiting for input from controller until A is pressed to
            #To stop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.JOYBUTTONDOWN:
                    if event.button == (0):
                        running = False
                        
                        
            
            if checkz(HRobot, pos, event) or check_y(HRobot, pos, event) or check_x(HRobot, pos, event) or check_neg_y(HRobot, pos, event) == True:
                last_input_time = time.time()
                joysticks[0].rumble(1,1,1000)



            #prints the current position of the robot
            curpos = getpos()
            print(f"\rCurrent position: {[round(x, 1) for x in curpos[0:3]]}    Time Until Reset: {round((30 - (time.time() - last_input_time)), 0)}", end='', flush=True)




            #This ensures your program can internally 
            # interact with the rest of the operating system.
            pygame.event.pump()

            #maps axis movements to their respective input
            x_axis = joysticks[0].get_axis(0)
            y_axis = joysticks[0].get_axis(1)
            z_axis = joysticks[0].get_axis(3)

            #Declared Deadzone where stick drift will not be read
            
            if (
                abs(x_axis) > 0.3
                or abs(y_axis) > 0.1
                or abs(z_axis) > 0.1
                
                
            ):
            
                move_robot(HRobot, x_axis, y_axis, z_axis)
                last_input_time = time.time()
            else:

                if time.time() - last_input_time >= 30:
                    running = False

#communicates with controller to pass along current positional
#Data in the form of a list
def getpos():
    Command = "CurPos"
    Param = ""
    tmp_cur_pos = m_bcapclient.robot_execute(HRobot, Command, Param)
    
    return tmp_cur_pos

#passed different movement axis' and moves them repsective to their input
def move_robot(HRobot, x_axis, y_axis, z_axis):
    takearm()
    speedset(50,10,10,10)
    Param = ""
    cur_pos = getpos()
    cur_pos = np.array(cur_pos[0:7])

    org_list = cur_pos.tolist()

    # Adjust the robot's X, Y, Z, and joint 5 position based on the joystick's position
    temp_pos = org_list
    temp_pos[1] += x_axis * speed_factor
    temp_pos[0] += y_axis * speed_factor
    temp_pos[2] -= z_axis * speed_factor
    temp_pos = [temp_pos, "P", "@P"]
    
    
    m_bcapclient.robot_move(HRobot, 1, temp_pos, Param)

#establishes connection between PC and the robot controller            
def bcapconnect():
    host = "192.168.0.1" #RC8 IP
    port = 5007 #RC8 Port
    timeout = 1000 #RC8 timeout determines how 
    #long the program will wait for a response 
    # from the RC8 device before timing out. (2000ms)

    global m_bcapclient 
    
    
    # Declare open connection with RC8
    m_bcapclient = bcapclient.BCAPClient(host, port, timeout)
    print("Open Connection")

    # Command to start the b-CAP service on the controller.
    m_bcapclient.service_start("")
    print("Send SERVICE_START packet")

    Name = ""
    Provider = "CaoProv.DENSO.VRC"
    Machine = "localhost"
    Option = ""

    # Declare controller variable for GP control
    global hCtrl
    hCtrl = m_bcapclient.controller_connect(Name, Provider, Machine, Option)
    print("Connect RC8")
    


    # Declare robot variable for GP control
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
    global joysticks
    pygame.joystick.init()
    joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]
    print(joysticks)
    


#Take Arm function: Prepares Robot arm to be controlled by program
def takearm():
    Command = "TakeArm"
    Param = [0, 0]
    
    
    m_bcapclient.robot_execute(HRobot, Command, Param)

def takearmstate():
    Command = "TakeArmState"
    Param = ""
    
    m_bcapclient.robot_execute(HRobot, Command, Param)

def givearm():
    #One Way make a way to send an io from the left dpad to the controller
    #make loop for the idle then throw an rexception when the i/o is triggered for the left dpad then exit while loop and GiveArm
    Command = "GiveArm"
    Param = None
    print("GiveArm")
    
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
        joysticks[0].rumble(0.0,1.0,1000)
        motor_off()
        print("Motor Off")
        print("You Are Exceeding Safety Range!")
        pygame.time.delay(3000)
        print("Press A To Reset From Safety Range!")

        # Wait until A button is pressed
        while True:
            pygame.event.pump()
            for event in pygame.event.get():
                if event.type == pygame.JOYBUTTONDOWN and event.button == 0:
                    joysticks[0].quit
                    ### TakeArm
                    speedset(10,10,10,2)

                    ###Motor On
                    motor_on()
                    print("Motor On")

                    Param = ""                    
                    tmp_cur_pos =getpos()
                    # Adjust the robot's X, Y, Z, and joint 5 position based on the joystick's position
                    tmp_cur_pos[2] += 70
                    pos = [tmp_cur_pos, "P", "@P"]
                    m_bcapclient.robot_move(HRobot, 1, pos, Param)
                    jstckinit()
                    
                    
                    
                    return True# Exit the function
    else: return False

def check_x(HRobot, cur_pos, event):
    if cur_pos[0] >= 400.0:
        motor_off()
        print("Motor Off")
        print("You Are Exceeding Safety Range!")
        pygame.time.delay(3000)
        print("Press A To Reset From Safety Range!")

        # Wait until A button is pressed
        while True:
            pygame.event.pump()
            for event in pygame.event.get():
                if event.type == pygame.JOYBUTTONDOWN and event.button == 0:
                    joysticks[0].quit
                    ### TakeArm
                    speedset(10,10,10,2)

                    ###Motor On
                    motor_on()
                    print("Motor On")

                    Param = ""                    
                    tmp_cur_pos =getpos()
                    # Adjust the robot's X, Y, Z, and joint 5 position based on the joystick's position
                    tmp_cur_pos[0] -= 70
                    pos = [tmp_cur_pos, "P", "@P"]
                    m_bcapclient.robot_move(HRobot, 1, pos, Param)
                    jstckinit()
                    
                    
                    
                    return True# Exit the function
    else: return False
                
def check_y(HRobot, cur_pos, event):
    if cur_pos[1] >= 360.0:
        motor_off()
        print("Motor Off")
        print("You Are Exceeding Safety Range!")
        pygame.time.delay(3000)
        print("Press A To Reset From Safety Range!")

        # Wait until A button is pressed
        while True:
            pygame.event.pump()
            for event in pygame.event.get():
                if event.type == pygame.JOYBUTTONDOWN and event.button == 0:
                    joysticks[0].quit
                    ### TakeArm
                    speedset(10,10,10,2)

                    ###Motor On
                    motor_on()
                    print("Motor On")

                    Param = ""                    
                    tmp_cur_pos =getpos()
                    # Adjust the robot's X, Y, Z, and joint 5 position based on the joystick's position
                    tmp_cur_pos[1] -= 70
                    pos = [tmp_cur_pos, "P", "@P"]
                    m_bcapclient.robot_move(HRobot, 1, pos, Param)
                    jstckinit()
                    
                    
                    
                    return True# Exit the function
    else: return False

def check_neg_y(HRobot, cur_pos, event):
    if cur_pos[1] <= -350.0:
        motor_off()
        print("Motor Off")
        print("You Are Exceeding Safety Range!")
        pygame.time.delay(3000)
        print("Press A To Reset From Safety Range!")

        # Wait until A button is pressed
        while True:
            pygame.event.pump()
            for event in pygame.event.get():
                if event.type == pygame.JOYBUTTONDOWN and event.button == 0:
                    joysticks[0].quit
                    ### TakeArm
                    speedset(10,10,10,2)

                    ###Motor On
                    motor_on()
                    print("Motor On")

                    Param = ""                    
                    tmp_cur_pos =getpos()
                    # Adjust the robot's X, Y, Z, and joint 5 position based on the joystick's position
                    tmp_cur_pos[1] += 70
                    pos = [tmp_cur_pos, "P", "@P"]
                    m_bcapclient.robot_move(HRobot, 1, pos, Param)
                    jstckinit()
                    
                    
                    
                    return True# Exit the function
    else: return False
            





















if __name__ == "__main__":
    main()


