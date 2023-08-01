# MBI_Denso_6DOF_GPCNTRL
This repository Dives into the control of a Denso 6 DOF Robot using Python-3, More information is shown in the b-Cap_Guide_RC_en.pdf file below

# Setup
You Will need a PC, Ethernet Cable, RC8 Robot controller, and a Denso Robot. Any Python IDE will work but I recommend
Microsoft's Visual Studio Code.

The Basic Connection Code is as Follows

    #Change IP, Host, and Port as needed
    host = "192.168.0.1"
    port = 5007
    timeout = 2000
    
    #Connection processing of tcp communication
    m_bcapclient = bcapclient.BCAPClient(host,port,timeout)
    print("Open Connection")
    
    #start b_cap Service
    m_bcapclient.service_start("")
    print("Send SERVICE_START packet")
    
    #set Parameter
    Name = ""
    Provider="CaoProv.DENSO.VRC"
    Machine = ("localhost")
    Option = ("")
    
    #Connect to RC8 (RC8(VRC)provider)
    hCtrl = m_bcapclient.controller_connect(Name,Provider,Machine,Option)
    print("Connect RC8")
    #get Robot Object Handl
    HRobot = m_bcapclient.controller_getrobot(hCtrl,"Arm","")
    print("AddRobot")
    
    #TakeArm
    Command = "TakeArm"
    Param = [0,0]
    m_bcapclient.robot_execute(HRobot,Command,Param)
    print("TakeArm")
    
    #Motor On
    Command = "Motor"
    Param = [1,0]
    m_bcapclient.robot_execute(HRobot,Command,Param)
    print("Motor On")

After this connection program is written in your code, you will be able to use different types of bcap executables for controlling the robot and controller

If there are any questions email coopersd036@gmail.com

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
    
    Add folder to Program Library in IDE

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











