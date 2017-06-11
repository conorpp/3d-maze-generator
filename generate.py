
from solid import *
from math import *
from random import randint
import operator


unit = 8.
dia = 6.
stop_dist = unit * 1.

RESOLUTION = 25
DEBUG = 0


def get_tile(i):

    x = sqrt(2.) * unit/2. - 2. * (unit - stop_dist) / sqrt(2.)
    ang_off =  x/sqrt(2)
    b = rotate_extrude(angle=90)( translate([ang_off, 0,0])( circle(d=dia) ))
    b += translate([0,ang_off,0])( sphere(d = dia) )
    b += translate([ang_off, 0, 0])( sphere(d = dia) )
    def path(mat):

        #   0,
        # 2,  3,
        #   1


        bot_stop_to_top_open = translate([0,0,unit/2])( cylinder(d = dia, h = unit/2 + ang_off) ) + translate([0,0,unit/2])( sphere(d = dia))
        bot_open_to_top_stop = translate([0,0,0])( cylinder(d = dia, h = unit/2) ) + translate([0,0,unit/2])( sphere(d = dia)) + sphere(d = dia)
        bot_open_to_top_open = translate([0,0,0])( cylinder(d = dia, h = unit) )
        bot_open_to_top_open += translate([0, 0, unit])( sphere(d = dia) ) + sphere(d = dia)



        left_stop_to_right_open = translate([0,-unit/2 ,unit/2 ])( rotate([-90,0,0])( cylinder(d = dia, h = unit/2) ) ) + translate([0,0,unit/2])( sphere(d = dia))  + translate([0,-unit/2,unit/2])( sphere(d = dia))



        left_open_to_right_stop = translate([0,0,unit/2 ])( rotate([-90,0,0])( cylinder(d = dia, h = unit/2) ) ) + translate([0,0,unit/2])( sphere(d = dia)) + translate([0,unit/2,unit/2])( sphere(d = dia))

        left_open_to_right_open = translate([0,-unit/2,unit/2 ])( rotate([-90,0,0])( cylinder(d = dia, h = unit+ ang_off) ) )
        left_open_to_right_open += translate([0,unit/2,unit/2])(sphere(d = dia))
        left_open_to_right_open += translate([0,-unit/2,unit/2])(sphere(d = dia))

        top_hole = (translate([0,0,unit/2 ])( rotate([0,90,0])( cylinder(d = dia, h = unit/2) ) + sphere(d = dia) ) + (translate([unit/2,0,unit/2])(sphere(d = dia)))
)

        bot_hole = (translate([-unit/2,0,0])(top_hole)) 
    
        ang = b

        ang_left_bot = translate([0, -ang_off ,unit - stop_dist])( rotate([0,-90,0])(ang) )
        ang_left_top = ( translate([0, -ang_off ,unit/2 + ang_off])( rotate([0,90,0])(ang) ))

        ang_right_top = translate([0, ang_off ,unit/2 + ang_off])( rotate([0,90,180])(ang) )
        ang_right_bot = translate([0, ang_off ,unit - stop_dist])( rotate([0,-90,180])(ang) )

        #point = translate([0,0,unit/2])(cube(2))
        #if i.visited: point = color('purple')(point)
        #else: point = color('blue')(point)
        items = [cube(0)]

        if mat[0] and mat[1]:
            items.append(bot_open_to_top_open)
        elif mat[0]:
            items.append(bot_stop_to_top_open)
        elif mat[1]:
            items.append(bot_open_to_top_stop)


        if mat[2] and mat[3]:
            items.append(left_open_to_right_open )
        elif mat[2]:
            items.append(left_stop_to_right_open )
        elif mat[3]:
            items.append(left_open_to_right_stop )

        if mat[1] and mat[2]:
            items.append(ang_left_bot)
            if bot_open_to_top_stop in items:
                items.remove(bot_open_to_top_stop )


        if mat[0] and mat[2]:
            items.append(ang_left_top)
            if bot_stop_to_top_open in items:
                items.remove(bot_stop_to_top_open)



        if mat[0] and mat[3]:
            items.append(ang_right_top)
            if bot_stop_to_top_open in items:
                items.remove(bot_stop_to_top_open)



        if mat[1] and mat[3]:
            items.append(ang_right_bot)
            if bot_open_to_top_stop in items:
                items.remove(bot_open_to_top_stop )

        if mat[4]:
            items.append(top_hole)
        if mat[5]:
            items.append(bot_hole)

        if (ang_left_top in items) and (left_stop_to_right_open in items):
            items.append(bot_stop_to_top_open)


        if (ang_right_top in items) and (left_open_to_right_stop in items):
            items.append(bot_stop_to_top_open)


        if (ang_left_bot in items) and (left_stop_to_right_open in items):
            items.append(bot_open_to_top_stop)


        if (ang_right_bot in items) and (left_open_to_right_stop in items):
            items.append(bot_open_to_top_stop)


        if (ang_right_bot in items) and (ang_left_bot in items):
            items.append(bot_open_to_top_stop)

        if (ang_right_top in items) and (ang_left_top in items):
            items.append(bot_stop_to_top_open)





        return reduce(operator.add, items)

        #   0,
        # 2,  3,
        #   1
    b_via = b
    via = cylinder(h = unit, d = dia)
    via += translate([ang_off,0,0])( rotate([-90,0,180])( b_via ))
    via += translate([-ang_off,0,unit])( rotate([-90,-90,0])( b_via ))

    top_off = .1
    top_via = translate([unit,0,unit - top_off])( rotate([0,-90,0])(
                    via
                ) )

    bot_via = translate([unit,0,top_off])( rotate([0,90,180])( via ))

    right_via = translate([0,unit/2,unit/2])( rotate([0,-90,0])(cylinder(h = unit , d = dia)) )
    left_via = translate([0,-unit/2,unit/2])( rotate([0,-90,0])(cylinder(h = unit , d = dia)) )

    short_off = dia + ang_off/2
    vert_short = translate([-ang_off,0,short_off/2])( cylinder(d = dia, h = 0) )

    p = path(i.mat())

    extra = dia/2 * 1.3
    extra2 = dia/2

    if i.start: 
        p = color('orange')(p + translate([-unit*1.1,0,unit/2])(rotate([0,90,0])(cylinder(r2 = dia/2, r1 = extra, h = unit*1.1))))

    if i.end: 
        print 'exit (red) is on face',i.edge
        cyl = cylinder(d = extra2*2, h = unit*2)
        if i.edge == 0:
            p += translate([0,0,-unit*2/2 + dia/2- dia*1.3])(rotate([0,0,0])(cyl))
        if i.edge == 1:
            p += translate([0,0,unit/2])(rotate([0,0,0])(cyl))
        if i.edge == 2:
            p += translate([0,-unit*2,unit/2])(rotate([-90,0,0])(cyl))
        if i.edge == 3:
            p += translate([0,unit*2,unit/2])(rotate([90,0,0])(cyl))
        if i.edge == 4:
            p += translate([-unit*2,0,unit/2])(rotate([0,90,0])(cyl))
        if i.edge == 5:
            p += translate([-dia/2,0,unit/2])(rotate([0,90,0])(cyl))
        p = color('red')(p)

    if not DEBUG:
        return p

    if DEBUG:

        blocks = []
        for i in range(64):
            blocks.append([i & 1, i & 2, i & 4, i & 8, i & 0x10, i & 0x20])

        blocks = [path(x) for x in blocks]


        items = [translate([0,unit * 1.5 * i, 0])(x) for i,x in enumerate(blocks)]
        
        b = rotate_extrude(angle=90)( translate([dia/1.7,0,0])( circle(d=dia) ))
        b = translate([0,0,unit - stop_dist])( rotate([0,90,0])(b) )
        items.append(b)

        return reduce(operator.add, items)


    return TILES[i]

