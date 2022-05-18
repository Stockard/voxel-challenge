from scene import Scene
import taichi as ti
from taichi.math import *

night_mode = True
exposure = 1.0 + night_mode * 4.0

scene = Scene(voxel_edges = 0, exposure = exposure)
scene.set_floor(-20, (0.6, 0.8, 1.0))
scene.set_directional_light((1, 1, 0), 0.2, vec3(1.0, 1.0, 1.0) / exposure)
scene.set_background_color(vec3(0.6, 0.8, 1.0) / exposure)

@ti.func
def create_watermellon(r, pos = ivec3(0, 0, 0), density = 0.2):
    color_outside = vec3(12/255, 236/255, 66/255)
    color_inside = vec3(242/255, 46/255, 26/255)
    color_seeds = vec3(0.0, 0.0, 0.0)
    for x in ti.grouped(ti.ndrange((-r, r), (-r, r), (-r, r))):
        if x[1] < 0:
            if x.dot(x) < r * r * 0.5:
                scene.set_voxel(x + pos, 1, color_inside)
                is_seed = ti.random() < density
                if is_seed:
                    scene.set_voxel(x + pos, 1, color_seeds)
            else:
                is_guapi = 0
                for i in ti.grouped(ti.ndrange((-1, 1), (-1, 1), (-1, 1))):
                    j = i + x
                    if j.dot(j) < r * r * 0.5:
                        is_guapi = 1
                if is_guapi:
                    scene.set_voxel(x + pos, 1, color_outside)

@ti.kernel
def initialize_voxels():
    create_watermellon(20)

initialize_voxels()

scene.finish()
