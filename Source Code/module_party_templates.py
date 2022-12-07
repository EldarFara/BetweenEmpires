from header_common import *
from header_parties import *
from ID_troops import *
from ID_factions import *
from ID_map_icons import *

pmf_is_prisoner = 0x0001

# #######################################################################
#	("template_id", "template_name", map_icon_id, menu_id, fac_id, merchant_personality, [(troop_id, troop_min. troop_max, flags)]),
#
#  Each party template record contains the following fields:
#  1) Party-template id: used for referencing party-templates in other files.
#     The prefix pt_ is automatically added before each party-template id.
#  2) Party-template name.
#  3) Party Icon, check module_map_icons to see available map icons.
#  4) Menu. ID of the menu to use when this party is met. The value 0 uses the default party encounter system.
#  5) Faction
#  6) Personality. See header_parties.py for an explanation of personality flags.
#  7) List of stacks. Each stack record is a tuple that contains the following fields:
#    7.1) Troop-id. 
#    7.2) Minimum number of troops in the stack. 
#    7.3) Maximum number of troops in the stack. 
#    7.4) Member flags(optional). Use pmf_is_prisoner to note that this member is a prisoner.
#     Note: There can be at most 6 stacks.
# #######################################################################



party_templates = [

    # #######################################################################
    # 		Hardcoded
	# #######################################################################
	
    ("none", "none", icon_player, 0, fac_commoners, merchant_personality, []),
    ("rescued_prisoners", "Rescued Prisoners", icon_player, 0, fac_commoners, merchant_personality, []),
    ("enemy", "Enemy", icon_player, 0, fac_commoners, merchant_personality, []),
    ("hero_party", "Hero Party", icon_player, 0, fac_commoners, merchant_personality, []),

    # #######################################################################
	#		Party on!
	# #######################################################################
]
