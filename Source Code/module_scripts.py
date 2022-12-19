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
(sss, s1, "@French Second Republic"), (sss, s2, "@France"), (sss, s3, "@faction_flag_france"), (sss, s4, "@faction_color_france"), (sss, s5, "@French"), (call_script, "script_add_faction", faction_france),
(sss, s1, "@Kingdom of Belgium"), (sss, s2, "@Belgium"), (sss, s3, "@faction_flag_belgium"), (sss, s4, "@faction_color_belgium"), (sss, s5, "@Belgian"), (call_script, "script_add_faction", faction_belgium),
(sss, s1, "@Kingdom of Netherlands"), (sss, s2, "@Netherlands"), (sss, s3, "@faction_flag_netherlands"), (sss, s4, "@faction_color_netherlands"), (sss, s5, "@Dutch"), (call_script, "script_add_faction", faction_netherlands),
(sss, s1, "@United Kingdom of Great Britain and Ireland"), (sss, s2, "@Britain"), (sss, s3, "@faction_flag_britain"), (sss, s4, "@faction_color_britain"), (sss, s5, "@British"), (call_script, "script_add_faction", faction_britain),
(sss, s1, "@Swiss Confederation"), (sss, s2, "@Switzerland"), (sss, s3, "@faction_flag_switzerland"), (sss, s4, "@faction_color_switzerland"), (sss, s5, "@Swiss"), (call_script, "script_add_faction", faction_switzerland),
(sss, s1, "@Duchy of Luxembourg"), (sss, s2, "@Luxembourg"), (sss, s3, "@faction_flag_luxembourg"), (sss, s4, "@faction_color_luxembourg"), (sss, s5, "@Luxembourgish"), (call_script, "script_add_faction", faction_luxembourg),
(sss, s1, "@Kingdom of Spain"), (sss, s2, "@Spain"), (sss, s3, "@faction_flag_spain"), (sss, s4, "@faction_color_spain"), (sss, s5, "@Spanish"), (call_script, "script_add_faction", faction_spain),
(sss, s1, "@Kingdom of Portugal"), (sss, s2, "@Portugal"), (sss, s3, "@faction_flag_portugal"), (sss, s4, "@faction_color_portugal"), (sss, s5, "@Portuguese"), (call_script, "script_add_faction", faction_portugal),
(sss, s1, "@Kingdom of Sardinia"), (sss, s2, "@Sardinia"), (sss, s3, "@faction_flag_italy"), (sss, s4, "@faction_color_italy"), (sss, s5, "@Sardinian"), (call_script, "script_add_faction", faction_italy),
(sss, s1, "@Austrian Empire"), (sss, s2, "@Austria"), (sss, s3, "@faction_flag_austria"), (sss, s4, "@faction_color_austria"), (sss, s5, "@Austrian"), (call_script, "script_add_faction", faction_austria),
(sss, s1, "@State of the Church"), (sss, s2, "@Papal Sates"), (sss, s3, "@faction_flag_papal"), (sss, s4, "@faction_color_papal"), (sss, s5, "@Papal"), (call_script, "script_add_faction", faction_papal),
(sss, s1, "@Duchy of Parma and Piacenza"), (sss, s2, "@Parma"), (sss, s3, "@faction_flag_parma"), (sss, s4, "@faction_color_parma"), (sss, s5, "@Parmese"), (call_script, "script_add_faction", faction_parma),
(sss, s1, "@Grand Duchy of Tuscany"), (sss, s2, "@Tuscany"), (sss, s3, "@faction_flag_tuscany"), (sss, s4, "@faction_color_tuscany"), (sss, s5, "@Tuscan"), (call_script, "script_add_faction", faction_tuscany),
(sss, s1, "@Kingdom of Two Sicilies"), (sss, s2, "@Two Sicilies"), (sss, s3, "@faction_flag_sicily"), (sss, s4, "@faction_color_sicily"), (sss, s5, "@Bourbon"), (call_script, "script_add_faction", faction_sicily),
(sss, s1, "@Kingdom of Prussia"), (sss, s2, "@Prussia"), (sss, s3, "@faction_flag_prussia"), (sss, s4, "@faction_color_prussia"), (sss, s5, "@Prussian"), (call_script, "script_add_faction", faction_prussia),
(sss, s1, "@Kingdom of Bavaria"), (sss, s2, "@Bavaria"), (sss, s3, "@faction_flag_bavaria"), (sss, s4, "@faction_color_bavaria"), (sss, s5, "@Bavarian"), (call_script, "script_add_faction", faction_bavaria),
(sss, s1, "@Kingdom of Hanover"), (sss, s2, "@Hanover"), (sss, s3, "@faction_flag_hanover"), (sss, s4, "@faction_color_hanover"), (sss, s5, "@Hanoveranian"), (call_script, "script_add_faction", faction_hanover),
(sss, s1, "@Kingdom of Saxony"), (sss, s2, "@Saxony"), (sss, s3, "@faction_flag_saxony"), (sss, s4, "@faction_color_saxony"), (sss, s5, "@Saxon"), (call_script, "script_add_faction", faction_saxony),
(sss, s1, "@Kingdom of Wurttemberg"), (sss, s2, "@Wurttemberg"), (sss, s3, "@faction_flag_wurttemberg"), (sss, s4, "@faction_color_wurttemberg"), (sss, s5, "@Wurttemberg"), (call_script, "script_add_faction", faction_wurttemberg),
(sss, s1, "@Electorate of Hesse"), (sss, s2, "@Hesse"), (sss, s3, "@faction_flag_hesse"), (sss, s4, "@faction_color_hesse"), (sss, s5, "@Hessian"), (call_script, "script_add_faction", faction_hesse),
(sss, s1, "@Grand Duchy of Mecklenburg-Schwerin"), (sss, s2, "@Mecklenburg"), (sss, s3, "@faction_flag_mecklenburg"), (sss, s4, "@faction_color_mecklenburg"), (sss, s5, "@Mecklenburg"), (call_script, "script_add_faction", faction_mecklenburg),
(sss, s1, "@Grand Duchy of Oldenburg"), (sss, s2, "@Oldenburg"), (sss, s3, "@faction_flag_oldenburg"), (sss, s4, "@faction_color_oldenburg"), (sss, s5, "@Oldenburg"), (call_script, "script_add_faction", faction_oldenburg),
(sss, s1, "@Kingdom of Denmark"), (sss, s2, "@Denmark"), (sss, s3, "@faction_flag_denmark"), (sss, s4, "@faction_color_denmark"), (sss, s5, "@Danish"), (call_script, "script_add_faction", faction_denmark),
(sss, s1, "@Sublime Ottoman State"), (sss, s2, "@Turkey"), (sss, s3, "@faction_flag_ottoman"), (sss, s4, "@faction_color_ottoman"), (sss, s5, "@Turkish"), (call_script, "script_add_faction", faction_ottoman),
(sss, s1, "@Kingdom of Greece"), (sss, s2, "@Greece"), (sss, s3, "@faction_flag_greece"), (sss, s4, "@faction_color_greece"), (sss, s5, "@Greek"), (call_script, "script_add_faction", faction_greece),
(sss, s1, "@Principality of Serbia"), (sss, s2, "@Serbia"), (sss, s3, "@faction_flag_serbia"), (sss, s4, "@faction_color_serbia"), (sss, s5, "@Serbian"), (call_script, "script_add_faction", faction_serbia),
(sss, s1, "@Principality of Montenegro"), (sss, s2, "@Montenegro"), (sss, s3, "@faction_flag_montenegro"), (sss, s4, "@faction_color_montenegro"), (sss, s5, "@Montenegrin"), (call_script, "script_add_faction", faction_montenegro),
(sss, s1, "@Principality of Wallachia"), (sss, s2, "@Wallachia"), (sss, s3, "@faction_flag_wallachia"), (sss, s4, "@faction_color_wallachia"), (sss, s5, "@Wallachian"), (call_script, "script_add_faction", faction_romania),
(sss, s1, "@Principality of Moldavia"), (sss, s2, "@Moldavia"), (sss, s3, "@faction_flag_moldavia"), (sss, s4, "@faction_color_moldavia"), (sss, s5, "@Moldavian"), (call_script, "script_add_faction", faction_moldavia),
(sss, s1, "@Russian Empire"), (sss, s2, "@Russia"), (sss, s3, "@faction_flag_russia"), (sss, s4, "@faction_color_russia"), (sss, s5, "@Russian"), (call_script, "script_add_faction", faction_russia),
(sss, s1, "@Kingdom of Sweden-Norway"), (sss, s2, "@Sweden-Norway"), (sss, s3, "@faction_flag_swednor"), (sss, s4, "@faction_color_swednor"), (sss, s5, "@Swedish"), (call_script, "script_add_faction", faction_sweden),

