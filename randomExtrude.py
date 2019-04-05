import bpy
import bmesh
from mathutils import Vector
from bmesh.types import BMVert
import random

bl_info = {"name": "Random Facial Extrusion Add-on", "category": "Mesh", "author": "Jake Costen", "blender": (2, 80, 0)}

class MeshRandomExtrude(bpy.types.Operator):
    """Extrude each face of an object a random distance."""      # Use this as a tooltip for menu items and buttons.
    bl_idname = "mesh.extrude_random"        # Unique identifier for buttons and menu items to reference.
    bl_label = "Extrude all faces a random distance"         # Display name in the interface.
    bl_options = {'REGISTER', 'UNDO'}

    RANDOM_MAX = bpy.props.IntProperty(name="Maximum extrude distance", default = 5, min = 2)
    RANDOM_MIN = bpy.props.IntProperty(name="Minimum extrude distance", default = 1, min = 1)
    RANDOM_MULTIPLIER = bpy.props.FloatProperty(name="Distance multiplier", default = 0.3, min = 0.005)
    
    def execute(self, context):
        if (self.RANDOM_MAX < self.RANDOM_MIN):
            return {'FAILED'}
        
        obj = bpy.context.view_layer.objects.active
        bpy.ops.object.editmode_toggle()
        me = obj.data
        bm = bmesh.from_edit_mesh(me)
        bm.faces.ensure_lookup_table()

        numFaces = len (bm.faces)
        for i in range (numFaces):
            newG = bmesh.ops.extrude_face_region (bm, geom=[bm.faces[i]], use_keep_orig=False)
            bmesh.ops.translate(bm, vec=Vector((0.0,0.0,random.randint(self.RANDOM_MIN,self.RANDOM_MAX)*self.RANDOM_MULTIPLIER)), verts=[v for v in newG['geom'] if isinstance(v, BMVert)])
            bm.faces.ensure_lookup_table()
    
        bmesh.update_edit_mesh(me, True)
        bpy.ops.object.editmode_toggle()
        
        return {'FINISHED'}
    
    
def menu_func (self, context):
    self.layout.operator(MeshRandomExtrude.bl_idname)
    
def register():
    bpy.utils.register_class(MeshRandomExtrude)
    bpy.types.VIEW3D_MT_object.append(menu_func)


def unregister():
    bpy.utils.unregister_class(MeshRandomExtrude)
    
if __name__ == "__main__":
    register()