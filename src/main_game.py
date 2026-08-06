from typing import Any
import pygame
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
        self.scores: dict[str, int] = {
            k: v
            for k, v in sorted(
                game_config.heighscores.items(),
                key=lambda x: x[1],
                reverse=True,
            )[:10]
        }
        self.game_config = game_config
        self.renderer: Renderer = Renderer()
        self.scene_stack: list[Scene] = [MainMenuScene()]

    def __update_score(self, new_recorder: tuple[str, int]):
        scores = self.scores
        name, score = new_recorder

        old_score = scores.get(name)

        if old_score and score <= old_score:
            return

        scores[name] = score

        self.scores = {
            k: v
            for k, v in sorted(
                scores.items(),
                key=lambda x: x[1],
                reverse=True,
            )[:10]
        }

    def __navigate(self, arguments: dict[str, Any]):
        next_scene: SceneName | None = arguments.get("next_scene")
        new_recorder: tuple[str, int] | None = arguments.get("new_recorder")
        last_score: int = arguments.get("score", 0)

        if new_recorder:
            self.__update_score(new_recorder)

        if arguments.get("pop"):
            print("pop:", self.scene_stack[-1])
            self.scene_stack.pop()

        match next_scene:
            case SceneName.GAME:
                self.scene_stack.append(GameScene())
                print("insert:", self.scene_stack[-1])

            case SceneName.SCOREBOARD:
                self.scene_stack.append(ScoreboardScene(self.scores))
                print("insert:", self.scene_stack[-1])

            case SceneName.SCORE_ENTRY:
                self.scene_stack.append(
                    ScoreEntryScene(
                        self.game_config.heighscores_path, last_score
                    )
                )
                print("insert:", self.scene_stack[-1])

            case SceneName.OPTIONS:
                self.scene_stack.append(OptionsScene())
                print("insert:", self.scene_stack[-1])

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

            scene = self.scene_stack[-1]

            scene_arguments = scene.handle_events(events)
            self.__navigate(scene_arguments)
            self.renderer.clear()
            scene.render_scene(self.renderer)
            # self.renderer.draw_debug()

            self.renderer.update_window()
