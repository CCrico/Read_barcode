from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPixmap
from PIL import ImageTk, Image
import sys
import cv2
import detect_barcode as db
import detect_numberBarcode as dnb
class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('gui.ui', self)
        self.button = self.findChild(QtWidgets.QPushButton, 'barcode') 
        self.button.clicked.connect(self.printButtonPressed) 
        self.input = self.findChild(QtWidgets.QTextEdit, 'input')
        self.output = self.findChild(QtWidgets.QTextEdit, 'output')
        self.show()
    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            print("123")
            pixmap = QPixmap(self.input.toPlainText()[8:])
            self.label_1.setPixmap(pixmap)
            self.label_1.setScaledContents(True)
            self.resize(pixmap.width(), pixmap.height())

    def printButtonPressed(self):
        pixmap = QPixmap(self.input.toPlainText()[8:])
        self.label_1.setPixmap(pixmap)
        self.label_1.setScaledContents(True)
        self.resize(pixmap.width(), pixmap.height())

        db.detectBarcode(self.input.toPlainText()[8:])
        pixmap = QPixmap('barcode.png')
        self.label_2.setPixmap(pixmap)
        self.output.setText(dnb.run())
        print(self.output.toPlainText())
app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_()
