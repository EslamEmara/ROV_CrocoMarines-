import time
# import busio
# from Adafruit_BNO055 import BNO055
# from Directions import Direction
# from press_sensor import p_sensor

# pid constants
kp = 0.5
kd = 70
ki = 0.0001
sent = False
def server_recieve():
    global sent
    if sent == False:
        sent = True
        return True
    else:
        return False

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
    if (server_recieve()):
        global sent
        sent = False
        return imu_current_reading()
    else:
        return False


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



def calculate_pid_error(desired_value,actual_value,old_error,current_integral,old_time):
    new_time = time.time()
    deltaT = new_time - old_time
    print(" deltaT = ",deltaT)
    current_error = desired_value-actual_value
    print("the old error : ", old_error)
    print("the current error :",current_error)
    derivative = (current_error-old_error)/deltaT
    current_integral += (current_error*deltaT)
    pid_error = kp*current_error + ki*current_integral + kd*derivative
    print("the pid error : ",pid_error)
    return pid_error,current_integral,current_error,new_time


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



while True:
    # get the speed from gui


    roll_desired_value, pitch_desired_value, rotate_desired_value = get_desired_location()
    roll_actual_value = int(input('actual roll position = '))
    pitch_actual_value = int(input('actual pitch position = '))
    rotate_actual_value = int(input('actual rotate position = '))

    # Read the Euler angles for heading, roll, pitch (all in degrees).
    # rotate_actual_value, roll_actual_value, pitch_actual_value = imu.read_euler()
    # Print out.
    # print('Heading={0:0.2F} Roll={1:0.2F} Pitch={2:0.2F}'.format(heading, roll, pitch))
    roll_pid_error,roll_error_integral, roll_old_error, roll_old_time = calculate_pid_error(roll_desired_value, roll_actual_value,
                                                                roll_old_error,roll_error_integral,roll_old_time)
    if roll_pid_error > 0:
        print('roll right with speed ', roll_pid_error)
        # Direction.RollToRight(roll_pid_error)
    else:
        print('roll left with speed ', roll_pid_error)
        # Direction.RollToLeft(abs(roll_pid_error))
    # #################################################################################################################
    # rotate_actual_value, roll_actual_value, pitch_actual_value = imu.read_euler()
    pitch_pid_error,pitch_error_integral, pitch_old_error, pitch_old_time = calculate_pid_error(pitch_desired_value, pitch_actual_value,
                                                                pitch_old_error, pitch_error_integral,pitch_old_time)
    if pitch_pid_error > 0:
        print('pitch right with speed ', pitch_pid_error)
        # Direction.PitchUp(pitch_pid_error)
    else:
        print('pitch left with speed ', pitch_pid_error)
        # Direction.PitchDown(abs(pitch_pid_error))

    # #################################################################################################################
    # rotate_actual_value, roll_actual_value, pitch_actual_value = imu.read_euler()
    rotate_pid_error,rotate_error_integral, rotate_old_error, rotate_old_time = calculate_pid_error(rotate_desired_value, rotate_actual_value,
                                                                  rotate_old_error, rotate_error_integral,rotate_old_time)
    if rotate_pid_error > 0:
        print('rotate right with speed ', rotate_pid_error)
        # Direction.YawCw(rotate_pid_error)
    else:
        print('rotate left with speed ', rotate_pid_error)
        # Direction.YawCCw(abs(rotate_pid_error))

    # #################################################################################################################
    # depth_desired_value = Direction.depth
    # depth_actual_value = p_sensor.calculate_depth()
    # depth_pid_error,depth_error_integral, depth_old_error,depth_old_time = calculate_pid_error(depth_desired_value,
    #                       depth_actual_value,depth_old_error, depth_error_integral,depth_old_time)
    # if depth_pid_error > 0:
        # print('move down with speed ', depth_pid_error)
        # dir.ROV_Down(depth_pid_error)
    # else:
        # print('move up with speed ', depth_pid_error)
        # dir.ROV_Down(abs(depth_pid_error))
    time.sleep(0.5)
    print('###############################################')
