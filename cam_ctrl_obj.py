###############################
# page 27
import glfw
import wx
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import numpy as np
from OpenGL.arrays import vbo
import ctypes

gElevation = 0.
gAzimuth = 0.

drag_x_origin = 0.
drag_y_origin = 0.

panning_x = 0.
panning_y = 0.

orbit = 0
panning = 0
zooming = 1

gCamAng = 0.
gCamHeight = 1.
gFovy = 45
gPolygon = 1

gIndexArray = np.array([])
gNormalArray = np.array([])
gVertexArray = np.array([])

def drawUnitCube_glVertex():
    glBegin(GL_TRIANGLES)

    glNormal3f(0, 1, 0)  # v0, v1, ... v5 normal
    glVertex3f(0.5, 0.5, -0.5)  # v0 position
    glVertex3f(-0.5, 0.5, -0.5)  # v1 position
    glVertex3f(-0.5, 0.5, 0.5)  # v2 position

    glVertex3f(0.5, 0.5, -0.5)  # v3 position
    glVertex3f(-0.5, 0.5, 0.5)  # v4 position
    glVertex3f(0.5, 0.5, 0.5)  # v5 position

    glNormal3f(0, -1, 0)  # v6, v7, ... v11 normal
    glVertex3f(0.5, -0.5, 0.5)  # v6 position
    glVertex3f(-0.5, -0.5, 0.5)  # v7 position
    glVertex3f(-0.5, -0.5, -0.5)  # v8 position

    glVertex3f(0.5, -0.5, 0.5)  # v9 position
    glVertex3f(-0.5, -0.5, -0.5)  # v10 position
    glVertex3f(0.5, -0.5, -0.5)  # v11 position

    glNormal3f(0, 0, 1)
    glVertex3f(0.5, 0.5, 0.5)
    glVertex3f(-0.5, 0.5, 0.5)
    glVertex3f(-0.5, -0.5, 0.5)

    glVertex3f(0.5, 0.5, 0.5)
    glVertex3f(-0.5, -0.5, 0.5)
    glVertex3f(0.5, -0.5, 0.5)

    glNormal3f(0, 0, -1)
    glVertex3f(0.5, -0.5, -0.5)
    glVertex3f(-0.5, -0.5, -0.5)
    glVertex3f(-0.5, 0.5, -0.5)

    glVertex3f(0.5, -0.5, -0.5)
    glVertex3f(-0.5, 0.5, -0.5)
    glVertex3f(0.5, 0.5, -0.5)

    glNormal3f(-1, 0, 0)
    glVertex3f(-0.5, 0.5, 0.5)
    glVertex3f(-0.5, 0.5, -0.5)
    glVertex3f(-0.5, -0.5, -0.5)

    glVertex3f(-0.5, 0.5, 0.5)
    glVertex3f(-0.5, -0.5, -0.5)
    glVertex3f(-0.5, -0.5, 0.5)

    glNormal3f(1, 0, 0)
    glVertex3f(0.5, 0.5, -0.5)
    glVertex3f(0.5, 0.5, 0.5)
    glVertex3f(0.5, -0.5, 0.5)

    glVertex3f(0.5, 0.5, -0.5)
    glVertex3f(0.5, -0.5, 0.5)
    glVertex3f(0.5, -0.5, -0.5)

    glEnd()

def createVertexArraySeparate():
    varr = np.array([
        [0, 1, 0],  # v0 normal
        [0.5, 0.5, -0.5],  # v0 position
        [0, 1, 0],  # v1 normal
        [-0.5, 0.5, -0.5],  # v1 position
        [0, 1, 0],  # v2 normal
        [-0.5, 0.5, 0.5],  # v2 position

        [0, 1, 0],  # v3 normal
        [0.5, 0.5, -0.5],  # v3 position
        [0, 1, 0],  # v4 normal
        [-0.5, 0.5, 0.5],  # v4 position
        [0, 1, 0],  # v5 normal
        [0.5, 0.5, 0.5],  # v5 position

        [0, -1, 0],  # v6 normal
        [0.5, -0.5, 0.5],  # v6 position
        [0, -1, 0],  # v7 normal
        [-0.5, -0.5, 0.5],  # v7 position
        [0, -1, 0],  # v8 normal
        [-0.5, -0.5, -0.5],  # v8 position

        [0, -1, 0],
        [0.5, -0.5, 0.5],
        [0, -1, 0],
        [-0.5, -0.5, -0.5],
        [0, -1, 0],
        [0.5, -0.5, -0.5],

        [0, 0, 1],
        [0.5, 0.5, 0.5],
        [0, 0, 1],
        [-0.5, 0.5, 0.5],
        [0, 0, 1],
        [-0.5, -0.5, 0.5],

        [0, 0, 1],
        [0.5, 0.5, 0.5],
        [0, 0, 1],
        [-0.5, -0.5, 0.5],
        [0, 0, 1],
        [0.5, -0.5, 0.5],

        [0, 0, -1],
        [0.5, -0.5, -0.5],
        [0, 0, -1],
        [-0.5, -0.5, -0.5],
        [0, 0, -1],
        [-0.5, 0.5, -0.5],

        [0, 0, -1],
        [0.5, -0.5, -0.5],
        [0, 0, -1],
        [-0.5, 0.5, -0.5],
        [0, 0, -1],
        [0.5, 0.5, -0.5],

        [-1, 0, 0],
        [-0.5, 0.5, 0.5],
        [-1, 0, 0],
        [-0.5, 0.5, -0.5],
        [-1, 0, 0],
        [-0.5, -0.5, -0.5],

        [-1, 0, 0],
        [-0.5, 0.5, 0.5],
        [-1, 0, 0],
        [-0.5, -0.5, -0.5],
        [-1, 0, 0],
        [-0.5, -0.5, 0.5],

        [1, 0, 0],
        [0.5, 0.5, -0.5],
        [1, 0, 0],
        [0.5, 0.5, 0.5],
        [1, 0, 0],
        [0.5, -0.5, 0.5],

        [1, 0, 0],
        [0.5, 0.5, -0.5],
        [1, 0, 0],
        [0.5, -0.5, 0.5],
        [1, 0, 0],
        [0.5, -0.5, -0.5],
    ], 'float32')
    return varr

