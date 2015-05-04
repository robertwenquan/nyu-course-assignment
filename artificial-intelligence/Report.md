##Report of Mini Camelot Project
Caicai CHEN<br>
May 3, 2015

#### Programming Language

Python 2.7 with Tkinter for GUI

#### How to run the game

```
$ python playcc.py
```

#### How to play the game

##### Choose Side and Level

After running playcc.py, you will see the window below:
	
![Image of SET](images/SideLevel.jpg)	

* Choose White or Black for the human player. White always goes first.  
* Choose difficulty level for the robot. Dumb, Smart to Genius are with increasing difficulty.
* Click SET to start the game

###### Note: 
* When White is chosen, the game will start with the default canvass and wait for the first move of the human player.
* When Black is chosen, meaning the robot is playing the white. The robot player will start with the default game canvass and proceed with its first move. The human player will observe the game canvass in a non-default mode before his/her first move.
	
##### Terms:

* Cell Status
  * Disabled: The 6 cells on each corner. Those cells are not be able to hold any game piece.
  * Free: It is a legitimate cell on the game canvass. But it is not taken by any piece of the players.
  * Player: It is a legitimate cell on the game canvass. But it is taken by either white or black player.

##### Game Moving Rules

1. Step 1: Select one of your own piece on the canvass when it is on your turn to play
  * You can select the piece by single clicking the mouse
  * When you by mistake choose one move before you make the move, you can de-select it by another single click on the same piece.
  * When it is robot playing time, you may end up being unable to select any piece of your own.
  * When one piece is selected, that piece will have highlighted background color.
1. Step 2: Click the next cell you want to move
  * This is the first move, you can either proceed with a plain move or leaped move to a free cell.
  * If your move is not legitimate, there will be notification one the screen
  * If you would like to end at the first move, go to Step 4
  * If you would like to continue with leaped move, go to Step 3
1. Step 3: Click the next cell if you still want to move
  * You can leap over your own piece or enemy piece
  * If you leap over a enemy piece, that enemy piece will be taken off from the canvass
  * If you want to keep leaping, keep doing step3
  * When you want to finish the move, to to step4
1. Step 4: Click the cell you want to stop with
  * At this point the cell should be in selected state
  * Just simply click it one more time to end the move
  * The game control will be handed over to the robot immediately
	
#### Sample Canvass Map
  ![Image of canvass](images/Canvass.jpg)	

####Software Design

##### MVC Model

1. Model
  * For the Model of this game, game canvass and canvass cell are defined
  * Cell() class in playcc.py
    * to define a single cell on the game canvass
    * each cell has a status of ['free', 'north', 'south', 'disabled']
      * 'free' : the cell is a valid cell, and has not been occupied by any player
      * 'north' : the cell is currently occupied by the 'north'/'white' player
      * 'north' : the cell is currently occupied by the 'south'/'black' player
      * 'disabled' : not a valid cell on the game canvass. (cells from four corners)
  * Canvass() class in playcc.py
    * canvass is the core data structure of this game
    * canvass initialization, canvass update, cell movement, cell removal are all in this class
  * For more details refer to the pydoc of playcc.py

1. View
  * View is implemented with Python Tkinter library. 
  * View is all implemented in PlayGround() class in tkui.py
  * For more details refer to the pydoc of tkui.py

1. Control
  * game logic is implemented in GameEngine() class in playcc.py
  * robot player logic is implemented in Player() class in playcc.py
  * For more details refer to the pydoc of playcc.py

##### Smart learning cache

* Purpose of the smart cache
  * As the thinking time of the robot is non-trivial, especially in Genius mode(level 3), the smart learning cache is introduced to speed up the thinking time of the robot.
* How smart learning cache works
  * Generally, the cache comes from pre-learning and active-learning
  * pre-learning is that we simulate the canvass maps and precalculate the optimum move results based on the canvass map scenarios. 
  * active-learning is the compliment of the pre-learning cache. In active-learning, every play that is with a smart-cache-miss will trigger a real-time optimum move calculation. Then this optimum result associated with the canvass map will be stored in the cache. When the same canvass map appears again, it will be a cache hit.
* How it is implemented
  * Python pickle file is used to store the Python dictionary format.
  * At each game start, the whole cache will be loaded from the pickle file.
  * At each turn of robot play, cache is checked. With cache hit, the cached result will be fetched.
  * When there is a cache miss, a real-time optimum move will be calculated. Then this result will be appended into the cache.
	
#### Algorithmic Design

##### Cutoff

  Pass the parameter `level` to alpha-beta algorithm. 
  When passing to next level, level - 1.
  Stop when level = 0, call evaluation function

##### Evaluation function

  My evaluation function consists of four parts: (The coefficients are empirical)
  1. Distance to castle points(Coefficient: 1)
    * Squared (14 - distance), the closer, the higher utility.
    * It encourages the robot player to move the piece near to castle. If two pieces are under the same circumstances.
  1. Penalty of being captured (Coefficient: 30)
    * It courages robot to capture enemy piece and avoid been captured.
  1. Penalty of far away from center (Coefficient: 2)
    * Encourages Robot choosing more central cell
  1. Penalty of being far away from center (Coefficient: 2) 
    * Encourage the robot to choose more central cells

##### Different levels of difficulty
  * Using cutting-off level to set different levels of difficulty 
  * Dumb: level = 1
  * Smart: level = 2
  * Genius: level = 3

