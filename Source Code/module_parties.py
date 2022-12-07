from header_common import *
from header_parties import *
from ID_troops import *
from ID_factions import *
from ID_party_templates import *
from ID_map_icons import *


# #######################################################################
#
#	("party_id", "party_name", flags, menu, pt_template, faction, personality, ai_behavior, ai_target, (initial_x, initial_y), [(troop, num_of_troops, troop_flags)], party_rotation),
#
#  Each party record contains the following fields:
#  1) Party id: used for referencing parties in other files.
#     The prefix p_ is automatically added before each party id.
#  2) Party name.
#  3) Party flags. See header_parties.py for a list of available flags
#  4) Menu. ID of the menu to use when this party is met. The value 0 uses the default party encounter system.
#  5) Party-template. ID of the party template this party belongs to. Use pt_none as the default value.
#  6) Faction.
#  7) Personality. See header_parties.py for an explanation of personality flags.
#  8) Ai-behavior
#  9) Ai-target party
# 10) Initial coordinates.
# 11) List of stacks. Each stack record is a triple that contains the following fields:
#   11.1) Troop-id. 
#   11.2) Number of troops in this stack. 
#   11.3) Member flags. Use pmf_is_prisoner to note that this member is a prisoner.
# 12) Party direction in degrees [optional]
# #######################################################################


# #######################################################################
# 		Definitions
#			Basically a way to make common declarations more humanly readable.
#			Defintely not hardcoded, but a good reference.
# #######################################################################
pt_none = 0

# #######################################################################
#		Parties
# #######################################################################
parties = [
    
	# #######################################################################
	#		Hardcoded, in both order and name.
	# #######################################################################
	
    ("main_party", "Main Party", icon_player|pf_limit_members, 0, pt_none, fac_commoners, 0, ai_bhvr_hold, 0, (17, 52.5), [(trp_player, 1, 0)]),
    ("temp_party", "{!}temp_party", pf_disabled, 0, pt_none, fac_commoners, 0, ai_bhvr_hold, 0, (0, 0), []),
    ("camp_bandits", "{!}camp_bandits", pf_disabled, 0, pt_none, fac_commoners, 0, ai_bhvr_attack_party, 0,(1, 1), [(trp_temp_troop, 3, 0)]),

	# #######################################################################
	#		Run free, my child!
	# #######################################################################
]