def render(ang):
    global gCamAng, gCamHeight, gFovy, gPolygon
    global gAzimuth, gElevation
    global panning_x, panning_y
    global zooming
    global orbit, panning, zooming

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glEnable(GL_DEPTH_TEST)

    glMatrixMode(GL_PROJECTION)  # use projection matrix stack for projection transformation for correct lighting
    glLoadIdentity()

    gluPerspective(gFovy, 1, 1, 40)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    gluLookAt(10 * np.sin(gCamAng), gCamHeight, 10 * np.cos(gCamAng), 0, 0, 0, 0, 1, 0)

    glTranslatef(panning_x, -panning_y, zooming)

    glRotatef(gAzimuth, 1.0, 0.0, 0.0)
    glRotatef(gElevation, 0.0, 1.0, 0.0)

    drawFrame()

    glEnable(GL_LIGHTING)  # try to uncomment: no lighting
    glEnable(GL_LIGHT0)
    glEnable(GL_LIGHT1)

    # light position
    glPushMatrix()

    # glRotatef(ang,0,1,0)  # try to uncomment: rotate light
    lightPos0 = (3., 0., 0., 1.) # try to change 4th element to 0. or 1.
    lightPos1 = (0., 0., 3., 1.)
    glLightfv(GL_LIGHT0, GL_POSITION, lightPos0)
    glLightfv(GL_LIGHT0, GL_POSITION, lightPos1)

    glPopMatrix()

    # light intensity for each color channel
    ambientLightColor0 = (.1, .1, .1, 1.)
    diffuseLightColor0 = (.3, .3, .3, 1.)
    specularLightColor0 = (.1, .1, .1, .1)
    glLightfv(GL_LIGHT0, GL_AMBIENT, ambientLightColor0)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, diffuseLightColor0)
    glLightfv(GL_LIGHT0, GL_SPECULAR, specularLightColor0)

    ambientLightColor1 = (.1, .1, .1, 1.)
    diffuseLightColor1 = (.3, .3, .3, 1.)
    specularLightColor1 = (.1, .1, .1, 1.)
    glLightfv(GL_LIGHT1, GL_AMBIENT, ambientLightColor1)
    glLightfv(GL_LIGHT1, GL_DIFFUSE, diffuseLightColor1)
    glLightfv(GL_LIGHT1, GL_SPECULAR, specularLightColor1)

    # material reflectance for each color channel
    diffuseObjectColor = (1., 1., 1., 1.)
    specularObjectColor = (1., 0., 0., 1.)
    glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, diffuseObjectColor)
    #glMaterialfv(GL_FRONT, GL_SPECULAR, specularObjectColor)

    glPushMatrix()
    # glRotatef(ang,0,1,0)    # try to uncomment: rotate object

    glColor3ub(0, 0, 255)  # glColor*() is ignored if lighting is enabled

    # drawUnitCube_glVertex()
    # drawUnitCube_glDrawArray()
    draw_obj()
    glPopMatrix()

    glDisable(GL_LIGHTING)

def draw_obj():
    global gVertexArray, gNormalArray
    varr = gVertexArray
    narr = gNormalArray
    glEnableClientState(GL_VERTEX_ARRAY)
    glEnableClientState(GL_NORMAL_ARRAY)
    glNormalPointer(GL_FLOAT, 0, narr)
    glVertexPointer(3, GL_FLOAT, 0, varr)
    glDrawArrays(GL_TRIANGLES, 0, int(varr.size / 3))

def drawFrame():
    glBegin(GL_LINES)
    glColor3ub(255, 0, 0)
    glVertex3fv(np.array([0., 0., 0.]))
    glVertex3fv(np.array([1., 0., 0.]))
    glColor3ub(0, 255, 0)
    glVertex3fv(np.array([0., 0., 0.]))
    glVertex3fv(np.array([0., 1., 0.]))
    glColor3ub(0, 0, 255)
    glVertex3fv(np.array([0., 0., 0]))
    glVertex3fv(np.array([0., 0., 1.]))
    glEnd()

