import pygame
from src.enums import DisplayInfo
from src.models import Button
from src.render import Renderer


class PauseMenu:
    def __init__(self) -> None:
        self.working_area: pygame.Surface = pygame.Surface(
            (DisplayInfo.SCREEN_WIDTH.value, DisplayInfo.SCREEN_HEIGHT.value),
            pygame.SRCALPHA
        )

        # self.resume_button: Button = Button("resume", Renderer.get_pos((0, 0), ()))
