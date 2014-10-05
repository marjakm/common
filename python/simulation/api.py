from car import Car
from track import Track


class SensorMeasurements(object):
    def __init__(self):
        self.ir_front_left  = None
        self.ir_front_right = None
        self.ir_left        = None
        self.ir_right       = None

class ControllerValues(object):
    def __init__(self):
        self.steering = None #from -1 as full left to 1 as full right
        self.throttle = None #from 0 as stop to 1 as full power

class Simulator(object):

    def __init__(self):
        self.step_period = None
        self.car   = Car(410., 750.)
        self.track = Track()

    def test_car_position(self):
        return self.track.contains(self.car.corners, self.car.edges)

    def get_sensor_values(self):
        result = dict()
        sensor_data = self.car.get_sensor_data()
        for name,data in sensor_data.items():
            dst = self.compute_distance(data)
            print(name, dst)
            result[name] = data['s'].distance_to_voltage(dst)
        return result

    def compute_distance(self, data):
        if data['uv'][0] != 0:
            a = data['uv'][1]/data['uv'][0]
            c = data['pos'][1]-a*data['pos'][0]

        distance = None
        for a2,c2,xmin,xmax in self.track.lines:
            if data['uv'][0] == 0:
                x = data['pos'][0]
            else:
                if a == a2:
                    # print("parallel")
                    continue
                x = (c2-c)/(a-a2)
            if round(x,0) > round(xmax,0) or round(x,0) < round(xmin,0):
                # print("out of bounds {:>10.2f} {:>10.2f} {:>10.2f}".format(xmin, x, xmax))
                continue

            if data['uv'][0] == 0:
                dst = (a2*x+c2-data['pos'][1])/data['uv'][1]
            else:
                dst = (x-data['pos'][0])/data['uv'][0]
            if dst < 0:
                # print("Found point {} is not in the direction of the unit vector {}".format(x, dst))
                continue
            else:
                # print("Found suitable point {} with distance {}".format(x, dst))
                if distance is None or dst < distance:
                    distance = dst
        return distance

if __name__ == "__main__":
    s = Simulator()
    print(s.test_car_position())
    print(s.get_sensor_values())