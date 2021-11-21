from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
import sys

def window() :
    app = QApplication(sys.argv)
    win = QMainWindow()
    win.setGeometry(150, 150, 400, 400)
    win.setWindowTitle("Gotcha")
    
    label = QLabel(win)
    label.setText("my first label")
    label.move(50, 50)  

    win.show()
    sys.exit(app.exec_())

window()




# from PyQt5.QtGui import * 
# from PyQt5.QtWidgets import * 
# import sys
  
# class Window(QMainWindow):
    # def __init__(self):
        # super().__init__()
  
        # # set the title
        # self.setWindowTitle("Geometry")
  
        # # setting  the geometry of window
        # # setGeometry(left, top, width, height)
        # self.setGeometry(100, 60, 1000, 800)
  
        # # creating a label widget
        # self.widget = QLabel('Hello', self)
  
  
  
        # # show all the widgets
        # self.show()
  
  
  
# # create pyqt5 app
# App = QApplication(sys.argv)
  
# # create the instance of our Window
# window = Window()
# # start the app
# sys.exit(App.exec())