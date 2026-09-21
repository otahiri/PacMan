"""Configuration parsing utilities and Pydantic models.

This module provides `GameConfig` for validating game configuration JSON
and the `Parser` helper for loading and pre-processing the configuration
file passed on the command line.
"""

import sys
import json
from pathlib import Path
from typing import Any
from pydantic_core import PydanticCustomError
from pydantic import (
    BaseModel,
    ValidationError,
    field_validator,
    model_validator,
)


class GameConfig(BaseModel):
    """Validated game configuration loaded from a JSON file.

    Attributes:
        highscores: Dictionary of player names to high-score values.
        highscores_path: Path to the high-score JSON file.
        color_scheme: Selected color palette index.
        mode: Gameplay mode.
    """

    highscores: dict[str, int] = {}
    highscores_path: Path = Path("highscores.json")
    color_scheme: int = 0
    mode: str = "normal"

    @staticmethod
    def field_status_log(field: str, value: Any, is_provided: bool):
        """Log whether a field came from the config file or a default.

        Args:
            field: Name of the configuration field.
            value: Value being used for the field.
            is_provided: Whether the field was explicitly set by the user.
        """
        if is_provided:
            print(
                f"[Config] '{field}' was provided: '{value}'", file=sys.stderr
            )
        else:
            print(
                f"[Config] '{field}' was not provided; "
                f"using default value: '{value}'",
                file=sys.stderr,
            )

    @staticmethod
    def valid_field_log(field: str, value: Any):
        """Log a successfully validated field.

        Args:
            field: Name of the configuration field.
            value: Accepted value for the field.
        """
        print(f"[Config] '{field}' accepted value: '{value}'", file=sys.stderr)

    @staticmethod
    def invalid_field_log(field: str, value: Any, default: Any):
        """Log a rejected field and the fallback value applied.

        Args:
            field: Name of the configuration field.
            value: Invalid value supplied by the user.
            default: Replacement value used after validation fails.
        """
        print(
            f"[Config] '{field}' rejected value '{value}'; "
            f"using default value: '{default}'",
            file=sys.stderr,
        )

    @model_validator(mode="before")
    @classmethod
    def log_field_sources(cls, data: Any) -> Any:
        """Log whether each known field was provided or defaulted.

        Args:
            data: Raw configuration passed.

        Returns:
            The original data object unchanged.
        """
        if not isinstance(data, dict):
            return data

        defaults = {
            "highscores_path": "highscores.json",
            "color_scheme": 0,
            "mode": "normal",
        }

        for field, default in defaults.items():
            if field in data:
                cls.field_status_log(field, data[field], True)
            else:
                cls.field_status_log(field, default, False)

        return data

    @field_validator("highscores_path", mode="before")
    @classmethod
    def validate_highscores_path(cls, value: Any) -> str:
        """Validate that the configured score
        file exists and uses a JSON suffix.

        Args:
            value: File path provided in the configuration.

        Returns:
            The validated path string.
        """

        if not isinstance(value, str):
            GameConfig.invalid_field_log(
                "highscores_path", value, "highscores.json"
            )
            return "highscores.json"

        file = Path(value)

        if file.suffix != ".json":
            GameConfig.invalid_field_log(
                "highscores_path", value, "highscores.json"
            )
            return "highscores.json"

        return str(file)

    @field_validator("color_scheme", mode="before")
    @classmethod
    def validate_color_scheme(cls, value: Any) -> int:
        """Validate the selected color scheme index.

        Args:
            value: Raw value from the config file.

        Returns:
            The validated integer color scheme value.
        """
        try:
            number = int(value)
        except Exception:
            GameConfig.invalid_field_log("color_scheme", value, 0)
            return 0

        if number < 0 or number > 6:
            GameConfig.invalid_field_log("color_scheme", number, 0)
            return 0

        GameConfig.valid_field_log("color_scheme", value)
        return number

    @field_validator("mode", mode="before")
    @classmethod
    def validate_mode(cls, value: Any) -> str:
        """Validate the selected gameplay mode.

        Args:
            value: Raw value from the config file.

        Returns:
            The validated game mode string.
        """
        if not isinstance(value, str):
            GameConfig.invalid_field_log("mode", value, "normal")
            return "normal"

        if value not in ["normal", "hardcore", "cheat"]:
            GameConfig.invalid_field_log("mode", value, "normal")
            return "normal"

        GameConfig.valid_field_log("mode", value)
        return value

    @model_validator(mode="after")
    def load_scores_from_path(self) -> "GameConfig":
        """Load and validate the score
        dictionary from the configured JSON file.

        Returns:
            The validated GameConfig` instance with `highscores`.

        Raises:
            PydanticCustomError: If the JSON root is invalid, the leaderboard
                contains invalid scores, or the file cannot be read.
        """
        file = self.highscores_path
        try:
            if not file.is_file():
                print(
                    f"[Highscore] 'highscores_path' file was missing; "
                    f"creating empty leaderboard at: {file}",
                    file=sys.stderr,
                )
                file.write_text("{}")
                return self
            else:
                print(
                    "[Highscore] loading highscores from"
                    f" existing file: {file}",
                    file=sys.stderr,
                )
            scores_data: Any = json.loads(Parser.get_file_content(file))
            if not isinstance(scores_data, dict):
                raise PydanticCustomError(
                    "highscore_error",
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
                        "highscore_error",
                        "Score's value must be a non negative integer, "
                        "for '{player}' got '{val}'",
                        {"player": name, "val": score},
                    )
                if len(name) == 0 or len(name) > 10:
                    raise PydanticCustomError(
                        "highscore_error",
                        "Player's name must be at least 1 and at most 10"
                        " characters, got '{player}'",
                        {"player": name},
                    )

                for c in name:
                    if c.isupper() or (not c == " " and not c.isalnum()):
                        raise PydanticCustomError(
                            "highscore_error",
                            "Player's name must be a lowercase alphanumeric,"
                            " got '{player}'",
                            {"player": name},
                        )
                scores.update({name: score})
            self.highscores = scores
            return self

        except OSError as e:
            raise PydanticCustomError(
                "highscore_error",
                "{os_error} when reading file '{path}'",
                {"os_error": e.strerror, "path": str(file)},
            )


class Parser:
    """Utility class for reading and validating configuration file."""

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

        try:
            file = Parser.get_file_path()
            if file.suffix != ".json":
                raise ValueError(
                    f"Invalid config file extension '{file}'. Must be .json"
                )

            if not file.is_file():
                print(
                    f"[Create configuration] The file '{file}' "
                    "does not exist. Initializing empty configuration.",
                    file=sys.stderr,
                )
                file.write_text("{}")

            else:
                print(
                    "[Load configuration] Configuration file"
                    f" '{file}' already exists.",
                    file=sys.stderr,
                )
            try:
                file_content = Parser.get_file_content(file)
            except OSError as e:
                print(
                    f"[Config] {e.strerror} when reading file '{file}'",
                    file=sys.stderr,
                )
                sys.exit(1)

            game_config = GameConfig.model_validate_json(file_content)

            return game_config

        except ValidationError as e:
            for error in e.errors():
                title = (
                    "Highscore"
                    if error["type"] == "highscore_error"
                    else "Config"
                )
                msg = error["msg"]
                print(f"[{title}] {msg}", file=sys.stderr)
            sys.exit(1)

        except ValueError as e:
            print("[Error]", e, file=sys.stderr)
            sys.exit(1)
