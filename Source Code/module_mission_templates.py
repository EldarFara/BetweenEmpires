from header_common import *
from header_operations import *
from header_mission_templates import *
from header_animations import *
from header_sounds import *
from header_music import *
from header_items import *
from module_constants import *

# There are 2 mission templates in BE2: world map and battle, each having its own trigger sets

# This is for player spawn. Since presentations won't work if player wasn't spawn, player agent will still technically be present on world map.
world_map_on_agent_spawn = (
ti_on_agent_spawn, 0, 0, [],
[
(store_trigger_param_1, ":agent"),
(call_script, "script_world_map_agent_spawn", ":agent"),
])

# Triggers every frame
world_map_frame = (
0, 0, 0, [],
[
(call_script, "script_world_map_camera_movement_frame"),

])

# Triggers every 5 ms
world_map_5ms = (
0.005, 0, 0, [],
[
(call_script, "script_world_map_camera_movement_5ms"),

])

# Triggers after scene loads and appears on screen
world_map_start = (
0, 0, ti_once, [],
[
(call_script, "script_world_map_start"),
])

world_map_trigger_set = [
world_map_start,
world_map_frame,
world_map_5ms,
world_map_on_agent_spawn,
]

mission_templates = [
# Hardcoded mission templates
("town_default", 0, -1,
"Town Default",
[
(0, mtef_scene_source|mtef_team_0, af_override_horse, 0, 1, []),
],     
[]),
("conversation_encounter", 0, -1,
"Conversation Encounter",
[
(0, mtef_visitor_source, af_override_fullhelm, 0, 1, []), 
(1, mtef_visitor_source, af_override_fullhelm, 0, 1, []),
(2, mtef_visitor_source, af_override_fullhelm, 0, 1, []), 
(3, mtef_visitor_source, af_override_fullhelm, 0, 1, []),
(4, mtef_visitor_source, af_override_fullhelm, 0, 1, []),
(5, mtef_visitor_source, af_override_fullhelm, 0, 1, []),
(6, mtef_visitor_source, af_override_fullhelm, 0, 1, []),
(7, mtef_visitor_source, af_override_fullhelm, 0, 1, []), 
(8, mtef_visitor_source, af_override_fullhelm, 0, 1, []),
(9, mtef_visitor_source, af_override_fullhelm, 0, 1, []),
(10, mtef_visitor_source, af_override_fullhelm, 0, 1, []),
(11, mtef_visitor_source, af_override_fullhelm, 0, 1, []),
(12, mtef_visitor_source, af_override_fullhelm, 0, 1, []),
(13, mtef_visitor_source, af_override_fullhelm, 0, 1, []),
(14, mtef_visitor_source, af_override_fullhelm, 0, 1, []),
(15, mtef_visitor_source, af_override_fullhelm, 0, 1, []),
(16, mtef_visitor_source, af_override_fullhelm, 0, 1, []),
(17, mtef_visitor_source, af_override_fullhelm, 0, 1, []),
(18, mtef_visitor_source, af_override_fullhelm, 0, 1, []),
(19, mtef_visitor_source, af_override_fullhelm, 0, 1, []),
(20, mtef_visitor_source, af_override_fullhelm, 0, 1, []),
(21, mtef_visitor_source, af_override_fullhelm, 0, 1, []),
(22, mtef_visitor_source, af_override_fullhelm, 0, 1, []),
(23, mtef_visitor_source, af_override_fullhelm, 0, 1, []),
(24, mtef_visitor_source, af_override_fullhelm, 0, 1, []),
(25, mtef_visitor_source, af_override_fullhelm, 0, 1, []),
(26, mtef_visitor_source, af_override_fullhelm, 0, 1, []),
(27, mtef_visitor_source, af_override_fullhelm, 0, 1, []),
(28, mtef_visitor_source, af_override_fullhelm, 0, 1, []),
(29, mtef_visitor_source, af_override_fullhelm, 0, 1, []),
(30, mtef_visitor_source, af_override_fullhelm, 0, 1, []),
(31, mtef_visitor_source, af_override_fullhelm, 0, 1, []),
],
[],
),

# World map mission template. Added mtf_battle_mode to this so player can't save the game with traditional way
("world_map", mtf_battle_mode, -1, " ",
[ (0, 0, 0, 0, 1, []), ],
[] + world_map_trigger_set,
),




]