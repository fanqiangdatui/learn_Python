import sys
from PyQtCloudGUI import *
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QFileDialog


class MainWindow(QMainWindow, Ui_Form):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.textEdit.setText('message')



if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())