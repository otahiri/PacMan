"""High level game loop and scene navigation.

This module implements `MainGame` which manages the renderer, scene
stack and top-level game loop used by the application.
"""

from typing import Any
import pygame
from src.enums import SceneName
from src.models import Scene
from src.parsing import GameConfig
from src.render import Renderer
from src.scenes.game import GameScene
from src.scenes.info import InfoScene
from src.scenes.main_menu import MainMenuScene
from src.scenes.score_board import ScoreboardScene
from src.scenes.score_entry import ScoreEntryScene


class MainGame:
    """Top-level controller for the game.

    The class manages the active scene stack, high-score data and the main
    event loop used to render each screen.

    Args:
        game_config: Parsed configuration containing the selected color
                scheme, score file path and game mode.
    Attributes:
        game_config: Parsed configuration.
        scores: Sorted dictionary of top scores.
        renderer: Global renderer used for all scenes.
        scene_stack: Stack of active scenes.
    """

    def __init__(self, game_config: GameConfig) -> None:
        self.game_config = game_config
        self.scores: dict[str, int] = self.__get_sort_scores(
            game_config.highscores
        )
        self.renderer: Renderer = Renderer(game_config.color_scheme)
        self.scene_stack: list[Scene] = [MainMenuScene()]

    def __get_sort_scores(self, scores: dict[str, int]) -> dict[str, int]:
        """Get the top 10 scores sorted in descending order.

        Args:
            scores: Dictionary of player names to score values.

        Returns:
            A new dictionary containing at most the top 10 scores, ordered by
            highest score first.
        """

        return {
            k: v
            for k, v in sorted(
                scores.items(),
                key=lambda x: x[1],
                reverse=True,
            )[:10]
        }

    def __update_score(self, new_record: tuple[str, int]) -> None:
        """Insert or update a score entry if it is better than the current one.

        Args:
            new_record: Tuple containing the player name and score value.
        """
        scores = self.scores
        name, score = new_record

        old_score = scores.get(name)

        if old_score and score <= old_score:
            return

        scores[name] = score

        self.scores = self.__get_sort_scores(scores)

    def __navigate(self, arguments: dict[str, Any]) -> None:
        """Handle scene transitions and related navigation actions.

        Args:
            arguments: Dictionary potentially containing keys like
                `next_scene`, `new_record`, `pop`, and `score` used to
                control scene stack behavior.
        """
        next_scene: SceneName | None = arguments.get("next_scene")
        new_record: tuple[str, int] | None = arguments.get("new_record")
        last_score: int = arguments.get("score", 0)

        if new_record:
            self.__update_score(new_record)

        if arguments.get("pop"):
            self.scene_stack.pop()
            menu_scene = self.scene_stack[-1]

            # reset animated bar pos when returning to main menu
            if isinstance(menu_scene, MainMenuScene) and not next_scene:
                menu_scene.animated_bar.reset_pos()

        match next_scene:
            case SceneName.GAME:
                self.scene_stack.append(GameScene(self.game_config))

            case SceneName.SCOREBOARD:
                self.scene_stack.append(ScoreboardScene(self.scores))

            case SceneName.SCORE_ENTRY:
                self.scene_stack.append(
                    ScoreEntryScene(
                        self.game_config.highscores_path, last_score
                    )
                )
            case SceneName.INFO:
                self.scene_stack.append(InfoScene())

    def game_loop(self) -> None:
        """Run the main loop until the user quits.

        The method processes events, routes scene updates, clears the display,
        renders the current scene and refreshes the window.
        """
        running = True
        while running:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    running = False
            scene = self.scene_stack[-1]

            scene_arguments = scene.handle_events(events)
            self.__navigate(scene_arguments)
            self.renderer.clear()
            scene.render_scene(self.renderer)
            pygame.display.flip()
