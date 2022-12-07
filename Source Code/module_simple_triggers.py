from header_common import *
from header_operations import *
from header_parties import *
from header_items import *
from header_skills import *
from header_triggers import *
from header_troops import *
from header_music import *
from module_constants import *


# #######################################################################
#		(check-interval, [operations]),
#	Each simple trigger contains the following fields:
# 	1) Check interval: How frequently this trigger will be checked (in hours)
# 	2) Operation block: This must be a valid operation block. See header_operations.py for reference. 
# #######################################################################

# #######################################################################
#	So simple_triggers basically run off the game clock and are used 
#	to check things on the world map. You'll see them used pretty often
#	for like checking if the party is hungry and all that. Used instead
#	of module_triggers when there is no need for conditions or 
#	rearm and delay times.
# #######################################################################

simple_triggers = [

    (0,[]),
]
