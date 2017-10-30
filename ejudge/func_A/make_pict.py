# -*- coding: utf-8 -*-

''' Run for picture and picture with test points:
taty@nearbird ~/work/svn_ejudge/contests/c/func/func_kr/func_A
$ python3a make_pict.py
$ python3a make_pict.py d
'''

import matplotlib.pyplot as plt
import numpy as np
import sys
import os

pic_task_name = 'img/tfunc_A_fill.png'
pic_test_name = 'img/sfunc_A_fill.png'

fill_color = 'khaki'

def main():

  xmin = -8
  xmax = 8
  x = np.arange(xmin, xmax+0.1, 0.1)

  y1 = x+3
  y2 = -x+3
  y0 = -2

  fig, ax = plt.subplots()

  ax.plot(x, y1, color='red', lw=3, label='3+x')
  ax.plot(x, y2, color='green', lw=3, label='3-x')
  ax.axhline(y0, color='blue', lw=3, label=str(y0))

  ax.fill_between(x, y0, np.minimum(y1,y2), where=np.logical_and(y1 >= y0, y2 >= y0), facecolor=fill_color, interpolate=True)

  if len(sys.argv) > 1:
    plot_tests(ax)

  plt.axhline(0, color='black', lw=1)
  plt.axvline(0, color='black', lw=1)
  ax.grid()
  ax.legend()

  if len(sys.argv) == 1:
    ax.set_ylim(-4, 4)
    ax.set_xlim(-7, 7)

  plt.show()
  if not os.path.exists('img'):
    os.mkdir('img')
  if len(sys.argv) > 1:
    fig.savefig(pic_test_name, dpi=90)
  else:
    fig.savefig(pic_task_name, dpi=90)
    
if __name__ == '__main__' :
  sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
  from plot_tests import plot_tests
  main()
    

