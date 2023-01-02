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
(sss, s1, "@Caucasian Imamate"), (sss, s2, "@Caucasia"), (sss, s3, "@faction_flag_caucasia"), (sss, s4, "@faction_color_caucasia"), (sss, s5, "@Caucasian"), (call_script, "script_add_faction", faction_caucasia),
(sss, s1, "@Circassian Confederation"), (sss, s2, "@Circassia"), (sss, s3, "@faction_flag_circassia"), (sss, s4, "@faction_color_circassia"), (sss, s5, "@Circassian"), (call_script, "script_add_faction", faction_circassia),
(sss, s1, "@Emirate of Bukhara"), (sss, s2, "@Bukhara"), (sss, s3, "@faction_flag_bukhara"), (sss, s4, "@faction_color_bukhara"), (sss, s5, "@Bukharan"), (call_script, "script_add_faction", faction_bukhara),
(sss, s1, "@Khanate of Khiva"), (sss, s2, "@Khiva"), (sss, s3, "@faction_flag_khiva"), (sss, s4, "@faction_color_khiva"), (sss, s5, "@Khivan"), (call_script, "script_add_faction", faction_khiva),
(sss, s1, "@Khanate of Kokand"), (sss, s2, "@Kokand"), (sss, s3, "@faction_flag_kokand"), (sss, s4, "@faction_color_kokand"), (sss, s5, "@Kokand"), (call_script, "script_add_faction", faction_kokand),
(sss, s1, "@United States of America"), (sss, s2, "@USA"), (sss, s3, "@faction_flag_usa31"), (sss, s4, "@faction_color_usa"), (sss, s5, "@American"), (call_script, "script_add_faction", faction_usa),
(sss, s1, "@Sublime State of Persia"), (sss, s2, "@Persia"), (sss, s3, "@faction_flag_qajar"), (sss, s4, "@faction_color_qajar"), (sss, s5, "@Persian"), (call_script, "script_add_faction", faction_iran),
(sss, s1, "@Great Qing"), (sss, s2, "@China"), (sss, s3, "@faction_flag_qingearly"), (sss, s4, "@faction_color_qing"), (sss, s5, "@Chinese"), (call_script, "script_add_faction", faction_china),
(sss, s1, "@Emirate of Jabal Shammar"), (sss, s2, "@Shammar"), (sss, s3, "@faction_flag_shammar"), (sss, s4, "@faction_color_shammar"), (sss, s5, "@Shammari"), (call_script, "script_add_faction", faction_rashidi),
(sss, s1, "@Emirate of Nejd"), (sss, s2, "@Nejd"), (sss, s3, "@faction_flag_nejd"), (sss, s4, "@faction_color_saudi"), (sss, s5, "@Najdi"), (call_script, "script_add_faction", faction_saudi),
(sss, s1, "@Mahra State of Qishn and Socotra"), (sss, s2, "@Mahra"), (sss, s3, "@faction_flag_mahra"), (sss, s4, "@faction_color_mahra"), (sss, s5, "@Mahri"), (call_script, "script_add_faction", faction_mahra),
(sss, s1, "@Kathiri State of Seiyun"), (sss, s2, "@Kathiri"), (sss, s3, "@faction_flag_kathiri"), (sss, s4, "@faction_color_kathiri"), (sss, s5, "@Kathiri"), (call_script, "script_add_faction", faction_kathiri),
(sss, s1, "@Omani Empire"), (sss, s2, "@Oman"), (sss, s3, "@faction_flag_red"), (sss, s4, "@faction_color_oman"), (sss, s5, "@Omani"), (call_script, "script_add_faction", faction_oman),
(sss, s1, "@Trucial States"), (sss, s2, "@Trucial States"), (sss, s3, "@faction_flag_trucialearly"), (sss, s4, "@faction_color_trucial"), (sss, s5, "@Trucial"), (call_script, "script_add_faction", faction_trucial),
(sss, s1, "@State of Qatar"), (sss, s2, "@Qatar"), (sss, s3, "@faction_flag_red"), (sss, s4, "@faction_color_qatar"), (sss, s5, "@Qatar"), (call_script, "script_add_faction", faction_qatar), 
(sss, s1, "@Emirate of Afghanistan"), (sss, s2, "@Afghanistan"), (sss, s3, "@faction_flag_black"), (sss, s4, "@faction_color_afghanistan"), (sss, s5, "@Afghan"), (call_script, "script_add_faction", faction_afghanistan),
(sss, s1, "@Principality of Herat"), (sss, s2, "@Herat"), (sss, s3, "@faction_flag_durrani"), (sss, s4, "@faction_color_durrani"), (sss, s5, "@Herati"), (call_script, "script_add_faction", faction_durrani),
(sss, s1, "@Great Joseon"), (sss, s2, "@Joseon"), (sss, s3, "@faction_flag_joseon"), (sss, s4, "@faction_color_joseon"), (sss, s5, "@Korean"), (call_script, "script_add_faction", faction_korea),
(sss, s1, "@Kingdom of Nepal"), (sss, s2, "@Nepal"), (sss, s3, "@faction_flag_nepalearly"), (sss, s4, "@faction_color_nepal"), (sss, s5, "@Nepali"), (call_script, "script_add_faction", faction_nepal),
(sss, s1, "@Kingdom of Bhutan"), (sss, s2, "@Bhutan"), (sss, s3, "@faction_flag_bhutan"), (sss, s4, "@faction_color_bhutan"), (sss, s5, "@Bhutanese"), (call_script, "script_add_faction", faction_bhutan),
(sss, s1, "@Rajputana States"), (sss, s2, "@Rajputana"), (sss, s3, "@faction_flag_rajput"), (sss, s4, "@faction_color_rajput"), (sss, s5, "@Rajput"), (call_script, "script_add_faction", faction_rajput),
(sss, s1, "@Hyderabad State"), (sss, s2, "@Hyderabad"), (sss, s3, "@faction_flag_hyderabadearly"), (sss, s4, "@faction_color_hyderabad"), (sss, s5, "@Hyderabadi"), (call_script, "script_add_faction", faction_hyderabad),
(sss, s1, "@Mysore State"), (sss, s2, "@Mysore"), (sss, s3, "@faction_flag_mysore"), (sss, s4, "@faction_color_mysore"), (sss, s5, "@Mysorean"), (call_script, "script_add_faction", faction_mysore),
(sss, s1, "@Princely State of Oudh"), (sss, s2, "@Oudh"), (sss, s3, "@faction_flag_oudh"), (sss, s4, "@faction_color_oudh"), (sss, s5, "@Oudhwasi"), (call_script, "script_add_faction", faction_oudh),
(sss, s1, "@Kingdom of Sikkim"), (sss, s2, "@Sikkim"), (sss, s3, "@faction_flag_sikkim"), (sss, s4, "@faction_color_sikkim"), (sss, s5, "@Sikkimese"), (call_script, "script_add_faction", faction_sikkim),
(sss, s1, "@Khanate of Kalat"), (sss, s2, "@Kalat"), (sss, s3, "@faction_flag_kalat"), (sss, s4, "@faction_color_kalat"), (sss, s5, "@Kalati"), (call_script, "script_add_faction", faction_kalat),
(sss, s1, "@Konbaung Empire"), (sss, s2, "@Burma"), (sss, s3, "@faction_flag_konbaung"), (sss, s4, "@faction_color_burma"), (sss, s5, "@Burmese"), (call_script, "script_add_faction", faction_burma),
(sss, s1, "@Rattanakosin Kingdom"), (sss, s2, "@Siam"), (sss, s3, "@faction_flag_siamearly"), (sss, s4, "@faction_color_siam"), (sss, s5, "@Siamese"), (call_script, "script_add_faction", faction_siam),
(sss, s1, "@United Mexican States"), (sss, s2, "@Mexico"), (sss, s3, "@faction_flag_mexico1"), (sss, s4, "@faction_color_mexico"), (sss, s5, "@Mexican"), (call_script, "script_add_faction", faction_mexico),
(sss, s1, "@Kingdom of Luang Prabang"), (sss, s2, "@Luang Prabang"), (sss, s3, "@faction_flag_luangprabang"), (sss, s4, "@faction_color_laos"), (sss, s5, "@Lao"), (call_script, "script_add_faction", faction_laos),
(sss, s1, "@Kingdom of Champasak"), (sss, s2, "@Champasak"), (sss, s3, "@faction_flag_champasak"), (sss, s4, "@faction_color_champasak"), (sss, s5, "@Bassac"), (call_script, "script_add_faction", faction_champasak),
(sss, s1, "@Kingdom of Cambodia"), (sss, s2, "@Cambodia"), (sss, s3, "@faction_flag_cambodiaearly"), (sss, s4, "@faction_color_cambodia"), (sss, s5, "@Khmer"), (call_script, "script_add_faction", faction_cambodia),
(sss, s1, "@Great Nam"), (sss, s2, "@Vietnam"), (sss, s3, "@faction_flag_nguyen"), (sss, s4, "@faction_color_nguyenviet"), (sss, s5, "@Vietnamese"), (call_script, "script_add_faction", faction_vietnam),
(sss, s1, "@Sultanate of Johor"), (sss, s2, "@Johor"), (sss, s3, "@faction_flag_johorearly"), (sss, s4, "@faction_color_johor"), (sss, s5, "@Johorian"), (call_script, "script_add_faction", faction_johor),
(sss, s1, "@Sultanate of Pahang"), (sss, s2, "@Pahang"), (sss, s3, "@faction_flag_black"), (sss, s4, "@faction_color_pahang"), (sss, s5, "@Pahangite"), (call_script, "script_add_faction", faction_pahang),
(sss, s1, "@Sultanate of Perak"), (sss, s2, "@Perak"), (sss, s3, "@faction_flag_perak"), (sss, s4, "@faction_color_perak"), (sss, s5, "@Perakian"), (call_script, "script_add_faction", faction_perak),
(sss, s1, "@Sultanate of Sarawak"), (sss, s2, "@Sarawak"), (sss, s3, "@faction_flag_sarawak"), (sss, s4, "@faction_color_sarawak"), (sss, s5, "@Sarawakian"), (call_script, "script_add_faction", faction_sarawak),
(sss, s1, "@Sultanate of Brunei"), (sss, s2, "@Brunei"), (sss, s3, "@faction_flag_yellow"), (sss, s4, "@faction_color_brunei"), (sss, s5, "@Bruneian"), (call_script, "script_add_faction", faction_brunei),
(sss, s1, "@Sultanate of Sulu"), (sss, s2, "@Sulu"), (sss, s3, "@faction_flag_sulu"), (sss, s4, "@faction_color_sulu"), (sss, s5, "@Suluan"), (call_script, "script_add_faction", faction_sulu),
(sss, s1, "@Sultanate of Maguindanao"), (sss, s2, "@Maguindanao"), (sss, s3, "@faction_flag_yellow"), (sss, s4, "@faction_color_maguindanao"), (sss, s5, "@Maguindanaoan"), (call_script, "script_add_faction", faction_maguindanao),
(sss, s1, "@Sultanate of Aceh"), (sss, s2, "@Aceh"), (sss, s3, "@faction_flag_aceh"), (sss, s4, "@faction_color_aceh"), (sss, s5, "@Acehnese"), (call_script, "script_add_faction", faction_aceh),
(sss, s1, "@Kingdomship of Bali"), (sss, s2, "@Bali"), (sss, s3, "@faction_flag_bali"), (sss, s4, "@faction_color_bali"), (sss, s5, "@Balinese"), (call_script, "script_add_faction", faction_bali),
(sss, s1, "@Sultanate of Banjar"), (sss, s2, "@Banjar"), (sss, s3, "@faction_flag_banjar"), (sss, s4, "@faction_color_banjar"), (sss, s5, "@Banjar"), (call_script, "script_add_faction", faction_banjar),
(sss, s1, "@Sultanate of Lombok"), (sss, s2, "@Lombok"), (sss, s3, "@faction_flag_lombok"), (sss, s4, "@faction_color_lombok"), (sss, s5, "@Lombokish"), (call_script, "script_add_faction", faction_lombok),
(sss, s1, "@Sultanate of Pontianak"), (sss, s2, "@Pontianak"), (sss, s3, "@faction_flag_pontianak"), (sss, s4, "@faction_color_pontianak"), (sss, s5, "@Pontianak"), (call_script, "script_add_faction", faction_pontianak),
(sss, s1, "@Lanfang Republic"), (sss, s2, "@Kongsi"), (sss, s3, "@faction_flag_lanfang"), (sss, s4, "@faction_color_lanfang"), (sss, s5, "@Kongsi"), (call_script, "script_add_faction", faction_lanfang),
(sss, s1, "@Sultanate of Kutai Kertanegara"), (sss, s2, "@Kutai"), (sss, s3, "@faction_flag_kutai"), (sss, s4, "@faction_color_kutai"), (sss, s5, "@Kutai"), (call_script, "script_add_faction", faction_kutai),
(sss, s1, "@Sunanate of Surakarta"), (sss, s2, "@Surakarta"), (sss, s3, "@faction_flag_surakarta"), (sss, s4, "@faction_color_surakarta"), (sss, s5, "@Surakartan"), (call_script, "script_add_faction", faction_surakarta),
(sss, s1, "@Sultanate of Yogyakarta"), (sss, s2, "@Yogyakarta"), (sss, s3, "@faction_flag_yogyakarta"), (sss, s4, "@faction_color_yogyakarta"), (sss, s5, "@Yogyakartan"), (call_script, "script_add_faction", faction_yogyakarta),
(sss, s1, "@Emirate of Tunisia"), (sss, s2, "@Tunisia"), (sss, s3, "@faction_flag_tunisia"), (sss, s4, "@faction_color_tunisia"), (sss, s5, "@Tunisian"), (call_script, "script_add_faction", faction_tunisia),
(sss, s1, "@Kingdom of Morocco"), (sss, s2, "@Morocco"), (sss, s3, "@faction_flag_red"), (sss, s4, "@faction_color_morocco"), (sss, s5, "@Moroccan"), (call_script, "script_add_faction", faction_morocco),
(sss, s1, "@Tokugawa Shogunate"), (sss, s2, "@Japan"), (sss, s3, "@faction_flag_shogunate"), (sss, s4, "@faction_color_shogunate"), (sss, s5, "@Japanese"), (call_script, "script_add_faction", faction_shogunate),
(sss, s1, "@Satsuma Domain"), (sss, s2, "@Satsuma"), (sss, s3, "@faction_flag_satsuma"), (sss, s4, "@faction_color_satsuma"), (sss, s5, "@Satsuma"), (call_script, "script_add_faction", faction_satsuma),
(sss, s1, "@Choshu Domain"), (sss, s2, "@Choshu"), (sss, s3, "@faction_flag_choshu"), (sss, s4, "@faction_color_choshu"), (sss, s5, "@Choshu"), (call_script, "script_add_faction", faction_choshu),
(sss, s1, "@Tosa Domain"), (sss, s2, "@Tosa"), (sss, s3, "@faction_flag_tosa"), (sss, s4, "@faction_color_tosa"), (sss, s5, "@Tosa"), (call_script, "script_add_faction", faction_tosa),
(sss, s1, "@Saga Domain"), (sss, s2, "@Saga"), (sss, s3, "@faction_flag_saga"), (sss, s4, "@faction_color_saga"), (sss, s5, "@Saga"), (call_script, "script_add_faction", faction_saga),
(sss, s1, "@Kingdom of Ryukyu"), (sss, s2, "@Ryukyu"), (sss, s3, "@faction_flag_ryukyu"), (sss, s4, "@faction_color_ryukyu"), (sss, s5, "@Ryukyuan"), (call_script, "script_add_faction", faction_ryukyu),
(sss, s1, "@Sultanate of Darfur"), (sss, s2, "@Darfur"), (sss, s3, "@faction_flag_darfur"), (sss, s4, "@faction_color_darfur"), (sss, s5, "@Darfuri"), (call_script, "script_add_faction", faction_darfur),
(sss, s1, "@Kel Ahaggar Tuaregs"), (sss, s2, "@Ahaggar"), (sss, s3, "@faction_flag_ahaggar"), (sss, s4, "@faction_color_ahaggar"), (sss, s5, "@Tuareg"), (call_script, "script_add_faction", faction_ahaggar),
(sss, s1, "@Kingdom of Shilluk"), (sss, s2, "@Shilluk"), (sss, s3, "@faction_flag_shilluk"), (sss, s4, "@faction_color_shilluk"), (sss, s5, "@Shilluk"), (call_script, "script_add_faction", faction_shilluk),
(sss, s1, "@Solomonic Dynasty"), (sss, s2, "@Ethiopia"), (sss, s3, "@faction_flag_ethiopiaearly"), (sss, s4, "@faction_color_ethiopia"), (sss, s5, "@Ethiopian"), (call_script, "script_add_faction", faction_ethiopia),
(sss, s1, "@Sultanate of Harar"), (sss, s2, "@Harar"), (sss, s3, "@faction_flag_harar"), (sss, s4, "@faction_color_harar"), (sss, s5, "@Harari"), (call_script, "script_add_faction", faction_harar),
(sss, s1, "@Sultanate of Aussa"), (sss, s2, "@Aussa"), (sss, s3, "@faction_flag_red"), (sss, s4, "@faction_color_aussa"), (sss, s5, "@Aussan"), (call_script, "script_add_faction", faction_aussa),
(sss, s1, "@Sultanate of Isaaq"), (sss, s2, "@Isaaq"), (sss, s3, "@faction_flag_isaaq"), (sss, s4, "@faction_color_isaaq"), (sss, s5, "@Isaaqi"), (call_script, "script_add_faction", faction_isaaq),
(sss, s1, "@Somalian Sultanates"), (sss, s2, "@Somalia"), (sss, s3, "@faction_flag_red"), (sss, s4, "@faction_color_somalia"), (sss, s5, "@Somali"), (call_script, "script_add_faction", faction_somalia),
(sss, s1, "@Heavenly Kingdom of Great Peace"), (sss, s2, "@Taiping"), (sss, s3, "@faction_flag_taiping"), (sss, s4, "@faction_color_taiping"), (sss, s5, "@Taiping"), (call_script, "script_add_faction", faction_taiping),
(sss, s1, "@Masai Tribes"), (sss, s2, "@Masai"), (sss, s3, "@faction_flag_masai"), (sss, s4, "@faction_color_masai"), (sss, s5, "@Masai"), (call_script, "script_add_faction", faction_masai),
(sss, s1, "@Bornu Empire"), (sss, s2, "@Bornu"), (sss, s3, "@faction_flag_bornu"), (sss, s4, "@faction_color_bornu"), (sss, s5, "@Bornu"), (call_script, "script_add_faction", faction_bornu),
(sss, s1, "@Sultanate of Wadai"), (sss, s2, "@Wadai"), (sss, s3, "@faction_flag_wadai"), (sss, s4, "@faction_color_wadai"), (sss, s5, "@Wadai"), (call_script, "script_add_faction", faction_wadai),
(sss, s1, "@Sultanate of Baghirmi"), (sss, s2, "@Baghirmi"), (sss, s3, "@faction_flag_baghirmi"), (sss, s4, "@faction_color_baghirmi"), (sss, s5, "@Baghirmi"), (call_script, "script_add_faction", faction_baghirmi),
(sss, s1, "@Sultanate of Kanem"), (sss, s2, "@Kanem"), (sss, s3, "@faction_flag_kanem"), (sss, s4, "@faction_color_kanem"), (sss, s5, "@Kanuri"), (call_script, "script_add_faction", faction_kanem),
(sss, s1, "@Sokoto Caliphate"), (sss, s2, "@Sokoto"), (sss, s3, "@faction_flag_green"), (sss, s4, "@faction_color_sokoto"), (sss, s5, "@Fulani"), (call_script, "script_add_faction", faction_sokoto),
(sss, s1, "@Sokoto Caliphate"), (sss, s2, "@Sokoto"), (sss, s3, "@faction_flag_green"), (sss, s4, "@faction_color_sokoto"), (sss, s5, "@Fulani"), (call_script, "script_add_faction", faction_sokoto),
(sss, s1, "@Oyo Empire"), (sss, s2, "@Oyo"), (sss, s3, "@faction_flag_oyo"), (sss, s4, "@faction_color_oyo"), (sss, s5, "@Oyo"), (call_script, "script_add_faction", faction_oyo),
(sss, s1, "@Kingdom of Benin"), (sss, s2, "@Benin"), (sss, s3, "@faction_flag_beninedo"), (sss, s4, "@faction_color_beninedo"), (sss, s5, "@Beninese"), (call_script, "script_add_faction", faction_beninedo),
(sss, s1, "@Cameroonian Kingdoms"), (sss, s2, "@Cameroon"), (sss, s3, "@faction_flag_cameroonearly"), (sss, s4, "@faction_color_cameroon"), (sss, s5, "@Cameroonian"), (call_script, "script_add_faction", faction_cameroon),
(sss, s1, "@Kingdom of Hawaii"), (sss, s2, "@Hawaii"), (sss, s3, "@faction_flag_hawaii"), (sss, s4, "@faction_color_hawaii"), (sss, s5, "@Hawaiian"), (call_script, "script_add_faction", faction_hawaii),
(sss, s1, "@Sultanate of Agadez"), (sss, s2, "@Agadez"), (sss, s3, "@faction_flag_agadez"), (sss, s4, "@faction_color_agadez"), (sss, s5, "@Agadez"), (call_script, "script_add_faction", faction_agadez),
(sss, s1, "@Sultanate of Damagaram"), (sss, s2, "@Damagaram"), (sss, s3, "@faction_flag_black"), (sss, s4, "@faction_color_damagaram"), (sss, s5, "@Damagaram"), (call_script, "script_add_faction", faction_damagaram),
(sss, s1, "@Kel Adagh Tuaregs"), (sss, s2, "@Adagh"), (sss, s3, "@faction_flag_tuareg"), (sss, s4, "@faction_color_adagh"), (sss, s5, "@Tuareg"), (call_script, "script_add_faction", faction_adagh),
(sss, s1, "@Bamana Empire"), (sss, s2, "@Mali"), (sss, s3, "@faction_flag_bamana"), (sss, s4, "@faction_color_bamana"), (sss, s5, "@Bamana"), (call_script, "script_add_faction", faction_bamana),
(sss, s1, "@Kingdom of Dendi"), (sss, s2, "@Dendi"), (sss, s3, "@faction_flag_dendi"), (sss, s4, "@faction_color_dendi"), (sss, s5, "@Dendi"), (call_script, "script_add_faction", faction_dendi),
(sss, s1, "@Toubou Tribes"), (sss, s2, "@Toubou"), (sss, s3, "@faction_flag_toubou"), (sss, s4, "@faction_color_toubou"), (sss, s5, "@Toubouan"), (call_script, "script_add_faction", faction_toubou),


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
    (array_set_val, "$factions", 2660000, faction_hesse, faction_population), 
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
    (array_set_val, "$factions", 2443000, faction_caucasia, faction_population),
    (array_set_val, "$factions", 97000, faction_circassia, faction_population),
    (array_set_val, "$factions", 2258000, faction_bukhara, faction_population),
    (array_set_val, "$factions", 1580000, faction_khiva, faction_population),
    (array_set_val, "$factions", 729000, faction_kokand, faction_population),
    (array_set_val, "$factions", 7735000, faction_iran, faction_population),
    (array_set_val, "$factions", 436100000, faction_china, faction_population),
    (array_set_val, "$factions", 1341000, faction_rashidi, faction_population),
    (array_set_val, "$factions", 1287000, faction_saudi, faction_population),
    (array_set_val, "$factions", 15000, faction_mahra, faction_population),
    (array_set_val, "$factions", 17000, faction_kathiri, faction_population),
    (array_set_val, "$factions", 408000, faction_oman, faction_population),
    (array_set_val, "$factions", 59000, faction_trucial, faction_population),
    (array_set_val, "$factions", 23000, faction_qatar, faction_population),
    (array_set_val, "$factions", 3465000, faction_afghanistan, faction_population),
    (array_set_val, "$factions", 395000, faction_durrani, faction_population),
    (array_set_val, "$factions", 15460000, faction_korea, faction_population),
    (array_set_val, "$factions", 2987000, faction_nepal, faction_population),
    (array_set_val, "$factions", 458000, faction_bhutan, faction_population),
    (array_set_val, "$factions", 7563000, faction_rajput, faction_population),
    (array_set_val, "$factions", 9912000, faction_hyderabad, faction_population),
    (array_set_val, "$factions", 1817000, faction_mysore, faction_population),
    (array_set_val, "$factions", 7973000, faction_oudh, faction_population),
    (array_set_val, "$factions", 88000, faction_sikkim, faction_population),
    (array_set_val, "$factions", 771000, faction_kalat, faction_population),
    (array_set_val, "$factions", 12800000, faction_burma, faction_population),
    (array_set_val, "$factions", 7960000, faction_siam, faction_population),
    (array_set_val, "$factions", 7940000, faction_mexico, faction_population),
    (array_set_val, "$factions", 982000, faction_laos, faction_population),
    (array_set_val, "$factions", 897000, faction_champasak, faction_population),
    (array_set_val, "$factions", 821000, faction_cambodia, faction_population),
    (array_set_val, "$factions", 11273000, faction_vietnam, faction_population),
    
    (else_try),
    (try_end),
    
]),

