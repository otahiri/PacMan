import pygame
from src.display import Screen

pygame.init()
screen = Screen()
screen.game_loop()

# import pygame
# import mazegenerator


# class Corner:
#     """corner object to decide the look of the corner connecting walls

#     Attributes:
#         hex: hex value for the corner representing the sides it has
#     """

#     def __init__(self) -> None:
#         """constructor of the Corner class"""
#         self.hex = 0


# class Cell:
#     """cell class that has all the attributes of the cell

#     Attributes:
#         hex_value: the hex value of the cell representing which  walls are open
#         top_left: top left corner
#         top_right: top right corner
#         bottom_left: bottom left corner
#         bottom_right: bottom right corner
#     """

#     def __init__(self, hex: int, corners: list[Corner]) -> None:
#         """constructor of the Cell class

#         Args:
#             hex: hex value of the cell
#             corners: list of corners surrounding the cell
#         """
#         self.hex_value = hex
#         self.top_left = corners[0]
#         self.top_right = corners[1]
#         self.bottom_left = corners[2]
#         self.bottom_right = corners[3]
#         self.update_corners()

#     def update_corners(self) -> None:
#         """mask the corner hex value according to the hex value of the cell
#         top left corner will have an east side if the cell has a north wall
#         and a south side if the cell has a west wall
#         top right corner will have a west side if the cell has a north wall
#         and a south side if the cell has an east wall
#         bottom right corner will have north side if the cell has an east
#         wall and a west side if the cell has a south wall
#         bottom left corner  will have a north side if the cell has a west
#         wall and an east side if the cell has a south wall
#         """
#         self.top_left.hex |= (1 & self.hex_value) << 1
#         self.top_left.hex |= (8 & self.hex_value) >> 1
#         self.top_right.hex |= (1 & self.hex_value) << 3
#         self.top_right.hex |= (2 & self.hex_value) << 1
#         self.bottom_right.hex |= (2 & self.hex_value) >> 1
#         self.bottom_right.hex |= (4 & self.hex_value) << 1
#         self.bottom_left.hex |= (4 & self.hex_value) >> 1
#         self.bottom_left.hex |= (8 & self.hex_value) >> 3


# def draw_maze(
#     maze: list[list[Cell]],
#     corner_images: dict,
#     wall_images: dict,
#     screen: pygame.Surface,
# ) -> None:
#     """rendering the map in pygame surface

#     Args:
#         maze: 2d array containing the cells
#         corner_images: images of all possible corners pre-loaded
#         wall_images: vertical and horzontal walls pre-loaded
#         screen: surface of pygame
#     """
#     cord_y = 400
#     for y in range(len(maze)):
#         cord_x = 400
#         for x in range(len(maze[0])):
#             cell = maze[y][x]
#             tl_corner = corner_images[cell.top_left.hex]
#             screen.blit(tl_corner, (cord_x, cord_y))
#             if cell.hex_value & 1:
#                 screen.blit(wall_images[0], (cord_x + 16, cord_y))
#             tr_corner = corner_images[cell.top_right.hex]
#             screen.blit(tr_corner, (cord_x + 32, cord_y))
#             if cell.hex_value & 8:
#                 screen.blit(wall_images[1], (cord_x, cord_y + 16))
#             if cell.hex_value & 2:
#                 screen.blit(wall_images[1], (cord_x + 32, cord_y + 16))
#             bl_corner = corner_images[cell.bottom_left.hex]
#             screen.blit(bl_corner, (cord_x, cord_y + 32))
#             if cell.hex_value & 4:
#                 screen.blit(wall_images[0], (cord_x + 16, cord_y + 32))
#             br_corner = corner_images[cell.bottom_right.hex]
#             screen.blit(br_corner, (cord_x + 32, cord_y + 32))
#             cord_x += 32
#         cord_y += 32


# def main() -> None:
#     """main function"""
#     pygame.init()
#     asset_path = "assets/walls/"
#     screen = pygame.display.set_mode((1400, 1400))
#     maze = mazegenerator.MazeGenerator()
#     maze.generate()
#     bit_maze = maze.maze
#     corner_images = {}
#     for i in range(16):
#         corner_images[i] = pygame.image.load(f"{asset_path}{i}.png").convert_alpha()
#     wall_images = {
#         0: pygame.image.load(f"{asset_path}horizontanl_wall.png"),
#         1: pygame.image.load(f"{asset_path}vertical_wall.png").convert_alpha(),
#     }
#     corner_grid = [
#         [Corner() for _ in range(len(bit_maze) + 1)] for _ in range(len(bit_maze) + 1)
#     ]
#     cell_grid = [
#         [
#             Cell(
#                 bit_maze[y][x],
#                 [
#                     corner_grid[y][x],
#                     corner_grid[y][x + 1],
#                     corner_grid[y + 1][x],
#                     corner_grid[y + 1][x + 1],
#                 ],
#             )
#             for x in range(len(bit_maze[0]))
#         ]
#         for y in range(len(bit_maze))
#     ]
#     running = True
#     while running:
#         draw_maze(cell_grid, corner_images, wall_images, screen)
#         pygame.display.update()
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 running = False
#             if event.type == pygame.KEYDOWN:
#                 if event.key == pygame.K_ESCAPE:
#                     running = False


# if __name__ == "__main__":
#     main()
