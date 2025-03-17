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
        self._robot_arm = robot_arm
        self._robot_pose = robot_pose

    @property
    def robot_arm(self) -> RobotArm:
        """
        Returns:
            the RobotArm this scene is centered around
        """
        return self._robot_arm

    @property
    def robot_pose(self) -> np.ndarray:
        """
        Returns:
            4x4 ndarray, the pose of the robot in world frame
        """
        return self._robot_pose.copy()
