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

import os

import bpy
from bpy.types import Operator

FILE_NAME = "hair_curves.blend"
HAIR_CURVE_COLLECTION = "HairCurveSamples"
ROOT_NAME = "haircurves"


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

        if ROOT_NAME not in bpy.data.objects:
            _append_spline_curves(obj)

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


def _append_spline_curves(obj):
    hair_arranger_dir = os.path.split(__file__)[0]
    bpy.ops.wm.append(filename=HAIR_CURVE_COLLECTION,
                      filepath=os.path.join(hair_arranger_dir, FILE_NAME,
                                            "Collection", HAIR_CURVE_COLLECTION),
                      directory=os.path.join(hair_arranger_dir, "hair_curves.blend", "Collection"))
    # generate root
    root = bpy.data.objects.new(ROOT_NAME, None)
    bpy.context.scene.collection.objects.link(root)

    x = obj.location.x + obj.dimensions.x * 3 / 5
    z = obj.location.z + obj.dimensions.z / 2
    root.empty_display_size = 0.1
    root.location = (x, 0.0, z)
    for i in range(3):
        root.lock_rotation[i] = True
        root.lock_scale[i] = True

    for curve in bpy.data.collections[HAIR_CURVE_COLLECTION].objects:
        if not curve.name.startswith("haircurve"):
            continue
        curve.parent = root
        curve.scale = (0.1, 0.1, 0.1)
        bpy.data.collections[HAIR_CURVE_COLLECTION].objects.unlink(curve)
        bpy.context.scene.collection.objects.link(curve)

    bpy.data.collections.remove(bpy.data.collections[HAIR_CURVE_COLLECTION])


class HAIR_ARRANGER_OT_start_arrange(bpy.types.Operator):
    bl_idname = "hair_arranger.start_arrange"
    bl_label = "Start hair arranger"

    @classmethod
    def poll(cls, context):
        return context.area.type == 'VIEW_3D'

    def execute(self, context):
        bpy.ops.object.editmode_toggle()
        return {'FINISHED'}


class HAIR_ARRANGER_OT_select_points(bpy.types.Operator):
    bl_idname = "hair_arranger.select_points"
    bl_label = "Start hair arranger"

    @classmethod
    def poll(cls, context):
        return context.area.type == 'VIEW_3D'

    def execute(self, context):
        selected_splines = _get_selected_curves()
        print("selected_splines", selected_splines)
        bpy.ops.curve.select_all(action='DESELECT')
        for s in selected_splines:
            if s.type == "BEZIER":
                for p in s.bezier_points:
                    p.select_control_point = True
            else:
                for p in s.points:
                    p.select = True
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
            if s.type == "BEZIER":
                s.bezier_points[0].select_control_point = True
            else:
                s.points[0].select = True
        return {'FINISHED'}


class HAIR_ARRANGER_OT_select_all_middles(bpy.types.Operator):
    bl_idname = "hair_arranger.select_all_middles"
    bl_label = "Start hair arranger"

    @classmethod
    def poll(cls, context):
        return context.area.type == 'VIEW_3D'

    def execute(self, context):
        bpy.ops.curve.select_all(action='DESELECT')
        splines = bpy.context.object.data.splines
        for s in splines:
            if s.type == "BEZIER" and len(s.bezier_points) > 1:
                for p in s.bezier_points[1:-1]:
                    p.select_control_point = True
            elif len(s.points) > 1:
                for p in s.points[1:-1]:
                    p.select = True
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
            if s.type == "BEZIER":
                s.bezier_points[-1].select_control_point = True
            else:
                s.points[-1].select = True

        return {'FINISHED'}


class HAIR_ARRANGER_OT_convert_to_nurbs(bpy.types.Operator):
    bl_idname = "hair_arranger.convert_to_nurbs"
    bl_label = "Start hair arranger"

    @classmethod
    def poll(cls, context):
        return context.area.type == 'VIEW_3D'

    def execute(self, context):
        bpy.ops.curve.spline_type_set(type='NURBS', use_handles=True)
        return {'FINISHED'}