# parameters that are dependant on starting date
    (try_begin),
    (eq, ":start_date", 1853),
    (array_set_val, "$factions", 36600000, faction_france, faction_population),
    (array_set_val, "$factions", 4530000, faction_belgium, faction_population),  
    (array_set_val, "$factions", 3160000, faction_netherlands, faction_population),  
    (array_set_val, "$factions", 21290000, faction_britain, faction_population),  
    (array_set_val, "$factions", 2410000, faction_switzerland, faction_population),  
    (array_set_val, "$factions", 196000, faction_luxembourg, faction_population),  
    (array_set_val, "$factions", 15100000, faction_spain, faction_population),  
    (array_set_val, "$factions", 3870000, faction_portugal, faction_population),  
    (array_set_val, "$factions", 1794000, faction_italy, faction_population),  
    (array_set_val, "$factions", 37236000, faction_austria, faction_population), 
    (array_set_val, "$factions", 3481000, faction_papal, faction_population), 
    (array_set_val, "$factions", 603000, faction_parma, faction_population), 
    (array_set_val, "$factions", 1564000, faction_tuscany, faction_population), 
    (array_set_val, "$factions", 7808000, faction_sicily, faction_population), 
    (array_set_val, "$factions", 16935000, faction_prussia, faction_population), 
    (array_set_val, "$factions", 4559000, faction_bavaria, faction_population), 
    (array_set_val, "$factions", 3318000, faction_hanover, faction_population), 
    (array_set_val, "$factions", 1988000, faction_saxony, faction_population), 
    (array_set_val, "$factions", 1733000, faction_wurttemberg, faction_population),  
    (array_set_val, "$factions", 2660769, faction_hesse, faction_population), 
    (array_set_val, "$factions", 476000, faction_mecklenburg, faction_population), 
    (array_set_val, "$factions", 71000, faction_oldenburg, faction_population), 
    (array_set_val, "$factions", 1560000, faction_denmark, faction_population), 
    (array_set_val, "$factions", 35350000, faction_ottoman, faction_population), 
    (array_set_val, "$factions", 1035000, faction_greece, faction_population), 
    (array_set_val, "$factions", 998000, faction_serbia, faction_population), 
    (array_set_val, "$factions", 178000, faction_montenegro, faction_population), 
    (array_set_val, "$factions", 1910000, faction_romania, faction_population), 
    (array_set_val, "$factions", 1643000, faction_moldavia, faction_population), 
    (array_set_val, "$factions", 68800000, faction_russia, faction_population), 
    (array_set_val, "$factions", 49320000, faction_sweden, faction_population),
    (else_try),
    (try_end),
    
]),

