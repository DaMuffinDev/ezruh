from Resources.Imports import *
import install
import random
import time
import sys

class MainScreen(Widget):
    def __init__(self):
        super().__init__()
        self.window_width, self.window_height = 1200, 800
        self.setMinimumSize(self.window_width, self.window_height)

        layout = VBoxLayout()
        self.setLayout(layout)

class SplashScreen(Widget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Spash Screen Example')
        self.setFixedSize(700, 300)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.counter = 0
        self.repeat = 3
        self.n = 100 # total instance

        self.initUI()

        self.timer = QTimer()
        self.timer.timeout.connect(self.loading)
        self.timer.start(5)

    def initUI(self):
        layout = VBoxLayout()
        self.setLayout(layout)

        self.frame = Frame()
        layout.addWidget(self.frame)

        self.labelTitle = Label(self.frame)
        self.labelTitle.setObjectName('LabelTitle')

        # center labels
        self.labelTitle.resize(self.width() - 10, 100)
        self.labelTitle.move(0, 10) # x, y
        self.labelTitle.setText('Ezruh')
        self.labelTitle.setAlignment(Qt.AlignCenter)

        self.labelDescription = Label(self.frame)
        self.labelDescription.resize(self.width() - 10, 50)
        self.labelDescription.move(0, self.labelTitle.height())
        self.labelDescription.setObjectName('LabelDesc')
        self.labelDescription.setText("Locating script [text]")
        self.labelDescription.setAlignment(Qt.AlignCenter)

        self.progressBar = ProgressBar(self.frame)
        self.progressBar.resize(self.width() - 200 - 10, 30)
        self.progressBar.move(100, self.labelDescription.y() + 50)
        self.progressBar.setAlignment(Qt.AlignCenter)
        self.progressBar.setFormat('%p%')
        self.progressBar.setTextVisible(True)
        self.progressBar.setRange(0, self.n)
        self.progressBar.setValue(20)

        self.labelLoading = Label(self.frame)
        self.labelLoading.resize(self.width() - 10, 70)
        self.labelLoading.move(0, self.progressBar.y() + 30)
        self.labelLoading.setObjectName('LabelLoading')
        self.labelLoading.setAlignment(Qt.AlignCenter)
        self.labelLoading.setText('loading...')

    def loading(self):
        self.progressBar.setValue(self.counter)

        if self.counter == int(self.n * 0.3):
            if self.repeat == 3:
                self.labelDescription.setText("Verifying script [text]")
                if not install.verify_build_file("Modules/text.py"):
                    install.repair("Modules")
            elif self.repeat == 2:
                self.labelDescription.setText("Verifying script [email]")
                if not install.verify_build_file("Modules/mailer.py"):
                    install.repair("Modules")
            elif self.repeat == 1:
                self.labelDescription.setText("Verifying Resources & Assets")
                if not install.verify_build_folder("Resources"):
                    install.repair("Resources")
                
                if not install.verify_build_folder("Assets"):
                    install.repair("Assets")
                
                if not install.verify_build_folder("Modules"):
                    install.repair("Modules")
        elif self.counter == int(self.n * 0.6):
            if self.repeat == 3:
                self.labelDescription.setText("Retrieving script [text]")
            elif self.repeat == 2:
                self.labelDescription.setText("Retrieving script [email]")
            elif self.repeat == 1:
                self.labelDescription.setText("Retrieving Resources & Assets")
        elif self.counter >= self.n:
            if self.repeat == 1:
                self.timer.stop()
                self.close()

                self.MainScreen = MainScreen()
                self.MainScreen.show()
            else:
                self.repeat -= 1
                self.counter = 0

                if self.repeat == 2:
                    self.labelDescription.setText("Locating script [email]")
                elif self.repeat == 1:
                    self.labelDescription.setText("Locating Resources & Assets")

        if random.randint(0, 100) <= 1:
            time.sleep(random.randint(1, 5)/10)
        self.counter += 1

if __name__ == '__main__':
    # don't auto scale when drag app to a different monitor.
    # QApplication.setAttribute(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    
    app = App(sys.argv)
    app.setStyleSheet('''
        #LabelTitle {
            font-size: 40px;
            color: #000;
        }

        #LabelDesc {
            font-size: 20px;
            color: #000;
        }

        #LabelLoading {
            font-size: 25px;
            color: #000;
        }

        QFrame {
            background-color: #FFFFFF;
            color: rgb(220, 220, 220);
        }

        QProgressBar {
            background-color: #cccccc;
            color: #000;
            border-style: none;
            text-align: center;
            font-size: 15px;
        }

        QProgressBar::chunk {
            background-color: #63FFA8;
        }
    ''')
    
    splash = SplashScreen()
    splash.show()

    try:
        sys.exit(app.exec_())
    except:
        sys.exit(1)