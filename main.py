import pybullet as p
import pybullet_data
import serial
import time
import logging


class Simulation():
    def __init__(self) -> None:
        self.client = p.connect(p.GUI)

        p.setGravity(0,0,-9.81  )
        p.setAdditionalSearchPath(pybullet_data.getDataPath())

        self.startPos = [0,0,.5]
        self.orientation = [0.0,0.0,0.0,1.0]
        self.accelerations = [0,0,0]

        self.rocket = p.loadURDF("assets/simple_rocket.xml", self.startPos, self.orientation)
        self.plane = p.loadURDF("plane.urdf")

        # Enable physics for the rocket
        p.setCollisionFilterGroupMask(self.rocket, -1, 0, 0)
        p.setCollisionFilterPair(self.rocket, self.plane, -1, -1, 1)
        p.changeDynamics(self.rocket, -1, mass=1.0)

        # serial connection config
        self.PORT = '/dev/ttyUSB0'
        self.BAUD_RATE = 115200


    def processLine(self, line):
        tokens = list(map(float, line.split(',')))

        self.orientation = [tokens[0], tokens[1], tokens[2], tokens[3]]
        self.accelerations = [tokens[4], tokens[5], tokens[6]]
    
    def updateOrientationAccel(self):
        ser = None
        try:
            ser = serial.Serial(self.PORT, self.BAUD_RATE)
            while True:
                line = ser.readline().decode('utf-8').strip()
                if line:
                    p.stepSimulation()
                    self.processLine(line)
                    p.resetBasePositionAndOrientation(self.rocket, self.startPos, self.orientation)
                    time.sleep(1./240.)

        except KeyboardInterrupt:
            return
        except Exception as e:
            return e
        finally:
            if ser and ser.is_open:
                ser.close()


    def start(self):
        for i in range(10000):
            p.stepSimulation()

            # updating matrix
            
            p.resetBasePositionAndOrientation(self.rocket, self.startPos, self.orientation)

            # 
            time.sleep(1./240.)
        cubePos, cubeOrn = p.getBasePositionAndOrientation(self.rocket)
        print(cubePos,cubeOrn)




if __name__ == '__main__':
    sim = Simulation()
    sim.updateOrientationAccel()
    p.disconnect()