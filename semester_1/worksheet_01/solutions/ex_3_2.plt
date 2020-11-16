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
set out "plots/ex_3_2.pdf"

#[b'Sun' b'Earth' b'Moon' b'Mars' b'Venus' b'Jupiter']

set xrange [-5:6]
set yrange [-5:6]
set xlabel "x [10^{-3}]"
set ylabel "y [10^{-3}]"
plot "outfiles/ex_3_2_symeul.out" u (($6-$4)*1000):(($7-$5)*1000) w l title "Symplectic Euler" lt rgb "grey",\
	"outfiles/ex_3_2_fourier.out" u ($2*1000):($3*1000) w l title "Center movement" lt rgb "red"
plot "outfiles/ex_3_2_velver.out" u (($6-$4)*1000):(($7-$5)*1000) w l title "Velocity Verlet" lt rgb "grey"
set ztics 0.2
set border 4095
set zlabel "time [a]" rotate by 90
set view 70, 50
splot "outfiles/ex_3_2_symeul.out" u (($6-$4)*1000):(($7-$5)*1000):1 w l title "Symplectic Euler" lt rgb "grey",\
	"outfiles/ex_3_2_fourier.out" u ($2*1000):($3*1000):1 w l title "Center movement" lt rgb "red"
splot "outfiles/ex_3_2_velver.out" u (($6-$4)*1000):(($7-$5)*1000):1 w l title "Velocity Verlet" lt rgb "grey"

set key left
unset xrange
set yrange [-5:6]
set multiplot layout 2,1
	set bmargin 0
	unset xlabel
	set ylabel "x [10^{-3}]"
	set xtics format ""
	plot "outfiles/ex_3_2_symeul.out" u 1:(($6-$4)*1000) w l title "Symplectic Euler" lt rgb "blue",\
		"outfiles/ex_3_2_fourier.out" u 1:($2*1000) w l notitle lt rgb "blue" dashtype "."
	unset bmargin
	set xlabel "time [a] ^{}"
	set ylabel "y [10^{-3}]"
	set xtics format "%.1f"
	plot "outfiles/ex_3_2_symeul.out" u 1:(($7-$5)*1000) w l title "Symplectic Euler" lt rgb "red",\
		"outfiles/ex_3_2_fourier.out" u 1:($3*1000) w l notitle lt rgb "red" dashtype "."
unset multiplot

set multiplot layout 2,1
	set bmargin 0
	unset xlabel
	set ylabel "x [10^{-3}]"
	set xtics format ""
	plot "outfiles/ex_3_2_velver.out" u 1:(($6-$4)*1000) w l title "Velocity Verlet" lt rgb "blue"
	unset bmargin
	set xlabel "time [a] ^{}"
	set ylabel "y [10^{-3}]"
	set xtics format "%.1f"
	plot "outfiles/ex_3_2_velver.out" u 1:(($7-$5)*1000) w l title "Velocity Verlet" lt rgb "red"
unset multiplot

