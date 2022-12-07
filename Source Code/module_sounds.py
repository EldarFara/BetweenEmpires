from header_sounds import *

# #######################################################################
#	("sound_id", sound_flags, [sound-file]),
#
#	There was never a header to this file.
#		Weird.
#
#	Essentially it's:
#	Field 1: Sound ID (string)
#	Field 2: Flags (string|string), see header_sounds
#	Field 3: Sound file (string, or list of strings), 
#			 seems like it could be .ogg, .mp3, or .wav
# #######################################################################

# #######################################################################
#	I also took the time to categorize these sounds, It seems like so
#	long as you leave in the ones called by engine events you're good
# #######################################################################


sounds = [
 # UI/UX Sounds, THE ACTUAL HARDCODED SOUNDS ############################
 ("click", sf_2d|sf_vol_1,["drum_3.ogg"]),
 ("gong", sf_2d|sf_priority_9|sf_vol_7, ["s_cymbals.ogg"]),
 ("quest_taken", sf_2d|sf_priority_9|sf_vol_7, []),
 ("quest_completed", sf_2d|sf_priority_9|sf_vol_7, ["quest_completed.ogg"]),
 ("quest_succeeded", sf_2d|sf_priority_9|sf_vol_7, ["quest_succeeded.ogg"]),
 ("quest_concluded", sf_2d|sf_priority_9|sf_vol_7, ["quest_concluded.ogg"]),
 ("quest_failed", sf_2d|sf_priority_9|sf_vol_7, ["quest_failed.ogg"]),
 ("quest_cancelled", sf_2d|sf_priority_9|sf_vol_7, ["quest_cancelled.ogg"]),
 ("hide", 0, ["s_hide.wav"]),
 ("unhide", 0, ["s_unhide.wav"]),
 
 # #######################################################################
 # 	From here everything ~could~ probably be deleted. I just don't know 
 #	enough about how the engine handles what sound is played when, so I
 #	left these as they seem like they might accidentally be called.
 # #######################################################################
 
 # More UI/UX Sounds
 ("money_received", sf_2d|sf_priority_10|sf_vol_6, ["coins_dropped_1.ogg"]),
 ("money_paid", sf_2d|sf_priority_10|sf_vol_10, ["coins_dropped_2.ogg"]),
 
 # Party Sounds
 ("gallop", sf_vol_3, ["horse_gallop_3.ogg","horse_gallop_4.ogg","horse_gallop_5.ogg"]),
 ("battle", sf_vol_4, ["battle.ogg"]),

 # Combat Sounds
 # # Attacking Sounds 
 ("sword_clash_1", 0, ["sword_clank_metal_09.ogg","sword_clank_metal_09b.ogg","sword_clank_metal_10.ogg","sword_clank_metal_10b.ogg","sword_clank_metal_12.ogg","sword_clank_metal_12b.ogg","sword_clank_metal_13.ogg","sword_clank_metal_13b.ogg"]),
 ("sword_clash_2", 0, ["s_swordClash2.wav"]),
 ("sword_clash_3", 0, ["s_swordClash3.wav"]),
 ("sword_swing", sf_vol_8|sf_priority_2, ["s_swordSwing.wav"]),
  # # Equipping/Unequipping Sounds
 ("draw_sword", sf_priority_4, ["draw_sword.ogg"]),
 ("put_back_sword", sf_priority_4, ["put_back_sword.ogg"]),
 ("draw_greatsword", sf_priority_4, ["draw_greatsword.ogg"]),
 ("put_back_greatsword", sf_priority_4, ["put_back_sword.ogg"]),
 ("draw_axe", sf_priority_4, ["draw_mace.ogg"]),
 ("put_back_axe", sf_priority_4, ["put_back_to_holster.ogg"]),
 ("draw_greataxe", sf_priority_4, ["draw_greataxe.ogg"]),
 ("put_back_greataxe", sf_priority_4, ["put_back_to_leather.ogg"]),
 ("draw_spear", sf_priority_4, ["draw_spear.ogg"]),
 ("put_back_spear", sf_priority_4, ["put_back_to_leather.ogg"]),
 ("draw_crossbow", sf_priority_4, ["draw_crossbow.ogg"]),
 ("put_back_crossbow", sf_priority_4, ["put_back_to_leather.ogg"]),
 ("draw_revolver", sf_priority_4, ["draw_from_holster.ogg"]),
 ("put_back_revolver", sf_priority_4, ["put_back_to_holster.ogg"]),
 ("draw_dagger", sf_priority_4, ["draw_dagger.ogg"]),
 ("put_back_dagger", sf_priority_4, ["put_back_dagger.ogg"]),
 ("draw_bow", sf_priority_4, ["draw_bow.ogg"]),
 ("put_back_bow", sf_priority_4, ["put_back_to_holster.ogg"]),
 ("draw_shield", sf_priority_4|sf_vol_7, ["draw_shield.ogg"]),
 ("put_back_shield", sf_priority_4|sf_vol_7, ["put_back_shield.ogg"]),
 ("draw_other", sf_priority_4, ["draw_other.ogg"]),
 ("put_back_other", sf_priority_4, ["draw_other2.ogg"]),
 # # Melee Striking Sounds
 # # # Block/Whiff Sounds
 ("hit_wood_wood", sf_priority_7|sf_vol_10, ["hit_wood_wood_1.ogg","hit_wood_wood_2.ogg","hit_wood_wood_3.ogg","hit_wood_wood_4.ogg","hit_wood_metal_4.ogg","hit_wood_metal_5.ogg","hit_wood_metal_6.ogg"]),
 ("hit_metal_metal", sf_priority_7|sf_vol_10, ["hit_metal_metal_3.ogg","hit_metal_metal_4.ogg",
                                              "hit_metal_metal_5.ogg","hit_metal_metal_6.ogg","hit_metal_metal_7.ogg","hit_metal_metal_8.ogg",
                                              "hit_metal_metal_9.ogg","hit_metal_metal_10.ogg",
                                              "clang_metal_1.ogg","clang_metal_2.ogg"]),
 ("hit_wood_metal", sf_priority_7|sf_vol_10, ["hit_metal_metal_1.ogg","hit_metal_metal_2.ogg","hit_wood_metal_7.ogg"]),
 ("block_fist", 0, ["block_fist_3.ogg","block_fist_4.ogg"]),
 # # # Hitting Armored Opponent Sounds
 ("metal_hit_low_armor_low_damage", sf_priority_5|sf_vol_9, ["sword_hit_lo_armor_lo_dmg_1.ogg","sword_hit_lo_armor_lo_dmg_2.ogg","sword_hit_lo_armor_lo_dmg_3.ogg"]),
 ("metal_hit_low_armor_high_damage", sf_priority_5|sf_vol_9, ["sword_hit_lo_armor_hi_dmg_1.ogg","sword_hit_lo_armor_hi_dmg_2.ogg","sword_hit_lo_armor_hi_dmg_3.ogg"]),
 ("metal_hit_high_armor_low_damage", sf_priority_5|sf_vol_9, ["metal_hit_high_armor_low_damage.ogg","metal_hit_high_armor_low_damage_2.ogg","metal_hit_high_armor_low_damage_3.ogg"]),
 ("metal_hit_high_armor_high_damage", sf_priority_5|sf_vol_9, ["sword_hit_hi_armor_hi_dmg_1.ogg","sword_hit_hi_armor_hi_dmg_2.ogg","sword_hit_hi_armor_hi_dmg_3.ogg"]),
 ("wooden_hit_low_armor_low_damage", sf_priority_5|sf_vol_9, ["blunt_hit_low_1.ogg","blunt_hit_low_2.ogg","blunt_hit_low_3.ogg"]),
 ("wooden_hit_low_armor_high_damage", sf_priority_5|sf_vol_9, ["blunt_hit_high_1.ogg","blunt_hit_high_2.ogg","blunt_hit_high_3.ogg"]),
 ("wooden_hit_high_armor_low_damage", sf_priority_5|sf_vol_9, ["wooden_hit_high_armor_low_damage.ogg","wooden_hit_high_armor_low_damage_2.ogg"]),
 ("wooden_hit_high_armor_high_damage", sf_priority_5|sf_vol_9, ["blunt_hit_high_1.ogg","blunt_hit_high_2.ogg","blunt_hit_high_3.ogg"]),
 # # # Hitting Unarmored Opponent Sounds
 ("man_hit_blunt_weak", sf_priority_5|sf_vol_10, ["man_hit_13.ogg","man_hit_29.ogg","man_hit_32.ogg","man_hit_47.ogg","man_hit_57.ogg"]),
 ("man_hit_blunt_strong", sf_priority_5|sf_vol_10, ["man_hit_13.ogg","man_hit_29.ogg","man_hit_32.ogg","man_hit_47.ogg","man_hit_57.ogg"]),
 ("man_hit_pierce_weak", sf_priority_5|sf_vol_10, ["man_hit_13.ogg","man_hit_29.ogg","man_hit_32.ogg","man_hit_47.ogg","man_hit_57.ogg"]),
 ("man_hit_pierce_strong", sf_priority_5|sf_vol_10, ["man_hit_13.ogg","man_hit_29.ogg","man_hit_32.ogg","man_hit_47.ogg","man_hit_57.ogg"]),
 ("man_hit_cut_weak", sf_priority_5|sf_vol_10, ["man_hit_13.ogg","man_hit_29.ogg","man_hit_32.ogg","man_hit_47.ogg","man_hit_57.ogg"]),
 ("man_hit_cut_strong", sf_priority_5|sf_vol_10, ["man_hit_13.ogg","man_hit_29.ogg","man_hit_32.ogg","man_hit_47.ogg","man_hit_57.ogg"]),
 ("blunt_hit", sf_priority_5|sf_vol_9, ["punch_1.ogg","punch_4.ogg","punch_4.ogg","punch_5.ogg"]),
 # # Shield Sounds
 ("shield_hit_wood_wood", sf_priority_7|sf_vol_10, ["shield_hit_wood_wood_1.ogg","shield_hit_wood_wood_2.ogg","shield_hit_wood_wood_3.ogg"]),
 ("shield_hit_metal_metal", sf_priority_7|sf_vol_10, ["shield_hit_metal_metal_1.ogg","shield_hit_metal_metal_2.ogg","shield_hit_metal_metal_3.ogg","shield_hit_metal_metal_4.ogg"]),
 ("shield_hit_wood_metal", sf_priority_7|sf_vol_10, ["shield_hit_cut_3.ogg","shield_hit_cut_4.ogg","shield_hit_cut_5.ogg","shield_hit_cut_10.ogg"]),
 ("shield_hit_metal_wood", sf_priority_7|sf_vol_10, ["shield_hit_metal_wood_1.ogg","shield_hit_metal_wood_2.ogg","shield_hit_metal_wood_3.ogg"]),
 ("shield_broken", sf_priority_9, ["shield_broken.ogg"]),
 
 # # Biped Movement Sounds
 ("footstep_grass", sf_vol_4|sf_priority_1,["footstep_1.ogg","footstep_2.ogg","footstep_3.ogg","footstep_4.ogg"]),
 ("footstep_wood", sf_vol_6|sf_priority_1,["footstep_wood_1.ogg","footstep_wood_2.ogg","footstep_wood_4.ogg"]),
 ("footstep_water", sf_vol_4|sf_priority_3,["water_walk_1.ogg","water_walk_2.ogg","water_walk_3.ogg","water_walk_4.ogg"]),
 # # # Biped Jump
 ("jump_begin", sf_vol_7|sf_priority_9,["jump_begin.ogg"]),
 ("jump_end", sf_vol_5|sf_priority_9,["jump_end.ogg"]),
 ("jump_begin_water", sf_vol_4|sf_priority_9,["jump_begin_water.ogg"]),
 ("jump_end_water", sf_vol_4|sf_priority_9,["jump_end_water.ogg"]),
 # # Horse Movement Sounds
 ("horse_walk", sf_priority_3|sf_vol_12, ["horse_walk_1.ogg","horse_walk_2.ogg","horse_walk_3.ogg","horse_walk_4.ogg"]),
 ("horse_trot", sf_priority_3|sf_vol_13, ["horse_trot_1.ogg","horse_trot_2.ogg","horse_trot_3.ogg","horse_trot_4.ogg"]),
 ("horse_canter", sf_priority_3|sf_vol_14, ["horse_canter_1.ogg","horse_canter_2.ogg","horse_canter_3.ogg","horse_canter_4.ogg"]),
 ("horse_gallop", sf_priority_3|sf_vol_15, ["horse_gallop_6.ogg","horse_gallop_7.ogg","horse_gallop_8.ogg","horse_gallop_9.ogg"]), 
 ("footstep_horse", sf_priority_3|sf_vol_15, ["footstep_horse_5.ogg","footstep_horse_2.ogg","footstep_horse_3.ogg","footstep_horse_4.ogg"]),
 ("footstep_horse_1b", sf_priority_3|sf_vol_15, ["s_footstep_horse_4b.wav","s_footstep_horse_4f.wav","s_footstep_horse_5b.wav","s_footstep_horse_5f.wav"]),
 ("footstep_horse_1f", sf_priority_3|sf_vol_15, ["s_footstep_horse_2b.wav","s_footstep_horse_2f.wav","s_footstep_horse_3b.wav","s_footstep_horse_3f.wav"]),
 ("footstep_horse_2b", sf_priority_3|sf_vol_15, ["s_footstep_horse_2b.wav"]),
 ("footstep_horse_2f", sf_priority_3|sf_vol_15, ["s_footstep_horse_2f.wav"]),
 ("footstep_horse_3b", sf_priority_3|sf_vol_15, ["s_footstep_horse_3b.wav"]),
 ("footstep_horse_3f", sf_priority_3|sf_vol_15, ["s_footstep_horse_3f.wav"]),
 ("footstep_horse_4b", sf_priority_3|sf_vol_15, ["s_footstep_horse_4b.wav"]),
 ("footstep_horse_4f", sf_priority_3|sf_vol_15, ["s_footstep_horse_4f.wav"]),
 ("footstep_horse_5b", sf_priority_3|sf_vol_15, ["s_footstep_horse_5b.wav"]),
 ("footstep_horse_5f", sf_priority_3|sf_vol_15, ["s_footstep_horse_5f.wav"]),
 # # # Horse Jump 
 ("horse_jump_begin", sf_vol_12|sf_priority_9,["horse_jump_begin.ogg"]),
 ("horse_jump_end", sf_vol_12|sf_priority_9,["horse_jump_end.ogg"]),
 ("horse_jump_begin_water", sf_vol_6|sf_priority_9,["jump_begin_water.ogg"]),
 ("horse_jump_end_water", sf_vol_6|sf_priority_9,["jump_end_water.ogg"]),
 # Ranged Attacking Sounds
 # # Readying
 ("reload_crossbow", sf_vol_3, []),
 ("reload_crossbow_continue", sf_vol_6, []),
 ("pull_bow", sf_vol_4, []),
 ("pull_arrow", sf_vol_5, []),
 # # Shooting
 ("release_bow", sf_vol_5, []),
 ("release_crossbow", sf_vol_7, []),
 ("release_crossbow_medium", sf_vol_5, []),
 ("release_crossbow_far", sf_vol_2, []),
 ("throw_javelin", sf_vol_5, ["throw_javelin_2.ogg"]),
 ("throw_axe", sf_vol_7, ["throw_axe_1.ogg"]),
 ("throw_knife", sf_vol_5, ["throw_knife_1.ogg"]),
 ("throw_stone", sf_vol_7, ["throw_stone_1.ogg"]),
 ("pistol_shot", sf_priority_10|sf_vol_10, ["fl_pistol.wav"]),
 # # Struck
 ("bullet_hit_body", sf_priority_4, ["arrow_hit_body_1.ogg","arrow_hit_body_2.ogg","arrow_hit_body_3.ogg"]), 
 ("player_hit_by_bullet", sf_priority_10|sf_vol_10, ["player_hit_by_arrow.ogg"]),
 ("arrow_hit_body", sf_priority_4, ["arrow_hit_body_1.ogg","arrow_hit_body_2.ogg","arrow_hit_body_3.ogg"]),
 ("player_hit_by_arrow", sf_priority_10|sf_vol_10, ["player_hit_by_arrow.ogg"]),
 ("mp_arrow_hit_target", sf_2d|sf_priority_10|sf_vol_9, ["mp_arrow_hit_target.ogg"]),
 # # Fly Past
 ("arrow_pass_by", 0, ["arrow_pass_by_1.ogg","arrow_pass_by_2.ogg","arrow_pass_by_3.ogg","arrow_pass_by_4.ogg"]),
 ("bolt_pass_by", 0, ["bolt_pass_by_1.ogg"]),
 ("javelin_pass_by", 0, ["javelin_pass_by_1.ogg","javelin_pass_by_2.ogg"]),
 ("stone_pass_by", sf_vol_9, ["stone_pass_by_1.ogg"]),
 ("axe_pass_by", 0, ["axe_pass_by_1.ogg"]),
 ("knife_pass_by", 0, ["knife_pass_by_1.ogg"]),
 ("bullet_pass_by", 0, ["arrow_whoosh_1.ogg"]),
 # # Hit Ground, Aimed Towards Player
 ("incoming_arrow_hit_ground", sf_priority_7|sf_vol_7, ["arrow_hit_ground_2.ogg","arrow_hit_ground_3.ogg","incoming_bullet_hit_ground_1.ogg"]),
 ("incoming_bolt_hit_ground", sf_priority_7|sf_vol_7, ["arrow_hit_ground_2.ogg","arrow_hit_ground_3.ogg","incoming_bullet_hit_ground_1.ogg"]),
 ("incoming_javelin_hit_ground", sf_priority_7|sf_vol_7, ["incoming_javelin_hit_ground_1.ogg"]),
 ("incoming_stone_hit_ground", sf_priority_7|sf_vol_7, ["incoming_stone_hit_ground_1.ogg"]),
 ("incoming_axe_hit_ground", sf_priority_7|sf_vol_7, ["incoming_javelin_hit_ground_1.ogg"]),
 ("incoming_knife_hit_ground", sf_priority_7|sf_vol_7, ["incoming_stone_hit_ground_1.ogg"]),
 ("incoming_bullet_hit_ground", sf_priority_7|sf_vol_7, ["incoming_bullet_hit_ground_1.ogg"]),
 # # Hit Ground, Aimed Away From Player
 ("outgoing_arrow_hit_ground", sf_priority_7|sf_vol_7, ["outgoing_arrow_hit_ground.ogg"]),
 ("outgoing_bolt_hit_ground", sf_priority_7|sf_vol_7,  ["outgoing_arrow_hit_ground.ogg"]),
 ("outgoing_javelin_hit_ground", sf_priority_7|sf_vol_10, ["outgoing_arrow_hit_ground.ogg"]),
 ("outgoing_stone_hit_ground", sf_priority_7|sf_vol_7, ["incoming_stone_hit_ground_1.ogg"]),
 ("outgoing_axe_hit_ground", sf_priority_7|sf_vol_7, ["incoming_javelin_hit_ground_1.ogg"]),
 ("outgoing_knife_hit_ground", sf_priority_7|sf_vol_7, ["incoming_stone_hit_ground_1.ogg"]),
 ("outgoing_bullet_hit_ground", sf_priority_7|sf_vol_7, ["incoming_bullet_hit_ground_1.ogg"]),


 # Death Sounds
 # # Human
 ("body_fall_small", sf_priority_6|sf_vol_10, ["body_fall_small_1.ogg","body_fall_small_2.ogg"]),
 ("body_fall_big", sf_priority_6|sf_vol_10, ["body_fall_1.ogg","body_fall_2.ogg","body_fall_3.ogg"]),
 # # Horse
 ("horse_body_fall_begin", sf_priority_6|sf_vol_10, ["horse_body_fall_begin_1.ogg"]),
 ("horse_body_fall_end", sf_priority_6|sf_vol_10, ["horse_body_fall_end_1.ogg","body_fall_2.ogg","body_fall_very_big_1.ogg"]),
 
 
 # Vocalizations
 # # Human
 # # # Man
 ("man_grunt", sf_priority_6|sf_vol_4, ["man_excercise_1.ogg","man_excercise_2.ogg","man_excercise_4.ogg"]),
 ("man_breath_hard", sf_priority_3|sf_vol_8, ["man_ugh_1.ogg","man_ugh_2.ogg","man_ugh_4.ogg","man_ugh_7.ogg","man_ugh_12.ogg","man_ugh_13.ogg","man_ugh_17.ogg"]),
 ("man_stun", sf_priority_3|sf_vol_9, ["man_stun_1.ogg"]),
 ("man_grunt_long", sf_priority_5|sf_vol_8, ["man_grunt_1.ogg","man_grunt_2.ogg","man_grunt_3.ogg","man_grunt_5.ogg","man_grunt_13.ogg","man_grunt_14.ogg"]),
 ("man_yell", sf_priority_6|sf_vol_10, ["man_yell_4.ogg","man_yell_4_2.ogg","man_yell_7.ogg","man_yell_9.ogg","man_yell_11.ogg","man_yell_13.ogg","man_yell_15.ogg","man_yell_16.ogg","man_yell_17.ogg","man_yell_20.ogg","man_shortyell_4.ogg","man_shortyell_5.ogg","man_shortyell_6.ogg","man_shortyell_9.ogg","man_shortyell_11.ogg","man_shortyell_11b.ogg",
                        "man_yell_b_18.ogg","man_yell_22.ogg", "man_yell_c_20.ogg"]),

 ("man_warcry", sf_priority_6, ["man_insult_2.ogg","man_insult_3.ogg","man_insult_7.ogg","man_insult_9.ogg","man_insult_13.ogg","man_insult_15.ogg","man_insult_16.ogg"]),
 ("man_victory", sf_priority_5|sf_vol_10, ["man_victory_3.ogg","man_victory_4.ogg","man_victory_5.ogg","man_victory_8.ogg","man_victory_15.ogg","man_victory_49.ogg","man_victory_52.ogg","man_victory_54.ogg","man_victory_57.ogg","man_victory_71.ogg"]),
 ("man_hit", sf_priority_7|sf_vol_10, ["man_hit_5.ogg","man_hit_6.ogg","man_hit_7.ogg","man_hit_8.ogg","man_hit_9.ogg","man_hit_10.ogg","man_hit_11.ogg","man_hit_12.ogg","man_hit_13.ogg","man_hit_14.ogg","man_hit_15.ogg",
                                      "man_hit_17.ogg","man_hit_18.ogg","man_hit_19.ogg","man_hit_22.ogg","man_hit_29.ogg","man_hit_32.ogg","man_hit_47.ogg","man_hit_57.ogg","man_hit_59.ogg"]),
 ("man_die", sf_priority_10,  ["man_death_1.ogg","man_death_8.ogg","man_death_8b.ogg","man_death_11.ogg","man_death_14.ogg","man_death_16.ogg","man_death_18.ogg","man_death_21.ogg","man_death_29.ogg","man_death_40.ogg","man_death_44.ogg","man_death_46.ogg","man_death_48.ogg","man_death_64.ogg"]),
 # # # Woman
 ("woman_hit", sf_priority_7, ["woman_hit_2.ogg","woman_hit_3.ogg",
                              "woman_hit_b_2.ogg","woman_hit_b_4.ogg","woman_hit_b_6.ogg","woman_hit_b_7.ogg","woman_hit_b_8.ogg",
                              "woman_hit_b_11.ogg","woman_hit_b_14.ogg","woman_hit_b_16.ogg"]),
 ("woman_die", sf_priority_10, ["woman_fall_1.ogg","woman_hit_b_5.ogg"]),
 ("woman_yell", sf_priority_10|sf_vol_10, ["woman_yell_1.ogg","woman_yell_2.ogg"]),
 # # Horse
 ("horse_breath", sf_priority_3|sf_priority_9|sf_vol_10, ["horse_breath_4.ogg","horse_breath_5.ogg","horse_breath_6.ogg","horse_breath_7.ogg"]),
 ("horse_snort", sf_priority_5|sf_vol_10, ["horse_snort_1.ogg","horse_snort_2.ogg","horse_snort_3.ogg","horse_snort_4.ogg","horse_snort_5.ogg"]),
 ("horse_low_whinny", sf_vol_12, ["horse_whinny-1.ogg","horse_whinny-2.ogg"]),
 
 # Scene Sounds
 # # Animal Ambience Sounds
 ("neigh", 0, ["horse_exterior_whinny_01.ogg","horse_exterior_whinny_02.ogg","horse_exterior_whinny_03.ogg","horse_exterior_whinny_04.ogg","horse_exterior_whinny_05.ogg","horse_whinny.ogg"]),

 # # City Ambience Sounds

 # # Weather Sounds
 ("rain", sf_2d|sf_priority_10|sf_vol_4|sf_looping, ["rain_1.ogg"]),
 
 # Prop Sounds
 
 # Multiplayer Sounds
 
 
]