# Set provinces parameters
("initialize_provinces", [
(store_script_param, ":start_date", 1),
# parameters that aren't dependant on starting date
(call_script, "script_add_province", 0, 49481, 42387, faction_france, 79, 105, 42, 19, 23, 13, 41, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 1, 46335, 42196, faction_france, 2, 3, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 2, 47126, 42460, faction_france, 14, 5, 1, 3, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 3, 46982, 41908, faction_france, 1, 2, 4, 5, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 4, 47126, 41332, faction_france, 3, 5, 6, 7, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 5, 47774, 41812, faction_france, 2, 3, 4, 7, 12, 14, 17, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 6, 46958, 40756, faction_france, 4, 7, 8, 46, 47, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 7, 47966, 41140, faction_france, 4, 5, 6, 8, 9, 11, 12, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 8, 47582, 40492, faction_france, 6, 7, 9, 45, 46, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 9, 48134, 40372, faction_france, 7, 8, 10, 11, 45, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 10, 49022, 40468, faction_france, 9, 11, 64, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 11, 48854, 41068, faction_france, 7, 9, 10, 12, 13, 41, 64, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 12, 48518, 41788, faction_france, 5, 7, 12, 13, 17, 18, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 13, 49118, 41812, faction_france, 0, 11, 12, 18, 19, 41, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 14, 47558, 42628, faction_france, 2, 5, 15, 17, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 15, 48110, 42772, faction_france, 14, 17, 18, 16, 20, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 16, 48590, 42628, faction_france, 15, 18, 19, 22, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 17, 48038, 42388, faction_france, 14, 5, 12, 18, 15, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 18, 48638, 42244, faction_france, 15, 17, 12, 13, 19, 16, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 19, 49118, 42388, faction_france, 16, 18, 13, 0, 22, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 20, 48134, 43084, faction_france, 15, 22, 21, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 21, 48566, 43300, faction_belgium, 20, 22, 80, 25, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 22, 48830, 43036, faction_belgium, 21, 20, 16, 23, 19, 105, 80, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 23, 49082, 42820, faction_luxembourg, 22, 105, 0, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 24, 48770, 43564, faction_netherlands, 21, 80, 25, 26, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 25, 48746, 43780, faction_netherlands, 24, 26, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 26, 49214, 43972, faction_netherlands, 25, 24, 81, 101, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 27, 50011, 39831, faction_france, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 28, 46229, 43270, faction_britain, 33, 32, 29, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 29, 47191, 43296, faction_britain, 28, 32, 31, 30, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 30, 47529, 43816, faction_britain, 31, 29, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 31, 47061, 43894, faction_britain, 34, 32, 29, 30, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 32, 46645, 43920, faction_britain, 33, 28, 29, 31, 34, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 33, 46177, 43790, faction_britain, 32, 28, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 34, 46749, 44700, faction_britain, 35, 32, 31, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 35, 46333, 44986, faction_britain, 36, 34, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 36, 46244, 45527, faction_britain, 35, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 37, 45423, 44674, faction_britain, 39, 38, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 38, 45259, 44151, faction_britain, 40, 39, 37, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 39, 44629, 44259, faction_britain, 40, 38, 37, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 40, 44773, 43755, faction_britain, 39, 38, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 41, 49417, 41631, faction_switzerland, 0, 13, 11, 64, 42, 43, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 42, 49664, 41877, faction_switzerland, 0, 41, 43, 79, 84, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 43, 50108, 41601, faction_switzerland, 42, 41, 64, 65, 68, 107, 84, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 44, 47984, 38815, faction_spain, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 45, 47559, 39715, faction_spain, 8, 9, 51, 46, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 46, 46859, 39590, faction_spain, 45, 51, 53, 54, 47, 6, 8, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 47, 46434, 40115, faction_spain, 48, 54, 46, 6, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 48, 45809, 40140, faction_spain, 50, 49, 54, 47, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 49, 45184, 39740, faction_spain, 50, 62, 61, 55, 54, 48, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 50, 44559, 40040, faction_spain, 62, 49, 48, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 51, 46809, 38715, faction_spain, 52, 53, 46, 45, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 52, 46459, 38365, faction_spain, 56, 53, 51, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 53, 46034, 38940, faction_spain, 54, 55, 56, 52, 51, 46, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 54, 45859, 39590, faction_spain, 48, 49, 55, 53, 46, 47, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 55, 45034, 38690, faction_spain, 49, 61, 60, 59, 57, 56, 59, 54, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 56, 45809, 38065, faction_spain, 57, 55, 59, 52, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 57, 45134, 37840, faction_spain, 59, 55, 56, 58, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 58, 45254, 37480, faction_britain, 57, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 59, 44359, 38020, faction_portugal, 60, 55, 57, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 60, 44431, 38569, faction_portugal, 59, 55, 61, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 61, 44485, 39145, faction_portugal, 60, 55, 49, 62, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 62, 44593, 39586, faction_portugal, 61, 49, 50, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 63, 49977, 39036, faction_italy, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 64, 49600, 40949, faction_italy, 10, 11, 41, 43, 65, 66, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 65, 50185, 41235, faction_austria, 64, 43, 68, 67, 70, 66, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 66, 50393, 40793, faction_parma, 64, 65, 70, 78, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 67, 50822, 41183, faction_austria, 70, 65, 68, 69, 107, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 68, 50666, 41521, faction_austria, 43, 65, 67, 107, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 69, 51225, 41456, faction_austria, 67, 107, 110, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 70, 50913, 40715, faction_papal, 67, 65, 66, 78, 71, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 71, 51233, 40244, faction_papal, 70, 78, 72, 73, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 72, 51155, 39734, faction_papal, 78, 71, 73, 74, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 73, 51605, 39814, faction_sicily, 71, 72, 74, 75, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 74, 51885, 39364, faction_sicily, 72, 73, 75, 76, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 75, 52485, 39364, faction_sicily, 73, 74, 76, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 76, 52345, 38814, faction_sicily, 74, 75, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 77, 51605, 38024, faction_sicily, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 78, 50670, 40288, faction_tuscany, 66, 70, 71, 72, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 79, 49952, 42314, faction_wurttemberg, 0, 42, 84, 86, 82, 105, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 80, 49277, 43314, faction_prussia, 25, 24, 22, 105, 82, 81, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 81, 49666, 43550, faction_prussia, 101, 26, 80, 82, 83, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 82, 49946, 43158, faction_hesse, 81, 80, 105, 79, 86, 89, 83, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 83, 50212, 43937, faction_hanover, 101, 81, 82, 89, 90, 91, 87, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 84, 50730, 42234, faction_bavaria, 86, 79, 42, 43, 107, 85, 86, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 85, 50898, 42626, faction_bavaria, 86, 84, 109, 130, 93, 89, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 86, 50450, 42766, faction_bavaria, 82, 79, 84, 85, 89, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 87, 50170, 44530, faction_denmark, 83, 91, 88, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 88, 50030, 44943, faction_denmark, 87, 104, 102, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 89, 50582, 43264, faction_prussia, 83, 82, 86, 85, 93, 90, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 90, 50812, 43701, faction_prussia, 83, 89, 93, 92, 91, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 91, 51044, 44370, faction_mecklenburg, 87, 83, 92, 94, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 92, 51316, 43877, faction_prussia, 91, 90, 93, 95, 94, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 93, 51316, 43316, faction_saxony, 90, 89, 85, 130, 96, 95, 92, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 94, 52047, 44285, faction_prussia, 91, 92, 95, 97, 98, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 95, 51894, 43809, faction_prussia, 94, 92, 93, 96, 97, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 96, 52132, 43401, faction_prussia, 95, 93, 130, 126, 106, 97, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 97, 52370, 43894, faction_prussia, 94, 95, 96, 106, 194, 195, 98, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 98, 52863, 44302, faction_prussia, 94, 97, 195, 99, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 99, 53560, 44404, faction_prussia, 98, 191, 192, 100, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 100, 53628, 44710, faction_prussia, 204, 203, 99, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 101, 49633, 44115, faction_oldenburg, 26, 81, 83, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 102, 50075, 45288, faction_denmark, 88, 103, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 103, 50126, 45560, faction_denmark, 102, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 104, 50557, 44911, faction_denmark, 88, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 105, 49463, 42806, faction_prussia, 23, 0, 79, 82, 80, 22, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 106, 52727, 43163, faction_prussia, 127, 132, 193, 194, 97, 96, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 107, 51169, 41791, faction_austria, 84, 43, 68, 69, 111, 112, 109, 108, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 108, 51904, 42295, faction_austria, 85, 107, 109, 116, 128, 127, 126, 130, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 109, 51799, 41896, faction_austria, 108, 107, 112, 116, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 110, 51484, 41203, faction_austria, 69, 111, 112, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 111, 51714, 41364, faction_austria, 110, 107, 112, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 112, 52197, 41341, faction_austria, 110, 111, 107, 109, 116, 117, 114, 136, 135, 113, -1, terrain_plains),
(call_script, "script_add_province", 113, 52174, 40536, faction_austria, 112, 135, 137, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 114, 52864, 41134, faction_austria, 112, 136, 115, 117, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 115, 53416, 41157, faction_austria, 114, 136, 144, 122, 119, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 116, 52496, 41847, faction_austria, 109, 112, 117, 118, 128, 108, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 117, 52772, 41479, faction_austria, 116, 112, 114, 119, 118, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 118, 53048, 41893, faction_austria, 116, 117, 119, 120, 121, 128, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 119, 53393, 41548, faction_austria, 118, 117, 114, 115, 122, 120, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 120, 53692, 41916, faction_austria, 121, 118, 119, 123, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 121, 53692, 42261, faction_austria, 128, 118, 120, 123, 131, 129, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 122, 53899, 41387, faction_austria, 144, 115, 119, 123, 125, 155, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 123, 54221, 41893, faction_austria, 120, 122, 125, 124, 131, 121, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 124, 54704, 41962, faction_austria, 123, 125, 156, 134, 131, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 125, 54796, 41433, faction_austria, 123, 122, 155, 156, 157, 156, 124, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 126, 51875, 42836, faction_austria, 130, 108, 127, 96, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 127, 52565, 42698, faction_austria, 106, 126, 108, 128, 132, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 128, 52933, 42353, faction_austria, 127, 108, 116, 118, 121, 129, 132, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 129, 53761, 42537, faction_austria, 132, 128, 121, 131, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 130, 51208, 42928, faction_austria, 93, 85, 108, 126, 96, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 131, 54382, 42284, faction_austria, 133, 129, 121, 123, 124, 134, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 132, 53784, 42859, faction_austria, 193, 106, 127, 128, 129, 133, 190, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 133, 54658, 42744, faction_austria, 174, 190, 132, 131, 134, 172, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 134, 54980, 42238, faction_austria, 133, 131, 124, 156, 163, 172, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 135, 52750, 40550, faction_ottoman, 136, 112, 113, 137, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 136, 52650, 40900, faction_ottoman, 114, 112, 135, 137, 144, 115, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 137, 53050, 40375, faction_ottoman, 135, 113, 144, 143, 138, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 138, 53225, 40100, faction_montenegro, 137, 143, 142, 139, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 139, 53450, 39600, faction_ottoman, 138, 142, 141, 140, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 140, 53550, 39150, faction_ottoman, 139, 141, 147, 146, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 141, 54000, 39650, faction_ottoman, 142, 139, 140, 147, 169, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 142, 53650, 39975, faction_ottoman, 143, 138, 139, 141, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 143, 53500, 40350, faction_ottoman, 144, 137, 138, 142, 141, 145, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 144, 53625, 40675, faction_serbia, 115, 136, 137, 143, 145, 122, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 145, 54175, 40375, faction_ottoman, 144, 143, 169, 170, 155, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 146, 53800, 38825, faction_ottoman, 140, 147, 149, 150, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 147, 54328, 39284, faction_ottoman, 141, 140, 146, 149, 148, 169, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 148, 55200, 39425, faction_ottoman, 147, 167, 164, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 149, 54200, 38850, faction_ottoman, 147, 146, 151, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 150, 53950, 38525, faction_greece, 146, 151, 152, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 151, 54550, 38425, faction_greece, 150, 149, 152, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 152, 54300, 38050, faction_greece, 150, 151, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 153, 55225, 37075, faction_ottoman, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 154, 56175, 37475, faction_ottoman, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 155, 54625, 40800, faction_romania, 125, 122, 145, 170, 168, 156, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 156, 55400, 40800, faction_romania, 157, 125, 155, 168, 166, 160, 159, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 157, 55700, 41425, faction_moldavia, 158, 125, 156, 159, 162, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 158, 55375, 41925, faction_moldavia, 134, 124, 125, 157, 162, 163, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 159, 56100, 40825, faction_ottoman, 161, 157, 156, 160, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 160, 55825, 40500, faction_ottoman, 159, 156, 166, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 161, 56350, 41325, faction_russia, 159, 162, 171, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 162, 56025, 41900, faction_russia, 161, 157, 158, 163, 172, 171, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 163, 55300, 42300, faction_russia, 173, 134, 158, 162, 172, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 164, 55875, 39500, faction_ottoman, 165, 148, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 165, 55650, 39950, faction_ottoman, 168, 166, 167, 164, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 166, 55675, 40325, faction_ottoman, 156, 168, 165, 160, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 167, 55050, 39850, faction_ottoman, 168, 169, 148, 165, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 168, 55045, 40279, faction_ottoman, 155, 156, 170, 169, 167, 165, 166, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 169, 54525, 39925, faction_ottoman, 170, 145, 141, 147, 167, 168, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 170, 54525, 40400, faction_ottoman, 155, 145, 169, 167, 168, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 171, 56574, 41862, faction_russia, 161, 162, 172, 179, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 172, 56094, 42582, faction_russia, 175, 173, 163, 162, 171, 178, 177, 176, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 173, 55442, 42748, faction_russia, 174, 133, 134, 163, 172, 175, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 174, 55074, 43346, faction_russia, 196, 190, 133, 173, 175, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 175, 55994, 43208, faction_russia, 201, 174, 173, 172, 176, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 176, 56546, 43024, faction_russia, 201, 175, 172, 177, 184, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 177, 56868, 42656, faction_russia, 176, 172, 178, 183, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 178, 57102, 42344, faction_russia, 177, 172, 179, 182, 183, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 179, 57102, 41876, faction_russia, 171, 178, 182, 180, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 180, 57726, 41681, faction_russia, 179, 182, 181, 189, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 181, 58272, 41837, faction_russia, 180, 182, 187, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 182, 57921, 42383, faction_russia, 183, 178, 179, 180, 181, 187, 186, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 183, 57492, 42929, faction_russia, 185, 184, 177, 178, 182, 186, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 184, 56946, 43436, faction_russia, 201, 176, 183, 185, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 185, 57609, 43319, faction_russia, 184, 183, 186, 314, 244, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 186, 58350, 42812, faction_russia, 185, 183, 182, 187, 188, 244, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 187, 58857, 42188, faction_russia, 186, 182, 181, 188, 312, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 188, 59169, 42539, faction_russia, 186, 187, 244, 312, 320, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 189, 57921, 41057, faction_russia, 180, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 190, 54138, 43475, faction_russia, 192, 191, 132, 133, 174, 196, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 191, 53631, 43826, faction_russia, 99, 195, 194, 193, 190, 192, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 192, 54177, 44177, faction_russia, 99, 191, 196, 197, 202, 203, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 193, 53397, 43163, faction_russia, 194, 106, 132, 191, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 194, 53124, 43553, faction_russia, 195, 97, 106, 193, 191, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 195, 52851, 43826, faction_russia, 98, 97, 194, 191, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 196, 54996, 43865, faction_russia, 197, 192, 190, 174, 201, 199, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 197, 54801, 44333, faction_russia, 202, 192, 196, 199, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 198, 55854, 44957, faction_russia, 206, 202, 199, 200, 315, 242, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 199, 55542, 44372, faction_russia, 198, 197, 196, 201, 200, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 200, 56400, 44294, faction_russia, 198, 199, 201, 242, 314, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 201, 56244, 43748, faction_russia, 200, 199, 196, 175, 176, 184, 314, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 202, 54684, 44762, faction_russia, 203, 192, 197, 198, 205, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 203, 54294, 44996, faction_russia, 205, 204, 100, 192, 202, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 204, 53748, 45113, faction_russia, 205, 203, 100, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 205, 54207, 45465, faction_russia, 206, 202, 203, 204, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 206, 55048, 45552, faction_russia, 208, 207, 205, 198, 315, 239, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 207, 54352, 46219, faction_russia, 208, 206, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 208, 54990, 46190, faction_russia, 207, 206, 238, 239, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 209, 55876, 47201, faction_russia, 210, 211, 238, 256, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 210, 55369, 47201, faction_russia, 212, 211, 209, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 211, 55837, 47747, faction_russia, 213, 212, 210, 209, 256, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 212, 55096, 47669, faction_russia, 215, 217, 219, 210, 211, 213, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 213, 55408, 48215, faction_russia, 215, 212, 211, 256, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 214, 54550, 49307, faction_russia, 220, 228, 215, 256, 257, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 215, 54745, 48371, faction_russia, 214, 216, 217, 212, 213, 256, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 216, 53770, 47630, faction_russia, 215, 217, 218, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 217, 54433, 47396, faction_russia, 216, 218, 219, 212, 215, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 218, 53926, 46889, faction_russia, 216, 217, 219, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 219, 54589, 46889, faction_russia, 218, 217, 212, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 220, 54277, 50204, faction_sweden, 221, 214, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 221, 51859, 49463, faction_sweden, 220, 214, 228, 229, 222, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 222, 50611, 48059, faction_sweden, 221, 230, 223, 227, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 223, 50416, 47201, faction_sweden, 227, 226, 224, 234, 321, 230, 222, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 224, 50221, 46733, faction_sweden, 223, 226, 225, 234, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 225, 49649, 46337, faction_sweden, 226, 224, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 226, 49297, 47041, faction_sweden, 227, 223, 224, 225, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 227, 49737, 47657, faction_sweden, 222, 223, 226, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 228, 52993, 49109, faction_sweden, 214, 221, 229, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 229, 52377, 48405, faction_sweden, 228, 221, 230, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 230, 51805, 47877, faction_sweden, 229, 222, 223, 231, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 231, 51717, 46997, faction_sweden, 230, 223, 234, 233, 232, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 232, 52333, 46513, faction_sweden, 231, 233, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 233, 51761, 46205, faction_sweden, 232, 231, 234, 236, 235, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 234, 51101, 46337, faction_sweden, 224, 223, 231, 233, 235, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 235, 51321, 45721, faction_sweden, 234, 233, 236, 237, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 236, 51893, 45589, faction_sweden, 237, 235, 233, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 237, 51453, 45193, faction_sweden, 235, 236, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 238, 55923, 46477, faction_russia, 209, 240, 239, 208, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 239, 55710, 45855, faction_russia, 238, 208, 206, 315, 240, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 240, 56325, 46142, faction_russia, 238, 239, 315, 317, 256, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 241, 57678, 45773, faction_russia, 317, 316, 242, 243, 254, 255, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 242, 56957, 44765, faction_russia, 316, 315, 198, 200, 314, 318, 243, 241, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 243, 58659, 44995, faction_russia, 254, 241, 242, 318, 319, 320, 252, 253, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 244, 58344, 43385, faction_russia, 319, 314, 185, 186, 188, 320, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 245, 60060, 41773, faction_russia, 312, 250, 309, 249, 247, 246, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 246, 59410, 41022, faction_russia, 189, 245, 247, 310, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 247, 60736, 40733, faction_caucasia, 310, 246, 245, 249, 308, 322, 321, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 248, 62138, 40092, faction_russia, 308, 249, 323, 238, 329, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 249, 61308, 41409, faction_russia, 248, 308, 247, 245, 309, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 250, 60528, 42345, faction_russia, 311, 312, 245, 309, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 251, 60736, 43645, faction_russia, 252, 320, 311, 313, 262, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 252, 60432, 44300, faction_russia, 253, 243, 320, 251, 262, 261, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 253, 60222, 45350, faction_russia, 254, 243, 252, 261, 260, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 254, 59172, 45840, faction_russia, 255, 241, 243, 253, 260, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 255, 58332, 46680, faction_russia, 258, 256, 317, 241, 254, 260, 259, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 256, 56582, 48010, faction_russia, 257, 215, 213, 211, 209, 238, 240, 317, 255, 258, -1, terrain_plains),
(call_script, "script_add_province", 257, 56792, 49480, faction_russia, 220, 214, 256, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 258, 57702, 47730, faction_russia, 256, 255, 259, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 259, 59172, 48010, faction_russia, 258, 255, 260, 266, 267, 269, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 260, 61622, 46190, faction_russia, 266, 259, 255, 254, 253, 261, 265, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 261, 61762, 45140, faction_russia, 260, 253, 252, 262, 263, 264, 265, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 262, 61902, 44335, faction_russia, 261, 252, 251, 313, 263, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 263, 63566, 43711, faction_russia, 262, 261, 264, 274, 332, 334, 335, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 264, 64034, 44439, faction_russia, 265, 261, 263, 274, 273, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 265, 63165, 46177, faction_russia, 268, 266, 260, 261, 264, 273, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 266, 61822, 47284, faction_russia, 267, 259, 260, 265, 268, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 267, 61744, 48454, faction_russia, 269, 259, 266, 268, 270, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 268, 63343, 48181, faction_russia, 270, 267, 266, 265, 273, 272, 271, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 269, 60446, 49174, faction_russia, 259, 267, 270, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 270, 62998, 49464, faction_russia, 269, 267, 268, 271, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 271, 65460, 49254, faction_russia, 270, 268, 272, 278, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 272, 65822, 47536, faction_russia, 271, 268, 273, 276, 277, 278, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 273, 65192, 46087, faction_russia, 272, 268, 265, 264, 274, 275, 276, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 274, 65232, 44642, faction_russia, 273, 264, 263, 275, 335, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 275, 66340, 45009, faction_russia, 274, 273, 276, 335, 336, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 276, 68117, 45611, faction_russia, 277, 272, 273, 275, 282, 283, 336, 338, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 277, 68438, 47323, faction_russia, 278, 272, 276, 282, 281, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 278, 68438, 48607, faction_russia, 279, 271, 272, 277, 281, 280, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 279, 67475, 49784, faction_russia, 278, 280, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 280, 70311, 50585, faction_russia, 279, 278, 281, 286, 291, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 281, 74150, 45625, faction_russia, 280, 278, 277, 282, 284, 287, 288, 286, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 282, 70909, 46225, faction_russia, 277, 276, 283, 284, 281, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 283, 70789, 45025, faction_russia, 282, 276, 284, 285, 338, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 284, 73309, 44545, faction_russia, 282, 283, 285, 287, 281, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 285, 72469, 43945, faction_russia, 283, 284, 287, 338, 339, 340, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 286, 74030, 48265, faction_russia, 280, 281, 288, 290, 291, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 287, 75950, 43585, faction_russia, 285, 284, 281, 288, 289, 496, 497, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 288, 77510, 44665, faction_russia, 290, 286, 281, 287, 289, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 289, 79910, 44305, faction_russia, 287, 288, 290, 296, 499, 497, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 290, 77963, 46039, faction_russia, 291, 286, 288, 289, 296, 295, 292, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 291, 76841, 49813, faction_russia, 280, 286, 290, 292, 293, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 292, 79697, 48079, faction_russia, 293, 291, 290, 295, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 293, 80513, 49915, faction_russia, 291, 292, 294, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 294, 85291, 49064, faction_russia, 293, 295, 299, 305, 307, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 295, 83811, 46429, faction_russia, 294, 292, 290, 296, 297, 299, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 296, 82101, 43807, faction_russia, 289, 290, 295, 297, 499, 502, 506, 505, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 297, 84723, 44491, faction_russia, 296, 295, 299, 298, 504, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 298, 86584, 43419, faction_china, 297, 299, 300, 301, 507, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 299, 86928, 45655, faction_russia, 305, 294, 295, 297, 298, 300, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 300, 88787, 43192, faction_china, 299, 298, 301, 302, 304, 514, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 301, 87950, 42262, faction_china, 298, 300, 507, 513, 514, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 302, 89438, 40960, faction_china, 300, 514, 512, 518, 533, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 303, 91112, 42169, faction_china, 304, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 304, 90275, 43564, faction_china, 303, 300, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 305, 90065, 47483, faction_russia, 306, 307, 294, 299, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 306, 93285, 45943, faction_russia, 307, 305, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 307, 92865, 49163, faction_russia, 294, 305, 306, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 308, 61463, 40316, faction_caucasia, 247, 249, 248, 323, 322, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 309, 61724, 41882, faction_russia, 311, 250, 245, 249, 331, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 310, 59897, 40664, faction_circassia, 246, 247, 321, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 311, 60788, 42794, faction_russia, 313, 251, 320, 312, 250, 309, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 312, 59798, 42380, faction_russia, 187, 188, 320, 311, 250, 245, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 313, 61767, 43422, faction_russia, 262, 251, 311, 332, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 314, 57248, 44060, faction_russia, 242, 200, 201, 184, 185, 244, 319, 318, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 315, 56072, 45433, faction_russia, 239, 206, 198, 242, 316, 317, 240, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 316, 56932, 45454, faction_russia, 317, 315, 242, 241, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 317, 56932, 46210, faction_russia, 240, 315, 316, 241, 255, 256, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 318, 57751, 44635, faction_russia, 248, 314, 319, 243, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 319, 58255, 44194, faction_russia, 318, 314, 244, 320, 243, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 320, 59389, 43627, faction_russia, 243, 319, 244, 188, 312, 311, 251, 252, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 321, 60239, 40172, faction_russia, 310, 247, 322, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 322, 60745, 39896, faction_russia, 321, 247, 308, 323, 324, 376, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 323, 61481, 39712, faction_russia, 308, 322, 324, 328, 248, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 324, 61343, 39229, faction_russia, 322, 323, 328, 325, 326, 375, 376, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 325, 61849, 38930, faction_russia, 324, 326, 328, 327, 450, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 326, 61826, 38700, faction_russia, 324, 325, 450, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 327, 62286, 38953, faction_russia, 325, 328, 329, 330, 451, 450, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 328, 62102, 39321, faction_russia, 323, 324, 325, 327, 329, 248, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 329, 62723, 39252, faction_russia, 248, 328, 327, 330, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 330, 62884, 38700, faction_russia, 329, 327, 451, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 331, 63247, 41930, faction_russia, 309, 332, 334, 333, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 332, 62558, 42937, faction_russia, 313, 311, 309, 331, 334, 263, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 333, 64042, 40605, faction_khiva, 331, 334, 348, 356, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 334, 65102, 42407, faction_russia, 263, 332, 331, 333, 348, 343, 341, 335, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 335, 66480, 43573, faction_russia, 275, 274, 263, 334, 341, 342, 337, 336, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 336, 68070, 44315, faction_russia, 276, 275, 335, 337, 338, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 337, 68282, 43467, faction_russia, 336, 335, 342, 338, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 338, 70138, 43732, faction_russia, 276, 336, 337, 342, 339, 285, 283, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 339, 71841, 42322, faction_russia, 285, 338, 342, 347, 340, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 340, 73105, 42480, faction_russia, 285, 339, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 341, 68080, 42011, faction_russia, 335, 334, 343, 344, 345, 342, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 342, 70157, 42212, faction_russia, 337, 335, 341, 345, 346, 347, 339, 338, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 343, 67209, 41006, faction_russia, 341, 334, 348, 349, 350, 344, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 344, 68951, 40336, faction_russia, 341, 343, 350, 354, 361, 345, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 345, 69956, 40604, faction_russia, 342, 341, 344, 362, 346, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 346, 71564, 40537, faction_russia, 342, 345, 362, 363, 347, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 347, 71899, 41140, faction_russia, 339, 342, 346, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 348, 65318, 40456, faction_khiva, 334, 333, 356, 358, 349, 343, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 349, 66496, 40146, faction_khiva, 343, 348, 358, 359, 351, 350, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 350, 67736, 39836, faction_bukhara, 343, 349, 351, 352, 354, 344, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 351, 67612, 39030, faction_bukhara, 350, 349, 359, 352, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 352, 68542, 38658, faction_bukhara, 350, 351, 359, 353, 364, 354, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 353, 69038, 38162, faction_bukhara, 359, 352, 364, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 354, 69193, 39278, faction_kokand, 344, 350, 352, 364, 355, 361, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 355, 70122, 39308, faction_kokand, 354, 364, 361, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 356, 64901, 38932, faction_khiva, 333, 348, 358, 357, 461, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 357, 66232, 38542, faction_khiva, 356, 358, 359, 360, 461, 462, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 358, 65959, 39478, faction_khiva, 348, 356, 357, 359, 349, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 359, 67636, 38464, faction_khiva, 349, 358, 357, 360, 353, 352, 351, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 360, 67558, 37801, faction_khiva, 357, 359, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 361, 70775, 39199, faction_kokand, 365, 364, 355, 354, 344, 362, 363, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 362, 70985, 39934, faction_kokand, 345, 361, 363, 346, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 363, 71661, 39622, faction_kokand, 361, 362, 346, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 364, 69486, 38608, faction_bukhara, 353, 352, 354, 355, 361, 365, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 365, 70786, 38218, faction_bukhara, 364, 361, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 366, 56302, 39004, faction_ottoman, 164, 367, 395, 398, 371, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 367, 56228, 38043, faction_ottoman, 366, 395, 368, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 368, 57122, 37815, faction_ottoman, 367, 395, 370, 369, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 369, 58598, 37856, faction_ottoman, 368, 370, 372, 375, 374, 377, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 370, 57827, 38207, faction_ottoman, 368, 395, 398, 372, 369, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 371, 57417, 39478, faction_ottoman, 366, 395, 398, 372, 396, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 372, 58639, 38676, faction_ottoman, 396, 371, 398, 370, 369, 375, 373, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 373, 59582, 39291, faction_ottoman, 396, 372, 375, 376, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 374, 59952, 38021, faction_ottoman, 375, 369, 377, 380, 379, 397, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 375, 59952, 38734, faction_ottoman, 373, 372, 369, 374, 397, 450, 324, 376, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 376, 60727, 39261, faction_ottoman, 322, 324, 375, 373, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 377, 58885, 37569, faction_ottoman, 369, 374, 380, 383, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 378, 57942, 36995, faction_ottoman, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 379, 60402, 37610, faction_ottoman, 374, 380, 381, 387, 388, 397, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 380, 59623, 37446, faction_ottoman, 374, 377, 383, 382, 381, 379, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 381, 60238, 36954, faction_ottoman, 379, 380, 382, 386, 387, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 382, 59623, 36708, faction_ottoman, 380, 383, 385, 384, 386, 381, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 383, 59008, 37159, faction_ottoman, 377, 380, 382, 385, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 384, 59213, 36339, faction_ottoman, 382, 385, 399, 472, 473, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 385, 58804, 36566, faction_ottoman, 383, 382, 384, 399, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 386, 60773, 36225, faction_ottoman, 382, 381, 387, 389, 390, 391, 477, 476, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 387, 61049, 37421, faction_ottoman, 388, 379, 381, 386, 389, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 388, 61739, 37283, faction_ottoman, 397, 387, 389, 452, 450, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 389, 61693, 36639, faction_ottoman, 388, 387, 386, 390, 454, 452, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 390, 62061, 35949, faction_ottoman, 389, 386, 391, 392, 454, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 391, 62061, 35121, faction_ottoman, 386, 390, 392, 393, 477, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 392, 62751, 35765, faction_ottoman, 390, 391, 393, 457, 454, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 393, 62889, 35213, faction_ottoman, 391, 392, 457, 394, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 394, 63027, 34753, faction_ottoman, 393, 480, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 395, 56714, 38427, faction_ottoman, 366, 367, 368, 370, 398, 371, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 396, 58352, 39441, faction_ottoman, 371, 372, 373, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 397, 61001, 38293, faction_ottoman, 375, 374, 379, 388, 450, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 398, 57343, 38851, faction_ottoman, 371, 395, 370, 372, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 399, 58625, 35466, faction_ottoman, 400, 385, 384, 539, 474, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 400, 58747, 35794, faction_ottoman, 400, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 401, 9802, 41948, faction_usa, 547, 404, 402, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 402, 8838, 40559, faction_usa, 401, 404, 405, 403, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 403, 7618, 37997, faction_usa, 402, 405, 406, 677, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 404, 10978, 40598, faction_usa, 547, 401, 402, 405, 407, 410, 411, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 405, 8835, 38739, faction_usa, 402, 403, 406, 407, 404, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 406, 9875, 36709, faction_usa, 407, 405, 403, 678, 408, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 407, 10785, 38809, faction_usa, 404, 405, 406, 409, 410, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 408, 11765, 36849, faction_usa, 409, 406, 679, 446, 445, 416, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 409, 12745, 38739, faction_usa, 410, 407, 408, 416, 415, 414, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 410, 12955, 40349, faction_usa, 411, 404, 407, 409, 414, 413, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 411, 13305, 41959, faction_usa, 549, 547, 404, 410, 413, 412, 450, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 412, 16290, 41993, faction_usa, 551, 550, 411, 413, 421, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 413, 15730, 40953, faction_usa, 412, 411, 410, 414, 420, 421, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 414, 15210, 39713, faction_usa, 413, 410, 409, 415, 419, 420, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 415, 15025, 38439, faction_usa, 414, 409, 416, 419, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 416, 14877, 37231, faction_usa, 415, 409, 408, 445, 418, 419, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 417, 15803, 35545, faction_usa, 418, 445, 427, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 418, 16233, 36928, faction_usa, 419, 416, 445, 417, 427, 426, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 419, 16787, 38374, faction_usa, 420, 414, 415, 416, 418, 426, 425, 424, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 420, 17268, 39887, faction_usa, 421, 413, 414, 419, 424, 423, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 421, 17688, 41273, faction_usa, 551, 412, 413, 420, 423, 552, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 422, 19621, 41480, faction_usa, 552, 423, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 423, 18778, 40840, faction_usa, 422, 421, 420, 424, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 424, 18118, 39030, faction_usa, 423, 420, 419, 425, 436, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 425, 18918, 37960, faction_usa, 436, 424, 419, 426, 433, 434, 435, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 426, 18170, 37350, faction_usa, 425, 419, 418, 427, 428, 430, 432, 433, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 427, 16878, 36114, faction_usa, 417, 418, 426, 428, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 428, 17805, 36052, faction_usa, 427, 426, 430, 429, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 429, 19247, 34138, faction_usa, 428, 430, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 430, 18952, 36026, faction_usa, 426, 428, 429, 431, 432, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 431, 19896, 36557, faction_usa, 432, 430, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 432, 20899, 37265, faction_usa, 433, 426, 430, 431, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 433, 21411, 38001, faction_usa, 438, 434, 425, 426, 432, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 434, 20604, 38381, faction_usa, 435, 425, 433, 438, 439, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 435, 20223, 39122, faction_usa, 437, 436, 425, 434, 439, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 436, 19203, 39075, faction_usa, 424, 425, 435, 437, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 437, 20143, 40327, faction_usa, 422, 436, 435, 553, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 438, 22259, 38672, faction_usa, 440, 439, 434, 433, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 439, 22035, 39372, faction_usa, 441, 440, 438, 434, 435, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 440, 22987, 39232, faction_usa, 438, 439, 441, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 441, 23022, 40106, faction_usa, 440, 439, 553, 443, 442, 554, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 442, 24015, 39772, faction_usa, 441, 443, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 443, 24192, 40489, faction_usa, 554, 441, 442, 444, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 444, 25452, 41142, faction_usa, 555, 554, 443, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 445, 14106, 36181, faction_usa, 417, 418, 416, 408, 446, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 446, 13371, 35250, faction_usa, 445, 408, 679, 680, 682, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 447, 6491, 47746, faction_russia, 547, 548, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 448, 8185, 49440, faction_russia, 548, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 449, 2708, 29999, faction_hawaii, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 450, 62133, 38067, faction_iran, 325, 326, 375, 397, 388, 452, 453, 451, 327, -1, -1, terrain_plains),
(call_script, "script_add_province", 451, 62883, 38157, faction_iran, 330, 327, 450, 453, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 452, 62643, 37047, faction_iran, 450, 388, 389, 454, 455, 453, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 453, 63183, 37617, faction_iran, 451, 450, 452, 455, 456, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 454, 62763, 36327, faction_iran, 452, 389, 390, 392, 457, 458, 455, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 455, 63576, 36777, faction_iran, 453, 452, 454, 458, 460, 456, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 456, 64185, 37444, faction_iran, 453, 455, 460, 461, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 457, 63518, 35559, faction_iran, 393, 392, 454, 458, 465, 466, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 458, 64127, 36313, faction_iran, 455, 454, 457, 465, 459, 460, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 459, 64881, 36313, faction_iran, 460, 458, 465, 464, -1, -1, -1, -1, -1, -1, -1, terrain_plains), 
(call_script, "script_add_province", 460, 65142, 37125, faction_iran, 461, 456, 455, 458, 459, 464, 462, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 461, 65432, 37995, faction_iran, 356, 357, 462, 460, 456, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 462, 66476, 37183, faction_iran, 357, 461, 460, 464, 463, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 463, 66728, 35986, faction_iran, 462, 464, 467, 468, 470, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 464, 65531, 35734, faction_iran, 460, 459, 465, 467, 463, 462, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 465, 64964, 34600, faction_iran, 466, 457, 458, 459, 464, 467, 469, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 466, 64198, 34495, faction_iran, 457, 465, 469, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 467, 65846, 35104, faction_iran, 464, 465, 469, 468, 463, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 468, 66539, 34663, faction_iran, 463, 467, 469, 471, 470, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 469, 66161, 33781, faction_iran, 466, 465, 467, 468, 471, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 470, 67358, 34978, faction_iran, 463, 468, 471, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 471, 67547, 33781, faction_iran, 469, 468, 470, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 472, 59613, 35986, faction_ottoman, 386, 382, 384, 473, 475, 476, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 473, 59136, 35679, faction_ottoman, 472, 384, 399, 400, 474, 475, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 474, 59163, 35139, faction_ottoman, 399, 473, 475, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 475, 60080, 34893, faction_ottoman, 476, 472, 473, 474, 481, 478, 477, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 476, 60572, 35508, faction_ottoman, 386, 472, 475, 477, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 477, 61597, 34647, faction_rashidi, 391, 386, 476, 475, 478, 479, 480, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 478, 61176, 33724, faction_rashidi, 477, 475, 481, 482, 479, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 479, 62508, 32096, faction_saudi, 478, 482, 483, 484, 480, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 480, 64538, 31574, faction_saudi, 394, 477, 479, 484, 487, 489, 490, 491, 493, 495, -1, terrain_plains),
(call_script, "script_add_province", 481, 59284, 34163, faction_ottoman, 475, 478, 482, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 482, 60428, 32863, faction_ottoman, 481, 478, 479, 483, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 483, 60991, 31597, faction_ottoman, 482, 479, 484, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 484, 62343, 30453, faction_ottoman, 483, 479, 480, 487, 485, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 485, 62248, 29275, faction_ottoman, 484, 487, 486, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 486, 63141, 28781, faction_britain, 485, 487, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 487, 63825, 29845, faction_kathiri, 486, 485, 484, 480, 488, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 488, 64775, 29617, faction_mahra, 487, 489, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 489, 65535, 30415, faction_oman, 488, 480, 490, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 490, 66333, 31061, faction_oman, 489, 480, 491, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 491, 66523, 31973, faction_oman, 490, 480, 493, 492, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 492, 66447, 32657, faction_oman, 494, 493, 491, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 493, 65307, 32581, faction_trucial, 480, 491, 492, 494, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 494, 65915, 33303, faction_trucial, 493, 492, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 495, 64393, 33173, faction_qatar, 480, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 496, 75339, 42259, faction_china, 285, 287, 497, 498, 631, 630, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 497, 77283, 42637, faction_china, 287, 289, 499, 498, 496, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 498, 77607, 41233, faction_china, 497, 496, 627, 629, 501, 500, 499, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 499, 78957, 42421, faction_china, 498, 497, 289, 296, 502, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 500, 80037, 41611, faction_china, 501, 498, 499, 502, 503, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 501, 80037, 40423, faction_china, 500, 498, 629, 628, 624, 503, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 502, 81927, 42313, faction_china, 296, 500, 503, 506, 509, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 503, 82089, 41179, faction_china, 502, 500, 501, 624, 621, 618, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 504, 84587, 43848, faction_china, 297, 505, 507, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 505, 84407, 43218, faction_china, 504, 506, 296, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 506, 84257, 42378, faction_china, 502, 296, 505, 507, 508, 509, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 507, 86294, 42424, faction_china, 298, 301, 513, 508, 506, 504, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 508, 86041, 41803, faction_china, 507, 512, 511, 509, 506, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 509, 84707, 41228, faction_china, 506, 502, 618, 510, 511, 508, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 510, 85448, 40332, faction_china, 509, 618, 617, 516, 511, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 511, 86057, 41001, faction_china, 509, 510, 508, 512, 515, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 512, 87536, 41117, faction_china, 513, 514, 302, 518, 515, 511, 508, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 513, 87449, 41842, faction_china, 301, 514, 512, 507, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 514, 88464, 41581, faction_china, 301, 300, 302, 512, 513, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 515, 87101, 40566, faction_china, 511, 512, 518, 516, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 516, 86195, 39640, faction_china, 616, 617, 510, 511, 515, 518, 517, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 517, 86915, 39208, faction_china, 519, 516, 518, 533, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 518, 87875, 40024, faction_china, 517, 515, 516, 512, 302, 533, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 519, 86579, 38584, faction_china, 517, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 520, 67647, 36512, faction_durrani, 360, 462, 463, 470, 521, 523, 524, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 521, 68515, 35449, faction_afghanistan, 520, 470, 531, 530, 522, 523, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 522, 69475, 36169, faction_afghanistan, 523, 521, 530, 528, 526, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 523, 68803, 36841, faction_afghanistan, 524, 520, 521, 522, 526, 525, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 524, 68755, 37561, faction_afghanistan, 359, 360, 520, 523, 525, 353, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 525, 69715, 37705, faction_afghanistan, 364, 353, 524, 523, 526, 527, 365, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 526, 70099, 36841, faction_afghanistan, 527, 525, 523, 522, 528, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 527, 70339, 37705, faction_afghanistan, 365, 525, 526, 528, 636, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 528, 71228, 37174, faction_afghanistan, 527, 526, 522, 530, 529, 562, 636, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 529, 71140, 35326, faction_britain, 528, 530, 532, 566, 565, 563, 562, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 530, 69688, 34754, faction_afghanistan, 522, 521, 531, 532, 529, 528, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 531, 68940, 33742, faction_kalat, 471, 470, 521, 530, 532, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 532, 70348, 33346, faction_britain, 531, 530, 529, 566, 568, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 533, 87952, 39384, faction_korea, 517, 518, 302, 534, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 534, 88128, 38812, faction_korea, 533, 535, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 535, 88387, 38416, faction_korea, 534, 536, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 536, 88883, 38075, faction_korea, 535, 537, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 537, 89162, 37579, faction_korea, 536, 538, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 538, 89111, 37063, faction_korea, 537, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 539, 58290, 34899, faction_ottoman, 399, 540, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 540, 57318, 34755, faction_ottoman, 539, 541, 542, 543, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 541, 55986, 34935, faction_ottoman, 540, 543, 741, 782, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 542, 58413, 32946, faction_ottoman, 540, 543, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 543, 56583, 33007, faction_ottoman, 540, 541, 542, 741, 782, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 544, 38243, 51165, faction_denmark, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 545, 42173, 48323, faction_denmark, 546, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 546, 43275, 48464, faction_denmark, 545, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 547, 10616, 44446, faction_britain, 447, 548, 559, 549, 411, 404, 401, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 548, 11101, 47938, faction_britain, 448, 447, 547, 559, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 549, 13817, 44834, faction_britain, 559, 547, 411, 550, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 550, 16145, 44543, faction_britain, 559, 549, 411, 412, 551, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 551, 19346, 45319, faction_britain, 560, 550, 412, 421, 552, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 552, 21286, 43282, faction_britain, 551, 421, 422, 553, 554, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 553, 21530, 40506, faction_britain, 552, 437, 441, 455, 456, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 554, 24235, 42231, faction_britain, 557, 552, 441, 443, 444, 555, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 555, 26516, 41561, faction_britain, 554, 444, 556, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 556, 27295, 41069, faction_britain, 555, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 557, 26390, 44734, faction_britain, 558, 554, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 558, 29324, 44309, faction_britain, 557, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 559, 15487, 48222, faction_britain, 548, 547, 549, 550, 560, -1, -1, -1, -1, -1, -1, terrain_plains), 
(call_script, "script_add_province", 560, 21591, 48419, faction_britain, 559, 551, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 561, 73196, 37107, faction_britain, 562, 636, 638, 739, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 562, 72580, 36267, faction_britain, 528, 529, 563, 564, 572, 636, 638, 738, 739, 561, -1, terrain_plains),
(call_script, "script_add_province", 563, 72210, 35208, faction_britain, 529, 562, 564, 565, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 564, 72750, 34728, faction_britain, 562, 563, 565, 572, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 565, 72270, 34008, faction_rajput, 529, 563, 564, 566, 567, 571, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 566, 71430, 33528, faction_rajput, 529, 532, 565, 567, 569, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 567, 72450, 33108, faction_rajput, 565, 566, 569, 571, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 568, 70770, 32448, faction_britain, 532, 569, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 569, 71490, 32268, faction_britain, 532, 566, 567, 603, 570, 571, 568, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 570, 72456, 30451, faction_britain, 569, 571, 575, 577, 578, 580, 582, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 571, 73327, 32495, faction_britain, 565, 567, 569, 570, 572, 574, 575, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 572, 73546, 34612, faction_britain, 562, 564, 565, 571, 573, 574, 600, 738, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 573, 74349, 33882, faction_oudh, 572, 574, 600, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 574, 75006, 33371, faction_britain, 571, 572, 573, 575, 576, 590, 591, 592, 600, -1, -1, terrain_plains),
(call_script, "script_add_province", 575, 73911, 31911, faction_britain, 570, 571, 574, 576, 577, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 576, 74568, 32276, faction_britain, 574, 575, 577, 590, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 577, 73765, 31035, faction_hyderabad, 570, 575, 576, 578, 579, 588, 590, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 578, 73327, 29940, faction_hyderabad, 570, 577, 579, 580, 583, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 579, 74349, 30232, faction_hyderabad, 577, 578, 583, 587, 588, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 580, 73327, 28699, faction_mysore, 570, 578, 581, 582, 583, 584, 585, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 581, 72865, 28303, faction_britain, 580, 585, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 582, 72568, 29062, faction_portugal, 570, 580, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 583, 74242, 28894, faction_britain, 578, 579, 580, 584, 587, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 584, 74350, 27462, faction_britain, 580, 583, 585, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 585, 73558, 27102, faction_britain, 580, 584, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 586, 75034, 26058, faction_britain, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 587, 75270, 30056, faction_britain, 579, 583, 588, 589, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 588, 74975, 30865, faction_britain, 577, 579, 587, 589, 590, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 589, 76445, 31243, faction_britain, 587, 588, 590, 592, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 590, 75686, 31657, faction_britain, 576, 577, 574, 588, 591, 589, 592, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 591, 75686, 32830, faction_britain, 574, 590, 592, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 592, 76652, 32830, faction_britain, 574, 589, 590, 591, 593, 595, 596, 601, 602, -1, -1, terrain_plains),
(call_script, "script_add_province", 593, 77549, 32554, faction_britain, 592, 594, 596, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 594, 78170, 32347, faction_britain, 593, 596, 599, 604, 608, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 595, 76898, 34069, faction_sikkim, 592, 601, 602, 734, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 596, 78682, 33561, faction_britain, 592, 593, 594, 599, 597, 598, 602, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 597, 78778, 34327, faction_britain, 596, 598, 602, 609, 730, 731, 733, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 598, 79017, 33053, faction_britain, 596, 597, 599, 608, 609, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 599, 78646, 32417, faction_britain, 594, 596, 598, 608, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 600, 74777, 34537, faction_nepal, 572, 573, 574, 601, 736, 738, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 601, 76208, 33954, faction_nepal, 592, 595, 600, 734, 736, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 602, 77586, 34007, faction_bhutan, 592, 595, 596, 597, 733, 734, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 603, 71850, 31968, faction_britain, 569, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 604, 79194, 30810, faction_britain, 594, 605, 608, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 605, 80031, 29919, faction_britain, 604, 606, 607, 608, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 606, 80904, 28762, faction_britain, 605, 607, 610, 613, 614, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 607, 80363, 31653, faction_burma, 605, 608, 609, 610, 606, 639, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 608, 79399, 31289, faction_burma, 594, 598, 599, 604, 605, 607, 609, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 609, 79831, 33257, faction_burma, 597, 598, 607, 608, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 610, 81315, 30032, faction_siam, 606, 607, 611, 612, 613, 639, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 611, 82659, 29444, faction_siam, 610, 612, 639, 640, 641, 642, 643, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 612, 81993, 28442, faction_siam, 610, 611, 613, 643, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 613, 81525, 28286, faction_siam, 606, 610, 612, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 614, 81372, 26540, faction_siam, 606, 613, 615, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 615, 81972, 25940, faction_siam, 614, 649, 650, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 616, 85157, 39077, faction_china, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 617, 84517, 39813, faction_china, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 618, 83685, 40645, faction_china, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 619, 84514, 38616, faction_china, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 620, 83595, 39354, faction_china, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 621, 82846, 39890, faction_china, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 622, 85527, 37750, faction_china, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 623, 86424, 37566, faction_china, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 624, 81881, 39031, faction_china, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 625, 83410, 38224, faction_china, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 626, 84390, 37629, faction_china, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 627, 76888, 39723, faction_china, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 628, 80247, 39051, faction_china, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 629, 78687, 39415, faction_china, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 630, 74222, 41578, faction_china, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 631, 75368, 40485, faction_china, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 632, 73694, 40377, faction_china, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 633, 72329, 38973, faction_china, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 634, 74084, 38973, faction_china, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 635, 75605, 39090, faction_china, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 636, 72407, 37881, faction_china, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 637, 75878, 38076, faction_china, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 638, 74045, 37803, faction_china, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 639, 81964, 31138, faction_laos, 607, 610, 611, 640, 644, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 640, 82909, 30508, faction_siam, 611, 639, 641, 644, 645, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 641, 83728, 29311, faction_champasak, 611, 640, 642, 643, 645, 646, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 642, 83854, 28177, faction_cambodia, 641, 643, 646, 647, 648, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 643, 83035, 28114, faction_cambodia, 611, 612, 641, 642, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 644, 82980, 31681, faction_vietnam, 639, 640, 645, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 645, 83611, 30269, faction_vietnam, 640, 641, 644, 646, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 646, 84651, 28582, faction_vietnam, 641, 642, 645, 647, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 647, 84158, 27557, faction_vietnam, 642, 646, 648, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 648, 83702, 26987, faction_vietnam, 642, 643, 647, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 649, 82106, 25021, faction_perak, 615, 650, 651, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 650, 82871, 24796, faction_pahang, 615, 649, 651, 652, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 651, 82511, 24166, faction_britain, 649, 650, 652, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 652, 83101, 23833, faction_johor, 650, 651, 653, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 653, 83221, 23621, faction_britain, 652, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 654, 85764, 23747, faction_sarawak, 708, 707, 655, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 655, 86714, 24298, faction_brunei, 654, 656, 657, 707, 709, 710, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 656, 86961, 24887, faction_brunei, 655, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 657, 87816, 25134, faction_sulu, 655, 710, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 658, 90370, 25926, faction_maguindanao, 659, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 659, 90685, 26486, faction_spain, 661, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 660, 88200, 26906, faction_spain, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 661, 90043, 27403, faction_spain, 659, 662, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 662, 88999, 28795, faction_spain, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 663, 80760, 24853, faction_aceh, 664, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 664, 81596, 23973, faction_aceh, 665, 667, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 665, 82168, 23577, faction_aceh, 664, 666, 667, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 666, 82652, 23137, faction_aceh, 665, 667, 668, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 667, 82036, 22741, faction_netherlands, 664, 665, 666, 668, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 668, 83004, 21993, faction_netherlands, 666, 667, 669, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 669, 83532, 20981, faction_netherlands, 668, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 670, 84368, 20409, faction_netherlands, 671, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 671, 85304, 20153, faction_netherlands, 670, 672, 673, 674, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 672, 85455, 19884, faction_yogyakarta, 671, 673, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 673, 85650, 19982, faction_surakarta, 671, 672, 674, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 674, 86168, 19984, faction_netherlands, 673, 675, 671, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 675, 87036, 19732, faction_bali, 674, 700, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 676, 8541, 33851, faction_mexico, 677, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 677, 8127, 35559, faction_mexico, 676, 403, 678, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 678, 9577, 34972, faction_mexico, 677, 406, 679, 686, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 679, 10926, 34539, faction_mexico, 408, 678, 686, 685, 680, 446, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 680, 12102, 33867, faction_mexico, 446, 679, 685, 684, 681, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 681, 12830, 33363, faction_mexico, 680, 683, 682, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 682, 12998, 32411, faction_mexico, 446, 681, 683, 692, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 683, 12438, 31739, faction_mexico, 681, 684, 689, 691, 692, 682, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 684, 11374, 32131, faction_mexico, 680, 685, 687, 688, 683, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 685, 11038, 33139, faction_mexico, 679, 686, 687, 684, 680, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 686, 10030, 33307, faction_mexico, 678, 679, 685, 687, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 687, 10870, 31683, faction_mexico, 686, 685, 684, 688, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 688, 10926, 30955, faction_mexico, 687, 684, 689, 690, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 689, 12214, 31179, faction_mexico, 683, 688, 690, 691, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 690, 11822, 30731, faction_mexico, 689, 688, 693, 691, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 691, 12774, 30731, faction_mexico, 689, 690, 693, 694, 692, 683, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 692, 13894, 30339, faction_mexico, 682, 683, 691, 694, 695, 696, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 693, 12214, 30059, faction_mexico, 690, 691, 694, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 694, 13334, 29835, faction_mexico, 693, 691, 692, 695, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 695, 14734, 29667, faction_mexico, 694, 692, 696, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 696, 14622, 30283, faction_mexico, 692, 695, 697, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 697, 15630, 30507, faction_mexico, 696, 699, 698, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 698, 16190, 31347, faction_mexico, 697, 699, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 699, 16302, 30787, faction_mexico, 698, 697, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 700, 87876, 19620, faction_lombok, 675, 701, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 701, 89137, 19350, faction_netherlands, 700, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 702, 90173, 19128, faction_netherlands, 703, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 703, 90839, 19572, faction_portugal, 702, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 704, 87261, 21928, faction_banjar, 705, 709, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 705, 86497, 22396, faction_netherlands, 704, 706, 707, 709, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 706, 85489, 22228, faction_netherlands, 705, 707, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 707, 85881, 22984, faction_pontianak, 654, 655, 705, 706, 708, 709, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 708, 85265, 23333, faction_lanfang, 654, 707, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 709, 87751, 23249, faction_kutai, 655, 704, 705, 707, 710, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 710, 87622, 24369, faction_sulu, 655, 657, 709, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 711, 88869, 21615, faction_netherlands, 712, 713, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 712, 89514, 21486, faction_netherlands, 711, 713, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 713, 89041, 22690, faction_netherlands, 711, 712, 714, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 714, 89987, 23335, faction_netherlands, 713, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 715, 91922, 21787, faction_netherlands, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 716, 91664, 23335, faction_netherlands, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 717, 94810, 21274, faction_netherlands, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 718, 80606, 37402, faction_china, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 719, 80338, 36742, faction_china, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 720, 79842, 37142, faction_china, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 721, 80084, 37780, faction_china, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 722, 79379, 38007, faction_china, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 723, 79039, 37276, faction_china, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 724, 78155, 37412, faction_china, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 725, 78580, 38177, faction_china, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 726, 77510, 38348, faction_china, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 727, 77198, 37256, faction_china, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 728, 78199, 36632, faction_china, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 729, 79118, 36364, faction_china, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 730, 80030, 34948, faction_china, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 731, 79454, 35404, faction_china, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 732, 78614, 35788, faction_china, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 733, 78254, 34948, faction_china, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 734, 77174, 34972, faction_china, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 735, 77318, 36124, faction_china, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 736, 76022, 35188, faction_china, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 737, 76022, 36844, faction_china, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 738, 74390, 35596, faction_china, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 739, 74270, 36652, faction_china, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 740, 80049, 36208, faction_china, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 741, 54576, 33642, faction_ottoman, 541, 543, 742, 743, 782, 862, 863, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 742, 51951, 33642, faction_ottoman, 741, 743, 746, 861, 862, 882, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 743, 51701, 35517, faction_ottoman, 741, 742, 746, 744, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 744, 50162, 36143, faction_tunisia, 743, 745, 746, 748, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 745, 50162, 37313, faction_tunisia, 744, 748, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 746, 47901, 33375, faction_ahaggar, 756, 747, 750, 749, 748, 744, 742, 746, 882, 886, -1, terrain_plains),
(call_script, "script_add_province", 747, 46081, 35080, faction_ahaggar, 746, 756, 752, 750, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 748, 49121, 37240, faction_france, 744, 745, 746, 749, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 749, 48014, 37132, faction_france, 746, 748, 750, 751, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 750, 47121, 36280, faction_france, 752, 746, 747, 749, 751, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 751, 46989, 37173, faction_france, 750, 752, 749, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 752, 45677, 36353, faction_morocco, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 753, 45430, 37091, faction_morocco, 751, 752, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 754, 46010, 37171, faction_spain, 752, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 755, 44319, 36074, faction_morocco, 752, 756, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 756, 43741, 34857, faction_morocco, 746, 747, 752, 755, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 757, 87878, 11166, faction_britain, 746, 756, 752, 750, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 758, 88582, 13792, faction_britain, 744, 745, 746, 749, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 759, 92622, 14196, faction_britain, 746, 748, 750, 751, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 760, 92420, 11166, faction_britain, 752, 746, 747, 749, 751, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 761, 96359, 13489, faction_britain, 750, 752, 749, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 762, 95753, 10156, faction_britain, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 763, 93935, 8439, faction_britain, 751, 752, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 764, 93935, 6318, faction_britain, 752, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 765, 104310, 7671, faction_britain, 752, 756, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 766, 102588, 6332, faction_britain, 746, 747, 752, 755, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 767, 100344, 5150, faction_britain, 746, 747, 752, 755, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 768, 92531, 40384, faction_shogunate, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 769, 92084, 39735, faction_shogunate, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 770, 92733, 38918, faction_shogunate, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 771, 92772, 38193, faction_shogunate, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 772, 92964, 37597, faction_shogunate, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 773, 92663, 37163, faction_shogunate, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 774, 92079, 37373, faction_shogunate, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 775, 92079, 36663, faction_shogunate, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 776, 91409, 36508, faction_tosa, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 777, 91569, 37068, faction_shogunate, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 778, 90879, 36874, faction_choshu, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 779, 90518, 36378, faction_saga, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 780, 90754, 35823, faction_satsuma, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 781, 90447, 33649, faction_ryukyu, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 782, 57803, 30739, faction_ottoman, 542, 543, 741, 783, 784, 785, 786, 839, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 783, 55535, 28471, faction_darfur, 782, 784, 787, 863, 865, 867, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 784, 57155, 28255, faction_ottoman, 782, 783, 785, 787, 788, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 785, 58286, 28897, faction_ottoman, 782, 784, 786, 788, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 786, 58949, 28540, faction_ottoman, 782, 785, 788, 839, 842, 843, 845, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 787, 56533, 26321, faction_shilluk, 783, 784, 788, 789, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 788, 58033, 26321, faction_shilluk, 785, 784, 787, 789, 786, 845, 846, 847, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 789, 57683, 25021, faction_shilluk, 787, 788, 847, 854, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 790, 81385, 37348, faction_china, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 791, 82309, 37902, faction_china, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 792, 82811, 33886, faction_china, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 793, 82979, 35230, faction_china, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 794, 82383, 36623, faction_china, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 795, 84155, 32063, faction_china, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 796, 84346, 32750, faction_china, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 797, 83333, 36646, faction_china, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 798, 84739, 30668, faction_china, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 799, 84252, 36536, faction_china, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 800, 84016, 35494, faction_china, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 801, 81193, 36194, faction_china, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 802, 83768, 33905, faction_china, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 803, 84332, 34659, faction_china, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 804, 84702, 33823, faction_china, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 805, 86996, 36204, faction_taiping, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 806, 85278, 36724, faction_china, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 807, 87394, 35433, faction_taiping, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 808, 86207, 36177, faction_china, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 809, 86459, 35484, faction_taiping, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 810, 85136, 36051, faction_china, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 811, 85241, 35442, faction_china, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 812, 81360, 35296, faction_china, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 813, 87832, 34756, faction_china, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 814, 87327, 34294, faction_china, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 815, 86913, 34690, faction_taiping, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 816, 85311, 32223, faction_china, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 817, 85223, 33301, faction_china, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 818, 86003, 32376, faction_china, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 819, 85829, 33130, faction_china, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 820, 85220, 34697, faction_china, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 821, 86045, 34943, faction_taiping, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 822, 85958, 34392, faction_taiping, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 823, 81576, 34392, faction_china, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 824, 84806, 31933, faction_china, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 825, 86312, 33881, faction_taiping, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 826, 88302, 32251, faction_china, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 827, 87365, 33755, faction_china, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 828, 87185, 33341, faction_china, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 829, 87041, 32891, faction_china, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 830, 86519, 33143, faction_china, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 831, 88319, 32765, faction_china, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 832, 86546, 32564, faction_china, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 833, 86480, 36682, faction_china, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 834, 80841, 33904, faction_china, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 835, 80928, 32976, faction_china, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 836, 81653, 32367, faction_china, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 837, 82320, 32831, faction_china, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 838, 83335, 32802, faction_china, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 839, 60152, 29333, faction_aussa, 782, 786, 840, 842, 844, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 840, 61292, 28493, faction_aussa, 839, 842, 844, 841, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 841, 61632, 27733, faction_aussa, 840, 844, 849, 850, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 842, 60125, 28634, faction_ethiopia, 786, 839, 843, 844, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 843, 60041, 27710, faction_ethiopia, 786, 842, 844, 845, 846, 848, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 844, 61091, 27878, faction_aussa, 839, 840, 841, 842, 843, 848, 849, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 845, 59238, 27309, faction_ethiopia, 786, 788, 843, 846, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 846, 59510, 26425, faction_ethiopia, 788, 843, 845, 847, 848, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 847, 59578, 25575, faction_ethiopia, 788, 789, 846, 848, 854, 857, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 848, 60700, 25677, faction_harar, 843, 844, 846, 847, 849, 857, 859, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 849, 62332, 25915, faction_harar, 841, 844, 847, 850, 851, 852, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 850, 63080, 27003, faction_isaaq, 841, 849, 851, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 851, 64016, 26198, faction_somalia, 849, 850, 851, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 852, 62264, 23977, faction_somalia, 849, 851, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 853, 65565, 28051, faction_mahra, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 854, 59391, 23906, faction_masai, 789, 847, 855, 856, 857, 858, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 855, 58901, 22996, faction_masai, 854, 856, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 856, 59496, 22681, faction_masai, 854, 855, 858, 860, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 857, 60126, 24081, faction_masai, 847, 848, 854, 858, 859, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 858, 60126, 22611, faction_masai, 854, 856, 857, 859, 860, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 859, 60861, 23591, faction_masai, 848, 849, 852, 857, 858, 860, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 860, 60616, 21911, faction_oman, 856, 858, 860, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 861, 52603, 31109, faction_toubou, 742, 862, 882, 883, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 862, 53307, 30341, faction_toubou, 741, 742, 862, 863, 864, 865, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 863, 54623, 30123, faction_toubou, 741, 783, 862, 865, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 864, 52277, 28919, faction_kanem, 862, 865, 866, 883, 877, 869, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 865, 53761, 28760, faction_wadai, 783, 862, 863, 864, 866, 867, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 866, 52754, 27541, faction_baghirmi, 864, 865, 867, 868, 877, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 867, 54079, 27488, faction_wadai, 783, 865, 866, 868, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 868, 52731, 26610, faction_baghirmi, 866, 867, 877, 878, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 869, 50890, 27437, faction_bornu, 864, 870, 872, 873, 883, 877, 878, 883, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 870, 49514, 27480, faction_sokoto, 869, 871, 873, 874, 883, 884, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 871, 48611, 28039, faction_sokoto, 870, 874, 884, 885, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 872, 50589, 26276, faction_sokoto, 869, 873, 881, 878, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 873, 49514, 26276, faction_sokoto, 869, 870, 872, 874, 875, 876, 881, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 874, 48611, 26835, faction_sokoto, 870, 871, 873, 876, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 875, 49084, 25287, faction_beninedo, 873, 876, 881, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 876, 48181, 26018, faction_oyo, 873, 874, 875, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 877, 51842, 27357, faction_sokoto, 864, 877, 866, 868, 869, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 878, 51572, 26091, faction_sokoto, 868, 869, 872, 877, 879, 880, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 879, 51747, 24516, faction_cameroon, 878, 880, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 880, 50872, 24586, faction_spain, 879, 881, 878, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 881, 50242, 25216, faction_spain, 880, 872, 873, 875, 878, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 882, 50348, 30675, faction_agadez, 742, 746, 861, 883, 884, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 883, 50683, 29000, faction_damagaram, 882, 884, 870, 869, 864, 861, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 884, 48713, 29060, faction_dendi, 871, 870, 882, 883, 885, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 885, 47679, 28590, faction_dendi, 871, 884, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 886, 46328, 30575, faction_adagh, 885, 884, 882, 887, 746, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 887, 45088, 28777, faction_bamana, 886, 888, 889, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 888, 44468, 27599, faction_bamana, 887, 889, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),
(call_script, "script_add_province", 889, 43563, 28528, faction_bamana, 888, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, terrain_plains),


# Initparam multipliers
# Index, population_multiplier, literacy_multiplier, urbanization_multiplier
(call_script, "script_province_set_initparams", 191, 130, 150, 140),
(call_script, "script_province_set_initparams", 307, 50, 80, 70),

    (try_begin),
    (eq, ":start_date", 1861),
    (else_try),
    (eq, ":start_date", 1877),
    (array_set_val, "$provinces", faction_prussia, 0, province_owner),
    (else_try),
    (eq, ":start_date", 1914),
    (else_try),
    (eq, ":start_date", 1919),
    (else_try),
    (eq, ":start_date", 1936),
    (try_end),

    (try_for_range, ":province", 0, number_of_provinces),
    (array_get_val, ":owner", "$provinces", ":province", province_owner),
    (array_set_val, "$provinces", ":owner", ":province", province_controller),
    (try_end),
    
(call_script, "script_initialize_faction_provinces_arrays"),

    (try_for_range, ":faction", 0, number_of_factions),
    (call_script, "script_faction_calculate_if_active", ":faction"),
    (try_end),

(call_script, "script_initialize_provinces_parameters"),

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
(store_script_param, ":owner_faction", 4),
(store_script_param, ":sea_province", 15),
(store_script_param, ":terrain", 16),

(array_set_val, "$provinces", ":x", ":index", province_x),
(array_set_val, "$provinces", ":y", ":index", province_y),
(array_set_val, "$provinces", ":owner_faction", ":index", province_owner),
(array_set_val, "$provinces", ":sea_province", ":index", province_bordering_sea_province),
(array_set_val, "$provinces", ":terrain", ":index", province_terrain),
(array_set_val, "$provinces", 100, ":index", province_initparam_population_multiplier),
(array_set_val, "$provinces", 100, ":index", province_initparam_literacy_multiplier),
(array_set_val, "$provinces", 100, ":index", province_initparam_urbanization_multiplier),

    (try_for_range, ":param", 5, 14+1),
    (store_script_param, ":bordering_province", ":param"),
    (store_add, ":province_param", ":param", -5),
    (array_set_val, "$provinces_borders", ":bordering_province", ":index", ":province_param"),
    (try_end),
    
(store_add, ":string_name", "str_province0", ":index"),
(sss, s1, ":string_name"),
(array_set_val, "$provinces_strings", s1, ":index", province_string_name),
]),

