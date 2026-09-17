"""Blender worker, launched by the uv-driven render_chair_cover.py."""

import json
from pathlib import Path
import sys

import bpy
from mathutils import Matrix, Vector
import numpy as np

folder = Path(sys.argv[sys.argv.index("--") + 1])
samples = int(sys.argv[sys.argv.index("--") + 2])
data = json.loads((folder / "scene.json").read_text())
arrays = np.load(folder / "chair.npz")
bpy.ops.object.select_all(action="SELECT")
bpy.ops.object.delete(use_global=False)


def material(name, color, metallic=0.0):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    shader = m.node_tree.nodes.get("Principled BSDF")
    shader.inputs["Base Color"].default_value = (*color, 1)
    shader.inputs["Roughness"].default_value = 0.34
    shader.inputs["Metallic"].default_value = metallic
    return m


body = material("Porcelain blue", (0.39, 0.57, 0.70))
tab = material("Teal: positive signed depth", (0.025, 0.70, 0.47), 0.15)
pocket = material("Amber: negative signed depth", (0.95, 0.32, 0.075), 0.1)
palette = [material(f"Child {i}", c) for i, c in enumerate([
    (0.28, 0.53, 0.68), (0.79, 0.49, 0.16), (0.46, 0.36, 0.70),
    (0.29, 0.57, 0.39), (0.71, 0.34, 0.43), (0.24, 0.61, 0.60),
    (0.57, 0.65, 0.27), (0.69, 0.38, 0.24)])]
mesh = bpy.data.meshes.new("Frozen port layout: specified display scales")
mesh.from_pydata(arrays["vertices"].tolist(), [], arrays["faces"].tolist())
mesh.update()
for m in (body, tab, pocket):
    mesh.materials.append(m)
for poly, kind in zip(mesh.polygons, arrays["kinds"]):
    poly.material_index = int(kind)
    poly.use_smooth = bool(kind)

scene = bpy.context.scene
scene.render.engine = "CYCLES"
scene.cycles.samples = samples
scene.cycles.use_denoising = True
scene.cycles.seed = 0
device = "CPU"
prefs = bpy.context.preferences.addons["cycles"].preferences
for backend in ("OPTIX", "CUDA", "HIP"):
    try:
        prefs.compute_device_type = backend
        prefs.get_devices()
        available = [d for d in prefs.devices if d.type != "CPU"]
        if available:
            for d in prefs.devices:
                d.use = d.type != "CPU"
            scene.cycles.device = "GPU"
            device = backend + ": " + ", ".join(d.name for d in available)
            break
    except (TypeError, RuntimeError):
        continue
scene.render.resolution_x = 800
scene.render.resolution_y = 800
scene.render.resolution_percentage = 100
scene.render.image_settings.file_format = "PNG"
scene.render.image_settings.color_mode = "RGBA"
scene.render.film_transparent = True
scene.view_settings.view_transform = "AgX"
scene.view_settings.look = "AgX - Medium High Contrast"
scene.world.use_nodes = True
scene.world.node_tree.nodes["Background"].inputs["Color"].default_value = (0.35, 0.46, 0.60, 1)
scene.world.node_tree.nodes["Background"].inputs["Strength"].default_value = 0.45


def aim(obj, at):
    obj.rotation_euler = (Vector(at)-obj.location).to_track_quat("-Z", "Y").to_euler()


def light(name, location, energy, size, color):
    lamp = bpy.data.lights.new(name, "AREA")
    lamp.energy = energy
    lamp.shape = "DISK"
    lamp.size = size
    lamp.color = color
    obj = bpy.data.objects.new(name, lamp)
    scene.collection.objects.link(obj)
    obj.location = location
    aim(obj, (0, 0, 0))


light("Large soft key", (2, -3, 6), 650, 4, (0.78, 0.88, 1.0))
light("Warm side light", (-4, 1, 3), 420, 3, (1.0, 0.79, 0.56))
light("Front fill", (4, 6, 2), 350, 4, (0.70, 0.88, 1.0))
camera_data = bpy.data.cameras.new("Orthographic camera")
camera = bpy.data.objects.new("Orthographic camera", camera_data)
scene.collection.objects.link(camera)
scene.camera = camera
camera_data.type = "ORTHO"
camera_data.lens = 50
camera_data.clip_start = 0.001
camera_data.clip_end = 200


def render(panel, location, scale):
    camera.location = location
    aim(camera, (0, 0, 0))
    camera_data.ortho_scale = scale
    scene.render.filepath = str(folder / f"panel-{panel}.png")
    bpy.ops.render.render(write_still=True)


def instance(name, placement, scale=1, color=None):
    obj = bpy.data.objects.new(name, mesh)
    scene.collection.objects.link(obj)
    obj.matrix_world = Matrix.Translation(Vector(placement["center"])*scale) @ Matrix(placement["matrix"]).to_4x4() @ Matrix.Scale(scale, 4)
    if color is not None:
        obj.material_slots[0].link = "OBJECT"
        obj.material_slots[0].material = color
    return obj


