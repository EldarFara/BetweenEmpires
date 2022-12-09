from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from module_constants import *

game_menus = [

    ("start_game_0", menu_text_color(0xFF000000)|mnf_disable_all_keys,
    " ",
    "none", [
    # After player pressed new game button, game runs script_game_start and then comes here
    
    # todo This is temporary, later I will make it so after pressing new game button, date choosing menu will appear, and only then - the world map
    # Initialize_new_game
	(call_script,"script_initialize_new_game", 1850),
    # Jump to world map
	(set_jump_mission,"mt_world_map"),
	(jump_to_scene,"scn_world_map"),
	(change_screen_mission),
	], []),
	
	("start_phase_2", mnf_disable_all_keys,
	" ",
	"none",
	[], []),
	
	("start_game_3", mnf_disable_all_keys,
	" ",
	"none",
	[], []),
	
	("tutorial", mnf_disable_all_keys,
	" ",
	"none",
	[], []),

    ("reports", 0,
    " ",
    "none", [], []),

    ("camp", mnf_disable_all_keys,
    " ",
    "none",
    [], []),
	
    ("to_main_menu", mnf_disable_all_keys,
    " ",
    "none",
    [(change_screen_quit),], []),
	
 ]
