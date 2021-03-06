#!/usr/bin/gnuplot

#SETUP AREA
reset
set encoding utf8
#set decimalsign ','

set grid
set key top left Left

#OUTPUT AREA
set term pdf enhanced color font "Helvetica,14" size 4,3
#set out "daten.pdf"
#set term postscript eps enhanced color font "Helvetica,14" size 4,3
set out "plots/ex_3_1.pdf"

#[b'Sun' b'Earth' b'Moon' b'Mars' b'Venus' b'Jupiter']

set xlabel "x [au]"
set ylabel "y [au]"

set xrange [-2:5.5]
set yrange [-1.5:4]
plot "outfiles/ex_3_1.out" u 2:3 w p title "Sun" pt 7 lt rgb "yellow",\
	"outfiles/ex_3_1.out" u 10:11 w l title "Venus" lt rgb "green",\
	"outfiles/ex_3_1.out" u 4:5 w l title "Earth" lt rgb "blue",\
	"outfiles/ex_3_1.out" u 6:7 w l title "Moon" lt rgb "grey",\
	"outfiles/ex_3_1.out" u 8:9 w l title "Mars" lt rgb "orange",\
	"outfiles/ex_3_1.out" u 12:13 w l title "Jupiter" lt rgb "brown"

set key opaque
set xrange [-1.1:1.1]
set yrange [-1.1:1.1]
plot "outfiles/ex_3_1.out" u 2:3 w p title "Sun" pt 7 lt rgb "yellow",\
	"outfiles/ex_3_1.out" u 10:11 w l title "Venus" lt rgb "green",\
	"outfiles/ex_3_1.out" u 4:5 w l title "Earth" lt rgb "blue",\
	"outfiles/ex_3_1.out" u 6:7 w l title "Moon" lt rgb "grey"

set key right nobox
set xrange [0.5:0.9]
set yrange [0.5:0.9]
plot "outfiles/ex_3_1.out" u 4:5 w l title "Earth" lt rgb "blue",\
	"outfiles/ex_3_1.out" u 6:7 w l title "Moon" lt rgb "grey"


set xlabel "x [10^{-3} au]"
set ylabel "y [10^{-3} au]"
set xrange [-5:6]
set yrange [-5:6]
plot "outfiles/ex_3_1.out" u (($6-$4)*1000):(($7-$5)*1000) w l title "Moon (relative), {/Symbol D}t = 0.0001" lt rgb "grey"
set xrange [-50:260]
set yrange [-50:260]
plot "outfiles/ex_3_1_coarse.out" u (($6-$4)*1000):(($7-$5)*1000) w l title "Moon (relative), {/Symbol D}t = 0.001" lt rgb "grey"

set key left
unset xrange
set yrange [-5:6]
set xlabel "time [a]^{}" # emüty exponent to format correctly
set ylabel "position [10^{-3} au]"
plot "outfiles/ex_3_1.out" u 1:(($6-$4)*1000) w l title "Moon X (relative), {/Symbol D}t = 0.0001" lt rgb "blue",\
	"outfiles/ex_3_1.out" u 1:(($7-$5)*1000) w l title "Moon Y (relative), {/Symbol D}t = 0.0001" lt rgb "red"
set yrange [-50:260]
plot "outfiles/ex_3_1_coarse.out" u 1:(($6-$4)*1000) w l title "Moon X (relative), {/Symbol D}t = 0.001" lt rgb "blue",\
	"outfiles/ex_3_1_coarse.out" u 1:(($7-$5)*1000) w l title "Moon Y (relative), {/Symbol D}t = 0.001" lt rgb "red"

