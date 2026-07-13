import pygame
from mazegenerator.mazegenerator import MazeGenerator


def draw_cell(maze: list[list[int]], screen: pygame.Surface, corner: tuple, size: tuple, thickness: int):

    """render cell on the screen

    Args:
        maze: the list of hex value representing the map walls
        (the bits go from least significant bit to the most significant
        each representing a direction in the order NESW)
        screen: the Surface object created by pygame representing the display
        corner: the cords for the top left corner of the maze
        used as an anchor for the maze
        size: the width and height of the maze
        thickness: the thickness of the lines of the maps
    """
    x_intervals = size[0] // len(maze[0])
    y_intervals = size[1] // len(maze)
    y = 0
    white = (
        255,
        255,
        255,
    )
    cord_y = corner[1]
    for row in maze:
        x = 0
        cord_x = corner[0]
        for cell in row:
            (
                pygame.draw.line(
                    screen, white, (cord_x, cord_y), (cord_x + x_intervals, cord_y), thickness
                )
                if 1 & cell
                else None
            )
            (
                pygame.draw.line(
                    screen, white, (cord_x + x_intervals, cord_y), (cord_x + x_intervals, cord_y + y_intervals), thickness
                )
                if 2 & cell
                else None
            )
            (
                pygame.draw.line(
                    screen, white, (cord_x, cord_y + y_intervals), (cord_x + x_intervals, cord_y + y_intervals), thickness
                )
                if 4 & cell
                else None
            )

            (
                pygame.draw.line(
                    screen, white, (cord_x, cord_y), (cord_x, cord_y + y_intervals), thickness
                )
                if 8 & cell
                else None
            )
            x += 1
            cord_x += y_intervals

        y += 1
        cord_y += y_intervals


def main():
    maze = MazeGenerator()
    maze.generate()
    for row in maze.maze:
        print([bin(i) for i in row])
    print(maze)
    pygame.init()
    screen = pygame.display.set_mode((1400, 1400))
    running = True
    while running:
        draw_cell(maze.maze, screen, (200, 200), (500, 500), 5)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False


if __name__ == "__main__":
    main()
