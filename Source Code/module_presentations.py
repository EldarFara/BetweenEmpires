from header_common import *
from header_presentations import *
from header_mission_templates import *
from ID_meshes import *
from header_operations import *
from header_triggers import *
from module_constants import *
import string

# #######################################################################
#
#	("presentation_id", flags, bg_mesh, [triggers]),
#
#  Each presentation record contains the following fields:
#  1) Presentation id: used for referencing presentations in other files. The prefix prsnt_ is automatically added before each presentation id.
#  2) Presentation flags. See header_presentations.py for a list of available flags
#  3) Presentation background mesh: See module_meshes.py for a list of available background meshes
#  4) Triggers: Simple triggers that are associated with the presentation
# #######################################################################
presentations = [

    # #######################################################################
    # 		Hardcoded, mostly things the engine will try to call and will
	#		cause errors if not declared, even if they do nothing.
	# #######################################################################
	
	# #######################################################################
	# 	Called by engine when game starts, can be used to add to the main
	# 	menu. The funny thing is that if it doesn't exist, there is no error,
	#	but if it does exist it ~A B S O L U T E L Y~ must be first.
	# #######################################################################
	("game_start", 0, 0,
		[(ti_on_presentation_load,[(presentation_set_duration, 0)]),
	]),
	
	# Called by engine when pressing `ESC`, can be used to add to the escape menu
	("game_escape", 0, 0,
		[(ti_on_presentation_load,[(presentation_set_duration, 0)]),
	]),
	
	# Called by pressing the credits button on the main menu
	("game_credits", 0, 0,
		[(ti_on_presentation_load,[(presentation_set_duration, 0)]),
	]),
	
	# #######################################################################
	# Called by engine when setting up a banner for Multiplayer, the engine
	# looks for its existance even if your module.ini has_multiplayer = 0
	# #######################################################################
	("game_profile_banner_selection", 0, 0,
		[(ti_on_presentation_load,[(presentation_set_duration, 0)]),
	]),
	
	# #######################################################################
	# Called by engine when setting up a custom battle from the main menu.
	#	Copy and Paste from Native if you would like to re-add,
	#	If you want to take out entirely, find :
	# initial_custom_battle_button_size_x, initial_custom_battle_button_size_y
	# initial_custom_battle_button_text_size_x, initial_custom_battle_button_text_size_y
	#	in game_variables.txt and set to 0.0
	# #######################################################################
	("game_custom_battle_designer", 0, 0,
		[(ti_on_presentation_load,[(presentation_set_duration, 0)]),
	]),
	
	# #######################################################################
	# Called by engine when looking at the admin menu in multiplayer, 
	# is hardcoded an required even if your module.ini has_multiplayer = 0
	# #######################################################################
	("game_multiplayer_admin_panel", 0, 0,
		[(ti_on_presentation_load,[(presentation_set_duration, 0)]),
	]),
	
	# #######################################################################
	# Called by the engine when a player exits the game. Basically used
	# in Native to show a purchase promo screen in demo mode.
	# #######################################################################
	("game_before_quit", 0, 0,
		[(ti_on_presentation_load,[(presentation_set_duration, 0)]),
	]),
    
# Auto-ending presentation for script_wse_window_opened
("empty", 0, 0, [(ti_on_presentation_load,[(presentation_set_duration, 0)]), ]),
]
