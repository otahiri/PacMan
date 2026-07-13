import pygame
from mazegenerator.mazegenerator import MazeGenerator


def draw_cell(maze: list[list[int]], screen: pygame.Surface):
    y = 0
    white = (
        255,
        255,
        255,
    )
    cord_y = 10
    for row in maze:
        x = 0
        cord_x = 10
        for cell in row:
            pygame.draw.line(screen, white, (cord_x, cord_y), (cord_x + 10, cord_y), 1) if 1 & cell else None
            pygame.draw.line( screen, white, (cord_x + 10, cord_y), (cord_x + 10, cord_y + 10), 1) if 2 & cell else None
            pygame.draw.line( screen, white, (cord_x, cord_y + 10), (cord_x + 10, cord_y + 10), 1)  if 4 & cell else None

            pygame.draw.line(screen, white, (cord_x, cord_y), (cord_x, cord_y + 10), 1) if 8 & cell else None
            x += 1
            cord_x += 10
            
        y += 1
        cord_y += 10

    pass


def main():
    maze = MazeGenerator()
    maze.generate()
    for row in maze.maze:
        print([bin(i) for i in row])
    print(maze)
    pygame.init()
    screen = pygame.display.set_mode((400, 500))
    running = True
    while running:
        draw_cell(maze.maze, screen)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False


if __name__ == "__main__":
    main()