def circle_mesh(width, height, depth):
    # this takes way too long to render!
    box_h = unit * height * 1.2
    box_d = unit * max(width,depth) * 1.2

    box = cube(0)

    RES = 25
    circles = []
    for i in range(1,RES):
        circles.append(translate([box_h * i /RES ,0,0])( circle(d = unit/20  ) ))

    rings = rotate_extrude()( *circles )
    circles = []

    #box = rings
    for i in range(1,RES):
        circles.append(translate([0,0,box_h * i / RES])(rings))

    box = union()(*circles)

    box = box + translate([-box_h/2,0,box_d/2])(rotate([0,90,0])(box))
    box = translate([(unit * depth - unit/2)/2, (unit * depth - unit/2)/2, 0])(box)

    box = box * translate([-unit/2, -unit/2, 0])(cube([unit * depth + unit/2, unit * width + unit/2, unit * height]))

    return box

def stick_mesh(width, height, depth):
    x = max(width,height,depth) * unit + unit
    step = unit/20
    stick = cube([x,step,step])
    b = cube([x,step,step])
    b += translate([0,x,0])( cube([x,step,step]) )
    b += cube([step,x,step])
    b += translate([x,0,0])( cube([step,x,step]) )
    b = b + translate([0,0,x])(b)
    b += cube([step,step,x])
    b += translate([0,x,0])(cube([step,step,x]))
    b += translate([x,0,0])(cube([step,step,x]))
    b += translate([x,x,0])(cube([step,step,x]))

    sticks = []
    for i in range(2000):
        trans = [randint(int(-100 * x*2/3),int(x*100*2/3))/100.0 for i in range(3)]
        rot = [randint(0,3600)/10. for i in range(3)]

        sticks.append(translate([x/2,x/2,x/2])(
                    translate(trans)(rotate(rot)(stick))
                ))

    b = b + union()(*sticks)

    b = b * cube(x+step)

    return b

