from Point3 import Point3
from Vector3 import Vector3
import math

class Ray:
    def __init__(self, source=None, dir=None, dest=None):
        if source is None:
            source = Point3()
        if dir is None and dest is None:
            dir = Vector3(0, 0, 1)
        elif dir is None:
            dir = Vector3.from_points(source, dest)
        
        self.source = source
        self.dir = dir

    def eval(self, t):
        return self.source.lerp(self.source, self.dir, t)

    def get_source(self): return self.source

    def adjust_source(self, epsilon):
        self.source.x += self.dir.dx * epsilon
        self.source.y += self.dir.dy * epsilon
        self.source.z += self.dir.dz * epsilon

    """
    * computeReflection(refSource, norm):
    *    Computes the reflection of current ray about the given normal
    *    ref_source: Source for the reflect ray
    *    norm: Normal of the reflection
    *    returns the resulting reflected ray
    """
    def compute_reflection(self, ref_source, norm):
        norm.normalize()
        t = 2 * norm.dot(self.dir)
        reflected_dir = Vector3(
            self.dir.dx - t * norm.dx,
            self.dir.dy - t * norm.dy,
            self.dir.dz - t * norm.dz
        )
        return Ray(ref_source.__copy__(), reflected_dir)
    
    def compute_refraction(self, ref_source, norm, ref_index):
        a = (self.dir - norm.scale(norm.dot(self.dir))).scale(1/ref_index)  # Verified, is correct
        b = norm.scale(math.sqrt(1 - math.pow(1/ref_index , 2) * (1-math.pow(norm.dot(self.dir) , 2)))) #
        refracted_dir = a - b

        return Ray(ref_source.__copy__(), refracted_dir)
    
    def __repr__(self):
        return f"Ray(Start: {self.source}, Dir: {self.dir})"