# Set initparams for one province
("province_set_initparams", [
(store_script_param, ":index", 1),
(store_script_param, ":population_multiplier", 2),
(store_script_param, ":literacy_multiplier", 3),
(store_script_param, ":urbanization_multiplier", 4),

(array_set_val, "$provinces", ":population_multiplier", ":index", province_initparam_population_multiplier),
(array_set_val, "$provinces", ":literacy_multiplier", ":index", province_initparam_literacy_multiplier),
(array_set_val, "$provinces", ":urbanization_multiplier", ":index", province_initparam_urbanization_multiplier),
]),

# Set provinces parameters according to initparams
("initialize_provinces_parameters", [

    (try_for_range, ":faction", 0, number_of_factions),
    (array_eq, "$factions", 1, ":faction", faction_is_active),
    (array_get_val, ":faction_population", "$factions", ":faction", faction_population),
    (array_get_val, ":faction_literacy", "$factions", ":faction", faction_literacy),
    (array_get_val, ":faction_urbanization", "$factions", ":faction", faction_urbanization),
    (array_get_val, ":array_provinces_owned", "$factions", ":faction", faction_array_provinces_owned),
    (array_get_dim_size, ":array_size", ":array_provinces_owned", 0),
    # For initparam_population_multiplier we calculate sum of all provinces multiplier,
    # and for province_initparam_literacy_multiplier and province_initparam_urbanization_multiplier we calculate the average.
    (assign, ":sum_population_multiplier", 0),
    (assign, ":sum_literacy_multiplier", 0),
    (assign, ":sum_urbanization_multiplier", 0),
        (try_for_range, ":index", 0, ":array_size"),
        (array_get_val, ":province", ":array_provinces_owned", ":index"),
        (array_get_val, ":population_multiplier", "$provinces", ":province", province_initparam_population_multiplier),
        (array_get_val, ":literacy_multiplier", "$provinces", ":province", province_initparam_literacy_multiplier),
        (array_get_val, ":urbanization_multiplier", "$provinces", ":province", province_initparam_urbanization_multiplier),
        (val_add, ":sum_population_multiplier", ":population_multiplier"),
        (val_add, ":sum_literacy_multiplier", ":population_multiplier"),
        (val_add, ":sum_urbanization_multiplier", ":population_multiplier"),
        (try_end),
    (store_div, ":average_literacy_multiplier", ":sum_literacy_multiplier", ":array_size"),
    (store_div, ":average_urbanization_multiplier", ":sum_urbanization_multiplier", ":array_size"),
        (try_for_range, ":index", 0, ":array_size"),
        (array_get_val, ":province", ":array_provinces_owned", ":index"),
        (array_get_val, ":population_multiplier", "$provinces", ":province", province_initparam_population_multiplier),
        (array_get_val, ":literacy_multiplier", "$provinces", ":province", province_initparam_literacy_multiplier),
        (array_get_val, ":urbanization_multiplier", "$provinces", ":province", province_initparam_urbanization_multiplier),
        # province_population = (population_multiplier / sum_population_multiplier) * faction_population
        (store_mul, ":province_population_multiplier", ":population_multiplier", 100),
        (val_div, ":province_population_multiplier", ":sum_population_multiplier"),
        (val_max, ":province_population_multiplier", 1),
        (store_mul, ":province_population", ":faction_population", ":province_population_multiplier"),
        (val_div, ":province_population", 100),
        (array_set_val, "$provinces", ":province_population", ":index", province_population),
        # province_literacy = literacy_multiplier * ((average_literacy_multiplier/100) * faction_literacy)
        (store_mul, ":province_literacy", ":average_literacy_multiplier", ":faction_literacy"),
        (val_div, ":province_literacy", 100),
        (val_mul, ":province_literacy", ":literacy_multiplier"),
        (val_div, ":province_literacy", 100),
        (array_set_val, "$provinces", ":province_literacy", ":index", province_literacy),
        # province_urbanization = urbanization_multiplier * ((average_urbanization_multiplier/100) * faction_urbanization)
        (store_mul, ":province_urbanization", ":average_urbanization_multiplier", ":faction_urbanization"),
        (val_div, ":province_urbanization", 100),
        (val_mul, ":province_urbanization", ":urbanization_multiplier"),
        (val_div, ":province_urbanization", 100),
        (array_set_val, "$provinces", ":province_urbanization", ":index", province_urbanization),
        (try_end),
    (try_end),

]),

