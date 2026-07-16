from abc import ABC, abstractmethod


class Scene(ABC):

    @abstractmethod
    def render_scene(self) -> None: ...


class MainMenuScene(Scene):
    def __init__(self) -> None:
        pass

    def render_scene(self) -> None: ...


class GameScene(Scene):
    def __init__(self) -> None:
        pass

    def render_scene(self) -> None: ...


class ScoreboardScene(Scene):
    def __init__(self) -> None:
        pass

    def render_scene(self) -> None: ...


class ScoreEntryScene(Scene):
    def __init__(self) -> None:
        pass

    def render_scene(self) -> None: ...
