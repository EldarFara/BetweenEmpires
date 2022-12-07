from header_map_icons import *
from module_constants import *
from header_operations import *
from header_triggers import *
from ID_sounds import *

# #######################################################################
# ("icon_id", flags, "mesh_name", icon_scale, movement_sound, flag_x_offset, flag_y_offset, flag_z_offset),
#
#  Each map icon record contains the following fields:
#  1) Map icon id: used for referencing map icons in other files.
#     The prefix icon_ is automatically added before each map icon id.
#  2) Map icon flags. See header_map icons.py for a list of available flags
#  3) Mesh name.
#  4) Scale. 
#  5) Sound.
#  6) Offset x position for the flag icon.
#  7) Offset y position for the flag icon.
#  8) Offset z position for the flag icon.
# #######################################################################



# #######################################################################
#	Declarations/Scales/Constants
#		This is not hardcoded, but they are useful declarations to simplify things later.
#		Essentially you name the scale so you can copy and paste in human readable words as
#		opposed to some number. Try giving a unit a really big one. It's neat.
# #######################################################################

avatar_scale = 0.15

map_icons = [
# #######################################################################
#		Map Icons, I don't think these are hardcoded, 
#			but I left them referenced to make it easier to start work.
# #######################################################################
    ("player", 0, "player", avatar_scale, snd_footstep_grass, 0.15, 0.173, 0),
    ("player_horseman", 0, "player_horseman", avatar_scale, snd_gallop, 0.15, 0.173, 0),
]
