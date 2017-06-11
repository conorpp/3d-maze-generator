#!/usr/bin/env python

# Copyright (c) 2017 Conor Patrick

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
# of the Software, and to permit persons to whom the Software is furnished to do
# so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import random
from random import shuffle, randint
import sys
from docopt import docopt

from generate import render_maze, RESOLUTION, solid_cube, cube_mesh
from solid import *

def maze(width, height, depth, **kwargs):


    class Cell():
        #
        #   0/forward
        #2/left      3/right
        #   1/back
        # top: 4
        # bot: 5
        def __init__(self,):
            self.walls = [ {'broken': False, 'neighbor': None, 'cell':self, 'i': i, 'ni': self.inv_i(i)} for i in range(0,6)]
            self.visited = False
            self.start = False
            self.end = False
            self.walls_broken = 0
            self.edge = -1

        def wall(self,i):
            return self.walls[i]

        def visit(self,i):
            self.visited = True

        def inv_i(self,i):
            return [1,0,3,2,5,4][i]

        def remove(self,i):
            self.walls[i]['broken'] = True
            self.visit(i)
            self.walls_broken += 1

            ni = self.inv_i(i)

            assert(self == self.walls[i]['neighbor'].walls[ni]['neighbor'])
            self.walls[i]['neighbor'].walls[ni]['broken'] = True
            self.walls[i]['neighbor'].visit(ni)
            self.walls[i]['neighbor'].walls_broken += 1


        def set_neighbor(self, i, n):
            ni = self.inv_i(i)
            self.walls[i]['neighbor'] = n
            self.walls[i]['neighbor'].walls[ni]['neighbor'] = self

        def mat(self,):
            return [self.walls[0]['broken'],self.walls[1]['broken'],
                    self.walls[2]['broken'],self.walls[3]['broken'], 
                    self.walls[4]['broken'], self.walls[5]['broken']]

    grid = [[[Cell() for x in range(width)] for y in range(height)] for z in range(depth)]

    for z in range(0,depth):
        for y in range(0,height):
            for x in range(0,width):
                if y == 0:                  # forward
                    grid[z][y][x].edge = 0
                if y == height - 1:         # backward
                    grid[z][y][x].edge = 1

                if x == 0:                  # left
                    grid[z][y][x].edge = 2
                if x == (width - 1):        # right
                    grid[z][y][x].edge = 3


                if z == 0:                  # top
                    grid[z][y][x].edge = 4
                if z == (depth - 1):        # bottem
                    grid[z][y][x].edge = 5


                # forward (height)
                if (y+1) < height:
                    grid[z][y][x].set_neighbor(0, grid[z][y+1][x])

                # backward (height)
                if (y-1) >= 0:
                    grid[z][y][x].set_neighbor(1,grid[z][y-1][x])

                # right (width)
                if (x+1) > width:
                    grid[z][y][x].set_neighbor(3, grid[z][y][x+1])

                # left (width)
                if (x-1) >=0:
                    grid[z][y][x].set_neighbor(2, grid[z][y][x-1])

                # top (depth)
                if (z+1) < depth:
                    grid[z][y][x].set_neighbor(4, grid[z+1][y][x])

                # bottom (depth)
                if (z-1) >=0:
                    grid[z][y][x].set_neighbor(5, grid[z-1][y][x])



    #for z in range(1,depth-1):
        #for x in range(1,height-1):
            #for y in range(1,width-1):
                #for l in range(4):
                    #assert(grid[z][y][x].walls[l]['neighbor'] != None)


    # prim's alg
    start = random.choice(random.choice(grid[0]))

    start.start = True
    start.visited = True
    wall_list = [] + start.walls

    grid2 = [[[0,0,0,0,0,0] for x in range(width)] for x in range(height)]

    c = 0
    print 'running Prim\'s alg on potentially %d walls.' % (6 * height * width * depth)
    while len(wall_list):
        w = random.choice(wall_list)

        if w['neighbor']:
            if w['neighbor'].visited ^ w['cell'].visited:
                wall_list = wall_list + w['neighbor'].walls
                w['cell'].remove(w['i'])


        wall_list.remove(w)

    # depth-first-search to find the hardest path to determine end node, i.e. longest path
    def dfs(node, edge = None, depth = 0):
        walls = [] + node.walls
        children = []

        if edge is not None: del walls[edge]

        for x in walls:
            if x['broken']:
                children += dfs(x['neighbor'], x['ni'], depth + 1)

        return children + [(node, depth)]

    paths = dfs(start)
    end = paths[0]
    for i in paths:
        if i[0].edge  == 5:
            if i[1] > end[1]:
                end = i
    print 'correct path is %d nodes long' % end[1]
    end = end[0]
    end.end = True

    return render_maze(grid, **kwargs)

doc = '''
3D maze generator.  Uses Prim's alg to generator maze with
a start and an end and no loops.  Outputs openscad.

Usage:
  maze.py -h
  maze.py [-x WIDTH] [-y HEIGHT] [-z DEPTH] [-r RES] [-n SPACING] [-d DIAMETER] [-m | -s] <output.scad>
Options:
  -h, --help                    Show this help message and exit
  -x --width WIDTH              Number of cells wide [default: 5]
  -y --height HEIGHT            Number of cells high [default: 5]
  -z --depth DEPTH              Number of cells deep [default: 5]
  -r --resolution RES           Resolution of rendering [default: 25]
  -n --node-spacing SPACING     Distance between nodes in mm [default: 8.0]
  -d --diameter DIAMETER        Diameter of nodes in mm [default: 6.0]
  -m --enable-mesh              Creates a cross hatch mesh and subtracts maze from it.
  -s --enable-solid             Creates a solid cube and subtracts maze from it.
Examples:
maze.py output.scad
maze.py [-x 10] [-y 5] [-z 4]  [-n 10] [-d 3] [-m | -s] <output.scad>
'''


if __name__ == "__main__":

    args = docopt(doc)

    dims = [int(args['--width'][0]),int(args['--height'][0]),int(args['--depth'][0])]

    m = maze(*dims, unit = float(args['--node-spacing'][0]), diameter = float(args['--diameter'][0]))

    if args['--enable-mesh']:
        m = cube_mesh(*dims) - m
    elif args['--enable-solid']:
        m = solid_cube(*dims) - m

    out = ('$fn=%d;' % int(args['--resolution'][0]))+scad_render(m)

    open(args['<output.scad>'],'w+').write(out)







