import pygame
from mazegenerator.mazegenerator import MazeGenerator


def draw_cell(maze: list[list[int]]):
    
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
        pygame.draw.line(screen, (0,0, 255), (0, 0), (10,10), 5)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False


if __name__ == "__main__":
    main()
