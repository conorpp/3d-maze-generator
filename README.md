# 3d-maze-generator

This is a parametric model for a 3D maze.  Generates openscad which can render
to STL.  It uses Prim's algorithm to generate the maze so it has a defined
start.

The maze is generated randomly but the start is always on the same face.
Parameters like size, diameter, and number of nodes can be supplied.  The end is 
chosen by choosing the node on an outside edge that is furthest from the start.

## Installation

Install my version of Solid Python.  The official version currently has a couple bugs.

```
git clone https://github.com/conorpp/SolidPython
cd SolidPython
sudo python setup.py install
```

Install other pip modules

```
pip install docopt
```

## Usage

```
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
python maze.py output.scad
python maze.py [-x 10] [-y 5] [-z 4]  [-n 10] [-d 3] [-m | -s] <output.scad>
```

Running the maze.py program will generate an openscad file.  Open this with an openscad version
built after 2017.  You can find these versions right now by going to the [downloads](http://www.openscad.org/downloads.html) page
and going to **Development Snapshots**.

## Pictures

Default 5x5x5 maze

![](/pics/skel.PNG)

Solid - Default 5x5x5 maze

![](/pics/solid.PNG)

Mesh - Default 5x5x5 maze

![](/pics/mesh.PNG)

# LICENSE

Copyright (c) 2017 Conor Patrick

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
