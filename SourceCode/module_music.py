from header_music import *
####################################################################################################################
#  Each track record contains the following fields:
#  1) Track id: used for referencing tracks.
#  2) Track file: filename of the track
#  3) Track flags. See header_music.py for a list of available flags
#  4) Continue Track flags: Shows in which situations or cultures the track can continue playing. See header_music.py for a list of available flags
####################################################################################################################

# WARNING: You MUST add mtf_module_track flag to the flags of the tracks located under module directory

tracks = [
("bogus", "cant_find_this.ogg", 0, 0),

("main_menu", "main_menu.ogg", mtf_sit_main_title|mtf_start_immediately, mtf_situation_global_map),

("game_start1", "game_start1.ogg", mtf_situation_game_start|mtf_start_immediately, mtf_situation_global_map),


  
]