# Set provinces parameters
("initialize_provinces", [
(store_script_param, ":start_date", 1),
# parameters that aren't dependant on starting date
(call_script, "script_add_province", 0, 49534, 42272, faction_france, 79, 105, 42, 19, 23, 13, 41, -1, -1, -1, -1),
(call_script, "script_add_province", 1, 46335, 42196, faction_france, 2, 3, -1, -1, -1, -1, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 2, 47126, 42460, faction_france, 14, 5, 1, 3, -1, -1, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 3, 46982, 41908, faction_france, 1, 2, 4, 5, -1, -1, -1, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 4, 47126, 41332, faction_france, 3, 5, 6, 7, -1, -1, -1, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 5, 47774, 41812, faction_france, 2, 3, 4, 7, 12, 14, 17, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 6, 46958, 40756, faction_france, 4, 7, 8, 46, 47, -1, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 7, 47966, 41140, faction_france, 4, 5, 6, 8, 9, 11, 12, -1, -1, -1, -1),
(call_script, "script_add_province", 8, 47582, 40492, faction_france, 6, 7, 9, 45, 46, -1, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 9, 48134, 40372, faction_france, 7, 8, 10, 11, 45, -1, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 10, 49022, 40468, faction_france, 9, 11, 64, -1, -1, -1, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 11, 48854, 41068, faction_france, 7, 9, 10, 12, 13, 41, 64, -1, -1, -1, -1),
(call_script, "script_add_province", 12, 48518, 41788, faction_france, 5, 7, 12, 13, 17, 18, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 13, 49118, 41812, faction_france, 0, 11, 12, 18, 19, 41, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 14, 47558, 42628, faction_france, 2, 5, 15, 17, -1, -1, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 15, 48110, 42772, faction_france, 14, 17, 18, 16, 20, -1, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 16, 48590, 42628, faction_france, 15, 18, 19, 22, -1, -1, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 17, 48038, 42388, faction_france, 14, 5, 12, 18, 15, -1, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 18, 48638, 42244, faction_france, 15, 17, 12, 13, 19, 16, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 19, 49118, 42388, faction_france, 16, 18, 13, 0, 22, -1, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 20, 48134, 43084, faction_france, 15, 22, 21, -1, -1, -1, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 21, 48566, 43300, faction_belgium, 20, 22, 80, 25, -1, -1, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 22, 48830, 43036, faction_belgium, 21, 20, 16, 23, 19, 105, 80, -1, -1, -1, -1),
(call_script, "script_add_province", 23, 49082, 42820, faction_luxembourg, 22, 105, 0, -1, -1, -1, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 24, 48770, 43564, faction_netherlands, 21, 80, 25, 26, -1, -1, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 25, 48746, 43780, faction_netherlands, 24, 26, -1, -1, -1, -1, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 26, 49214, 43972, faction_netherlands, 25, 24, 81, 101, -1, -1, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 27, 50011, 39831, faction_france, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 28, 46229, 43270, faction_britain, 33, 32, 29, -1, -1, -1, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 29, 47191, 43296, faction_britain, 28, 32, 31, 30, -1, -1, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 30, 47529, 43816, faction_britain, 31, 29, -1, -1, -1, -1, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 31, 47061, 43894, faction_britain, 34, 32, 29, 30, -1, -1, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 32, 46645, 43920, faction_britain, 33, 28, 29, 31, 34, -1, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 33, 46177, 43790, faction_britain, 32, 28, -1, -1, -1, -1, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 34, 46749, 44700, faction_britain, 35, 32, 31, -1, -1, -1, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 35, 46333, 44986, faction_britain, 36, 34, -1, -1, -1, -1, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 36, 46244, 45527, faction_britain, 35, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 37, 45423, 44674, faction_britain, 39, 38, -1, -1, -1, -1, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 38, 45259, 44151, faction_britain, 40, 39, 37, -1, -1, -1, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 39, 44629, 44259, faction_britain, 40, 38, 37, -1, -1, -1, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 40, 44773, 43755, faction_britain, 39, 38, -1, -1, -1, -1, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 41, 49417, 41631, faction_switzerland, 0, 13, 11, 64, 42, 43, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 42, 49664, 41877, faction_switzerland, 0, 41, 43, 79, 84, -1, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 43, 50108, 41601, faction_switzerland, 42, 41, 64, 65, 68, 107, 84, -1, -1, -1, -1),
(call_script, "script_add_province", 44, 47984, 38815, faction_spain, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 45, 47559, 39715, faction_spain, 8, 9, 51, 46, -1, -1, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 46, 46859, 39590, faction_spain, 45, 51, 53, 54, 47, 6, 8, -1, -1, -1, -1),
(call_script, "script_add_province", 47, 46434, 40115, faction_spain, 48, 54, 46, 6, -1, -1, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 48, 45809, 40140, faction_spain, 50, 49, 54, 47, -1, -1, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 49, 45184, 39740, faction_spain, 50, 62, 61, 55, 54, 48, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 50, 44559, 40040, faction_spain, 62, 49, 48, -1, -1, -1, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 51, 46809, 38715, faction_spain, 52, 53, 46, 45, -1, -1, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 52, 46459, 38365, faction_spain, 56, 53, 51, -1, -1, -1, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 53, 46034, 38940, faction_spain, 54, 55, 56, 52, 51, 46, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 54, 45859, 39590, faction_spain, 48, 49, 55, 53, 46, 47, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 55, 45034, 38690, faction_spain, 49, 61, 60, 59, 57, 56, 59, 54, -1, -1, -1),
(call_script, "script_add_province", 56, 45809, 38065, faction_spain, 57, 55, 59, 52, -1, -1, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 57, 45134, 37840, faction_spain, 59, 55, 56, 58, -1, -1, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 58, 45254, 37480, faction_britain, 57, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 59, 44359, 38020, faction_portugal, 60, 55, 57, -1, -1, -1, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 60, 44431, 38569, faction_portugal, 59, 55, 61, -1, -1, -1, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 61, 44485, 39145, faction_portugal, 60, 55, 49, 62, -1, -1, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 62, 44593, 39586, faction_portugal, 61, 49, 50, -1, -1, -1, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 63, 49977, 39036, faction_italy, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 64, 49600, 40949, faction_italy, 10, 11, 41, 43, 65, 66, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 65, 50185, 41235, faction_austria, 64, 43, 68, 67, 70, 66, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 66, 50393, 40793, faction_parma, 64, 65, 70, 78, -1, -1, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 67, 50822, 41183, faction_austria, 70, 65, 68, 69, 107, -1, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 68, 50666, 41521, faction_austria, 43, 65, 67, 107, -1, -1, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 69, 51225, 41456, faction_austria, 67, 107, 110, -1, -1, -1, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 70, 50913, 40715, faction_papal, 67, 65, 66, 78, 71, -1, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 71, 51233, 40244, faction_papal, 70, 78, 72, 73, -1, -1, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 72, 51155, 39734, faction_papal, 78, 71, 73, 74, -1, -1, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 73, 51605, 39814, faction_sicily, 71, 72, 74, 75, -1, -1, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 74, 51885, 39364, faction_sicily, 72, 73, 75, 76, -1, -1, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 75, 52485, 39364, faction_sicily, 73, 74, 76, -1, -1, -1, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 76, 52345, 38814, faction_sicily, 74, 75, -1, -1, -1, -1, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 77, 51605, 38024, faction_sicily, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 78, 50670, 40288, faction_tuscany, 66, 70, 71, 72, -1, -1, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 79, 49952, 42314, faction_wurttemberg, 0, 42, 84, 86, 82, 105, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 80, 49277, 43314, faction_prussia, 25, 24, 22, 105, 82, 81, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 81, 49666, 43550, faction_prussia, 101, 26, 80, 82, 83, -1, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 82, 49946, 43158, faction_hesse, 81, 80, 105, 79, 86, 89, 83, -1, -1, -1, -1),
(call_script, "script_add_province", 83, 50212, 43937, faction_hanover, 101, 81, 82, 89, 90, 91, 87, -1, -1, -1, -1),
(call_script, "script_add_province", 84, 50730, 42234, faction_bavaria, 86, 79, 42, 43, 107, 85, 86, -1, -1, -1, -1),
(call_script, "script_add_province", 85, 50898, 42626, faction_bavaria, 86, 84, 109, 130, 93, 89, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 86, 50450, 42766, faction_bavaria, 82, 79, 84, 85, 89, -1, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 87, 50170, 44530, faction_denmark, 83, 91, 88, -1, -1, -1, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 88, 50030, 44943, faction_denmark, 87, 104, 102, -1, -1, -1, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 89, 50582, 43264, faction_prussia, 83, 82, 86, 85, 93, 90, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 90, 50812, 43701, faction_prussia, 83, 89, 93, 92, 91, -1, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 91, 51044, 44370, faction_mecklenburg, 87, 83, 92, 94, -1, -1, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 92, 51316, 43877, faction_prussia, 91, 90, 93, 95, 94, -1, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 93, 51316, 43316, faction_saxony, 90, 89, 85, 130, 96, 95, 92, -1, -1, -1, -1),
(call_script, "script_add_province", 94, 52047, 44285, faction_prussia, 91, 92, 95, 97, 98, -1, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 95, 51894, 43809, faction_prussia, 94, 92, 93, 96, 97, -1, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 96, 52132, 43401, faction_prussia, 95, 93, 130, 126, 106, 97, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 97, 52370, 43894, faction_prussia, 94, 95, 96, 106, 194, 195, 98, -1, -1, -1, -1),
(call_script, "script_add_province", 98, 52863, 44302, faction_prussia, 94, 97, 195, 99, -1, -1, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 99, 53560, 44404, faction_prussia, 98, 191, 192, 100, -1, -1, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 100, 53628, 44710, faction_prussia, 204, 203, 99, -1, -1, -1, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 101, 49633, 44115, faction_oldenburg, 26, 81, 83, -1, -1, -1, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 102, 50075, 45288, faction_denmark, 88, 103, -1, -1, -1, -1, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 103, 50126, 45560, faction_denmark, 102, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 104, 50789, 44999, faction_denmark, 88, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 105, 49463, 42806, faction_prussia, 23, 0, 79, 82, 80, 22, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 106, 52727, 43163, faction_prussia, 127, 132, 193, 194, 97, 96, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 107, 51169, 41791, faction_austria, 84, 43, 68, 69, 111, 112, 109, 108, -1, -1, -1),
(call_script, "script_add_province", 108, 51904, 42295, faction_austria, 85, 107, 109, 116, 128, 127, 126, 130, -1, -1, -1),
(call_script, "script_add_province", 109, 51799, 41896, faction_austria, 108, 107, 112, 116, -1, -1, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 110, 51484, 41203, faction_austria, 69, 111, 112, -1, -1, -1, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 111, 51714, 41364, faction_austria, 110, 107, 112, -1, -1, -1, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 112, 52197, 41341, faction_austria, 110, 111, 107, 109, 116, 117, 114, 136, 135, 113, -1),
(call_script, "script_add_province", 113, 52174, 40536, faction_austria, 112, 135, 137, -1, -1, -1, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 114, 52864, 41134, faction_austria, 112, 136, 115, 117, -1, -1, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 115, 53416, 41157, faction_austria, 114, 136, 144, 122, 119, -1, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 116, 52496, 41847, faction_austria, 109, 112, 117, 118, 128, 108, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 117, 52772, 41479, faction_austria, 116, 112, 114, 119, 118, -1, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 118, 53048, 41893, faction_austria, 116, 117, 119, 120, 121, 128, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 119, 53393, 41548, faction_austria, 118, 117, 114, 115, 122, 120, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 120, 53692, 41916, faction_austria, 121, 118, 119, 123, -1, -1, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 121, 53692, 42261, faction_austria, 128, 118, 120, 123, 131, 129, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 122, 53899, 41387, faction_austria, 144, 115, 119, 123, 125, 155, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 123, 54221, 41893, faction_austria, 120, 122, 125, 124, 131, 121, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 124, 54704, 41962, faction_austria, 123, 125, 156, 134, 131, -1, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 125, 54796, 41433, faction_austria, 123, 122, 155, 156, 157, 156, 124, -1, -1, -1, -1),
(call_script, "script_add_province", 126, 51875, 42836, faction_austria, 130, 108, 127, 96, -1, -1, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 127, 52565, 42698, faction_austria, 106, 126, 108, 128, 132, -1, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 128, 52933, 42353, faction_austria, 127, 108, 116, 118, 121, 129, 132, -1, -1, -1, -1),
(call_script, "script_add_province", 129, 53761, 42537, faction_austria, 132, 128, 121, 131, -1, -1, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 130, 51208, 42928, faction_austria, 93, 85, 108, 126, 96, -1, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 131, 54382, 42284, faction_austria, 133, 129, 121, 123, 124, 134, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 132, 53784, 42859, faction_austria, 193, 106, 127, 128, 129, 133, 190, -1, -1, -1, -1),
(call_script, "script_add_province", 133, 54658, 42744, faction_austria, 174, 190, 132, 131, 134, 172, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 134, 54980, 42238, faction_austria, 133, 131, 124, 156, 163, 172, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 135, 52750, 40550, faction_ottoman, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 136, 52650, 40900, faction_ottoman, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 137, 53050, 40375, faction_ottoman, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 138, 53225, 40100, faction_montenegro, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 139, 53450, 39600, faction_ottoman, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 140, 53550, 39150, faction_ottoman, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 141, 54000, 39650, faction_ottoman, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 142, 53650, 39975, faction_ottoman, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 143, 53500, 40350, faction_ottoman, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 144, 53625, 40675, faction_serbia, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 145, 54175, 40375, faction_ottoman, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 146, 53800, 38825, faction_ottoman, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 147, 54350, 30300, faction_ottoman, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 148, 55200, 39425, faction_ottoman, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 149, 54200, 38850, faction_ottoman, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 150, 53950, 38525, faction_greece, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 151, 54550, 38425, faction_greece, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 152, 54300, 38050, faction_greece, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 153, 55225, 37075, faction_ottoman, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 154, 56175, 37475, faction_ottoman, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 155, 54625, 40800, faction_romania, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 156, 55400, 40800, faction_romania, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 157, 55700, 41425, faction_moldavia, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 158, 55375, 41925, faction_moldavia, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 159, 56100, 40825, faction_ottoman, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 160, 55825, 40500, faction_ottoman, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 161, 56350, 41325, faction_russia, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 162, 56025, 41900, faction_russia, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 163, 55300, 42300, faction_russia, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 164, 55875, 39500, faction_ottoman, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 165, 55650, 39950, faction_ottoman, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 166, 55675, 40325, faction_ottoman, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 167, 55050, 39850, faction_ottoman, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 168, 55650, 40275, faction_ottoman, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 169, 54525, 39925, faction_ottoman, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 170, 54525, 40400, faction_ottoman, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 171, 56058, 41829, faction_russia, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 172, 55402, 42772, faction_russia, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 173, 55442, 42748, faction_russia, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 174, 55074, 43346, faction_russia, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 175, 55994, 43208, faction_russia, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 176, 56546, 43024, faction_russia, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 177, 56868, 42656, faction_russia, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 178, 57102, 42344, faction_russia, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 179, 57102, 41876, faction_russia, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 180, 57726, 41681, faction_russia, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 181, 58272, 41837, faction_russia, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 182, 57921, 42383, faction_russia, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 183, 57492, 42929, faction_russia, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 184, 56946, 43436, faction_russia, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 185, 57609, 43319, faction_russia, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 186, 58350, 42812, faction_russia, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 187, 58857, 42188, faction_russia, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 188, 59169, 42539, faction_russia, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 189, 57921, 41057, faction_russia, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 190, 54138, 43475, faction_russia, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 191, 53631, 43826, faction_russia, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 192, 54177, 44177, faction_russia, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 193, 53397, 43163, faction_russia, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 194, 53124, 43553, faction_russia, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 195, 52851, 43826, faction_russia, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 196, 54996, 43865, faction_russia, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 197, 54801, 44333, faction_russia, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 198, 55854, 44957, faction_russia, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 199, 55542, 44372, faction_russia, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 200, 56400, 44294, faction_russia, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 201, 56244, 43748, faction_russia, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 202, 54684, 44762, faction_russia, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 203, 54294, 44996, faction_russia, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 204, 53748, 45113, faction_russia, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 205, 54207, 45465, faction_russia, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 206, 55048, 45552, faction_russia, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 207, 54352, 46219, faction_russia, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 208, 54990, 46190, faction_russia, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 209, 55876, 47201, faction_russia, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 210, 55369, 47201, faction_russia, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 211, 55837, 47747, faction_russia, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 212, 55096, 47669, faction_russia, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 213, 55408, 48215, faction_russia, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 214, 54550, 49307, faction_russia, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 215, 54745, 48371, faction_russia, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 216, 53770, 47630, faction_russia, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 217, 54433, 47396, faction_russia, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 218, 53926, 46889, faction_russia, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 219, 54589, 46889, faction_russia, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 220, 54277, 50204, faction_sweden, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 221, 51859, 49463, faction_sweden, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 222, 50611, 48059, faction_sweden, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 223, 50416, 47201, faction_sweden, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 224, 50221, 46733, faction_sweden, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 225, 49649, 46337, faction_sweden, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 226, 49297, 47041, faction_sweden, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 227, 49737, 47657, faction_sweden, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 228, 52993, 49109, faction_sweden, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 229, 52377, 48405, faction_sweden, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 230, 51805, 47877, faction_sweden, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 231, 51717, 46997, faction_sweden, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 232, 52333, 46513, faction_sweden, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 233, 51761, 46205, faction_sweden, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 234, 51101, 46337, faction_sweden, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 235, 51321, 45721, faction_sweden, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 236, 51893, 45589, faction_sweden, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1),
(call_script, "script_add_province", 237, 51453, 45193, faction_sweden, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1),

(call_script, "script_initialize_provinces_population"),

# parameters that are dependant on starting date
(call_script, "script_initialize_provinces_owners", ":start_date"),

]),

