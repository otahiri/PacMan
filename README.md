*This project has been created as part of the 42 curriculum by otahiri- and satifi.*
# Pac-Man


## Description

This project is a faithful recreation of the classic Pac-Man gameplay experience in Python using Pygame. The goal is to reproduce the core loop of the original arcade game: navigate a maze, eat pellets to increase the score, collect super pellets to temporarily make the ghosts edible, and avoid being caught while the timer and level progression create pressure.

The game is implemented as a full graphical application with distinct scenes, animated sprites, maze generation, ghost AI, score tracking, and configurable difficulty modes. It focuses on readability, maintainability, and a gameplay loop that is close to the original while still fitting a modular Python architecture.

## Instructions

The project uses a small Makefile to simplify installation and execution.

### Installation

From the project root, run:

```bash
make install
```

This installs the project dependencies with the workspace-managed environment.

### Execution

To launch the game:

```bash
make run
```

This runs:

```bash
uv run python3 pac-man.py config.json
```

### Debugging

For debugging and stepping through the program:

```bash
make debug
```

### Quality checks

To run the configured static checks:

```bash
make lint
```

To remove generated caches and Python bytecode artifacts:

```bash
make clean
```

### Controls

- Arrow keys or WASD: move the player
- Escape: pause/unpause
- Enter: confirm a selected pause menu action
- N: in cheat mode, skip the current level

## Resources

### Reference material

- Pac-Man official game archive: https://www.pacman1.net/
- Pac-Man ghost AI behavior reference: https://pacman.fandom.com/wiki/Maze_Ghost_AI_Behaviors
- A-Maze-ing maze generation concepts and bitmask wall representation: the assignment package used in this project (`mazegenerator`)
- Pygame documentation: https://www.pygame.org/docs/
- Python typing and data validation reference: https://docs.pydantic.dev/

- the pacman game: [pacman game](https://www.pacman1.net/)
- the ghost algo: [algo](https://pacman.fandom.com/wiki/Maze_Ghost_AI_Behaviors)

### AI usage

AI was used as a support tool during the project, not as a replacement for the design or validation work. Its main contributions were:

- Explaining gameplay and architecture concepts during early design work.
- Helped with documenting the project (e.g., docstrings, README.).


## Configuration

The game configuration is stored in a JSON file, and the application expects exactly one configuration file as an argument. The default configuration file is `config.json`.

### File structure

```json
{
  "hihscores_path": "heighscore.json",
  "mode": "hardcore",
  "color_scheme": 1
}
```

### Fields

- `highscores_path`: path to the JSON file containing saved high scores. The file must exist and must end with `.json`.
- `mode`: gameplay mode. Supported values are:
  - `normal`: default mode with 3 hearts and a 120-second timer
  - `hardcore`: stricter mode with 90 seconds and no extra player safety
  - `cheat`: debug-focused mode, effectively invincible, without a countdown, and allowing level skipping with `N` key
- `color_scheme`: integer index selecting the theme palette. The project supports several predefined color schemes; out-of-range values are clamped to the nearest valid palette index.

The parser also strips comments beginning with `#` or `//`, then validates the data using Pydantic before the game starts.

## Highscore

The highscore system stores names and scores in a JSON file, and it is loaded through `GameConfig` during startup. The scores are then sorted in descending order, and only the top 10 entries are kept in the in-memory leaderboard.

This design was chosen because it is simple, persistent, and easy to extend. Each score entry is linked to a player name and a numeric value, and the leaderboard is updated when a run ends or when a new record is achieved. The implementation keeps the score data independent from the game logic so the same configuration can be reused for local testing and runtime gameplay.

The persisted file used by the project is `highscore.json`, and the current implementation validates that:

- names are lower-case strings
- scores are non-negative integers
- the file exists and uses a valid JSON format

This makes the leaderboard robust and easy to inspect, while keeping the game runtime small and predictable.

## Maze Generation

The maze generation is handled by the assigned A-Maze-ing package, represented in the project by the `mazegenerator` dependency. The package generates a logical maze as a 2D grid of integer values, where each cell stores a bitmask encoding the walls around it.

The maze is not represented as a raw visual map; instead, each integer contains directional wall information. The bit flags encode whether a wall exists in each of the directions, conceptually following the ordering used by the project for north/south/east/west-style connectivity. In practice, the code uses these bit values to determine:

- whether a player can move through a given cell
- whether a ghost can continue in a direction
- how a cell should be rendered with the correct corner/edge combination

The class `MazeInterface` in `src/maze.py` converts the generated logical maze into a grid of `Cell` objects, then renders the wall textures and corner sprites to create the final maze view. This allows the game engine to separate logic, rendering, and map traversal cleanly.

## Implementation

### Main gameplay loop

The project uses a scene-based system, where `MainGame` acts as the global controller. It maintains a stack of active scenes and handles transitions between the main menu, gameplay, score board, and score-entry screens. Each scene receives events and decides whether it should remain active or pop.

### Movement logic

The player and ghosts are represented by character classes built from a common model. Movement is based on a grid-aligned system using direction enums, visual offsets, and maze occupancy checks. The player chooses a direction, and only valid moves are applied when the character is centered in a tile. Ghosts use vector-based algorithm to move toward the player or their assigned corners.

### Maze rendering

The visual maze is rendered from the logical bitmask structure. Walls are drawn based on the presence of nearby edges, then corner sprites connect the walls to avoid visual gaps. This mirrors the classic tile-based rendering style that makes the maze feel coherent and clean.

### Game states and progression

The game logic tracks:

- the player score
- remaining time
- level progression
- ghost states (scatter, chase, frightened, dead, respawn)
- super pellet effects
- collisions and death animations

The game state transitions are centralized in `src/game_logic.py`, which coordinates the maze, player, ghosts, and UI updates.

### Assets and UI

The project uses sprite-based rendering for all characters, walls, letters, and UI elements. The `Renderer` module loads images, recolors them according to the selected palette, and generates text surfaces from pre-loaded letters sprites. This allows the game to support multiple color themes without editing the artwork itself.

## General Software Architecture

The project follows a layered design:

- `pac-man.py`: entry point; loads the configuration and starts the game
- `src/parsing.py`: configuration parsing and validation using Pydantic
- `src/main_game.py`: global game loop and scene navigation
- `src/scenes/`: scene classes for the menu, gameplay, info, scoreboard, and score entry flows
- `src/game_logic.py`: central gameplay rules, timers, collisions, and ghost state management
- `src/maze.py`: maze generation wrapper and rendering logic
- `src/mobs.py`: player and ghost classes, movement, and animation logic
- `src/models.py`: shared UI widgets and core data models
- `src/render.py`: rendering engine and sprite handling
- `src/enums.py`: fixed game constants and enumeration values

The key relationship is that `MainGame` owns the active scene stack and delegates gameplay to `GameScene`, which in turn creates and updates `GameLogic`. `GameLogic` uses `MazeInterface` and the classes from `mobs.py` to process map, movement, collision, and score events. This separation keeps the game logic independent from rendering and scene flow, making the project logic easier to understand and later on expand it.

## Project Management

The project was managed with a lightweight, task-oriented workflow: each major feature was broken down into its own implementation area, such as maze generation, player movement, ghost AI, scene flow, score handling, and configuration parsing. Progress was organized around the game architecture and verification loop: implement a feature, validate it with the project’s runtime and static checks, then move to the next module.

This kept the project manageable while preserving a clear progression from the maze foundation to the full game loop and final polish.

A dedicated project-management folder is available here:

- [project-management](project-management)