one = instance("One chair with prescribed port layout", data["placements"]["one"][0])
render(0, (6, 8, 5.4), 3.65)
one.hide_render = True


def detail(port, x):
    # A cropped neighborhood, rigidly reoriented using a right-handed basis.
    # Uniform camera magnification is applied AFTER the disclosed feature scales.
    scale = data["detail_magnification"]
    width, depth = data["width"], data["depth"]
    edge = width * 1.45
    steps = np.linspace(-width, width, 81)
    coords = [-edge, *steps, edge]
    vertices, faces, kinds = [], [], []
    for y in coords:
        for u in coords:
            v = y*port["v_sign"]
            height = port["key"]*depth*(1-(u/width)**2)*(1-(v/width)**2)*(1+u/width/5+v/width/7) if abs(u) <= width and abs(v) <= width else 0
            vertices.append((scale*u, scale*y, scale*height))
    size = len(coords)
    for j in range(size-1):
        for i in range(size-1):
            faces.append((j*size+i, j*size+i+1, (j+1)*size+i+1, (j+1)*size+i))
            kinds.append(0 if i in (0, size-2) or j in (0, size-2) else (1 if port["key"] > 0 else 2))
    # Flat cut faces only provide context around the displayed surface crop.
    boundary = [*range(size), *(j*size+size-1 for j in range(1, size)),
                *((size-1)*size+i for i in range(size-2, -1, -1)),
                *(j*size for j in range(size-2, 0, -1))]
    bottom = []
    for idx in boundary:
        bottom.append(len(vertices))
        crop_depth = max(width * 0.384, abs(port["key"]) * depth * 1.5)
        vertices.append((*vertices[idx][:2], -scale*crop_depth))
    for j in range(len(boundary)):
        k = (j+1) % len(boundary)
        faces.append((boundary[k], boundary[j], bottom[j], bottom[k]))
        kinds.append(0)
    faces.append(tuple(reversed(bottom)))
    kinds.append(0)
    local_mesh = bpy.data.meshes.new(f"Cropped display port {port['key']}")
    local_mesh.from_pydata(vertices, [], faces)
    local_mesh.update()
    for m in (body, tab, pocket):
        local_mesh.materials.append(m)
    for poly, kind in zip(local_mesh.polygons, kinds):
        poly.material_index = kind
        poly.use_smooth = bool(kind)
    obj = bpy.data.objects.new(local_mesh.name, local_mesh)
    scene.collection.objects.link(obj)
    obj.location = (x, 0, 0)
    return obj


details = [detail(port, x) for port, x in zip(data["detail_ports"], (-0.90, 0.90))]
original_lights = [obj for obj in scene.objects if obj.type == "LIGHT"]
for obj in original_lights:
    obj.hide_render = True
scene.world.node_tree.nodes["Background"].inputs["Strength"].default_value = 0.08
tab.node_tree.nodes["Principled BSDF"].inputs["Roughness"].default_value = 0.20
pocket.node_tree.nodes["Principled BSDF"].inputs["Roughness"].default_value = 0.20
light("Raking detail light", (-1, -3, 0.85), 180, 1.0, (0.80, 0.91, 1.0))
light("Detail rim", (0, 3, 1.5), 110, 1.8, (1.0, 0.88, 0.69))
render(1, (0.7, -5, 2.6), 3.65)
for obj in details:
    obj.hide_render = True
for obj in scene.objects:
    if obj.type == "LIGHT":
        obj.hide_render = obj not in original_lights
scene.world.node_tree.nodes["Background"].inputs["Strength"].default_value = 0.45
tab.node_tree.nodes["Principled BSDF"].inputs["Roughness"].default_value = 0.34
pocket.node_tree.nodes["Principled BSDF"].inputs["Roughness"].default_value = 0.34

# Uniformly reducing the entire assembly preserves every feature proportion.
for i, placement in enumerate(data["placements"]["eight"]):
    instance(f"Child {i}", placement, scale=0.5, color=palette[i])
render(2, (6, 8, 5.4), 3.65)
(folder / "render.json").write_text(json.dumps({
    "blender_version": bpy.app.version_string, "engine": "Cycles", "device": device,
    "samples": samples, "detail_uniform_magnification_relative_to_single_chair": data["detail_magnification"],
    "detail_view": "Cropped neighborhoods of the recorded +/-7 contact ports; each independently rigidly reoriented to expose its surface. Artificial flat crop boundaries; the same disclosed feature scales as the whole-chair views.",
    "assembly_display_scale_relative_to_single_chair": 0.5,
    "surface_modifiers": [], "smooth_shading": "Cap normals only; no displaced vertices."
}, indent=2))