# Calculate provinces population according to faction population and population multipliers
("initialize_provinces_population", [

    (try_for_range, ":faction", 0, number_of_factions),
    (try_end),


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
(array_set_val, "$factions_strings", s5, ":index", faction_string_possessive_case),
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

    # (try_for_range, ":param", 4, 14+1),
    # (store_script_param, ":bordering_province", ":param"),
    # (try_end),
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
(array_set_val, "$globals", ui_mode_none, global_ui_mode),

]),

# Processes world map camera movement with WASD keys and mouse
("world_map_camera_movement_frame", [
(set_fixed_point_multiplier, 100),
    (try_begin), # prsnt_world_map should always be running 
    (neg|is_presentation_active, "prsnt_world_map"),
    (start_presentation, "prsnt_world_map"),
    (try_end),
(mission_cam_get_position, pos1),
(array_get_val, ":target_z", "$globals", global_world_map_camera_target_z),
(position_get_z, ":z", pos1),
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
(mission_cam_set_position, pos1),
    (try_begin),
    (key_clicked, key_space),
    (position_get_x, reg0, pos1),
    (position_get_y, reg1, pos1),
    (display_message, "@{reg0} {reg1}"),
    (try_end),
]),
("world_map_camera_movement_5ms", [
(set_fixed_point_multiplier, 100),
(mission_cam_get_position, pos1),
(position_get_z, ":z", pos1),
# camera movement speed is dependant on current camera height
(store_div, ":move_speed", ":z", 60),
(store_div, ":move_speed_negative", ":z", -60),
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
]),

