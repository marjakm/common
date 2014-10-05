import numpy as np
from sharp_sensor import SharpSensor

class Car(object):
    """
     w  -- D +-----------+ A
     i  |    |   pos     |
     d  |    |     *---> |
     t  |    |       uv  |
     h  -- C +-----------+ B

             |-----------|
                length
    """
    width  = 15
    length = 20

    sensors = dict(
        ir_front_left  = dict(s=SharpSensor, pos=np.array([9.5,  7.0]), uv=np.array([ 1.0,  0.0])),
        ir_front_right = dict(s=SharpSensor, pos=np.array([9.5, -7.0]), uv=np.array([ 1.0,  0.0])),
        ir_left        = dict(s=SharpSensor, pos=np.array([0.0,  7.0]), uv=np.array([ 0.0,  1.0])),
        ir_right       = dict(s=SharpSensor, pos=np.array([0.0, -7.0]), uv=np.array([ 0.0, -1.0])),
    )

    corner_locations = dict(
        A = np.array([ length/2,  width/2]),
        B = np.array([ length/2, -width/2]),
        C = np.array([-length/2, -width/2]),
        D = np.array([-length/2,  width/2]),
    )

    def __init__(self, x=0.0, y=0.0):
        self.uv   = np.array([1. , 0.])
        self.pos  = np.array([x , y])

    @property
    def perpendicular_unit_vec(self):
        return np.array([self.uv[1], self.uv[0]])

    @property
    def axes(self):
        return np.array([self.uv, self.perpendicular_unit_vec])

    def corner(self, name):
        return self.pos + np.dot(self.axes, self.corner_locations[name])

    @property
    def corners(self):
        return {k:self.corner(k) for k in self.corner_locations.keys()}

    @property
    def edges(self):
        dct = dict()
        for one,two in [('A','B'),('B','C'),('C','D'),('D','A')]:
            dct[one+two] = np.array([self.corner(one), self.corner(two)])
        return dct

    @property
    def A(self):
        return self.corner('A')

    @property
    def B(self):
        return self.corner('B')

    @property
    def C(self):
        return self.corner('C')

    @property
    def D(self):
        return self.corner('D')

    def get_sensor_data(self, *names):
        if len(names) == 0:
            names = self.sensors.keys()
        dct = dict()
        for nam in names:
            if nam not in self.sensors.keys():
                raise Exception("No sensor named {}".format(nam))
            dct[nam] = dict(
                s   = self.sensors[nam]['s'],
                pos = self.pos + np.dot(self.axes, self.sensors[nam]['pos']),
                uv  = np.dot(self.axes, self.sensors[nam]['uv'])
            )
        return dct

if __name__ == "__main__":
    c = Car()
    print(c.corners, c.edges)
    c.pos[0] = 10.
    c.pos[1] = 20.
    print(c.corners, c.edges)
    for k,v in c.get_sensor_data().items():
        print("{:<20} = {}".format(k,v))