from header_common import *
from header_parties import *
from ID_troops import *
from ID_factions import *
from ID_map_icons import *

pmf_is_prisoner = 0x0001

####################################################################################################################
#  Each party template record contains the following fields:
#  1) Party-template id: used for referencing party-templates in other files.
#     The prefix pt_ is automatically added before each party-template id.
#  2) Party-template name.
#  3) Party flags. See header_parties.py for a list of available flags
#  4) Menu. ID of the menu to use when this party is met. The value 0 uses the default party encounter system.
#  5) Faction
#  6) Personality. See header_parties.py for an explanation of personality flags.
#  7) List of stacks. Each stack record is a tuple that contains the following fields:
#    7.1) Troop-id. 
#    7.2) Minimum number of troops in the stack. 
#    7.3) Maximum number of troops in the stack. 
#    7.4) Member flags(optional). Use pmf_is_prisoner to note that this member is a prisoner.
#     Note: There can be at most 6 stacks.
####################################################################################################################


party_templates = [
  ("none","none",icon_gray_knight,0,fac_commoners,merchant_personality,[]),
  ("rescued_prisoners","Rescued Prisoners",icon_gray_knight,0,fac_commoners,merchant_personality,[]),
  ("enemy","Enemy",icon_gray_knight,0,fac_undeads,merchant_personality,[]),
  ("hero_party","Hero Party",icon_gray_knight,0,fac_commoners,merchant_personality,[]),
####################################################################################################################
# Party templates before this point are hard-wired into the game and should not be changed. 
####################################################################################################################
##  ("old_garrison","Old Garrison",icon_vaegir_knight,0,fac_neutral,merchant_personality,[]),
  ("village_defenders","Village Defenders",icon_peasant,0,fac_commoners,merchant_personality,[(trp_farmer,10,20),(trp_peasant_woman,0,4)]),

  ("cattle_herd","Cattle Herd",icon_cattle|carries_goods(10),0,fac_neutral,merchant_personality,[(trp_cattle,80,120)]),

##  ("vaegir_nobleman","Vaegir Nobleman",icon_vaegir_knight|carries_goods(10)|pf_quest_party,0,fac_commoners,merchant_personality,[(trp_nobleman,1,1),(trp_vaegir_knight,2,6),(trp_vaegir_horseman,4,12)]),
##  ("swadian_nobleman","Swadian Nobleman",icon_gray_knight|carries_goods(10)|pf_quest_party,0,fac_commoners,merchant_personality,[(trp_nobleman,1,1),(trp_swadian_knight,2,6),(trp_swadian_man_at_arms,4,12)]),
# Ryan BEGIN
  ("looters","Rural Outlaws",icon_axeman|carries_goods(7),0,fac_outlaws,bandit_personality,[(trp_european_outlaw_rural1,5,10),(trp_european_outlaw_rural2,4,8),(trp_european_outlaw_rural3,3,6),(trp_european_outlaw_rural4,2,4)]),
# Ryan END
  ("manhunters","Manhunters",icon_gray_knight,0,fac_manhunters,soldier_personality,[(trp_manhunter,9,40)]),
##  ("peasant","Peasant",icon_peasant,0,fac_commoners,merchant_personality,[(trp_farmer,1,6),(trp_peasant_woman,0,7)]),

#  ("black_khergit_raiders","Black Khergit Raiders",icon_khergit_horseman_b|carries_goods(2),0,fac_black_khergits,bandit_personality,[(trp_black_khergit_guard,1,10),(trp_black_khergit_horseman,5,5)]),
  ("steppe_bandits","Steppe Raiders",icon_khergit|carries_goods(2),0,fac_outlaws,bandit_personality,[(trp_steppe_bandit,4,58)]),
  ("taiga_bandits","Bandits",icon_axeman|carries_goods(2),0,fac_outlaws,bandit_personality,[(trp_taiga_bandit,4,58)]),
  ("desert_bandits","Desert Bandits",icon_vaegir_knight|carries_goods(2),0,fac_outlaws,bandit_personality,[(trp_desert_bandit,4,58)]),
  ("forest_bandits","Suburban Outlaws",icon_axeman|carries_goods(3),0,fac_forest_bandits,bandit_personality,[(trp_european_outlaw_suburban1,4,9),(trp_european_outlaw_suburban2,3,7),(trp_european_outlaw_suburban3,2,5),(trp_european_outlaw_suburban4,1,3)]),
  ("mountain_bandits","Bandits",icon_axeman|carries_goods(2),0,fac_mountain_bandits,bandit_personality,[(trp_mountain_bandit,4,60)]),
  ("sea_raiders","Urban Outlaws",icon_axeman|carries_goods(4),0,fac_outlaws,bandit_personality,[(trp_european_outlaw_urban1,4,6),(trp_european_outlaw_urban2,3,5),(trp_european_outlaw_urban3,2,4),(trp_european_outlaw_urban4,1,2)]),

  ("deserters","Deserters",icon_vaegir_knight|carries_goods(3),0,fac_deserters,bandit_personality,[]),
    
  ("merchant_caravan","Merchant Caravan",icon_gray_knight|carries_goods(20)|pf_auto_remove_in_town|pf_quest_party,0,fac_commoners,escorted_merchant_personality,[(trp_caravan_master,1,1),(trp_caravan_guard,5,25)]),
  ("troublesome_bandits","Troublesome Bandits",icon_axeman|carries_goods(9)|pf_quest_party,0,fac_outlaws,bandit_personality,[(trp_bandit,14,55)]),
  ("bandits_awaiting_ransom","Bandits Awaiting Ransom",icon_axeman|carries_goods(9)|pf_auto_remove_in_town|pf_quest_party,0,fac_neutral,bandit_personality,[(trp_bandit,24,58),(trp_kidnapped_girl,1,1,pmf_is_prisoner)]),
  ("kidnapped_girl","Kidnapped Girl",icon_woman|pf_quest_party,0,fac_neutral,merchant_personality,[(trp_kidnapped_girl,1,1)]),

  ("village_farmers","Village Farmers",icon_peasant|pf_civilian,0,fac_innocents,merchant_personality,[(trp_farmer,5,10),(trp_peasant_woman,3,8)]),

  ("spy_partners", "Unremarkable Travellers", icon_gray_knight|carries_goods(10)|pf_default_behavior|pf_quest_party,0,fac_neutral,merchant_personality,[(trp_spy_partner,1,1),(trp_caravan_guard,5,11)]),
  ("runaway_serfs","Runaway Serfs",icon_peasant|carries_goods(8)|pf_default_behavior|pf_quest_party,0,fac_neutral,merchant_personality,[(trp_farmer,6,7), (trp_peasant_woman,3,3)]),
  ("spy", "Ordinary Townsman", icon_gray_knight|carries_goods(4)|pf_default_behavior|pf_quest_party,0,fac_neutral,merchant_personality,[(trp_spy,1,1)]),
  ("sacrificed_messenger", "Sacrificed Messenger", icon_gray_knight|carries_goods(3)|pf_default_behavior|pf_quest_party,0,fac_neutral,merchant_personality,[]),
##  ("conspirator", "Conspirators", icon_gray_knight|carries_goods(8)|pf_default_behavior|pf_quest_party,0,fac_neutral,merchant_personality,[(trp_conspirator,3,4)]),
##  ("conspirator_leader", "Conspirator Leader", icon_gray_knight|carries_goods(8)|pf_default_behavior|pf_quest_party,0,fac_neutral,merchant_personality,[(trp_conspirator_leader,1,1)]),
##  ("peasant_rebels", "Peasant Rebels", icon_peasant,0,fac_peasant_rebels,bandit_personality,[(trp_peasant_rebel,33,97)]),
##  ("noble_refugees", "Noble Refugees", icon_gray_knight|carries_goods(12)|pf_quest_party,0,fac_noble_refugees,merchant_personality,[(trp_noble_refugee,3,5),(trp_noble_refugee_woman,5,7)]),

  ("forager_party","Foraging Party",icon_gray_knight|carries_goods(5)|pf_show_faction,0,fac_commoners,merchant_personality,[]),
  ("scout_party","Scouts",icon_gray_knight|carries_goods(1)|pf_show_faction,0,fac_commoners,bandit_personality,[]),
  ("patrol_party","Patrol",icon_gray_knight|carries_goods(2)|pf_show_faction,0,fac_commoners,soldier_personality,[]),
#  ("war_party", "War Party",icon_gray_knight|carries_goods(3),0,fac_commoners,soldier_personality,[]),
  ("messenger_party","Messenger",icon_gray_knight|pf_show_faction,0,fac_commoners,merchant_personality,[]),
  ("raider_party","Raiders",icon_gray_knight|carries_goods(16)|pf_quest_party,0,fac_commoners,bandit_personality,[]),
  ("raider_captives","Raider Captives",0,0,fac_commoners,0,[(trp_peasant_woman,6,30,pmf_is_prisoner)]),
  ("kingdom_caravan_party","Caravan",icon_mule|carries_goods(25)|pf_show_faction,0,fac_commoners,merchant_personality,[(trp_caravan_master,1,1),(trp_caravan_guard,12,40)]),
  ("prisoner_train_party","Prisoner Train",icon_gray_knight|carries_goods(5)|pf_show_faction,0,fac_commoners,merchant_personality,[]),
  ("default_prisoners","Default Prisoners",0,0,fac_commoners,0,[(trp_bandit,5,10,pmf_is_prisoner)]),

  ("routed_warriors","Routed Enemies",icon_vaegir_knight,0,fac_commoners,soldier_personality,[]),


# Caravans
  ("center_reinforcements","Reinforcements",icon_axeman|carries_goods(16),0,fac_commoners,soldier_personality,[(trp_townsman,5,30),(trp_watchman,4,20)]),  

  ("kingdom_hero_party","War Party",icon_flagbearer_a|pf_show_faction|pf_default_behavior,0,fac_commoners,soldier_personality,[]),
  
# Reinforcements
  # each faction includes three party templates. One is less-modernised, one is med-modernised and one is high-modernised
  # less-modernised templates are generally includes 7-14 troops in total, 
  # med-modernised templates are generally includes 5-10 troops in total, 
  # high-modernised templates are generally includes 3-5 troops in total

  ("kingdom_1_reinforcements_a", "{!}kingdom_1_reinforcements_a", 0, 0, fac_commoners, 0, [(trp_swadian_recruit,5,10),(trp_swadian_militia,2,4)]),
  ("kingdom_1_reinforcements_b", "{!}kingdom_1_reinforcements_b", 0, 0, fac_commoners, 0, [(trp_swadian_footman,3,6),(trp_swadian_skirmisher,2,4)]),
  ("kingdom_1_reinforcements_c", "{!}kingdom_1_reinforcements_c", 0, 0, fac_commoners, 0, [(trp_swadian_man_at_arms,2,4),(trp_swadian_crossbowman,1,2)]), #Swadians are a bit less-powered thats why they have a bit more troops in their modernised party template (3-6, others 3-5)

  ("kingdom_2_reinforcements_a", "{!}kingdom_2_reinforcements_a", 0, 0, fac_commoners, 0, [(trp_vaegir_recruit,5,10),(trp_vaegir_footman,2,4)]),
  ("kingdom_2_reinforcements_b", "{!}kingdom_2_reinforcements_b", 0, 0, fac_commoners, 0, [(trp_vaegir_veteran,2,4),(trp_vaegir_skirmisher,2,4),(trp_vaegir_footman,1,2)]),
  ("kingdom_2_reinforcements_c", "{!}kingdom_2_reinforcements_c", 0, 0, fac_commoners, 0, [(trp_vaegir_horseman,2,3),(trp_vaegir_infantry,1,2)]),

  ("kingdom_3_reinforcements_a", "{!}kingdom_3_reinforcements_a", 0, 0, fac_commoners, 0, [(trp_khergit_tribesman,3,5),(trp_khergit_skirmisher,4,9)]), #Khergits are a bit less-powered thats why they have a bit more 2nd upgraded(trp_khergit_skirmisher) than non-upgraded one(trp_khergit_tribesman).
  ("kingdom_3_reinforcements_b", "{!}kingdom_3_reinforcements_b", 0, 0, fac_commoners, 0, [(trp_khergit_horseman,2,4),(trp_khergit_horse_archer,2,4),(trp_khergit_skirmisher,1,2)]),
  ("kingdom_3_reinforcements_c", "{!}kingdom_3_reinforcements_c", 0, 0, fac_commoners, 0, [(trp_khergit_horseman,2,4),(trp_khergit_veteran_horse_archer,2,3)]), #Khergits are a bit less-powered thats why they have a bit more troops in their modernised party template (4-7, others 3-5)

  ("kingdom_4_reinforcements_a", "{!}kingdom_4_reinforcements_a", 0, 0, fac_commoners, 0, [(trp_nord_footman,5,10),(trp_nord_recruit,2,4)]),
  ("kingdom_4_reinforcements_b", "{!}kingdom_4_reinforcements_b", 0, 0, fac_commoners, 0, [(trp_nord_huntsman,2,5),(trp_nord_archer,2,3),(trp_nord_footman,1,2)]),
  ("kingdom_4_reinforcements_c", "{!}kingdom_4_reinforcements_c", 0, 0, fac_commoners, 0, [(trp_nord_warrior,3,5)]),

  ("kingdom_5_reinforcements_a", "{!}kingdom_5_reinforcements_a", 0, 0, fac_commoners, 0, [(trp_rhodok_tribesman,5,10),(trp_rhodok_spearman,2,4)]),
  ("kingdom_5_reinforcements_b", "{!}kingdom_5_reinforcements_b", 0, 0, fac_commoners, 0, [(trp_rhodok_crossbowman,3,6),(trp_rhodok_trained_crossbowman,2,4)]),
  ("kingdom_5_reinforcements_c", "{!}kingdom_5_reinforcements_c", 0, 0, fac_commoners, 0, [(trp_rhodok_veteran_spearman,2,3),(trp_rhodok_veteran_crossbowman,1,2)]), 

  ("kingdom_6_reinforcements_a", "{!}kingdom_6_reinforcements_a", 0, 0, fac_commoners, 0, [(trp_sarranid_recruit,5,10),(trp_sarranid_footman,2,4)]),
  ("kingdom_6_reinforcements_b", "{!}kingdom_6_reinforcements_b", 0, 0, fac_commoners, 0, [(trp_sarranid_skirmisher,2,4),(trp_sarranid_veteran_footman,2,3),(trp_sarranid_footman,1,3)]),
  ("kingdom_6_reinforcements_c", "{!}kingdom_6_reinforcements_c", 0, 0, fac_commoners, 0, [(trp_sarranid_horseman,3,5)]),


  ("faction1_reinforcements_a", "{!}faction1_reinforcements_a", 0, 0, fac_commoners, 0, [(trp_faction1_troop1,2,4),(trp_faction1_troop2,5,7)]),
  ("faction1_reinforcements_b", "{!}faction1_reinforcements_b", 0, 0, fac_commoners, 0, [(trp_faction1_troop3,5,7),(trp_faction1_troop4,2,4)]),
  ("faction1_reinforcements_c", "{!}faction1_reinforcements_c", 0, 0, fac_commoners, 0, [(trp_faction1_troop5,2,4),(trp_faction1_troop6,1,2)]),
  ("faction2_reinforcements_a", "{!}faction2_reinforcements_a", 0, 0, fac_commoners, 0, [(trp_faction2_troop1,2,4),(trp_faction2_troop2,5,7)]),
  ("faction2_reinforcements_b", "{!}faction2_reinforcements_b", 0, 0, fac_commoners, 0, [(trp_faction2_troop3,5,7),(trp_faction2_troop4,2,4)]),
  ("faction2_reinforcements_c", "{!}faction2_reinforcements_c", 0, 0, fac_commoners, 0, [(trp_faction2_troop5,2,4),(trp_faction2_troop6,1,2)]),
  ("faction3_reinforcements_a", "{!}faction3_reinforcements_a", 0, 0, fac_commoners, 0, [(trp_faction3_troop1,2,4),(trp_faction3_troop2,5,7)]),
  ("faction3_reinforcements_b", "{!}faction3_reinforcements_b", 0, 0, fac_commoners, 0, [(trp_faction3_troop3,5,7),(trp_faction3_troop4,2,4)]),
  ("faction3_reinforcements_c", "{!}faction3_reinforcements_c", 0, 0, fac_commoners, 0, [(trp_faction3_troop5,2,4),(trp_faction3_troop6,1,2)]),
  ("faction4_reinforcements_a", "{!}faction4_reinforcements_a", 0, 0, fac_commoners, 0, [(trp_faction4_troop1,2,4),(trp_faction4_troop2,5,7)]),
  ("faction4_reinforcements_b", "{!}faction4_reinforcements_b", 0, 0, fac_commoners, 0, [(trp_faction4_troop3,5,7),(trp_faction4_troop4,2,4)]),
  ("faction4_reinforcements_c", "{!}faction4_reinforcements_c", 0, 0, fac_commoners, 0, [(trp_faction4_troop5,2,4),(trp_faction4_troop6,1,2)]),
  ("faction5_reinforcements_a", "{!}faction5_reinforcements_a", 0, 0, fac_commoners, 0, [(trp_faction5_troop1,2,4),(trp_faction5_troop2,5,7)]),
  ("faction5_reinforcements_b", "{!}faction5_reinforcements_b", 0, 0, fac_commoners, 0, [(trp_faction5_troop3,5,7),(trp_faction5_troop4,2,4)]),
  ("faction5_reinforcements_c", "{!}faction5_reinforcements_c", 0, 0, fac_commoners, 0, [(trp_faction5_troop5,2,4),(trp_faction5_troop6,1,2)]),
  ("faction6_reinforcements_a", "{!}faction6_reinforcements_a", 0, 0, fac_commoners, 0, [(trp_faction6_troop1,2,4),(trp_faction6_troop2,5,7)]),
  ("faction6_reinforcements_b", "{!}faction6_reinforcements_b", 0, 0, fac_commoners, 0, [(trp_faction6_troop3,5,7),(trp_faction6_troop4,2,4)]),
  ("faction6_reinforcements_c", "{!}faction6_reinforcements_c", 0, 0, fac_commoners, 0, [(trp_faction6_troop5,2,4),(trp_faction6_troop6,1,2)]),
  ("faction7_reinforcements_a", "{!}faction7_reinforcements_a", 0, 0, fac_commoners, 0, [(trp_faction7_troop1,2,4),(trp_faction7_troop2,5,7)]),
  ("faction7_reinforcements_b", "{!}faction7_reinforcements_b", 0, 0, fac_commoners, 0, [(trp_faction7_troop3,5,7),(trp_faction7_troop4,2,4)]),
  ("faction7_reinforcements_c", "{!}faction7_reinforcements_c", 0, 0, fac_commoners, 0, [(trp_faction7_troop5,2,4),(trp_faction7_troop6,1,2)]),
  ("faction8_reinforcements_a", "{!}faction8_reinforcements_a", 0, 0, fac_commoners, 0, [(trp_faction8_troop1,2,4),(trp_faction8_troop2,5,7)]),
  ("faction8_reinforcements_b", "{!}faction8_reinforcements_b", 0, 0, fac_commoners, 0, [(trp_faction8_troop3,5,7),(trp_faction8_troop4,2,4)]),
  ("faction8_reinforcements_c", "{!}faction8_reinforcements_c", 0, 0, fac_commoners, 0, [(trp_faction8_troop5,2,4),(trp_faction8_troop6,1,2)]),
  ("faction9_reinforcements_a", "{!}faction9_reinforcements_a", 0, 0, fac_commoners, 0, [(trp_faction9_troop1,2,4),(trp_faction9_troop2,5,7)]),
  ("faction9_reinforcements_b", "{!}faction9_reinforcements_b", 0, 0, fac_commoners, 0, [(trp_faction9_troop3,5,7),(trp_faction9_troop4,2,4)]),
  ("faction9_reinforcements_c", "{!}faction9_reinforcements_c", 0, 0, fac_commoners, 0, [(trp_faction9_troop5,2,4),(trp_faction9_troop6,1,2)]),
  ("faction10_reinforcements_a", "{!}faction10_reinforcements_a", 0, 0, fac_commoners, 0, [(trp_faction10_troop1,2,4),(trp_faction10_troop2,5,7)]),
  ("faction10_reinforcements_b", "{!}faction10_reinforcements_b", 0, 0, fac_commoners, 0, [(trp_faction10_troop3,5,7),(trp_faction10_troop4,2,4)]),
  ("faction10_reinforcements_c", "{!}faction10_reinforcements_c", 0, 0, fac_commoners, 0, [(trp_faction10_troop5,2,4),(trp_faction10_troop6,1,2)]),
  ("faction11_reinforcements_a", "{!}faction11_reinforcements_a", 0, 0, fac_commoners, 0, [(trp_faction11_troop1,2,4),(trp_faction11_troop2,5,7)]),
  ("faction11_reinforcements_b", "{!}faction11_reinforcements_b", 0, 0, fac_commoners, 0, [(trp_faction11_troop3,5,7),(trp_faction11_troop4,2,4)]),
  ("faction11_reinforcements_c", "{!}faction11_reinforcements_c", 0, 0, fac_commoners, 0, [(trp_faction11_troop5,2,4),(trp_faction11_troop6,1,2)]),
  ("faction12_reinforcements_a", "{!}faction12_reinforcements_a", 0, 0, fac_commoners, 0, [(trp_faction12_troop1,2,4),(trp_faction12_troop2,5,7)]),
  ("faction12_reinforcements_b", "{!}faction12_reinforcements_b", 0, 0, fac_commoners, 0, [(trp_faction12_troop3,5,7),(trp_faction12_troop4,2,4)]),
  ("faction12_reinforcements_c", "{!}faction12_reinforcements_c", 0, 0, fac_commoners, 0, [(trp_faction12_troop5,2,4),(trp_faction12_troop6,1,2)]),
  ("faction13_reinforcements_a", "{!}faction13_reinforcements_a", 0, 0, fac_commoners, 0, [(trp_faction13_troop1,2,4),(trp_faction13_troop2,5,7)]),
  ("faction13_reinforcements_b", "{!}faction13_reinforcements_b", 0, 0, fac_commoners, 0, [(trp_faction13_troop3,5,7),(trp_faction13_troop4,2,4)]),
  ("faction13_reinforcements_c", "{!}faction13_reinforcements_c", 0, 0, fac_commoners, 0, [(trp_faction13_troop5,2,4),(trp_faction13_troop6,1,2)]),
  ("faction14_reinforcements_a", "{!}faction14_reinforcements_a", 0, 0, fac_commoners, 0, [(trp_faction14_troop1,2,4),(trp_faction14_troop2,5,7)]),
  ("faction14_reinforcements_b", "{!}faction14_reinforcements_b", 0, 0, fac_commoners, 0, [(trp_faction14_troop3,5,7),(trp_faction14_troop4,2,4)]),
  ("faction14_reinforcements_c", "{!}faction14_reinforcements_c", 0, 0, fac_commoners, 0, [(trp_faction14_troop5,2,4),(trp_faction14_troop6,1,2)]),
  ("faction15_reinforcements_a", "{!}faction15_reinforcements_a", 0, 0, fac_commoners, 0, [(trp_faction15_troop1,2,4),(trp_faction15_troop2,5,7)]),
  ("faction15_reinforcements_b", "{!}faction15_reinforcements_b", 0, 0, fac_commoners, 0, [(trp_faction15_troop3,5,7),(trp_faction15_troop4,2,4)]),
  ("faction15_reinforcements_c", "{!}faction15_reinforcements_c", 0, 0, fac_commoners, 0, [(trp_faction15_troop5,2,4),(trp_faction15_troop6,1,2)]),
  ("faction16_reinforcements_a", "{!}faction16_reinforcements_a", 0, 0, fac_commoners, 0, [(trp_faction16_troop1,2,4),(trp_faction16_troop2,5,7)]),
  ("faction16_reinforcements_b", "{!}faction16_reinforcements_b", 0, 0, fac_commoners, 0, [(trp_faction16_troop3,5,7),(trp_faction16_troop4,2,4)]),
  ("faction16_reinforcements_c", "{!}faction16_reinforcements_c", 0, 0, fac_commoners, 0, [(trp_faction16_troop5,2,4),(trp_faction16_troop6,1,2)]),
  ("faction17_reinforcements_a", "{!}faction17_reinforcements_a", 0, 0, fac_commoners, 0, [(trp_faction17_troop1,2,4),(trp_faction17_troop2,5,7)]),
  ("faction17_reinforcements_b", "{!}faction17_reinforcements_b", 0, 0, fac_commoners, 0, [(trp_faction17_troop3,5,7),(trp_faction17_troop4,2,4)]),
  ("faction17_reinforcements_c", "{!}faction17_reinforcements_c", 0, 0, fac_commoners, 0, [(trp_faction17_troop5,2,4),(trp_faction17_troop6,1,2)]),
  ("faction18_reinforcements_a", "{!}faction18_reinforcements_a", 0, 0, fac_commoners, 0, [(trp_faction18_troop1,2,4),(trp_faction18_troop2,5,7)]),
  ("faction18_reinforcements_b", "{!}faction18_reinforcements_b", 0, 0, fac_commoners, 0, [(trp_faction18_troop3,5,7),(trp_faction18_troop4,2,4)]),
  ("faction18_reinforcements_c", "{!}faction18_reinforcements_c", 0, 0, fac_commoners, 0, [(trp_faction18_troop5,2,4),(trp_faction18_troop6,1,2)]),
  ("faction19_reinforcements_a", "{!}faction19_reinforcements_a", 0, 0, fac_commoners, 0, [(trp_faction19_troop1,2,4),(trp_faction19_troop2,5,7)]),
  ("faction19_reinforcements_b", "{!}faction19_reinforcements_b", 0, 0, fac_commoners, 0, [(trp_faction19_troop3,5,7),(trp_faction19_troop4,2,4)]),
  ("faction19_reinforcements_c", "{!}faction19_reinforcements_c", 0, 0, fac_commoners, 0, [(trp_faction19_troop5,2,4),(trp_faction19_troop6,1,2)]),
  ("faction20_reinforcements_a", "{!}faction20_reinforcements_a", 0, 0, fac_commoners, 0, [(trp_faction20_troop1,2,4),(trp_faction20_troop2,5,7)]),
  ("faction20_reinforcements_b", "{!}faction20_reinforcements_b", 0, 0, fac_commoners, 0, [(trp_faction20_troop3,5,7),(trp_faction20_troop4,2,4)]),
  ("faction20_reinforcements_c", "{!}faction20_reinforcements_c", 0, 0, fac_commoners, 0, [(trp_faction20_troop5,2,4),(trp_faction20_troop6,1,2)]),
  ("faction21_reinforcements_a", "{!}faction21_reinforcements_a", 0, 0, fac_commoners, 0, [(trp_faction21_troop1,2,4),(trp_faction21_troop2,5,7)]),
  ("faction21_reinforcements_b", "{!}faction21_reinforcements_b", 0, 0, fac_commoners, 0, [(trp_faction21_troop3,5,7),(trp_faction21_troop4,2,4)]),
  ("faction21_reinforcements_c", "{!}faction21_reinforcements_c", 0, 0, fac_commoners, 0, [(trp_faction21_troop5,2,4),(trp_faction21_troop6,1,2)]),
  ("faction22_reinforcements_a", "{!}faction22_reinforcements_a", 0, 0, fac_commoners, 0, [(trp_faction22_troop1,2,4),(trp_faction22_troop2,5,7)]),
  ("faction22_reinforcements_b", "{!}faction22_reinforcements_b", 0, 0, fac_commoners, 0, [(trp_faction22_troop3,5,7),(trp_faction22_troop4,2,4)]),
  ("faction22_reinforcements_c", "{!}faction22_reinforcements_c", 0, 0, fac_commoners, 0, [(trp_faction22_troop5,2,4),(trp_faction22_troop6,1,2)]),
  ("faction23_reinforcements_a", "{!}faction23_reinforcements_a", 0, 0, fac_commoners, 0, [(trp_faction23_troop1,2,4),(trp_faction23_troop2,5,7)]),
  ("faction23_reinforcements_b", "{!}faction23_reinforcements_b", 0, 0, fac_commoners, 0, [(trp_faction23_troop3,5,7),(trp_faction23_troop4,2,4)]),
  ("faction23_reinforcements_c", "{!}faction23_reinforcements_c", 0, 0, fac_commoners, 0, [(trp_faction23_troop5,2,4),(trp_faction23_troop6,1,2)]),
  ("faction24_reinforcements_a", "{!}faction24_reinforcements_a", 0, 0, fac_commoners, 0, [(trp_faction24_troop1,2,4),(trp_faction24_troop2,5,7)]),
  ("faction24_reinforcements_b", "{!}faction24_reinforcements_b", 0, 0, fac_commoners, 0, [(trp_faction24_troop3,5,7),(trp_faction24_troop4,2,4)]),
  ("faction24_reinforcements_c", "{!}faction24_reinforcements_c", 0, 0, fac_commoners, 0, [(trp_faction24_troop5,2,4),(trp_faction24_troop6,1,2)]),
  ("faction25_reinforcements_a", "{!}faction25_reinforcements_a", 0, 0, fac_commoners, 0, [(trp_faction25_troop1,2,4),(trp_faction25_troop2,5,7)]),
  ("faction25_reinforcements_b", "{!}faction25_reinforcements_b", 0, 0, fac_commoners, 0, [(trp_faction25_troop3,5,7),(trp_faction25_troop4,2,4)]),
  ("faction25_reinforcements_c", "{!}faction25_reinforcements_c", 0, 0, fac_commoners, 0, [(trp_faction25_troop5,2,4),(trp_faction25_troop6,1,2)]),
  ("faction26_reinforcements_a", "{!}faction26_reinforcements_a", 0, 0, fac_commoners, 0, [(trp_faction26_troop1,2,4),(trp_faction26_troop2,5,7)]),
  ("faction26_reinforcements_b", "{!}faction26_reinforcements_b", 0, 0, fac_commoners, 0, [(trp_faction26_troop3,5,7),(trp_faction26_troop4,2,4)]),
  ("faction26_reinforcements_c", "{!}faction26_reinforcements_c", 0, 0, fac_commoners, 0, [(trp_faction26_troop5,2,4),(trp_faction26_troop6,1,2)]),
  ("faction27_reinforcements_a", "{!}faction27_reinforcements_a", 0, 0, fac_commoners, 0, [(trp_faction27_troop1,2,4),(trp_faction27_troop2,5,7)]),
  ("faction27_reinforcements_b", "{!}faction27_reinforcements_b", 0, 0, fac_commoners, 0, [(trp_faction27_troop3,5,7),(trp_faction27_troop4,2,4)]),
  ("faction27_reinforcements_c", "{!}faction27_reinforcements_c", 0, 0, fac_commoners, 0, [(trp_faction27_troop5,2,4),(trp_faction27_troop6,1,2)]),
  ("faction28_reinforcements_a", "{!}faction28_reinforcements_a", 0, 0, fac_commoners, 0, [(trp_faction28_troop1,2,4),(trp_faction28_troop2,5,7)]),
  ("faction28_reinforcements_b", "{!}faction28_reinforcements_b", 0, 0, fac_commoners, 0, [(trp_faction28_troop3,5,7),(trp_faction28_troop4,2,4)]),
  ("faction28_reinforcements_c", "{!}faction28_reinforcements_c", 0, 0, fac_commoners, 0, [(trp_faction28_troop5,2,4),(trp_faction28_troop6,1,2)]),
  ("faction29_reinforcements_a", "{!}faction29_reinforcements_a", 0, 0, fac_commoners, 0, [(trp_faction29_troop1,2,4),(trp_faction29_troop2,5,7)]),
  ("faction29_reinforcements_b", "{!}faction29_reinforcements_b", 0, 0, fac_commoners, 0, [(trp_faction29_troop3,5,7),(trp_faction29_troop4,2,4)]),
  ("faction29_reinforcements_c", "{!}faction29_reinforcements_c", 0, 0, fac_commoners, 0, [(trp_faction29_troop5,2,4),(trp_faction29_troop6,1,2)]),
  ("faction30_reinforcements_a", "{!}faction30_reinforcements_a", 0, 0, fac_commoners, 0, [(trp_faction30_troop1,2,4),(trp_faction30_troop2,5,7)]),
  ("faction30_reinforcements_b", "{!}faction30_reinforcements_b", 0, 0, fac_commoners, 0, [(trp_faction30_troop3,5,7),(trp_faction30_troop4,2,4)]),
  ("faction30_reinforcements_c", "{!}faction30_reinforcements_c", 0, 0, fac_commoners, 0, [(trp_faction30_troop5,2,4),(trp_faction30_troop6,1,2)]),
  ("faction31_reinforcements_a", "{!}faction31_reinforcements_a", 0, 0, fac_commoners, 0, [(trp_faction31_troop1,2,4),(trp_faction31_troop2,5,7)]),
  ("faction31_reinforcements_b", "{!}faction31_reinforcements_b", 0, 0, fac_commoners, 0, [(trp_faction31_troop3,5,7),(trp_faction31_troop4,2,4)]),
  ("faction31_reinforcements_c", "{!}faction31_reinforcements_c", 0, 0, fac_commoners, 0, [(trp_faction31_troop5,2,4),(trp_faction31_troop6,1,2)]),
  ("faction32_reinforcements_a", "{!}faction32_reinforcements_a", 0, 0, fac_commoners, 0, [(trp_faction32_troop1,2,4),(trp_faction32_troop2,5,7)]),
  ("faction32_reinforcements_b", "{!}faction32_reinforcements_b", 0, 0, fac_commoners, 0, [(trp_faction32_troop3,5,7),(trp_faction32_troop4,2,4)]),
  ("faction32_reinforcements_c", "{!}faction32_reinforcements_c", 0, 0, fac_commoners, 0, [(trp_faction32_troop5,2,4),(trp_faction32_troop6,1,2)]),
  ("faction33_reinforcements_a", "{!}faction33_reinforcements_a", 0, 0, fac_commoners, 0, [(trp_faction33_troop1,2,4),(trp_faction33_troop2,5,7)]),
  ("faction33_reinforcements_b", "{!}faction33_reinforcements_b", 0, 0, fac_commoners, 0, [(trp_faction33_troop3,5,7),(trp_faction33_troop4,2,4)]),
  ("faction33_reinforcements_c", "{!}faction33_reinforcements_c", 0, 0, fac_commoners, 0, [(trp_faction33_troop5,2,4),(trp_faction33_troop6,1,2)]),
("factionplayer_reinforcements_artillery", "{!}reinforcements_artillery", 0, 0, fac_commoners, 0, [(trp_factionplayer_howitzer_cannoneer_officer,1,2)]),
("faction1_reinforcements_artillery", "{!}reinforcements_artillery", 0, 0, fac_commoners, 0, [(trp_faction1_howitzer_cannoneer_officer,1,2)]),
("faction2_reinforcements_artillery", "{!}reinforcements_artillery", 0, 0, fac_commoners, 0, [(trp_faction2_howitzer_cannoneer_officer,1,2)]),
("faction3_reinforcements_artillery", "{!}reinforcements_artillery", 0, 0, fac_commoners, 0, [(trp_faction3_howitzer_cannoneer_officer,1,2)]),
("faction4_reinforcements_artillery", "{!}reinforcements_artillery", 0, 0, fac_commoners, 0, [(trp_faction4_howitzer_cannoneer_officer,1,2)]),
("faction5_reinforcements_artillery", "{!}reinforcements_artillery", 0, 0, fac_commoners, 0, [(trp_faction5_howitzer_cannoneer_officer,1,2)]),
("faction6_reinforcements_artillery", "{!}reinforcements_artillery", 0, 0, fac_commoners, 0, [(trp_faction6_howitzer_cannoneer_officer,1,2)]),
("faction7_reinforcements_artillery", "{!}reinforcements_artillery", 0, 0, fac_commoners, 0, [(trp_faction7_howitzer_cannoneer_officer,1,2)]),
("faction8_reinforcements_artillery", "{!}reinforcements_artillery", 0, 0, fac_commoners, 0, [(trp_faction8_howitzer_cannoneer_officer,1,2)]),
("faction9_reinforcements_artillery", "{!}reinforcements_artillery", 0, 0, fac_commoners, 0, [(trp_faction9_howitzer_cannoneer_officer,1,2)]),
("faction10_reinforcements_artillery", "{!}reinforcements_artillery", 0, 0, fac_commoners, 0, [(trp_faction10_howitzer_cannoneer_officer,1,2)]),
("faction11_reinforcements_artillery", "{!}reinforcements_artillery", 0, 0, fac_commoners, 0, [(trp_faction11_howitzer_cannoneer_officer,1,2)]),
("faction12_reinforcements_artillery", "{!}reinforcements_artillery", 0, 0, fac_commoners, 0, [(trp_faction12_howitzer_cannoneer_officer,1,2)]),
("faction13_reinforcements_artillery", "{!}reinforcements_artillery", 0, 0, fac_commoners, 0, [(trp_faction13_howitzer_cannoneer_officer,1,2)]),
("faction14_reinforcements_artillery", "{!}reinforcements_artillery", 0, 0, fac_commoners, 0, [(trp_faction14_howitzer_cannoneer_officer,1,2)]),
("faction15_reinforcements_artillery", "{!}reinforcements_artillery", 0, 0, fac_commoners, 0, [(trp_faction15_howitzer_cannoneer_officer,1,2)]),
("faction16_reinforcements_artillery", "{!}reinforcements_artillery", 0, 0, fac_commoners, 0, [(trp_faction16_howitzer_cannoneer_officer,1,2)]),
("faction17_reinforcements_artillery", "{!}reinforcements_artillery", 0, 0, fac_commoners, 0, [(trp_faction17_howitzer_cannoneer_officer,1,2)]),
("faction18_reinforcements_artillery", "{!}reinforcements_artillery", 0, 0, fac_commoners, 0, [(trp_faction18_howitzer_cannoneer_officer,1,2)]),
("faction19_reinforcements_artillery", "{!}reinforcements_artillery", 0, 0, fac_commoners, 0, [(trp_faction19_howitzer_cannoneer_officer,1,2)]),
("faction20_reinforcements_artillery", "{!}reinforcements_artillery", 0, 0, fac_commoners, 0, [(trp_faction20_howitzer_cannoneer_officer,1,2)]),
("faction21_reinforcements_artillery", "{!}reinforcements_artillery", 0, 0, fac_commoners, 0, [(trp_faction21_howitzer_cannoneer_officer,1,2)]),
("faction22_reinforcements_artillery", "{!}reinforcements_artillery", 0, 0, fac_commoners, 0, [(trp_faction22_howitzer_cannoneer_officer,1,2)]),
("faction23_reinforcements_artillery", "{!}reinforcements_artillery", 0, 0, fac_commoners, 0, [(trp_faction23_howitzer_cannoneer_officer,1,2)]),
("faction24_reinforcements_artillery", "{!}reinforcements_artillery", 0, 0, fac_commoners, 0, [(trp_faction24_howitzer_cannoneer_officer,1,2)]),
("faction25_reinforcements_artillery", "{!}reinforcements_artillery", 0, 0, fac_commoners, 0, [(trp_faction25_howitzer_cannoneer_officer,1,2)]),
("faction26_reinforcements_artillery", "{!}reinforcements_artillery", 0, 0, fac_commoners, 0, [(trp_faction26_howitzer_cannoneer_officer,1,2)]),
("faction27_reinforcements_artillery", "{!}reinforcements_artillery", 0, 0, fac_commoners, 0, [(trp_faction27_howitzer_cannoneer_officer,1,2)]),
("faction28_reinforcements_artillery", "{!}reinforcements_artillery", 0, 0, fac_commoners, 0, [(trp_faction28_howitzer_cannoneer_officer,1,2)]),
("faction29_reinforcements_artillery", "{!}reinforcements_artillery", 0, 0, fac_commoners, 0, [(trp_faction29_howitzer_cannoneer_officer,1,2)]),
("faction30_reinforcements_artillery", "{!}reinforcements_artillery", 0, 0, fac_commoners, 0, [(trp_faction30_howitzer_cannoneer_officer,1,2)]),
("faction31_reinforcements_artillery", "{!}reinforcements_artillery", 0, 0, fac_commoners, 0, [(trp_faction31_howitzer_cannoneer_officer,1,2)]),
("faction32_reinforcements_artillery", "{!}reinforcements_artillery", 0, 0, fac_commoners, 0, [(trp_faction32_howitzer_cannoneer_officer,1,2)]),
("faction33_reinforcements_artillery", "{!}reinforcements_artillery", 0, 0, fac_commoners, 0, [(trp_faction33_howitzer_cannoneer_officer,1,2)]),

  ("steppe_bandit_lair" ,"Steppe Bandit Lair",icon_bandit_lair|carries_goods(2)|pf_is_static|pf_hide_defenders,0,fac_neutral,bandit_personality,[(trp_steppe_bandit,15,58)]),
  ("taiga_bandit_lair","Tundra Bandit Lair",icon_bandit_lair|carries_goods(2)|pf_is_static|pf_hide_defenders,0,fac_neutral,bandit_personality,[(trp_taiga_bandit,15,58)]),
  ("desert_bandit_lair" ,"Desert Bandit Lair",icon_bandit_lair|carries_goods(2)|pf_is_static|pf_hide_defenders,0,fac_neutral,bandit_personality,[(trp_desert_bandit,15,58)]),
  ("forest_bandit_lair" ,"Forest Bandit Camp",icon_bandit_lair|carries_goods(2)|pf_is_static|pf_hide_defenders,0,fac_neutral,bandit_personality,[(trp_forest_bandit,15,58)]),
  ("mountain_bandit_lair" ,"Mountain Bandit Hideout",icon_bandit_lair|carries_goods(2)|pf_is_static|pf_hide_defenders,0,fac_neutral,bandit_personality,[(trp_mountain_bandit,15,58)]),
  ("sea_raider_lair","Sea Raider Landing",icon_bandit_lair|carries_goods(2)|pf_is_static|pf_hide_defenders,0,fac_neutral,bandit_personality,[(trp_sea_raider,15,50)]),
  ("looter_lair","Kidnappers' Hideout",icon_bandit_lair|carries_goods(2)|pf_is_static|pf_hide_defenders,0,fac_neutral,bandit_personality,[(trp_looter,15,25)]),
  
  ("bandit_lair_templates_end","{!}bandit_lair_templates_end",icon_axeman|carries_goods(2)|pf_is_static,0,fac_outlaws,bandit_personality,[(trp_sea_raider,15,50)]),

  ("leaded_looters","Band of robbers",icon_axeman|carries_goods(8)|pf_quest_party,0,fac_neutral,bandit_personality,[(trp_looter_leader,1,1),(trp_looter,3,3)]),
  ("persian_bandits","Persian Bandits",icon_vaegir_knight|carries_goods(2),0,fac_outlaws,bandit_personality,[(trp_desert_bandit,4,58)]),
  ("turkish_bandits","Turkish Bandits",icon_vaegir_knight|carries_goods(2),0,fac_outlaws,bandit_personality,[(trp_desert_bandit,4,58)]),
  ("indian_bandits","Indian Bandits",icon_vaegir_knight|carries_goods(2),0,fac_outlaws,bandit_personality,[(trp_desert_bandit,4,58)]),
  ("middleasia_bandits","Middle Asian Bandits",icon_vaegir_knight|carries_goods(2),0,fac_outlaws,bandit_personality,[(trp_desert_bandit,4,58)]),
]


# modmerger_start version=201 type=2
try:
    component_name = "party_templates"
    var_set = { "party_templates" : party_templates }
    from modmerger import modmerge
    modmerge(var_set)
except:
    raise
# modmerger_end
