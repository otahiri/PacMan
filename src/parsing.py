"""Configuration parsing utilities and Pydantic models.

This module provides `GameConfig` for validating game configuration JSON
and the `Parser` helper for loading and pre-processing the configuration
file passed on the command line.
"""

import sys
import json
from pathlib import Path
from typing import Annotated, Any, Literal
from pydantic_core import PydanticCustomError
from pydantic import (
    BaseModel,
    ConfigDict,
    NonNegativeInt,
    StringConstraints,
    ValidationError,
    field_validator,
    model_validator,
)

ScoreName = Annotated[
    str,
    StringConstraints(strip_whitespace=True, min_length=3, max_length=10),
]


class GameConfig(BaseModel):
    """Validated game configuration loaded from a JSON file.

    Attributes:
        highscores: Dictionary of player names to high-score values.
        highscores_path: Path to the high-score JSON file.
        color_scheme: Selected color palette index.
        mode: Gameplay mode.
    """

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)
    highscores: dict[ScoreName, NonNegativeInt] = {}
    highscores_path: Path
    color_scheme: NonNegativeInt
    mode: Literal["normal", "hardcore", "cheat"] = "normal"

    @field_validator("highscores_path", mode="before")
    @classmethod
    def validate_scores_path(cls, value: str) -> str:
        """Validate that the configured score
        file exists and uses a JSON suffix.

        Args:
            value: File path provided in the configuration.

        Returns:
            The validated path string.

        Raises:
            PydanticCustomError: If the path is missing, invalid, or not JSON.
        """
        if not isinstance(value, str):
            raise PydanticCustomError(
                "invalid_type",
                "'highscores_path' must be a valid file path",
            )

        file = Path(value)

        if file.suffix != ".json":
            raise PydanticCustomError(
                "invalid_extension",
                "Invalid scores file extension for '{filepath}'."
                " Must be .json",
                {"filepath": str(file)},
            )

        if not file.is_file():
            raise PydanticCustomError(
                "file_not_found",
                "File '{filepath}' does not exist",
                {"filepath": str(file)},
            )
        return str(file)

    @model_validator(mode="after")
    def load_scores_from_path(self) -> "GameConfig":
        """Load and validate the score
        dictionary from the configured JSON file.

        Returns:
            The validated `GameConfig` instance with `highscores` populated.

        Raises:
            PydanticCustomError: If the JSON root is invalid, the leaderboard
                contains invalid scores, or the file cannot be read.
        """
        file = self.highscores_path
        try:
            scores_data: Any = json.loads(Parser.get_file_content(file))
            if not isinstance(scores_data, dict):
                raise PydanticCustomError(
                    "invalid_json_root",
                    "json root in '{filepath}' must be an object",
                    {"filepath": str(file)},
                )
            scores = {}

            for name, score in scores_data.items():
                if (
                    not isinstance(score, int)
                    or score < 0
                    or score > 2147483647
                ):
                    raise PydanticCustomError(
                        "invalid_score",
                        "score value must be a non negative integer, "
                        "for '{player}' got '{val}'",
                        {"player": name, "val": score},
                    )
                if any(c.isupper() for c in name):
                    raise PydanticCustomError(
                        "invalid_player_name",
                        "player name must be lowercase, got '{player}'",
                        {"player": name},
                    )
                scores.update({name: score})
            self.highscores = scores
            return self

        except OSError:
            raise PydanticCustomError(
                "permission_denied",
                "Permission denied when reading file '{path}'",
                {"path": str(file)},
            )


class Parser:
    """Utility class for reading and validating configuration files."""

    @staticmethod
    def get_file_path() -> Path:
        """Read the config path from command-line arguments.

        Returns:
            Path to the JSON config file.

        Raises:
            ValueError: If the command line arguments are not exactly one file.
        """
        if len(sys.argv) != 2:
            raise ValueError(
                "Invalid number of arguments. "
                "Usage: python3 pac-man.py <config.json>"
            )

        return Path(sys.argv[1])

    @staticmethod
    def get_file_content(file) -> str:
        """Return the file contents after stripping comments.

        Args:
            file: JSON configuration file to read.

        Returns:
            The cleaned configuration text without `#` or `//` comments.
        """
        content = ""
        with open(file) as f:
            for line in f:
                if "#" in line:
                    command_idx = line.index("#")
                    line = line[0:command_idx]
                if "//" in line:
                    command_idx = line.index("//")
                    line = line[0:command_idx]
                content += line

        return content

    @staticmethod
    def parse() -> GameConfig:
        """Parse and validate the game configuration
        from the command-line file.

        Returns:
            A validated `GameConfig` object containing the parsed data.
        """
        current_file = Path()
        try:
            file: Path = Parser.get_file_path()
            current_file = file
            if file.suffix != ".json":
                raise ValueError(
                    f"Invalid config file extension '{file}'. Must be .json"
                )
            file_content: str = Parser.get_file_content(file)
            game_config: GameConfig = GameConfig.model_validate_json(
                file_content
            )

            return game_config

        except ValidationError as e:
            print("File:", current_file.absolute())
            for error in e.errors():
                loc = error["loc"][0] if error["loc"] else "Config"
                msg = error["msg"]
                if msg.startswith("Value error, "):
                    msg = msg.removeprefix("Value error, ")

                print(f"[{loc}] {msg}")
            sys.exit(1)

        except OSError as e:
            print("File:", current_file.absolute())
            print(f"Error: {e.strerror}")
            sys.exit(1)
        except ValueError as e:
            print("File:", current_file.absolute())
            print("Error:", e)
            sys.exit(1)
