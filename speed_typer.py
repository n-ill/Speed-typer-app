from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton
import sys
import random
import time
#################This is working on xubuntu virtual box but no on windows ???#####################


class MyWindow(QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.setFixedSize(600,400)
        self.setWindowTitle("Speed Typer Test")

        self.quote_list = get_quotes_list()

        self.label = QLabel(self)
        self.current_quote = ""
        self.random_quote() #set inital quote
        #self.label.setText('<span style="background-color:#D8D5D4;">Placeholder</span>')
        self.label.setGeometry(25,5,550,300)
        self.label.setWordWrap(True)
        self.label.setStyleSheet("border : 2px solid black; font-size: 18px;")

        self.counter_label = QLabel(self)
        self.counter_label.setGeometry(275,310,50,30)
        self.counter_label.setAlignment(QtCore.Qt.AlignCenter)
        self.counter_label.setStyleSheet("border : 2px solid black; font-size: 18px;")


        self.random_button = QPushButton(self)
        self.random_button.clicked.connect(self.random_quote)
        self.random_button.setGeometry(50,310,100,25)
        self.random_button.setText("Random Prompt")
        self.start_button = QPushButton(self)
        self.start_button.clicked.connect(self.start_countdown)
        self.start_button.setGeometry(450,310,100,25)
        self.start_button.setText("Start")

        self.user_input = QLineEdit(self)
        self.user_input.setGeometry(200, 350, 200, 30)
        self.user_input.setStyleSheet("font-size: 16px;")
        #self.user_input.setDisabled(True)

        self.count = 5 #5 second countdown
        self.countdown_timer = QtCore.QTimer(self)
        self.countdown_timer.timeout.connect(self.countdown)
        self.countdown_timer.start(1000)

        self.start = False
        self.temp()

    def random_quote(self):
        rand_quote = random.choice(self.quote_list)
        self.label.setText(rand_quote)
        self.current_quote = rand_quote

    def countdown(self):
        if self.start:
            self.counter_label.setText(str(self.count))
            self.count -= 1

            if self.count == 0: # open up input box 1 second before start
                self.user_input.setDisabled(False)

            if self.count == -1:
                self.start = False
                self.counter_label.setText('GO')
                self.counter_label.setStyleSheet("background-color:green;")


    def start_countdown(self):
        self.counter_label.setText("")
        self.count = 5 # resets the timer
        self.counter_label.setStyleSheet("background-color:red;")
        self.user_input.setDisabled(True)
        self.user_input.clear()
        self.start = True

        if self.count == -1:
            self.start = False

    def temp(self):
        list = self.current_quote.split(' ')
        self.label.setText(f'<span style="background-color:#C6C2C1 ;">{list[0]}</span>' + ' ' + ' '.join(list[1:]))

def get_quotes_list():
    list = []

    with open('quotes.txt', 'r') as file:
        for line in file:
            list.append(line)

    return list


app = QApplication(sys.argv)
win = MyWindow()

win.show()
sys.exit(app.exec_())

#TO DO:
#input checking - might need timer object to check input ever 1 ms or so
#need to move over the highlight to current word - the temp func
#another timer for wpm calculation etc