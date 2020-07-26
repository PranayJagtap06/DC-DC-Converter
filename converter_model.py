import sys
from ConverterPackage import bucklc, boostlc, dutycycle
from colorama import init, Fore, Style
import numpy as np

init(convert=True)


class Converter:

    def __init__(self):
        print(Fore.RED + "\nDC-DC Converter model parameter calculation.\n" + Style.RESET_ALL)

        while True:
            try:
                self.Vin = int(input("Enter Input Voltage(Volts): "))
                self.Vo = int(input("Enter Output Voltage(Volts): "))
                self.R = int(input("Enter output resistance(Ohms): "))
                self.fsw = int(input("Enter switching frequency(Hertz): "))

                if self.Vin > self.Vo:
                    print(Fore.LIGHTRED_EX + "It is a Buck Converter!" + Style.RESET_ALL)

                else:
                    print(Fore.LIGHTRED_EX + "It is a Boost Converter!" + Style.RESET_ALL)

                self.Irp = float(input("Enter Ripple current (Amp): "))
                self.Vrp = float(input("Enter % Output Voltage Ripple(maximum two decimal places): "))
                if self.Vrp > 1:
                    print(
                        Fore.RED + "Ripple voltage must be greater than 1. Try again!\nRecommended 30%."
                        + Style.RESET_ALL)
                    continue
            except ValueError:
                print(Fore.RED + "Invalid input! Try again." + Style.RESET_ALL)
                if input("Press 'ENTER' to continue or pass 'q' to exit -> ") == 'q':
                    sys.exit()
                else:
                    continue
            else:
                break

    def run_converter(self):
        while True:
            print(Fore.GREEN + "\nCalculating the components ratings and essential parameters ->" + Style.RESET_ALL)
            print("\tDuty Cycle of the converter: ", round(self.duty_cycle(), ndigits=2))
            print("\tAverage Output Current: {}Amp".format(round(self.output_current(), ndigits=2)))
            print("\tAverage Input Current: {}Amp".format(round(self.input_current(), ndigits=2)))
            if self.Vin > self.Vo:
                print(Fore.BLUE + "\n\tCritical Inductance(Lcr): {}H".format(
                    format(self.buck_ind(), ".3e")) + Style.RESET_ALL)
                text_ind()
                print(Fore.BLUE + "\n\tCapacitor Rating(Co): {}F".format(
                    format(self.buck_cap(), ".3e")) + Style.RESET_ALL)
                text_cap()
            else:
                print(Fore.BLUE + "\n\tCritical Inductance(Lcr): {}H".format(
                    format(self.boost_ind(), ".3e")) + Style.RESET_ALL)
                text_ind()
                print(Fore.BLUE + "\n\tCapacitor Rating(Co): {}F".format(
                    format(self.boost_cap(), ".3e")) + Style.RESET_ALL)
                text_cap()
            print(Fore.GREEN + "\nSuccessfully completed calculation!" + Style.RESET_ALL)
            break

    def duty_cycle(self):

        if self.Vin > self.Vo:
            D_buck = dutycycle.buck_duty_cycle(self.Vo, self.Vin)
            return D_buck
        else:
            D_boost = dutycycle.boost_duty_cycle(self.Vo, self.Vin)
            return D_boost

    def output_current(self):
        output_current = np.divide(self.Vo, self.R)
        return output_current

    def input_current(self):
        if self.Vin > self.Vo:
            ip_current_buck = np.multiply(self.duty_cycle(), self.output_current())
            return ip_current_buck
        else:
            ip_current_boost = np.divide(self.output_current(), np.subtract(1, self.duty_cycle()))
            return ip_current_boost

    def buck(self):

        self.buck_ind()
        self.buck_cap()

    def boost(self):

        self.boost_ind()
        self.boost_cap()

    def buck_ind(self):
        inductor = bucklc.inductor_rating(self.Vin, self.duty_cycle(), self.fsw, self.Irp)
        return inductor

    def buck_cap(self):
        capacitor = bucklc.capacitor_rating(self.Vo, self.duty_cycle(), self.buck_ind(), self.Vrp, self.fsw)
        return capacitor

    def boost_ind(self):
        inductor = boostlc.inductor_rating(self.Vin, self.duty_cycle(), self.fsw, self.Irp)
        return inductor

    def boost_cap(self):
        capacitor = boostlc.capacitor_rating(self.output_current(), self.duty_cycle(), self.Vrp, self.fsw)
        return capacitor


def text_ind():
    print(
        Fore.YELLOW + "\nCritical Inductance (Lcr) is the minimum value of the inductor for which the converter "
                      "will operate in continuous current conduction mode. "
                      "Critical Inductance is the boundary between Continuous and Discontinuous conduction modes "
                      "of the dc-dc converter. Below the critical inductance "
                      "value of the inductor the converter will start performing in discontinuous current "
                      "conduction mode. It is recommended to select inductor value "
                      "slightly above the critical inductance value, '25%' higher the critical inductance is a "
                      "decent choice." + Style.RESET_ALL)


def text_cap():
    print(
        Fore.YELLOW + "\nThe Output Capacitor (Co) is used to keep the output voltage constant and the reduce the "
                      "output Ripple Voltage. The higher the capacitor value the "
                      "lesser will be the Ripple Voltage." + Style.RESET_ALL)


if __name__ == "__main__":
    converter = Converter()
    converter.run_converter()

    while True:
        if input("\nTake another reading (y/n)-> ") == "y":
            converter.__init__()
            converter.run_converter()
        else:
            sys.exit()
