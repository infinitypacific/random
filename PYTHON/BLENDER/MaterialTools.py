bl_info = {
    "name": "MaterialTools",
    "description": "Sets all image texture nodes in selected objects to a chosen interpolation mode.",
    "author": "Frostbyte",
    "version": (1, 2),
    "blender": (2, 80, 0),
    "location": "View3D > Object Menu",
    "category": "Material",
}

import bpy

class MATERIALTOOLS_OT_set_image_interpolation(bpy.types.Operator):
    bl_idname = "materialtools.set_image_interpolation"
    bl_label = "Set Image Interpolation"
    bl_options = {'REGISTER', 'UNDO'}

    interpolation_mode: bpy.props.EnumProperty(
        name="Mode",
        description="Interpolation method to set",
        items=[
            ('Linear', "Linear", "Bilinear interpolation"),
            ('Closest', "Closest", "No interpolation (nearest neighbor)"),
            ('Cubic', "Cubic", "Cubic interpolation"),
            ('Smart', "Smart", "Smart interpolation"),
        ],
        default='Linear'
    )

    @classmethod
    def poll(cls, context):
        return context.selected_objects

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def execute(self, context):
        updated_nodes = 0

        for obj in context.selected_objects:
            if not hasattr(obj, 'material_slots'):
                continue

            for slot in obj.material_slots:
                mat = slot.material
                if mat and mat.use_nodes:
                    for node in mat.node_tree.nodes:
                        if node.type == 'TEX_IMAGE':
                            if node.interpolation != self.interpolation_mode:
                                node.interpolation = self.interpolation_mode
                                updated_nodes += 1

        self.report({'INFO'}, f"Updated {updated_nodes} image node(s) to {self.interpolation_mode} interpolation.")
        return {'FINISHED'}

def draw_menu(self, context):
    self.layout.separator()
    self.layout.operator(MATERIALTOOLS_OT_set_image_interpolation.bl_idname, icon='SHADING_TEXTURE')

def register():
    bpy.utils.register_class(MATERIALTOOLS_OT_set_image_interpolation)
    bpy.types.VIEW3D_MT_object.append(draw_menu)

def unregister():
    bpy.utils.unregister_class(MATERIALTOOLS_OT_set_image_interpolation)
    bpy.types.VIEW3D_MT_object.remove(draw_menu)

if __name__ == "__main__":
    register()