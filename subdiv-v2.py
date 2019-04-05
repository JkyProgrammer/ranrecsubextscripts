import bpy
import bmesh
import random

bl_info = {"name": "Random Recursive Subdivision Add-on", "category": "Mesh", "author": "Jake Costen", "blender": (2, 80, 0)}

class MeshAddRandomRecursiveSubdividedPlane(bpy.types.Operator):
    """Construct a plane with random recursive subdivisions."""
    bl_idname = "mesh.add_random_recursive_subdivided_plane"
    bl_label = "Plane with random recursive subdivisions"
    bl_options = {'REGISTER', 'UNDO'}  # Enable undo for the operator.
    MAX_SUBDIV_LEVELS = bpy.props.IntProperty(name="Maximum subdivision level", default=4, min=4, max=10)
    SUBDIV_TRIES = bpy.props.IntProperty(name="Number of subdivision attempts", default=10, min=2, max=100)
    POSITION = bpy.props.FloatVectorProperty (name="Location")
    RADIUS = bpy.props.FloatProperty (name="Radius", default=1.0)
    
    def execute(self, context):
        
        bpy.ops.mesh.primitive_plane_add (size=self.RADIUS*2, enter_editmode=True, location=self.POSITION)

        obj = context.edit_object
        me = obj.data
        bm = bmesh.from_edit_mesh(me)
        bm.faces.ensure_lookup_table()

        FACE_AREA_MIN = (bm.faces[0].calc_area())/(4 ** self.MAX_SUBDIV_LEVELS)
        print (FACE_AREA_MIN)


        tries = self.SUBDIV_TRIES
        while tries > 0:
            face = bm.faces[random.randint (0, len (bm.faces)-1)]
            if (face.calc_area()/4 >= FACE_AREA_MIN):
                bmesh.ops.subdivide_edges(bm, edges=face.edges, use_grid_fill=True, cuts=1)
                bm.faces.ensure_lookup_table()
                bmesh.ops.split_edges(bm, edges=bm.edges)
                tries -= 1
                
        bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=0.000001)
        bmesh.update_edit_mesh(me, True)
        bpy.ops.object.editmode_toggle()

        return {'FINISHED'}            # Lets Blender know the operator finished successfully.

        def invoke(self, context, event):
                self.POSITION = bpy.props.FloatVectorProperty (name="Location", default=bpy.context.scene.cursor_location)
                return self.execute(context)

def menu_func(self, context):
    self.layout.operator(MeshAddRandomRecursiveSubdividedPlane.bl_idname)

def register():
    bpy.utils.register_class(MeshAddRandomRecursiveSubdividedPlane)
    bpy.types.VIEW3D_MT_add.append(menu_func)


def unregister():
    bpy.utils.unregister_class(MeshAddRandomRecursiveSubdividedPlane)
    
if __name__ == "__main__":
    register()