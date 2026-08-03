import pygame
import time
from src.enums import SceneName
from src.models import Scene
from src.parsing import GameConfig
from src.render import Renderer
from src.scenes.game import GameScene
from src.scenes.main_menu import MainMenuScene
from src.scenes.option import OptionsScene
from src.scenes.score_board import ScoreboardScene
from src.scenes.score_entry import ScoreEntryScene


class MainGame:
    def __init__(self, game_config: GameConfig) -> None:
        print("initialize MainGame")

        self.renderer: Renderer = Renderer()

        self.scenes: dict[SceneName, Scene] = {
            SceneName.MAIN_MENU: MainMenuScene(),
            SceneName.GAME: GameScene(),
            SceneName.SCORE_ENTRY: ScoreEntryScene(),
            SceneName.SCOREBOARD: ScoreboardScene(game_config.heighscores),
            SceneName.OPTIONS: OptionsScene(),
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

            scene: Scene = self.scenes[self.current_scene]

            scene_arguments = scene.handle_events(events)
            next_scene: SceneName | None = scene_arguments.get("next_scene")

            if next_scene:
                self.current_scene = next_scene
                scene = self.scenes[next_scene]
                scene.get_scene_arguments(scene_arguments)

            self.renderer.clear()
            scene.render_scene(self.renderer)
            # self.renderer.draw_debug()

            self.renderer.update_window()
            time.sleep(0.001)
