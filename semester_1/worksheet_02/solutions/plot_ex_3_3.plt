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

c = "black red green blue orange"
set for [i=1:words(c)] linetype i lc rgb word(c, i)

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

set arrow from 1.97, graph 0 to 1.97, graph 1 nohead lt rgb "grey"
set arrow from 3.17, graph 0 to 3.17, graph 1 nohead lt rgb "grey"
set arrow from 6.53, graph 0 to 6.53, graph 1 nohead lt rgb "grey"
set arrow from 7.65, graph 0 to 7.65, graph 1 nohead lt rgb "grey"
plot "outfiles/ex_3_3.out" u 1:($2+$3) w l notitle
