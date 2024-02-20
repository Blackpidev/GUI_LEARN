import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem
from PyQt5.QtCore import Qt, pyqtSlot
from threadReadFile import ThreadManager
from ui_main import Ui_MainWindow

class Main(QMainWindow):
    def __init__(self):
        super(Main, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui_controller()

    def ui_controller(self):
        self.ui.btnStart.clicked.connect(self.runStart)
        self.ui.btnStop.clicked.connect(self.runStop)

    def runStart(self):
        path_boy = r'D:\KHOAHOC\giaodien_android\DS\Boys_First_Names_Top_1000.txt'
        path_girl = r'D:\KHOAHOC\giaodien_android\DS\Girls_Names_Top_1000.txt'
        spThread = self.ui.spThread.value()

        options = {
            "path_boy": path_boy,
            "path_girl": path_girl,
            "spThread": spThread
        }
        self.thread_start = ThreadManager()
        self.thread_start.set_options(options)
        self.thread_start.sig_show_bar.connect(self.showBar)
        self.thread_start.sig_show_table.connect(self.showTable)
        self.thread_start.start()

    def runStop(self):
        try:
            self.thread_start.setStop()
        except:
            pass

    def showBar(self, log):
        self.ui.statusbar.showMessage(log)

    def showTable(self, datas, value):
        # self.ui.tbShow.
        countRow = self.ui.tbShow.rowCount()
        self.ui.tbShow.setRowCount(countRow+1)
        row, col, message = datas
        self.ui.tbShow.setItem(row, col, QTableWidgetItem(str(message)))

if __name__ == "__main__":

    app = QApplication(sys.argv)
    main = Main()
    main.show()
    sys.exit(app.exec_())
