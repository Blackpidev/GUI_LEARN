from concurrent.futures import thread
from time import sleep
from PyQt5.QtCore import QThread, pyqtSignal

class ThreadManager(QThread):
    sig_show_table = pyqtSignal(list, str)
    sig_show_bar = pyqtSignal(str)

    def __init__(self):
        super(ThreadManager, self).__init__()
        global stop_thread
        stop_thread = False
        self.thread_running = 0

    def run(self):
        self.startThreadRunning()

    def step_thread_running(self):
        self.thread_running -= 1

    def startThreadRunning(self):
        count = 0
        while not stop_thread:
            if self.thread_running == 0:
                self.thread_object = {}
                for x in range(self.spThread):
                    self.thread_object[x] = DemoReadFile()
                    try:
                        self.thread_object[x].setName(count, self.data_boys[count], self.data_girls[count])
                    except IndexError:
                        break
                    self.thread_object[x].sig_show_bar.connect(self.sig_show_bar)
                    self.thread_object[x].sig_show_table.connect(self.sig_show_table)
                    self.thread_object[x].sig_done.connect(self.step_thread_running)
                    self.thread_object[x].start()
                    self.thread_running += 1
                    count+=1
                    sleep(0.05)
            sleep(0.05)

    def set_options(self, options):
        path_boy = options.get('path_boy')
        path_girl = options.get('path_girl')
        self.spThread = options.get('spThread')
        with open(path_boy, 'r', encoding="utf8") as f:
            self.data_boys = f.read().split('\n')
        with open(path_girl, 'r', encoding="utf8") as f:
            self.data_girls = f.read().split('\n')

    def setStop(self):
        try:
            for value, thread_object in self.thread_object.items():
                thread_object.setStop(value)
        except:
            pass
        global stop_thread
        stop_thread = True


class DemoReadFile(QThread):
    sig_show_table = pyqtSignal(list, str)
    sig_show_bar = pyqtSignal(str)
    sig_done = pyqtSignal()

    def __init__(self):
        super(DemoReadFile, self).__init__()
        global stop_thread
        stop_thread = False

    def run(self):

        self.sig_show_bar.emit("Start")
        # sleep(100)
        self.read_file()
        self.sig_done.emit()

    def read_file(self):
        if stop_thread:
            return
        self.sig_show_table.emit(
            [self.row_index, 3, f"Name => {self.boy}|{self.girl}"], "AHIHI")
        sleep(1)

    def setName(self, row, boy, girl):
        self.row_index = row
        self.boy = boy
        self.girl =girl

    def setStop(self, value):
        print("set_stop", value)
        global stop_thread
        stop_thread = True