# Start of start date selection UI
("start_date_selection_prsnt_start", [
(presentation_set_duration, 9999999),
(set_fixed_point_multiplier, 1000),

(position_set_x, pos2, 1000), (position_set_y, pos2, 179),
(position_set_x, pos3, 1000), (position_set_y, pos3, 65),

(create_image_button_overlay, "$ui_startdate_title", "mesh_ui_background", "mesh_ui_background"),
(overlay_set_material, "$ui_startdate_title", "@ui_startdate_title"), (position_set_x, pos1, 0), (position_set_y, pos1, 715),
(overlay_set_position, "$ui_startdate_title", pos1), (overlay_set_size, "$ui_startdate_title", pos3),
(create_text_overlay, "$ui_startdate_title_text", "@Choose starting date:"),
(position_set_x, pos1, 400), (position_set_y, pos1, 725), (overlay_set_position, "$ui_startdate_title_text", pos1),

# Button for each starting date
(create_image_button_overlay, "$ui_1853", "mesh_ui_background", "mesh_ui_background"),
(overlay_set_material, "$ui_1853", "@ui_startdate_1853"), (position_set_x, pos1, 0), (position_set_y, pos1, 600),
(overlay_set_position, "$ui_1853", pos1), (overlay_set_size, "$ui_1853", pos2),
(create_image_button_overlay, "$ui_1861", "mesh_ui_background", "mesh_ui_background"),
(overlay_set_material, "$ui_1861", "@ui_startdate_1861"), (position_set_x, pos1, 0), (position_set_y, pos1, 480),
(overlay_set_position, "$ui_1861", pos1), (overlay_set_size, "$ui_1861", pos2),
(create_image_button_overlay, "$ui_1877", "mesh_ui_background", "mesh_ui_background"),
(overlay_set_material, "$ui_1877", "@ui_startdate_1877"), (position_set_x, pos1, 0), (position_set_y, pos1, 360),
(overlay_set_position, "$ui_1877", pos1), (overlay_set_size, "$ui_1877", pos2),
(create_image_button_overlay, "$ui_1910", "mesh_ui_background", "mesh_ui_background"),
(overlay_set_material, "$ui_1910", "@ui_startdate_1910"), (position_set_x, pos1, 0), (position_set_y, pos1, 240),
(overlay_set_position, "$ui_1910", pos1), (overlay_set_size, "$ui_1910", pos2),
(create_image_button_overlay, "$ui_1919", "mesh_ui_background", "mesh_ui_background"),
(overlay_set_material, "$ui_1919", "@ui_startdate_1919"), (position_set_x, pos1, 0), (position_set_y, pos1, 120),
(overlay_set_position, "$ui_1919", pos1), (overlay_set_size, "$ui_1919", pos2),
(create_image_button_overlay, "$ui_1936", "mesh_ui_background", "mesh_ui_background"),
(overlay_set_material, "$ui_1936", "@ui_startdate_1936"), (position_set_x, pos1, 0), (position_set_y, pos1, 0),
(overlay_set_position, "$ui_1936", pos1), (overlay_set_size, "$ui_1936", pos2),
]),

