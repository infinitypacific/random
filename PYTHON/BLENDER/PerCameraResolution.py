bl_info = {
    "name": "Per-Camera Resolution",
    "author": "Frostbyte",
    "version": (1, 1),
    "blender": (2, 80, 0),
    "location": "Properties > Data (Camera) > Custom Resolution",
    "description": "Allows setting custom render resolutions per camera.",
    "warning": "",
    "doc_url": "",
    "category": "Camera",
}

import bpy
from bpy.app.handlers import persistent

class PerCameraResolution_PT_Main(bpy.types.Panel):
    bl_label = "Camera Resolution"
    bl_idname = "PerCameraResolution_PT_Main"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "data"

    @classmethod
    def poll(cls, context):
        return context.camera is not None

    def draw(self, context):
        layout = self.layout
        cam = context.camera

        layout.prop(cam, "use_custom_resolution", text="Enable Custom Resolution")

        if cam.use_custom_resolution:
            col = layout.column(align=True)
            col.prop(cam, "camera_res_x", text="Resolution X (px)")
            col.prop(cam, "camera_res_y", text="Resolution Y (px)")

@persistent
def depsgraph_update_handler(scene, depsgraph):
    cam = scene.camera
    if not cam:
        return
    cam = cam.data
    
    if getattr(cam, "use_custom_resolution", False):
        if scene.render.resolution_x != cam.camera_res_x:
            scene.render.resolution_x = cam.camera_res_x
        if scene.render.resolution_y != cam.camera_res_y:
            scene.render.resolution_y = cam.camera_res_y

def register():
    bpy.types.Camera.use_custom_resolution = bpy.props.BoolProperty(
        name="Use Custom Resolution",
        description="Override scene resolution when this camera is active",
        default=False,
    )
    bpy.types.Camera.camera_res_x = bpy.props.IntProperty(
        name="Resolution X",
        description="Horizontal resolution for this camera",
        default=1920,
        min=4,
        max=65536,
    )
    bpy.types.Camera.camera_res_y = bpy.props.IntProperty(
        name="Resolution Y",
        description="Vertical resolution for this camera",
        default=1080,
        min=4,
        max=65536,
    )
    bpy.utils.register_class(PerCameraResolution_PT_Main)
    if depsgraph_update_handler not in bpy.app.handlers.depsgraph_update_post:
        bpy.app.handlers.depsgraph_update_post.append(depsgraph_update_handler)

def unregister():
    if depsgraph_update_handler in bpy.app.handlers.depsgraph_update_post:
        bpy.app.handlers.depsgraph_update_post.remove(depsgraph_update_handler)
    bpy.utils.unregister_class(PerCameraResolution_PT_Main)
    del bpy.types.Camera.use_custom_resolution
    del bpy.types.Camera.camera_res_x
    del bpy.types.Camera.camera_res_y

if __name__ == "__main__":
    register()
