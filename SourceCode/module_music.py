from header_music import *
####################################################################################################################
#  Each track record contains the following fields:
#  1) Track id: used for referencing tracks.
#  2) Track file: filename of the track
#  3) Track flags. See header_music.py for a list of available flags
#  4) Continue Track flags: Shows in which situations or cultures the track can continue playing. See header_music.py for a list of available flags
####################################################################################################################

tracks = [
("bogus", "cant_find_this.ogg", 0, 0),

("main_menu", "main_menu.ogg", mtf_sit_main_title|mtf_start_immediately, mtf_situation_global_map),

("game_start1", "game_start1.ogg", mtf_situation_game_start|mtf_start_immediately, mtf_situation_global_map),

("battle_generic01", "battle_generic01.ogg", mtf_situation_battle, 0),

("victory_heavy01", "victory_heavy01.ogg", mtf_situation_victory_heavy, mtf_situation_global_map),

("globalmap_generic01", "globalmap_generic01.ogg", mtf_culture_europe|mtf_situation_global_map, mtf_culture_middleeast),
("globalmap_generic01b", "globalmap_generic01b.ogg", mtf_culture_europe|mtf_situation_global_map, mtf_culture_middleeast),
("globalmap_generic02", "globalmap_generic02.ogg", mtf_culture_europe|mtf_situation_global_map, mtf_culture_middleeast),
("globalmap_generic03", "globalmap_generic03.ogg", mtf_culture_europe|mtf_situation_global_map, mtf_culture_middleeast),
("globalmap_generic03b", "globalmap_generic03b.ogg", mtf_culture_europe|mtf_situation_global_map, mtf_culture_middleeast),
("globalmap_generic04", "globalmap_generic04.ogg", mtf_culture_europe|mtf_situation_global_map, mtf_culture_middleeast),
("globalmap_generic04b", "globalmap_generic04b.ogg", mtf_culture_europe|mtf_situation_global_map, mtf_culture_middleeast),
("globalmap_generic05", "globalmap_generic05.ogg", mtf_culture_europe|mtf_situation_global_map, mtf_culture_middleeast),
("globalmap_generic05b", "globalmap_generic05b.ogg", mtf_culture_europe|mtf_situation_global_map, mtf_culture_middleeast),

("globalmap_easteurope01", "globalmap_easteurope01.ogg", mtf_culture_easteurope|mtf_situation_global_map, mtf_culture_middleeast|mtf_culture_europe),
("globalmap_easteurope02", "globalmap_easteurope02.ogg", mtf_culture_easteurope|mtf_situation_global_map, mtf_culture_middleeast|mtf_culture_europe),
("globalmap_easteurope02b", "globalmap_easteurope02b.ogg", mtf_culture_easteurope|mtf_situation_global_map, mtf_culture_middleeast|mtf_culture_europe),
("globalmap_easteurope03", "globalmap_easteurope03.ogg", mtf_culture_easteurope|mtf_situation_global_map, mtf_culture_middleeast|mtf_culture_europe),
("globalmap_easteurope04", "globalmap_easteurope04.ogg", mtf_culture_easteurope|mtf_situation_global_map, mtf_culture_middleeast|mtf_culture_europe),
("globalmap_easteurope05", "globalmap_easteurope05.ogg", mtf_culture_easteurope|mtf_situation_global_map, mtf_culture_middleeast|mtf_culture_europe),
("globalmap_easteurope05b", "globalmap_easteurope05b.ogg", mtf_culture_easteurope|mtf_situation_global_map, mtf_culture_middleeast|mtf_culture_europe),
("globalmap_easteurope06", "globalmap_easteurope06.ogg", mtf_culture_easteurope|mtf_situation_global_map, mtf_culture_middleeast|mtf_culture_europe),
("globalmap_easteurope06b", "globalmap_easteurope06b.ogg", mtf_culture_easteurope|mtf_situation_global_map, mtf_culture_middleeast|mtf_culture_europe),
("globalmap_easteurope07", "globalmap_easteurope07.ogg", mtf_culture_easteurope|mtf_situation_global_map, mtf_culture_middleeast|mtf_culture_europe),
("globalmap_easteurope08", "globalmap_easteurope08.ogg", mtf_culture_easteurope|mtf_situation_global_map, mtf_culture_middleeast|mtf_culture_europe),
("globalmap_easteurope09", "globalmap_easteurope09.ogg", mtf_culture_easteurope|mtf_situation_global_map, mtf_culture_middleeast|mtf_culture_europe),
("globalmap_easteurope10", "globalmap_easteurope10.ogg", mtf_culture_easteurope|mtf_situation_global_map, mtf_culture_middleeast|mtf_culture_europe),
("globalmap_easteurope11", "globalmap_easteurope11.ogg", mtf_culture_easteurope|mtf_situation_global_map, mtf_culture_middleeast|mtf_culture_europe),
("globalmap_easteurope12", "globalmap_easteurope12.ogg", mtf_culture_easteurope|mtf_situation_global_map, mtf_culture_middleeast|mtf_culture_europe),
("globalmap_easteurope13", "globalmap_easteurope13.ogg", mtf_culture_easteurope|mtf_situation_global_map, mtf_culture_middleeast|mtf_culture_europe),
("globalmap_easteurope14", "globalmap_easteurope14.ogg", mtf_culture_easteurope|mtf_situation_global_map, mtf_culture_middleeast|mtf_culture_europe),

("globalmap_middleeast01", "globalmap_middleeast01.ogg", mtf_culture_middleeast|mtf_situation_global_map, 0),
("globalmap_middleeast01b", "globalmap_middleeast01b.ogg", mtf_culture_middleeast|mtf_situation_global_map, 0),
("globalmap_middleeast02", "globalmap_middleeast02.ogg", mtf_culture_middleeast|mtf_situation_global_map, 0),
("globalmap_middleeast03", "globalmap_middleeast03.ogg", mtf_culture_middleeast|mtf_situation_global_map, 0),
("globalmap_middleeast04", "globalmap_middleeast04.ogg", mtf_culture_middleeast|mtf_situation_global_map, 0),
("globalmap_middleeast04b", "globalmap_middleeast04b.ogg", mtf_culture_middleeast|mtf_situation_global_map, 0),
("globalmap_middleeast05", "globalmap_middleeast05.ogg", mtf_culture_middleeast|mtf_situation_global_map, 0),
("globalmap_middleeast06", "globalmap_middleeast06.ogg", mtf_culture_middleeast|mtf_situation_global_map, 0),
("globalmap_middleeast07", "globalmap_middleeast07.ogg", mtf_culture_middleeast|mtf_situation_global_map, 0),
("globalmap_middleeast08", "globalmap_middleeast08.ogg", mtf_culture_middleeast|mtf_situation_global_map, 0),
("globalmap_middleeast09", "globalmap_middleeast09.ogg", mtf_culture_middleeast|mtf_situation_global_map, 0),
("globalmap_middleeast10", "globalmap_middleeast10.ogg", mtf_culture_middleeast|mtf_situation_global_map, 0),

("globalmap_spain01", "globalmap_spain01.ogg", mtf_culture_spain|mtf_situation_global_map, mtf_culture_middleeast|mtf_culture_europe),
("globalmap_spain02", "globalmap_spain02.ogg", mtf_culture_spain|mtf_situation_global_map, mtf_culture_middleeast|mtf_culture_europe),
("globalmap_spain03", "globalmap_spain03.ogg", mtf_culture_spain|mtf_situation_global_map, mtf_culture_middleeast|mtf_culture_europe),
("globalmap_spain04", "globalmap_spain04.ogg", mtf_culture_spain|mtf_situation_global_map, mtf_culture_middleeast|mtf_culture_europe),
("globalmap_spain05", "globalmap_spain05.ogg", mtf_culture_spain|mtf_situation_global_map, mtf_culture_middleeast|mtf_culture_europe),
]