("start_date_selection_prsnt_frame", [
(set_fixed_point_multiplier, 1000),

(mouse_get_position, pos1),
(position_get_y, ":mouse_y", pos1),

(overlay_set_material, "$ui_1853", "@ui_startdate_1853"),
(overlay_set_material, "$ui_1861", "@ui_startdate_1861"),
(overlay_set_material, "$ui_1877", "@ui_startdate_1877"),
(overlay_set_material, "$ui_1910", "@ui_startdate_1910"),
(overlay_set_material, "$ui_1919", "@ui_startdate_1919"),
(overlay_set_material, "$ui_1936", "@ui_startdate_1936"),

    (try_begin), # Highlight hovered buttons
    (ge, ":mouse_y", 600),
    (overlay_set_material, "$ui_1853", "@ui_startdate_1853_selected"),
    (else_try),
    (ge, ":mouse_y", 480),
    (overlay_set_material, "$ui_1861", "@ui_startdate_1861_selected"),
    (else_try),
    (ge, ":mouse_y", 360),
    (overlay_set_material, "$ui_1877", "@ui_startdate_1877_selected"),
    (else_try),
    (ge, ":mouse_y", 240),
    (overlay_set_material, "$ui_1910", "@ui_startdate_1910_selected"),
    (else_try),
    (ge, ":mouse_y", 120),
    (overlay_set_material, "$ui_1919", "@ui_startdate_1919_selected"),
    (else_try),
    (ge, ":mouse_y", 0),
    (overlay_set_material, "$ui_1936", "@ui_startdate_1936_selected"),
    (try_end),
]),

