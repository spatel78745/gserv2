'''
Created on Nov 21, 2015

@author: spatel78745
'''

import _thread as thread, math, pysock
from tkinter import Tk, Canvas
from tkinter.constants import N,W,E,S

#
# Config
#
CANVAS_WIDTH = 800
CANVAS_HEIGHT = 800
RADIUS = 12 
PAD = 4

root = Tk()
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

canvas = Canvas(root)
canvas['width'] = CANVAS_WIDTH
canvas['height'] = CANVAS_HEIGHT

canvas.grid(column=0, row=0, sticky=(N, W, E, S))

''' Draws a circle at (x, y, r)'''
def drawCircle(circle):
    global canvas
    x, y, r = circle[0], circle[1], circle[2]
    canvas.create_oval(x - r, y - r, x + r, y + r) 

''' Converts degrees to radians'''
def rad(degrees):
    return math.pi / 180 * degrees

''' 
Returns a point (x,y) on circle that's at an angle of theta degrees to the x-axis
'''
def pointOnCircle(theta, circle):
    theta = rad(theta)
    x, y, r = circle[0], circle[1], circle[2]
    return (r * math.cos(theta) + x, y - r * math.sin(theta))

'''
Plots a dot on the circumference of a circle
- originX, originY: The origin of the circle
-                r: The radius of the dot
'''
def plotDotOnCircle(theta, circle=(CANVAS_WIDTH / 2, CANVAS_HEIGHT / 2, 50), dotRadius=5):
# Calculate the center of the dot
    center = pointOnCircle(theta, circle)
    drawCircle((center[0], center[1], dotRadius))

def testPlotDotOnCircle():
    for theta in range(0, 360):
        plotDotOnCircle(theta)

def box_center(row, col):
    box_size = 2 * RADIUS + 2 * PAD
    x = box_size * col
    y = box_size * row
    xc = x + PAD + RADIUS
    yc = y + PAD + RADIUS

    return (xc, yc)

def box_size():
    return 2 * PAD + 2 * RADIUS

def num_rows():
    return CANVAS_HEIGHT / box_size()

def num_cols():
    return CANVAS_WIDTH / box_size()

def row_to_x(row):
    return box_size() * row

def col_to_y(col):
    return box_size * col

def drawNode(row, col, key="?"):
    xc, yc = box_center(row, col) 
    drawCircle((xc, yc, RADIUS))
    canvas.create_text(xc, yc, text=key)

def drawLeftLeg(row1, col1, row2, col2):
    xc1, yc1 = box_center(row1, col1)
    drawCircle((xc1, yc1, RADIUS))
    xc2, yc2 = box_center(row2, col2)
    m = (yc2 - yc1) / (xc2 - xc1)
    theta = abs(math.atan(m))
    print('theta = ', theta)
    x1 = xc1 - RADIUS * math.sin(180 - 90 - theta)
    y1 = yc1 + RADIUS * math.cos(180 - 90 - theta)
    x2 = xc2 + RADIUS * math.cos(theta)
    y2 = yc2 - RADIUS * math.sin(theta)
    canvas.create_line(x1, y1, x2, y2)
    #  canvas.create_line(xc1, yc1, xc2, yc2)

def drawRightLeg(row1, col1, row2, col2):
    xc1, yc1 = box_center(row1, col1)
    xc2, yc2 = box_center(row2, col2)
    m = (yc2 - yc1) / (xc2 - xc1)
    theta = abs(math.atan(m))
    print('theta = ', theta)
    x1 = xc1 + RADIUS * math.sin(180 - 90 - theta)
    y1 = yc1 + RADIUS * math.cos(180 - 90 - theta)
    x2 = xc2 - RADIUS * math.cos(theta)
    y2 = yc2 - RADIUS * math.sin(theta)
    canvas.create_line(x1, y1, x2, y2)

def testDrawNode():
    box_size = 25
    max_cols = int(CANVAS_WIDTH / box_size)
    max_rows = int(CANVAS_HEIGHT / box_size)
    for row in range(0, max_rows):
        for col in range(0, max_cols):
            drawNode(row, col)

def testDrawLeg():
    max_col = CANVAS_WIDTH / box_size()
    max_row = CANVAS_HEIGHT / box_size()
    center_row = (max_col / 2, max_row / 2)
    print(max_col, max_row, center_row)

    cx = center_row[0]
    drawNode(0, cx)

    cx1 = cx / 2
    drawNode(1, cx - cx1)
    drawNode(1, cx + cx1)
    drawLeftLeg(0, cx, 1, cx - cx1)
    drawRightLeg(0, cx, 1, cx + cx1)
    
    cx2 = cx1 / 2
    drawNode(2, cx - cx1 - cx2)
    drawNode(2, cx - cx1 + cx2)
    drawLeftLeg(1, cx - cx1, 2, cx - cx1 - cx2)
    drawRightLeg(1, cx - cx1, 2, cx - cx1 + cx2)
    
    drawNode(2, cx + cx1 - cx2)
    drawNode(2, cx + cx1 + cx2)
    drawLeftLeg(1, cx + cx1, 2, cx + cx1 - cx2)
    drawRightLeg(1, cx + cx1, 2, cx + cx1 + cx2)

def treePlotResponder(msg):
    print('GOT: ', msg)
    words = msg.split()
    if words[0] == 'drawNode':
        row = words[1]
        col = words[2]
        key = words[3]
        print('drawNode row: ', row, 'col: ', col, 'key: ', key)
        drawNode(int(row), int(col), key)
        return 'err\n'
    
    if words[0] == 'drawLeftLeg':
        row1 = words[1]
        col1 = words[2]
        row2 = words[3]
        col2 = words[4]
        print('drawLeftLeg row: ', row1, 'col: ', col1, 'row2: ', row2, 'col2: ', col2)
        drawLeftLeg(int(row1), int(col1), int(row2), int(col2))
        return 'ok\n'
    
    if words[0] == 'drawRightLeg':
        row1 = words[1]
        col1 = words[2]
        row2 = words[3]
        col2 = words[4]
        print('drawRightLeg row: ', row1, 'col: ', col1, 'row2: ', row2, 'col2: ', col2)
        drawRightLeg(int(row1), int(col1), int(row2), int(col2))
        return 'ok\n'

    if words[0] == 'dim':
        return '%d %d\n' % (num_rows(), num_cols())
        
    return 'err\n'

def testTreePlotResponder():
    print(treePlotResponder('drawNode 1 20 H'))
    print(treePlotResponder('drawNode 2 17 H'))
    print(treePlotResponder('drawNode 2 23 H'))
    print(treePlotResponder('drawLeftLeg 1 20 2 17'))
    print(treePlotResponder('drawRightLeg 1 20 2 23'))
    
if __name__ == '__main__':
#    testDrawLeg()
#    print('Hello World')
#    pysock.server(pysock.echoResponder)
    thread.start_new_thread(pysock.server, (treePlotResponder,))
    root.mainloop()
    
