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


__author__ = "Nako"
__status__ = "production"
__version__ = "0.8"
__date__ = "14 June 2022"

bl_info = {
    "name": "Hair Arranger",
    "author": "Nako",
    "version": (0, 8),
    "blender": (2, 80, 0),
    "description": "Generate, modify and set anime-like hair",
    "doc_url": "TODO",
    "category": "Mesh",
}

# from . import properties
from . import operators
from . import ui_panel


def register():
    print("register HAIR ARRANGER")
    # properties.register()
    operators.register()
    ui_panel.register()


def unregister():
    print("unregister HAIR ARRANGER")
    ui_panel.unregister()
    operators.unregister()
    # properties.unregister()


if __name__ == '__main__':
    register()
