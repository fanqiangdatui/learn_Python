# -*- coding: utf-8 -*-
import sys
#PyQt5中使用的基本控件都在PyQt5.QtWidgets模块中
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import QDateTime
#导入designer工具生成的login模块
from PyQtCloudGUI import Ui_Form
import cloud

class CloudMainForm(QMainWindow, Ui_Form):
    def __init__(self, parent=None):
        super(CloudMainForm, self).__init__(parent)
        self.setupUi(self)
        #添加登录按钮信号和槽。注意display函数不加小括号()
        # self.pushButton_Live.clicked.connect(self.GetNorthToken)
        self.dateTimeEdit_start_time.setDateTime(QDateTime.currentDateTime().addDays(1))
        self.dateTimeEdit_stop_time.setDateTime(QDateTime.currentDateTime().addDays(-1))
        self.PyQtGUIInfo = {"env":self.comboBox_env.currentText(),
                            "device_id":self.comboBox_device_id.currentText(),
                            "channel_id":self.comboBox_channel_id.currentText(),
                            "live_protocol":self.comboBox_live_protocol.currentText(),
                            "playback_protocol ":self.comboBox_playback_protocol.currentText(),
                            "stream_type":self.comboBox_stream_type.currentText(),
                            "record_type":self.comboBox_record_type.currentText(),
                            "Client_Type":self.comboBox_Client_Type.currentText(),
                            "start_time":self.dateTimeEdit_start_time.text(),
                            "stop_time":self.dateTimeEdit_stop_time.text(),
                            "rtsp_info":self.comboBox_rtsp.currentText(),
                            }
        self.pushButton_Live.clicked.connect(self.GetNorthToken)

    def GetNorthToken(self):
        #利用line Edit控件对象text()函数获取界面输入
        self.textEdit.setText(cloud.CLOUD().GetToken(self.comboBox_env.currentText()))
        # print(self.comboBox_env.currentText())
        print(self.PyQtGUIInfo)

if __name__ == "__main__":
    #固定的，PyQt5程序都需要QApplication对象。sys.argv是命令行参数列表，确保程序可以双击运行
    app = QApplication(sys.argv)
    #初始化
    CloudMainForm = CloudMainForm()
    CloudMainForm.setWindowTitle("PyQtCloudGUI")
    CloudMainForm.move(0,0)
    #将窗口控件显示在屏幕上
    CloudMainForm.show()
    #程序运行，sys.exit方法确保程序完整退出。
    sys.exit(app.exec_())