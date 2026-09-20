# Project Management and Peer Collaboration

The project was managed as a peer-to-peer collaboration rather than a strict manager/worker hierarchy. It workflow was intentionally lightweight but organized enough to keep a medium-size Python game moving without losing track of responsibilities, review, and bug fixing.

## 1. Project structure and tracking

We used a small project-management setup to keep work visible:

- A Trello board was used to track the backlog and feature work.
- The project-management folder contains the project notes and commit history.
- Git commit messages show how tasks were split into small, readable units, such as `feat`, `fix`, `ref`, `doc`, and `wip`.

This created a practical rhythm: the next task was visible, the current change was isolated, and we could review progress without a heavy formal process.


## 2. Workflow used during development

The typical workflow looked like this:

1. Define a task or feature in the Trello board.
2. Implement the change locally with a focused commit.
3. Run validation checks (`make lint`, runtime tests, and manual gameplay verification).
4. Merge or integrate the work when it was stable.
5. Resolve conflicts collaboratively when we both had edited the same logic.

The project history shows several examples of this pattern
## 3. Role split and shared ownership

- `satifi` appears strongly involved in refactoring, scene logic, menu flow, scoring, and project-level polish.
- `otahiri-` appears strongly involved in rendering fixes, sprite corrections, docs, bug fixes, and maze/gameplay stabilization.

This division was not absolute. We both worked across many parts of the project, and the commit log shows alternating contributions throughout the whole timeline. This helped prevent bottlenecks and kept us aware of the full project state.

## 4. Quality and delivery process

The project was managed with a simple quality loop:

- implement a feature,
- check if it works,
- clean up bugs or edge cases,
- document the change,
- then continue to the next part of the game.

This is reflected in the commit patterns:

- `feat:` entries for new functionality,
- `fix:` entries for errors and edge cases,
- `ref:` entries for code cleanup and structure,
- `doc:` and `readme:` entries for documentation,
- `merge/fix:` entries for integration issues.
