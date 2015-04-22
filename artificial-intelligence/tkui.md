  ---------- -----------------------------------------------------------------------------------------------------------------------------------------------
   \         [index](.)\
    \        [/root/github/nyu-course-assignment/artificial-intelligence/tkui.py](file:/root/github/nyu-course-assignment/artificial-intelligence/tkui.py)
  **tkui**   
  ---------- -----------------------------------------------------------------------------------------------------------------------------------------------

`this is the Mini Camelot game for CS-GY 6613 Artificial Intelligence course in Spring 2015 semester   this source code defines the GUI part of the game. The GUI is based on Python Tkinter interface via Tcl/Tk`

 \
 **Classes**

`      `

 

[\_\_builtin\_\_.object](__builtin__.html#object)

[PlayGround](tkui.html#PlayGround)

 \
 class **PlayGround**([\_\_builtin\_\_.object](__builtin__.html#object))

`   `

`play ground for the game canvass the button_map is made of 8 x 14 squared cells `

 

Methods defined here:\

**\_\_init\_\_**(self, game)
:   `# pylint: disable=too-many-instance-attributes # we just need those attributes`

**about\_me**(self)
:   `show the author and version of this application`

**display**(self)
:   `start the display mainloop All buttons will be on the screen right now`

**make\_menu**(self)
:   `make the menu bar`

**make\_top\_bar**(self)
:   `make the top bar, with game restart, and statistics information`

**notify\_win**(self, who)
:   `notify the game ending by annoucing the winner on top the whole canvass will be locked and unclickable at this point`

**prepare\_the\_playground**(self, ncol, nrow)
:   `draw the playground according to the cell status map different status maps to different color`

**refresh\_playground**(self)
:   `refresh the playground`

**reset\_ui**(self)
:   `reset UI by hiding the game winning picture from the canvass`

**select\_start\_options**(self)
:   `popup box to select side and difficulty levels`

**selected\_start\_options**(self, popup, choose\_side, choose\_level)
:   `this is the callback function of the submit button for the game start options`

**update\_statistics**(self, move\_stats)
:   `update the move statistics for the bot player, for each move   Four metrics are collected for the statistics:  - max_depth_reached  - nodes_generated-  - num_pruning_max_value  - num_pruning_min_value`

* * * * *

Data descriptors defined here:\

**\_\_dict\_\_**
:   `dictionary for instance variables (if defined)`

**\_\_weakref\_\_**
:   `list of weak references to the object (if defined)`

 \
 **Data**

`      `

 

**DISABLED** = 'disabled'\
 **LEFT** = 'left'\
 **NORMAL** = 'normal'