# Fill faction arrays with provinces, can be called during both new game or load game initialization
("initialize_faction_provinces_arrays", [

    (try_for_range, ":faction", 0, number_of_factions),
    (array_create, ":array", 0, 1),
    (array_set_val, "$factions", ":array", ":faction", faction_array_provinces_owned),
    (array_create, ":array", 0, 1),
    (array_set_val, "$factions", ":array", ":faction", faction_array_provinces_controlled),
    (try_end),
    (try_for_range, ":province", 0, number_of_provinces),
    (neg|array_eq, "$provinces", -1, ":province", province_controller),
    (array_get_val, ":controller", "$provinces", ":province", province_controller),
    (array_get_val, ":owner", "$provinces", ":province", province_owner),
    (array_get_val, ":array_provinces_owned", "$factions", ":owner", faction_array_provinces_owned),
    (array_get_val, ":array_provinces_controlled", "$factions", ":controller", faction_array_provinces_controlled),
    (array_push, ":array_provinces_owned", ":province"),
    (array_push, ":array_provinces_controlled", ":province"),
    (try_end),
]),

# Global containers initialization
("initialize_global_containers", [
(dict_create, "$dictionary_global"),
(array_create, "$globals", 0, number_of_global_parameters),
(array_create, "$factions", 0, number_of_factions, number_of_factions_parameters),
(array_create, "$factions_strings", 1, number_of_factions, number_of_factions_strings),
(array_create, "$provinces", 0, number_of_provinces, number_of_provinces_parameters),
(array_create, "$provinces_borders", 0, number_of_provinces, number_of_provinces_borders),
(array_create, "$provinces_strings", 1, number_of_provinces, number_of_provinces_strings),
(array_create, "$provinces_manufacturers", 0, number_of_provinces, number_of_resources),

(array_set_val_all, "$globals", -1),
(array_set_val_all, "$factions", -1),
(array_set_val_all, "$provinces", -1),
(array_set_val_all, "$provinces_manufacturers", -1),
]),

