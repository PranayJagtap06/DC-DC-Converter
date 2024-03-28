#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 28 10:07:00 2022

@author: pranayjagtap
"""

"""ConverterCalc is a simple calculator for dc-dc converter built using Python and PyQt5."""

import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit,
    QComboBox,
    QLabel,
    QWidget,
    QScrollArea,
)
from ConverterPackage import bucklc, boostlc, bckbstlc
import numpy as np

Hist_list = []
file = open("file_history.txt", "a+")
file.close()


class ConverterCalcUi(QMainWindow):
    """Mainwindow."""

    switch_window = QtCore.pyqtSignal(str)

    def __init__(self, parent=None):
        """Initialize."""
        super(ConverterCalcUi, self).__init__(parent)
        QtWidgets.QWidget.__init__(self)

        self.setWindowTitle("ConverterCalc")
        self.setGeometry(200, 200, 680, 640)
        self.outerLayout = QVBoxLayout()
        self.bottomLayout = QVBoxLayout()
        self._centralWidget = QWidget(self)
        self.setCentralWidget(self._centralWidget)

        font_ = QtGui.QFont("Times", 12)

        mode_lay = QHBoxLayout()
        self.mode_label = QLabel("Converter Type")
        self.mode_label.setFont(font_)
        self.mode_ = QComboBox()
        self.mode_.setFont(font_)
        self.mode_.addItems(["--Select Type--", "boost", "buck", "buckboost"])
        mode_lay.addWidget(self.mode_label)
        mode_lay.addWidget(self.mode_)
        mode_lay.setAlignment(QtCore.Qt.AlignLeft)
        mode_lay.setSpacing(164)

        Vin_lay = QHBoxLayout()
        Vin_label = QLabel("Input Volatge(Vin)")
        Vin_label.setFont(font_)
        self.Vin = QLineEdit()
        self.Vin.setFixedWidth(150)
        self.Vin.setFont(font_)
        self.Vin.setValidator(QtGui.QDoubleValidator())
        Vin_lay.addWidget(Vin_label)
        Vin_lay.addWidget(self.Vin)
        Vin_lay.setSpacing(143)
        Vin_lay.addStretch(0)

        Vo_lay = QHBoxLayout(parent)
        self.Vo_label = QLabel("Output Volatge(Vo)")
        self.Vo_label.setFont(font_)
        self.Vo = QLineEdit()
        self.Vo.setFixedWidth(150)
        self.Vo.setFont(font_)
        self.Vo.setValidator(QtGui.QDoubleValidator())
        Vo_lay.addWidget(self.Vo_label)
        Vo_lay.addWidget(self.Vo)
        Vo_lay.setSpacing(137)
        Vo_lay.addStretch(0)

        Ro_lay = QHBoxLayout()
        self.Ro_label = QLabel("Output Resistance(Ro)")
        self.Ro_label.setFont(font_)
        self.Ro = QLineEdit()
        self.Ro.setFixedWidth(150)
        self.Ro.setFont(font_)
        self.Ro.setValidator(QtGui.QDoubleValidator())
        Ro_lay.addWidget(self.Ro_label)
        Ro_lay.addWidget(self.Ro)
        Ro_lay.setSpacing(120)
        Ro_lay.addStretch(0)

        fsw_lay = QHBoxLayout()
        self.fsw_label = QLabel("Frequency(f) (in Hz)")
        self.fsw_label.setFont(font_)
        self.fsw = QLineEdit()
        self.fsw.setFixedWidth(150)
        self.fsw.setFont(font_)
        self.fsw.setValidator(QtGui.QDoubleValidator())
        fsw_lay.addWidget(self.fsw_label)
        fsw_lay.addWidget(self.fsw)
        fsw_lay.setSpacing(133)
        fsw_lay.addStretch(0)

        Irp_lay = QHBoxLayout()
        self.Irp_label = QLabel("Percentage i/p Ripple Current(Ir)(optional)\nEg.: 40")
        self.Irp_label.setFont(font_)
        self.Irp = QLineEdit()
        self.Irp.setFixedWidth(150)
        self.Irp.setFont(font_)
        self.Irp.setValidator(QtGui.QDoubleValidator())
        Irp_lay.addWidget(self.Irp_label)
        Irp_lay.addWidget(self.Irp)
        Irp_lay.setSpacing(55)
        Irp_lay.addStretch(0)
        self.Irp.setText("0")

        Vrp_lay = QHBoxLayout()
        self.Vrp_label = QLabel("Percentage o/p Ripple Volatge(Vr)\nEg.: 3")
        self.Vrp_label.setFont(font_)
        self.Vrp = QLineEdit()
        self.Vrp.setFixedWidth(150)
        self.Vrp.setFont(font_)
        self.Vrp.setValidator(QtGui.QDoubleValidator())
        Vrp_lay.addWidget(self.Vrp_label)
        Vrp_lay.addWidget(self.Vrp)
        Vrp_lay.setSpacing(45)
        Vrp_lay.addStretch(0)

        PB_lay = QHBoxLayout()
        self.calc = QPushButton("Calculate")
        self.calc.setStyleSheet("background-color: blue")
        self.calc.setFont(font_)
        self.clear = QPushButton("Clear")
        self.clear.setStyleSheet("background-color: red")
        self.clear.setFont(font_)
        self.label = ""
        self.hist_list = ""
        self.calcResult = ScrollLabel(self)

        PB_lay.addWidget(self.calc)
        PB_lay.addWidget(self.clear)
        PB_lay.setSpacing(31)
        PB_lay.setAlignment(QtCore.Qt.AlignRight)

        self.bottomLayout.addWidget(self.calcResult)
        # self.bottomLayout.addStretch()

        self.outerLayout.addLayout(mode_lay)
        self.outerLayout.addLayout(Vin_lay)
        self.outerLayout.addLayout(Vo_lay)
        self.outerLayout.addLayout(Ro_lay)
        self.outerLayout.addLayout(fsw_lay)
        self.outerLayout.addLayout(Irp_lay)
        self.outerLayout.addLayout(Vrp_lay)
        self.outerLayout.addLayout(PB_lay)
        self.outerLayout.setSpacing(10)
        self.outerLayout.addLayout(self.bottomLayout)
        self._centralWidget.setLayout(self.outerLayout)

        self.createMenu()
        self._signals()

    def createMenu(self):
        self.menu = self.menuBar().addMenu("&Menu")
        self.menu.addAction("&Exit", self.close_)
        self.menu.addAction("&History", self.switch)
        self.menu.addAction("&Clear History", self.ClearHist)

    def labelText(self, l_):
        (
            duty,
            Pi,
            Po,
            op_current,
            Ind_current,
            ip_current,
            i_ripple,
            Ind_cr,
            Ind,
            Ind_cr_ripple,
            max_indI,
            min_indI,
            cap,
            esr,
        ) = l_
        txt1 = "Converter Paramerters:\n\tDuty Cycle = {}\n".format(duty)
        txt_I = "\tPower Input = {}W\n".format(Pi)
        txt_O = "\tPower Output = {}W\n".format(Po)
        txt2 = "\tOutput Current = {}Amp\n".format(op_current)
        txt3 = "\tInductor Current = {}Amp\n".format(Ind_current)
        txt4 = "\tInput Current = {}Amp\n".format(ip_current)
        txt5 = "\tRipple Current = {}Amp\n".format(i_ripple)
        txt6 = "\tCritical Inductance(Lcr) = {}H\n".format(Ind_cr)
        txt7 = "\tInductance(L) as per calculated ripple current = {}H\n".format(Ind)
        txt8 = "\tRipple Current due to Lcr = {}Amp\n".format(Ind_cr_ripple)
        txt9 = "\tMaximum inductor ripple current = {}Amp\n".format(max_indI)
        txt10 = "\tMinimum inductor ripple current = {}Amp\n".format(min_indI)
        txt11 = "\tOutput Capacitor = {}F\n".format(cap)
        txt12 = "\tCapacitor ESR = {}Ohms".format(esr)
        txt_ = (
            txt1
            + txt_I
            + txt_O
            + txt2
            + txt3
            + txt4
            + txt5
            + txt6
            + txt7
            + txt8
            + txt9
            + txt10
            + txt11
            + txt12
        )
        self.label = txt_
        self.calcResult.setText(txt_)

    def hist_params(self):
        Mode, Vin, Vo, R, fsw, Irp, Vrp = self.onIpEdit()
        txt13 = "Converter Mode = {}\n".format(Mode)
        txt14 = "\tVin = {}\n".format(Vin)
        txt15 = "\tVo = {}\n".format(Vo)
        txt16 = "\tRo = {}\n".format(R)
        txt17 = "\tfsw = {}\n".format(fsw)
        txt18 = "\tIrp = {}\n".format(Irp)
        txt19 = "\tVrp = {}\n".format(Vrp)
        txt_ip = txt13 + txt14 + txt15 + txt16 + txt17 + txt18 + txt19
        hist_params = txt_ip + self.label + "\n\n\n"
        hist_file = open("file_history.txt", "a+")
        hist_file.write(hist_params)
        hist_file.close()

    def onclickHist(self):
        l = list()
        st = 0
        nd = 20
        txt = ""
        file = open("file_history.txt", "r")
        f = file.readlines()
        file.close()
        for _ in range(len(f)):
            if st == len(f):
                break
            l.append(f[st:nd])
            st += 20
            nd += 20
        L = l[::-1]
        for x in range(len(L)):
            txt += "".join(L[x])
        self.hist_list = txt

    def errorLabel(self, text):
        self.calcResult.setText(text)

    def clearLabel(self):
        self.calcResult.setText("")
        self.mode_.setCurrentIndex(0)
        self.Vin.setText("")
        self.Vo.setText("")
        self.Ro.setText("")
        self.fsw.setText("")
        self.Irp.setText("0")
        self.Vrp.setText("")

    def _signals(self):
        self.calc.clicked.connect(self.evaluateResults)
        self.calc.clicked.connect(self.hist_params)
        self.clear.clicked.connect(self.clearLabel)

    def onIpEdit(self):
        try:
            mode = str(self.mode_.currentText())
            vin = float(self.Vin.text())
            vo = float(self.Vo.text())
            r = float(self.Ro.text())
            Fsw = float(self.fsw.text())
            irp = float(self.Irp.text())
            vrp = float(self.Vrp.text())
        except ValueError:
            self.errorLabel(
                "Inappropriate block values. Block values must be of type Float.\nRetry!"
            )
        finally:
            ip = [mode, vin, vo, r, Fsw, irp, vrp]
            return ip

    def evaluateResults(self):
        Mode, Vin, Vo, R, fsw, Irp, Vrp = self.onIpEdit()
        if Mode == "boost":
            duty_ = boostlc.bst_duty_cycle(Vo, Vin)
            output_current = np.round(np.divide(Vo, R), decimals=2)
            ind_current = boostlc.bst_ind_current(duty_, output_current)
            input_current = ind_current
            ind_cr = boostlc.bst_cr_ind(duty_, R, fsw)
            if Irp != 0:
                I_ripple = boostlc.bst_ripl_current(ind_current, Irp)
                ind_ = boostlc.bst_cont_ind(Vin, duty_, fsw, I_ripple)
            else:
                ind_ = np.format_float_scientific(
                    np.multiply(float(ind_cr), 1.25),
                    unique=False,
                    precision=4,
                    trim="-",
                    exp_digits=1,
                )
                I_ripple = boostlc.bst_Irp(Vin, duty_, fsw, ind_)
            ind_cr_ripple = boostlc.bst_ind_ripl_(Vin, duty_, fsw, ind_cr)
            max_indcrnt = np.round(
                np.add(float(ind_current), float(I_ripple) / 2), decimals=2
            )
            min_indcrnt = np.round(
                np.subtract(float(ind_current), float(I_ripple) / 2), decimals=2
            )
            capacitor = boostlc.bst_cap_val(duty_, R, Vrp, fsw)
            Esr = boostlc.Esr(Vrp, Vo, I_ripple)
        elif Mode == "buck":
            duty_ = bucklc.bck_duty_cycle(Vo, Vin)
            output_current = np.round(np.divide(Vo, R), decimals=2)
            ind_current = output_current
            input_current = bucklc.bck_ip_current(duty_, output_current)
            ind_cr = bucklc.bck_cr_ind(duty_, R, fsw)
            if Irp != 0:
                I_ripple = bucklc.bck_ripl_current(ind_current, Irp)
                ind_ = bucklc.bck_cont_ind(Vo, duty_, fsw, I_ripple)
            else:
                ind_ = np.format_float_scientific(
                    np.multiply(float(ind_cr), 1.25),
                    unique=False,
                    precision=4,
                    trim="-",
                    exp_digits=1,
                )
                I_ripple = bucklc.bck_Irp(Vo, duty_, fsw, ind_)
            ind_cr_ripple = bucklc.bck_ind_ripl_(Vo, duty_, fsw, ind_cr)
            max_indcrnt = np.round(
                np.add(float(ind_current), float(I_ripple) / 2), decimals=2
            )
            min_indcrnt = np.round(
                np.subtract(float(ind_current), float(I_ripple) / 2), decimals=2
            )
            capacitor = bucklc.bck_cap_val(duty_, ind_, Vrp, fsw)
            Esr = bucklc.Esr(Vrp, Vo, I_ripple)
        elif Mode == "buckboost":
            duty_ = bckbstlc.bckbst_duty_cycle(Vo, Vin)
            output_current = np.round(np.divide(Vo, R), decimals=2)
            ind_current = bckbstlc.bckbst_ind_current(duty_, output_current)
            input_current = np.round(np.multiply(ind_current, duty_), decimals=3)
            ind_cr = bckbstlc.bckbst_cr_ind(duty_, R, fsw)
            if Irp != 0:
                I_ripple = bckbstlc.bckbst_ripl_current(input_current, Irp)
                ind_ = bckbstlc.bckbst_cont_ind(Vin, duty_, fsw, I_ripple)
            else:
                ind_ = np.format_float_scientific(
                    np.multiply(float(ind_cr), 1.25),
                    unique=False,
                    precision=4,
                    trim="-",
                    exp_digits=1,
                )
                I_ripple = bckbstlc.bckbst_Irp(Vin, duty_, fsw, ind_)
            ind_cr_ripple = bckbstlc.bckbst_ind_ripl_(Vin, duty_, fsw, ind_cr)
            max_indcrnt = np.round(
                np.add(float(ind_current), float(I_ripple) / 2), decimals=2
            )
            min_indcrnt = np.round(
                np.subtract(float(ind_current), float(I_ripple) / 2), decimals=2
            )
            capacitor = bckbstlc.bckbst_cap_val(duty_, R, Vrp, fsw)
            Esr = bckbstlc.Esr(Vrp, Vo, I_ripple)
        elif Mode == "--Select Type--":
            self.errorLabel("Converter type not selected!")
        power_in = np.multiply(Vin, input_current)
        power_out = np.multiply(Vo, output_current)

        params = [
            duty_,
            power_in,
            power_out,
            output_current,
            ind_current,
            input_current,
            I_ripple,
            ind_cr,
            ind_,
            ind_cr_ripple,
            max_indcrnt,
            min_indcrnt,
            capacitor,
            Esr,
        ]
        self.labelText(l_=params)

    def ClearHist(self):
        hist_file = open("file_history.txt", "r+")
        hist_file.truncate(0)

    def switch(self):
        self.onclickHist()
        self.switch_window.emit(self.hist_list)

    def close_(self):
        self.close()


class ScrollLabel(QScrollArea):
    def __init__(self, *args, **kwargs):
        QScrollArea.__init__(self, *args, **kwargs)

        self.setWidgetResizable(True)
        content = QWidget(self)
        self.setWidget(content)
        lay = QVBoxLayout(content)
        self.label = QLabel(content)
        self.label.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.label.setWordWrap(True)
        lay.addWidget(self.label)

    def setText(self, text):
        self.label.setText(text)
        font = QtGui.QFont("Georgia", 12)
        self.label.setFont(font)
        self.label.setStyleSheet("background-color: lightgreen")


class History(QtWidgets.QWidget):
    switch_window = QtCore.pyqtSignal()

    def __init__(self, text):
        QtWidgets.QWidget.__init__(self)
        self.setWindowTitle("Calculator History")
        self.setGeometry(200, 200, 680, 640)
        hist_lay = QVBoxLayout()
        history = ScrollLabel(self)
        history.setText(text)
        self.back_button = QPushButton("Back")
        self.back_button.clicked.connect(self.back)
        self.back_button.clicked.connect(self.close)
        hist_lay.addWidget(history)
        hist_lay.addWidget(self.back_button, QtCore.Qt.AlignBottom)
        hist_lay.setAlignment(QtCore.Qt.AlignTop)
        self.setLayout(hist_lay)

    def back(self):
        self.switch_window.emit()


class Login(QtWidgets.QWidget):
    switch_window = QtCore.pyqtSignal()

    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.setWindowTitle("Login")
        self.setGeometry(200, 200, 680, 640)
        layout = QtWidgets.QGridLayout()
        self.button = QtWidgets.QPushButton("Login")
        self.button.setFont(QtGui.QFont("Times", 10))
        self.button.clicked.connect(self.login)
        layout.addWidget(self.button)
        self.setLayout(layout)

    def login(self):
        self.switch_window.emit()


class Controller:
    def __init__(self):
        pass

    def show_login(self):
        self.login = Login()
        self.login.switch_window.connect(self.show_main)
        self.login.show()

    def show_history(self, text):
        self.history_ = History(text)
        self.history_.switch_window.connect(self.show_main)
        self.history_.show()

    def show_main(self):
        self.window = ConverterCalcUi()
        self.window.switch_window.connect(self.show_history)
        self.login.close()
        self.window.show()


def main():
    convertercalc = QApplication(sys.argv)
    controller = Controller()
    controller.show_login()
    sys.exit(convertercalc.exec_())


if __name__ == "__main__":
    main()
