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
set out "plots/ex_3_2.pdf"

set xlabel "radial distance r_{ij}"
set ylabel "potential U"
set xrange [0.8:2.6]
set yrange [-1.9:18]
set object 1 rectangle from 0.93,-1.5 to 1.87,2 behind
plot "outfiles/ex_3_2.out" u 1:2 w l notitle lt rgb "red"

set xrange [0.93:1.87]
set yrange [-1.5:2]
unset object 1
replot

set ylabel "radial force F_r"
set xrange [0.8:2.6]
set yrange [-25:350]
set object 2 rectangle from 1,-5 to 2.2,10 behind
plot "outfiles/ex_3_2.out" u 1:3 w l notitle lt rgb "red"
set xrange [1:2.2]
set yrange [-3:4]
unset object 2
replot