# Sets 0 to faction_is_active if faction doesnt have owned provinces, otherwise sets 1
# Should be called when faction loses province
("faction_calculate_if_active", [
(store_script_param, ":faction", 1),

(array_get_val, ":array_provinces_owned", "$factions", ":faction", faction_array_provinces_owned),
(array_get_dim_size, ":array_size", ":array_provinces_owned", 0),
    (try_begin),
    (le, ":array_size", 0),
    (array_set_val, "$factions", 0, ":faction", faction_is_active),
    (else_try),
    (array_set_val, "$factions", 1, ":faction", faction_is_active),
    (try_end),
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
    (set_fog_distance, 999999999),
    (try_end),
]),

# Called whenever world map scene starts: after new game start, after loading there after battle ended and after loading a save file.
# Script adds props to the scene, sets up camera and runs the UI.
("world_map_start", [
# Spawning world map base prop and province props
(init_position, pos1),
(set_spawn_position, pos1),
(spawn_scene_prop, "spr_world_map_base"),

(position_move_z, pos1, 30, 1),
(set_spawn_position, pos1),
    (try_for_range, ":province", 0, number_of_provinces),
    (store_add, ":prop_type", "spr_province0", ":province"),
    (spawn_scene_prop, ":prop_type"),
    (array_set_val, "$provinces", reg0, ":province", province_prop1),
    (array_get_val, ":faction", "$provinces", ":province", province_controller),
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
(store_mul, ":scroll_speed", ":z", 30),
(store_mul, ":scroll_speed_negative", ":z", -30),
(val_div, ":scroll_speed", 100),
(val_div, ":scroll_speed_negative", 100),
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
    (display_message, "@{reg0}, {reg1}"),
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

(call_script, "script_world_map_ui_start_devmode"),
(call_script, "script_world_map_ui_start_faction_selection"),
(call_script, "script_world_map_ui_start_bottom_panel"),
(call_script, "script_world_map_ui_start_province_menu_small_player"),
(call_script, "script_world_map_ui_start_province_menu_small_foreign"),
(call_script, "script_world_map_ui_start_province_menu_small_noowner"),

]),

