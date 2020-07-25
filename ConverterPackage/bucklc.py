import numpy as np


def inductor_rating(Vin, duty_cycle, fsw, Irp):
    Lcr = np.divide(np.multiply(Vin, np.multiply((1-duty_cycle), duty_cycle)), np.multiply(fsw, Irp))
    return Lcr


def capacitor_rating(Vo, duty_cycle, Lcr, Vrp, fsw):
    Co = np.divide(np.multiply(Vo, (1 - duty_cycle)),
                       np.multiply(np.multiply(8, Lcr), np.multiply(Vrp, pow(fsw, 2))))
    return Co
