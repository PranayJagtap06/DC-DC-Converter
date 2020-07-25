<<<<<<< HEAD
import numpy as np


def inductor_rating(Vin, duty_cycle, fsw, Irp):
    Lcr = np.divide(np.multiply(Vin, duty_cycle), np.multiply(fsw, Irp))
    return Lcr


def capacitor_rating(output_current, duty_cycle, Vrp, fsw):
    Co = np.divide(np.multiply(output_current, duty_cycle),
                       np.multiply(Vrp, fsw))
=======
import numpy as np


def inductor_rating(Vin, duty_cycle, fsw, Irp):
    Lcr = np.divide(np.multiply(Vin, duty_cycle), np.multiply(fsw, Irp))
    return Lcr


def capacitor_rating(output_current, duty_cycle, Vrp, fsw):
    Co = np.divide(np.multiply(output_current, duty_cycle),
                       np.multiply(Vrp, fsw))
>>>>>>> 87820a8f68402c754ea9c9cdd6df2caab85774e4
    return Co