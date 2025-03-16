from abc import ABC, abstractmethod

from src.model.scene import Scene


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
        raise NotImplementedError

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
    def draw(self) -> None:
        """
        Update the meshcat scene with the state of the internal scene
        """
        raise NotImplementedError
