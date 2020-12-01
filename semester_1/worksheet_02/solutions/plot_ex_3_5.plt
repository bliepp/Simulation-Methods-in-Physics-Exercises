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
set out "plots/ex_3_5.pdf"

c = "red blue green orange"
set for [i=1:words(c)] linetype i lc rgb word(c, i)

set xlabel "number of particles n"
set ylabel "calculation time t [s]"

a = 1 #exp(-6)
f(x) = b*x + log(a) # linearized
set fit log "fit.ex_3_5.log"
fit f(x) "outfiles/ex_3_5.out" u (log($1)):(log($2)) via a, b

f_mod(x) = a*x**b
set key left Left
plot "outfiles/ex_3_5.out" u 1:2 notitle, f_mod(x) title sprintf("(%.2fe-3) n^{%.2f}", a*1000, b)

set log y
plot "outfiles/ex_3_5.out" u 1:2 notitle, f_mod(x) title sprintf("(%.2fe-3) n^{%.2f}", a*1000, b)

set log
set xrange [8:200]
plot "outfiles/ex_3_5.out" u 1:2 notitle, f_mod(x) title sprintf("(%.2fe-3) n^{%.2f}", a*1000, b)

