from header_common import *
from header_operations import *
from module_constants import *
from module_constants import *
from header_parties import *
from header_skills import *
from header_mission_templates import *
from header_items import *
from header_triggers import *
from header_terrain_types import *
from header_music import *
from header_presentations import *
from ID_animations import *

# #######################################################################
# scripts is a list of script records.
# Each script record contains the following two fields:
# 1) Script id: The prefix "script_" will be inserted when referencing scripts.
# 2) Operation block: This must be a valid operation block. See header_operations.py for reference.
# #######################################################################

# #######################################################################
#		(script_id, [operation_block]),
#	Pretty simple stuff. It's also pretty standard practice for the person making the code to do something like
#			#script_script_id:
# 			#This is a description of the script
# 			#INPUT:
#			#	Param 1: 
#			#	Param 2:
#			#OUTPUT: 
#			#	What the output would be.
# #######################################################################

# (display_message, "@  "),

scripts = [	
	
	# #######################################################################
	# 	Engine Scripts, the engine will look for these on load 
	#	so they you need them to prevent errors but they are not required 
	#	to stay in this order or to actually function.
	# #######################################################################

	#script_game_start:
	# This script is called by the engine when a new game is started
	# INPUT: none
	# OUTPUT: none
	("game_start",
	[
    
	]),

	#script_game_quick_start
	# This script is called from the game engine for initializing the global variables 
	# for tutorial, multiplayer and custom battle modes. Similar to game_start without 
	# the stuff for map and diplomacy things
	# INPUT: none
	# OUTPUT: none
	("game_quick_start",
	[
	]),

	#script_game_set_multiplayer_mission_end
	# This script is called from the game engine when a multiplayer map is ended in clients (not in server).
	# INPUT: none
	# OUTPUT: none
	("game_set_multiplayer_mission_end",
	[
	]),
	
	#script_game_get_use_string
	# This script is called from the game engine for getting using information text
	# INPUT: used_scene_prop_id
	# OUTPUT: s0
	("game_get_use_string",
	[
	]),
	
	#script_game_enable_cheat_menu
	# This script is called from the game engine when user enters "cheatmenu from command console (ctrl+~).
	# INPUT:
	# none
	# OUTPUT:
	# none
	("game_enable_cheat_menu",
	[
	]),

	# script_game_event_party_encounter:
	# This script is called from the game engine whenever player party encounters another party or a battle on the world map
	# INPUT:
	# param1: encountered_party
	# param2: second encountered_party (if this was a battle
	("game_event_party_encounter",
	[
	]),

	#script_game_event_simulate_battle:
	# This script is called whenever the game simulates the battle between two parties on the map.
	# INPUT:
	# param1: Defender Party
	# param2: Attacker Party
	("game_event_simulate_battle",
	[
	]),

	#script_game_event_battle_end:
	# This script is called whenever the game ends the battle between two parties on the map.
	# INPUT:
	# param1: Defender Party
	# param2: Attacker Party
	("game_event_battle_end",
	[
	]), 

	#script_game_get_item_buy_price_factor:
	# This script is called from the game engine for calculating the buying price of any item.
	# INPUT:
	# param1: item_kind_id
	# OUTPUT:
	# trigger_result and reg0 = price_factor
	("game_get_item_buy_price_factor",
	[
	]),

	#script_game_get_item_sell_price_factor:
	# This script is called from the game engine for calculating the selling price of any item.
	# INPUT:
	# param1: item_kind_id
	# OUTPUT:
	# trigger_result and reg0 = price_factor
	("game_get_item_sell_price_factor",
	[
	]),

	#script_game_event_buy_item:
	# This script is called from the game engine when player buys an item.
	# INPUT:
	# param1: item_kind_id
	("game_event_buy_item",
	[
	]),

	#script_game_event_sell_item:
	# This script is called from the game engine when player sells an item.
	# INPUT:
	# param1: item_kind_id
	("game_event_sell_item",
	[
	]),	

	# script_game_get_troop_wage
	# This script is called from the game engine for calculating troop wages.
	# Input:
	# param1: troop_id, param2: party-id
	# Output: reg0: weekly wage
	("game_get_troop_wage",
	[
	]),

	# script_game_get_total_wage
	# This script is called from the game engine for calculating total wage of the player party which is shown at the party window.
	# Input: none
	# Output: reg0: weekly wage
	("game_get_total_wage",
	[
	]),

	# script_game_get_join_cost
	# This script is called from the game engine for calculating troop join cost.
	# Input:
	# param1: troop_id,
	# Output: reg0: weekly wage
	("game_get_join_cost",
	[
	]),

	# script_game_get_upgrade_xp
	# This script is called from game engine for calculating needed troop upgrade exp
	# Input:
	# param1: troop_id,
	# Output: reg0 = needed exp for upgrade 
	("game_get_upgrade_xp",
	[
	]),

	# script_game_get_upgrade_cost
	# This script is called from game engine for calculating needed troop upgrade exp
	# Input:
	# param1: troop_id,
	# Output: reg0 = needed cost for upgrade
	("game_get_upgrade_cost",
	[
	]),

	# script_game_get_prisoner_price
	# This script is called from the game engine for calculating prisoner price
	# Input:
	# param1: troop_id,
	# Output: reg0
	("game_get_prisoner_price",
	[
	]),


	# script_game_check_prisoner_can_be_sold
	# This script is called from the game engine for checking if a given troop can be sold.
	# Input: 
	# param1: troop_id,
	# Output: reg0: 1= can be sold; 0= cannot be sold.
	("game_check_prisoner_can_be_sold",
	[
	]),

	# script_game_get_morale_of_troops_from_faction
	# This script is called from the game engine 
	# Input: 
	# param1: faction_no,
	# Output: reg0: extra morale x 100
	("game_get_morale_of_troops_from_faction",
	[
	]),

	#script_game_event_detect_party:
	# This script is called from the game engine when player party inspects another party.
	# INPUT:
	# param1: Party-id
	("game_event_detect_party",
	[
	]),

	#script_game_event_undetect_party:
	# This script is called from the game engine when player party inspects another party.
	# INPUT:
	# param1: Party-id
	("game_event_undetect_party",
	[
	]),

	#script_game_get_statistics_line:
	# This script is called from the game engine when statistics page is opened.
	# INPUT:
	# param1: line_no
	("game_get_statistics_line",
	[
	]),

	#script_game_get_date_text:
	# This script is called from the game engine when the date needs to be displayed.
	# INPUT: arg1 = number of days passed since the beginning of the game
	# OUTPUT: result string = date
	("game_get_date_text",
	[
	]),

	#script_game_get_money_text:
	# This script is called from the game engine when an amount of money needs to be displayed.
	# INPUT: arg1 = amount in units
	# OUTPUT: result string = money in text
	("game_get_money_text",
	[
	]),

	#script_game_get_party_companion_limit:
	# This script is called from the game engine when the companion limit is needed for a party.
	# INPUT: arg1 = none
	# OUTPUT: reg0 = companion_limit
	("game_get_party_companion_limit",
	[
	]),


	#script_game_reset_player_party_name:
	# This script is called from the game engine when the player name is changed.
	# INPUT: none
	# OUTPUT: none
	("game_reset_player_party_name",
	[
	]),

	#script_game_get_troop_note
	# This script is called from the game engine when the notes of a troop is needed.
	# INPUT: arg1 = troop_no, arg2 = note_index
	# OUTPUT: s0 = note
	("game_get_troop_note",
	[
	]),

	#script_game_get_center_note
	# This script is called from the game engine when the notes of a center is needed.
	# INPUT: arg1 = center_no, arg2 = note_index
	# OUTPUT: s0 = note
	("game_get_center_note",
	[
	]),

	#script_game_get_faction_note
	# This script is called from the game engine when the notes of a faction is needed.
	# INPUT: arg1 = faction_no, arg2 = note_index
	# OUTPUT: s0 = note
	("game_get_faction_note",
	[
	]),

	#script_game_get_quest_note
	# This script is called from the game engine when the notes of a quest is needed.
	# INPUT: arg1 = quest_no, arg2 = note_index
	# OUTPUT: s0 = note
	("game_get_quest_note",
	[
	]),

	#script_game_get_info_page_note
	# This script is called from the game engine when the notes of a info_page is needed.
	# INPUT: arg1 = info_page_no, arg2 = note_index
	# OUTPUT: s0 = note
	("game_get_info_page_note",
	[
	]),

	#script_game_get_scene_name
	# This script is called from the game engine when a name for the scene is needed.
	# INPUT: arg1 = scene_no
	# OUTPUT: s0 = name
	("game_get_scene_name",
	[
	]),

	#script_game_get_mission_template_name
	# This script is called from the game engine when a name for the mission template is needed.
	# INPUT: arg1 = mission_template_no
	# OUTPUT: s0 = name
	("game_get_mission_template_name",
	[
	]),

	#script_game_receive_url_response
	# response format should be like this:
	# [a number or a string]|[another number or a string]|[yet another number or a string] ...
	# here is an example response:
	# 12|Player|100|another string|142|323542|34454|yet another string
	# INPUT: arg1 = num_integers, arg2 = num_strings
	# reg0, reg1, reg2, ... up to 128 registers contain the integer values
	# s0, s1, s2, ... up to 128 strings contain the string values
	("game_receive_url_response",
	[
	]),
	#script_game_get_cheat_mode
	# dstn speculation for this whole entry: 
	# Assuming this script determines whether or not cheat mode on the ctrl+~ 
	# command line has been activated.
	# INPUT: NONE
	# OUTPUT: reg0 = cheatmenu_status, 0 for inactive, 1 for active. I assume. 
	("game_get_cheat_mode",
	[
	]),

	#script_game_receive_network_message
	# This script is called from the game engine when a new network message is received.
	# INPUT: arg1 = player_no, arg2 = event_type, arg3 = value, arg4 = value_2, arg5 = value_3, arg6 = value_4
	("game_receive_network_message",
	[
	]),

	#script_game_get_multiplayer_server_option_for_mission_template
	# Input: arg1 = mission_template_id, arg2 = option_index
	# Output: trigger_result = 1 for option available, 0 for not available
	# reg0 = option_value
	("game_get_multiplayer_server_option_for_mission_template",
	[
	]),

	#script_game_multiplayer_server_option_for_mission_template_to_string
	# Input: arg1 = mission_template_id, arg2 = option_index, arg3 = option_value
	# Output: s0 = option_text
	("game_multiplayer_server_option_for_mission_template_to_string",
	[
	]),

	#script_game_multiplayer_event_duel_offered
	# Input: arg1 = agent_no
	# Output: none
	("game_multiplayer_event_duel_offered",
	[
	]),
		 
	#script_game_get_multiplayer_game_type_enum
	# Input: none
	# Output: reg0:first type, reg1:type count
	("game_get_multiplayer_game_type_enum",
	[
	]),

	#script_game_multiplayer_get_game_type_mission_template
	# Input: arg1 = game_type
	# Output: mission_template 
	("game_multiplayer_get_game_type_mission_template",
	[
	]),

	#script_game_get_party_prisoner_limit
	# This script is called from the game engine when the prisoner limit is needed for a party.
	# INPUT: arg1 = party_no
	# OUTPUT: reg0 = prisoner_limit
	("game_get_party_prisoner_limit",
	[
	]),

	#script_game_get_item_extra_text:
	# This script is called from the game engine when an item's properties are displayed.
	# INPUT: arg1 = item_no, arg2 = extra_text_id (this can be between 0-7 (7 included)), arg3 = item_modifier
	# OUTPUT: result_string = item extra text, trigger_result = text color (0 for default)
	("game_get_item_extra_text",
	[
	]),

	#script_game_on_disembark:
	# This script is called from the game engine when the player reaches the shore with a ship.
	# INPUT: pos0 = disembark position
	# OUTPUT: none
	("game_on_disembark",
	[
	]),


	#script_game_context_menu_get_buttons:
	# This script is called from the game engine when the player clicks the right mouse button over a party on the map.
	# INPUT: arg1 = party_no
	# OUTPUT: none, fills the menu buttons
	("game_context_menu_get_buttons",
	[
	]),

	#script_game_event_context_menu_button_clicked:
	# This script is called from the game engine when the player clicks on a button at the right mouse menu.
	# INPUT: arg1 = party_no, arg2 = button_value
	# OUTPUT: none
	("game_event_context_menu_button_clicked",
	[
	]),

	#script_game_get_skill_modifier_for_troop
	# This script is called from the game engine when a skill's modifiers are needed
	# INPUT: arg1 = troop_no, arg2 = skill_no
	# OUTPUT: trigger_result = modifier_value
	("game_get_skill_modifier_for_troop",
	[
	]),

	("game_check_party_sees_party",
	[
		(set_trigger_result, 1),
	]),

	("game_get_party_speed_multiplier",
	[
		(set_trigger_result, 100),
	]),

	#script_game_get_console_command
	# This script is called from the game engine when a console command is entered from the dedicated server.
	# INPUT: anything
	# OUTPUT: s0 = result text
	("game_get_console_command",
	[
	]),
	
	# script_game_missile_launch
	# Input: arg1 = shooter_agent_id, arg2 = agent_weapon_item_id, 
	# arg3 = missile_weapon_id, arg4 = missile_item_id
	# pos1 = weapon_item_position
	# Output: none 
	("game_missile_launch",
	[
	]),
	
	# script_game_missile_dives_into_water
	# Input: arg1 = missile_item_id, pos1 = missile_position_on_water
	# Output: none
	("game_missile_dives_into_water",
	[
	]),
	
	#script_game_troop_upgrades_button_clicked
	# This script is called from the game engine when the player clicks on said button from the party screen
	# INPUT: arg1 = troop_id
	("game_troop_upgrades_button_clicked",
	[
	]),
	
	#script_game_character_screen_requested
	# This script is called from the game engine when the player clicks the character button or presses the
	# relevant gamekey default is 'c'
	("game_character_screen_requested",
	[
	]),
	
("add_troop_to_cur_tableau",
[
]),
("add_troop_to_cur_tableau_for_character",
[
]),
("add_troop_to_cur_tableau_for_inventory",
[
]),
("add_troop_to_cur_tableau_for_profile",
[
]),
("add_troop_to_cur_tableau_for_party",
[
]),

#script_wse_window_opened
# Called each time a window (party/inventory/character) is opened
# INPUT
# script param 1 = window no
# script param 2 = window param 1
# script param 3 = window param 2
# OUTPUT
# trigger result = presentation that replaces the window (if not set or negative, window will open normally)
("wse_window_opened", [
# Runs auto-ending presentation prsnt_empty instead of native menus
(set_trigger_result, "prsnt_empty"),
]),

#script_wse_initial_window_start
# Called each time after initial window started with bMainMenuScene=true (requires WSE2)
("wse_initial_window_start", [
]),

#
# Between Empires scripts start
#

# Initializes all variables for fresh new game start according to chosen starting date.
("initialize_new_game", [
(store_script_param, ":start_date", 1),

(call_script, "script_initialize_global_containers"),

(array_set_val, "$globals", ":start_date", global_date_year),
(array_set_val, "$globals", 1, global_date_day_of_year),
(array_set_val, "$globals", 20000, global_world_map_camera_target_z),

(call_script, "script_initialize_factions", ":start_date"),
(call_script, "script_initialize_provinces", ":start_date"),
]),

# Initializes all variables according to chosen save file.
("initialize_load_game", [
# unfinished


(call_script, "script_initialize_global_containers"),

# global variables that need to be saved/loaded:
# $globals
# $dictionary_global
# $provinces
# $provinces_strings
# $provinces_manufacturers
# $factions
# $factions_strings
# $factions_relations

]),

# Set factions parameters
("initialize_factions", [
(store_script_param, ":start_date", 1),
# parameters that aren't dependant on starting date
(sss, s1, "@French Second Republic"), (sss, s2, "@France"), (sss, s3, "@faction_flag_france"), (sss, s4, "@faction_color_france"), (call_script, "script_add_faction", faction_france),
(sss, s1, "@Kingdom of Belgium"), (sss, s2, "@Belgium"), (sss, s3, "@faction_flag_belgium"), (sss, s4, "@faction_color_belgium"), (call_script, "script_add_faction", faction_belgium),
(sss, s1, "@Kingdom of Netherlands"), (sss, s2, "@Netherlands"), (sss, s3, "@faction_flag_netherlands"), (sss, s4, "@faction_color_netherlands"), (call_script, "script_add_faction", faction_netherlands),
(sss, s1, "@United Kingdom of Great Britain and Ireland"), (sss, s2, "@United Kingdom"), (sss, s3, "@faction_flag_britain"), (sss, s4, "@faction_color_britain"), (call_script, "script_add_faction", faction_britain),
(sss, s1, "@Swiss Confederation"), (sss, s2, "@Switzerland"), (sss, s3, "@faction_flag_switzerland"), (sss, s4, "@faction_color_switzerland"), (call_script, "script_add_faction", faction_switzerland),
(sss, s1, "@Duchy of Luxembourg"), (sss, s2, "@Luxembourg"), (sss, s3, "@faction_flag_luxembourg"), (sss, s4, "@faction_color_luxembourg"), (call_script, "script_add_faction", faction_luxembourg),
# parameters that are dependant on starting date

]),

# Set provinces parameters
("initialize_provinces", [
(store_script_param, ":start_date", 1),
# parameters that aren't dependant on starting date
(call_script, "script_add_province", 0, 49534, 42272, faction_france),
(call_script, "script_add_province", 1, 46335, 42196, faction_france),
(call_script, "script_add_province", 2, 47126, 42460, faction_france),
(call_script, "script_add_province", 3, 46982, 41908, faction_france),
(call_script, "script_add_province", 4, 47126, 41332, faction_france),
(call_script, "script_add_province", 5, 47774, 41812, faction_france),
(call_script, "script_add_province", 6, 46958, 40756, faction_france),
(call_script, "script_add_province", 7, 47966, 41140, faction_france),
(call_script, "script_add_province", 8, 47582, 40492, faction_france),
(call_script, "script_add_province", 9, 48134, 40372, faction_france),
(call_script, "script_add_province", 10, 49022, 40468, faction_france),
(call_script, "script_add_province", 11, 48854, 41068, faction_france),
(call_script, "script_add_province", 12, 48518, 41788, faction_france),
(call_script, "script_add_province", 13, 49118, 41812, faction_france),
(call_script, "script_add_province", 14, 47558, 42628, faction_france),
(call_script, "script_add_province", 15, 48110, 42772, faction_france),
(call_script, "script_add_province", 16, 48590, 42628, faction_france),
(call_script, "script_add_province", 17, 48038, 42388, faction_france),
(call_script, "script_add_province", 18, 48638, 42244, faction_france),
(call_script, "script_add_province", 19, 49118, 42388, faction_france),
(call_script, "script_add_province", 20, 48134, 43084, faction_france),
(call_script, "script_add_province", 21, 48566, 43300, faction_belgium),
(call_script, "script_add_province", 22, 48830, 43036, faction_belgium),
(call_script, "script_add_province", 23, 49082, 42820, faction_luxembourg),
(call_script, "script_add_province", 24, 48770, 43564, faction_netherlands),
(call_script, "script_add_province", 25, 48746, 43780, faction_netherlands),
(call_script, "script_add_province", 26, 49214, 43972, faction_netherlands),
(call_script, "script_add_province", 27, 50011, 39831, faction_france),
(call_script, "script_add_province", 28, 46087, 43215, faction_britain),
(call_script, "script_add_province", 29, 47203, 43287, faction_britain),
(call_script, "script_add_province", 30, 47581, 43863, faction_britain),
(call_script, "script_add_province", 31, 46951, 43989, faction_britain),
(call_script, "script_add_province", 32, 46177, 43809, faction_britain),
(call_script, "script_add_province", 33, 46879, 44475, faction_britain),
(call_script, "script_add_province", 34, 46393, 44943, faction_britain),
(call_script, "script_add_province", 35, 46213, 45537, faction_britain),
(call_script, "script_add_province", 36, 45349, 44673, faction_britain),
(call_script, "script_add_province", 37, 44863, 44547, faction_britain),
(call_script, "script_add_province", 38, 45259, 44151, faction_britain),
(call_script, "script_add_province", 39, 44629, 44259, faction_britain),
(call_script, "script_add_province", 40, 44773, 43755, faction_britain),
(call_script, "script_add_province", 41, 49417, 41631, faction_switzerland),
(call_script, "script_add_province", 42, 49813, 41631, faction_switzerland),
# parameters that are dependant on starting date
(call_script, "script_initialize_provinces_owners", ":start_date"),

]),

# Set provinces owners according to start date
("initialize_provinces_owners", [
(store_script_param, ":start_date", 1),



]),

# Initialize one faction
("add_faction", [
(store_script_param, ":index", 1), # array index in $factions, each index is also constant, like faction_france

(array_set_val, "$factions_strings", s1, ":index", faction_string_name),
(array_set_val, "$factions_strings", s2, ":index", faction_string_name_short),
(array_set_val, "$factions_strings", s3, ":index", faction_string_flag),
(array_set_val, "$factions_strings", s4, ":index", faction_string_color),
]),

# Initialize one province
("add_province", [
(store_script_param, ":index", 1), # array index in $provinces
(store_script_param, ":x", 2),
(store_script_param, ":y", 3),
(store_script_param, ":owner_faction", 4), # used for provinces, owners of which are same in any date. for date-specific owners, initialize_provinces_owners is used

(array_set_val, "$provinces", ":x", ":index", province_x),
(array_set_val, "$provinces", ":y", ":index", province_y),
(array_set_val, "$provinces", ":owner_faction", ":index", province_owner),
]),

# Global containers initialization
("initialize_global_containers", [
(dict_create, "$dictionary_global"),
(array_create, "$globals", 0, number_of_global_parameters),
(array_create, "$factions", 0, number_of_factions, number_of_factions_parameters),
(array_create, "$factions_strings", 1, number_of_factions, number_of_factions_strings),
(array_create, "$provinces", 0, number_of_provinces, number_of_provinces_parameters),
(array_create, "$provinces_strings", 1, number_of_provinces, number_of_provinces_strings),
(array_create, "$provinces_manufacturers", 0, number_of_provinces, number_of_resources),

(array_set_val_all, "$globals", -1),
(array_set_val_all, "$factions", -1),
(array_set_val_all, "$provinces", -1),
(array_set_val_all, "$provinces_manufacturers", -1),
]),

# Called when agent spawns on the world map, i. e. player agent.
# Makes player agent invisible and immovable.
("world_map_agent_spawn", [
(store_script_param, ":agent", 1),

    (try_begin),
    (neg|agent_is_non_player, ":agent"),
    (init_position, pos1),
    (position_move_x, pos1, 5000, 0), # Move agent a bit from zero coordinates so "Leave battle" sign doesn't show up
    (position_move_y, pos1, 5000, 0),
    (agent_set_position, ":agent", pos1),
    (agent_set_no_dynamics, ":agent", 1),
    (agent_set_visibility, ":agent", 0),
    (agent_stop_sound, ":agent"),
    (try_end),
]),

# Called whenever world map scene starts: after new game start, after loading there after battle ended and after loading a save file.
# Script adds props to the scene, sets up camera and runs the UI.
("world_map_start", [
# Spawning world map base prop and province props
(init_position, pos1),
(set_spawn_position, pos1),
(spawn_scene_prop, "spr_world_map_base"),

(position_move_z, pos1, 20, 1),
(set_spawn_position, pos1),
    (try_for_range, ":province", 0, number_of_provinces),
    (store_add, ":prop_type", "spr_province0", ":province"),
    (spawn_scene_prop, ":prop_type"),
    (array_set_val, "$provinces", reg0, ":province", province_prop1),
    (array_get_val, ":faction", "$provinces", ":province", province_owner),
        (try_begin),
        (neq, ":faction", -1),
        (array_get_val, s1, "$factions_strings", ":faction", faction_string_color),
        (else_try), # if province doesnt have owner (uncolonized land), use neutral color instead
        (sss, s1, "@solid_gray"),
        (try_end),
    (prop_instance_set_material, reg0, -1, s1),
    (try_end),

# Setting up camera
(init_position, pos1),
(mission_cam_set_mode, 1, 0, 0),
(position_move_x, pos1, 40000, 1),
(position_move_y, pos1, 40000, 1),
(position_move_z, pos1, 20000, 1),
(position_rotate_x, pos1, 90, 0),
(position_rotate_z, pos1, -180, 0),
(position_rotate_z, pos1, 180, 1),
(mission_cam_set_position, pos1),

]),

# Processes world map camera movement with WASD keys and mouse
("world_map_camera_movement", [
(set_fixed_point_multiplier, 100),
    (try_begin), # prsnt_world_map should always be running 
    (neg|is_presentation_active, "prsnt_world_map"),
    (start_presentation, "prsnt_world_map"),
    (try_end),
(mission_cam_get_position, pos1),
(array_get_val, ":target_z", "$globals", global_world_map_camera_target_z),
(position_get_z, ":z", pos1),
# camera movement speed is dependant on current camera height
(store_div, ":move_speed", ":z", 100),
(store_div, ":move_speed_negative", ":z", -100),
(store_div, ":scroll_speed", ":z", 2),
(store_div, ":scroll_speed_negative", ":z", -2),
    (try_begin), # global_world_map_camera_target_z is used for gradual changing of camera height
    (key_is_down, key_mouse_scroll_up),
    (val_add, ":target_z", ":scroll_speed_negative"),
    (array_set_val, "$globals", ":target_z", global_world_map_camera_target_z),
    (else_try),
    (key_is_down, key_mouse_scroll_down),
    (val_add, ":target_z", ":scroll_speed"),
    (array_set_val, "$globals", ":target_z", global_world_map_camera_target_z),
    (try_end),
    (try_begin),
    (store_sub, ":z_difference", ":target_z", ":z"),
    (val_div, ":z_difference", 5),
    (position_move_z, pos1, ":z_difference", 1),
    (try_end),
    (try_begin),
    (try_end),
    (try_begin),
    (key_is_down, key_w),
    (position_move_y, pos1, ":move_speed", 1),
    (try_end),
    (try_begin),
    (key_is_down, key_s),
    (position_move_y, pos1,":move_speed_negative", 1),
    (try_end),
    (try_begin),
    (key_is_down, key_a),
    (position_move_x, pos1, ":move_speed_negative", 1),
    (try_end),
    (try_begin),
    (key_is_down, key_d),
    (position_move_x, pos1, ":move_speed", 1),
    (try_end),
(mission_cam_set_position, pos1),

    (try_begin),
    (key_clicked, key_space),
    (position_get_x, reg0, pos1),
    (position_get_y, reg1, pos1),
    (display_message, "@{reg0} {reg1}"),
    (try_end),
]),

# Start of world map UI
("world_map_prsnt_start", [
(presentation_set_duration, 9999999),
(set_fixed_point_multiplier, 1000),

(create_mesh_overlay, "$ui_black_dot", "mesh_black_dot"),
(position_set_x, pos1, 500),
(position_set_y, pos1, 375),
(overlay_set_position, "$ui_black_dot", pos1),
(overlay_set_display, "$ui_black_dot", 0),
(assign, "$ui_black_dot_is_visible", 0),

]),

# Frame of world map UI
("world_map_prsnt_frame", [

    (try_begin),
    (key_clicked, key_back_space),
        (try_begin),
        (eq, "$ui_black_dot_is_visible", 0),
        (assign, "$ui_black_dot_is_visible", 1),
        (else_try),
        (assign, "$ui_black_dot_is_visible", 0),
        (try_end),
    (overlay_set_display, "$ui_black_dot", "$ui_black_dot_is_visible"),
    (try_end),

]),

]