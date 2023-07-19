# MBI_Denso_6DOF_GPCNTRL
This repository Dives into the control of a Denso 6 DOF Robot using Python-3

# Libraries

The required Libraries for this project are as follows:

• pygame: https://www.pygame.org/docs/
    
    cmd: pip install pygame
  
•numpy: https://numpy.org/install/
    
    cmd: pip install numpy

•time: (https://docs.python.org/3/library/time.html)
    
    cmd: pip install python-time

•system: (https://docs.python.org/3/library/sys.html)
    
    cmd: pip install os-sys

•bcapclient: https://github.com/DENSORobot/orin_bcap/tree/master/Python/bCAPClient
    
    Add to Program Library in IDE

*BCAPCLIENT*
This Library is used to connect and communicate with A Denso RC8 controller.

*PyGame* 
Used to translate inputs from the Xbox controller to readable, mappable movements the robot can take.

# Connection With RC8 and Controller
    host = "192.168.0.1"
    port = 5007
    timeout = 2000
•Host = Controller IP

•Port = RC port number

•timeout = allotted time for controller PC communication


# Basic Functions
        
    def move_robot()
This function will take the robot's current position and adjusts the robot's XY and Z positioning based on the Xbox controller's left joystick position

    def getpos()
the getpos function will communicate with the robot controller to determine the robot's current position and return a list of cartesian coordinates

    def check_y
    def check_x
    def check_z
    def check_neg_y
These functions are necessary if the robot is in an enclosed location. Use a teach pendant to determine the robot's maximum travel distance before stopping and resetting. The architecture of all of these functions is the same. While the robot is in movement it constantly compares the coordinates of its current position to the coordinates of the pre-determined maximum distance it can travel before stopping. Once stopped you are prompted with an error for 3 seconds then you can recover the robot by pressing A on the controller. This will send the robot back perpendicularly a predetermined distance away from the stopped location. 

    def bcapconnect()
Automatically sends Service start packet for connection, creates a robot and controller variable. This can all be done by calling this function at the beginning of the program. 

    def motor on()
    def motor off()
sends a request to turn the motors on or off depending on what function you use. This is needed to immediately stop the robot in case of a fault or to prep the robot for incoming input or to start a task. 

    def jstckinit()
This function allows the Xbox controller to be used in the program by first initializing it and appending it to a joystick list.











