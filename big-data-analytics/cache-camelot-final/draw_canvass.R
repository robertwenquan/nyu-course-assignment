#!/usr/bin/R -f
#
# draw_canvass.R
#
# draw the Mini Camelot Game Canvass 
# from specified pieces information
#

# draw the game canvass
plot(c(0,600), c(0,600))

# disabled cells are here

# white cells are here

# black cells are here

# draw all cells
for (x in 0:13)
  for (y in 0:7)
    rect(20 + y * 40, 20 + x * 40, 60 + y * 40, 60 + x * 40, col=5)