# Small menu on the left on screen for player faction provinces
("world_map_ui_start_province_menu_small_player", [
    (try_begin),
    (array_eq, "$globals", ui_mode_province_menu_small_player, global_ui_mode),
    (call_script, "script_world_map_ui_start_province_menu_small_shared"),
    
    (try_end),
]),

# Small menu on the left on screen for non-player faction provinces
("world_map_ui_start_province_menu_small_foreign", [
    (try_begin),
    (array_eq, "$globals", ui_mode_province_menu_small_foreign, global_ui_mode),
    (call_script, "script_world_map_ui_start_province_menu_small_shared"),
    
    (try_end),
]),

# Small menu on the left on screen for no owner provinces
("world_map_ui_start_province_menu_small_noowner", [
    (try_begin),
    (array_eq, "$globals", ui_mode_province_menu_small_noowner, global_ui_mode),
    (call_script, "script_world_map_ui_start_province_menu_small_shared"),
    
    (try_end),
]),


("world_map_ui_start_province_menu_small_shared", [
(create_mesh_overlay, "$ui_province_menu_small_bg", "mesh_ui_background"),
(overlay_set_material, "$ui_province_menu_small_bg", "@ui_province_menu_small"),
(position_set_x, pos1, 0), (position_set_y, pos1, 0), (overlay_set_position, "$ui_province_menu_small_bg", pos1),
(position_set_x, pos1, 290), (position_set_y, pos1, 800), (overlay_set_size, "$ui_province_menu_small_bg", pos1),

(array_get_val, ":selected_province", "$globals", global_selected_province),
(array_get_val, s1, "$provinces_strings", ":selected_province", province_string_name),
(create_text_overlay, "$ui_province_name", "@{s1}", tf_center_justify),
(position_set_x, pos1, 145), (position_set_y, pos1, 510), (overlay_set_position, "$ui_province_name", pos1),
(position_set_x, pos1, 1200), (position_set_y, pos1, 1200), (overlay_set_size, "$ui_province_name", pos1),

(array_get_val, ":owner", "$provinces", ":selected_province", province_owner),
    (try_begin),
    (lt, ":owner", 0),
    (create_text_overlay, "$ui_province_in_text", "@Unclaimed territory", tf_right_align),
    (position_set_x, pos1, 150), (position_set_y, pos1, 480), (overlay_set_position, "$ui_province_in_text", pos1),
    (position_set_x, pos1, 590), (position_set_y, pos1, 590), (overlay_set_size, "$ui_province_in_text", pos1),
    (else_try),
    (create_text_overlay, "$ui_province_in_text", "@Province in", tf_right_align),
    (position_set_x, pos1, 137), (position_set_y, pos1, 480), (overlay_set_position, "$ui_province_in_text", pos1),
    (position_set_x, pos1, 590), (position_set_y, pos1, 590), (overlay_set_size, "$ui_province_in_text", pos1),

    (create_image_button_overlay, "$ui_province_owner_flag", "mesh_ui_picture", "mesh_ui_picture"),
    (position_set_x, pos1, 152), (position_set_y, pos1, 486), (overlay_set_position, "$ui_province_owner_flag", pos1),
    (position_set_x, pos1, 210*1.5), (position_set_y, pos1, 210), (overlay_set_size, "$ui_province_owner_flag", pos1),
    (call_script, "script_ui_flag_overlay_set_material_and_tooltip", "$ui_province_owner_flag", ":owner"),

    (array_get_val, s1, "$factions_strings", ":owner", faction_string_name_short),
    (create_text_overlay, "$ui_province_in_text2", "@{s1}", tf_left_align),
    (position_set_x, pos1, 160), (position_set_y, pos1, 480), (overlay_set_position, "$ui_province_in_text2", pos1),
    (position_set_x, pos1, 590), (position_set_y, pos1, 590), (overlay_set_size, "$ui_province_in_text2", pos1),
    (try_end),
]),

