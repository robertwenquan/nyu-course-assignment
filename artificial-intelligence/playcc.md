  -------------------------- ---------------------------------------------------------------------------------------------------------------------------------------------------
   \                         [index](.)\
    \                        [/root/github/nyu-course-assignment/artificial-intelligence/playcc.py](file:/root/github/nyu-course-assignment/artificial-intelligence/playcc.py)
  **playcc** (22 Apr 2015)   
  -------------------------- ---------------------------------------------------------------------------------------------------------------------------------------------------

`this is the Mini Camelot game for CS-GY 6613 Artificial Intelligence course in Spring 2015 semester   this source code defines a few classes: - the rules of the game (GameEngine) - the logic of the game player (Player) - the core data structure to support the game play (GameCanvass, Cell)`

 \
 **Modules**

`      `

 

  ------------------------ ------------------ -------------------- --
  [getopt](getopt.html)\   [sys](sys.html)\   [time](time.html)\   
                                                                   
  ------------------------ ------------------ -------------------- --

 \
 **Classes**

`      `

 

[\_\_builtin\_\_.object](__builtin__.html#object)

[Cell](playcc.html#Cell)

[GameCanvass](playcc.html#GameCanvass)

[GameEngine](playcc.html#GameEngine)

[Player](playcc.html#Player)

 \
 class **Cell**([\_\_builtin\_\_.object](__builtin__.html#object))

`   `

`one cell of the game canvass `

 

Methods defined here:\

**\_\_init\_\_**(self, x, y, status='disabled')

* * * * *

Data descriptors defined here:\

**\_\_dict\_\_**
:   `dictionary for instance variables (if defined)`

**\_\_weakref\_\_**
:   `list of weak references to the object (if defined)`

 \
 class
**GameCanvass**([\_\_builtin\_\_.object](__builtin__.html#object))

`   `

`This is the main data structure to define the game canvass matrix(14 x 8) Canvass is made of cells filled in rows and columns `

 

Methods defined here:\

**\_\_init\_\_**(self, nrow, ncol)

**add\_cell**(self, loc, side)

**free\_cell**(self, loc)
:   `set the cell free`

**get\_adjacent\_cell\_list**(self, loc, query\_type\_blacklist)
:   `get the adjacent cell list based on a type check BLACKLIST   NORMALLY there are 8 adjacent cells surrounding the (x,y) BUT in the border area, some of the 8 cells might be non-existing and should be excluded IN SOME OTHER CASES, we dont want 'disabled' cells, or 'free' cells, so we have a query blacklist   loc: (x,y) location of the cell query_type_blacklist: [] get all valid adjacent cells in a list                       ['disabled', 'free'], to exclude 'disabled' and 'free' cells from the adjacent cells                       ['disabled'], only exclude 'disabled' cells from the adjacent cells`

**get\_cell**(self, loc)
:   `get the cell object according to x,y coordinates return None if cell is not found`

**init\_canvass**(self, nrow, ncol)
:   `initialize cell coordinates and state   FIXME: this is a dirty initialization, with hard-coded cell selection an ideal one should be converting a visualized map like below to the desired cell map   +--------+ |xxx  xxx| |xx    xx|  x : disabled cells, not used in this map |x      x| ' ': free cells |        |  = : machine player |  ====  |  + : human player |   ==   | |        | |        | |   ++   | |  ++++  | |        | |x      x| |xx    xx| |xxx  xxx| +--------+`

**lock\_canvass**(self)
:   `lock all celss when game ends`

**move\_cell**(self, loc\_start, loc\_end)
:   `move one cell from one location to another`

**print\_debug\_cell\_map**(self)
:   `print the ASCII cell map on the console for debugging purpose ONLY`

**remove\_cell**(self, loc)

**reset\_canvass**(self)
:   `when the game is reset, the canvass needs to be reset to initial state`

**unlock\_canvass**(self)
:   `unlock all cells when game is reset`

* * * * *

Data descriptors defined here:\

**\_\_dict\_\_**
:   `dictionary for instance variables (if defined)`

**\_\_weakref\_\_**
:   `list of weak references to the object (if defined)`

 \
 class **GameEngine**([\_\_builtin\_\_.object](__builtin__.html#object))

`   `

`Define the rules of the game  - move rules  - defeat rules  - internal logic of the ganme `

 

Methods defined here:\

**\_\_init\_\_**(self)

**about\_me**(self)

**bot\_play**(self, player)

**get\_human\_player**(self)
:   `return the human player object limit: there is at most one human player in the game        there is possibility no human player is available in the game`

**human\_play**(self, x, y)
:   `handle the click event`

**is\_all\_pieces\_dead**(self, player)
:   `Check if all pieces of any side are dead This is one of the game winning(end) rules   Input: player Output: True / False`

**is\_castle\_occupied**(self, player)
:   `Check if the castle of any side is occupied This is one of the game winning(end) rules   Input: side = "north" or "south" Output: True / False   north castle points: (0, 3), (0, 4) south castle points: (13, 3), (13, 4)`

**is\_leap\_over\_rival**(self, loc\_start, loc\_end, player)
:   `Check if (x1, y1) -> (x2, y2) is a leap over rival this is a helper function to determine whether one rival needs to be taken   Return Value:   status - True/False, whether it is a leap over rival   loc    - (x,y) location of the rival`

**is\_legitimate\_first\_move**(self, loc\_start, loc\_end, player)
:   `This function checks whether the first jump is legitimate The reason to distinguish first jump is first jump could be either plain move or leap move while the successive moves could be only leap move   Input: loc_start: (x,y) a tuple of row and column index        loc_end  : (x,y) a tuple of row and column index        player   : need to know the play in order to do leap move                   because leap move might involve removal of rival's cells   Return Value: whether_this_is_a_legal_move (True/False), whether_it_is_terminated_move     A legitimate plain move is a True for first move     A legitimate leap move is a True for first move     terminated move means the first move is a plain move. In this case it is not allowed to move again     If the first move is a leap move, it is ok to leap again and again.`

**is\_legitimate\_leap**(self, loc\_start, loc\_end, player)
:   `This function checks whether a leap move is legal As leap move might involve removal of rival's cells player is required in order to identify its identity   Input : loc_start is a tuple of (x,y)         loc_end   is a tuple of (x,y)         player    is the game player object Output: True/False         True  - it is a legal move                 if it's leaped on rival's cells, they are removed from the cell map                 if it's leaped on its own cells, just leap         False - it is not a legal move`

**is\_match\_end**(self)
:   `Determine whether the current condition is a match end meaning either the human player wins or the AI bot wins the game   Game Winning Condition (meeting one wins the game) 1. one side taking the position of the other side 2. one side kills all cells of the other side   Input: N/A (Check the global class canvass) Output: (result, who) result = True / False, who = "north" / "south"`

**reset\_game**(self)
:   `reset the game canvass to default`

**start**(self)
:   `kickstart the game by calling the ui display`

**start\_game**(self)
:   `start the game let north plays first`

* * * * *

Data descriptors defined here:\

**\_\_dict\_\_**
:   `dictionary for instance variables (if defined)`

**\_\_weakref\_\_**
:   `list of weak references to the object (if defined)`

* * * * *

Data and other attributes defined here:\

**ncol** = 8

**north\_player** = None

**nrow** = 14

**south\_player** = None

**status** = ''

 \
 class **Player**([\_\_builtin\_\_.object](__builtin__.html#object))

`   `

`the AI game player   common attributes: ------------------ - robot          : True/False - name           : a human readable name of the player - side           : 'north' or 'south' - move_status    : intermediate status ['idle', 'selected', 'hopped'] - list_of_pieces : a list of all active pieces(soldiers) - castle_points  : castle points of this side - rival          : the opponent player - canvass        : the global canvass view   robot attributes : ------------------ - intell_level   : the intelligence level (1,2,3), the higher the smarter - `

 

Methods defined here:\

**\_\_init\_\_**(self, robot=True, name='aibot', side='',
move\_status='idle', difficulty=1)

**action\_simulation**(self, player, piece, path)
:   `Given a piece and path, simulate the action and return the captured set for recovery.`

**add\_cell\_to\_select\_path**(self, loc)

**add\_piece**(self, location)
:   `add one piece to the canvass`

**clear\_select\_path**(self)

**estimate\_function**(self)
:   `Estimate utility based on current canvass to help player make decision It composed of 4 parts: 1. distance to castle, the closer the better. 2. penalty of being captured 3. penalty of stoping beside a rival piece 4. penalty of far away from center`

**init\_castle\_points**(self)
:   `initialize the castle points of one player north player and south play has different castle points`

**init\_pieces**(self)
:   `initialize the pieces of this player north player and south player has different default pieces locations`

**is\_match\_point**(self)

**is\_self\_piece**(self, loc)
:   `Input:   loc is a tuple like (x,y) Return Value:   True/False - whether this location is a valid piece for this player`

**max\_value**(self, level, alpha, beta, num\_pruning\_max, num\_pruning\_min, nodes\_generated)
:   `Help robot to find the optimal action`

**min\_value**(self, level, alpha, beta, num\_pruning\_max, num\_pruning\_min, nodes\_generated)
:   `Calculate best solution of rival player`

**move\_piece**(self, loc\_from, loc\_to)
:   `move one piece from loc1 to loc2 update player piece info as well as canvass map`

**possible\_action**(self, piece, player)
:   `Calculate every possible of each piece Input: available piece Output: all possible path of this piece`

**possible\_jump**(self, cell\_loc, player, current\_path, explored\_set, pending\_set)
:   `Calculate all possible path for a cell to move, is used for robot to choose the best move.   Input: cell_loc: a tuple like (x,y)        current_path: the path from original path to current cell        explored_set: all cell expeared on the path        pending_set: enemy piece that have been captured Output: pathes reached this piece and moving on`

**remove\_piece**(self, location)
:   `remove one piece from the canvass`

**reset\_player**(self)
:   `This is for the game reset reset all player info to the initial state`

**select\_piece**(self, loc)

**set\_canvass**(self, canvass)

**set\_game**(self, game)

**set\_intell\_level**(self, level)

**set\_rival**(self, rival)

**simulation\_recovery**(self, player, piece, path, pending\_set)
:   `Recover simulated canvass to original one`

**whats\_next\_move**(self)
:   `from current canvass situation, calculate what is next step input:   output: [(x1,y1),(x2,y2),(x3,y3),...]`

* * * * *

Data descriptors defined here:\

**\_\_dict\_\_**
:   `dictionary for instance variables (if defined)`

**\_\_weakref\_\_**
:   `list of weak references to the object (if defined)`

* * * * *

Data and other attributes defined here:\

**list\_of\_pieces** = []

**move\_status** = 'idle'

**name** = 'aibot'

**robot** = True

**select\_loc** = None

**select\_path** = []

**side** = 'north'

 \
 **Functions**

`      `

 

**main**(argv)
:   `main function arguments parsing, initialize players, and launch game with two players`

**print\_cmdline\_help**()
:   `command line helper`

 \
 **Data**

`      `

 

**\_\_author\_\_** = 'Caicai CHEN \<caicai.chen@nyu.edu\>'\
 **\_\_date\_\_** = '22 Apr 2015'

 \
 **Author**

`      `

 

Caicai CHEN \<caicai.chen@nyu.edu\>