("start_date_selection_prsnt_event", [
(store_script_param, ":object", 1),
(store_script_param, ":unused", 2),
(set_fixed_point_multiplier, 1000),

(assign, ":start_date", -1),
    (try_begin), # Set start date according to button that was clicked
    (eq, ":object", "$ui_1853"),
    (assign, ":start_date", 1853),
    (else_try),
    (eq, ":object", "$ui_1861"),
    (assign, ":start_date", 1861),
    (else_try),
    (eq, ":object", "$ui_1877"),
    (assign, ":start_date", 1877),
    (else_try),
    (eq, ":object", "$ui_1910"),
    (assign, ":start_date", 1910),
    (else_try),
    (eq, ":object", "$ui_1919"),
    (assign, ":start_date", 1919),
    (else_try),
    (eq, ":object", "$ui_1936"),
    (assign, ":start_date", 1936),
    (try_end),
    
    (try_begin),
    (neq, ":start_date", -1),
    (presentation_set_duration, 0),
    # Initialize_new_game
	(call_script,"script_initialize_new_game", ":start_date"),
    # Jump to world map
    (jump_to_menu, "mnu_to_world_map"),
    (try_end),
]),

("world_map_prsnt_event", [
(store_script_param, ":object", 1),
(store_script_param, ":unused", 2),
(set_fixed_point_multiplier, 1000),

    (try_begin),
    (eq, ":object", "$ui_start_game"),
    (array_eq, "$globals", ui_mode_faction_selection, global_ui_mode),
    (array_set_val, "$globals", ui_mode_none, global_ui_mode),
    (array_get_val, ":faction", "$globals", global_faction_selection_selected_faction),
    (array_set_val, "$globals", ":faction", global_player_faction),
    (presentation_set_duration, 0),
    (try_end),
]),

# Start of world map UI
("world_map_prsnt_start", [
(presentation_set_duration, 9999999),
(set_fixed_point_multiplier, 1000),

(call_script, "script_world_map_ui_start_black_dot"),
(call_script, "script_world_map_ui_start_faction_selection"),
(call_script, "script_world_map_ui_start_bottom_panel"),

]),

# Bottom panel of world map with common info about faction
("world_map_ui_start_bottom_panel", [
    (try_begin),
    (array_eq, "$globals", ui_mode_none, global_ui_mode),
    (create_mesh_overlay, "$ui_bottom_panel", "mesh_ui_background"),
    (overlay_set_material, "$ui_bottom_panel", "@ui_world_map_bottom_panel"),
    (position_set_x, pos1, 0), (position_set_y, pos1, 0),
    (overlay_set_position, "$ui_bottom_panel", pos1),
    (position_set_x, pos1, 1000), (position_set_y, pos1, 130),
    (overlay_set_size, "$ui_bottom_panel", pos1),
    (create_image_button_overlay, "$ui_bottom_panel_flag", "mesh_ui_picture", "mesh_ui_picture"),
    (position_set_x, pos1, 60), (position_set_y, pos1, 35),
    (overlay_set_position, "$ui_bottom_panel_flag", pos1),
    (position_set_x, pos1, 1000*1.5), (position_set_y, pos1, 1000),
    (overlay_set_size, "$ui_bottom_panel_flag", pos1),
    (array_get_val, ":player_faction", "$globals", global_player_faction),
    (call_script, "script_ui_flag_overlay_set_material_and_tooltip", "$ui_bottom_panel_flag", ":player_faction"),
    (try_end),
]),

# Simply sets material (faction flag string) and tooltip (faction full name string) for specified overlay for specified faction
("ui_flag_overlay_set_material_and_tooltip", [
(store_script_param, ":overlay", 1),
(store_script_param, ":faction", 2),

    (try_begin),
    (ge, ":faction", 0),
    (array_get_val, s10, "$factions_strings", ":faction", faction_string_flag),
    (array_get_val, s11, "$factions_strings", ":faction", faction_string_name),
    (overlay_set_material, ":overlay", s10),
    (overlay_set_tooltip, ":overlay", s11),
    (try_end),
]),

    
# Faction selection UI consists of start game button, faction name and flag, or just the "select faction" prompt if no faction selected yet
("world_map_ui_start_faction_selection", [
    (try_begin),
    (array_eq, "$globals", ui_mode_faction_selection, global_ui_mode),
    (create_mesh_overlay, "$ui_bottom_panel", "mesh_ui_background"),
    (overlay_set_material, "$ui_bottom_panel", "@ui_faction_selection_bottom_panel"),
    (position_set_x, pos1, 0), (position_set_y, pos1, 0),
    (overlay_set_position, "$ui_bottom_panel", pos1),
    (position_set_x, pos1, 1000), (position_set_y, pos1, 95),
    (overlay_set_size, "$ui_bottom_panel", pos1),

    (create_mesh_overlay, "$ui_selected_faction_flag", "mesh_ui_picture"),
    (position_set_x, pos1, 50), (position_set_y, pos1, 27),
    (overlay_set_position, "$ui_selected_faction_flag", pos1),
    (position_set_x, pos1, 800*1.5), (position_set_y, pos1, 800),
    (overlay_set_size, "$ui_selected_faction_flag", pos1),
    (overlay_set_display, "$ui_selected_faction_flag", 0),

    (create_text_overlay, "$ui_faction_selection_title", "@ ", tf_center_justify),
    (position_set_x, pos1, 500), (position_set_y, pos1, 20),
    (overlay_set_position, "$ui_faction_selection_title", pos1),

    (create_game_button_overlay, "$ui_start_game", "@Start Game"),
    (position_set_x, pos1, 870), (position_set_y, pos1, 12),
    (overlay_set_position, "$ui_start_game", pos1),
    (overlay_set_display, "$ui_start_game", 0),
    (try_end),
]),

