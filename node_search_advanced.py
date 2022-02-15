# MIT License
#
# Copyright (c) 2021 Lukas Toenne
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import bpy
from bpy.props import *


class AdvancedNodeSearchSettings(bpy.types.PropertyGroup):
    include_node_groups: BoolProperty(
        name="Include Node Groups",
        description="Include node groups in search results",
        default=True,
    )


class AdvancedNodeSearchResult(bpy.types.PropertyGroup):
    node_tree: PointerProperty(
        type=bpy.types.NodeTree,
        name="Node Tree",
        description="Node tree that contains the item",
    )


class AdvancedNodeSearch(bpy.types.PropertyGroup):
    def search_term_update(self, context):
        if self.search_term:
            bpy.ops.dynamic_nodes.advanced_search(search_term=self.search_term)

    search_term: StringProperty(
        name="Search Term",
        update=search_term_update,
    )

    search_settings: PointerProperty(
        type=AdvancedNodeSearchSettings,
        name="Search Settings",
    )

    search_results: CollectionProperty(
        type=AdvancedNodeSearchResult,
        name="Search Results",
    )

    active_search_result_index: IntProperty(
        name="Active Search Result Index",
        default=-1,
    )


class AdvancedNodeSearchOperator(bpy.types.Operator):
    """Search in node data blocks."""
    bl_idname = 'dynamic_nodes.advanced_search'
    bl_label = 'Advanced Search'
    bl_options = {'REGISTER'}

    search_term: StringProperty(
        name="Search Term",
    )

    def execute(self, context):
        print(f"Search: {self.search_term}")
        return {'FINISHED'}


class AdvancedNodePanel:
    @classmethod
    def poll(cls, context):
        space = context.space_data
        return space.type == 'NODE_EDITOR' and space.node_tree is not None


class AdvancedNodeSearchPanel(bpy.types.Panel, AdvancedNodePanel):
    """Node search with advanced usability features"""
    bl_label = "Search"
    bl_idname = "DYNAMIC_NODES_PT_advanced_search"
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_category = "Advanced Search"

    def draw(self, context):
        layout = self.layout
        ntree = context.space_data.node_tree
        data = ntree.advanced_search

        layout.prop(data, "search_term")
        props = layout.operator(AdvancedNodeSearchOperator.bl_idname)
        props.search_term = data.search_term

        settings = data.search_settings
        layout.prop(settings, "include_node_groups")


class AdvancedNodeSearchResultsList(bpy.types.UIList):
    bl_idname = "DYNAMIC_NODES_UL_advanced_search_result_list"

    def draw_item(self, context, layout, data, item, icon, active_data, active_propname):
        prefs = data
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            layout.prop(item.node_tree, "node_tree", text="", emboss=False, icon_value=icon)
        elif self.layout_type in {'GRID'}:
            layout.alignment = 'CENTER'
            layout.label(text="", icon_value=icon)


class AdvancedNodeSearchResultsPanel(bpy.types.Panel, AdvancedNodePanel):
    """Node search results"""
    bl_label = "Results"
    bl_idname = "DYNAMIC_NODES_PT_advanced_search_results"
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_category = "Advanced Search"

    def draw(self, context):
        layout = self.layout
        ntree = context.space_data.node_tree
        data = ntree.advanced_search

        layout.template_list(AdvancedNodeSearchResultsList.bl_idname, "", data, "search_results", data, "active_search_result_index")


def register():
    bpy.utils.register_class(AdvancedNodeSearchSettings)
    bpy.utils.register_class(AdvancedNodeSearchResult)
    bpy.utils.register_class(AdvancedNodeSearch)
    bpy.types.NodeTree.advanced_search = PointerProperty(
        type=AdvancedNodeSearch,
        name="Advanced Search",
    )

    bpy.utils.register_class(AdvancedNodeSearchOperator)
    bpy.utils.register_class(AdvancedNodeSearchPanel)
    bpy.utils.register_class(AdvancedNodeSearchResultsList)
    bpy.utils.register_class(AdvancedNodeSearchResultsPanel)


def unregister():
    bpy.utils.unregister_class(AdvancedNodeSearchSettings)
    bpy.utils.unregister_class(AdvancedNodeSearchResult)
    bpy.utils.unregister_class(AdvancedNodeSearch)
    del bpy.types.NodeTree.advanced_search

    bpy.utils.unregister_class(AdvancedNodeSearchOperator)
    bpy.utils.unregister_class(AdvancedNodeSearchPanel)
    bpy.utils.unregister_class(AdvancedNodeSearchResultsList)
    bpy.utils.unregister_class(AdvancedNodeSearchResultsPanel)
