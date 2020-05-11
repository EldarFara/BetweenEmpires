from header_factions import *

####################################################################################################################
#  Each faction record contains the following fields:
#  1) Faction id: used for referencing factions in other files.
#     The prefix fac_ is automatically added before each faction id.
#  2) Faction name.
#  3) Faction flags. See header_factions.py for a list of available flags
#  4) Faction coherence. Relation between members of this faction.
#  5) Relations. This is a list of relation records.
#     Each relation record is a tuple that contains the following fields:
#    5.1) Faction. Which other faction this relation is referring to
#    5.2) Value: Relation value between the two factions.
#         Values range between -1 and 1.
#  6) Ranks
#  7) Faction color (default is gray)
####################################################################################################################

default_kingdom_relations = [("outlaws",-0.05),("peasant_rebels", -0.1),("deserters", -0.05),("mountain_bandits", -0.02),("forest_bandits", -0.02)]
factions = [
  ("no_faction","No Faction",0, 0.9, [], []),
  ("commoners","Commoners",0, 0.1,[("player_faction",0.1)], []),
  ("outlaws","Outlaws", max_player_rating(-30), 0.5,[("commoners",-0.6),("player_faction",-0.15)], [], 0x888888),
# Factions before this point are hardwired into the game end their order should not be changed.

  ("neutral","Neutral",0, 0.1,[("player_faction",0.0)], [],0xFFFFFF),
  ("innocents","Innocents", ff_always_hide_label, 0.5,[("outlaws",-0.05)], []),
  ("merchants","Merchants", ff_always_hide_label, 0.5,[("outlaws",-0.5),], []),

  ("dark_knights","{!}Dark Knights", 0, 0.5,[("innocents",-0.9),("player_faction",-0.4)], []),

  ("culture_1",  "{!}culture_1", 0, 0.9, [], []),
  ("culture_2",  "{!}culture_2", 0, 0.9, [], []),
  ("culture_3",  "{!}culture_3", 0, 0.9, [], []),
  ("culture_4",  "{!}culture_4", 0, 0.9, [], []),
  ("culture_5",  "{!}culture_5", 0, 0.9, [], []),
  ("culture_6",  "{!}culture_6", 0, 0.9, [], []),
("culture_7",  "{!}culture_7", 0, 0.9, [], []),
("culture_8",  "{!}culture_8", 0, 0.9, [], []),
("culture_9",  "{!}culture_9", 0, 0.9, [], []),
("culture_10",  "{!}culture_10", 0, 0.9, [], []),
("culture_11",  "{!}culture_11", 0, 0.9, [], []),
("culture_12",  "{!}culture_12", 0, 0.9, [], []),
("culture_13",  "{!}culture_13", 0, 0.9, [], []),
("culture_14",  "{!}culture_14", 0, 0.9, [], []),
("culture_15",  "{!}culture_15", 0, 0.9, [], []),
("culture_16",  "{!}culture_16", 0, 0.9, [], []),
("culture_17",  "{!}culture_17", 0, 0.9, [], []),
("culture_18",  "{!}culture_18", 0, 0.9, [], []),
("culture_19",  "{!}culture_19", 0, 0.9, [], []),
("culture_20",  "{!}culture_20", 0, 0.9, [], []),
("culture_21",  "{!}culture_21", 0, 0.9, [], []),
("culture_22",  "{!}culture_22", 0, 0.9, [], []),
("culture_23",  "{!}culture_23", 0, 0.9, [], []),
("culture_24",  "{!}culture_24", 0, 0.9, [], []),
("culture_25",  "{!}culture_25", 0, 0.9, [], []),
("culture_26",  "{!}culture_26", 0, 0.9, [], []),
("culture_27",  "{!}culture_27", 0, 0.9, [], []),
("culture_28",  "{!}culture_28", 0, 0.9, [], []),
("culture_29",  "{!}culture_29", 0, 0.9, [], []),
("culture_30",  "{!}culture_30", 0, 0.9, [], []),
("culture_31",  "{!}culture_31", 0, 0.9, [], []),
("culture_32",  "{!}culture_32", 0, 0.9, [], []),
("culture_33",  "{!}culture_33", 0, 0.9, [], []),

## ZZ culture_player 
  ("culture_player",  "{!}culture_7", 0, 0.9, [], []),
## ZZ culture_player
#  ("swadian_caravans","Swadian Caravans", 0, 0.5,[("outlaws",-0.8), ("dark_knights",-0.2)], []),#,("kingdom_1",0.1),("kingdom_3",0.1),("kingdom_4",0.1),("kingdom_5",0.1),("kingdom_8",0.1),("kingdom_9",0.1),("kingdom_14",0.1),("kingdom_12",0.1),("kingdom_13",0.1)
#  ("vaegir_caravans","Vaegir Caravans", 0, 0.5,[("outlaws",-0.8), ("dark_knights",-0.2)], []),

  ("player_faction","Player Faction",0, 0.9, [], []),
  ("player_supporters_faction","Player's Supporters",0, 0.9, [("player_faction",1.00),("outlaws",-0.05),("peasant_rebels", -0.1),("deserters", -0.02),("mountain_bandits", -0.05),("forest_bandits", 0)], [], 0xFF4433), #changed name so that can tell difference if shows up on map
  ("kingdom_1",  "French_Empire", 0, 0.9, [("outlaws",-0.05),("kingdom_16", -0.02),("peasant_rebels", -0.1),("kingdom_7",0.1),("kingdom_10",0.1),("kingdom_11",0.1),("kingdom_8",-0.4),("deserters", -0.02),("mountain_bandits", -0.05),("forest_bandits", 0.05)], [], 23805),
  ("kingdom_2",  "Russian_Empire",    0, 0.9, [("outlaws",-0.05),("kingdom_13",-0.4),("kingdom_27",-0.1),("kingdom_7",0.1),("kingdom_11",0.1),("peasant_rebels", -0.1),("deserters", -0.02),("mountain_bandits", -0.05),("forest_bandits", 0)], [], 29440),
  ("kingdom_3",  "Austrian_Empire", 0, 0.9, [("kingdom_5",-0.4),("outlaws",-0.05),("kingdom_6",-0.4),("peasant_rebels", -0.1),("kingdom_7",0.1),("kingdom_10",0.1),("kingdom_11",0.1),("deserters", -0.02),("mountain_bandits", -0.05),("forest_bandits", 0)], [], 15724020),#0xFFAAAAAA #30303
  ("kingdom_4",  "Kingdom_of_Sardinia",    0, 0.9, [("outlaws",-0.05),("peasant_rebels", -0.1),("kingdom_6",-0.4),("deserters", -0.02),("kingdom_7",0.1),("kingdom_10",0.1),("kingdom_11",0.1),("mountain_bandits", -0.05),("forest_bandits", 0)], [], 39198),
  ("kingdom_5",  "Kingdom_of_Prussia",  0, 0.9, [("kingdom_3",-0.4),("outlaws",-0.05),("peasant_rebels", -0.1),("deserters", -0.02),("kingdom_7",0.1),("kingdom_10",0.1),("kingdom_11",0.1),("mountain_bandits", -0.05),("forest_bandits", 0)], [], 5065283),
  ("kingdom_6",  "Ottoman_Empire",  0, 0.9, [("outlaws",-0.05),("kingdom_28",-0.2),("kingdom_23",-0.2),("peasant_rebels", -0.1),("kingdom_3",-0.4),("kingdom_7",0.1),("kingdom_11",0.1),("kingdom_4",-0.4),("kingdom_12",-0.4),("deserters", -0.02),("mountain_bandits", -0.05),("forest_bandits", -0.05)], [], 8781824),
("kingdom_7",  "British_Empire", 0, 0.9, [("outlaws",-0.05),("peasant_rebels", -0.1),("kingdom_11",-0.6),("kingdom_1",0.1),("kingdom_3",0.1),("kingdom_19",0.2),("kingdom_20",0.2),("kingdom_4",0.1),("kingdom_5",0.1),("kingdom_8",0.1),("kingdom_9",0.1),("kingdom_14",0.1),("kingdom_13",0.1),("kingdom_10",-0.5),("deserters", -0.02),("mountain_bandits", -0.05),("forest_bandits", 0)], [], 13636204),#0xFF6AAA89 #0x931124
("kingdom_8",  "Kingdom_of_Netherlands", 0, 0.9, [("outlaws",-0.05),("kingdom_24",-0.1),("peasant_rebels", -0.1),("deserters", -0.02),("kingdom_7",0.1),("kingdom_10",0.1),("kingdom_11",0.1),("kingdom_1",-0.4),("mountain_bandits", -0.05),("forest_bandits", -0.45)], [], 15961892),
("kingdom_9",  "Spanish_Empire", 0, 0.9, [("kingdom_25",-0.2),("outlaws",-0.05),("kingdom_16",0.2),("peasant_rebels", -0.1),("deserters", -0.02),("kingdom_7",0.1),("kingdom_10",0.1),("kingdom_11",0.1),("kingdom_14",-0.2),("kingdom_15",-0.2),("mountain_bandits", -0.05),("forest_bandits", 0)], [], 6959360),
("kingdom_10",  "Emirate_of_Tunisia", 0, 0.9, [("outlaws",-0.05),("kingdom_20",-0.2),("kingdom_1",0.1),("kingdom_3",0.1),("kingdom_4",0.1),("kingdom_5",0.1),("kingdom_8",0.1),("kingdom_9",0.1),("kingdom_14",0.1),("kingdom_13",0.1),("kingdom_1",0.1),("kingdom_3",0.1),("kingdom_4",0.1),("kingdom_5",0.1),("kingdom_8",0.1),("kingdom_9",0.1),("kingdom_14",0.1),("kingdom_12",0.1),("kingdom_13",0.1),("peasant_rebels", -0.1),("deserters", -0.02),("kingdom_7",-0.5),("mountain_bandits", -0.05),("forest_bandits", -0.05)], [], 13611157),
("kingdom_11",  "Kingdom_of_Two_Sicilies", 0, 0.9, [("outlaws",-0.05),("kingdom_19",-0.2),("kingdom_1",0.1),("kingdom_3",0.1),("kingdom_4",0.1),("kingdom_5",0.1),("kingdom_8",0.1),("kingdom_9",0.1),("kingdom_14",0.1),("kingdom_12",0.1),("kingdom_13",0.1),("peasant_rebels", -0.1),("deserters", -0.02),("kingdom_7",-0.6),("mountain_bandits", -0.05)], [], 8852121),
("kingdom_12",  "Shahdom_of_Persia", 0, 0.9, [("outlaws",-0.05),("kingdom_21", -0.02),("peasant_rebels", -0.1),("deserters", -0.02),("kingdom_7",0.1),("kingdom_10",0.1),("kingdom_6",-0.2),("mountain_bandits", -0.05),("forest_bandits", 0)], [], 3640261),
("kingdom_13",  "Switzerland", 0, 0.9, [("outlaws",-0.05),("kingdom_22",-0.2),("kingdom_2",-0.4),("peasant_rebels", -0.1),("deserters", -0.02),("kingdom_7",0.1),("kingdom_10",0.1),("kingdom_11",0.1),("mountain_bandits", -0.05),("forest_bandits", 0)], [], 12058624),
("kingdom_14",  "Khadivate_of_Egypt", 0, 0.9, [("outlaws",-0.05),("kingdom_29", -0.02),("peasant_rebels", -0.1),("deserters", -0.02),("kingdom_7",0.1),("kingdom_10",0.1),("kingdom_11",0.1),("mountain_bandits", -0.05),("kingdom_9",-0.2),("forest_bandits", 0)], [], 13796892),
("kingdom_15",  "Sultanate_of_Morocco", 0, 0.9, [("outlaws",-0.05),("peasant_rebels", -0.1),("deserters", -0.02),("kingdom_7",0.1),("kingdom_10",0.1),("kingdom_11",0.1),("mountain_bandits", -0.05),("kingdom_9",-0.2),("forest_bandits", 0)], [], 12058787),#15
("kingdom_16",  "Kingdom_of_Portugal", 0, 0.9, [("outlaws",-0.05),("kingdom_9",0.2),("peasant_rebels", -0.1),("deserters", -0.02),("kingdom_1",-0.2),("kingdom_10",0.1),("kingdom_11",0.1),("mountain_bandits", -0.05),("kingdom_14",-0.2),("forest_bandits", 0)], [], 0x0000CD),
("kingdom_17",  "Sultanate_of_Oman", 0, 0.9, [("outlaws",-0.05),("peasant_rebels", -0.1),("deserters", -0.02),("kingdom_7",0.1),("kingdom_10",0.1),("kingdom_11",0.1),("mountain_bandits", -0.05),("kingdom_18",-0.2),("forest_bandits", 0)], [], 7264768),
("kingdom_18",  "Kingdom_of_Denmark", 0, 0.9, [("outlaws",-0.05),("peasant_rebels", -0.1),("deserters", -0.02),("kingdom_7",0.1),("kingdom_10",0.1),("kingdom_11",0.1),("mountain_bandits", -0.05),("kingdom_17",-0.2),("forest_bandits", 0)], [], 15682423),
("kingdom_19",  "Papal_States", 0, 0.9, [("outlaws",-0.05),("kingdom_7",0.2),("peasant_rebels", -0.1),("deserters", -0.02),("kingdom_7",0.1),("kingdom_10",0.1),("kingdom_11",-0.2),("mountain_bandits", -0.05),("kingdom_14",0.1),("forest_bandits", 0)], [], 16233991),
("kingdom_20",  "British_Colonies", 0, 0.9, [("outlaws",-0.05),("kingdom_7",0.2),("peasant_rebels", -0.1),("deserters", -0.02),("kingdom_7",0.1),("kingdom_10",0.1),("kingdom_11",0.1),("mountain_bandits", -0.05),("kingdom_10",-0.2),("forest_bandits", 0)], [], 13636204),
("kingdom_21",  "Emirate_of_Afghanistan", 0, 0.9, [("outlaws",-0.05),("peasant_rebels", -0.1),("deserters", -0.02),("kingdom_7",0.1),("kingdom_10",0.1),("kingdom_11",0.1),("mountain_bandits", -0.05),("kingdom_12",-0.2),("forest_bandits", 0)], [], 3352843),
("kingdom_22",  "Emirate_of_Bukhara", 0, 0.9, [("outlaws",-0.05),("peasant_rebels", -0.1),("deserters", -0.02),("kingdom_7",0.1),("kingdom_10",0.1),("kingdom_11",0.1),("mountain_bandits", -0.05),("kingdom_13",-0.2),("forest_bandits", 0)], [], 15178273),
("kingdom_23",  "Khanate_of_Khiva", 0, 0.9, [("outlaws",-0.05),("peasant_rebels", -0.1),("deserters", -0.02),("kingdom_7",0.1),("kingdom_10",0.1),("kingdom_11",0.1),("mountain_bandits", -0.05),("kingdom_14",0.2),("kingdom_6",-0.2),("forest_bandits", 0)], [], 8886135),
("kingdom_24",  "Kingdom_of_Greece", 0, 0.9, [("outlaws",-0.05),("peasant_rebels", -0.1),("deserters", -0.02),("kingdom_7",0.1),("kingdom_10",0.1),("kingdom_8",-0.1),("kingdom_11",0.1),("mountain_bandits", -0.05),("kingdom_1",0.2),("forest_bandits", 0)], [], 308981),
("kingdom_25",  "Principate_of_Wallachia_and_Moldavia", 0, 0.9, [("outlaws",-0.05),("peasant_rebels", -0.1),("deserters", -0.02),("kingdom_7",0.1),("kingdom_10",0.1),("kingdom_11",0.1),("mountain_bandits", -0.05),("kingdom_26",-0.2),("kingdom_15",-0.2),("kingdom_9",-0.2),("forest_bandits", 0)], [], 8342049),
("kingdom_26",  "Kingdom_of_Belgium", 0, 0.9, [("outlaws",-0.05),("peasant_rebels", -0.1),("deserters", -0.02),("kingdom_7",0.1),("kingdom_10",0.1),("kingdom_11",0.1),("mountain_bandits", -0.05),("kingdom_25",-0.2),("forest_bandits", 0)], [], 13465578),
("kingdom_27",  "Kingdom_of_Wurttemberg", 0, 0.9, [("outlaws",-0.05),("kingdom_2",-0.1),("peasant_rebels", -0.1),("deserters", -0.02),("kingdom_7",0.1),("kingdom_10",0.1),("kingdom_11",0.1),("mountain_bandits", -0.05),("kingdom_3",0.2),("forest_bandits", 0)], [], 14522962),
("kingdom_28",  "Principality of Serbia", 0, 0.9, [("outlaws",-0.05),("peasant_rebels", -0.1),("deserters", -0.02),("kingdom_7",0.1),("kingdom_10",0.1),("kingdom_11",0.1),("mountain_bandits", -0.05),("kingdom_4",0.2),("kingdom_6",-0.2),("forest_bandits", 0)], [], 23805),##0xFFAAAAAA
("kingdom_29",  "Kingdom_of_Sweden", 0, 0.9, [("outlaws",-0.05),("kingdom_14", -0.02),("peasant_rebels", -0.1),("deserters", -0.02),("kingdom_11",0.1),("kingdom_4",0.2),("forest_bandits", 0)], [], 6658814),##0xFFAAAAAA
("kingdom_30",  "Kingdom_of_Bavaria", 0, 0.9, [("outlaws",-0.05),("peasant_rebels", -0.1),("deserters", -0.02),("kingdom_11",0.1),("forest_bandits", 0)], [], 308981),##0xFFAAAAAA
("kingdom_31",  "Kingdom_of_Hannover", 0, 0.9, [("outlaws",-0.05),("peasant_rebels", -0.1),("deserters", -0.02),("kingdom_11",0.1),("forest_bandits", 0)], [], 8505753),##0xFFAAAAAA
("kingdom_32",  "Emirate_of_Shammar", 0, 0.9, [("outlaws",-0.05),("peasant_rebels", -0.1),("deserters", -0.02),("kingdom_11",0.1),("forest_bandits", 0)], [], 8342049),##0xFFAAAAAA
("kingdom_33",  "Emirate_of_Najd", 0, 0.9, [("outlaws",-0.05),("peasant_rebels", -0.1),("deserters", -0.02),("kingdom_11",0.1),("forest_bandits", 0)], [], 1863680),##0xFFAAAAAA

  ("kingdoms_end","{!}kingdoms_end", 0, 0,[], []),

  ("robber_knights",  "{!}robber_knights", 0, 0.1, [], []),

  ("khergits","{!}Khergits", 0, 0.5,[("player_faction",0.0)], []),
  ("black_khergits","{!}Black Khergits", 0, 0.5,[("player_faction",-0.3),("kingdom_1",-0.02),("kingdom_2",-0.02)], []),

##  ("rebel_peasants","Rebel Peasants", 0, 0.5,[("vaegirs",-0.5),("player_faction",0.0)], []),

  ("manhunters","Manhunters", 0, 0.5,[("outlaws",-0.6),("player_faction",0.1)], []),
  ("deserters","Deserters", 0, 0.5,[("manhunters",-0.6),("merchants",-0.5),("player_faction",-0.1)], [], 0x888888),
  ("mountain_bandits","Mountain Bandits", 0, 0.5,[("commoners",-0.2),("merchants",-0.5),("manhunters",-0.6),("player_faction",-0.15)], [], 0x888888),
  ("forest_bandits","Forest Bandits", 0, 0.5,[("commoners",-0.2),("merchants",-0.5),("manhunters",-0.6),("player_faction",-0.15)], [], 0x888888),

  ("undeads","{!}Undeads", max_player_rating(-30), 0.5,[("commoners",-0.7),("player_faction",-0.5)], []),
  ("slavers","{!}Slavers", 0, 0.1, [], []),
  ("peasant_rebels","{!}Peasant Rebels", 0, 1.0,[("noble_refugees",-1.0),("player_faction",-0.4)], []),
  ("noble_refugees","{!}Noble Refugees", 0, 0.5,[], []),
#INVASION MODE START
  ("ccoop_all_stars","All Stars", 0, 0.5,[], []),
#INVASION MODE END
]