# Frame of world map UI
("world_map_prsnt_frame", [
(set_fixed_point_multiplier, 1000),

(call_script, "script_world_map_ui_black_dot_frame"),
(call_script, "script_world_map_ui_faction_selection"),
(call_script, "script_world_map_ui_process_province_click"),
(call_script, "script_world_map_ui_province_small_menu"),
]),

# After starting new game and selecting starting date player needs to click on any factions province to set it as playable and click "Start Game"
("world_map_ui_faction_selection", [
    (try_begin),
    (array_eq, "$globals", -1, global_player_faction),
    (neg|array_eq, "$globals", ui_mode_faction_selection, global_ui_mode),
    (array_set_val, "$globals", ui_mode_faction_selection, global_ui_mode),
    (array_set_val, "$globals", -1, global_faction_selection_selected_faction),
    (presentation_set_duration, 0),
    (try_end),
    (try_begin),
    (array_eq, "$globals", ui_mode_faction_selection, global_ui_mode),
        (try_begin),
        (array_ge, "$globals", 0, global_faction_selection_selected_faction),
        (array_get_val, ":faction", "$globals", global_faction_selection_selected_faction),
        (array_get_val, s1, "$factions_strings", ":faction", faction_string_flag),
        (array_get_val, s2, "$factions_strings", ":faction", faction_string_name),
        (overlay_set_display, "$ui_start_game", 1),
        (overlay_set_display, "$ui_selected_faction_flag", 1),
        (overlay_set_material, "$ui_selected_faction_flag", s1),
        (overlay_set_text, "$ui_faction_selection_title", s2),
        (else_try),
        (overlay_set_display, "$ui_start_game", 0),
        (overlay_set_display, "$ui_selected_faction_flag", 0),
        (overlay_set_text, "$ui_faction_selection_title", "@Choose a country to play as"),
        (try_end),
    (try_end),
]),

# Handle event when player clicks on province on world map
("world_map_ui_process_province_click", [
(set_fixed_point_multiplier, 1000),

    (try_begin),
    (key_clicked, key_left_mouse_button),
    (this_or_next|array_eq, "$globals", ui_mode_none, global_ui_mode), # Only register clicks if on specific ui modes
    (this_or_next|array_eq, "$globals", ui_mode_faction_selection, global_ui_mode),
    (array_eq, "$globals", ui_mode_province_menu_small, global_ui_mode),
    (mouse_get_position, pos1),
    (assign, ":continue", 1),
    (position_get_x, ":x", pos1),
    (position_get_y, ":y", pos1),
        (try_begin), # Dont register click if clicked on UI areas
        (array_eq, "$globals", ui_mode_faction_selection, global_ui_mode),
        (le, ":y", 64),
        (assign, ":continue", 0),
        (try_end),
    (eq, ":continue", 1),
    (init_position, pos2),
    (set_fixed_point_multiplier, 100),
    (assign, ":closest_province", -1),
    (assign, ":closest_province_distance_to_mouse", 9999999),
        (try_for_range, ":province", 0, number_of_provinces),
        (array_get_val, ":x", "$provinces", ":province", province_x),
        (array_get_val, ":y", "$provinces", ":province", province_y),
        (position_set_x, pos2, ":x"),
        (position_set_y, pos2, ":y"),
        (position_get_screen_projection, pos3, pos2),
        (get_distance_between_positions, ":distance", pos1, pos3),
        (le, ":distance", ":closest_province_distance_to_mouse"),
        (assign, ":closest_province", ":province"),
        (assign, ":closest_province_distance_to_mouse", ":distance"),
        (try_end),
    (set_fixed_point_multiplier, 1000),
        (try_begin),
        (ge, ":closest_province_distance_to_mouse", 7), # If distance is above that, then probably nothing at all was selected
        (assign, ":closest_province", -1),
        (try_end),
        (try_begin),
        (ge, ":closest_province", 0),
(assign, reg0, ":closest_province"),
(display_message, "@{reg0}"),
            (try_begin), # Set faction for faction selection if province has owner
            (array_eq, "$globals", ui_mode_faction_selection, global_ui_mode),
            (array_ge, "$provinces", 0, ":closest_province", province_owner),
            (array_get_val, ":faction", "$provinces", ":closest_province", province_owner),
            (array_set_val, "$globals", ":faction", global_faction_selection_selected_faction),
            (try_end),
        (try_end),
    (try_end),
]),

# Province small menu appears when player clicks on world map 
("world_map_ui_province_small_menu", [
(set_fixed_point_multiplier, 1000),
]),

# Black dot scripts. Black dot on center of screen is toggled by backspace and is used for getting position coordinates on the map
("world_map_ui_start_black_dot", [
(create_mesh_overlay, "$ui_black_dot", "mesh_black_dot"),
(position_set_x, pos1, 500),
(position_set_y, pos1, 375),
(overlay_set_position, "$ui_black_dot", pos1),
(overlay_set_display, "$ui_black_dot", 0),
(assign, "$ui_black_dot_is_visible", 0),
]),

("world_map_ui_black_dot_frame", [
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