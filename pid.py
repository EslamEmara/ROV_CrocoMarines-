import time
# import busio
# from Adafruit_BNO055 import BNO055
# from Directions import Direction
#from press_sensor import p_sensor
#from imu_client import *
import imu_client 
from imu_client import IMUClass
import threading

# pid constants
kp = 0.5
kd = 70
ki = 0.0001

# time variables
roll_old_time = time.time()
pitch_old_time = time.time()
rotate_old_time = time.time()
depth_old_time = time.time()

# roll variables
roll_old_error=0
roll_error_integral = 0
roll_desired_value = 0
roll_pid_error = 0

# pitch variables
pitch_old_error=0
pitch_error_integral = 0
pitch_desired_value = 0
pitch_pid_error = 0

# rotate variables
rotate_old_error=0
rotate_error_integral = 0
rotate_desired_value = 0
rotate_pid_error = 0

# depth variables
depth_desired_value = 0         # change its value when the rov goes up or down
depth_old_error = 0
depth_error_integral = 0
depth_pid_error = 0

ROV_is_moving = False
ROV_pitching = False
ROV_rolling = False
ROV_rotating = False
ROV_height_change = False

ROV_speed = 0

pid_gui = IMUClass()
#pressure_sensor = p_sensor()

def recieve_msgs():
    global ROV_is_moving,ROV_pitching,ROV_rolling,ROV_rotating,ROV_height_change,ROV_speed
    msg = imu_client.pid_msg
    if msg:
        print ('message here =' ,msg)
    ## check for moves done by the pilot and setting flags##
    if ("yawcw" in msg or "yawccw" in msg):
        ROV_rolling = True 
        #ROV_pitching = False
    elif ("pitchup" in msg or "pitchdown" in msg):
        ROV_pitching = True
        #ROV_rolling = False
    elif ("rotatetoleft" in msg or "rotatetoright" in msg):
        ROV_rotating = True    
    elif ("up" in msg or "down" in msg):
        ROV_height_change = True 
    
    if ("move" in msg):
        if("stop" in msg):              ## no button pressed
            ROV_is_moving = False
            ROV_speed = 0
        elif (("left" in msg or "right" in msg or "backward" in msg or "forward") in msg): ###other moves
            ROV_is_moving = True
            ROV_pitching = False
            ROV_rolling = False
            ROV_rotating = False
            ROV_height_change = False
    if ('speed' in msg):                        ## get the int speed from the message speed (n)
        ROV_speed = int(''.join(x for x in msg if x.isdigit()))

def get_data_test():
    roll = int(input('current imu roll reading='))
    pitch = int(input('current imu pitch reading='))
    rotate = int(input('current imu rotate reading='))
    return roll,pitch,rotate

def imu_current_reading():
    # roll,pitch,rotate = imu.read_euler()
    roll,pitch,rotate = get_data_test()
    return roll,pitch,rotate

def get_desired_location():
    global ROV_is_moving,ROV_pitching,ROV_rolling,ROV_rotating,ROV_height_change
    global roll_desired_value,pitch_desired_value,rotate_desired_value,depth_desired_value
    if ROV_rolling == True:
        if ROV_is_moving == False:
            ROV_rolling == False 
            roll_desired_value,_,__=imu_current_reading()
    if ROV_pitching == True:
        if ROV_is_moving == False:
            ROV_pitching == False 
            _,pitch_desired_value,__=imu_current_reading()
    if ROV_rotating == True:
        if ROV_is_moving == False:
            ROV_rotating == False 
            _,__,rotate_desired_value=imu_current_reading()
    if ROV_height_change == True:
        if ROV_is_moving == False:
            ROV_height_change == False 
            #depth_desired_value=pressure_sensor.calculate_depth()
            depth_desired_value=int(input('depth desired value'))
    return roll_desired_value,pitch_desired_value,rotate_desired_value,depth_desired_value

def calculate_pid_error(desired_value,actual_value,old_error,current_integral,old_time):
    new_time = time.time()
    deltaT = new_time - old_time
    #print(" deltaT = ",deltaT)
    current_error = desired_value-actual_value
    #print("the old error : ", old_error)
    #print("the current error :",current_error)
    derivative = (current_error-old_error)/deltaT
    current_integral += (current_error*deltaT)
    pid_error = kp*current_error + ki*current_integral + kd*derivative
    print("the pid error : ",pid_error)
    return pid_error,current_integral,current_error,new_time

def clamp(n, minn, maxn):           ##function to limit the speed of the motors to max and min
    if n < minn:
        return minn
    elif n > maxn:
        return maxn
    else:
        return n


# Raspberry Pi configuration with serial UART and RST connected to GPIO 18:
# imu = BNO055.BNO055(serial_port='/dev/serial0', rst=18)

# Enable verbose debug logging if -v is passed as a parameter.
# if len(sys.argv) == 2 and sys.argv[1].lower() == '-v':
    # logging.basicConfig(level=logging.DEBUG)

# Initialize the BNO055 and stop if something went wrong.
# if not imu.begin():
    # raise RuntimeError('Failed to initialize BNO055! Is the sensor connected?')

# Print system status and self test result.
# status, self_test, error = bno.get_system_status()
# print('System status: {0}'.format(status))
# print('Self test result (0x0F is normal): 0x{0:02X}'.format(self_test))
# Print out an error if system status is in error mode.
# if status == 0x01:
    # print('System error: {0}'.format(error))
    # print('See datasheet section 4.3.59 for the meaning.')
