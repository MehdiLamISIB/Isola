# Console Isola game and pygame version:
This project consist of creating the isola game
in the console using an IA with minmax alpha-beta optimisation.

* main.py as a console version of the Isola game
* game.py as a pygame version of the Isola game
* minmax.py is used in both of the 2 version and return the best board for the IA

The evaluation value is:
```python
    # move_player : the possible move of player
    # move_player : the possible move of adversary
    return move_player-2*move_adversary
```
