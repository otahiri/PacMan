**Focus:** Initializing the workspace, setting up the game engine, and building the underlying map logic.
*   **Environment:** Set up project dependencies (`pyproject`, `Makefile`) and transitioned the core engine to `pygame-ce`.
*   **Map Logic:** Implemented the maze generator module and developed a custom bitwise rendering system for the map walls.
*   **Architecture:** Built the core `Screen` class and implemented a Scene Management system (Main Menu, Game Scene) to handle state transitions and user events.



**Focus:** Bringing the game to life with entities, movement logic, and core game loops.
*   **Player Mechanics:** Separated player logic, added grid-based movement with animations, and integrated player death/lives logic with visual hearts.
*   **Ghost AI:** Introduced enemy ghosts (including Pinky), implemented pathfinding, and resolved critical bugs where ghosts became stuck in infinite loops.
*   **Game Loop:** Completed the gum consumption logic, score tracking, and custom rendering utilities (blit and fill) for smoother screen updates.



**Focus:** Polishing the user experience, adding advanced game states, and building data persistence.
*   **Game States:** Added global timers, Frightened Mode for ghosts, and improved death/respawn animations.
*   **Data Handling:** Built a JSON parser to handle game settings and validate files, including support for comments.
*   **User Interface:** Created an interactive Scoreboard scene with custom cursor navigation, keyboard input support, and automatic score saving.



**Focus:** Refactoring the visual rendering system, fixing sprite artifacts, and finalizing game features after a development break.
*   **Visual Refactoring:** Removed the buggy dynamic scaling system, switched the global color logic to support color schemes, and fixed transparent mask issues on rotated sprites.
*   **UI Enhancements:** Added dynamic animated bars, a Title bar, a functional Pause screen, and an Info scene.
*   **System Upgrades:** Implemented a level progression system and finalized the overarching game timer.