temperature = 0
depth_actual_value = 0
while True:
    # get the speed from gui
    recieve_msgs()
    roll_desired_value,pitch_desired_value,rotate_desired_value,depth_desired_value= get_desired_location()
    roll_actual_value = int(input('actual roll position = '))
    pitch_actual_value = int(input('actual pitch position = '))
    rotate_actual_value = int(input('actual rotate position = '))
    #depth_actual_value,temperature = p_sensor.calculate_depth()
    pid_gui.send_msg("angel"+str(pitch_actual_value)+str(roll_actual_value)\
        +str(rotate_actual_value)+str(temperature) +str(depth_actual_value))

    # Read the Euler angles for heading, roll, pitch (all in degrees).
    # rotate_actual_value, roll_actual_value, pitch_actual_value = imu.read_euler()
    # Print out.
    # print('Heading={0:0.2F} Roll={1:0.2F} Pitch={2:0.2F}'.format(heading, roll, pitch))
    roll_pid_error,roll_error_integral, roll_old_error, roll_old_time = calculate_pid_error(roll_desired_value, roll_actual_value,
                                                                roll_old_error,roll_error_integral,roll_old_time)

        
    if roll_pid_error > 0:
        if ROV_is_moving == True:
            print('roll right with speed ', clamp(int(roll_pid_error)+ROV_speed,0,150))
            #Direction.RollToRight(clamp(roll_pid_error+ROV_speed,0,150))
        else:
            print('roll right with speed ', clamp(int(roll_pid_error),0,150))
            #Direction.RollToRight(clamp(roll_pid_error,0,150))
    
    elif roll_pid_error <0:
        if ROV_is_moving == True :
            print('roll left with speed ', clamp(abs(int(roll_pid_error))+ROV_speed,0,150))
            #Direction.RollToLeft(clamp(abs(int(roll_pid_error))+ROV_speed,0,150))
        else :
            print('roll left with speed ', clamp(abs(int(roll_pid_error)),0,150))
            #Direction.RollToLeft(clamp(abs(int(roll_pid_error)),0,150))
    else:
        print ('roll movement is constant')
        #if ROV_is_moving == False:
        #    Direction.stop()
    # #################################################################################################################
    # rotate_actual_value, roll_actual_value, pitch_actual_value = imu.read_euler()
    pitch_pid_error,pitch_error_integral, pitch_old_error, pitch_old_time = calculate_pid_error(pitch_desired_value, pitch_actual_value,
                                                                pitch_old_error, pitch_error_integral,pitch_old_time)
    if pitch_pid_error > 0:
        if ROV_is_moving == True:
            print('pitch up with speed ', clamp(ROV_speed + pitch_pid_error,0,150))
            #Direction.PitchUp(clamp(ROV_speed + pitch_pid_error,0,150))
        else:
            print('pitch up with speed ',clamp(pitch_pid_error,0,150))
            #Direction.PitchUp(clamp(pitch_pid_error,0,150))


    else:
        if ROV_is_moving == True:
            print('pitch down with speed ', clamp(ROV_speed + abs(pitch_pid_error),0,150))
            #Direction.PitchDown(clamp(ROV_speed + abs(pitch_pid_error),0,150))
        else:
            print('pitch right with speed ',clamp(abs(pitch_pid_error),0,150))
            #Direction.PitchDown(clamp(abs(pitch_pid_error),0,150))       

    # #################################################################################################################
    # rotate_actual_value, roll_actual_value, pitch_actual_value = imu.read_euler()
    rotate_pid_error,rotate_error_integral, rotate_old_error, rotate_old_time = calculate_pid_error(rotate_desired_value, rotate_actual_value,
                                                                  rotate_old_error, rotate_error_integral,rotate_old_time)
    if rotate_pid_error > 0:
        if ROV_is_moving == True:
            print('rotate right with speed ', clamp(ROV_speed + rotate_pid_error,0,150))
            #Direction.YawCw(clamp(ROV_speed + rotate_pid_error,0,150))
        else:
            print('rotate right with speed ',clamp(rotate_pid_error,0,150))
            #Direction.YawCw(clamp(rotate_pid_error,0,150))       
    else:
        if ROV_is_moving == True:
            print('rotate left with speed ', clamp(ROV_speed + abs(rotate_pid_error),0,150))
            #Direction.YawCcw(clamp(ROV_speed + abs(rotate_pid_error),0,150))
        else:
            print('rotate left with speed ',clamp(abs(rotate_pid_error),0,150))
            #Direction.YawCcw(clamp(abs(rotate_pid_error),0,150))  
    # #################################################################################################################
    # depth_desired_value = Direction.depth
    # depth_pid_error,depth_error_integral, depth_old_error,depth_old_time = calculate_pid_error(depth_desired_value,
    #                       depth_actual_value,depth_old_error, depth_error_integral,depth_old_time)
    # if depth_pid_error > 0:
        #if ROV_height_change == True:
        #    print('move down with speed ', clamp(ROV_speed + depth_pid_error,0,150))
        #    Direction.Down(clamp(ROV_speed + depth_pid_error,0,150))
        #else:
        #    print('move down with speed ',clamp(depth_pid_error,0,150))
        #    Direction.Down(clamp(depth_pid_error,0,150))  
    # else:
        #if ROV_height_change == True:
        #    print('move up with speed ', clamp(ROV_speed + abs(depth_pid_error),0,150))
        #    Direction.Up(ROV_speed +clamp(abs(depth_pid_error),0,150))
        #else:
        #    print('move up with speed ',clamp(abs (depth_pid_error),0,150))
        #    Direction.Up(clamp(abs(depth_pid_error),0,150)) 

    time.sleep(0.5)
    print('###############################################')