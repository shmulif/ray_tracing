from GeomObj import GeomObj
from Vector3 import Vector3
from Hit import Hit
from OpenGL.GL import *
from OpenGL.GLU import *

class CylinderObj(GeomObj):
    def __init__(self):
        super().__init__()
        self.quadric = gluNewQuadric()

    def render_solid(self, slices=30, stacks=1):
        # Draws the body
        gluCylinder(self.quadric, 1.0, 1.0, 2.0, slices, stacks)

        # Draws the top
        glPushMatrix()
        glTranslatef(0.0, 0.0, 2.0)
        gluDisk(self.quadric, 0.0, 1.0, slices, 1)
        glPopMatrix()

        # Draw the bottom
        glPushMatrix()
        glRotatef(180.0, 1.0, 0.0, 0.0)
        gluDisk(self.quadric, 0.0, 1.0, slices, 1)
        glPopMatrix()

    def local_intersect(self, ray, best_hit):
        # Defines cylinder
        ox, oy, oz = ray.source.x, ray.source.y, ray.source.z
        dx, dy, dz = ray.dir.dx, ray.dir.dy, ray.dir.dz

        # Quadratic coefficient for cylinder 
        A = dx*dx + dy*dy
        B = 2.0 * (ox*dx + oy*dy)
        C = ox*ox + oy*oy - 1.0

        t_candidates = []

        # Calculates side interaction based on verticality
        if abs(A) > 1e-12:
            disc = B*B - 4*A*C
            if disc >= 0:
                sqrt_disc = disc**0.5
                t1 = (-B - sqrt_disc) / (2*A)
                t2 = (-B + sqrt_disc) / (2*A)
                # Hit check
                for t_side in [t1, t2]:
                    if t_side > 1e-9:
                        z_hit = oz + dz*t_side
                        if -1 <= z_hit <= 1:
                            t_candidates.append((t_side, "side"))

        # Top and Bottom check
        if abs(dz) > 1e-12:
            t_top = (1.0 - oz) / dz
            if t_top > 1e-9:
                x_top = ox + dx*t_top
                y_top = oy + dy*t_top
                if x_top*x_top + y_top*y_top <= 1.0:
                    t_candidates.append((t_top, "top"))

            t_bottom = (-1.0 - oz) / dz
            if t_bottom > 1e-9:
                x_bottom = ox + dx*t_bottom
                y_bottom = oy + dy*t_bottom
                if x_bottom*x_bottom + y_bottom*y_bottom <= 1.0:
                    t_candidates.append((t_bottom, "bottom"))

        # Intersection check based on our candidates
        if not t_candidates:
            return False

        # Find our interaction
        t_candidates.sort(key=lambda x: x[0])
        t = t_candidates[0][0]
        part = t_candidates[0][1]

        if best_hit.t != -1 and t >= best_hit.t:
            return False

        # Update best_hit
        best_hit.t = t
        best_hit.point = ray.eval(t)

        # Normal computation
        px, py, pz = best_hit.point.x, best_hit.point.y, best_hit.point.z
        if part == "side":
            # Normal is outward from center, ignoring z
            norm = Vector3(px, py, 0)
            norm.normalize()
            best_hit.norm = norm
        elif part == "top":
            best_hit.norm = Vector3(0,0,1)
        elif part == "bottom":
            best_hit.norm = Vector3(0,0,-1)

        best_hit.obj = self
        return True
