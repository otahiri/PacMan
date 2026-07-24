import pygame
from src.enums import DisplayInfo, SceneName
from src.models import Scene
from src.render import Renderer
from src.scenes.game import GameScene
from src.scenes.main_menu import MainMenuScene
from src.scenes.option import OptionsScene
from src.scenes.score_board import ScoreboardScene
from src.scenes.score_entry import ScoreEntryScene


class Screen:
    def __init__(self) -> None:
        print("initialize Screen")

        self.renderer: Renderer = Renderer()

        self.scenes: dict[SceneName, Scene] = {
            SceneName.MAIN_MENU: MainMenuScene(),
            SceneName.GAME: GameScene(
                DisplayInfo.SCREEN_WIDTH.value,
                DisplayInfo.SCREEN_HEIGHT.value,
                self.renderer.window,
            ),
            SceneName.SCORE_ENTRY: ScoreEntryScene(),
            SceneName.SCOREBOARD: ScoreboardScene(),
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

            scene = self.scenes[self.current_scene]
            next_scene = scene.handle_events(events)

            if next_scene:
                self.current_scene = next_scene
                scene = self.scenes[next_scene]

            self.renderer.clear()
            scene.render_scene(self.renderer)
            # self.renderer.draw_debug()

            self.renderer.update_window()
