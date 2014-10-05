import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import PiecewisePolynomial

class SharpSensor(object):
    # values imported from
    # http://www.sharpsme.com/download/gp2y0a21yk-epdf
    # by converting pdf to svg with inkscape
    distance_to_voltage_characteristic = [
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
    x,y = map(np.array, zip(*distance_to_voltage_characteristic))
    distance_to_voltage_polyline = PiecewisePolynomial(
        x, y[:,np.newaxis]
    )

    @classmethod
    def plot(cls):
        fig, ax = plt.subplots()
        ax.plot(cls.x, cls.y)
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

if __name__ == "__main__":
    print(SharpSensor.distance_to_voltage(130, 400, 460.86))
    # ss.plot()
