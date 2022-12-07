from header_common import *
from header_operations import *
from header_triggers import *
from header_scenes import *
from module_constants import *

# #######################################################################
#
#	("scene_id", flags, "mesh_name", "collision_mesh", (min_x, min_y), (max_x, max_y), water_level, "terrain_string", [], [chest_troops], "outer_terrain_mesh"),
#
#  Each scene record contains the following fields:
#  1) Scene id {string}: used for referencing scenes in other files. The prefix scn_ is automatically added before each scene-id.
#  2) Scene flags {int}. See header_scenes.py for a list of available flags
#  3) Mesh name {string}: This is used for indoor scenes only. Use the keyword "none" for outdoor scenes.
#  4) Body name {string}: This is used for indoor scenes only. Use the keyword "none" for outdoor scenes.
#  5) Min-pos {(float,float)}: minimum (x,y) coordinate. Player can't move beyond this limit.
#  6) Max-pos {(float,float)}: maximum (x,y) coordinate. Player can't move beyond this limit.
#  7) Water-level {float}. 
#  8) Terrain code {string}: You can obtain the terrain code by copying it from the terrain generator screen
#  9) List of other scenes accessible from this scene {list of strings}.
#     (deprecated. This will probably be removed in future versions of the module system)
#     (In the new system passages are used to travel between scenes and
#     the passage's variation-no is used to select the game menu item that the passage leads to.)
# 10) List of chest-troops used in this scene {list of strings}. You can access chests by placing them in edit mode.
#     The chest's variation-no is used with this list for selecting which troop's inventory it will access.
# 11) OPTIONAL: Outer terrain mesh id (string)
# #######################################################################

scenes = [

    # #######################################################################
	# 		These are summoned by the engine in specific cases.
	# #######################################################################
	
  ("random_scene", sf_generate|sf_randomize|sf_auto_entry_points, "none", "none", (0, 0), (240, 240), -0.5,"0x300028000003e8fa0000034e00004b34000059be",
    [], []),
  ("conversation_scene", 0, "encounter_spot", "bo_encounter_spot", (-40, -40),(40, 40), -100, "0",
    [], []),
  ("water", 0, "none", "none", (-1000, -1000), (1000, 1000), -0.5, "0", [], []),
  ("random_scene_steppe", sf_generate|sf_randomize|sf_auto_entry_points, "none", "none", (0, 0),(240, 240),-0.5, "0x0000000229602800000691a400003efe00004b34000059be",
    [], [], "outer_terrain_steppe"),
  ("random_scene_plain", sf_generate|sf_randomize|sf_auto_entry_points, "none", "none", (0, 0), (240, 240), -0.5, "0x0000000229602800000691a400003efe00004b34000059be",
    [], [], "outer_terrain_plain"),
  ("random_scene_snow", sf_generate|sf_randomize|sf_auto_entry_points, "none", "none", (0, 0), (240, 240), -0.5, "0x0000000229602800000691a400003efe00004b34000059be",
    [],[], "outer_terrain_snow"),
  ("random_scene_desert", sf_generate|sf_randomize|sf_auto_entry_points, "none", "none", (0, 0),(240, 240), -0.5, "0x0000000229602800000691a400003efe00004b34000059be",
    [], [], "outer_terrain_desert_b"),
  ("random_scene_steppe_forest", sf_generate|sf_randomize|sf_auto_entry_points, "none", "none", (0, 0), (240, 240), -0.5, "0x300028000003e8fa0000034e00004b34000059be",
    [], [], "outer_terrain_plain"),
  ("random_scene_plain_forest", sf_generate|sf_randomize|sf_auto_entry_points, "none", "none", (0, 0), (240, 240), -0.5, "0x300028000003e8fa0000034e00004b34000059be",
    [], [], "outer_terrain_plain"),
  ("random_scene_snow_forest", sf_generate|sf_randomize|sf_auto_entry_points, "none", "none", (0, 0), (240, 240), -0.5, "0x300028000003e8fa0000034e00004b34000059be",
    [], [], "outer_terrain_snow"),
  ("random_scene_desert_forest", sf_generate|sf_randomize|sf_auto_entry_points, "none", "none", (0, 0), (240, 240), -0.5, "0x300028000003e8fa0000034e00004b34000059be",
    [], [], "outer_terrain_desert"),
	
# World map scene is a completely empty scene without terrain
("world_map", 0, "none", "none", (-1000, -1000), (1000, 1000), -0.5, "0", [], []),

]