def cube_mesh(width, height, depth):
    step = unit/12
    print 'stick c-s: ', step
    x = max(width,height,depth) * unit + unit
    stick = cube([depth * unit + unit,step,step])
    stick2 = cube([step,width* unit + unit,step])
    stick3 = cube([step,step,height* unit + unit])

    b = []
    RES = 28
    for i in range (1, RES):
        for j in range (1, RES):
            b.append(translate([0, (width*unit + unit) * i/RES, (height*unit + unit) * j/RES])(stick))
            b.append(translate([(depth*unit + unit) * i/RES,0, (height*unit + unit) * j/RES])(stick2))
            b.append(translate([(depth*unit + unit) * i/RES,(width*unit + unit) * j/RES, 0])(stick3))

    #b = translate([-unit, -unit, -unit/2])(cube(x))
    b = translate([-unit, -unit, -unit/2])(union()(*b))

    return b

def solid_cube(width, height, depth):
    x = max(width,height,depth) * unit + unit
    b = translate([-unit, -unit, -unit/2])(cube([depth*unit+unit,width*unit+unit,height*unit+unit,]))
    return b



def render_maze(grid, **kwargs):
    global unit
    global dia
    global stop_dist
    unit = kwargs['unit']
    dia = kwargs['diameter']
    stop_dist = unit * 1.

    if DEBUG:
        print type(grid[0][0][0])
        print (grid[0][0][0])
        cad = get_tile(grid[0][0][0])
        #open('test.txt','w+').write(text.render(grid, options))
        out = ('$fn=%d;' % RESOLUTION)+scad_render(cad)
        open('maze.scad','w+').write(out)
        return

    depth = len(grid)
    height = len(grid[0])
    width = len(grid[0][0])


    print '%d x %d x %d cube' % (depth, height, width)
    print '(%d x %d x %d) mm cube' % (depth*unit, height*unit, width*unit)

    m = []
    for k,z in enumerate(grid):
        for j,y in enumerate(z):
            for i,x in enumerate(y):
                m.append(translate([unit * k,unit * i, unit * j])(get_tile(x)))


    m = union()(*m)

    #mesh = cube_mesh(width,height,depth)
    #m = box - m
    
    return m




