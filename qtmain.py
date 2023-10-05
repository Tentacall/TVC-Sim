import sys
import random
from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QSurfaceFormat
from PySide6.QtWidgets import (QMainWindow, QApplication, QWidget, QVBoxLayout, QSplitter,
                                QDockWidget, QPushButton)
from components.viewport import RenderWindow
# from tutorial.tut2 import RenderWindow

class App(QMainWindow):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.setWindowTitle("SimModule")

        # menubars
        self.menu = self.menuBar()
        file_menu = self.menu.addMenu("File")
        help_menu = self.menu.addMenu("Help")

        quit_action = file_menu.addAction("Quit")
        quit_action.triggered.connect(self.quit_app)

        #central Widgets
        c_widget = QWidget(self)
        v_box_layout = QVBoxLayout(c_widget)
        splitter = QSplitter()


        self._render_window = RenderWindow(QSurfaceFormat())
        container = QWidget.createWindowContainer(self._render_window)
        container.setMinimumSize(QSize(400,400))
        splitter.addWidget(container)

        v_box_layout.addWidget(splitter)

        # docked_widget = QDockWidget("viewport", self)
        # docked_widget.setWidget(QPushButton("sex"))
        # self.addDockWidget(Qt.LeftDockWidgetArea, docked_widget)
        
        self.setCentralWidget(c_widget)

    def quit_app(self):
        self.app.quit()

if __name__ == "__main__":
    app = QApplication([])

    widget = App(app)
    widget.resize(800, 600)
    widget.show()

    sys.exit(app.exec())