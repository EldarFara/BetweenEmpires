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

# Opens after clicking new game button, serves for start date selection and leads to world map
("start_date_selection", prsntf_manual_end_only, 0, [
(ti_on_presentation_load,[
(call_script, "script_start_date_selection_prsnt_start"),
]), 

(ti_on_presentation_run,[
(call_script, "script_start_date_selection_prsnt_frame"),
]), 

(ti_on_presentation_event_state_change,[
(store_trigger_param_1, ":object"),
(store_trigger_param_2, ":value"),
(call_script, "script_start_date_selection_prsnt_event", ":object", ":value"),
]), 

]),

# Main world map presentation, should always be running while on the world map
("world_map", prsntf_manual_end_only, 0, [
(ti_on_presentation_load,[
(call_script, "script_world_map_prsnt_start"),
]), 

(ti_on_presentation_run,[
(call_script, "script_world_map_prsnt_frame"),
]), 

(ti_on_presentation_event_state_change,[
(store_trigger_param_1, ":object"),
(store_trigger_param_2, ":value"),
(call_script, "script_world_map_prsnt_event", ":object", ":value"),
]), 

]),

]


# ("test1", [
# (store_script_param, ":province1", 1),

# (dict_create, ":nearest_provinces"),
# (array_create, ":next_provinces_ring", 0, 0),
# (assign, reg0, ":province1"), (dict_set_int, ":nearest_provinces", "@{reg0}", ":province1"),
# (array_push, ":next_provinces_ring", ":province1"),
    # (try_for_range, ":unused", 0, 2),
    # (array_copy, ":current_provinces_ring", ":next_provinces_ring"),
    # (array_free, ":next_provinces_ring"), (array_create, ":next_provinces_ring", 0, 0),
    # (array_get_dim_size, ":size_current_provinces_ring", ":current_provinces_ring", 0),
        # (try_for_range, ":index_current_provinces_ring", 0, ":size_current_provinces_ring"),
        # (array_get_val, ":province_current_provinces_ring", ":current_provinces_ring", ":index_current_provinces_ring"),
            # (try_for_range, ":index", 0, number_of_provinces_borders),
                # (try_begin),
                # (array_eq, "$provinces_borders", -1, ":province_current_provinces_ring", ":index"),
                # (break_loop),
                # (try_end),
            # (array_get_val, ":province2", "$provinces_borders", ":province_current_provinces_ring", ":index"),
                # (try_begin),
                # (assign, reg0, ":province2"), (neg|dict_has_key, ":nearest_provinces", "@{reg0}"),
                # (dict_set_int, ":nearest_provinces", "@{reg0}", ":province2"),
                # (array_push, ":next_provinces_ring", ":province2"),
                # (try_end),
            # (try_end),
        # (try_end),
    # (try_end),


    # # (try_for_dict_keys, s1, ":nearest_provinces"),
    # # (display_message, "@{s1}"),
    # # (dict_get_int, ":province", ":nearest_provinces", s1, -1),
    # # (array_get_val, ":prop", "$provinces", ":province", province_prop1),
    # # (sss, s2, "@rika"),
    # # (prop_instance_set_material, ":prop", -1, s2),
    # # (try_end),
# (dict_free, ":nearest_provinces"),
# (array_free, ":next_provinces_ring"),
# (array_free, ":current_provinces_ring"),
    
# ]),