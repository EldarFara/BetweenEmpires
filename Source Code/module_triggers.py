from header_common import *
from header_operations import *
from header_parties import *
from header_items import *
from header_skills import *
from header_triggers import *
from header_troops import *
from module_constants import *

# #######################################################################
#	(check_interval, delay_interval, rearm_interval, [conditions], [consequences]),
#
#  Each trigger contains the following fields:
# 1) Check interval: How frequently this trigger will be checked
# 2) Delay interval: Time to wait before applying the consequences of the trigger
#    After its conditions have been evaluated as true.
# 3) Re-arm interval. How much time must pass after applying the consequences of the trigger for the trigger to become active again.
#    You can put the constant ti_once here to make sure that the trigger never becomes active again after it fires once.
# 4) Conditions block (list). This must be a valid operation block. See header_operations.py for reference.
#    Every time the trigger is checked, the conditions block will be executed.
#    If the conditions block returns true, the consequences block will be executed.
#    If the conditions block is empty, it is assumed that it always evaluates to true.
# 5) Consequences block (list). This must be a valid operation block. See header_operations.py for reference. 
# #######################################################################

# #######################################################################
#	Used on the overworld to trigger events if conditions are true 
#	during the interval of which it was checked. 
#
#	Used very often to do things like restock vendors, add parties 
#	to the map, and check quest progress. 
#
#	If you do not need to use the delay, rearm, and conditions 
#	use simple_triggers instead.
# #######################################################################

triggers = [

    (0, 0, 0, [],
    [
    ]),	
]
