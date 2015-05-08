#!/usr/bin/Rscript
#
# draw_canvass.R
#
# draw the Mini Camelot Game Canvass 
# from specified pieces information
#

library(plotrix)

# echo OFF
options(echo=FALSE)

# arg parsing
args <- commandArgs(trailingOnly = TRUE)
mapkey <- args[1]

# set target output file
png(paste("canvass",".png",sep=""), width=800, height=1200)

# draw the game canvass
plot(c(0,400), c(0,600), axes = F, xlab = NA, ylab = NA)

# disabled cells are here
disabled_cells <- rbind(c(x=0,y=0), c(0,1), c(0,2), c(0,5), c(0,6), c(0,7))
disabled_cells <- rbind(disabled_cells, c(1,0), c(1,1), c(1,6), c(1,7))
disabled_cells <- rbind(disabled_cells, c(2,0), c(2,7))

# white cells are here
white_cells <- rbind(c( ))

# black cells are here

# draw all cells
for (x in 0:13) {
    for (y in 0:7) {
        if ((y == 0 | y == 1 | y == 2 | y == 5 | y == 6 | y == 7) & (x == 0 | x == 13)) {
            a <- 1
        } else if ((y == 0 | y == 1 | y == 6 | y == 7) & (x == 1 | x == 12)) {
            a <- 1
        } else if ((y == 0 | y == 7) & (x == 2 | x == 11)) {
            a <- 1 
        } else if ((x %% 2 == 0 & y %% 2 == 1) | (x %% 2 == 1 & y %% 2 == 0)){
            color <- "bisque1"
            rect(20 + y * 40, 20 + x * 40, 60 + y * 40, 60 + x * 40, col=color)
        } else if ((x %% 2 == 0 & y %% 2 == 0) | (x %% 2 == 1 & y %% 2 == 1)){
            color <- "burlywood3"
            rect(20 + y * 40, 20 + x * 40, 60 + y * 40, 60 + x * 40, col=color)
        }
    }
}

# draw white cells

# draw black cells

draw.circle(80,120,18,border="black",col="black")
draw.circle(160,200,18,border="white",col="white")
draw.circle(40,40,18,border="black",col="black")

