"""
Run from here
"""
import numpy as np

from src.model.robot import ArmSectionDescription, RobotArm
from src.model.scene import Scene
from src.view.view import MeshcatView


def main():
    section0 = ArmSectionDescription(radius=0.1, length=0.1)
    section1 = ArmSectionDescription(radius=0.1, length=1.5)
    section2 = ArmSectionDescription(radius=0.08, length=1)
    section3 = ArmSectionDescription(radius=0.08, length=0.5)
    section4 = ArmSectionDescription(radius=0.05, length=0.2)
    section5 = ArmSectionDescription(radius=0.05, length=0.1)
    sections = [section0, section1, section2, section3, section4, section5]
    scene = Scene(RobotArm(sections))
    view = MeshcatView(scene)
    input("Press enter to exit.")


if __name__ == '__main__':
    main()
