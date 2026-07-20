import pygame
from src.enums import SceneName
from src.models import Scene
from src.scenes.game import GameScene
from src.scenes.main_menu import MainMenuScene
from src.scenes.score_board import ScoreboardScene
from src.scenes.score_entry import ScoreEntryScene


class Screen:
    def __init__(self) -> None:
        print("initialize Screen")
        self.height = 1280
        self.width = 1280
        self.screen: pygame.Surface = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()
        self.scenes: dict[SceneName, Scene] = {
            SceneName.MAIN_MENU: MainMenuScene(),
            SceneName.GAME: GameScene(self.width, self.height, self.screen),
            SceneName.SCORE_ENTRY: ScoreEntryScene(),
            SceneName.SCOREBOARD: ScoreboardScene(),
        }
        self.current_scene: SceneName = SceneName.MAIN_MENU

    def game_loop(self) -> None:

        running = True
        while running:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        running = False

            scene = self.scenes[self.current_scene]
            next_scene = scene.handle_events(events)
            print(scene.__class__.__name__)

            if next_scene:
                self.current_scene = next_scene
                scene = self.scenes[next_scene]

            self.screen.fill("black")
            scene.render_scene(self.screen)

            self.clock.tick(60)
            pygame.display.flip()