# Bottom panel of world map with common info about faction
("world_map_ui_start_bottom_panel", [
    (try_begin),
    (this_or_next|array_eq, "$globals", ui_mode_none, global_ui_mode),
    (this_or_next|array_eq, "$globals", ui_mode_province_menu_small_foreign, global_ui_mode),
    (this_or_next|array_eq, "$globals", ui_mode_province_menu_small_noowner, global_ui_mode),
    (array_eq, "$globals", ui_mode_province_menu_small_player, global_ui_mode),
    (create_mesh_overlay, "$ui_bottom_panel", "mesh_ui_background"),
    (overlay_set_material, "$ui_bottom_panel", "@ui_world_map_bottom_panel"),
    (position_set_x, pos1, 0), (position_set_y, pos1, 0), (overlay_set_position, "$ui_bottom_panel", pos1),
    (position_set_x, pos1, 1000), (position_set_y, pos1, 130), (overlay_set_size, "$ui_bottom_panel", pos1),
    (create_image_button_overlay, "$ui_bottom_panel_flag", "mesh_ui_picture", "mesh_ui_picture"),
    (position_set_x, pos1, 60), (position_set_y, pos1, 35), (overlay_set_position, "$ui_bottom_panel_flag", pos1),
    (position_set_x, pos1, 1000*1.5), (position_set_y, pos1, 1000), (overlay_set_size, "$ui_bottom_panel_flag", pos1),
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

(call_script, "script_world_map_ui_frame_devmode"),
(call_script, "script_world_map_ui_frame_faction_selection"),
(call_script, "script_world_map_ui_frame_process_province_click"),
(call_script, "script_world_map_ui_frame_province_small_menu_player"),
]),

