bl_info = {
    'name': "Rokk's Manual Atlas Helper",
    'description': 'Utilities for helping with manual texture atlasing.',
    'author': 'shotariya',
    'version': (1, 0, 0, 0),
    'blender': (2, 79, 0),
    'location': 'View3D > Tool Shelf > Manual Atlas',
    'warning': '',
    'category': 'UV'
}

import bpy
from .resize_uvs import *
from bpy.types import PropertyGroup

def get_all_meshes(self, context):
    meshes = []

    for ob in context.scene.objects:
        if ob.type == 'MESH':
            meshes.append((ob.name, ob.name, ob.name))

    return meshes

class AtlasHelperPropertyGroup(PropertyGroup):

    atlas_resolution_x = bpy.props.EnumProperty(
        name="Atlas Width",
        items=[
            ('64', '64', ''),
            ('128', '128', ''),
            ('256', '256', ''),
            ('512', '512', ''),
            ('1024', '1024', ''),
            ('2048', '2048', ''),
            ('4096', '4096', ''),
            ('8192', '8192', 'This resolution is quite high.'),
            ('16384', '16384', 'This resolution is unusable in Unity!')
        ]
    )
    
    atlas_resolution_y = bpy.props.EnumProperty(
        name="Atlas Height",
        items=[
            ('64', '64', ''),
            ('128', '128', ''),
            ('256', '256', ''),
            ('512', '512', ''),
            ('1024', '1024', ''),
            ('2048', '2048', ''),
            ('4096', '4096', ''),
            ('8192', '8192', 'This resolution is quite high.'),
            ('16384', '16384', 'This resolution is unusable in Unity!')
        ]
    )

    size_multiplier = bpy.props.FloatProperty(
        name="Size Multiplier",
        default=1.1,
        step=1,
        min = 0
        )

    mesh_to_resize = bpy.props.EnumProperty(
            name="Select Mesh",
            items=get_all_meshes)


class ShelfPanel(bpy.types.Panel):
    bl_label = 'Rokks Manual Atlasing Helper'
    bl_idname = '3D_VIEW_ATLAS_HELPER'
    bl_category = 'ManualAtlasHelper'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = 'Manual Atlas'

    def draw(self, context):
        scene = context.scene
        layout = self.layout
        props = context.scene.AtlasHelperPropertyGroup

        col = layout.column()
        col = col.column(align=True)
        col.label('Select mesh to perform automatic UV resize on:')
        row = col.row()
        row.prop(props, 'mesh_to_resize', text='Mesh')
        row = col.row()
        row.prop(props, 'atlas_resolution_x')
        row = col.row()
        row.prop(props, 'atlas_resolution_y')
        row = col.row()
        row.prop(props, 'size_multiplier')
        row = col.row()
        row.operator('uv.atlashelper_resize', text="Resize UV's!")


class UvResizer(bpy.types.Operator):
    """Perform UV Resize"""
    bl_idname = "uv.atlashelper_resize"
    bl_label = "Resize UV's for atlas"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        props = context.scene.AtlasHelperPropertyGroup
        atlas_width = props.atlas_resolution_x
        atlas_height = props.atlas_resolution_y
        size_mul = props.size_multiplier
        mesh_name = props.mesh_to_resize
        mesh = bpy.data.objects.get(mesh_name)

        perform_uv_resize(mesh, int(atlas_width), int(atlas_height), float(size_mul))

        return {'FINISHED'}


class ObjectMoveX(bpy.types.Operator):
    """My Object Moving Script"""      # Use this as a tooltip for menu items and buttons.
    bl_idname = "object.move_x"        # Unique identifier for buttons and menu items to reference.
    bl_label = "Move X by One"         # Display name in the interface.
    bl_options = {'REGISTER', 'UNDO'}  # Enable undo for the operator.

    def execute(self, context):        # execute() is called when running the operator.

        # The original script
        scene = context.scene
        for obj in scene.objects:
            obj.location.x += 1.0

        return {'FINISHED'}            # Lets Blender know the operator finished successfully.


def register():
    bpy.utils.register_class(ObjectMoveX)
    bpy.utils.register_class(ShelfPanel)
    bpy.utils.register_class(UvResizer)
    bpy.utils.register_class(AtlasHelperPropertyGroup)

    bpy.types.Scene.AtlasHelperPropertyGroup = bpy.props.PointerProperty(type=AtlasHelperPropertyGroup)


def unregister():
    bpy.utils.unregister_class(ObjectMoveX)
    bpy.utils.unregister_class(ShelfPanel)
    bpy.utils.unregister_class(UvResizer)
    bpy.utils.unregister_class(AtlasHelperPropertyGroup)

    del bpy.types.Scene.AtlasHelperPropertyGroup
