import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

# Define cuboid vertices
def cuboid_vertices(x, y, z):
    vertices = [
        (x/2, -y/2, -z/2),
        (x/2,  y/2, -z/2),
        (-x/2,  y/2, -z/2),
        (-x/2, -y/2, -z/2),
        (x/2, -y/2,  z/2),
        (x/2,  y/2,  z/2),
        (-x/2, -y/2,  z/2),
        (-x/2,  y/2,  z/2),
    ]
    return vertices

# Define edges of the cuboid
edges = (
    (0, 1), (1, 2), (2, 3), (3, 0),
    (4, 5), (5, 6), (6, 7), (7, 4),
    (0, 4), (1, 5), (2, 6), (3, 7)
)

# Function to draw a cuboid
def draw_cuboid(vertices):
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])
    glEnd()

# Main function
def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -5)

    # Example skeleton with a single bone
    skeleton = [
        cuboid_vertices(1, 0.2, 0.2)  # Bone 1
    ]

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        glRotatef(1, 3, 1, 1)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Draw skeleton
        for bone in skeleton:
            draw_cuboid(bone)

        pygame.display.flip()
        pygame.time.wait(10)

if __name__ == "__main__":
    main()
