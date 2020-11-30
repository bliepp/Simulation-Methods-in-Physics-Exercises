#!/usr/bin/gnuplot

#SETUP AREA
reset
set encoding utf8
#set decimalsign ','

set grid
set key top right Right
set xyplane 0

#OUTPUT AREA
set term pdf enhanced color font "Helvetica,12" size 4,3
#set out "daten.pdf"
#set term postscript eps enhanced color font "Helvetica,14" size 4,3
set out "plots/ex_3_3.pdf"

set xlabel "x position"
set ylabel "y position"
set xrange [-1:31]
set yrange [-15:25]
plot for [i=0:4] "outfiles/ex_3_3.out" u 4+2*i:5+2*i w l title sprintf("%d", i)

unset xrange
unset yrange
set xlabel "time"
set ylabel "total energy"
set format y "%.3f"
plot "outfiles/ex_3_3.out" u 1:($2+$3) w l notitle
