import pybullet as p
import pybullet_data
import serial
import time

class Simulation:
    def __init__(self) -> None:
        self.client = p.connect(p.GUI, )
        p.setAdditionalSearchPath(pybullet_data.getDataPath())

        self.startPos = [0,0,0.5]
        self.orientation = [0.0,0.0,0.0,1.0]
        self.accelerations = [0,0,0]

        self.PORT = '/dev/ttyUSB0'
        self.BAUD_RATE = 115200

    def processLine(self, line):
        tokens = list(map(float, line.split(',')))

        self.orientation = [tokens[0], tokens[1], tokens[2], tokens[3]]
        self.accelerations = [tokens[4], tokens[5], tokens[6]]

    def display(self, t):
        for i in range(t):
            p.stepSimulation()
            time.sleep(1./240.)