from header_factions import *

# #######################################################################
# ("faction_id", "faction_name_string", faction_flags_usually_0, faction_coherence, [(other_faction, relations_num)], [ranks], color_hex),
#
#  Each faction record contains the following fields:
#  1) Faction id: used for referencing factions in other files.
#     The prefix fac_ is automatically added before each faction id.
#  2) Faction name.
#  3) Faction flags. See header_factions.py for a list of available flags
#  4) Faction coherence. Relation between members of this faction.
#		Values range between 0.0 and 1.0.
#  5) Relations. This is a list of relation records.
#     Each relation record is a tuple that contains the following fields:
#    5.1) Faction. Which other faction this relation is referring to
#    5.2) Value: Relation value between the two factions.
#         Values range between -1 and 1.
#  6) Ranks
#  7) Faction color (default is gray)
# #######################################################################

# #######################################################################		
#	I have never, ever seen Ranks used, I have no idea what it does.
#	I believe it's depreciated from earlier iterations.
# #######################################################################



factions = [
    
	# #######################################################################
	# 		These Three are Hardcoded
	# #######################################################################

	("no_faction", "No Faction", 0, 0.9, [], []),
	("commoners", "Commoners", 0, 0.1, [], []),
	("outlaws", "Outlaws", max_player_rating(-30), 0.5, [("commoners",-0.6)], [], 0x888888),
	
	# #######################################################################
	#		Add new factions after here
	# #######################################################################
]
