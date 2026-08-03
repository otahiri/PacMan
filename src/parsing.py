import sys
from pathlib import Path
from typing import Annotated, Literal
from pydantic import (
    BaseModel,
    ConfigDict,
    PositiveInt,
    StringConstraints,
    ValidationError,
    field_validator,
    model_validator,
)
import json

from pydantic_core import PydanticCustomError

ScoreName = Annotated[
    str,
    StringConstraints(strip_whitespace=True, min_length=3, max_length=10),
]


class GameConfig(BaseModel):

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)
    heighscores: dict[ScoreName, str] = {}
    heighscores_path: Path

    mode: Literal["normal", "hardcore", "cheat"] = "normal"
    points_per_pacgum: PositiveInt = 10
    points_per_ghost: PositiveInt = 200
    points_per_super_pacgum: PositiveInt = 100
    seed: PositiveInt | None = None
    levels_number: PositiveInt = 10

    @field_validator("heighscores_path", mode="before")
    @classmethod
    def validate_scores_path(cls, value: str) -> str:
        if not isinstance(value, str):
            raise PydanticCustomError(
                "invalid_type",
                "'heighscores_path' must be a valid file path",
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
        file = self.heighscores_path
        try:
            scores_data = json.loads(Parser.get_file_content(file))
            if not isinstance(scores_data, dict):
                raise PydanticCustomError(
                    "invalid_json_root",
                    "json root in '{filepath}' must be an object",
                    {"filepath": str(file)},
                )
            scores = {}

            for name, score in scores_data.items():
                if not isinstance(score, int) or score <= 0:
                    raise PydanticCustomError(
                        "invalid_score_type",
                        "score value must be a positive integer, for '{player}' got '{val}'",
                        {"player": name, "val": score},
                    )
                scores.update({name.lower(): str(score)})
            self.heighscores = scores
            return self

        except OSError:
            raise PydanticCustomError(
                "permission_denied",
                "Permission denied when reading file '{path}'",
                {"path": str(file)},
            )


class Parser:

    @staticmethod
    def get_file_path():
        if len(sys.argv) != 2:
            raise ValueError(
                "Invalid number of arguments. "
                "Usage: python main.py <config.json>"
            )

        return Path(sys.argv[1])

    @staticmethod
    def get_file_content(file):
        content = ""
        with open(file) as f:
            for line in f:
                if "#" in line:
                    line = line[0 : line.index("#")]
                if "//" in line:
                    line = line[0 : line.index("//")]
                content += line

        return content

    @staticmethod
    def parse():
        current_file = Path()
        try:

            file = Parser.get_file_path()
            current_file = file
            if file.suffix != ".json":
                raise ValueError(
                    f"Invalid config file extension '{file}'. Must be .json"
                )
            file_conent = Parser.get_file_content(file)

            game_config = GameConfig.model_validate_json(file_conent)
            print(game_config)
            return game_config

        except ValidationError as e:
            print("File:", current_file.absolute())
            for error in e.errors():
                loc = (
                    " -> ".join(str(l) for l in error["loc"])
                    if error["loc"]
                    else "Config"
                )
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
