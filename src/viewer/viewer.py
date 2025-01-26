import numpy as np
import pygame
from OpenGL.raw.GLUT import glutSolidSphere, glutSwapBuffers
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *


def draw_cube(position, scale, rotation):
    glPushMatrix()
    glTranslatef(*position)  # Set the position
    glScalef(*scale)  # Set the scale
    glRotatef(rotation[0], 1, 0, 0)  # Rotate around x-axis
    glRotatef(rotation[1], 0, 1, 0)  # Rotate around y-axis
    glRotatef(rotation[2], 0, 0, 1)  # Rotate around z-axis

    glBegin(GL_QUADS)

    # Define vertices for each face of the cube
    vertices = [
        [1, 1, -1],
        [1, -1, -1],
        [-1, -1, -1],
        [-1, 1, -1],
        [1, 1, 1],
        [1, -1, 1],
        [-1, -1, 1],
        [-1, 1, 1]
    ]

    # Define indices for each face (corrected order)
    faces = [
        [0, 1, 2, 3],  # Back face
        [4, 5, 6, 7],  # Front face
        [0, 1, 5, 4],  # Right face
        [2, 3, 7, 6],  # Left face
        [0, 3, 7, 4],  # Top face
        [1, 2, 6, 5]  # Bottom face
    ]

    # Define normals for each face
    normals = [
        (0, 0, -1),  # Back face
        (0, 0, 1),  # Front face
        (1, 0, 0),  # Right face
        (-1, 0, 0),  # Left face
        (0, 1, 0),  # Top face
        (0, -1, 0)  # Bottom face
    ]

    # Draw the faces with normals
    for i, face in enumerate(faces):
        for vertex in face:
            glVertex3fv(vertices[vertex])

    glEnd()
    glPopMatrix()


def set_lighting():
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)

    # Set up light position and properties
    light_position = (0, 1, 2, 1)
    glLightfv(GL_LIGHT0, GL_POSITION, light_position)
    glLightfv(GL_LIGHT0, GL_AMBIENT, (0.1, 0.1, 0.1, 1.0))
    glLightfv(GL_LIGHT0, GL_DIFFUSE, (0.8, 0.8, 0.8, 1.0))
    glLightfv(GL_LIGHT0, GL_SPECULAR, (1.0, 1.0, 1.0, 1.0))

    # Enable color tracking
    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
    glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, (1.0, 1.0, 1.0, 1.0))
    glMateriali(GL_FRONT_AND_BACK, GL_SHININESS, 50)


def find_perpendicular_unit_vectors(v):
    v = np.array(v)
    # Find a vector that is not parallel to v
    if np.all(v == 0):
        raise ValueError("The zero vector does not have perpendicular vectors.")
    if v[0] != 0 or v[1] != 0:
        u1 = np.array([-v[1], v[0], 0])
    else:
        u1 = np.array([0, -v[2], v[1]])

    # Normalize u1 to be a unit vector
    u1 = u1 / np.linalg.norm(u1)

    # Find the second unit vector as the cross product of v and u1
    u2 = np.cross(v, u1)
    u2 = u2 / np.linalg.norm(u2)

    return u1, u2

def draw_bone(start, end, width):
    start = np.array(start)
    end = np.array(end)
    direction = end - start

    u1, u2 = find_perpendicular_unit_vectors(direction)
    vertices = [(start - u1 * width + u2 * width), (start + u1 * width + u2 * width), (start + u1 * width - u2 * width), (start - u1 * width - u2 * width),
                (end - u1 * width + u2 * width), (end + u1 * width + u2 * width), (end + u1 * width - u2 * width), (end - u1 * width - u2 * width)]

    quads = [
        [0, 1, 2, 3],  # Front face
        [4, 5, 6, 7],  # Back face
        [0, 1, 5, 4],  # Top face
        [2, 3, 7, 6],  # Bottom face
        [0, 3, 7, 4],  # Left face
        [1, 2, 6, 5]  # Right face
    ]
    # Draw filled quads
    glBegin(GL_QUADS)
    for quad in quads:
        for vertex in quad:
            glVertex3fv(vertices[vertex])
    glEnd()

    glFlush()


def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    glDisable(GL_CULL_FACE)  # Disable backface culling
    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -10)

    set_lighting()


    clock = pygame.time.Clock()
    frame = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        frame += 1

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glRotatef(1, 0, 1, 0)

        draw_bone((0, 0, 0), (2, 2, 0), 0.25)

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
