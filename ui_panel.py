# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

import bpy
from bpy.types import Panel


# Panels
class HAIR_ARRANGER_PT_pre_panel(bpy.types.Panel):
    bl_label = 'Hair Arranger'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Hair Arranger'

    @classmethod
    def poll(cls, context):
         return not bpy.context.object or bpy.context.object.type not in ['MESH', 'CURVE']

    def draw(self, context):
        col = self.layout.column(align=True)
        col.label(text='Select mesh to arrange hair')


class HAIR_ARRANGER_PT_start_panel(bpy.types.Panel):
    bl_label = 'Hair Arranger'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Hair Arranger'

    @classmethod
    def poll(cls, context):
        return bpy.context.object and bpy.context.object.type == 'MESH'

    def draw(self, context):
        self.layout.column(align=True)
        self.layout.operator('hair_arranger.start',
                             text='Start')


class HAIR_ARRANGER_PT_start_arrange_panel(bpy.types.Panel):
    bl_label = 'Hair Arranger'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Hair Arranger'

    @classmethod
    def poll(cls, context):
        return bpy.context.object and bpy.context.object.type == 'CURVE' and bpy.context.object.mode != 'EDIT'

    def draw(self, context):
        self.layout.column(align=True)
        self.layout.operator('hair_arranger.start_arrange', text='Arrange')


class HAIR_ARRANGER_PT_arrange_panel(bpy.types.Panel):
    bl_label = 'Hair Arranger'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Hair Arranger'

    @classmethod
    def poll(cls, context):
        return bpy.context.object and bpy.context.object.type == 'CURVE' and bpy.context.object.mode == 'EDIT'

    def draw(self, context):
        row = self.layout.row()
        row.prop(bpy.context.scene.tool_settings, 'use_snap', text='Use Snap')
        row = self.layout.row()
        row.prop(bpy.context.scene.tool_settings.curve_paint_settings, 'use_stroke_endpoints', text='Snap Only First')
        row = self.layout.row()
        row.prop(bpy.context.scene.tool_settings.curve_paint_settings, 'surface_plane', text='Surface')

        box = self.layout.box()
        row = box.row(align=True)
        col = row.column(align=True)
        col.prop(bpy.context.scene.tool_settings.curve_paint_settings, 'surface_offset', text='offset',
                 slider=True)
        col.prop(bpy.context.scene.tool_settings.curve_paint_settings, 'radius_taper_start', text='Taper start',
                 slider=True)
        col.prop(bpy.context.scene.tool_settings.curve_paint_settings, 'radius_taper_end', text='Taper end',
                 slider=True)

        box = self.layout.box()
        col = box.column(align=True)
        col.prop(bpy.context.object.data, "bevel_depth", text="Radius")
        col.prop(bpy.context.object.data, "resolution_u", text="Resolution U")
        col.prop(bpy.context.object.data, "bevel_resolution", text="Resolution Bevel")
        col.prop(bpy.context.object.data, "bevel_factor_start", text="Bevel Start")
        col.prop(bpy.context.object.data, "bevel_factor_end", text="Bevel End")
        col.prop(bpy.context.object.data, "bevel_object", text="Object")

        box = self.layout.box()
        col = box.column(align=True)
        col.operator("hair_arranger.select_points", text="Select Spline")
        col.operator("hair_arranger.select_all", text="Select All Spline")
        row = col.row(align=True)
        row.operator("hair_arranger.select_all_starts", text="Select Starts")
        row.operator("hair_arranger.select_all_ends", text="Select Ends")

        box = self.layout.box()
        col = box.column()
        col.operator("hair_arranger.convert_to_nurbs", text="Convert to NURBS")
        col.operator("hair_arranger.remove_end_points", text="Remove End Points")


classes = [HAIR_ARRANGER_PT_pre_panel, HAIR_ARRANGER_PT_start_panel,
           HAIR_ARRANGER_PT_arrange_panel, HAIR_ARRANGER_PT_start_arrange_panel]


def register():
    for c in classes:
        bpy.utils.register_class(c)


def unregister():
    for c in classes:
        bpy.utils.unregister_class(c)


if __name__ == '__main__':
    register()
