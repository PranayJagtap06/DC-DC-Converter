import numpy as np


def inductor_rating(Vin, duty_cycle, fsw, Irp):
    Lcr = np.divide(np.multiply(Vin, duty_cycle), np.multiply(fsw, Irp))
    return Lcr


def capacitor_rating(output_current, duty_cycle, Vrp, fsw):
    Co = np.divide(np.multiply(output_current, duty_cycle),
                       np.multiply(Vrp, fsw))
    return Co