##Report of Mini Camelot Project
<p align=center> Caicai CHEN </p>
<p align=center> May 3, 2015 </p>

#### Proramming Language

Python 2.7

####How to run:####

	Install Python 2.7

	Install Tkinter

	$ python ./playcc.py

####How to play:####

1. Choose Side and Level	

	After running playcc.py, you will see the windows below:
	
	![Image of SET](images/SideLevel.jpg)	
	- Choose White or Black. White goes first.  
	- Choose different level. Dumb is the easiest and Genius is the hardest.
	- Then press SET
	
2. How to play	

	- Step 1: Click one of your piece	
		If you want to give up moving this piece, click it again.
	- Step 2: Click the next cell, the piece will move to the cell
		If your move is not legitimate, there will be notification one the screen
	- Step 3: Repeat Step 2 if not finished
	- Step 4: Click the final position again	
	
		The canvass is like the following:
	
		![Image of canvass](images/Canvass.jpg)	
		 Four corners are disabled cells, you can not click.

####About Design:####

1. Cutoff

	Pass the parameter `level` to alpha-beta algorithm. 
	When passing to next level, level - 1.
	Stop when level = 0, call evaluation function
	
2. Evaluation function

	My evaluation function consist of four part: (The coefficients are empirical)
	- Distance to castle (Coefficient: 1)
		Squared (14 - distance), the closer, the higher utility.
		It encourages Robot player move the piece near to castle, if two piece under the same circumstances.
	- Penalty of being captured (Coefficient: 30)
		It courages robot to capture enemy piece and avoid been captured.
	- Penalty of stoping beside a enemy piece (Coefficient: 0)
    Avoid been captured in the next move of enemy
	- Penalty of far away from center (Coefficient: 2) 
		Encourages Robot choosing more central cell
	- Different levels of difficulty
		Using cutting-off level to set different level of difficulty 
    - Dumb: level = 1
		- Smart: level = 2
		- Genius: level = 3

3.  Smartcc.cache

	This file stores some playing history information of this game.
	After human player played, Robot will check this file first
	If this condition has appeared before
	It will move directly according to the stored information.
	If not, it will calculate the next move and store this condition in the file
	
