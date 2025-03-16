import numpy as np

from src.model.robot import RobotArm


class Scene:
    """
    Holds anything in the scene

    Currently just holds the robot, but will eventually expand to hold obstacles or objects of note
    """
    def __init__(self, robot_arm: RobotArm, robot_pose: np.ndarray | None = None):
        """
        Create a new Scene with the given robot

        Args:
            robot_arm: the RobotArm this scene is centered around
            robot_pose: 4x4 ndarray, the pose of the robot in world frame, or None to align robot and world frame
        """
        raise NotImplementedError

    @property
    def robot_arm(self) -> RobotArm:
        """
        Returns:
            the RobotArm this scene is centered around
        """
        raise NotImplementedError
