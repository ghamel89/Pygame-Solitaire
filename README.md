# Pygame-Solitaire
Implementation of Solitaire created with PyGame as an exercise to learn the package

Currently game will shuffle new hand each time the game is launched (unwinnable hands are possible).
Game logic is applied, cards can only be placed on cards of the opposite color and one value lower on the main game board.
Cards can be placed in set foundation piles in order from Ace to King if they are the same suit.
If a move is not valid, cards will snap back to their original position.
Can drag and drop stacks of cards at a time.

Possible additons:
- redeal button ( either new hand or reset current deal )
- undo ( save 'GameTable' in main file in array, be able to switch between states )