class HAIR_ARRANGER_OT_remove_end_points(bpy.types.Operator):
    bl_idname = "hair_arranger.remove_end_points"
    bl_label = "Start hair arranger"

    @classmethod
    def poll(cls, context):
        return context.area.type == 'VIEW_3D'

    def execute(self, context):
        selected_splines = _get_selected_curves()

        bpy.ops.curve.select_all(action='DESELECT')
        for s in selected_splines:
            pt = s.points[0]
            pt.select = True
            pt = s.points[-1]
            pt.select = True
            bpy.ops.curve.delete(type='VERT')

            s.use_bezier_u = False
            s.use_endpoint_u = True

        return {'FINISHED'}


def _get_selected_curves():
    splines = bpy.context.object.data.splines
    selected_splines = []
    for s in splines:
        if s.type == "BEZIER":
            for p in s.bezier_points:
                if p.select_control_point or p.select_left_handle or p.select_right_handle:
                    selected_splines.append(s)
                    break
        else:
            for p in s.points:
                if p.select:
                    selected_splines.append(s)
                    break
    return selected_splines


class HAIR_ARRANGER_OT_separate_curves(bpy.types.Operator):
    bl_idname = "hair_arranger.separate_curves"
    bl_label = "Start hair arranger"

    @classmethod
    def poll(cls, context):
        return context.area.type == 'VIEW_3D'

    def execute(self, context):
        selected_splines = _get_selected_curves()
        _separate_each_splines(selected_splines)

        if selected_splines:
            bpy.ops.object.mode_set(mode='OBJECT')
            bpy.ops.object.move_to_collection(collection_index=0, is_new=True,
                                              new_collection_name="separated_haircurves")
        return {'FINISHED'}


def _separate_each_splines(splines):
    _separate_splines_main(splines)

    selected_objects = bpy.context.selected_objects
    if selected_objects and len(selected_objects) > 1:
        generated_curve = bpy.context.selected_objects[1]
        _separate_splines_itr(generated_curve)


def _separate_splines_itr(curve):
    bpy.context.view_layer.objects.active = curve
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.curve.select_all(action='DESELECT')
    splines = bpy.context.object.data.splines
    if len(splines) > 1:
        _separate_splines_main(splines[:-1])
    else:
        return

    selected_objects = bpy.context.selected_objects
    for selected_obj in selected_objects:
        if selected_obj.name != bpy.context.object.name:
            _separate_splines_itr(selected_obj)


def _separate_splines_main(splines):
    for s in splines:
        print("s", s)
        if s.type == "BEZIER":
            points = s.bezier_points
            for p in points:
                p.select_control_point = True
        else:
            points = s.points
            for p in points:
                p.select = True
    if splines:
        bpy.ops.curve.separate()


class HAIR_ARRANGER_OT_convert_to_mesh(bpy.types.Operator):
    bl_idname = "hair_arranger.convert_to_mesh"
    bl_label = "Start hair arranger"

    @classmethod
    def poll(cls, context):
        return context.area.type == 'VIEW_3D'

    def execute(self, context):
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.convert(target='MESH')

        bpy.ops.object.shade_smooth()
        bpy.ops.object.mode_set(mode='EDIT')

        return {'FINISHED'}


classes = [HAIR_ARRANGER_OT_start, HAIR_ARRANGER_OT_start_arrange,
           HAIR_ARRANGER_OT_select_points, HAIR_ARRANGER_OT_select_all,
           HAIR_ARRANGER_OT_select_all_ends, HAIR_ARRANGER_OT_select_all_middles, HAIR_ARRANGER_OT_select_all_starts,
           HAIR_ARRANGER_OT_convert_to_nurbs, HAIR_ARRANGER_OT_remove_end_points,
           HAIR_ARRANGER_OT_separate_curves,
           HAIR_ARRANGER_OT_convert_to_mesh]


def register():
    for c in classes:
        bpy.utils.register_class(c)


def unregister():
    for c in classes:
        bpy.utils.unregister_class(c)


if __name__ == '__main__':
    register()
