from PyQt5 import QtWidgets, uic
from PyQt5.QtGui import QIcon, QPixmap
import sys
import cv2
import detect_barcode as db
import detect_numberBarcode as dnb
class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('gui.ui', self)
        self.button = self.findChild(QtWidgets.QPushButton, 'printButton') # Find the button
        self.button.clicked.connect(self.printButtonPressed) # Remember to pass the definition/method, not the return value!
        self.input = self.findChild(QtWidgets.QLineEdit, 'input')
        self.show()
    def printButtonPressed(self):
        db.detectBarcode(self.input.text())
        pixmap = QPixmap('barcode.png')
        self.label.setPixmap(pixmap)
        self.textOutput.setText(dnb.run())
        
app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_()
