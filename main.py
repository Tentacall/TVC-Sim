import pybullet as p
import pybullet_data
import serial
import time
import random
from utility.simulation import Simulation

class MainSimulation(Simulation):
    def __init__(self) -> None:
        super().__init__()
        p.setGravity(0,0,-9.81  )

        self.rocket = p.loadURDF("assets/simple_rocket.xml", self.startPos, self.orientation)
        # self.rocket = p.loadSTL("assets/rocket.stl", self.startPos, self.orientation)
        self.plane = p.loadURDF("plane.urdf")

        # Enable physics for the rocket
        p.setCollisionFilterGroupMask(self.rocket, -1, 0, 0)
        p.setCollisionFilterPair(self.rocket, self.plane, -1, -1, 1)
        p.changeDynamics(self.rocket, -1, mass=1.0)

    
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
        force = [0,0,10]
        position = [0,0,0]
        camera_target_postion = [0,0,0]
        c_distance, c_yaw, c_pitch = 3, 30, -40
        for i in range(10000):
            p.stepSimulation()
            r_pos, r_orientation = p.getBasePositionAndOrientation(self.rocket)
            # updating matrix
            noise_force = [random.uniform(-1, 1), random.uniform(-1, 1), random.uniform(-1, 1)]
            noise_position = [random.uniform(-1, 1), random.uniform(-1, 1), random.uniform(-1, 1)]
            for i in range(3):
                noise_force[i] += r_pos[i]
            p.applyExternalForce(self.rocket, -1, noise_force, r_pos, p.WORLD_FRAME)
            p.applyExternalForce(self.rocket, -1, force, r_pos, p.WORLD_FRAME)
            # p.resetBasePositionAndOrientation(self.rocket, self.startPos, self.orientation)
            # p.resetDebugVisualizerCamera(c_distance, c_yaw, c_pitch, camera_target_postion)
            position[2] += 10
            time.sleep(1./240.)
        cubePos, cubeOrn = p.getBasePositionAndOrientation(self.rocket)
        print(cubePos,cubeOrn)


if __name__ == '__main__':
    sim = MainSimulation()
    sim.updateOrientationAccel()
    # sim.start()
    p.disconnect()