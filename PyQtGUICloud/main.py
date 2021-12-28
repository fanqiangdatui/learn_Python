# import sys
# from PyQtCloudGUI import *
# from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QFileDialog
#
#
# class MainWindow(QMainWindow, Ui_Form):
#     def __init__(self, parent=None):
#         super(MainWindow, self).__init__(parent)
#         self.setupUi(self)
#         self.textEdit.setText('message')
#         self.pushButton_Live.clicked.connect(self.pr)
#     def pe(self):
#         return 'jghdjdg'
#
#
#
# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     mainWindow = MainWindow()
#     mainWindow.show()
#     sys.exit(app.exec_())
import sys
#PyQt5中使用的基本控件都在PyQt5.QtWidgets模块中
from PyQt5.QtWidgets import QApplication, QMainWindow
#导入designer工具生成的login模块
from PyQtCloudGUI import Ui_Form
import cloud

class MyMainForm(QMainWindow, Ui_Form):
    def __init__(self, parent=None):
        super(MyMainForm, self).__init__(parent)
        self.setupUi(self)
        #添加登录按钮信号和槽。注意display函数不加小括号()
        self.pushButton_Live.clicked.connect(self.GetNorthToken)

    def GetNorthToken(self):
        #利用line Edit控件对象text()函数获取界面输入
        self.textEdit.setText(cloud.CLOUD().GetToken(self.comboBox_env.currentText()))

if __name__ == "__main__":
    #固定的，PyQt5程序都需要QApplication对象。sys.argv是命令行参数列表，确保程序可以双击运行
    app = QApplication(sys.argv)
    #初始化
    myWin = MyMainForm()
    #将窗口控件显示在屏幕上
    myWin.show()
    #程序运行，sys.exit方法确保程序完整退出。
    sys.exit(app.exec_())