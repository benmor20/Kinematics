import copy
from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class ArmSectionDescription:
    """
    All the information needed to construct a single section of an arm.

    Uses a cylindrical model for each section. Assumes that the section can handle any given torque
    """
    # The radius of the cylindrical section (m)
    radius: float
    # The length of the cylindrical section (m)
    length: float
    # The minimum angle the section can rotate to (rad), or None for no limit
    theta_min: float | None = None
    # The maximum angle the section can rotate to (rad), or None for no limit
    theta_max: float | None = None


class InvalidJointsError(ValueError):
    """
    Raised if a RobotArm receives a set of joints that violate limits
    """
    pass


class IKFailure(RuntimeError):
    """
    Raised if a RobotArm is asked to perform inverse kinematics to a pose it cannot reach
    """
    pass


class RobotArm:
    """
    A description of a robot arm and any information relating to its current state

    The RobotArm is modelled as a set of cylinders connected at a point along the circumference. The connection point is
    along the x-axis at the far end of the cylinder, and the joint rotates around that same axis. The first cylinder
    points along the global z-axis.
    """
    def __init__(self, arm_sections: list[ArmSectionDescription]):
        """
        Create a new RobotArm with the given description of each of its arm sections

        Defaults the starting joint angles to be the middle of the range for each section

        Args:
            arm_sections: description of each section of the arm in order
        """
        self._arm_sections = [copy.deepcopy(sec) for sec in arm_sections]
        self._joints = np.array(
            [
                (sec.theta_min + sec.theta_max) / 2
                if sec.theta_min is not None and sec.theta_max is not None
                else 0
                for sec in self._arm_sections
            ]
        )

    @property
    def num_sections(self) -> int:
        """
        Returns:
            the number of sections this robot arm has
        """
        return len(self._arm_sections)

    @property
    def joints(self) -> np.ndarray:
        """
        Returns:
            N-vector (N = self.num_sections) giving the current position of the joints
        """
        return self._joints.copy()

    @property
    def arm_sections(self) -> list[ArmSectionDescription]:
        """
        Returns:
            Descriptions of each arm section, in order
        """
        return [copy.deepcopy(sec) for sec in self._arm_sections]

    def set_joints(self, new_joints: np.ndarray) -> None:
        """
        Set the current joint positions to the given joints

        Args:
            new_joints: N-vector (N = self.num_sections) giving the target positions of all the joints

        Raises:
            InvalidJointsError: if the input is the wrong shape or if any of the given joints violate joint limits for
                their section
        """
        if new_joints.ndim != 1:
            raise InvalidJointsError(f"Given joints must be 1D - shape is {new_joints.shape}")
        if new_joints.shape[0] != self.num_sections:
            raise InvalidJointsError(f"Expected {self.num_sections} joint positions, got {new_joints.shape[0]}")
        for idx, (angle, sec) in enumerate(zip(new_joints, self._arm_sections)):
            if sec.theta_min is not None and angle < sec.theta_min:
                raise InvalidJointsError(
                    f"Joint {idx} violates minimum angle of {sec.theta_min:.5f} (received {angle:.5f})"
                )
            if sec.theta_max is not None and angle > sec.theta_max:
                raise InvalidJointsError(
                    f"Joint {idx} violates maximum angle of {sec.theta_max:.5f} (received {angle:.5f})"
                )

        self._joints = new_joints

    def get_tip_pose(self) -> np.ndarray:
        """
        Returns:
            4x4 matrix giving the pose of the end of this robot arm in robot frame
        """
        raise NotImplementedError

    def get_tip_position(self) -> np.ndarray:
        """
        Returns:
            3-element vector giving the position of the end of this robot arm in robot frame
        """
        raise NotImplementedError

    def get_joints_from_pose(self, target_pose: np.ndarray) -> np.ndarray:
        """
        Perform inverse kinematics to determine the joints that result in the tip of this arm ending in the given pose

        Args:
            target_pose: 4x4 ndarray giving the target pose in robot frame for the IK problem

        Returns:
            N-vector (N=self.num_sections) giving the joints the robot would need to be at for the tip to reach the
            given pose

        Raises:
            IKFailure: if the robot cannot reach the given pose
        """
        raise NotImplementedError

    def set_tip_pose(self, target_pose: np.ndarray) -> None:
        """
        Perform inverse kinematics to determine the joints that result in the tip of this arm ending in the given pose,
        and set the joints to match

        Args:
            target_pose: 4x4 ndarray giving the target pose in robot frame for tip to end up at

        Raises:
            IKFailure: if the robot cannot reach the given pose
        """
        raise NotImplementedError
