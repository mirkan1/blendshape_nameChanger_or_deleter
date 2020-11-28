#Ok cool ,lets start with simple blendshape tool that I need
#Can we add buttons to the UI?
#Functionality
#1. Delete all blendshapes
#2. Rename blendshapes - where I can enter searched substring and the desired substring to search with

#so if the shape key name - left_eye_brows_boom
#if the searched substring is "boom" and the desired is "zoom"
#everywhere you find boom should be replaced with zoom

bl_info = {
    "name": "Bmesh playground", 
    "author": "Mirkan(Raq)",
    "category": "3D View",
    "blender": (2, 80, 0),
    "description": "VIEW3D_PT_BmeshPlayground",
    "location": "View3D > Object",
    "warning": "",
    "wiki_url": "",
    "category": "Object",
    }
    
import bpy

#GUI
class Main_Panel(bpy.types.Panel):
    bl_label = "Bmesh playground"
    bl_idname = "VIEW3D_PT_BmeshPlayground"
    bl_description = "delete and rename meshes"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'BMESH PLAYGROUND'
    
    def draw(self, context):
        props = bpy.context.scene.Playground_QueryProps
        layout = self.layout
        
        # Main Operators/Basic
        row = layout.row()
        row.label(text="SUBSTRING:")
        row.label(text="DESIRED:")
        row = layout.row()
        row.prop(props, "search_prop", text="")
        row.prop(props, "rename_prop", text="")
        row = layout.row()
        row.operator("object.raname", text="Rename blendshapes")
        
        row = layout.row()
        row.label(text="DELETE ONLY SELECTED")
        row.prop(props, "check_button", text="")
        row = layout.row()
        row.operator("object.delete", text="Delete all blendshapes")
        
        
        
# Delete all blendshapes
class Delete_Blendshapes_OP(bpy.types.Operator):
    bl_idname = "object.delete"
    bl_label = "delete all objects or selected object"

    def execute(self, context):
        selected = bpy.context.scene.Playground_QueryProps.check_button
        if selected:
            try:
                object_to_delete = bpy.context.selected_objects[0]
                bpy.data.objects.remove(object_to_delete, do_unlink=True)
            except IndexError:
                self.report({"ERROR"}, "Object is not selected")
                return {"CANCELLED"}
        else:
            for i in bpy.data.objects:
                bpy.data.objects.remove(i, do_unlink=True)
                
            
        return {'FINISHED'}
    
# Rename blendshapes
class Rename_Blendshapes_OP(bpy.types.Operator):
    bl_idname = "object.raname"
    bl_label = "rename the sintax using regex"

    def execute(self, context):
        import re
        searched = bpy.context.scene.Playground_QueryProps.search_prop
        desired = bpy.context.scene.Playground_QueryProps.rename_prop
        for i in bpy.data.objects:
            r1 = re.findall(r"" + searched + ".*",i.name)
            print(r1)
            if len(r1) > 0:
                i.name = i.name.replace(searched, desired)
            #print(r1, searched, desired)
        return {'FINISHED'}

# Props
class Playground_QueryProps(bpy.types.PropertyGroup):        
    search_prop = bpy.props.StringProperty(default="")
    rename_prop = bpy.props.StringProperty(default="")
    check_button = bpy.props.BoolProperty()
    
    
classes = (
    Delete_Blendshapes_OP,
    Rename_Blendshapes_OP,
    Main_Panel,
    Playground_QueryProps,
)

def register():

    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)
    # Register QueryProps
    bpy.types.Scene.Playground_QueryProps = bpy.props.PointerProperty(type=Playground_QueryProps)


def unregister():

    from bpy.utils import unregister_class
    for cls in classes:
        unregister_class(cls)
    del(bpy.types.Scene.Playground_QueryProps)

if __name__ == "__main__":
    register();