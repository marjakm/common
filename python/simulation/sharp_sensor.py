import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import PiecewisePolynomial

class SharpSensor(object):
    # values imported from
    # http://www.sharpsme.com/download/gp2y0a21yk-epdf
    # by converting pdf to svg with inkscape
    distance_to_voltage_characteristic_150cm = [
        # (0.00, 0.00),
        # (10.49, 231.65),
        (15.53, 275.00),
        (20.76, 251.80),
        (29.99, 199.09),
        (40.00, 152.95),
        (50.00, 122.86),
        (60.00, 103.26),
        (70.00, 88.40),
        (79.99, 80.08),
        (90.54, 69.57),
        (100.00, 62.95),
        (110.50, 56.88),
        (120.00, 51.91),
        (129.99, 48.15),
        (139.99, 43.62),
        (150.00, 40.58),
    ]

    distance_to_voltage_characteristic_80cm = [
        (   0.00,    0.00),
        (  87.33,  467.44),
        ( 121.28,  690.47),
        ( 155.23,  940.98),
        ( 194.06, 1180.82),
        ( 232.86, 1451.20),
        ( 266.80, 1706.31),
        ( 305.63, 1956.82),
        ( 344.43, 2253.17),
        ( 407.51, 2612.16),
        ( 441.49, 2841.28),
        ( 460.86, 3033.77),
        ( 470.59, 3087.23),
        ( 475.44, 3108.61),
        ( 577.32, 3166.67),
        ( 999.38, 2323.44),
        (1513.62, 1655.90),
        (2003.64, 1313.72),
        (2508.18, 1084.59),
        (3012.75,  928.77),
        (4012.15,  736.28),
        (5011.53,  604.92),
        (6015.76,  510.22),
        (7020.02,  441.47),
        (8000.00,  412.45),
    ]
    x,y = map(np.array, zip(*distance_to_voltage_characteristic_150cm))
    distance_to_voltage_polyline = PiecewisePolynomial(
        x, y[:,np.newaxis]
    )
    x1,y1 = map(np.array, zip(*distance_to_voltage_characteristic_150cm[::-1]))
    voltage_to_distance_polyline = PiecewisePolynomial(
        y1, x1[:,np.newaxis]
    )

    @classmethod
    def plot(cls):
        fig, ax = plt.subplots()
        ax.plot(cls.y, cls.x)
        ax.set_ylabel("Output voltage (mV)")
        ax.set_xlabel("Distance to reflective object L(mm)")
        plt.show()

    @classmethod
    def distance_to_voltage(cls, *distances):
        return cls.distance_to_voltage_polyline(distances)

    @classmethod
    def distance_to_sample(cls):
        # TODO: Implement distance_to_sample
        raise NotImplemented

    @classmethod
    def create_vol_to_distance_lut(cls):
        sample_count = 1024
        voltage_step = 330./sample_count
        for i, vol in enumerate([voltage_step*x for x in range(1024)]):
            if i % 16 == 0:
                print ""
            if  vol > max(cls.y):
                vol = max(cls.y)
            elif vol < min(cls.y):
                vol = min(cls.y)
            print "{:>3.0f},".format(cls.voltage_to_distance_polyline((vol,))[0]),


if __name__ == "__main__":
    # print(SharpSensor.distance_to_voltage(130, 400, 460.86))

    SharpSensor.create_vol_to_distance_lut()
    # SharpSensor.plot()
    # print(SharpSensor.x)
    # print(SharpSensor.y)
    # for x,y in SharpSensor.distance_to_voltage_characteristic_150cm:
    #     print("({:>4.2f}, {:>4.2f}),".format(x*150/133.23, y*275/121.36))
