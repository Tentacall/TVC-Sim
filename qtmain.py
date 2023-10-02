import pybullet as p
import pybullet_data
from PyQt5.QtWidgets import QApplication, QMainWindow, QOpenGLWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Rocket Simulation")

        