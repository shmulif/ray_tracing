
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
        """ Draw a unit cube with one corner at origin in positive octant."""    
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

    # This must be updated, now it renders a sphere
    def local_intersect(self, ray, best_hit):
        s = ray.source
        c = ray.dir
        A = c.dx ** 2 + c.dy ** 2 + c.dz ** 2
        B = 2 * (s.x * c.dx + s.y * c.dy + s.z * c.dz)
        C = s.x ** 2 + s.y ** 2 + s.z ** 2 - 1
        discriminant = B ** 2 - 4 * A * C

        if discriminant < 0:
            return False

        sqrt_disc = discriminant ** 0.5
        t1 = (-B - sqrt_disc) / (2 * A)
        t2 = (-B + sqrt_disc) / (2 * A)
        t = min(t1, t2) if t1 > 0 and t2 > 0 else max(t1, t2)

        if t < 0 or (t >= best_hit.t and best_hit.t != -1):
            return False

        best_hit.t = t
        best_hit.point = ray.eval(t)
        best_hit.norm = Vector3(best_hit.point.x, best_hit.point.y, best_hit.point.z)
        best_hit.norm.normalize()
        best_hit.obj = self
        return True

    def compute_normal(self, point):
        normal = Vector3(0, 0, 0)
