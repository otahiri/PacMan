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
        self.scores: dict[str, str] = {}
        self.game_config = game_config
        self.__set_scores(game_config.heighscores)

        self.renderer: Renderer = Renderer()

        self.scenes: dict[SceneName, Scene] = {
            SceneName.MAIN_MENU: MainMenuScene(),
            SceneName.GAME: GameScene(self.game_config),
            SceneName.SCORE_ENTRY: ScoreEntryScene(
                game_config.heighscores_path
            ),
            SceneName.SCOREBOARD: ScoreboardScene(),
            SceneName.OPTIONS: OptionsScene(),
        }
        self.current_scene: SceneName = SceneName.MAIN_MENU

    def __set_scores(self, scores: dict[str, str]):
        self.scores = {
            k: v
            for k, v in sorted(
                scores.items(),
                key=lambda x: int(x[1]),
                reverse=True,
            )[:10]
        }

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

            new_score: dict[str, str] | None = scene_arguments.get("new_score")

            if new_score:
                self.scores.update(new_score)
                self.__set_scores(self.scores)

            if next_scene:
                self.current_scene = next_scene
                scene = self.scenes[next_scene]

                if next_scene == SceneName.SCOREBOARD:
                    scene.get_scene_arguments({"scores": self.scores})

                elif next_scene == SceneName.SCORE_ENTRY:
                    scene.get_scene_arguments(
                        {"scores_path": self.game_config.heighscores_path}
                    )

                scene.get_scene_arguments(scene_arguments)

            self.renderer.clear()
            scene.render_scene(self.renderer)
            self.renderer.draw_debug()

            self.renderer.update_window()
            time.sleep(0.001)
