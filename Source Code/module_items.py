from module_constants import *
from ID_factions import *
from header_items import  *
from header_operations import *
from header_triggers import *

# #######################################################################
#	["item_id", "Item_name_string", [("mesh_name",modifier)], flags, capabiliries, value, stats, modifiers, [triggers], [faction_id]],
#
#  Each item record contains the following fields:
#  1) Item id: used for referencing items in other files.
#     The prefix itm_ is automatically added before each item id.
#  2) Item name. Name of item as it'll appear in inventory window
#  3) List of meshes.  Each mesh record is a tuple containing the following fields:
#    3.1) Mesh name.
#    3.2) Modifier bits that this mesh matches.
#     Note that the first mesh record is the default.
#  4) Item flags. See header_items.py for a list of available flags.
#  5) Item capabilities. Used for which animations this item is used with. 
#						 See header_items.py for a list of available flags.
#  6) Item value.
#  7) Item stats: Bitwise-or of various stats about the item such as:
#      weight, abundance, difficulty, head_armor, body_armor,leg_armor, etc...
#  8) Modifier bits: Modifiers that can be applied to this item.
#  9) [Optional] Triggers: List of simple triggers to be associated with the item.
#  10) [Optional] Factions: List of factions that item can be found as merchandise.
# #######################################################################


# #######################################################################
# 	imodbits/constants declarations
#
#	You can use use this as a way of declaring multiple imodbits for 
#	convenience/ ease of use. Native MS uses this as a way to combine
#	the hardcoded imodbits from header_items for ease of use.
# #######################################################################
imodbits_none = 0

items = [

# #######################################################################
# 	Hardcoded items, according to Native MS
# #######################################################################
	
	["no_item", "INVALID ITEM", [("invalid_item", 0)], 0, 0, 1, 0, 0],
	["tutorial_spear", "INVALID ITEM", [("invalid_item", 0)], 0, 0, 1, 0, 0],
	["tutorial_club", "INVALID ITEM", [("invalid_item", 0)], 0, 0, 1, 0, 0],
	["tutorial_battle_axe", "INVALID ITEM", [("invalid_item", 0)], 0, 0, 1, 0, 0],
	["tutorial_arrows", "INVALID ITEM", [("invalid_item", 0)], 0, 0, 1, 0, 0],
	["tutorial_bolts", "INVALID ITEM", [("invalid_item", 0)], 0, 0, 1, 0, 0],
	["tutorial_short_bow", "INVALID ITEM", [("invalid_item", 0)], 0, 0, 1, 0, 0],
	["tutorial_crossbow", "INVALID ITEM", [("invalid_item", 0)], 0, 0, 1, 0, 0],
	["tutorial_throwing_daggers", "INVALID ITEM", [("invalid_item", 0)], 0, 0, 1, 0, 0],
	["tutorial_saddle_horse", "INVALID ITEM", [("invalid_item", 0)], 0, 0, 1, 0, 0],
	["tutorial_shield", "INVALID ITEM", [("invalid_item", 0)], 0, 0, 1, 0, 0],
	["tutorial_staff_no_attack", "INVALID ITEM", [("invalid_item", 0)], 0, 0, 1, 0, 0],
	["tutorial_sword", "INVALID ITEM", [("invalid_item", 0)], 0, 0, 1, 0, 0],
	["tutorial_axe", "INVALID ITEM", [("invalid_item", 0)], 0, 0, 1, 0, 0],
	["tutorial_dagger", "INVALID ITEM", [("invalid_item", 0)], 0, 0, 1, 0, 0],
	["horse_meat", "INVALID ITEM", [("invalid_item", 0)], 0, 0, 1, 0, 0],

# #######################################################################
#	This is as far as the engine requires, so feel free to go wild!!!
# #######################################################################
]
