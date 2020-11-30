#!/usr/bin/gnuplot

#SETUP AREA
reset
set encoding utf8
#set decimalsign ','

set grid
set key top right Right

#OUTPUT AREA
set term pdf enhanced color font "Helvetica,14" size 4,3
#set out "daten.pdf"
#set term postscript eps enhanced color font "Helvetica,14" size 4,3
set out "plots/ex_2_1.pdf"
set fit logfile "fit.ex_2_1.log"


## globals
set yrange [0:]	
set xrange [:11]
set xlabel "t [s]"
	
## yt
set ylabel "y [m]"
plot "outfiles/ex_2_1.out" u 1:3 w l title "Cannonball" lt rgb "red"

## xt
set key left
set ylabel "x [m]"
plot "outfiles/ex_2_1.out" u 1:2 w l title "Cannonball" lt rgb "red"

## xy
set key right
set xrange [:520]
set xlabel "x [m]"
set ylabel "y [m]"
plot "outfiles/ex_2_1.out" u 2:3 w l title "Cannonball" lt rgb "red"
