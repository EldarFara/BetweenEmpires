from header_common import *
from ID_animations import *
from header_mission_templates import *
from header_tableau_materials import *
from header_items import *
from module_constants import *


# #######################################################################
#	("tableau_id", flags, "tableau_sample_material", width, height, min_x, min_y, max_x, max_y, [operations_block]),
#  Each tableau material contains the following fields:
#  1) Tableau id (string): used for referencing tableaux in other files. The prefix tab_ is automatically added before each tableau-id.
#  2) Tableau flags (int). See header_tableau_materials.py for a list of available flags
#  3) Tableau sample material name (string).
#  4) Tableau width (int).
#  5) Tableau height (int).
#  6) Tableau mesh min x (int): divided by 1000 and used when a mesh is auto-generated using the tableau material
#  7) Tableau mesh min y (int): divided by 1000 and used when a mesh is auto-generated using the tableau material
#  8) Tableau mesh max x (int): divided by 1000 and used when a mesh is auto-generated using the tableau material
#  9) Tableau mesh max y (int): divided by 1000 and used when a mesh is auto-generated using the tableau material
#  10) Operations block (list): A list of operations. See header_operations.py for reference.
#     The operations block is executed when the tableau is activated.
# 
# #######################################################################

# #######################################################################
#	So, looking into it, RGL Log will store these are errors if this file
#	is built while it's empty
#
# WARNING: UNABLE TO MAP GAME TABLEAU CODE:  tab_game_character_sheet 
# WARNING: UNABLE TO MAP GAME TABLEAU CODE:  tab_game_inventory_window 
# WARNING: UNABLE TO MAP GAME TABLEAU CODE:  tab_game_party_window 
# WARNING: UNABLE TO MAP GAME TABLEAU CODE:  tab_game_troop_label_banner 
# WARNING: UNABLE TO MAP GAME TABLEAU CODE:  tab_game_profile_window
#
#	And each of those reference two (_color and _alpha_mask) other
#		tableaus themselves. You could probably erase those. I haven't
#		tried this personally.
#
#	I was unable to see if the _note meshes are necessary as my Clean
#	build doesn't include parties or centers for testing.
#
#	In other words, feel free to remove them, as they won't break your
#	game, but you should at least leave empty tableaus named identical
#	as above. 
# #######################################################################


tableaus = [

  ("game_character_sheet", 0, "solid_gray", 1024, 1024, 0, 0, 266, 532,
   [
  
       ]),

  ("game_inventory_window", 0, "solid_gray", 1024, 1024, 0, 0, 180, 270,
   [
   
       ]),

  ("game_profile_window", 0, "solid_gray", 1024, 1024, 0, 0, 320, 480, [
  
    ]),

  ("game_party_window", 0, "solid_gray", 1024, 1024, 0, 0, 300, 300,
   [
   
       ]),

  ("game_troop_label_banner", 0, "solid_gray", 256, 256, -128, 0, 128, 256,
   [
       ]),
  ("troop_note_alpha_mask", 0, "solid_gray", 1024, 1024, 0, 0, 400, 400,
   [
       ]),

  ("troop_note_color", 0, "solid_gray", 1024, 1024, 0, 0, 400, 400,
   [
       ]),

  ("troop_character_alpha_mask", 0, "solid_gray", 1024, 1024, 0, 0, 400, 400,
   [
       ]),

  ("troop_character_color", 0, "solid_gray", 1024, 1024, 0, 0, 400, 400,
   [
       ]),
  
  ("troop_inventory_alpha_mask", 0, "solid_gray", 1024, 1024, 0, 0, 400, 400,
   [
       ]),

  ("troop_inventory_color", 0, "solid_gray", 1024, 1024, 0, 0, 400, 400,
   [
       ]),

  ("troop_profile_alpha_mask", 0, "solid_gray", 1024, 1024, 0, 0, 400, 400,
   [
       ]),

  ("troop_profile_color", 0, "solid_gray", 1024, 1024, 0, 0, 400, 400,
   [
       ]),


  ("troop_party_alpha_mask", 0, "solid_gray", 1024, 1024, 0, 0, 400, 400,
   [
       ]),

  ("troop_party_color", 0, "solid_gray", 1024, 1024, 0, 0, 400, 400,
   [
       ]),

  ("troop_note_mesh", 0, "solid_gray", 1024, 1024, 0, 0, 350, 350,
   [
       ]),

  ("center_note_mesh", 0, "solid_gray", 1024, 1024, 0, 0, 200, 200,
   [
       ]),
]
