import pybullet as p
import time
import serial
from simulation import Simulation
import math 

class GimbleSimulation(Simulation):
    '''
    Serial connected Gimble simulation
    '''

    def __init__(self) -> None:
        super().__init__()
        self.gimble = p.loadURDF("assets/newMount/urdf/allBracketsAndJoints.SLDASM/urdf/allBracketsAndJoints.SLDASM.urdf")
        # camera configuration
        p.changeDynamics(self.gimble, linkIndex=-1, mass=0) # fixing the base
        p.resetDebugVisualizerCamera(0.25,30,-40,[0,0,0])

        self.outer_joint_index = 1
        self.inner_joint_index = 2

    def getXYRotation(self):
        x, y, z, w = self.orientation
        sinp = 2.0 * (w * y - z * x)
        if abs(sinp) >= 1:
            pitch = math.copysign(math.pi / 2, sinp)  # Use 90 degrees if out of range
        else:
            pitch = math.asin(sinp)

        siny_cosp = 2.0 * (w * z + x * y)
        cosy_cosp = 1.0 - 2.0 * (y * y + z * z)
        yaw = math.atan2(siny_cosp, cosy_cosp)

        return pitch, yaw

    def simulate(self):
        ser = None
        try:
            ser = serial.Serial(self.PORT, self.BAUD_RATE)
            while True:
                line = ser.readline().decode('utf-8').strip()
                if line:
                    p.stepSimulation()
                    self.processLine(line)
                    angle_x, angle_y = self.getXYRotation()
                    print(angle_x, angle_y)
                    p.setJointMotorControl2(
                        bodyUniqueId=self.gimble,
                        jointIndex=self.inner_joint_index,
                        controlMode=p.POSITION_CONTROL,
                        targetPosition=angle_y,
                        force = 100000.0,
                        maxVelocity = 100000.0
                    )
                    p.setJointMotorControl2(
                        bodyUniqueId=self.gimble,
                        jointIndex=self.outer_joint_index,
                        controlMode=p.POSITION_CONTROL,
                        targetPosition=angle_x,
                        force = 100000.0,
                        maxVelocity = 100000.0
                    )
                    time.sleep(1./10.)

        except KeyboardInterrupt:
            return
        except Exception as e:
            return e
        finally:
            if ser and ser.is_open:
                ser.close()

        # for i in range(p.getNumJoints(self.gimble)):
        #     joint_info = p.getJointInfo(self.gimble, i)
        #     print(i, joint_info)
        
    # def display(self):
    #     angle = 0.1
    #     diff = 0.01
    #     for i in range(10000):
    #         p.setJointMotorControl2(
    #             bodyUniqueId=self.gimble,
    #             jointIndex=self.inner_joint_index,
    #             controlMode=p.POSITION_CONTROL,
    #             targetPosition=angle,
    #         )
    #         # p.setJointMotorControl2(
    #         #     bodyUniqueId=self.gimble,
    #         #     jointIndex=self.outer_joint_index,
    #         #     controlMode=p.POSITION_CONTROL,
    #         #     targetPosition=angle,
    #         # )
    #         angle += diff
    #         if angle > 0.35 or angle < -0.35:
    #             diff *= -1
            
    #         p.stepSimulation()
    #         time.sleep(1./240.)
    

if __name__ == '__main__':
    sim = GimbleSimulation()
    sim.simulate()