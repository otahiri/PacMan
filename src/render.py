import pygame


class Renderer:
    def __init__(self) -> None:
        self.window = pygame.display.set_mode((1280, 1280))
        print("initialize Renderer")

    def clear(self):
        self.window.fill("black")

    @classmethod
    def get_button(cls):
        idel = pygame.image.load("assets/button/idel.png")
        hover = pygame.image.load("assets/button/hover.png")

        weight = 32
        height = 11
        return (idel, hover, weight, height)

    def render(self, source, pos):
        self.window.blit(source, pos)

    @classmethod
    def scale_surface(cls, src_image, size, new_size):
        orig_w, orig_h = size
        new_w, new_h = new_size

        scaled_surface = pygame.Surface((new_w, new_h))

        for y in range(new_h):
            for x in range(new_w):
                src_x = int(x * (orig_w / new_w))
                src_y = int(y * (orig_h / new_h))

                color = src_image.get_at((src_x, src_y))
                scaled_surface.set_at((x, y), color)

        return scaled_surface

    def update_window(self):
        pygame.display.flip()
