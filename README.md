*This project has been created as part of the 42 curriculum by otahiri- satifi*

*Description:
    this project is a try to remake the original game pacman as accurately as possible.
    the pacman (the character the player controls) is a circle with a mouth that goes around a maze,
    eating gums to gain points and super powers (mainly the ability to eat ghosts),
    if the pacman touches a ghost without the super gum ability the pacman dies.
    
*Instructions:
    to run the project you must first install the dependancies with the command
    ``bash
        make install
    ``
    and then run the command 
    ``bash
        make run
    ``
    to run the linter you must run the command
    ``bash
        make lint
    ``
    to clean the cache files you must run the command:
    ``bash
        make clean
    ``
    to run the program in debug mode you must use the the command:
    ``bash
        make debug
    ``
    while in the game you must use the arrow keys to control the player to avoid ghosts and collect the gums

*Resources:
    the pacman game: [pacman game](https://www.pacman1.net/)
    the ghost algo: [algo](https://pacman.fandom.com/wiki/Maze_Ghost_AI_Behaviors)

*Configuration:
    heighscores_path:
        the file to save the high scores, must be json file
    mode:
        the mode of the game:
            normal: the default one with 3 hearts and 120 seconds of time limit
            hardcore: hard difficulty you must not get hit ever, time limit is 90 seconds, only for the elite players
            cheat: for testing mainly, invincible player so the ghosts cannot kill you, no time limit, you can skip levels by tapping n
    color_schema:
        the index of the color pallet from 0 to 4 values less than 0 are not accepted, if the value is greater than 4 the default pallet will be used instead which is black and white


*Highscore:
    ["ToDo!!!"]

*Maze Generation:
    the provided mazegenerator model was used to make the logical maze,
    which is a list inside a list containing the hex value for each cell,
    each bit of that value represent a wall 1 means wall exist 0 means wall does not exist,
    each bit represent a direction WSEN from most significant to least significant bit.

*Implementation:

    maze rendering: the idea behind the maze rendering follow the same concept as amazeing project, first rending walls depending on the bit maze,
    then depending to existance of the wall the corners are chosens to link between the walls so the rendering is flawless.

    assets: the assets were made by hand using librsprite application aka asprite, it is the industry standard for pixel art drawing.

    player movements: the player movements was also the based on the logic behind the player logic in amazeing project,
    input movements will be translated to the appropriate direction enum,
    each direction contains the the x and y to add t your current cords to move to that direction,
    and the bit representing the direction in the bit map,
    the latter is used to check if the move is valid or not,
    if not it is ignored, otherwise it is applied to the player.

    ghost movements: the ghost used a vector based algo to go as close to their target as possible,
    the algo is simply the ghost take the x and y of all adjasent cells that it can go to,
    it then takes the x and y of the target cell, it does subtract the x of the cell and x of the target and squares them,
    and add them to y of the cell minus y of the target squared,
    it then choose the cell with the least value,
    the ghost cannot go backwards unless it has no other choice
