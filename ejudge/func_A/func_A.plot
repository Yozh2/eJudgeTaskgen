set terminal png size 320, 240
set grid
set output "func_A.png"

unset border
set xzeroaxis lt -1
set yzeroaxis lt -1
#set xtics axis
set xtics axis 1
set ytics axis 1
unset title
unset arrow

set xrange [-7:7]
set yrange [-5:4]
#set arrow from -3, graph 0 to -3, graph 1 nohead front lt 1 lw 2
#unset key
plot -x+3 lt 1 lw 2 , x+3 lt 2 lw 2, -2 lt 3 lw 2

#plot y(x) with filledcu below y1=2
#set object 2 rect from 0,0 to 2,3 fc lt 1
#unset object
#set arrow from 1,2 to 1,4 nohead front lt 3
#plot x*x, -x

