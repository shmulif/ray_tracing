
from GeomObj import GeomObj
from Vector3 import Vector3
from Hit import Hit
from OpenGL.GL import *

class BoxObj(GeomObj):
    def __init__(self):
        super().__init__()

    @staticmethod
    def draw_side(slices_x, slices_y):
        """ Draw a plane of the specified dimension.
            The plane is a 2x2 square centered at origin (coordinates go -1 to 1).
            slices_x and slices_y are the number of divisions in each dimension
        """
        dx = 2/slices_x  # Change in x direction
        dy = 2/slices_y  # Change in y direction

        glNormal3f(0, 0, 1)
        y = -1
        for j in range(slices_y):
            glBegin(GL_TRIANGLE_STRIP)
            cx = -1
            for i in range(slices_x):
                glVertex3f(cx, y+dy, 0)
                glVertex3f(cx, y, 0)
                cx += dx
            glVertex3f(1, y+dy, 0)
            glVertex3f(1, y, 0)
            glEnd()
            y += dy

        # Uncomment if you want to "see" the normal
        # isEnabled = glIsEnabled(GL_LIGHTING)
        # if isEnabled: glDisable(GL_LIGHTING)
        # glBegin(GL_LINES)
        # glColor3f(1,1,1)
        # glVertex(0, 0, 0)
        # glVertex(0, 0, 1)
        # glEnd()
        # if isEnabled: glEnable(GL_LIGHTING)

    def render_solid(self, slices=10):
        # Draw side 1 (Front)
        glPushMatrix()
        glTranslate(0, 0, 1)
        BoxObj.draw_side(slices, slices)
        glPopMatrix()

        # Draw side 2 (Back)
        glPushMatrix()
        glRotated(180, 0, 1, 0)
        glTranslate(0, 0, 1)
        BoxObj.draw_side(slices, slices)
        glPopMatrix()

        # Draw side 3 (Left)
        glPushMatrix()
        glRotatef(-90, 0, 1, 0)
        glTranslate(0,0,1)
        BoxObj.draw_side(slices, slices)
        glPopMatrix()

        # Draw side 4 (Right)
        glPushMatrix()
        glRotatef(90, 0, 1, 0)
        glTranslate(0,0,1)
        BoxObj.draw_side(slices, slices)
        glPopMatrix()

        # Draw side 5 (Top)
        glPushMatrix()
        glRotatef(-90, 1, 0, 0)
        glTranslate(0,0,1)
        BoxObj.draw_side(slices, slices)
        glPopMatrix()

        # Draw side 6 (Bottom)
        glPushMatrix()
        glRotatef(90, 1, 0, 0)
        glTranslate(0,0,1)
        BoxObj.draw_side(slices, slices)
        glPopMatrix()

    # Cube render
    def local_intersect(self, ray, best_hit):
        # Define bounds for cube
        cube_min = Vector3(-1, -1, -1)
        cube_max = Vector3(1, 1, 1)

        # Calculate min bound and max bound for each axis for entry point and exit point 
        if ray.dir.dx != 0:
            t_min_x = (cube_min.dx - ray.source.x) / ray.dir.dx
            t_max_x = (cube_max.dx - ray.source.x) / ray.dir.dx
            if t_min_x > t_max_x:
                t_min_x, t_max_x = t_max_x, t_min_x
        else:
            t_min_x = float('-inf')
            t_max_x = float('inf')

        # Calculate t_min_y and t_max_y
        if ray.dir.dy != 0:
            t_min_y = (cube_min.dy - ray.source.y) / ray.dir.dy
            t_max_y = (cube_max.dy - ray.source.y) / ray.dir.dy
            if t_min_y > t_max_y:
                t_min_y, t_max_y = t_max_y, t_min_y
        else:
            t_min_y = float('-inf')
            t_max_y = float('inf')

        # Calculate t_min_z and t_max_z
        if ray.dir.dz != 0:
            t_min_z = (cube_min.dz - ray.source.z) / ray.dir.dz
            t_max_z = (cube_max.dz - ray.source.z) / ray.dir.dz
            if t_min_z > t_max_z:
                t_min_z, t_max_z = t_max_z, t_min_z
        else:
            t_min_z = float('-inf')
            t_max_z = float('inf')


        # Define overarching t_min and t_max
        t_min = max(t_min_x, t_min_y, t_min_z)
        t_max = min(t_max_x, t_max_y, t_max_z)

        # If no valid intersection or intersection is behind the ray, return False
        if t_min > t_max or t_max < 0:
            return False
        
        # Check if t_min is valid, otherwise use t_max
        if t_min > 0:
            t = t_min
        else:
            t = t_max

        # Check position of intersection
        if best_hit.t != -1 and t >= best_hit.t:
            return False

        # Update best_hit
        best_hit.t = t
        best_hit.point = ray.eval(t)

        # Normal computation dependent on which face was hit
        epsilon = 1e-5
        if abs(best_hit.point.x - cube_min.dx) < epsilon:
            best_hit.norm = Vector3(-1, 0, 0)
        elif abs(best_hit.point.x - cube_max.dx) < epsilon:
            best_hit.norm = Vector3(1, 0, 0)
        elif abs(best_hit.point.y - cube_min.dy) < epsilon:
            best_hit.norm = Vector3(0, -1, 0)
        elif abs(best_hit.point.y - cube_max.dy) < epsilon:
            best_hit.norm = Vector3(0, 1, 0)
        elif abs(best_hit.point.z - cube_min.dz) < epsilon:
            best_hit.norm = Vector3(0, 0, -1)
        elif abs(best_hit.point.z - cube_max.dz) < epsilon:
            best_hit.norm = Vector3(0, 0, 1)

        best_hit.norm.normalize()
        best_hit.obj = self

        return True