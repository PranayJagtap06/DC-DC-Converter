"""ConverterCalc is a simple calculator for dc-dc converter built using Python and PyQt5."""

import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QHBoxLayout, QLineEdit, QComboBox, QLabel, QWidget, QScrollArea
from ConverterPackage import bucklc, boostlc, bckbstlc
import numpy as np
Hist_list = []
file = open('file_history.txt', 'a+')
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

        font_ = QtGui.QFont("Times", 10)

        mode_lay = QHBoxLayout()
        self.mode_label = QLabel('Converter Type')
        self.mode_label.setFont(font_)
        self.mode_ = QComboBox()
        self.mode_.setFont(font_)
        self.mode_.addItems(['--Select Type--', 'boost', 'buck', 'buckboost'])
        mode_lay.addWidget(self.mode_label)
        mode_lay.addWidget(self.mode_)
        mode_lay.setAlignment(QtCore.Qt.AlignLeft)
        mode_lay.setSpacing(164)

        Vin_lay = QHBoxLayout()
        Vin_label = QLabel('Input Volatge(Vin)')
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
        self.Vo_label = QLabel('Output Volatge(Vo)')
        self.Vo_label.setFont(font_)
        self.Vo = QLineEdit()
        self.Vo.setFixedWidth(150)
        self.Vo.setFont(font_)
        self.Vo.setValidator(QtGui.QDoubleValidator())
        Vo_lay.addWidget(self.Vo_label)
        Vo_lay.addWidget(self.Vo)
        Vo_lay.setSpacing(136)
        Vo_lay.addStretch(0)

        Rin_lay = QHBoxLayout()
        self.Rin_label = QLabel('Output Resistance(Ro)')
        self.Rin_label.setFont(font_)
        self.Rin = QLineEdit()
        self.Rin.setFixedWidth(150)
        self.Rin.setFont(font_)
        self.Rin.setValidator(QtGui.QDoubleValidator())
        Rin_lay.addWidget(self.Rin_label)
        Rin_lay.addWidget(self.Rin)
        Rin_lay.setSpacing(110)
        Rin_lay.addStretch(0)

        fsw_lay = QHBoxLayout()
        self.fsw_label = QLabel('Frequency(f)\n(in Hz)')
        self.fsw_label.setFont(font_)
        self.fsw = QLineEdit()
        self.fsw.setFixedWidth(150)
        self.fsw.setFont(font_)
        self.fsw.setValidator(QtGui.QDoubleValidator())
        fsw_lay.addWidget(self.fsw_label)
        fsw_lay.addWidget(self.fsw)
        fsw_lay.setSpacing(185)
        fsw_lay.addStretch(0)

        Irp_lay = QHBoxLayout()
        self.Irp_label = QLabel('Percentage i/p Ripple Current(Ir)')
        self.Irp_label.setFont(font_)
        self.Irp = QLineEdit()
        self.Irp.setFixedWidth(150)
        self.Irp.setFont(font_)
        self.Irp.setValidator(QtGui.QDoubleValidator())
        Irp_lay.addWidget(self.Irp_label)
        Irp_lay.addWidget(self.Irp)
        Irp_lay.setSpacing(35)
        Irp_lay.addStretch(0)

        Vrp_lay = QHBoxLayout()
        self.Vrp_label = QLabel('Percentage o/p Ripple Volatge(Vr)')
        self.Vrp_label.setFont(font_)
        self.Vrp = QLineEdit()
        self.Vrp.setFixedWidth(150)
        self.Vrp.setFont(font_)
        self.Vrp.setValidator(QtGui.QDoubleValidator())
        Vrp_lay.addWidget(self.Vrp_label)
        Vrp_lay.addWidget(self.Vrp)
        Vrp_lay.setSpacing(25)
        Vrp_lay.addStretch(0)

        PB_lay = QHBoxLayout()
        self.calc = QPushButton('Calculate')
        self.calc.setStyleSheet('background-color: blue')
        self.calc.setFont(font_)
        self.clear = QPushButton('Clear')
        self.clear.setStyleSheet('background-color: red')
        self.clear.setFont(font_)
        self.label = ''
        self.hist_list = ''
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
        self.outerLayout.addLayout(Rin_lay)
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
        duty, op_current, ip_current, i_ripple, Ind_cr, Ind, Ind_cr_ripple, max_indI, min_indI, cap = l_
        txt1 = "Converter Paramerters:\n\tDuty Cycle = {}\n".format(duty)
        txt2 = "\tOutput Current = {}Amp\n".format(op_current)
        txt3 = "\tInput Current = {}Amp\n".format(ip_current)
        txt4 = "\tRipple Current = {}Amp\n".format(i_ripple)
        txt5 = "\tCritical Inductance(Lcr) = {}H\n".format(Ind_cr)
        txt6 = "\tInductance(L) as per calculated ripple current = {}H\n".format(
            Ind)
        txt7 = "\tRipple Current due to Lcr = {}Amp\n".format(Ind_cr_ripple)
        txt8 = "\tMaximum inductor ripple current = {}Amp\n".format(max_indI)
        txt9 = "\tMinimum inductor ripple current = {}Amp\n".format(min_indI)
        txt10 = "\tOutput Capacitor = {}F".format(cap)
        txt_ = txt1 + txt2 + txt3 + txt4 + txt5 + txt6 + txt7 + txt8 + txt9 + txt10
        self.label = txt_
        self.calcResult.setText(txt_)

    def hist_params(self):
        Mode, Vin, Vo, R, fsw, Irp, Vrp = self.onIpEdit()
        txt11 = "Converter Mode = {}\n".format(Mode)
        txt12 = "\tVin = {}\n".format(Vin)
        txt13 = "\tVo = {}\n".format(Vo)
        txt14 = "\tRo = {}\n".format(R)
        txt15 = "\tfsw = {}\n".format(fsw)
        txt16 = "\tIrp = {}\n".format(Irp)
        txt17 = "\tVrp = {}\n".format(Vrp)
        txt_ip = txt11+txt12+txt13+txt14+txt15+txt16+txt17
        hist_params = txt_ip + self.label + "\n\n\n"
        hist_file = open('file_history.txt', 'a+')
        hist_file.write(hist_params)
        hist_file.close()

    def onclickHist(self):
        l = list()
        st = 0
        nd = 20
        txt = ''
        file = open('file_history.txt', 'r')
        f = file.readlines()
        file. close()
        for _ in range(len(f)):
            if st == len(f):
                break
            l.append(f[st:nd])
            st += 20
            nd += 20
        L = l[::-1]
        for x in range(len(L)):
            txt += ''. join(L[x])
        self.hist_list = txt

    def errorLabel(self, text):
        self.label = text

    def clearLabel(self):
        self.calcResult.setText('')
        self.mode_.setCurrentIndex(0)
        self.Vin.setText('')
        self.Vo.setText('')
        self.Rin.setText('')
        self.fsw.setText('')
        self.Irp.setText('')
        self.Vrp.setText('')

    def _signals(self):
        self.calc.clicked.connect(self.evaluateResults)
        self.calc.clicked.connect(self.hist_params)
        self.clear.clicked.connect(self.clearLabel)

    def onIpEdit(self):
        mode = str(self.mode_.currentText())
        vin = float(self.Vin.text())
        vo = float(self.Vo.text())
        r = float(self.Rin.text())
        Fsw = float(self.fsw.text())
        irp = float(self.Irp.text())
        vrp = float(self.Vrp.text())
        ip = [mode, vin, vo, r, Fsw, irp, vrp]
        return ip

    def evaluateResults(self):
        Mode, Vin, Vo, R, fsw, Irp, Vrp = self.onIpEdit()
        try:
            if Mode == 'boost':
                duty_ = boostlc.bst_duty_cycle(Vo, Vin)
                output_current = np.round(np.divide(Vo, R), decimals=2)
                input_current = boostlc.bst_ind_current(duty_, output_current)
                I_ripple = boostlc.bst_ripl_current(input_current, Irp)
                ind_cr = boostlc.bst_cr_ind(duty_, R, fsw)
                ind_ = boostlc.bst_cont_ind(Vin, duty_, fsw, I_ripple)
                ind_cr_ripple = boostlc.bst_ind_ripl_(Vin, duty_, fsw, ind_cr)
                max_indcrnt = np.round(
                    np.add(float(input_current), float(I_ripple)/2), decimals=2)
                min_indcrnt = np.round(np.subtract(
                    float(input_current), float(I_ripple)/2), decimals=2)
                capacitor = boostlc.bst_cap_val(Vo, duty_, R, Vrp, fsw)
            elif Mode == 'buck':
                duty_ = bucklc.bck_duty_cycle(Vo, Vin)
                output_current = np.round(np.divide(Vo, R), decimals=2)
                input_current = bucklc.bck_ind_current(duty_, output_current)
                I_ripple = bucklc.bck_ripl_current(input_current, Irp)
                ind_cr = bucklc.bck_cr_ind(duty_, R, fsw)
                ind_ = bucklc.bck_cont_ind(Vo, duty_, fsw, I_ripple)
                ind_cr_ripple = bucklc.bck_ind_ripl_(Vo, duty_, fsw, ind_cr)
                max_indcrnt = np.round(
                    np.add(float(input_current), float(I_ripple)/2), decimals=2)
                min_indcrnt = np.round(np.subtract(
                    float(input_current), float(I_ripple)/2), decimals=2)
                capacitor = bucklc.bck_cap_val(Vo, duty_, R, Vrp, fsw)
            elif Mode == 'buckboost':
                duty_ = bckbstlc.bckbst_duty_cycle(Vo, Vin)
                output_current = np.round(np.divide(Vo, R), decimals=2)
                input_current = bckbstlc.bckbst_ind_current(
                    duty_, output_current)
                I_ripple = bckbstlc.bckbst_ripl_current(input_current, Irp)
                ind_cr = bckbstlc.bckbst_cr_ind(duty_, R, fsw)
                ind_ = bckbstlc.bckbst_cont_ind(Vin, duty_, fsw, I_ripple)
                ind_cr_ripple = bckbstlc.bckbst_ind_ripl_(
                    Vin, duty_, fsw, ind_cr)
                max_indcrnt = np.round(
                    np.add(float(input_current), float(I_ripple)/2), decimals=2)
                min_indcrnt = np.round(np.subtract(
                    float(input_current), float(I_ripple)/2), decimals=2)
                capacitor = bckbstlc.bckbst_cap_val(Vo, duty_, R, Vrp, fsw)

        except Exception:
            msg = 'ERROR_MSG'
            self.errorLabel(msg)
        params = [duty_, output_current, input_current, I_ripple, ind_cr,
                  ind_, ind_cr_ripple, max_indcrnt, min_indcrnt, capacitor]
        self.labelText(l_=params)

    def ClearHist(self):
        hist_file = open('file_history.txt', 'r+')
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
        self.label.setStyleSheet('background-color: lightgreen')


class History(QtWidgets.QWidget):
    switch_window = QtCore.pyqtSignal()

    def __init__(self, text):
        QtWidgets.QWidget.__init__(self)
        self.setWindowTitle('Calculator History')
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
        self.setWindowTitle('Login')
        self.setGeometry(200, 200, 680, 640)
        layout = QtWidgets.QGridLayout()
        self.button = QtWidgets.QPushButton('Login')
        self.button.setFont(QtGui.QFont('Times', 10))
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
