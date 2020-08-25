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
        self.setFixedSize(600,500)
        self.setWindowTitle("Speed Typer Test")

        self.wpm = 0

        self.wpm_label = QLabel(self)
        self.wpm_label.setGeometry(200, 400, 100, 30)
        self.wpm_label.setStyleSheet("border : 2px solid black; font-size: 22px;")

        self.label = QLabel(self)
        self.label.setGeometry(25,5,550,300)
        self.label.setWordWrap(True)
        self.label.setStyleSheet("border : 2px solid black; font-size: 18px;")

        self.timer_label = QLabel(self)
        self.timer_label.setGeometry(200, 310, 100, 30)
        self.timer_label.setAlignment(QtCore.Qt.AlignCenter)
        self.timer_label.setStyleSheet("border : 2px solid black; font-size: 12px;")

        self.counter_label = QLabel(self)
        self.counter_label.setGeometry(325, 310, 50, 30)
        self.counter_label.setAlignment(QtCore.Qt.AlignCenter)
        #self.counter_label.setStyleSheet("border : 2px solid black; font-size: 18px;")

        self.quote_list = get_quotes_list()
        self.current_quote = ""
        self.current_word_index = 0  # need to update this <<<<<<
        self.random_quote()  # set current_quote
        self.quote_word_list = self.current_quote.split(' ')

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
        self.start = False
        self.countdown_timer = QtCore.QTimer(self)
        self.countdown_timer.timeout.connect(self.countdown)
        self.countdown_timer.start(1000)

        #timer for wpm calculations
        self.timer_start = False
        self.total_time = 0
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.wpm_timer)
        self.timer.start(1)

        self.highlight_curr_word()
        self.input_start = False
        self.user_input.textChanged.connect(self.check_input)

    def random_quote(self):
        self.current_word_index = 0
        rand_quote = random.choice(self.quote_list)
        self.label.setText(rand_quote)
        self.current_quote = rand_quote
        self.quote_word_list = self.current_quote.split(' ')
        self.highlight_curr_word()
        self.total_time = 0
        self.timer_label.setText("")
        self.counter_label.setText("")
        self.counter_label.setStyleSheet("border : 2px solid black; font-size: 18px;")
        self.wpm_label.setText("   wpm")


    def countdown(self):
        if self.start:
            self.counter_label.setText(str(self.count))
            self.count -= 1

            if self.count == -1: #when countdown ends
                self.start = False
                self.timer_start = True
                self.input_start = True
                self.user_input.clear()
                self.counter_label.setText('GO')
                self.counter_label.setStyleSheet("background-color:green;")


    def start_countdown(self):
        self.counter_label.setText("")
        self.count = 5 # resets the timer
        self.counter_label.setStyleSheet("background-color:red;")
        # self.user_input.setDisabled(True)
        self.user_input.clear()
        self.start = True

        if self.count == -1:
            self.start = False

    def highlight_curr_word(self):
        list = self.current_quote.split(' ')
        if self.current_word_index < len(self.quote_word_list):
            self.label.setText(' '.join(list[0:self.current_word_index]) + ' ' +
                               f'<span style="background-color:#C6C2C1 ;">{list[self.current_word_index]}</span>'
                               + ' ' + ' '.join(list[self.current_word_index+1:]))
        else:
            self.label.setText(self.current_quote)

    def check_input(self):
        if self.input_start:
            if self.current_word_index < len(self.quote_word_list)-1:
                if self.user_input.text() == (self.quote_word_list[self.current_word_index] + ' '):
                    self.user_input.clear()
                    self.current_word_index += 1
                    self.highlight_curr_word()
            else: #### Makes it so you don't need to press space after the final word
                if self.user_input.text() == (self.quote_word_list[self.current_word_index]):
                    self.user_input.clear()
                    self.current_word_index += 1
                    self.highlight_curr_word()
            if self.current_word_index == len(self.quote_word_list):
                self.timer_start = False
                self.input_start = False
                self.wpm_calculator()
                self.wpm_label.setText(str(self.wpm) + ' wpm')


    def wpm_timer(self):
        if self.timer_start:
            self.total_time += 0.001
            self.timer_label.setText(str(round(self.total_time,3)) + 's')

    def wpm_calculator(self):
        self.wpm = int((len(self.current_quote) / 5) / (self.total_time / 60))


def get_quotes_list():
    with open('quotes_fixed.txt', 'r') as file:
        list = file.read().split('\n')

    return list


app = QApplication(sys.argv)
win = MyWindow()

win.show()
sys.exit(app.exec_())