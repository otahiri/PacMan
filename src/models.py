import pygame
from abc import ABC, abstractmethod
from src.enums import SceneName
from src.render import Renderer


class Button:

    def __init__(self, name: str, pos: tuple[int, int], scale: tuple[int, int]) -> None:
        self.name = name
        x, y = pos

        self.idel, self.hover, size = Renderer.get_button(scale)

        self.width, self.height = size

        self.pos = (x - self.width // 2, y - self.height // 2)

        self.text = Text(name, pos, "black")

    def is_collide(self, pos: tuple[int, int]):
        my_x, my_y = self.pos
        target_x, target_y = pos
        is_inside_x = my_x <= target_x <= (my_x + self.width)
        is_inside_y = my_y <= target_y <= (my_y + self.height)
        return is_inside_x and is_inside_y


class Text:

    def __init__(self, text: str, pos: tuple[int, int], color: str) -> None:

        self.text = text
        self.surf, size = Renderer.get_text(text, (5, 5), color)
        self.width, self.height = size

        self.x, self.y = pos

    def get_pos(self, anchor: str = "center") -> tuple[int, int]:
        match anchor.lower():
            # Left anchors
            case "centerleft" | "leftcenter":
                return (self.x, self.y - self.height // 2)
            case "bottomleft" | "buttomleft":  # includes your typo safeguard
                return (self.x, self.y - self.height)

            # Center anchors
            case "topcenter" | "centertop":
                return (self.x - self.width // 2, self.y)
            case "center":
                return (self.x - self.width // 2, self.y - self.height // 2)
            case "bottomcenter" | "centerbottom" | "buttomcenter":
                return (self.x - self.width // 2, self.y - self.height)

            # Right anchors
            case "topright":
                return (self.x - self.width, self.y)
            case "centerright" | "rightcenter":
                return (self.x - self.width, self.y - self.height // 2)
            case "bottomright" | "buttomright":
                return (self.x - self.width, self.y - self.height)

            # Fallback default
            case _:
                return (self.x, self.y)


class Scene(ABC):

    @abstractmethod
    def render_scene(self, renderer: Renderer) -> None: ...

    @abstractmethod
    def handle_events(
        self, events: list[pygame.Event]
    ) -> None | SceneName: ...


class Character(ABC):
    @abstractmethod
    def  __init__(self) -> None:
        ...
    @abstractmethod
    def get_sprite(self, frame: int) -> pygame.Surface: ...