def key_callback(window, key, scancode, action, mods):
    global gCamAng, gCamHeight,gFovy, gPolygon, panning, zooming
    global panning_x, panning_y
    if action == glfw.PRESS or action == glfw.REPEAT:
        if key == glfw.KEY_1:
            gCamAng += np.radians(-10)
        elif key == glfw.KEY_3:
            gCamAng += np.radians(10)
        elif key == glfw.KEY_2:
            gCamHeight += .1
        elif key == glfw.KEY_W:
            gCamHeight += -.1
        elif key == glfw.KEY_A:     #zoom in & out
            gFovy += 1
        elif key == glfw.KEY_S:
            gFovy += -1
        elif key == glfw.KEY_Z:
            gPolygon *= -1
            if gPolygon == -1:
                glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
            elif gPolygon == 1:
                glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        elif key == glfw.KEY_LEFT_SHIFT:
            if panning == 0:
                panning = 1
            else:
                panning = 0
        elif key == glfw.KEY_LEFT_CONTROL:
            if zooming == 0:
                zooming = 1
            else:
                zooming = 0
        elif key == glfw.KEY_UP:
            panning_y -= 0.5
        elif key == glfw.KEY_DOWN:
            panning_y += 0.5
        elif key == glfw.KEY_LEFT:
            panning_x += 0.5
        elif key == glfw.KEY_RIGHT:
            panning_x -= 0.5

def drop_callback(window, paths):

    global gNormalArray, gVertexArray

    obj = open(paths[0], 'r') #list to string
    lines = obj.readlines()

    #indexes = []

    varr = []
    vnarr = []

    vertices = []
    normals = []

    cnt3 = 0
    cnt4 = 0
    cnt4m = 0

    for line in lines:
        split = line.split()

        if split[0] == "v":
            temp = [float(f) for f in split[1:]]
            varr.append(temp)

        elif split[0] == "vn":
            temp = [float(f) for f in split[1:]]
            vnarr.append(temp)

        elif split[0] == "f":

            if len(split) == 4:
                cnt3 += 1
                for vertex in split[1:]:
                    slash = vertex.split('/')
                    vertices.append(varr[int(slash[0]) - 1])
                    if len(slash) > 2:
                        normals.append(vnarr[int(slash[2]) - 1])

            elif len(split) > 4:
                if len(split) == 5:
                    cnt4 += 1
                else:
                    cnt4m += 1
                for i in range(2, len(split) - 1):
                    for j in [0, i - 1, i]:
                        slash = split[1:][j].split('/')
                        vertices.append(varr[int(slash[0]) - 1])
                        if len(slash) > 2:
                            normals.append(vnarr[int(slash[2]) - 1])


    print("File name: "+paths[0])
    print("Total number of faces: "+str(cnt3+cnt4+cnt4m))
    print("Number of faces with 3 vertices: "+str(cnt3))
    print("Number of faces with 4 vertices: "+str(cnt4))
    print("Number of faces with more than 4 vertices: "+str(cnt4m))

    gNormalArray = np.array(normals)
    gVertexArray = np.array(vertices)

def button_callback(window, button, action, mod):
    global orbit, panning
    global drag_x_origin, drag_y_origin
    global panning_x, panning_y

    x, y = glfw.get_cursor_pos(window)
    drag_x_origin = x
    drag_y_origin = y

    if action == glfw.PRESS or action == glfw.REPEAT:
        if button == glfw.MOUSE_BUTTON_LEFT:
            orbit = 1
        elif button == glfw.MOUSE_BUTTON_RIGHT:
            panning = 1
    elif action == glfw.RELEASE:
            orbit = panning = 0

def cursor_callback(window, xpos, ypos):
    global drag_x_origin, drag_y_origin, gAzimuth, gElevation
    global orbit, panning
    global panning_x, panning_y

    if orbit == 1:
        gAzimuth += (ypos - drag_y_origin)*0.3
        gElevation += (xpos - drag_x_origin)*0.3
        drag_x_origin = xpos
        drag_y_origin = ypos

    elif panning == 1:
        panning_x = (xpos-drag_x_origin)*0.01
        panning_y = (ypos-drag_y_origin)*0.01

def scroll_callback(window, xpos, ypos):
    global zooming
    if ypos > 0:
        zooming += 0.5
    elif ypos < 0:
        zooming -= 0.5

def main():

    if not glfw.init():
        return
    window = glfw.create_window(800, 800, '2015004466', None, None)
    if not window:
        glfw.terminate()
        return
    glfw.make_context_current(window)
    glfw.set_key_callback(window, key_callback)
    glfw.set_drop_callback(window, drop_callback)
    glfw.set_mouse_button_callback(window, button_callback)
    glfw.set_cursor_pos_callback(window, cursor_callback)
    glfw.set_scroll_callback(window, scroll_callback)
    glfw.swap_interval(1)

    count = 0
    while not glfw.window_should_close(window):
        glfw.poll_events()
        ang = count % 360
        render(ang)
        count += 1
        glfw.swap_buffers(window)

    glfw.terminate()


if __name__ == "__main__":
    main()
