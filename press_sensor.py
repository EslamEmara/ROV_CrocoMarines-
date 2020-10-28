import ms5803py
s = ms5803py.MS5803()

# p(h) = dgh
# density of water in kg/m^3
d = 1000
# the gravity in m/s^2
g = 9.8


class p_sensor:
    def calculate_depth(self):
        raw_temperature = s.read_raw_temperature(osr=4096)
        raw_pressure = s.read_raw_pressure(osr=256)
        press, temp = s.convert_raw_readings(raw_pressure, raw_temperature)
        # change pressure from mbar to N/m^2
        press *= 100
        depth = press/(d*g)
        # from meter to cm
        depth *= 100
        print ("the depth of rov = ",depth," cm")
        return depth , temp