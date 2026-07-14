# Contributing Guide

This document defines the coding standards, workflow, and collaboration rules for this project. The goal is to keep the codebase clean, consistent, and easy for everyone to work on.


# General Rules

* Keep functions focused.
* Remove dead code.
* Avoid duplicated logic.
* Write code that explains itself.
* Refactor when duplication appears.
* Keep commits small and meaningful.
* Readability is more important than cleverness.
* Keep solutions simple.
* Write code for developers, not just the computer.
* If something is difficult to understand, improve the implementation or document why it exists.
* Leave the codebase cleaner than you found it.
* When faced with multiple solutions, choose the one that is easiest for another developer to understand six months from now.

# Rules
* *Classes*, *functions* and *methods* should have *docstrings*.


- Formatting is handled automatically by *Black Formatter*.

- All *functions*, *methods*, *attributes* and *return types* should include type hints.

## Naming
- Use snake_case for  *files*, *variables*, *functions* and *methods*.
- Use uppercase for *Constants variables* and and *Enums variables*
- Use PascalCase for *Classes*

## Imports

Imports should be grouped.

```python
# Standard library
from pathlib import Path

# Third-party
import pygame

# Local
from game.player import Player
```

## Comments

Comment *why*, not *what*.
The code should explain what it is doing.

```python
# Prevent tunneling when the player moves quickly.
```
