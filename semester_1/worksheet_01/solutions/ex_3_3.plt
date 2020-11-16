#!/usr/bin/gnuplot

#SETUP AREA
reset
set encoding utf8
#set decimalsign ','

set grid
set key top left Left
set xyplane 0

#OUTPUT AREA
set term pdf enhanced color font "Helvetica,14" size 4,3
#set out "daten.pdf"
#set term postscript eps enhanced color font "Helvetica,14" size 4,3
set out "plots/ex_3_3.pdf"

set xlabel "time [a]"
set ylabel "distance [10^{-1} au]"

set yrange [-0.5:9.5]
plot "outfiles/ex_3_3_velver.out" u 1:($2*10) w l title "Velocity Verlet" lt rgb "red",\
	"outfiles/ex_3_3_symeul.out" u 1:($2*10) w l title "Symplectic Euler" lt rgb "blue"

set xrange [0:6.5]
set yrange [1.5:7.5]
set ylabel "distance [10^{-3} au]"
plot "outfiles/ex_3_3_velver.out" u 1:($2*1000) w l title "Velocity Verlet" lt rgb "red",\
	"outfiles/ex_3_3_symeul.out" u 1:($2*1000) w l title "Symplectic Euler" lt rgb "blue"
