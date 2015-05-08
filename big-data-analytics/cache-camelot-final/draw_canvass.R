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
for (x in 0:13) {
  for (y in 0:7) {
    if ((y == 0 | y == 1 | y == 2 | y == 5 | y == 6 | y == 7) & (x == 0 | x == 13)) {
      color <- 'grey'
    } else if ((y == 0 | y == 1 | y == 6 | y == 7) & (x == 1 | x == 12)) {
      color <- 'grey'
    } else if ((y == 0 | y == 7) & (x == 2 | x == 11)) {
      color <- 'grey'
    } else {
      color <- 5
    }
    rect(20 + y * 40, 20 + x * 40, 60 + y * 40, 60 + x * 40, col=color)
  }
}

