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
set out "plots/ex_3_4.pdf"

c = "black red green blue orange"
set for [i=1:words(c)] linetype i lc rgb word(c, i)

set xlabel "x position"
set ylabel "y position"
set key left Left
plot for [i=0:1] "outfiles/ex_3_4.out" u 4+2*i:5+2*i w l title sprintf("%d", i)

unset xrange
unset yrange
set xlabel "time"
set ylabel "total energy"
set format y "%.2f"

set arrow from 1.83, graph 0 to 1.83, graph 1 nohead lt rgb "grey"
set arrow from 5.48, graph 0 to 5.48, graph 1 nohead lt rgb "grey"
set arrow from 7.68, graph 0 to 7.68, graph 1 nohead lt rgb "grey"
set arrow from 12.97, graph 0 to 12.97, graph 1 nohead lt rgb "grey"
plot "outfiles/ex_3_4.out" u 1:($2+$3) w l notitle
