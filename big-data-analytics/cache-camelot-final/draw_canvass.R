#!/usr/bin/Rscript
#
# draw_canvass.R
#
# Big Data Analytics Final Project
#  Visualization Part
#
# draw the Mini Camelot Game Canvass 
# from specified pieces information
#
# Example:
#  $ ./draw_canvass.R "323334354344X737482838485"
#
# Output:
#  A static PNG 'canvass-start.png' will be generated
#    to represent the initial state of the game canass
#  A dynamic GIF 'canvass-move.gif' will be generated
#    to represent the game moving process
#
# Robert WEN (robert.wen@nyu.edu)
# N12246277
#

# library to draw circles
library(plotrix)
# library to filter data frame
library(dplyr)

# echo OFF
options(echo=FALSE)

#
# check whether one (x,y) is in the list of cell locations
#
is_cell_in_list <- function(cell, cell_list) {

  off_x = cell[1]
  off_y = cell[2]

  cc <- filter(cell_list, x==off_x & y==off_y)
  ret <- (nrow(cc) > 0)

  return(ret)
}

#
# convert the hash mapkey to a list of cell locations
#
convert_hash_mapkey <- function(mapkey) {

  loc1 <- substr(mapkey, 1, 2)
  loc2 <- substr(mapkey, 3, 4)
  loc3 <- substr(mapkey, 5, 6)
  loc4 <- substr(mapkey, 7, 8)
  loc5 <- substr(mapkey, 9, 10)
  loc6 <- substr(mapkey, 11, 12)

  for (loc in c(loc1, loc2, loc3, loc4, loc5, loc6)) {
    off_x = strtoi(paste('0x', substr(loc, 1, 1), sep=''))
    off_y = strtoi(paste('0x', substr(loc, 2, 2), sep=''))

    loc_xy = c(off_x, off_y, 'north')

    if (exists("map_cell_list") == FALSE) {
      map_cell_list <- c(x=off_x, y=off_y, side='north')
    } else {
      map_cell_list <- rbind(map_cell_list, loc_xy)
    }
  }

  loc1 <- substr(mapkey, 14, 15)
  loc2 <- substr(mapkey, 16, 17)
  loc3 <- substr(mapkey, 18, 19)
  loc4 <- substr(mapkey, 20, 21)
  loc5 <- substr(mapkey, 22, 23)
  loc6 <- substr(mapkey, 24, 25)

  for (loc in c(loc1, loc2, loc3, loc4, loc5, loc6)) {
    off_x = strtoi(paste('0x', substr(loc, 1, 1), sep=''))
    off_y = strtoi(paste('0x', substr(loc, 2, 2), sep=''))

    loc_xy = c(off_x, off_y, 'south')
    map_cell_list <- rbind(map_cell_list, loc_xy)
  }

  map_cell_list <- data.frame(map_cell_list)
  return(map_cell_list)
}

draw_a_cell <- function(cell_info) {

  off_x = strtoi(cell_info[1,1])
  off_y = strtoi(cell_info[1,2])

  draw_off_x <- (40 + (off_y) * 40)
  draw_off_y <- (40 + (13-off_x) * 40)

  side = cell_info[1,3]
  if (side == "north") {
    color <- "white"
  } else {
    color <- "black"
  }

  draw.circle(draw_off_x, draw_off_y, 18, border=color, col=color)
}

# argument parsing and get cell list in data frame
args <- commandArgs(trailingOnly = TRUE)
mapkey <- args[1]

cell_map_list <- convert_hash_mapkey(mapkey)

# set target output file
png(paste("canvass",".png",sep=""), width=800, height=1200)

# draw the game canvass
plot(c(0,400), c(0,600), axes = F, xlab = NA, ylab = NA)

# disabled cells are here
disabled_cells <- rbind(c(x=0,y=0),              c( 0,1), c( 0,2), c( 0,5), c( 0,6), c( 0,7))
disabled_cells <- rbind(disabled_cells, c(1, 0), c( 1,1),                   c( 1,6), c( 1,7))
disabled_cells <- rbind(disabled_cells, c(2, 0),                                     c( 2,7))
disabled_cells <- rbind(disabled_cells, c(11,0),                                     c(11,7))
disabled_cells <- rbind(disabled_cells, c(12,0), c(12,1),                   c(12,6), c(12,7))
disabled_cells <- rbind(disabled_cells, c(13,0), c(13,1), c(13,2), c(13,5), c(13,6), c(13,7))
disabled_cells <- data.frame(disabled_cells)

# draw all cells
for (x in 0:13) {
    for (y in 0:7) {
        if (is_cell_in_list(c(x,y), disabled_cells) == FALSE) {
            if ((x %% 2 == 0 & y %% 2 == 1) | (x %% 2 == 1 & y %% 2 == 0)){
                color <- "bisque1"
                rect(20 + y * 40, 20 + x * 40, 60 + y * 40, 60 + x * 40, col=color)
            } else if ((x %% 2 == 0 & y %% 2 == 0) | (x %% 2 == 1 & y %% 2 == 1)){
                color <- "burlywood3"
                rect(20 + y * 40, 20 + x * 40, 60 + y * 40, 60 + x * 40, col=color)
            }
        }
    }
}

# draw white and black cells
nrows <- nrow(cell_map_list)
for (i in 1:nrows) {
  draw_a_cell(cell_map_list[i,])
}

