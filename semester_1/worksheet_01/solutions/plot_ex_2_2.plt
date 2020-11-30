#!/usr/bin/gnuplot

#SETUP AREA
reset
set encoding utf8
#set decimalsign ','

set grid

#OUTPUT AREA
set term pdf enhanced color font "Helvetica,14" size 6,3
#set out "daten.pdf"
#set term postscript eps enhanced color font "Helvetica,14" size 4,3
set out "plots/ex_2_2.pdf"
set fit logfile "fit.ex_2_2.log"


## throw types
set key top right Right
set yrange [0:150]
plot "outfiles/ex_2_2_friction_wind.out" u 2:3 w l title "With friction and wind" lt rgb "green",\
	"outfiles/ex_2_2_friction.out" u 2:3 w l title "With friction" lt rgb "blue",\
	"outfiles/ex_2_2.out" u 2:3 w l title "Normal" lt rgb "red"


## wind velocities
set key left Left
set xrange [-350:350]
set yrange [-350:0]
set xlabel "Throw distance d [m]"
set ylabel "Wind velocity v_w [ms^{-1}]"

v_w(x) = m*x + b
fit v_w(x) "outfiles/ex_2_2_winds.out" u 2:1 via m, b
plot "outfiles/ex_2_2_winds.out" every 10 u 2:1 w p notitle lt rgb "blue",\
	v_w(x) title sprintf("%.2f x %.2f", m, b) lt rgb "red"
