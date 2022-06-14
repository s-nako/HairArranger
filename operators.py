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
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

import bpy
from bpy.types import Operator


class HAIR_ARRANGER_OT_start(bpy.types.Operator):
    bl_idname = "hair_arranger.start"
    bl_label = "Start hair arranger"

    @classmethod
    def poll(cls, context):
        return context.area.type == 'VIEW_3D'

    def execute(self, context):
        obj = bpy.context.object
        if not obj:
            return

        # Start draw
        bpy.ops.curve.primitive_bezier_curve_add()
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.curve.delete(type='VERT')  # Delete default vertices of generated curve

        # Set draw tool as active
        for area in bpy.context.screen.areas:
            if area.type == "VIEW_3D":
                override = bpy.context.copy()
                bpy.ops.wm.tool_set_by_id(override, name="builtin.draw")

        # Set snapping on (off at end)
        bpy.context.scene.tool_settings.snap_elements = {'FACE'}
        bpy.context.scene.tool_settings.use_snap_self = False
        bpy.context.scene.tool_settings.use_snap = True

        # tool setting
        bpy.context.scene.tool_settings.curve_paint_settings.error_threshold = 8  # "Tolerance"
        bpy.context.scene.tool_settings.curve_paint_settings.use_corners_detect = True
        bpy.context.scene.tool_settings.curve_paint_settings.corner_angle = 1.22173  # 70 degree
        bpy.context.scene.tool_settings.curve_paint_settings.radius_taper_end = 0.0
        bpy.context.scene.tool_settings.curve_paint_settings.radius_taper_start = 0.0
        bpy.context.scene.tool_settings.curve_paint_settings.radius_max = 1
        bpy.context.scene.tool_settings.curve_paint_settings.depth_mode = 'SURFACE'
        bpy.context.scene.tool_settings.curve_paint_settings.surface_offset = 0
        bpy.context.scene.tool_settings.curve_paint_settings.use_stroke_endpoints = True
        bpy.context.scene.tool_settings.curve_paint_settings.surface_plane = 'NORMAL_VIEW'

        # object setting
        bpy.context.object.data.dimensions = '3D'
        bpy.context.object.data.resolution_u = 8
        bpy.context.object.data.twist_mode = 'MINIMUM'
        bpy.context.object.data.fill_mode = 'FULL'
        bpy.context.object.data.offset = 0
        bpy.context.object.data.bevel_depth = 1.0 / 25
        bpy.context.object.data.bevel_resolution = 4
        bpy.context.object.data.bevel_object = None
        bpy.context.object.data.bevel_factor_start = 0
        bpy.context.object.data.bevel_factor_end = 1

        return {'FINISHED'}


class HAIR_ARRANGER_OT_select_all(bpy.types.Operator):
    bl_idname = "hair_arranger.select_all"
    bl_label = "Start hair arranger"

    @classmethod
    def poll(cls, context):
        return context.area.type == 'VIEW_3D'

    def execute(self, context):
        bpy.ops.curve.select_all(action='SELECT')
        return {'FINISHED'}

class HAIR_ARRANGER_OT_select_all_starts(bpy.types.Operator):
    bl_idname = "hair_arranger.select_all_starts"
    bl_label = "Start hair arranger"

    @classmethod
    def poll(cls, context):
        return context.area.type == 'VIEW_3D'

    def execute(self, context):
        bpy.ops.curve.select_all(action='DESELECT')
        splines = bpy.context.object.data.splines
        for s in splines:
            s.bezier_points[0].select_control_point = True
        return {'FINISHED'}

class HAIR_ARRANGER_OT_select_all_ends(bpy.types.Operator):
    bl_idname = "hair_arranger.select_all_ends"
    bl_label = "Start hair arranger"

    @classmethod
    def poll(cls, context):
        return context.area.type == 'VIEW_3D'

    def execute(self, context):
        bpy.ops.curve.select_all(action='DESELECT')
        splines = bpy.context.object.data.splines
        for s in splines:
            s.bezier_points[-1].select_control_point = True
        return {'FINISHED'}


classes = [HAIR_ARRANGER_OT_start, HAIR_ARRANGER_OT_select_all,
           HAIR_ARRANGER_OT_select_all_ends, HAIR_ARRANGER_OT_select_all_starts]


def register():
    for c in classes:
        bpy.utils.register_class(c)


def unregister():
    for c in classes:
        bpy.utils.unregister_class(c)


if __name__ == '__main__':
    register()
