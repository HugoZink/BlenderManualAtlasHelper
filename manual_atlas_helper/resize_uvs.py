import bpy

def get_materials(ob):
    return [mat_slot.material for mat_slot in ob.material_slots]


def get_texture(mat):
    return next((mat.texture_slots[slot_idx].texture for slot_idx in range(len(mat.texture_slots))
                 if (mat.texture_slots[slot_idx] is not None) and mat.use_textures[slot_idx]), None)            

#Scale a 2D vector v, considering a scale s and a pivot point p
def Scale2D( v, s, p ):
    return ( p[0] + s[0]*(v[0] - p[0]), p[1] + s[1]*(v[1] - p[1]) )     

#Scale a UV map iterating over its coordinates to a given scale and with a pivot point
def ScaleUV( uvMap, scale, pivot ):
    for uvIndex in range( len(uvMap.data) ):
        uvMap.data[uvIndex].uv = Scale2D( uvMap.data[uvIndex].uv, scale, pivot )

def perform_uv_resize(mesh, atlas_width, atlas_height, size_mul):
    original_area = bpy.context.area.type

    for num, mat in enumerate(get_materials(mesh)):
        # determine texture size for current mat
        # TODO: get *all* textures and determine the largest among them. Nobody really puts toon textures or matcaps first in the list, but what if they do?
        tex = get_texture(mat)
        
        # dont scale materials that have no texture or no image
        # TODO: these are probably solid colored and should be scaled to something absurdly small, possibly re-unwrapped too.
        if not tex:
            continue
        
        image = tex.image
        
        if not image:
            continue
        
        width, height = image.size
        
        # get the right scale to keep the UVs original relative size
        # size_mul (default 1.1x) is used because usually, atlasing by baking the textures is not a lossless ordeal if the UVs arent *slightly* larger than they have to be.
        scaleMultiplierX = (width / atlas_width) * size_mul
        scaleMultiplierY = (height / atlas_height) * size_mul
        
        # Remember current window type
        windowType = bpy.context.area.type
        
        # set image editor and edit mode
        bpy.context.area.type = 'IMAGE_EDITOR'
        bpy.ops.object.mode_set(mode='EDIT', toggle=False)
        
        # deselect all first
        bpy.ops.mesh.reveal()
        bpy.ops.mesh.select_all(action='DESELECT')
        
        # select material
        bpy.context.object.active_material_index = num
        bpy.ops.object.material_slot_select()
        
        # select all UVs
        bpy.ops.uv.select_all(action='DESELECT')
        bpy.ops.uv.select_all(action='SELECT')
        
        # Scale uvs
        bpy.ops.transform.resize(value=(scaleMultiplierX, scaleMultiplierY, 1), constraint_axis=(False, False, False))
        bpy.ops.uv.select_all(action='DESELECT')
        
        # Go back to last window type
        bpy.context.area.type = windowType;
