import itertools
import os.path
from abc import ABC, abstractmethod

from pydrake.geometry import StartMeshcat
from pydrake.visualization import ModelVisualizer

# from pydrake.visualization import ModelVisualizer

from src.model.robot import ArmSectionDescription
from src.model.scene import Scene
from src.utils import file_utils


class View(ABC):
    """
    An abstract view to draw the current state of the scene
    """
    def __init__(self, scene: Scene):
        """
        Create a new View

        Args:
            scene: the Scene this View should follow
        """
        self._scene = scene

    @abstractmethod
    def draw(self) -> None:
        """
        Draw the current state of the scene
        """
        raise NotImplementedError


class MeshcatView(View):
    """
    Draw the scene using Meshcat
    """
    def __init__(self, scene: Scene):
        """
        Create and initialize a new MeshcatView

        Print the meshcat URL to the console, set up any needed nodes

        Args:
            scene: the Scene this View should track
        """
        super().__init__(scene)
        self._meshcat = StartMeshcat()
        self._visualizer = ModelVisualizer(meshcat=self._meshcat)
        urdf_str = MeshcatView._create_urdf(self._scene.robot_arm.arm_sections)
        print(urdf_str)
        self._visualizer.parser().AddModelsFromString(urdf_str, "urdf")

    @staticmethod
    def _create_urdf(arm_sections: list[ArmSectionDescription]) -> str:
        """
        Create a URDF string from the given arm sections

        Args:
            arm_sections: the descriptions of the arm sections of the robot to create a URDF for

        Returns:
            the URDF string of the given arm sections
        """
        urdf_folder =  file_utils.path_to_file(__file__, "urdf_templates")
        urdf_elements = []

        # Add all the links
        for section_idx, section in enumerate(arm_sections):
            urdf_elements.append(
                file_utils.format_template(
                    f"{urdf_folder}/section_urdf_template.txt",
                    section_idx=section_idx,
                    radius=section.radius,
                    length=section.length,
                )
            )

        # Add all the joints
        for idx, (parent, child) in enumerate(itertools.pairwise(arm_sections)):
            urdf_elements.append(
                file_utils.format_template(
                    f"{urdf_folder}/joint_urdf_template.txt",
                    parent_idx=idx,
                    child_idx=idx + 1,
                    parent_radius=parent.radius,
                    parent_length=parent.length,
                    child_radius=child.radius,
                    lower_lim=parent.theta_min,
                    upper_lim=parent.theta_max,
                )
            )

        return file_utils.format_template(
            f"{urdf_folder}/full_urdf_template.txt",
            links_and_joints="\n".join(urdf_elements)
        )

    def draw(self) -> None:
        """
        Update the meshcat scene with the state of the internal scene
        """
        raise NotImplementedError