# After starting new game and selecting starting date player needs to click on any factions province to set it as playable and click "Start Game"
("world_map_ui_frame_faction_selection", [
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
("world_map_ui_frame_process_province_click", [
(set_fixed_point_multiplier, 1000),

    (try_begin),
    (key_clicked, key_left_mouse_button),
    (this_or_next|array_eq, "$globals", ui_mode_none, global_ui_mode), # Only register clicks if on specific ui modes
    (this_or_next|array_eq, "$globals", ui_mode_faction_selection, global_ui_mode),
    (this_or_next|array_eq, "$globals", ui_mode_province_menu_small_foreign, global_ui_mode),
    (this_or_next|array_eq, "$globals", ui_mode_province_menu_small_noowner, global_ui_mode),
    (array_eq, "$globals", ui_mode_province_menu_small_player, global_ui_mode),
    (mouse_get_position, pos1),
    (assign, ":continue", 1),
    (position_get_x, ":x", pos1),
    (position_get_y, ":y", pos1),
        (try_begin), # Dont register click if clicked on UI areas
        (array_eq, "$globals", ui_mode_faction_selection, global_ui_mode),
        (le, ":y", 64),
        (assign, ":continue", 0),
        (else_try),
        (this_or_next|array_eq, "$globals", ui_mode_none, global_ui_mode),
        (this_or_next|array_eq, "$globals", ui_mode_province_menu_small_foreign, global_ui_mode),
        (this_or_next|array_eq, "$globals", ui_mode_province_menu_small_noowner, global_ui_mode),
        (array_eq, "$globals", ui_mode_province_menu_small_player, global_ui_mode),
        (le, ":y", 90),
        (assign, ":continue", 0),
        (try_end),
    (eq, ":continue", 1),
    (init_position, pos2),
    (set_fixed_point_multiplier, 100),
    (assign, ":closest_province", -1),
    (assign, ":closest_province_distance_to_mouse", 9999999),
        (try_for_range, ":province", 0, number_of_provinces), # loop to detect province closest to mouse using position_get_screen_projection
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
        (ge, ":closest_province_distance_to_mouse", province_select_radius), # If distance is above province_select_radius, then probably sea province was selected
        (assign, ":closest_province", -1),
        (try_end),
        (try_begin),
        (ge, ":closest_province", 0),
            (try_begin), # Set faction for faction selection if province has owner
            (array_eq, "$globals", ui_mode_faction_selection, global_ui_mode),
            (array_ge, "$provinces", 0, ":closest_province", province_controller),
            (array_get_val, ":faction", "$provinces", ":closest_province", province_controller),
            (array_set_val, "$globals", ":faction", global_faction_selection_selected_faction),
            (try_end),
            (try_begin), # Switch to province small menu
            (this_or_next|array_eq, "$globals", ui_mode_none, global_ui_mode), # either no mode or previous selected province is not equal to new selected one
            (neg|array_eq, "$globals", ":closest_province", global_selected_province),
            (this_or_next|array_eq, "$globals", ui_mode_none, global_ui_mode),
            (this_or_next|array_eq, "$globals", ui_mode_province_menu_small_foreign, global_ui_mode),
            (this_or_next|array_eq, "$globals", ui_mode_province_menu_small_noowner, global_ui_mode),
            (array_eq, "$globals", ui_mode_province_menu_small_player, global_ui_mode),
                (try_begin), # switch to player faction province menu, foreign faction province menu or no owner province menu depending on faction controller
                (array_lt, "$provinces", 0, ":closest_province", province_controller),
                (array_set_val, "$globals", ui_mode_province_menu_small_noowner, global_ui_mode),
                (else_try),
                (array_get_val, ":player_faction", "$globals", global_player_faction),
                (array_eq, "$provinces", ":player_faction", ":closest_province", province_controller),
                (array_set_val, "$globals", ui_mode_province_menu_small_player, global_ui_mode),
                (else_try),
                (array_set_val, "$globals", ui_mode_province_menu_small_foreign, global_ui_mode),
                (try_end),
                (presentation_set_duration, 0),
            (try_end),
        (array_set_val, "$globals", ":closest_province", global_selected_province),
        (try_end),
    (try_end),
]),

("world_map_ui_frame_province_small_menu_player", [
(set_fixed_point_multiplier, 1000),


]),

# Dev mode is toggled by pressing F3 button
("world_map_ui_start_devmode", [
    (try_for_range, ":province", 0, number_of_provinces),
    (array_set_val, "$provinces", -1, ":province", province_index_overlay),
    (try_end),
(create_mesh_overlay, "$ui_black_dot", "mesh_black_dot"),
(position_set_x, pos1, 500),
(position_set_y, pos1, 375),
(overlay_set_position, "$ui_black_dot", pos1),
(overlay_set_display, "$ui_black_dot", 0),
(assign, "$devmode_enabled", 0),
]),

("world_map_ui_frame_devmode", [
(set_fixed_point_multiplier, 1000),
(close_order_menu),
    (try_begin), #exit to main menu by pressing tab
    (key_clicked, key_tab),
	(jump_to_menu, "mnu_to_main_menu"),
	(finish_mission, 0),
    (try_end),
    (try_begin), # enable devmode by pressing f3
    (key_clicked, key_f3),
        (try_begin),
        (eq, "$devmode_enabled", 0),
        (assign, "$devmode_enabled", 1),
            (try_begin), # Display index of each province on map
                (try_for_range, ":province", 0, number_of_provinces),
                (array_get_val, ":overlay", "$provinces", ":province", province_index_overlay),
                    (try_begin),
                    (eq, ":overlay", -1),
                    (assign, reg0, ":province"),
                    (create_text_overlay, ":overlay", "@{reg0}", tf_center_justify|tf_vertical_align_center),
                    (array_set_val, "$provinces", ":overlay", ":province", province_index_overlay),
                    (position_set_x, pos1, 700),
                    (position_set_y, pos1, 700),
                    (overlay_set_size, ":overlay", pos1),
                    (else_try),
                    (overlay_set_display, ":overlay", 1),
                    (try_end),
                (try_end),
            (try_end),
        (else_try),
        (assign, "$devmode_enabled", 0),
            (try_for_range, ":province", 0, number_of_provinces),
            (array_get_val, ":overlay", "$provinces", ":province", province_index_overlay),
            (neq, ":overlay", -1),
            (overlay_set_display, ":overlay", 0),
            (try_end),
        (try_end),
    (overlay_set_display, "$ui_black_dot", "$devmode_enabled"),
    (try_end),
    
    
    (try_begin),
    (eq, "$devmode_enabled", 1),
    (init_position, pos1),
        (try_for_range, ":province", 0, number_of_provinces),
        (array_get_val, ":overlay", "$provinces", ":province", province_index_overlay),
        (array_get_val, ":x", "$provinces", ":province", province_x),
        (array_get_val, ":y", "$provinces", ":province", province_y),
        (set_fixed_point_multiplier, 100),
        (position_set_x, pos1, ":x"),
        (position_set_y, pos1, ":y"),
        (set_fixed_point_multiplier, 1000),
        (position_get_screen_projection, pos2, pos1),
        (overlay_set_position, ":overlay", pos2),
        (try_end),
    (try_end),
]),


]