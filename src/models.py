import pygame


class Button:

    def __init__(self, name: str, pos: tuple[int, int]) -> None:
        self.name = name
        font = pygame.font.Font(None, 100)
        self.text_surf = font.render(name, True, "white")
        self.text_rect = self.text_surf.get_rect(center=pos)
        self.pos = pos
        self.surf = pygame.surface.Surface((300, 100))
        self.surf.fill("red")
        self.rect = self.surf.get_rect(center=pos)

    def in_rage(self, pos: tuple[int, int]) -> bool:
        x, y = pos
        if (
            x >= self.rect.topleft[0]
            and x <= self.rect.topright[0]
            and y >= self.rect.topleft[1]
            and y <= self.rect.bottomleft[1]
        ):
            return True
        return False
