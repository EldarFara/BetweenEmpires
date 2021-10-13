from ID_items import *
from ID_quests import *
from ID_factions import *
from ID_parties import *
##############################################################
# These constants are used in various files.
# If you need to define a value that will be used in those files,
# just define it here rather than copying it across each file, so
# that it will be easy to change it if you need to.
##############################################################

craters_limit = 400

cannon_type_fieldgun = 0
cannon_type_howitzer = 1

pas_points_for_rank_2 = 3000
pas_points_for_rank_3 = 8000
pas_points_for_rank_4 = 16000
pas_points_for_rank_5 = 30000
pas_points_for_rank_6 = 50000
pas_points_for_rank_7 = 70000
pas_points_for_rank_8 = 100000
pas_points_for_rank_9 = 170000
pas_points_for_rank_10 = 300000

pas_lord_state_undefined = 0
pas_lord_state_patrolling_center_peace_border = 1
pas_lord_state_patrolling_center_war_border = 2
pas_lord_state_following_marshall = 3
pas_marshall_state_traveling_to_siege_enemy_center = 4
pas_marshall_state_siege_enemy_center = 5
pas_marshall_state_assault_enemy_center = 6
pas_marshall_state_defend_center = 7
pas_marshall_state_gathering = 8

pas_faction_state_no_campaign = 0
pas_faction_state_campaign = 1

pai_preset_attack_setup_earlygame = 1
pai_preset_attack_setup_lategame = 2

pps_income_tax_rate_divider = 3
pps_import_tax_rate_divider = 6
pps_export_tax_rate_divider = 4
pps_goodsservices_tax_rate_divider = 5

pes_factory_devmode_addworkplaces = 0
pes_factory_devmode_improveconditions = 1
pes_factory_devmode_improvetools = 2
pes_factory_devmode_none = 3

pes_workers_base_number_urban = 7
pes_workers_base_number_rural = 8

pes_resource_menu_faction_flag1 = 1
pes_resource_menu_faction_name1 = 2
pes_resource_menu_faction_supply = 3
pes_resource_menu_faction_demand = 4
pes_resource_menu_faction_quality = 5
pes_resource_menu_faction_gdp = 6
pes_resource_menu_faction_produceramount = 7
pes_resource_menu_faction_population = 8
pes_resource_menu_faction_literacy = 9
pes_resource_menu_faction_urbanization = 10

display_pps_debug_messages = 0
display_pes_debug_messages = 0
display_pas_debug_messages = 1

preset_number_of_factories_britain = 37
preset_number_of_factories_germany = 15
preset_number_of_factories_france = 20
preset_number_of_factories_italy = 7
preset_number_of_factories_russia = 7
preset_number_of_factories_austria = 10
preset_number_of_factories_iberia = 6
preset_number_of_factories_scandinavia = 5
preset_number_of_factories_benelux = 15
preset_number_of_factories_balkans = 4
preset_number_of_factories_switzerland = 1

pes_region_menu_overlay_factory_name = 1
pes_region_menu_overlay_factory_workers_number = 2
pes_region_menu_overlay_factory_photo = 3
pes_region_menu_overlay_factory_budget = 4
pes_region_menu_overlay_factory_card = 5
pes_region_menu_overlay_factory_add = 6
pes_region_menu_overlay_factory_income = 7
pes_region_menu_overlay_factory_spent_and_earnt = 8
pes_region_menu_overlay_factory_product_quality = 9
pes_region_menu_overlay_factory_produced_and_sold = 10
pes_region_menu_overlay_factory_found_raw_resources1 = 11
pes_region_menu_overlay_factory_playershare_slider = 12
pes_region_menu_overlay_factory_playershare_buy = 13
pes_region_menu_overlay_factory_playershare_name = 14
pes_region_menu_overlay_factory_playershare_price = 15
pes_region_menu_variable_factory_playershare_balance_change = 16
pes_region_menu_variable_factory_playershare_selected_amount = 17
pes_region_menu_overlay_factory_clerks_percentage = 18
pes_region_menu_overlay_factory_deterioration = 19
pes_region_menu_overlay_factory_conditions = 20
pes_region_menu_overlay_factory_devmode_title = 21
pes_region_menu_overlay_factory_devmode1 = 22
pes_region_menu_overlay_factory_devmode2 = 23
pes_region_menu_overlay_factory_devmode3 = 24
pes_region_menu_overlay_factory_devmode4 = 25
pes_region_menu_overlay_factory_devmode_selected = 26
pes_region_menu_overlay_factory_worker_wage_title = 27
pes_region_menu_overlay_factory_worker_wage_slider = 28
pes_region_menu_overlay_factory_sell = 29
pes_region_menu_overlay_factory_build_icon = 30
pes_region_menu_variable_factory_build_icon_rotation = 31

mg_limit = 2

language_english = 1
language_russian = 2
language_german = 3
language_turkish = 4
language_spanish = 5
language_italian = 6
language_french = 7
language_polish = 8

vo_type_on_company_select = 1
vo_type_yes_sir = 2
vo_type_gogogo = 3
vo_type_retreat = 4
vo_type_attack = 5
vo_type_fire_at_will = 6
vo_type_keep_shooting = 7
vo_type_hold_ground = 8
vo_type_cease_fire = 9
vo_type_bayonets = 10
vo_type_fire = 11
vo_type_gas = 12
vo_type_gas_attack = 13
vo_type_gas_masks_on = 14

resource_iron = 1
resource_coal = 2
resource_meat = 3
resource_cotton = 4
resource_flour = 5
resource_wood = 6
resource_ammunition = 7
resource_weaponry = 8
resource_military_supplies = 9
resource_fabric = 10
resource_construction_materials = 11
resource_furniture = 12
resource_machine_parts = 13
resource_paper = 14
resource_clothes = 15
resource_timber = 16
resource_steel = 17

ideology_reactionary = 1
ideology_liberal = 2
ideology_socialist = 3

class_upper_aristocracy = 0
class_upper_bourgeoisie = 1
class_middle = 2
class_lower_urban = 3
class_lower_rural = 4

laws_number = 17

law_military_service_term = 0
law_nomination_rules = 1
law_voting_franchise = 2
law_public_meetings = 3
law_press = 4
law_voting_openness = 5
law_executive_branch = 6
law_income_tax = 7
law_goodsservices_tax = 8
law_importexport_tax = 9
law_education_expenses = 10
law_infrastructure_expenses = 11
law_healthcare_expenses = 12
law_workers_conditions = 13
law_workers_wage = 14
law_trade_unions = 15
law_military_expenses = 16

law_military_service_term_short = 0
law_military_service_term_medium = 50
law_military_service_term_long = 100

law_nomination_rules_rich_only = 0
law_nomination_rules_universal = 100

law_voting_franchise_aristocracy_only = 0
law_voting_franchise_rich_only = 100
law_voting_franchise_middle_and_upper_class_only = 125
law_voting_franchise_universal_weighted = 150
law_voting_franchise_universal = 175

law_public_meetings_not_allowed = 0
law_public_meetings_allowed = 100

law_press_state_press = 0
law_press_heavy_censorship = 33
law_press_light_censorship = 66
law_press_free_press = 100

law_voting_openness_harassment = 0
law_voting_openness_non_secret_ballot = 50
law_voting_openness_secret_ballot = 100

law_executive_branch_selected_by_state = 0
law_executive_branch_partially_by_voting = 50
law_executive_branch_mostly_by_voting = 100

law_income_tax_very_small = 10
law_income_tax_small = 35
law_income_tax_medium = 60
law_income_tax_big = 85
law_income_tax_very_big = 110

law_goodsservices_tax_very_small = 10
law_goodsservices_tax_small = 35
law_goodsservices_tax_medium = 60
law_goodsservices_tax_big = 85
law_goodsservices_tax_very_big = 110

law_importexport_tax_very_small = 10
law_importexport_tax_small = 35
law_importexport_tax_medium = 60
law_importexport_tax_big = 85
law_importexport_tax_very_big = 110

law_education_expenses_very_small = 10
law_education_expenses_small = 35
law_education_expenses_medium = 60
law_education_expenses_big = 80
law_education_expenses_very_big = 100

law_infrastructure_expenses_very_small = 10
law_infrastructure_expenses_small = 35
law_infrastructure_expenses_medium = 60
law_infrastructure_expenses_big = 80
law_infrastructure_expenses_very_big = 100

law_healthcare_expenses_very_small = 10
law_healthcare_expenses_small = 35
law_healthcare_expenses_medium = 60
law_healthcare_expenses_big = 80
law_healthcare_expenses_very_big = 100

law_workers_conditions_very_bad = 0
law_workers_conditions_bad = 33
law_workers_conditions_medium = 66
law_workers_conditions_good = 100

law_workers_wage_very_small = 0
law_workers_wage_small = 33
law_workers_wage_medium = 66
law_workers_wage_big = 100

law_trade_unions_not_allowed = 0
law_trade_unions_allowed = 100

law_military_expenses_very_small = 10
law_military_expenses_small = 35
law_military_expenses_medium = 60
law_military_expenses_big = 80
law_military_expenses_very_big = 100

government_type_absolute_monarchy = 1
government_type_constitutional_monarchy = 2
government_type_republic = 3

formation_column = 1
formation_extended_column = 2
formation_dense_line = 3
formation_line = 4
formation_extended_line = 5

shotgun_muzzle_velocity = 5500

default_fog_distance = 1600
rain_fog_distance = 350

ambience_sound_type_nosound = 1
ambience_sound_type_dusk = 2
ambience_sound_type_sunny = 3
ambience_sound_type_dawn = 4
ambience_sound_type_dawnsunset = 5
ambience_sound_type_overcast = 6
ambience_sound_type_desertday = 7
ambience_sound_type_desertnight = 8
ambience_sound_type_night = 9
ambience_sound_type_forestsunny = 10
ambience_sound_type_forestovercast = 11
ambience_sound_type_interior = 12

maximum_amount_of_bandit_parties = 150

battle_type_nobattle			= 0
battle_type_fieldbattle 		= 1
battle_type_siege				= 2
battle_type_bandits_at_night	= 3
battle_type_not_a_battle     	= 4
battle_type_siege_interior 	= 5

army_drill_level_good = 0
army_drill_level_bad = 1

faction_technologies_number = 19
faction_technology_preset_year = faction_technologies_number

cannons_limit = 5
cannons_limit_lategame = 10

howitzer_muzzle_velocity = 85

cannon_loading_type_muzzleloading = 0
cannon_loading_type_breechloading = 1

cannon_he_type_early = 0
cannon_he_type_late  = 1

cannon_projectile_type_cannonball   = 0
cannon_projectile_type_early_shell  = 1
cannon_projectile_type_late_shell   = 2
cannon_projectile_type_gas_shell    = 3

cannon_rifling_type_notrifled = 0
cannon_rifling_type_rifled    = 1

explosion_type_small = 1
explosion_type_medium = 2
explosion_type_big    = 3

YuriCannonCartridgeType_Cannonball = 1
YuriCannonCartridgeType_Grapeshot = 2

YuriCannonMode_Initial = 1
YuriCannonMode_Moving_Initial = 2
YuriCannonMode_Moving_CannoneersWalkingToPositions = 3
YuriCannonMode_Moving_Pulling = 4
YuriCannonMode_Reloading_Initial = 5
YuriCannonMode_Reloading_BarrelCleaning = 6
YuriCannonMode_Reloading_BarrelWetting = 7
YuriCannonMode_Reloading_LoadingCartridge = 8
YuriCannonMode_Reloading_PushingCartridge = 9
YuriCannonMode_Firing_Initial = 10
YuriCannonMode_Firing_Aiming = 11
YuriCannonMode_Firing_PreparingToFire = 12
YuriCannonMode_Firing_Lighting = 13
YuriCannonMode_Firing_Shot = 14
YuriCannonMode_Firing_PreparingToPullBack = 15
YuriCannonMode_Firing_PullingBack = 16
YuriCannonMode_BreechReloading_Initial = 17
YuriCannonMode_BreechReloading_BarrelCleaning = 18
YuriCannonMode_BreechReloading_LoadingCartridge = 19
YuriCannonMode_SiegeDefender_Initial = 20
YuriCannonMode_BreechSiegeDefender_Initial = 21

ImpaledLanceMode_HasImpaledEnemy = 1
ImpaledLanceMode_IsImpaled = 2

ImpaledLanceDamage = 150

YuriCannonMode_InterrruptedReloading_Initial = YuriCannonMode_Reloading_Initial + 100
YuriCannonMode_InterrruptedReloading_LoadCartridge = YuriCannonMode_Reloading_LoadingCartridge + 100
YuriCannonMode_InterrruptedReloading_LoadCartridge_Moving = YuriCannonMode_Reloading_LoadingCartridge + 200
YuriCannonMode_InterrruptedBreechReloading_Initial = YuriCannonMode_BreechReloading_Initial + 100
YuriCannonMode_InterrruptedBreechReloading_LoadingCartridge = YuriCannonMode_BreechReloading_LoadingCartridge + 100
YuriCannonMode_InterrruptedBreechReloading_LoadingCartridge_Moving = YuriCannonMode_BreechReloading_LoadingCartridge + 200

YuriSlotAgent_Cannoneer1 = 35
YuriSlotAgent_Cannoneer2 = 36
YuriSlotAgent_Cannoneer3 = 37
YuriSlotAgent_CannonProp = 38
slot_agent_cannon_prop = YuriSlotAgent_CannonProp
YuriSlotAgent_ImpaledLanceMode = 39
YuriSlotAgent_ImpaledLanceEnemy = 40
YuriSlotAgent_ImpaledLanceTimer = 41

YuriSlotProp_Cannoneer1 = 150
YuriSlotProp_Cannoneer2 = YuriSlotProp_Cannoneer1 + 1
YuriSlotProp_Cannoneer3 = YuriSlotProp_Cannoneer1 + 2
YuriSlotProp_CannoneerOfficer = YuriSlotProp_Cannoneer1 + 3
YuriSlotProp_CannonWheels = YuriSlotProp_Cannoneer1 + 4
YuriSlotProp_CannonBarrel = YuriSlotProp_Cannoneer1 + 5
YuriSlotProp_CannonRope1 = YuriSlotProp_Cannoneer1 + 6
YuriSlotProp_CannonRope2 = YuriSlotProp_Cannoneer1 + 7
YuriSlotProp_CannonMode = YuriSlotProp_Cannoneer1 + 8
YuriSlotProp_CannonWheels_RotationX = YuriSlotProp_Cannoneer1 + 9
YuriSlotProp_CannonTimer = YuriSlotProp_Cannoneer1 + 10
YuriSlotProp_CannonRamrod1 = YuriSlotProp_Cannoneer1 + 11
YuriSlotProp_CannonRamrod2 = YuriSlotProp_Cannoneer1 + 12
YuriSlotProp_CannonBarrel_RotationX = YuriSlotProp_Cannoneer1 + 13
YuriSlotProp_CannonBarrel_RotationZ = YuriSlotProp_Cannoneer1 + 14
YuriSlotProp_CannonLastReloadingPhase = YuriSlotProp_Cannoneer1 + 15
YuriSlotProp_CannonCannonball = YuriSlotProp_Cannoneer1 + 16
YuriSlotProp_CannonballIsFlying = YuriSlotProp_Cannoneer1 + 17
YuriSlotProp_CannonballAngleZ = YuriSlotProp_Cannoneer1 + 18
YuriSlotProp_CannonballAngleAlpha = YuriSlotProp_Cannoneer1 + 19
YuriSlotProp_CannonballMuzzleVelocity = YuriSlotProp_Cannoneer1 + 20
YuriSlotProp_CannonballFlyingTime = YuriSlotProp_Cannoneer1 + 21
YuriSlotProp_CannonRecoilVelocity = YuriSlotProp_Cannoneer1 + 22
YuriSlotProp_CannonTeamNumber = YuriSlotProp_Cannoneer1 + 23
YuriSlotProp_CannonCartridgeType = YuriSlotProp_Cannoneer1 + 24
YuriSlotProp_CannonballIncomingSoundWasPlayed = YuriSlotProp_Cannoneer1 + 25
YuriSlotProp_CannonIsActive = YuriSlotProp_Cannoneer1 + 26
YuriSlotProp_CannonballProjectileType = YuriSlotProp_Cannoneer1 + 27
YuriSlotProp_CannonballHEType = YuriSlotProp_Cannoneer1 + 28
YuriSlotProp_CannonballFuseBallTimer = YuriSlotProp_Cannoneer1 + 29
slot_prop_is_occupied = YuriSlotProp_Cannoneer1 + 30
slot_prop_agent_attached = YuriSlotProp_Cannoneer1 + 31
slot_prop_pss_next_route_prop = YuriSlotProp_Cannoneer1 + 32
slot_prop_pss_previous_route_prop = YuriSlotProp_Cannoneer1 + 33
slot_prop_animation_start_material_string = YuriSlotProp_Cannoneer1 + 34
slot_prop_animation_number_of_frames = YuriSlotProp_Cannoneer1 + 35
slot_prop_animation_current_frame = YuriSlotProp_Cannoneer1 + 36
slot_prop_grenade_timer = YuriSlotProp_Cannoneer1 + 37
slot_prop_grenade_agent = YuriSlotProp_Cannoneer1 + 38
slot_prop_cannon_wheels_offset_y = YuriSlotProp_Cannoneer1 + 39
slot_prop_cannon_wheels_offset_z = YuriSlotProp_Cannoneer1 + 40
slot_prop_cannon_barrel_offset_z = YuriSlotProp_Cannoneer1 + 41
slot_prop_cannon_cannoneer_officer = YuriSlotProp_Cannoneer1 + 42
slot_prop_cannon_cannoneer1 = YuriSlotProp_Cannoneer1 + 43
slot_prop_cannon_cannoneer2 = YuriSlotProp_Cannoneer1 + 44
slot_prop_cannon_cannoneer3 = YuriSlotProp_Cannoneer1 + 45
slot_prop_cannon_timer = YuriSlotProp_Cannoneer1 + 46
slot_prop_cannon_state = YuriSlotProp_Cannoneer1 + 47
slot_prop_cannon_order_target_postion_x = YuriSlotProp_Cannoneer1 + 48
slot_prop_cannon_order_target_postion_y = YuriSlotProp_Cannoneer1 + 49
slot_prop_cannon_rope1 = YuriSlotProp_Cannoneer1 + 50
slot_prop_cannon_rope2 = YuriSlotProp_Cannoneer1 + 51
slot_prop_cannon_ramrod1 = YuriSlotProp_Cannoneer1 + 52
slot_prop_cannon_ramrod2 = YuriSlotProp_Cannoneer1 + 53
slot_prop_cannon_shell = YuriSlotProp_Cannoneer1 + 54
slot_prop_cannon_wheels = YuriSlotProp_Cannoneer1 + 55
slot_prop_cannon_barrel = YuriSlotProp_Cannoneer1 + 56
slot_prop_cannon_wheels_rotation_x = YuriSlotProp_Cannoneer1 + 57
slot_prop_cannon_barrel_rotation_x = YuriSlotProp_Cannoneer1 + 58
slot_prop_cannon_reload_time = YuriSlotProp_Cannoneer1 + 59
slot_prop_cannon_reload_state_initial = YuriSlotProp_Cannoneer1 + 60
slot_prop_cannon_reload_state = YuriSlotProp_Cannoneer1 + 61
slot_prop_cannon_timer_reload = YuriSlotProp_Cannoneer1 + 62
slot_prop_cannon_type = YuriSlotProp_Cannoneer1 + 63
slot_prop_cannon_era = YuriSlotProp_Cannoneer1 + 64
slot_prop_shell_phase = YuriSlotProp_Cannoneer1 + 65
slot_prop_shell_agent = YuriSlotProp_Cannoneer1 + 66
slot_prop_cannon_pos_x = YuriSlotProp_Cannoneer1 + 67
slot_prop_cannon_pos_y = YuriSlotProp_Cannoneer1 + 68
slot_prop_cannon_recoil_velocity = YuriSlotProp_Cannoneer1 + 69
slot_prop_cannon_shell_phase = YuriSlotProp_Cannoneer1 + 70
slot_prop_cannon_target_x = YuriSlotProp_Cannoneer1 + 71
slot_prop_cannon_target_y = YuriSlotProp_Cannoneer1 + 72
slot_prop_cannon_target_z = YuriSlotProp_Cannoneer1 + 73

projectile_type_fieldgun_explosive_earlygame = 1
projectile_type_fieldgun_explosive_lategame = 2
projectile_type_fieldgun_gas_shell = 3
projectile_type_howitzer_explosive_earlygame = 4
projectile_type_howitzer_explosive_lategame = 5
projectile_type_howitzer_gas_shell = 6

cannon_state_inactive = -1
cannon_state_moving1 = 1
cannon_state_moving2 = 2
cannon_state_reloading = 3
cannon_state_aiming1 = 4
cannon_state_aiming2 = 5
cannon_state_aiming_finished = 6
cannon_state_firing1 = 7
cannon_state_firing2 = 8

cannon_reload_state_1_cleaning_barrel_1 = 1
cannon_reload_state_1_cleaning_barrel_2 = 2
cannon_reload_state_1_inserting_shell_1 = 3
cannon_reload_state_1_inserting_shell_2 = 4
cannon_reload_state_1_pushing_shell_1 = 5
cannon_reload_state_1_pushing_shell_2 = 6

cannon_reload_state_2_cleaning_barrel_1 = 7
cannon_reload_state_2_cleaning_barrel_2 = 8
cannon_reload_state_2_inserting_shell_1 = 9
cannon_reload_state_2_inserting_shell_2 = 10

cannon_reload_state_3_inserting_shell_1 = 11
cannon_reload_state_3_inserting_shell_2 = 12

cannon_reload_state_finished = 20

square_forming_phase_outer_square1 = 0
square_forming_phase_outer_square2 = 1
square_forming_phase_outer_square3 = 2
square_forming_phase_outer_square4 = 3
square_forming_phase_inner_square1 = 4
square_forming_phase_inner_square2 = 5
square_forming_phase_inner_square3 = 6
square_forming_phase_inner_square4 = 7
square_forming_phase_excess = 8

rifle_type_smoothbore = 0
rifle_type_rifled = 1
rifle_type_converted = 2
rifle_type_smallcaliber = 3
rifle_type_boltaction = 4
rifle_type_boltactionmodern = 5

voices_1000ms_limit_warcry = 7

company_pai_state_generic = 0
company_pai_state_detached = 1

formation_type_ranged = 1
formation_type_melee  = 2

pai_global_tactic_simple_charge = 1
pai_global_tactic_initial = 2
pai_global_tactic_defend_initial = 3
pai_global_tactic_attack_initial = 4
pai_global_tactic_attack_forming_ranks = 5
pai_global_tactic_attack_approaching = 6
pai_global_tactic_defend_holding_position = 7
pai_global_tactic_attack_charging = 8
pai_global_tactic_attack_approaching_close = 9
pai_global_tactic_attack_retreat = 10
pai_global_tactic_attack_stop_retreat = 11
pai_global_tactic_siege_defend_initial = 12
pai_global_tactic_siege_attack_initial = 13
pai_global_tactic_siege_defend_holding_position = 14
pai_global_tactic_attack_forming_ranks = 15
pai_global_tactic_attack = 16

spawable_prop_limit = 4000

pbs_menu_distance_between_infolists = 90

pbs_troop_type_line = 1
pbs_troop_type_light = 2
pbs_troop_type_guard = 3
pbs_troop_type_cavmelee = 4
pbs_troop_type_cavranged = 5
pbs_troop_type_cavguard = 6
pbs_troop_type_fieldguns = 7
pbs_troop_type_howitzers = 8
pbs_troop_type_heavyhowitzers = 9
pbs_troop_type_mg = 10
pbs_troop_type_shock = 11
pbs_troop_type_armor = 12

pbs_state_generic = 0
pbs_state_moving_to_position = 1
pbs_state_holding_position = 2
pbs_state_charging = 3
pbs_state_retreating = 4
pbs_state_is_reinforcement = 5

pbs_run_mode_walking = 0
pbs_run_mode_running = 1

company1 = 0
company2 = 1
company3 = 2
company4 = 3
company5 = 4
company6 = 5
company7 = 6
company8 = 7

shader_spring		= 0
shader_summer		= 1
shader_autumn		= 2
shader_winter		= 3

## Prebattle Deployment Begin
max_battle_size = 1000
slot_troop_prebattle_first_round      = 157 
slot_troop_prebattle_array            = 158 
slot_troop_prebattle_num_upgrade      = 159  
slot_troop_prebattle_preupgrade_check = 160   
slot_party_prebattle_customized_deployment = 73  
slot_party_prebattle_battle_size           = 74 
slot_party_prebattle_size_in_battle        = 75  
slot_party_prebattle_in_battle_count       = 76 
## Prebattle Deployment End

slot_troop_pbs_type = 162
slot_troop_language = 163

## ZZ Custom Kingdom Troops begin
slot_item_difficulty                = 101
slot_item_weight                    = 102
slot_item_price                     = 450
slot_custom_troop_wage              = 313
slot_custom_troop_weight            = 314
slot_custom_troop_ap                = 315
slot_custom_troop_sp                = 316
slot_custom_troop_wp                = 317
custom_troop_begin = "trp_kingdom_recruit"
custom_troop_end = "trp_array_a"
## ZZ Custom Kingdom Troops end

slot_item_pes_begin      = 500
slot_item_price_history_begin      = slot_item_pes_begin + 0
slot_item_price_history_end      = slot_item_pes_begin + 100
slot_item_factions_quality1_begin      = slot_item_price_history_end + 0
slot_item_factions_quality2_begin      = slot_item_price_history_end + 40
slot_item_factions_factory_number1_begin      = slot_item_price_history_end + 80
slot_item_factions_factory_number2_begin      = slot_item_price_history_end + 160
slot_item_factions_supply1_begin      = slot_item_price_history_end + 200
slot_item_factions_supply2_begin      = slot_item_price_history_end + 240
slot_item_factions_demand1_begin      = slot_item_price_history_end + 280
slot_item_factions_demand2_begin      = slot_item_price_history_end + 320
slot_item_factions_demand2_end        = slot_item_price_history_end + 360
slot_item_supply1      = slot_item_factions_demand2_end + 1
slot_item_supply2      = slot_item_factions_demand2_end + 2
slot_item_demand1      = slot_item_factions_demand2_end + 3
slot_item_demand2      = slot_item_factions_demand2_end + 4
slot_item_price_initial      = slot_item_factions_demand2_end + 5
slot_item_raw_resource1      = slot_item_factions_demand2_end + 6
slot_item_raw_resource2      = slot_item_factions_demand2_end + 7
slot_item_raw_resource1_amount      = slot_item_factions_demand2_end + 8
slot_item_raw_resource2_amount      = slot_item_factions_demand2_end + 9
slot_item_output_size      = slot_item_factions_demand2_end + 10
slot_item_price_aux      = slot_item_factions_demand2_end + 11

slot_item_pointer_number_of_pointers   = 400

########################################################
##  ITEM SLOTS             #############################
########################################################

slot_item_is_checked               = 0
slot_item_food_bonus               = 1
slot_item_book_reading_progress    = 2
slot_item_book_read                = 3
slot_item_intelligence_requirement = 4

slot_item_amount_available         = 7

slot_item_urban_demand             = 11 #consumer demand for a good in town, measured in abstract units. The more essential the item (ie, like grain) the higher the price
slot_item_rural_demand             = 12 #consumer demand in villages, measured in abstract units
slot_item_desert_demand            = 13 #consumer demand in villages, measured in abstract units

slot_item_production_slot          = 14 
slot_item_production_string        = 15 

slot_item_tied_to_good_price       = 20 #ie, weapons and metal armor to tools, padded to cloth, leather to leatherwork, etc

slot_item_num_positions            = 22
slot_item_positions_begin          = 23 #reserve around 5 slots after this


slot_item_multiplayer_faction_price_multipliers_begin = 30 #reserve around 10 slots after this

slot_item_primary_raw_material    		= 50
slot_item_is_raw_material_only_for      = 51
slot_item_input_number                  = 52 #ie, how many items of inputs consumed per run
slot_item_base_price                    = 53 #taken from module_items
#slot_item_production_site			    = 54 #a string replaced with function - Armagan
slot_item_output_per_run                = 55 #number of items produced per run
slot_item_overhead_per_run              = 56 #labor and overhead per run
slot_item_secondary_raw_material        = 57 #in this case, the amount used is only one
slot_item_enterprise_building_cost      = 58 #enterprise building cost
#INVASION MODE START
slot_item_ccoop_has_ammo                = 59 #should be set to 1 for Invasion item drops that have an additional item for ammunition (e.g. Javelin Bow)
#INVASION MODE END


slot_item_multiplayer_item_class   = 60 #temporary, can be moved to higher values
slot_item_multiplayer_availability_linked_list_begin = 61 #temporary, can be moved to higher values

slot_item_rifled_analog = 2000
slot_item_converted_analog = slot_item_rifled_analog + 1
slot_item_small_caliber_analog = slot_item_rifled_analog + 2
slot_item_bolt_action_analog = slot_item_rifled_analog + 3
slot_item_bolt_action_modern_analog = slot_item_rifled_analog + 4
slot_item_appearance_year = slot_item_rifled_analog + 5
slot_item_rpm = slot_item_rifled_analog + 6

########################################################
##  AGENT SLOTS            #############################
########################################################

slot_agent_target_entry_point     = 0
slot_agent_target_x_pos           = 1
slot_agent_target_y_pos           = 2
slot_agent_is_alive_before_retreat= 3
slot_agent_is_in_scripted_mode    = 4
slot_agent_is_not_reinforcement   = 5
slot_agent_tournament_point       = 6
slot_agent_arena_team_set         = 7
slot_agent_spawn_entry_point      = 8
slot_agent_target_prop_instance   = 9
slot_agent_map_overlay_id         = 10
slot_agent_target_entry_point     = 11
slot_agent_initial_ally_power     = 12
slot_agent_initial_enemy_power    = 13
slot_agent_enemy_threat           = 14
slot_agent_is_running_away        = 15
slot_agent_courage_score          = 16
slot_agent_is_respawn_as_bot      = 17
slot_agent_cur_animation          = 18
slot_agent_next_action_time       = 19
slot_agent_state                  = 20
slot_agent_in_duel_with           = 21
slot_agent_duel_start_time        = 22

slot_agent_walker_occupation      = 25
#Equipment cost fix
slot_agent_bought_horse           = 26
###
#INVASION MODE START
slot_agent_doom_javelin_count     = 27
slot_agent_doom_javelin_attacker  = 28
#INVASION MODE END
    
slot_agent_pbs_state              = 29
slot_agent_can_crouch             = 30
slot_agent_hold_order_x           = 31
slot_agent_hold_order_y           = 32
slot_agent_speaking_cooldown      = 33
slot_agent_square_formation_state = 34
#slots 35-41 are occupied
slot_agent_lemat_canister_has_been_shot = 42
slot_agent_pbs_stuck_timer = 43
slot_agent_was_killed_or_knocked_down      = 44
slot_agent_flag_prop      = 45
slot_agent_prone_status      = 46
slot_agent_prone_reload_timer      = 47
slot_agent_digin_timer      = 48
slot_agent_prop1      = 49
slot_agent_prop2      = 50
slot_agent_mg_is_deployed      = 51
slot_agent_mg_bullets      = 52
slot_agent_mg_bullets_timer      = 53
slot_agent_pss_current_route_prop      = 54
slot_agent_pss_current_direction      = 55
slot_agent_pss_wide_offset      = 56
slot_agent_musketramordanimation_animation_progress      = 57
slot_agent_musketramordanimation_ramrod_prop      = 58
slot_agent_lmg_fire_start_timer      = 59
slot_agent_grenade_state      = 60
slot_agent_cannon_gas_shell 	= 61
slot_agent_under_gas_attack_timer 	= 62
slot_agent_pinned_down_timer 	= 63

########################################################
##  FACTION SLOTS          #############################
########################################################
slot_faction_ai_state                   = 4
slot_faction_ai_object                  = 5
slot_faction_ai_rationale               = 6 #Currently unused, can be linked to strings generated from decision checklists


slot_faction_marshall                   = 8
slot_faction_ai_offensive_max_followers = 9

slot_faction_culture                    = 10
slot_faction_leader                     = 11

slot_faction_temp_slot                  = 12

##slot_faction_vassal_of            = 11
slot_faction_banner                     = 15

slot_faction_number_of_parties    = 20
slot_faction_state                = 21

slot_faction_adjective            = 22


slot_faction_player_alarm         		= 30
slot_faction_last_mercenary_offer_time 	= 31
slot_faction_recognized_player    		= 32

#overriding troop info for factions in quick start mode.
slot_faction_quick_battle_tier_1_infantry      = 41
slot_faction_quick_battle_tier_2_infantry      = 42
slot_faction_quick_battle_tier_1_archer        = 43
slot_faction_quick_battle_tier_2_archer        = 44
slot_faction_quick_battle_tier_1_cavalry       = 45
slot_faction_quick_battle_tier_2_cavalry       = 46

slot_faction_tier_1_troop         = 41
slot_faction_tier_2_troop         = 42
slot_faction_tier_3_troop         = 43
slot_faction_tier_4_troop         = 44
slot_faction_tier_5_troop         = 45

slot_faction_deserter_troop       = 48
slot_faction_guard_troop          = 49
slot_faction_messenger_troop      = 50
slot_faction_prison_guard_troop   = 51
slot_faction_castle_guard_troop   = 52

slot_faction_town_walker_male_troop      = 53
slot_faction_town_walker_female_troop    = 54
slot_faction_village_walker_male_troop   = 55
slot_faction_village_walker_female_troop = 56
slot_faction_town_spy_male_troop         = 57
slot_faction_town_spy_female_troop       = 58

slot_faction_has_rebellion_chance = 60

slot_faction_instability          = 61 #last time measured


#UNIMPLEMENTED FEATURE ISSUES
slot_faction_war_damage_inflicted_when_marshal_appointed = 62 #Probably deprecate
slot_faction_war_damage_suffered_when_marshal_appointed  = 63 #Probably deprecate

slot_faction_political_issue 							 = 64 #Center or marshal appointment
slot_faction_political_issue_time 						 = 65 #Now is used


#Rebellion changes
#slot_faction_rebellion_target                     = 65
#slot_faction_inactive_leader_location         = 66
#slot_faction_support_base                     = 67
#Rebellion changes



#slot_faction_deserter_party_template       = 62

slot_faction_reinforcements_a        = 77
slot_faction_reinforcements_b        = 78
slot_faction_reinforcements_c        = 79

slot_faction_num_armies              = 80
slot_faction_num_castles             = 81
slot_faction_num_towns               = 82

slot_faction_last_attacked_center    = 85
slot_faction_last_attacked_hours     = 86
slot_faction_last_safe_hours         = 87

slot_faction_num_routed_agents       = 90

#useful for competitive consumption
slot_faction_biggest_feast_score      = 91
slot_faction_biggest_feast_time       = 92
slot_faction_biggest_feast_host       = 93


#Faction AI states
slot_faction_last_feast_concluded       = 94 #Set when a feast starts -- this needs to be deprecated
slot_faction_last_feast_start_time      = 94 #this is a bit confusing


slot_faction_ai_last_offensive_time 	= 95 #Set when an offensive concludes
slot_faction_last_offensive_concluded 	= 95 #Set when an offensive concludes

slot_faction_ai_last_rest_time      	= 96 #the last time that the faction has had default or feast AI -- this determines lords' dissatisfaction with the campaign. Set during faction_ai script
slot_faction_ai_current_state_started   = 97 #

slot_faction_ai_last_decisive_event     = 98 #capture a fortress or declaration of war

slot_faction_morale_of_player_troops    = 99

#diplomacy
slot_faction_truce_days_with_factions_begin 			= 120
slot_faction_provocation_days_with_factions_begin 		= 160
slot_faction_war_damage_inflicted_on_factions_begin 	= 200
slot_faction_sum_advice_about_factions_begin 			= 240
slot_faction_ve_mod_slots_begin = 400
slot_faction_fieldgun_cannoneer_officer   	 = slot_faction_ve_mod_slots_begin + 1
slot_faction_howitzer_cannoneer_officer    	 = slot_faction_ve_mod_slots_begin + 2
slot_faction_fieldgun_cannoneer    			 = slot_faction_ve_mod_slots_begin + 3
slot_faction_howitzer_cannoneer    			 = slot_faction_ve_mod_slots_begin + 4
slot_faction_reinforcements_artillery   	 = slot_faction_ve_mod_slots_begin + 5
slot_faction_technology_modernattack   			 = slot_faction_ve_mod_slots_begin + 6
slot_faction_technology_crimeanwar   			 = slot_faction_ve_mod_slots_begin + 7
slot_faction_technology_riflesboltactionmodern    = slot_faction_ve_mod_slots_begin + 8
slot_faction_technology_riflesconverted   		 = slot_faction_ve_mod_slots_begin + 9
slot_faction_technology_riflessmallcaliber   	 = slot_faction_ve_mod_slots_begin + 10
slot_faction_technology_riflesboltaction   		 = slot_faction_ve_mod_slots_begin + 11
slot_faction_technology_lateshells		   		 = slot_faction_ve_mod_slots_begin + 12
slot_faction_technology_machineguns		   		 = slot_faction_ve_mod_slots_begin + 13
slot_faction_technology_infantrymgtactics		   	 = slot_faction_ve_mod_slots_begin + 14
slot_faction_technology_cannonsbreechloading		 = slot_faction_ve_mod_slots_begin + 15
slot_faction_technology_modernartillery			 = slot_faction_ve_mod_slots_begin + 16
slot_faction_technology_coveringfire	 		 = slot_faction_ve_mod_slots_begin + 17
slot_faction_technology_gasattacks			 = slot_faction_ve_mod_slots_begin + 18
slot_faction_technology_skirmishline			 = slot_faction_ve_mod_slots_begin + 19
slot_faction_technology_moderndefence		 = slot_faction_ve_mod_slots_begin + 20
slot_faction_technology_lmgs			 = slot_faction_ve_mod_slots_begin + 21
slot_faction_technology_shocktroops 		 = slot_faction_ve_mod_slots_begin + 22
slot_faction_technology_tanks		 = slot_faction_ve_mod_slots_begin + 23
slot_faction_technology_riflesrifled			 = slot_faction_ve_mod_slots_begin + 24
# 25 - 43 are occupied with presets
slot_faction_current_research_technology		 = slot_faction_ve_mod_slots_begin + 44
slot_faction_army_drill_level					 = slot_faction_ve_mod_slots_begin + 45
slot_faction_flag_map							 = slot_faction_ve_mod_slots_begin + 46
slot_faction_flag_material						 = slot_faction_ve_mod_slots_begin + 47
slot_faction_wardrobe_begin					 = slot_faction_ve_mod_slots_begin + 48
slot_faction_wardrobe_end						 = slot_faction_ve_mod_slots_begin + 49
slot_faction_infamy							 = slot_faction_ve_mod_slots_begin + 50
slot_faction_casus_belli_target				 = slot_faction_ve_mod_slots_begin + 51
slot_faction_casus_belli_progress				 = slot_faction_ve_mod_slots_begin + 52
slot_faction_improve_relations_target			 = slot_faction_ve_mod_slots_begin + 53
slot_faction_improve_relations_progress			 = slot_faction_ve_mod_slots_begin + 54
slot_faction_days_of_war_with_faction_before_pressure_begin= slot_faction_ve_mod_slots_begin + 55
# 56 - 96 are occupied
slot_faction_alliance_price = slot_faction_ve_mod_slots_begin + 97
slot_faction_increase_relations_price = slot_faction_ve_mod_slots_begin + 98
slot_faction_preset_aggressiveness = slot_faction_ve_mod_slots_begin + 99
slot_faction_preset_reliability = slot_faction_ve_mod_slots_begin + 100

slot_faction_government_type = slot_faction_ve_mod_slots_begin + 101
slot_faction_ruling_political_party = slot_faction_ve_mod_slots_begin + 102
slot_faction_does_have_parliament = slot_faction_ve_mod_slots_begin + 103
slot_faction_law_military_service_term = slot_faction_ve_mod_slots_begin + 104
slot_faction_law_nomination_rules = slot_faction_ve_mod_slots_begin + 105
slot_faction_law_voting_franchise = slot_faction_ve_mod_slots_begin + 106
slot_faction_law_public_meetings = slot_faction_ve_mod_slots_begin + 107
slot_faction_law_press = slot_faction_ve_mod_slots_begin + 108
slot_faction_law_voting_openness = slot_faction_ve_mod_slots_begin + 109
slot_faction_law_executive_branch = slot_faction_ve_mod_slots_begin + 110
slot_faction_law_income_tax = slot_faction_ve_mod_slots_begin + 111
slot_faction_law_goodsservices_tax = slot_faction_ve_mod_slots_begin + 112
slot_faction_law_importexport_tax = slot_faction_ve_mod_slots_begin + 113
slot_faction_law_education_expenses = slot_faction_ve_mod_slots_begin + 114
slot_faction_law_infrastructure_expenses = slot_faction_ve_mod_slots_begin + 115
slot_faction_law_healthcare_expenses = slot_faction_ve_mod_slots_begin + 116
slot_faction_law_workers_conditions = slot_faction_ve_mod_slots_begin + 117
slot_faction_law_workers_wage = slot_faction_ve_mod_slots_begin + 118
slot_faction_law_trade_unions = slot_faction_ve_mod_slots_begin + 119
slot_faction_law_military_expenses = slot_faction_ve_mod_slots_begin + 120
slot_faction_aileader_political_party = slot_faction_ve_mod_slots_begin + 121
slot_faction_aileader_pvol_military_service_term = slot_faction_ve_mod_slots_begin + 122
slot_faction_aileader_pvol_nomination_rules = slot_faction_ve_mod_slots_begin + 123
slot_faction_aileader_pvol_voting_franchise = slot_faction_ve_mod_slots_begin + 124
slot_faction_aileader_pvol_public_meetings = slot_faction_ve_mod_slots_begin + 125
slot_faction_aileader_pvol_press = slot_faction_ve_mod_slots_begin + 126
slot_faction_aileader_pvol_voting_openness = slot_faction_ve_mod_slots_begin + 127
slot_faction_aileader_pvol_executive_branch = slot_faction_ve_mod_slots_begin + 128
slot_faction_aileader_pvol_income_tax = slot_faction_ve_mod_slots_begin + 129
slot_faction_aileader_pvol_goodsservices_tax = slot_faction_ve_mod_slots_begin + 130
slot_faction_aileader_pvol_importexport_tax = slot_faction_ve_mod_slots_begin + 131
slot_faction_aileader_pvol_education_expenses = slot_faction_ve_mod_slots_begin + 132
slot_faction_aileader_pvol_infrastructure_expenses = slot_faction_ve_mod_slots_begin + 133
slot_faction_aileader_pvol_healthcare_expenses = slot_faction_ve_mod_slots_begin + 134
slot_faction_aileader_pvol_workers_conditions = slot_faction_ve_mod_slots_begin + 135
slot_faction_aileader_pvol_workers_wage = slot_faction_ve_mod_slots_begin + 136
slot_faction_aileader_pvol_trade_unions = slot_faction_ve_mod_slots_begin + 137
slot_faction_aileader_pvol_military_expenses = slot_faction_ve_mod_slots_begin + 138
slot_faction_political_party1_name = slot_faction_ve_mod_slots_begin + 139
slot_faction_political_party2_name = slot_faction_ve_mod_slots_begin + 140
slot_faction_political_party3_name = slot_faction_ve_mod_slots_begin + 141
slot_faction_political_party4_name = slot_faction_ve_mod_slots_begin + 142
slot_faction_political_party1_ideology = slot_faction_ve_mod_slots_begin + 143
slot_faction_political_party2_ideology = slot_faction_ve_mod_slots_begin + 144
slot_faction_political_party3_ideology = slot_faction_ve_mod_slots_begin + 145
slot_faction_political_party4_ideology = slot_faction_ve_mod_slots_begin + 146
slot_faction_political_party1_desc = slot_faction_ve_mod_slots_begin + 147
slot_faction_political_party2_desc = slot_faction_ve_mod_slots_begin + 148
slot_faction_political_party3_desc = slot_faction_ve_mod_slots_begin + 149
slot_faction_political_party4_desc = slot_faction_ve_mod_slots_begin + 150
slot_faction_political_party1_places_in_parliament = slot_faction_ve_mod_slots_begin + 151
slot_faction_political_party2_places_in_parliament = slot_faction_ve_mod_slots_begin + 152
slot_faction_political_party3_places_in_parliament = slot_faction_ve_mod_slots_begin + 153
slot_faction_political_party4_places_in_parliament = slot_faction_ve_mod_slots_begin + 154
slot_faction_political_party1_influence = slot_faction_ve_mod_slots_begin + 155
slot_faction_political_party2_influence = slot_faction_ve_mod_slots_begin + 156
slot_faction_political_party3_influence = slot_faction_ve_mod_slots_begin + 157
slot_faction_political_party4_influence = slot_faction_ve_mod_slots_begin + 158
slot_faction_political_party1_conservatism = slot_faction_ve_mod_slots_begin + 159
slot_faction_political_party2_conservatism = slot_faction_ve_mod_slots_begin + 160
slot_faction_political_party3_conservatism = slot_faction_ve_mod_slots_begin + 161
slot_faction_political_party4_conservatism = slot_faction_ve_mod_slots_begin + 162
slot_faction_political_party1_pvol_military_service_term = slot_faction_ve_mod_slots_begin + 163
slot_faction_political_party1_pvol_nomination_rules = slot_faction_ve_mod_slots_begin + 164
slot_faction_political_party1_pvol_voting_franchise = slot_faction_ve_mod_slots_begin + 165
slot_faction_political_party1_pvol_public_meetings = slot_faction_ve_mod_slots_begin + 166
slot_faction_political_party1_pvol_press = slot_faction_ve_mod_slots_begin + 167
slot_faction_political_party1_pvol_voting_openness = slot_faction_ve_mod_slots_begin + 168
slot_faction_political_party1_pvol_executive_branch = slot_faction_ve_mod_slots_begin + 169
slot_faction_political_party1_pvol_income_tax = slot_faction_ve_mod_slots_begin + 170
slot_faction_political_party1_pvol_goodsservices_tax = slot_faction_ve_mod_slots_begin + 171
slot_faction_political_party1_pvol_importexport_tax = slot_faction_ve_mod_slots_begin + 172
slot_faction_political_party1_pvol_education_expenses = slot_faction_ve_mod_slots_begin + 173
slot_faction_political_party1_pvol_infrastructure_expenses = slot_faction_ve_mod_slots_begin + 174
slot_faction_political_party1_pvol_healthcare_expenses = slot_faction_ve_mod_slots_begin + 175
slot_faction_political_party1_pvol_workers_conditions = slot_faction_ve_mod_slots_begin + 176
slot_faction_political_party1_pvol_workers_wage = slot_faction_ve_mod_slots_begin + 177
slot_faction_political_party1_pvol_trade_unions = slot_faction_ve_mod_slots_begin + 178
slot_faction_political_party1_pvol_military_expenses = slot_faction_ve_mod_slots_begin + 179
slot_faction_political_party2_pvol_military_service_term = slot_faction_ve_mod_slots_begin + 180
slot_faction_political_party2_pvol_nomination_rules = slot_faction_ve_mod_slots_begin + 181
slot_faction_political_party2_pvol_voting_franchise = slot_faction_ve_mod_slots_begin + 182
slot_faction_political_party2_pvol_public_meetings = slot_faction_ve_mod_slots_begin + 183
slot_faction_political_party2_pvol_press = slot_faction_ve_mod_slots_begin + 184
slot_faction_political_party2_pvol_voting_openness = slot_faction_ve_mod_slots_begin + 185
slot_faction_political_party2_pvol_executive_branch = slot_faction_ve_mod_slots_begin + 186
slot_faction_political_party2_pvol_income_tax = slot_faction_ve_mod_slots_begin + 187
slot_faction_political_party2_pvol_goodsservices_tax = slot_faction_ve_mod_slots_begin + 188
slot_faction_political_party2_pvol_importexport_tax = slot_faction_ve_mod_slots_begin + 189
slot_faction_political_party2_pvol_education_expenses = slot_faction_ve_mod_slots_begin + 190
slot_faction_political_party2_pvol_infrastructure_expenses = slot_faction_ve_mod_slots_begin + 191
slot_faction_political_party2_pvol_healthcare_expenses = slot_faction_ve_mod_slots_begin + 192
slot_faction_political_party2_pvol_workers_conditions = slot_faction_ve_mod_slots_begin + 193
slot_faction_political_party2_pvol_workers_wage = slot_faction_ve_mod_slots_begin + 194
slot_faction_political_party2_pvol_trade_unions = slot_faction_ve_mod_slots_begin + 195
slot_faction_political_party2_pvol_military_expenses = slot_faction_ve_mod_slots_begin + 196
slot_faction_political_party3_pvol_military_service_term = slot_faction_ve_mod_slots_begin + 197
slot_faction_political_party3_pvol_nomination_rules = slot_faction_ve_mod_slots_begin + 198
slot_faction_political_party3_pvol_voting_franchise = slot_faction_ve_mod_slots_begin + 199
slot_faction_political_party3_pvol_public_meetings = slot_faction_ve_mod_slots_begin + 200
slot_faction_political_party3_pvol_press = slot_faction_ve_mod_slots_begin + 201
slot_faction_political_party3_pvol_voting_openness = slot_faction_ve_mod_slots_begin + 202
slot_faction_political_party3_pvol_executive_branch = slot_faction_ve_mod_slots_begin + 203
slot_faction_political_party3_pvol_income_tax = slot_faction_ve_mod_slots_begin + 204
slot_faction_political_party3_pvol_goodsservices_tax = slot_faction_ve_mod_slots_begin + 205
slot_faction_political_party3_pvol_importexport_tax = slot_faction_ve_mod_slots_begin + 206
slot_faction_political_party3_pvol_education_expenses = slot_faction_ve_mod_slots_begin + 207
slot_faction_political_party3_pvol_infrastructure_expenses = slot_faction_ve_mod_slots_begin + 208
slot_faction_political_party3_pvol_healthcare_expenses = slot_faction_ve_mod_slots_begin + 209
slot_faction_political_party3_pvol_workers_conditions = slot_faction_ve_mod_slots_begin + 210
slot_faction_political_party3_pvol_workers_wage = slot_faction_ve_mod_slots_begin + 211
slot_faction_political_party3_pvol_trade_unions = slot_faction_ve_mod_slots_begin + 212
slot_faction_political_party3_pvol_military_expenses = slot_faction_ve_mod_slots_begin + 213
slot_faction_political_party4_pvol_military_service_term = slot_faction_ve_mod_slots_begin + 214
slot_faction_political_party4_pvol_nomination_rules = slot_faction_ve_mod_slots_begin + 215
slot_faction_political_party4_pvol_voting_franchise = slot_faction_ve_mod_slots_begin + 216
slot_faction_political_party4_pvol_public_meetings = slot_faction_ve_mod_slots_begin + 217
slot_faction_political_party4_pvol_press = slot_faction_ve_mod_slots_begin + 218
slot_faction_political_party4_pvol_voting_openness = slot_faction_ve_mod_slots_begin + 219
slot_faction_political_party4_pvol_executive_branch = slot_faction_ve_mod_slots_begin + 220
slot_faction_political_party4_pvol_income_tax = slot_faction_ve_mod_slots_begin + 221
slot_faction_political_party4_pvol_goodsservices_tax = slot_faction_ve_mod_slots_begin + 222
slot_faction_political_party4_pvol_importexport_tax = slot_faction_ve_mod_slots_begin + 223
slot_faction_political_party4_pvol_education_expenses = slot_faction_ve_mod_slots_begin + 224
slot_faction_political_party4_pvol_infrastructure_expenses = slot_faction_ve_mod_slots_begin + 225
slot_faction_political_party4_pvol_healthcare_expenses = slot_faction_ve_mod_slots_begin + 226
slot_faction_political_party4_pvol_workers_conditions = slot_faction_ve_mod_slots_begin + 227
slot_faction_political_party4_pvol_workers_wage = slot_faction_ve_mod_slots_begin + 228
slot_faction_political_party4_pvol_trade_unions = slot_faction_ve_mod_slots_begin + 229
slot_faction_political_party4_pvol_military_expenses = slot_faction_ve_mod_slots_begin + 230
slot_faction_class_upper_aristocracy_political_activity = slot_faction_ve_mod_slots_begin + 231
slot_faction_class_upper_bourgeoisie_political_activity = slot_faction_ve_mod_slots_begin + 232
slot_faction_class_middle_political_activity = slot_faction_ve_mod_slots_begin + 233
slot_faction_class_lower_urban_political_activity = slot_faction_ve_mod_slots_begin + 234
slot_faction_class_lower_rural_political_activity = slot_faction_ve_mod_slots_begin + 235
slot_faction_class_upper_aristocracy_attitude = slot_faction_ve_mod_slots_begin + 236
slot_faction_class_upper_bourgeoisie_attitude = slot_faction_ve_mod_slots_begin + 237
slot_faction_class_middle_attitude = slot_faction_ve_mod_slots_begin + 238
slot_faction_class_lower_urban_attitude = slot_faction_ve_mod_slots_begin + 239
slot_faction_class_lower_rural_attitude = slot_faction_ve_mod_slots_begin + 240
slot_faction_class_upper_aristocracy_pvol_military_service_term = slot_faction_ve_mod_slots_begin + 241
slot_faction_class_upper_aristocracy_pvol_nomination_rules = slot_faction_ve_mod_slots_begin + 242
slot_faction_class_upper_aristocracy_pvol_voting_franchise = slot_faction_ve_mod_slots_begin + 243
slot_faction_class_upper_aristocracy_pvol_public_meetings = slot_faction_ve_mod_slots_begin + 244
slot_faction_class_upper_aristocracy_pvol_press = slot_faction_ve_mod_slots_begin + 245
slot_faction_class_upper_aristocracy_pvol_voting_openness = slot_faction_ve_mod_slots_begin + 246
slot_faction_class_upper_aristocracy_pvol_executive_branch = slot_faction_ve_mod_slots_begin + 247
slot_faction_class_upper_aristocracy_pvol_income_tax = slot_faction_ve_mod_slots_begin + 248
slot_faction_class_upper_aristocracy_pvol_goodsservices_tax = slot_faction_ve_mod_slots_begin + 249
slot_faction_class_upper_aristocracy_pvol_importexport_tax = slot_faction_ve_mod_slots_begin + 250
slot_faction_class_upper_aristocracy_pvol_education_expenses = slot_faction_ve_mod_slots_begin + 251
slot_faction_class_upper_aristocracy_pvol_infrastructure_expenses = slot_faction_ve_mod_slots_begin + 252
slot_faction_class_upper_aristocracy_pvol_healthcare_expenses = slot_faction_ve_mod_slots_begin + 253
slot_faction_class_upper_aristocracy_pvol_workers_conditions = slot_faction_ve_mod_slots_begin + 254
slot_faction_class_upper_aristocracy_pvol_workers_wage = slot_faction_ve_mod_slots_begin + 255
slot_faction_class_upper_aristocracy_pvol_trade_unions = slot_faction_ve_mod_slots_begin + 256
slot_faction_class_upper_aristocracy_pvol_military_expenses = slot_faction_ve_mod_slots_begin + 257
slot_faction_class_upper_bourgeoisie_pvol_military_service_term = slot_faction_ve_mod_slots_begin + 258
slot_faction_class_upper_bourgeoisie_pvol_nomination_rules = slot_faction_ve_mod_slots_begin + 259
slot_faction_class_upper_bourgeoisie_pvol_voting_franchise = slot_faction_ve_mod_slots_begin + 260
slot_faction_class_upper_bourgeoisie_pvol_public_meetings = slot_faction_ve_mod_slots_begin + 261
slot_faction_class_upper_bourgeoisie_pvol_press = slot_faction_ve_mod_slots_begin + 262
slot_faction_class_upper_bourgeoisie_pvol_voting_openness = slot_faction_ve_mod_slots_begin + 263
slot_faction_class_upper_bourgeoisie_pvol_executive_branch = slot_faction_ve_mod_slots_begin + 264
slot_faction_class_upper_bourgeoisie_pvol_income_tax = slot_faction_ve_mod_slots_begin + 265
slot_faction_class_upper_bourgeoisie_pvol_goodsservices_tax = slot_faction_ve_mod_slots_begin + 266
slot_faction_class_upper_bourgeoisie_pvol_importexport_tax = slot_faction_ve_mod_slots_begin + 267
slot_faction_class_upper_bourgeoisie_pvol_education_expenses = slot_faction_ve_mod_slots_begin + 268
slot_faction_class_upper_bourgeoisie_pvol_infrastructure_expenses = slot_faction_ve_mod_slots_begin + 269
slot_faction_class_upper_bourgeoisie_pvol_healthcare_expenses = slot_faction_ve_mod_slots_begin + 270
slot_faction_class_upper_bourgeoisie_pvol_workers_conditions = slot_faction_ve_mod_slots_begin + 271
slot_faction_class_upper_bourgeoisie_pvol_workers_wage = slot_faction_ve_mod_slots_begin + 272
slot_faction_class_upper_bourgeoisie_pvol_trade_unions = slot_faction_ve_mod_slots_begin + 273
slot_faction_class_upper_bourgeoisie_pvol_military_expenses = slot_faction_ve_mod_slots_begin + 274
slot_faction_class_middle_pvol_military_service_term = slot_faction_ve_mod_slots_begin + 275
slot_faction_class_middle_pvol_nomination_rules = slot_faction_ve_mod_slots_begin + 276
slot_faction_class_middle_pvol_voting_franchise = slot_faction_ve_mod_slots_begin + 277
slot_faction_class_middle_pvol_public_meetings = slot_faction_ve_mod_slots_begin + 278
slot_faction_class_middle_pvol_press = slot_faction_ve_mod_slots_begin + 279
slot_faction_class_middle_pvol_voting_openness = slot_faction_ve_mod_slots_begin + 280
slot_faction_class_middle_pvol_executive_branch = slot_faction_ve_mod_slots_begin + 281
slot_faction_class_middle_pvol_income_tax = slot_faction_ve_mod_slots_begin + 282
slot_faction_class_middle_pvol_goodsservices_tax = slot_faction_ve_mod_slots_begin + 283
slot_faction_class_middle_pvol_importexport_tax = slot_faction_ve_mod_slots_begin + 284
slot_faction_class_middle_pvol_education_expenses = slot_faction_ve_mod_slots_begin + 285
slot_faction_class_middle_pvol_infrastructure_expenses = slot_faction_ve_mod_slots_begin + 286
slot_faction_class_middle_pvol_healthcare_expenses = slot_faction_ve_mod_slots_begin + 287
slot_faction_class_middle_pvol_workers_conditions = slot_faction_ve_mod_slots_begin + 288
slot_faction_class_middle_pvol_workers_wage = slot_faction_ve_mod_slots_begin + 289
slot_faction_class_middle_pvol_trade_unions = slot_faction_ve_mod_slots_begin + 290
slot_faction_class_middle_pvol_military_expenses = slot_faction_ve_mod_slots_begin + 291
slot_faction_class_lower_urban_pvol_military_service_term = slot_faction_ve_mod_slots_begin + 292
slot_faction_class_lower_urban_pvol_nomination_rules = slot_faction_ve_mod_slots_begin + 293
slot_faction_class_lower_urban_pvol_voting_franchise = slot_faction_ve_mod_slots_begin + 294
slot_faction_class_lower_urban_pvol_public_meetings = slot_faction_ve_mod_slots_begin + 295
slot_faction_class_lower_urban_pvol_press = slot_faction_ve_mod_slots_begin + 296
slot_faction_class_lower_urban_pvol_voting_openness = slot_faction_ve_mod_slots_begin + 297
slot_faction_class_lower_urban_pvol_executive_branch = slot_faction_ve_mod_slots_begin + 298
slot_faction_class_lower_urban_pvol_income_tax = slot_faction_ve_mod_slots_begin + 299
slot_faction_class_lower_urban_pvol_goodsservices_tax = slot_faction_ve_mod_slots_begin + 300
slot_faction_class_lower_urban_pvol_importexport_tax = slot_faction_ve_mod_slots_begin + 301
slot_faction_class_lower_urban_pvol_education_expenses = slot_faction_ve_mod_slots_begin + 302
slot_faction_class_lower_urban_pvol_infrastructure_expenses = slot_faction_ve_mod_slots_begin + 303
slot_faction_class_lower_urban_pvol_healthcare_expenses = slot_faction_ve_mod_slots_begin + 304
slot_faction_class_lower_urban_pvol_workers_conditions = slot_faction_ve_mod_slots_begin + 305
slot_faction_class_lower_urban_pvol_workers_wage = slot_faction_ve_mod_slots_begin + 306
slot_faction_class_lower_urban_pvol_trade_unions = slot_faction_ve_mod_slots_begin + 307
slot_faction_class_lower_urban_pvol_military_expenses = slot_faction_ve_mod_slots_begin + 308
slot_faction_class_lower_rural_pvol_military_service_term = slot_faction_ve_mod_slots_begin + 309
slot_faction_class_lower_rural_pvol_nomination_rules = slot_faction_ve_mod_slots_begin + 310
slot_faction_class_lower_rural_pvol_voting_franchise = slot_faction_ve_mod_slots_begin + 311
slot_faction_class_lower_rural_pvol_public_meetings = slot_faction_ve_mod_slots_begin + 312
slot_faction_class_lower_rural_pvol_press = slot_faction_ve_mod_slots_begin + 313
slot_faction_class_lower_rural_pvol_voting_openness = slot_faction_ve_mod_slots_begin + 314
slot_faction_class_lower_rural_pvol_executive_branch = slot_faction_ve_mod_slots_begin + 315
slot_faction_class_lower_rural_pvol_income_tax = slot_faction_ve_mod_slots_begin + 316
slot_faction_class_lower_rural_pvol_goodsservices_tax = slot_faction_ve_mod_slots_begin + 317
slot_faction_class_lower_rural_pvol_importexport_tax = slot_faction_ve_mod_slots_begin + 318
slot_faction_class_lower_rural_pvol_education_expenses = slot_faction_ve_mod_slots_begin + 319
slot_faction_class_lower_rural_pvol_infrastructure_expenses = slot_faction_ve_mod_slots_begin + 320
slot_faction_class_lower_rural_pvol_healthcare_expenses = slot_faction_ve_mod_slots_begin + 321
slot_faction_class_lower_rural_pvol_workers_conditions = slot_faction_ve_mod_slots_begin + 322
slot_faction_class_lower_rural_pvol_workers_wage = slot_faction_ve_mod_slots_begin + 323
slot_faction_class_lower_rural_pvol_trade_unions = slot_faction_ve_mod_slots_begin + 324
slot_faction_class_lower_rural_pvol_military_expenses = slot_faction_ve_mod_slots_begin + 325
slot_faction_class_upper_aristocracy_support_of_political_party1 = slot_faction_ve_mod_slots_begin + 326
slot_faction_class_upper_bourgeoisie_support_of_political_party1 = slot_faction_ve_mod_slots_begin + 327
slot_faction_class_middle_support_of_political_party1 = slot_faction_ve_mod_slots_begin + 328
slot_faction_class_lower_urban_support_of_political_party1 = slot_faction_ve_mod_slots_begin + 329
slot_faction_class_lower_rural_support_of_political_party1 = slot_faction_ve_mod_slots_begin + 330
slot_faction_class_upper_aristocracy_support_of_political_party2 = slot_faction_ve_mod_slots_begin + 331
slot_faction_class_upper_bourgeoisie_support_of_political_party2 = slot_faction_ve_mod_slots_begin + 332
slot_faction_class_middle_support_of_political_party2 = slot_faction_ve_mod_slots_begin + 333
slot_faction_class_lower_urban_support_of_political_party2 = slot_faction_ve_mod_slots_begin + 334
slot_faction_class_lower_rural_support_of_political_party2 = slot_faction_ve_mod_slots_begin + 335
slot_faction_class_upper_aristocracy_support_of_political_party3 = slot_faction_ve_mod_slots_begin + 336
slot_faction_class_upper_bourgeoisie_support_of_political_party3 = slot_faction_ve_mod_slots_begin + 337
slot_faction_class_middle_support_of_political_party3 = slot_faction_ve_mod_slots_begin + 338
slot_faction_class_lower_urban_support_of_political_party3 = slot_faction_ve_mod_slots_begin + 339
slot_faction_class_lower_rural_support_of_political_party3 = slot_faction_ve_mod_slots_begin + 340
slot_faction_class_upper_aristocracy_support_of_political_party4 = slot_faction_ve_mod_slots_begin + 341
slot_faction_class_upper_bourgeoisie_support_of_political_party4 = slot_faction_ve_mod_slots_begin + 342
slot_faction_class_middle_support_of_political_party4 = slot_faction_ve_mod_slots_begin + 343
slot_faction_class_lower_urban_support_of_political_party4 = slot_faction_ve_mod_slots_begin + 344
slot_faction_class_lower_rural_support_of_political_party4 = slot_faction_ve_mod_slots_begin + 345
slot_faction_class_upper_aristocracy_influence = slot_faction_ve_mod_slots_begin + 346
slot_faction_class_upper_bourgeoisie_influence = slot_faction_ve_mod_slots_begin + 347
slot_faction_class_middle_influence = slot_faction_ve_mod_slots_begin + 348
slot_faction_class_lower_urban_influence = slot_faction_ve_mod_slots_begin + 349
slot_faction_class_lower_rural_influence = slot_faction_ve_mod_slots_begin + 350
slot_faction_parliament_current_bill_law_type = slot_faction_ve_mod_slots_begin + 351
slot_faction_parliament_current_bill_law = slot_faction_ve_mod_slots_begin + 352
slot_faction_movement1_type = slot_faction_ve_mod_slots_begin + 353
slot_faction_movement2_type = slot_faction_ve_mod_slots_begin + 354
slot_faction_movement3_type = slot_faction_ve_mod_slots_begin + 355
slot_faction_movement4_type = slot_faction_ve_mod_slots_begin + 356
slot_faction_movement5_type = slot_faction_ve_mod_slots_begin + 357
slot_faction_movement1_influence = slot_faction_ve_mod_slots_begin + 358
slot_faction_movement2_influence = slot_faction_ve_mod_slots_begin + 359
slot_faction_movement3_influence = slot_faction_ve_mod_slots_begin + 360
slot_faction_movement4_influence = slot_faction_ve_mod_slots_begin + 361
slot_faction_movement5_influence = slot_faction_ve_mod_slots_begin + 362
slot_faction_movement1_popularity = slot_faction_ve_mod_slots_begin + 363
slot_faction_movement2_popularity = slot_faction_ve_mod_slots_begin + 364
slot_faction_movement3_popularity = slot_faction_ve_mod_slots_begin + 365
slot_faction_movement4_popularity = slot_faction_ve_mod_slots_begin + 366
slot_faction_movement5_popularity = slot_faction_ve_mod_slots_begin + 367
slot_faction_literacy = slot_faction_ve_mod_slots_begin + 368
slot_faction_population = slot_faction_ve_mod_slots_begin + 369
slot_faction_urbanization = slot_faction_ve_mod_slots_begin + 370
slot_faction_class_upper_aristocracy_wealth = slot_faction_ve_mod_slots_begin + 371
slot_faction_class_upper_bourgeoisie_wealth = slot_faction_ve_mod_slots_begin + 372
slot_faction_class_middle_wealth = slot_faction_ve_mod_slots_begin + 373
slot_faction_class_lower_urban_wealth = slot_faction_ve_mod_slots_begin + 374
slot_faction_class_lower_rural_wealth = slot_faction_ve_mod_slots_begin + 375
slot_faction_political_party1_places_in_executivebranch = slot_faction_ve_mod_slots_begin + 376
slot_faction_political_party2_places_in_executivebranch = slot_faction_ve_mod_slots_begin + 377
slot_faction_political_party3_places_in_executivebranch = slot_faction_ve_mod_slots_begin + 378
slot_faction_political_party4_places_in_executivebranch = slot_faction_ve_mod_slots_begin + 379
slot_faction_mgoperator    			 = slot_faction_ve_mod_slots_begin + 380
slot_faction_workers    			 = slot_faction_ve_mod_slots_begin + 381
slot_faction_workers_handicraft    			 = slot_faction_ve_mod_slots_begin + 382
slot_faction_workers_massproduction    			 = slot_faction_ve_mod_slots_begin + 383
slot_faction_gdp    			 = slot_faction_ve_mod_slots_begin + 384
slot_faction_pes_temp    			 = slot_faction_ve_mod_slots_begin + 385
slot_faction_gdp_urban    			 = slot_faction_ve_mod_slots_begin + 386
slot_faction_gdp_rural    			 = slot_faction_ve_mod_slots_begin + 387
slot_faction_political_party1_color_material_string = slot_faction_ve_mod_slots_begin + 388
slot_faction_political_party2_color_material_string = slot_faction_ve_mod_slots_begin + 389
slot_faction_political_party3_color_material_string = slot_faction_ve_mod_slots_begin + 390
slot_faction_political_party4_color_material_string = slot_faction_ve_mod_slots_begin + 391
slot_faction_law_balance_income_tax1 = slot_faction_ve_mod_slots_begin + 392
slot_faction_law_balance_importexport_tax1 = slot_faction_ve_mod_slots_begin + 393
slot_faction_law_balance_goodsservices_tax1 = slot_faction_ve_mod_slots_begin + 394
slot_faction_law_balance_income_tax2 = slot_faction_ve_mod_slots_begin + 395
slot_faction_law_balance_importexport_tax2 = slot_faction_ve_mod_slots_begin + 396
slot_faction_law_balance_goodsservices_tax2 = slot_faction_ve_mod_slots_begin + 397
slot_faction_law_balance_military_expenses = slot_faction_ve_mod_slots_begin + 398
slot_faction_law_balance_education_expenses = slot_faction_ve_mod_slots_begin + 399
slot_faction_law_balance_infrastructure_expenses = slot_faction_ve_mod_slots_begin + 400
slot_faction_law_balance_healthcare_expenses = slot_faction_ve_mod_slots_begin + 401
slot_faction_budget = slot_faction_ve_mod_slots_begin + 402
slot_faction_law_balance_state_expenses = slot_faction_ve_mod_slots_begin + 403
slot_faction_last_balance_change = slot_faction_ve_mod_slots_begin + 404
slot_faction_corruption_level = slot_faction_ve_mod_slots_begin + 405
slot_faction_last_balance_change_lost_from_corruption = slot_faction_ve_mod_slots_begin + 406
slot_faction_lmg =  slot_faction_ve_mod_slots_begin + 407
slot_faction_gasmask =  slot_faction_ve_mod_slots_begin + 408
slot_faction_troop_lineinf =  slot_faction_ve_mod_slots_begin + 409
slot_faction_troop_lightinf =  slot_faction_ve_mod_slots_begin + 410
slot_faction_troop_guardinf =  slot_faction_ve_mod_slots_begin + 411
slot_faction_troop_cav =  slot_faction_ve_mod_slots_begin + 412
slot_faction_is_cav_based =  slot_faction_ve_mod_slots_begin + 413
slot_faction_capital =  slot_faction_ve_mod_slots_begin + 414
slot_faction_pas_state =  slot_faction_ve_mod_slots_begin + 415
slot_faction_pas_center_target =  slot_faction_ve_mod_slots_begin + 416
slot_faction_pas_rank_infantry_string =  slot_faction_ve_mod_slots_begin + 417
slot_faction_pas_rank_cavalry_string =  slot_faction_ve_mod_slots_begin + 418
slot_faction_pas_player_rank =  slot_faction_ve_mod_slots_begin + 420
slot_faction_pas_player_points =  slot_faction_ve_mod_slots_begin + 421
slot_faction_mg_prop =  slot_faction_ve_mod_slots_begin + 422
slot_faction_mg_item =  slot_faction_ve_mod_slots_begin + 423
slot_faction_heavyhowitzer_cannoneer_officer =  slot_faction_ve_mod_slots_begin + 424
slot_faction_army_size =  slot_faction_ve_mod_slots_begin + 425
slot_faction_lordmodel_troop =  slot_faction_ve_mod_slots_begin + 426
slot_faction_extra_ammo_to_buy =  slot_faction_ve_mod_slots_begin + 427
slot_faction_extra_weaponry_to_buy =  slot_faction_ve_mod_slots_begin + 428
slot_faction_number_of_soldiers =  slot_faction_ve_mod_slots_begin + 429
slot_faction_number_of_lords =  slot_faction_ve_mod_slots_begin + 430
slot_faction_number_of_garrisons =  slot_faction_ve_mod_slots_begin + 431
slot_faction_number_of_soldiers =  slot_faction_ve_mod_slots_begin + 432
slot_faction_number_of_soldiers_lords =  slot_faction_ve_mod_slots_begin + 433
slot_faction_number_of_soldiers_garrisons =  slot_faction_ve_mod_slots_begin + 434



########################################################
##  PARTY SLOTS            #############################
########################################################
slot_party_type                = 0  #spt_caravan, spt_town, spt_castle

slot_party_retreat_flag        = 2
slot_party_ignore_player_until = 3
slot_party_ai_state            = 4
slot_party_ai_object           = 5
slot_party_ai_rationale        = 6 #Currently unused, but can be used to save a string explaining the lord's thinking

#slot_town_belongs_to_kingdom   = 6
slot_town_lord                 = 7
slot_party_ai_substate         = 8
slot_town_claimed_by_player    = 9

slot_cattle_driven_by_player = slot_town_lord #hack

slot_town_center        = 10
slot_town_castle        = 11
slot_town_prison        = 12
slot_town_tavern        = 13
slot_town_store         = 14
slot_town_arena         = 16
slot_town_alley         = 17
slot_town_walls         = 18
slot_center_culture     = 19

slot_town_tavernkeeper  = 20
slot_town_weaponsmith   = 21
slot_town_armorer       = 22
slot_town_merchant      = 23
slot_town_horse_merchant= 24
slot_town_elder         = 25
slot_center_player_relation = 26

slot_center_siege_with_belfry = 27
slot_center_last_taken_by_troop = 28

# party will follow this party if set:
slot_party_commander_party = 30 #default -1   #Deprecate
slot_party_following_player    = 31
slot_party_follow_player_until_time = 32
slot_party_dont_follow_player_until_time = 33

slot_village_raided_by        = 34
slot_village_state            = 35 #svs_normal, svs_being_raided, svs_looted, svs_recovering, svs_deserted
slot_village_raid_progress    = 36
slot_village_recover_progress = 37
slot_village_smoke_added      = 38

slot_village_infested_by_bandits   = 39

slot_center_last_visited_by_lord   = 41

slot_center_last_player_alarm_hour = 42

slot_village_player_can_not_steal_cattle = 46

slot_center_accumulated_rents      = 47 #collected automatically by NPC lords
slot_center_accumulated_tariffs    = 48 #collected automatically by NPC lords
slot_town_wealth        = 49 #total amount of accumulated wealth in the center, pays for the garrison
slot_town_prosperity    = 50 #affects the amount of wealth generated
slot_town_player_odds   = 51


slot_party_last_toll_paid_hours = 52
slot_party_food_store           = 53 #used for sieges
slot_center_is_besieged_by      = 54 #used for sieges
slot_center_last_spotted_enemy  = 55

slot_party_cached_strength        = 56
slot_party_nearby_friend_strength = 57
slot_party_nearby_enemy_strength  = 58
slot_party_follower_strength      = 59

slot_town_reinforcement_party_template = 60
slot_center_original_faction           = 61
slot_center_ex_faction                 = 62

slot_party_follow_me                   = 63
slot_center_siege_begin_hours          = 64 #used for sieges
slot_center_siege_hardness             = 65

slot_center_sortie_strength            = 66
slot_center_sortie_enemy_strength      = 67

slot_party_last_in_combat              = 68 #used for AI
slot_party_last_in_home_center         = 69 #used for AI
slot_party_leader_last_courted         = 70 #used for AI
slot_party_last_in_any_center          = 71 #used for AI



slot_castle_exterior    = slot_town_center

#slot_town_rebellion_contact   = 76
#trs_not_yet_approached  = 0
#trs_approached_before   = 1
#trs_approached_recently = 2

argument_none         = 0
argument_claim        = 1 #deprecate for legal
argument_legal        = 1

argument_ruler        = 2 #deprecate for commons
argument_commons      = 2

argument_benefit      = 3 #deprecate for reward
argument_reward       = 3 

argument_victory      = 4
argument_lords        = 5
argument_rivalries    = 6 #new - needs to be added

slot_town_village_product = 76

slot_town_rebellion_readiness = 77
#(readiness can be a negative number if the rebellion has been defeated)

slot_town_arena_melee_mission_tpl = 78
slot_town_arena_torny_mission_tpl = 79
slot_town_arena_melee_1_num_teams = 80
slot_town_arena_melee_1_team_size = 81
slot_town_arena_melee_2_num_teams = 82
slot_town_arena_melee_2_team_size = 83
slot_town_arena_melee_3_num_teams = 84
slot_town_arena_melee_3_team_size = 85
slot_town_arena_melee_cur_tier    = 86
##slot_town_arena_template	  = 87

slot_center_npc_volunteer_troop_type   = 90
slot_center_npc_volunteer_troop_amount = 91
slot_center_mercenary_troop_type  = 90
slot_center_mercenary_troop_amount= 91
slot_center_volunteer_troop_type  = 92
slot_center_volunteer_troop_amount= 93

#slot_center_companion_candidate   = 94
slot_center_ransom_broker         = 95
slot_center_tavern_traveler       = 96
slot_center_traveler_info_faction = 97
slot_center_tavern_bookseller     = 98
slot_center_tavern_minstrel       = 99

num_party_loot_slots    = 5
slot_party_next_looted_item_slot  = 109
slot_party_looted_item_1          = 110
slot_party_looted_item_2          = 111
slot_party_looted_item_3          = 112
slot_party_looted_item_4          = 113
slot_party_looted_item_5          = 114
slot_party_looted_item_1_modifier = 115
slot_party_looted_item_2_modifier = 116
slot_party_looted_item_3_modifier = 117
slot_party_looted_item_4_modifier = 118
slot_party_looted_item_5_modifier = 119

slot_village_bound_center         = 120
slot_village_market_town          = 121
slot_village_farmer_party         = 122
slot_party_home_center            = 123 #Only use with caravans and villagers

slot_center_current_improvement   = 124
slot_center_improvement_end_hour  = 125

slot_party_last_traded_center     = 126 



slot_center_has_manor            = 130 #village
slot_center_has_fish_pond        = 131 #village
slot_center_has_watch_tower      = 132 #village
slot_center_has_school           = 133 #village
slot_center_has_messenger_post   = 134 #town, castle, village
slot_center_has_prisoner_tower   = 135 #town, castle

village_improvements_begin = slot_center_has_manor
village_improvements_end          = 135

walled_center_improvements_begin = slot_center_has_messenger_post
walled_center_improvements_end               = 136

slot_center_player_enterprise     				  = 137 #noted with the item produced
slot_center_player_enterprise_production_order    = 138
slot_center_player_enterprise_consumption_order   = 139 #not used
slot_center_player_enterprise_days_until_complete = 139 #Used instead

slot_center_player_enterprise_balance             = 140 #not used
slot_center_player_enterprise_input_price         = 141 #not used
slot_center_player_enterprise_output_price        = 142 #not used

slot_center_closest_center1 = 140
slot_center_closest_center2 = 141
slot_center_closest_center3 = 142
slot_center_can_be_besieged_by_sea = 143
slot_center_official_faction = 144
slot_center_faction_to_assign = 145
slot_center_temp = 147

slot_center_has_bandits                        = 155
slot_town_has_tournament                       = 156
slot_town_tournament_max_teams                 = 157
slot_town_tournament_max_team_size             = 158

slot_center_faction_when_oath_renounced        = 159

slot_center_walker_0_troop                   = 160
slot_center_walker_1_troop                   = 161
slot_center_walker_2_troop                   = 162
slot_center_walker_3_troop                   = 163
slot_center_walker_4_troop                   = 164
slot_center_walker_5_troop                   = 165
slot_center_walker_6_troop                   = 166
slot_center_walker_7_troop                   = 167
slot_center_walker_8_troop                   = 168
slot_center_walker_9_troop                   = 169

slot_center_walker_0_dna                     = 170
slot_center_walker_1_dna                     = 171
slot_center_walker_2_dna                     = 172
slot_center_walker_3_dna                     = 173
slot_center_walker_4_dna                     = 174
slot_center_walker_5_dna                     = 175
slot_center_walker_6_dna                     = 176
slot_center_walker_7_dna                     = 177
slot_center_walker_8_dna                     = 178
slot_center_walker_9_dna                     = 179

slot_center_walker_0_type                    = 180
slot_center_walker_1_type                    = 181
slot_center_walker_2_type                    = 182
slot_center_walker_3_type                    = 183
slot_center_walker_4_type                    = 184
slot_center_walker_5_type                    = 185
slot_center_walker_6_type                    = 186
slot_center_walker_7_type                    = 187
slot_center_walker_8_type                    = 188
slot_center_walker_9_type                    = 189

slot_town_trade_route_1           = 190
slot_town_trade_route_2           = 191
slot_town_trade_route_3           = 192
slot_town_trade_route_4           = 193
slot_town_trade_route_5           = 194
slot_town_trade_route_6           = 195
slot_town_trade_route_7           = 196
slot_town_trade_route_8           = 197
slot_town_trade_route_9           = 198
slot_town_trade_route_10          = 199
slot_town_trade_route_11          = 200
slot_town_trade_route_12          = 201
slot_town_trade_route_13          = 202
slot_town_trade_route_14          = 203
slot_town_trade_route_15          = 204
slot_town_trade_routes_begin = slot_town_trade_route_1
slot_town_trade_routes_end = slot_town_trade_route_15 + 1


num_trade_goods = itm_siege_supply - itm_spice
slot_town_trade_good_productions_begin       = 500 #a harmless number, until it can be deprecated

#These affect production but in some cases also , so it is perhaps easier to itemize them than to have separate 

slot_village_number_of_cattle   = 205
slot_center_head_cattle         = 205 
slot_center_head_sheep			= 206 
slot_center_head_horses		 	= 207 

slot_center_acres_pasture       = 208 #pasture area for grazing of cattles and sheeps, if this value is high then number of cattles and sheeps increase faster
slot_production_sources_begin = 209
slot_center_acres_grain			= 209 #grain
slot_center_acres_olives        = 210 #olives
slot_center_acres_vineyard		= 211 #fruit
slot_center_acres_flax          = 212 #flax
slot_center_acres_dates			= 213 #dates

slot_center_fishing_fleet		= 214 #smoked fish
slot_center_salt_pans		    = 215 #salt

slot_center_apiaries       		= 216 #honey
slot_center_silk_farms			= 217 #silk
slot_center_kirmiz_farms		= 218 #dyes

slot_center_iron_deposits       = 219 #iron
slot_center_fur_traps			= 220 #furs

slot_center_mills				= 221 #bread
slot_center_breweries			= 222 #ale
slot_center_wine_presses		= 223 #wine
slot_center_olive_presses		= 224 #oil

slot_center_linen_looms			= 225 #linen
slot_center_silk_looms          = 226 #velvet
slot_center_wool_looms          = 227 #wool cloth

slot_center_pottery_kilns		= 228 #pottery
slot_center_smithies			= 229 #tools
slot_center_tanneries			= 230 #leatherwork
slot_center_shipyards			= 231 

slot_center_household_gardens   = 232 #cabbages
slot_production_sources_end = 233

#all spice comes overland to Tulga
#all dyes come by sea to Jelkala


slot_town_last_nearby_fire_time                         = 240

#slot_town_trade_good_prices_begin            = slot_town_trade_good_productions_begin + num_trade_goods + 1
slot_party_following_orders_of_troop        = 244
slot_party_orders_type				        = 245
slot_party_orders_object				    = 246
slot_party_orders_time				    	= 247

slot_party_temp_slot_1			            = 248 #right now used only within a single script, merchant_road_info_to_s42, to denote closed roads. Now also used in comparative scripts
slot_party_under_player_suggestion			= 249 #move this up a bit
slot_town_trade_good_prices_begin 			= 250

slot_center_last_reconnoitered_by_faction_time 				= 350
#slot_center_last_reconnoitered_by_faction_cached_strength 	= 360
#slot_center_last_reconnoitered_by_faction_friend_strength 	= 370

pes_slots_start = 400
slot_center_population = pes_slots_start + 1
slot_center_literacy = pes_slots_start + 2
slot_center_urbanization = pes_slots_start + 3
slot_center_workers = pes_slots_start + 4
slot_center_factory1_type = pes_slots_start + 5
slot_center_factory2_type = pes_slots_start + 6
slot_center_factory3_type = pes_slots_start + 7
slot_center_factory4_type = pes_slots_start + 8
slot_center_factory5_type = pes_slots_start + 9
slot_center_factory6_type = pes_slots_start + 10
slot_center_factory1_budget = pes_slots_start + 11
slot_center_factory2_budget = pes_slots_start + 12
slot_center_factory3_budget = pes_slots_start + 13
slot_center_factory4_budget = pes_slots_start + 14
slot_center_factory5_budget = pes_slots_start + 15
slot_center_factory6_budget = pes_slots_start + 16
slot_center_factory1_workers = pes_slots_start + 17
slot_center_factory2_workers = pes_slots_start + 18
slot_center_factory3_workers = pes_slots_start + 19
slot_center_factory4_workers = pes_slots_start + 20
slot_center_factory5_workers = pes_slots_start + 21
slot_center_factory6_workers = pes_slots_start + 22
slot_center_factory1_resource_amount = pes_slots_start + 23
slot_center_factory2_resource_amount = pes_slots_start + 24
slot_center_factory3_resource_amount = pes_slots_start + 25
slot_center_factory4_resource_amount = pes_slots_start + 26
slot_center_factory5_resource_amount = pes_slots_start + 27
slot_center_factory6_resource_amount = pes_slots_start + 28
slot_center_factory1_resource_quality = pes_slots_start + 29
slot_center_factory2_resource_quality = pes_slots_start + 30
slot_center_factory3_resource_quality = pes_slots_start + 31
slot_center_factory4_resource_quality = pes_slots_start + 32
slot_center_factory5_resource_quality = pes_slots_start + 33
slot_center_factory6_resource_quality = pes_slots_start + 34
slot_center_factory1_machine_tools_quality = pes_slots_start + 35
slot_center_factory2_machine_tools_quality = pes_slots_start + 36
slot_center_factory3_machine_tools_quality = pes_slots_start + 37
slot_center_factory4_machine_tools_quality = pes_slots_start + 38
slot_center_factory5_machine_tools_quality = pes_slots_start + 39
slot_center_factory6_machine_tools_quality = pes_slots_start + 40
slot_center_iron_amount = pes_slots_start + 41
slot_center_coal_amount = pes_slots_start + 42
slot_center_meat_amount = pes_slots_start + 43
slot_center_cotton_amount = pes_slots_start + 44
slot_center_flour_amount = pes_slots_start + 45
slot_center_wood_amount = pes_slots_start + 46
slot_center_villages_machine_tools_quality = pes_slots_start + 47
slot_center_factory1_max_workers = pes_slots_start + 48
slot_center_factory2_max_workers = pes_slots_start + 49
slot_center_factory3_max_workers = pes_slots_start + 50
slot_center_factory4_max_workers = pes_slots_start + 51
slot_center_factory5_max_workers = pes_slots_start + 52
slot_center_factory6_max_workers = pes_slots_start + 53
slot_center_villages_resource_bonus_type = pes_slots_start + 54
slot_center_villages_production_size = pes_slots_start + 55
slot_center_villages_budget = pes_slots_start + 56
slot_center_factory1_income = pes_slots_start + 57
slot_center_factory2_income = pes_slots_start + 58
slot_center_factory3_income = pes_slots_start + 59
slot_center_factory4_income = pes_slots_start + 60
slot_center_factory5_income = pes_slots_start + 61
slot_center_factory6_income = pes_slots_start + 62
slot_center_factory1_spentlastday1 = pes_slots_start + 63
slot_center_factory2_spentlastday1 = pes_slots_start + 64
slot_center_factory3_spentlastday1 = pes_slots_start + 65
slot_center_factory4_spentlastday1 = pes_slots_start + 66
slot_center_factory5_spentlastday1 = pes_slots_start + 67
slot_center_factory6_spentlastday1 = pes_slots_start + 68
slot_center_factory1_earntlastday1 = pes_slots_start + 69
slot_center_factory2_earntlastday1 = pes_slots_start + 70
slot_center_factory3_earntlastday1 = pes_slots_start + 71
slot_center_factory4_earntlastday1 = pes_slots_start + 72
slot_center_factory5_earntlastday1 = pes_slots_start + 73
slot_center_factory6_earntlastday1 = pes_slots_start + 74
slot_center_factory1_spentlastday2 = pes_slots_start + 75
slot_center_factory2_spentlastday2 = pes_slots_start + 76
slot_center_factory3_spentlastday2 = pes_slots_start + 77
slot_center_factory4_spentlastday2 = pes_slots_start + 78
slot_center_factory5_spentlastday2 = pes_slots_start + 79
slot_center_factory6_spentlastday2 = pes_slots_start + 80
slot_center_factory1_earntlastday2 = pes_slots_start + 81
slot_center_factory2_earntlastday2 = pes_slots_start + 82
slot_center_factory3_earntlastday2 = pes_slots_start + 83
slot_center_factory4_earntlastday2 = pes_slots_start + 84
slot_center_factory5_earntlastday2 = pes_slots_start + 85
slot_center_factory6_earntlastday2 = pes_slots_start + 86
slot_center_factory1_producedduringday = pes_slots_start + 87
slot_center_factory2_producedduringday = pes_slots_start + 88
slot_center_factory3_producedduringday = pes_slots_start + 89
slot_center_factory4_producedduringday = pes_slots_start + 90
slot_center_factory5_producedduringday = pes_slots_start + 91
slot_center_factory6_producedduringday = pes_slots_start + 92
slot_center_factory1_soldpercent = pes_slots_start + 93
slot_center_factory2_soldpercent = pes_slots_start + 94
slot_center_factory3_soldpercent = pes_slots_start + 95
slot_center_factory4_soldpercent = pes_slots_start + 96
slot_center_factory5_soldpercent = pes_slots_start + 97
slot_center_factory6_soldpercent = pes_slots_start + 98
slot_center_factory1_found_raw_resources1 = pes_slots_start + 99
slot_center_factory2_found_raw_resources1 = pes_slots_start + 100
slot_center_factory3_found_raw_resources1 = pes_slots_start + 101
slot_center_factory4_found_raw_resources1 = pes_slots_start + 102
slot_center_factory5_found_raw_resources1 = pes_slots_start + 103
slot_center_factory6_found_raw_resources1 = pes_slots_start + 104
slot_center_factory1_producedlastday = pes_slots_start + 105
slot_center_factory2_producedlastday = pes_slots_start + 106
slot_center_factory3_producedlastday = pes_slots_start + 107
slot_center_factory4_producedlastday = pes_slots_start + 108
slot_center_factory5_producedlastday = pes_slots_start + 109
slot_center_factory6_producedlastday = pes_slots_start + 110
slot_center_factory1_spentlastday3 = pes_slots_start + 111
slot_center_factory2_spentlastday3 = pes_slots_start + 112
slot_center_factory3_spentlastday3 = pes_slots_start + 113
slot_center_factory4_spentlastday3 = pes_slots_start + 114
slot_center_factory5_spentlastday3 = pes_slots_start + 115
slot_center_factory6_spentlastday3 = pes_slots_start + 116
slot_center_factory1_found_raw_resources2 = pes_slots_start + 117
slot_center_factory2_found_raw_resources2 = pes_slots_start + 118
slot_center_factory3_found_raw_resources2 = pes_slots_start + 119
slot_center_factory4_found_raw_resources2 = pes_slots_start + 120
slot_center_factory5_found_raw_resources2 = pes_slots_start + 121
slot_center_factory6_found_raw_resources2 = pes_slots_start + 122
slot_center_factory1_playershare = pes_slots_start + 123
slot_center_factory2_playershare = pes_slots_start + 124
slot_center_factory3_playershare = pes_slots_start + 125
slot_center_factory4_playershare = pes_slots_start + 126
slot_center_factory5_playershare = pes_slots_start + 127
slot_center_factory6_playershare = pes_slots_start + 128
slot_center_factory1_devmode = pes_slots_start + 129
slot_center_factory2_devmode = pes_slots_start + 130
slot_center_factory3_devmode = pes_slots_start + 131
slot_center_factory4_devmode = pes_slots_start + 132
slot_center_factory5_devmode = pes_slots_start + 133
slot_center_factory6_devmode = pes_slots_start + 134
slot_center_factory1_workers_wage = pes_slots_start + 135
slot_center_factory2_workers_wage = pes_slots_start + 136
slot_center_factory3_workers_wage = pes_slots_start + 137
slot_center_factory4_workers_wage = pes_slots_start + 138
slot_center_factory5_workers_wage = pes_slots_start + 139
slot_center_factory6_workers_wage = pes_slots_start + 140
slot_center_factory1_workers_conditions = pes_slots_start + 141
slot_center_factory2_workers_conditions = pes_slots_start + 142
slot_center_factory3_workers_conditions = pes_slots_start + 143
slot_center_factory4_workers_conditions = pes_slots_start + 144
slot_center_factory5_workers_conditions = pes_slots_start + 145
slot_center_factory6_workers_conditions = pes_slots_start + 146
slot_center_factory1_price = pes_slots_start + 147
slot_center_factory2_price = pes_slots_start + 148
slot_center_factory3_price = pes_slots_start + 149
slot_center_factory4_price = pes_slots_start + 150
slot_center_factory5_price = pes_slots_start + 151
slot_center_factory6_price = pes_slots_start + 152
slot_center_factory1_machine_tools_deterioration = pes_slots_start + 153
slot_center_factory2_machine_tools_deterioration = pes_slots_start + 154
slot_center_factory3_machine_tools_deterioration = pes_slots_start + 155
slot_center_factory4_machine_tools_deterioration = pes_slots_start + 156
slot_center_factory5_machine_tools_deterioration = pes_slots_start + 157
slot_center_factory6_machine_tools_deterioration = pes_slots_start + 158
slot_center_workers_handicraft = pes_slots_start + 159
slot_center_workers_massproduction = pes_slots_start + 160
slot_center_gdp1 = pes_slots_start + 161
slot_center_gdp2 = pes_slots_start + 162
slot_center_factory1_building_type = pes_slots_start + 163
slot_center_factory2_building_type = pes_slots_start + 164
slot_center_factory3_building_type = pes_slots_start + 165
slot_center_factory4_building_type = pes_slots_start + 166
slot_center_factory5_building_type = pes_slots_start + 167
slot_center_factory6_building_type = pes_slots_start + 168
slot_center_factory1_building_progress = pes_slots_start + 169
slot_center_factory2_building_progress = pes_slots_start + 170
slot_center_factory3_building_progress = pes_slots_start + 171
slot_center_factory4_building_progress = pes_slots_start + 172
slot_center_factory5_building_progress = pes_slots_start + 173
slot_center_factory6_building_progress = pes_slots_start + 174
slot_center_cotton_production_size = pes_slots_start + 175
slot_center_gdp_rural1 = pes_slots_start + 176
slot_center_gdp_rural2 = pes_slots_start + 177
slot_center_gdp_urban1 = pes_slots_start + 178
slot_center_gdp_urban2 = pes_slots_start + 179
slot_party_size_bonus = pes_slots_start + 180
slot_party_pas_lord_state = pes_slots_start + 181
slot_party_pas_center_target = pes_slots_start + 182
slot_party_pas_timer = pes_slots_start + 183

#slot_party_type values
##spt_caravan            = 1
spt_castle             = 2
spt_town               = 3
spt_village            = 4
##spt_forager            = 5
##spt_war_party          = 6
spt_patrol             = 7
##spt_messenger          = 8
##spt_raider             = 9
##spt_scout              = 10
spt_kingdom_caravan    = 11
##spt_prisoner_train     = 12
spt_kingdom_hero_party = 13
##spt_merchant_caravan   = 14
spt_village_farmer     = 15
spt_ship               = 16
spt_cattle_herd        = 17
spt_bandit_lair       = 18
#spt_deserter           = 20

kingdom_party_types_begin = spt_kingdom_caravan
kingdom_party_types_end = spt_kingdom_hero_party + 1

#slot_faction_state values
sfs_active                     = 0
sfs_defeated                   = 1
sfs_inactive                   = 2
sfs_inactive_rebellion         = 3
sfs_beginning_rebellion        = 4


#slot_faction_ai_state values
sfai_default                   		 = 0 #also defending
sfai_gathering_army            		 = 1
sfai_attacking_center          		 = 2
sfai_raiding_village           		 = 3
sfai_attacking_enemy_army      		 = 4
sfai_attacking_enemies_around_center = 5
sfai_feast             		 		 = 6 #can be feast, wedding, or major tournament
#Social events are a generic aristocratic gathering. Tournaments take place if they are in a town, and hunts take place if they are at a castle.
#Weddings will take place at social events between betrothed couples if they have been engaged for at least a month, if the lady's guardian is the town lord, and if both bride and groom are present


#Rebellion system changes begin
sfai_nascent_rebellion          = 7
#Rebellion system changes end

#slot_party_ai_state values
spai_undefined                  = -1
spai_besieging_center           = 1
spai_patrolling_around_center   = 4
spai_raiding_around_center      = 5
##spai_raiding_village            = 6
spai_holding_center             = 7
##spai_helping_town_against_siege = 9
spai_engaging_army              = 10
spai_accompanying_army          = 11
spai_screening_army             = 12
spai_trading_with_town          = 13
spai_retreating_to_center       = 14
##spai_trading_within_kingdom     = 15
spai_visiting_village           = 16 #same thing, I think. Recruiting differs from holding because NPC parties don't actually enter villages

#slot_village_state values
svs_normal                      = 0
svs_being_raided                = 1
svs_looted                      = 2
svs_recovering                  = 3
svs_deserted                    = 4
svs_under_siege                 = 5

#$g_player_icon_state values
pis_normal                      = 0
pis_camping                     = 1
pis_ship                        = 2


########################################################
##  SCENE SLOTS            #############################
########################################################
slot_scene_visited               = 0
#INVASION MODE START
slot_scene_ccoop_disallow_horses = 1 #should be set to 1 for scenes that should be played dismounted in Invasion mode (e.g. Forest Hideout)
#INVASION MODE END
slot_scene_belfry_props_begin    = 10



########################################################
##  TROOP SLOTS            #############################
########################################################
#slot_troop_role         = 0  # 10=Kingdom Lord

slot_troop_occupation          = 2  # 0 = free, 1 = merchant
#slot_troop_duty               = 3  # Kingdom duty, 0 = free
#slot_troop_homage_type         = 45
#homage_mercenary =             = 1 #Player is on a temporary contract
#homage_official =              = 2 #Player has a royal appointment
#homage_feudal   =              = 3 #


slot_troop_state               = 3  
slot_troop_last_talk_time      = 4
slot_troop_met                 = 5 #i also use this for the courtship state -- may become cumbersome
slot_troop_courtship_state     = 5 #2 professed admiration, 3 agreed to seek a marriage, 4 ended relationship

slot_troop_party_template      = 6
#slot_troop_kingdom_rank        = 7

slot_troop_renown              = 7

##slot_troop_is_prisoner         = 8  # important for heroes only
slot_troop_prisoner_of_party   = 8  # important for heroes only
#slot_troop_is_player_companion = 9  # important for heroes only:::USE  slot_troop_occupation = slto_player_companion

slot_troop_present_at_event    = 9

slot_troop_leaded_party         = 10 # important for kingdom heroes only
slot_troop_wealth               = 11 # important for kingdom heroes only
slot_troop_cur_center           = 12 # important for royal family members only (non-kingdom heroes)

slot_troop_banner_scene_prop    = 13 # important for kingdom heroes and player only

slot_troop_original_faction     = 14 # for pretenders
#slot_troop_loyalty              = 15 #deprecated - this is now derived from other figures
slot_troop_player_order_state   = 16 #Deprecated
slot_troop_player_order_object  = 17 #Deprecated

#troop_player order state are all deprecated in favor of party_order_state. This has two reasons -- 1) to reset AI if the party is eliminated, and 2) to allow the player at a later date to give orders to leaderless parties, if we want that


#Post 0907 changes begin
slot_troop_age                 =  18
slot_troop_age_appearance      =  19

#Post 0907 changes end

slot_troop_does_not_give_quest = 20
slot_troop_player_debt         = 21
slot_troop_player_relation     = 22
#slot_troop_player_favor        = 23
slot_troop_last_quest          = 24
slot_troop_last_quest_betrayed = 25
slot_troop_last_persuasion_time= 26
slot_troop_last_comment_time   = 27
slot_troop_spawned_before      = 28

#Post 0907 changes begin
slot_troop_last_comment_slot   = 29
#Post 0907 changes end

slot_troop_spouse              = 30
slot_troop_father              = 31
slot_troop_mother              = 32
slot_troop_guardian            = 33 #Usually siblings are identified by a common parent.This is used for brothers if the father is not an active npc. At some point we might introduce geneologies
slot_troop_betrothed           = 34 #Obviously superseded once slot_troop_spouse is filled
#other relations are derived from one's parents 
#slot_troop_daughter            = 33
#slot_troop_son                 = 34
#slot_troop_sibling             = 35
slot_troop_love_interest_1     = 35 #each unmarried lord has three love interests
slot_troop_love_interest_2     = 36
slot_troop_love_interest_3     = 37
slot_troop_love_interests_end  = 38
#ways to court -- discuss a book, commission/compose a poem, present a gift, recount your exploits, fulfil a specific quest, appear at a tournament
#preferences for women - (conventional - father's friends)
slot_lady_no_messages          				= 37
slot_lady_last_suitor          				= 38
slot_lord_granted_courtship_permission      = 38

slot_troop_betrothal_time                   = 39 #used in scheduling the wedding

slot_troop_trainer_met                       = 30
slot_troop_trainer_waiting_for_result        = 31
slot_troop_trainer_training_fight_won        = 32
slot_troop_trainer_num_opponents_to_beat     = 33
slot_troop_trainer_training_system_explained = 34
slot_troop_trainer_opponent_troop            = 35
slot_troop_trainer_training_difficulty       = 36
slot_troop_trainer_training_fight_won        = 37


slot_lady_used_tournament					= 40


slot_troop_current_rumor       = 45
slot_troop_temp_slot           = 46
slot_troop_promised_fief       = 47

slot_troop_set_decision_seed       = 48 #Does not change
slot_troop_temp_decision_seed      = 49 #Resets at recalculate_ai
slot_troop_recruitment_random      = 50 #used in a number of different places in the intrigue procedures to overcome intermediate hurdles, although not for the final calculation, might be replaced at some point by the global decision seed
#Decision seeds can be used so that some randomness can be added to NPC decisions, without allowing the player to spam the NPC with suggestions
#The temp decision seed is reset 24 to 48 hours after the NPC last spoke to the player, while the set seed only changes in special occasions
#The single seed is used with varying modula to give high/low outcomes on different issues, without using a separate slot for each issue

slot_troop_intrigue_impatience = 51
#recruitment changes end

#slot_troop_honorable          = 50
#slot_troop_merciful          = 51
slot_lord_reputation_type     		  = 52
slot_lord_recruitment_argument        = 53 #the last argument proposed by the player to the lord
slot_lord_recruitment_candidate       = 54 #the last candidate proposed by the player to the lord

slot_troop_change_to_faction          = 55

#slot_troop_readiness_to_join_army     = 57 #possibly deprecate
#slot_troop_readiness_to_follow_orders = 58 #possibly deprecate

# NPC-related constants

#NPC companion changes begin
slot_troop_first_encountered          = 59
slot_troop_home                       = 60

slot_troop_morality_state       = 61
tms_no_problem         = 0
tms_acknowledged       = 1
tms_dismissed          = 2

slot_troop_morality_type = 62
tmt_aristocratic = 1
tmt_egalitarian = 2
tmt_humanitarian = 3
tmt_honest = 4
tmt_pious = 5

slot_troop_morality_value = 63

slot_troop_2ary_morality_type  = 64
slot_troop_2ary_morality_state = 65
slot_troop_2ary_morality_value = 66

slot_troop_town_with_contacts  = 67
slot_troop_town_contact_type   = 68 #1 are nobles, 2 are commons

slot_troop_morality_penalties =  69 ### accumulated grievances from morality conflicts


slot_troop_personalityclash_object     = 71
#(0 - they have no problem, 1 - they have a problem)
slot_troop_personalityclash_state    = 72 #1 = pclash_penalty_to_self, 2 = pclash_penalty_to_other, 3 = pclash_penalty_to_other,
pclash_penalty_to_self  = 1
pclash_penalty_to_other = 2
pclash_penalty_to_both  = 3
#(a string)
slot_troop_personalityclash2_object   = 73
slot_troop_personalityclash2_state    = 74

slot_troop_personalitymatch_object   =  75
slot_troop_personalitymatch_state   =  76

slot_troop_personalityclash_penalties = 77 ### accumulated grievances from personality clash
slot_troop_personalityclash_penalties = 77 ### accumulated grievances from personality clash

slot_troop_home_speech_delivered = 78 #only for companions
slot_troop_discussed_rebellion   = 78 #only for pretenders

#courtship slots
slot_lady_courtship_heroic_recited 	    = 74
slot_lady_courtship_allegoric_recited 	= 75
slot_lady_courtship_comic_recited 		= 76
slot_lady_courtship_mystic_recited 		= 77
slot_lady_courtship_tragic_recited 		= 78



#NPC history slots
slot_troop_met_previously        = 80
slot_troop_turned_down_twice     = 81
slot_troop_playerparty_history   = 82

pp_history_scattered         = 1
pp_history_dismissed         = 2
pp_history_quit              = 3
pp_history_indeterminate     = 4

slot_troop_playerparty_history_string   = 83
slot_troop_return_renown        = 84

slot_troop_custom_banner_bg_color_1      = 85
slot_troop_custom_banner_bg_color_2      = 86
slot_troop_custom_banner_charge_color_1  = 87
slot_troop_custom_banner_charge_color_2  = 88
slot_troop_custom_banner_charge_color_3  = 89
slot_troop_custom_banner_charge_color_4  = 90
slot_troop_custom_banner_bg_type         = 91
slot_troop_custom_banner_charge_type_1   = 92
slot_troop_custom_banner_charge_type_2   = 93
slot_troop_custom_banner_charge_type_3   = 94
slot_troop_custom_banner_charge_type_4   = 95
slot_troop_custom_banner_flag_type       = 96
slot_troop_custom_banner_num_charges     = 97
slot_troop_custom_banner_positioning     = 98
slot_troop_custom_banner_map_flag_type   = 99

#conversation strings -- must be in this order!
slot_troop_intro 						= 101
slot_troop_intro_response_1 			= 102
slot_troop_intro_response_2 			= 103
slot_troop_backstory_a 					= 104
slot_troop_backstory_b 					= 105
slot_troop_backstory_c 					= 106
slot_troop_backstory_delayed 			= 107
slot_troop_backstory_response_1 		= 108
slot_troop_backstory_response_2 		= 109
slot_troop_signup   					= 110
slot_troop_signup_2 					= 111
slot_troop_signup_response_1 			= 112
slot_troop_signup_response_2 			= 113
slot_troop_mentions_payment 			= 114 #Not actually used
slot_troop_payment_response 			= 115 #Not actually used
slot_troop_morality_speech   			= 116
slot_troop_2ary_morality_speech 		= 117
slot_troop_personalityclash_speech 		= 118
slot_troop_personalityclash_speech_b 	= 119
slot_troop_personalityclash2_speech 	= 120
slot_troop_personalityclash2_speech_b 	= 121
slot_troop_personalitymatch_speech 		= 122
slot_troop_personalitymatch_speech_b 	= 123
slot_troop_retirement_speech 			= 124
slot_troop_rehire_speech 				= 125
slot_troop_home_intro           		= 126
slot_troop_home_description    			= 127
slot_troop_home_description_2 			= 128
slot_troop_home_recap         			= 129
slot_troop_honorific   					= 130
slot_troop_kingsupport_string_1			= 131
slot_troop_kingsupport_string_2			= 132
slot_troop_kingsupport_string_2a		= 133
slot_troop_kingsupport_string_2b		= 134
slot_troop_kingsupport_string_3			= 135
slot_troop_kingsupport_objection_string	= 136
slot_troop_intel_gathering_string	    = 137
slot_troop_fief_acceptance_string	    = 138
slot_troop_woman_to_woman_string	    = 139
slot_troop_turn_against_string	        = 140

slot_troop_strings_end 					= 141

slot_troop_payment_request 				= 141

#141, support base removed, slot now available

slot_troop_kingsupport_state			= 142
slot_troop_kingsupport_argument			= 143
slot_troop_kingsupport_opponent			= 144
slot_troop_kingsupport_objection_state  = 145 #0, default, 1, needs to voice, 2, has voiced

slot_troop_days_on_mission		        = 150
slot_troop_current_mission			    = 151
slot_troop_mission_object               = 152
npc_mission_kingsupport					= 1
npc_mission_gather_intel                = 2
npc_mission_peace_request               = 3
npc_mission_pledge_vassal               = 4
npc_mission_seek_recognition            = 5
npc_mission_test_waters                 = 6
npc_mission_non_aggression              = 7
npc_mission_rejoin_when_possible        = 8

#Number of routed agents after battle ends.
slot_troop_player_routed_agents                 = 146
slot_troop_ally_routed_agents                   = 147
slot_troop_enemy_routed_agents                  = 148

#Special quest slots
slot_troop_mission_participation        = 149
mp_unaware                              = 0 
mp_stay_out                             = 1 
mp_prison_break_fight                   = 2 
mp_prison_break_stand_back              = 3 
mp_prison_break_escaped                 = 4 
mp_prison_break_caught                  = 5 

#Below are some constants to expand the political system a bit. The idea is to make quarrels less random, but instead make them serve a rational purpose -- as a disincentive to lords to seek 

slot_troop_controversy                     = 150 #Determines whether or not a troop is likely to receive fief or marshalship
slot_troop_recent_offense_type 	           = 151 #failure to join army, failure to support colleague
slot_troop_recent_offense_object           = 152 #to whom it happened
slot_troop_recent_offense_time             = 153
slot_troop_stance_on_faction_issue         = 154 #when it happened
#INVASION MODE START
slot_troop_coop_lord_spawned               = 155 #used to keep track of lords spawning in Invasion mode
slot_troop_mp_squad_type                   = 156 #used while generating waves for Invasion mode
#INVASION MODE END

tro_failed_to_join_army                    = 1
tro_failed_to_support_colleague            = 2

#CONTROVERSY
#This is used to create a more "rational choice" model of faction politics, in which lords pick fights with other lords for gain, rather than simply because of clashing personalities
#It is intended to be a limiting factor for players and lords in their ability to intrigue against each other. It represents the embroilment of a lord in internal factional disputes. In contemporary media English, a lord with high "controversy" would be described as "embattled."
#The main effect of high controversy is that it disqualifies a lord from receiving a fief or an appointment
#It is a key political concept because it provides incentive for much of the political activity. For example, Lord Red Senior is worried that his rival, Lord Blue Senior, is going to get a fied which Lord Red wants. So, Lord Red turns to his protege, Lord Orange Junior, to attack Lord Blue in public. The fief goes to Lord Red instead of Lord Blue, and Lord Red helps Lord Orange at a later date.


slot_troop_will_join_prison_break      = 161


troop_slots_reserved_for_relations_start        = 165 #this is based on id_troops, and might change

slot_troop_relations_begin				= 0 #this creates an array for relations between troops
											#Right now, lords start at 165 and run to around 290, including pretenders
											
											
											
########################################################
##  PLAYER SLOTS           #############################
########################################################

slot_player_spawned_this_round                 = 0
slot_player_last_rounds_used_item_earnings     = 1
slot_player_selected_item_indices_begin        = 2
slot_player_selected_item_indices_end          = 11
slot_player_cur_selected_item_indices_begin    = slot_player_selected_item_indices_end
slot_player_cur_selected_item_indices_end      = slot_player_selected_item_indices_end + 9
slot_player_join_time                          = 21
slot_player_button_index                       = 22 #used for presentations
slot_player_can_answer_poll                    = 23
slot_player_first_spawn                        = 24
slot_player_spawned_at_siege_round             = 25
slot_player_poll_disabled_until_time           = 26
slot_player_total_equipment_value              = 27
slot_player_last_team_select_time              = 28
slot_player_death_pos_x                        = 29
slot_player_death_pos_y                        = 30
slot_player_death_pos_z                        = 31
slot_player_damage_given_to_target_1           = 32 #used only in destroy mod
slot_player_damage_given_to_target_2           = 33 #used only in destroy mod
slot_player_last_bot_count                     = 34
slot_player_bot_type_1_wanted                  = 35
slot_player_bot_type_2_wanted                  = 36
slot_player_bot_type_3_wanted                  = 37
slot_player_bot_type_4_wanted                  = 38
slot_player_spawn_count                        = 39
#INVASION MODE START
slot_player_ccoop_drop_item_1                  = 40
slot_player_ccoop_drop_item_2                  = 41
slot_player_companion_ids_locked               = 42
slot_player_companion_ids_begin                = 43
slot_player_companion_ids_end                  = slot_player_companion_ids_begin + 2 # there are 2 companions for each player
slot_player_companion_classes_begin            = slot_player_companion_ids_end
slot_player_companion_classes_end              = slot_player_companion_classes_begin + 2
slot_player_companion_levels_begin             = slot_player_companion_classes_end
slot_player_companion_levels_end               = slot_player_companion_levels_begin + 2
slot_player_coop_dropped_item                  = slot_player_companion_levels_end
slot_player_coop_opened_chests_begin           = slot_player_coop_dropped_item + 1
slot_player_coop_opened_chests_end             = slot_player_coop_opened_chests_begin + 10
#INVASION MODE END

########################################################
##  TEAM SLOTS             #############################
########################################################

slot_team_flag_situation                       = 0
slot_team_battle_started                       = 0

slot_team_company1_type                       = 1
slot_team_company2_type                       = 2
slot_team_company3_type                       = 3
slot_team_company4_type                       = 4
slot_team_company5_type                       = 5
slot_team_company6_type                       = 6
slot_team_company7_type                       = 7
slot_team_company8_type                       = 8

slot_team_company_assignment_order_number     = 9

slot_team_company1_energy                       = 18
slot_team_company2_energy                       = 19
slot_team_company3_energy                       = 20
slot_team_company4_energy                       = 21
slot_team_company5_energy                       = 22
slot_team_company6_energy                       = 23
slot_team_company7_energy                       = 24
slot_team_company8_energy                       = 25
slot_team_company1_run_mode                       = 26
slot_team_company2_run_mode                       = 27
slot_team_company3_run_mode                       = 28
slot_team_company4_run_mode                       = 29
slot_team_company5_run_mode                       = 30
slot_team_company6_run_mode                       = 31
slot_team_company7_run_mode                       = 32
slot_team_company8_run_mode                       = 33
slot_team_company1_soldier_number                       = 34
slot_team_company2_soldier_number                       = 35
slot_team_company3_soldier_number                       = 36
slot_team_company4_soldier_number                       = 37
slot_team_company5_soldier_number                       = 38
slot_team_company6_soldier_number                       = 39
slot_team_company7_soldier_number                       = 40
slot_team_company8_soldier_number                       = 41
slot_team_company1_moving_soldier_number                       = 42
slot_team_company2_moving_soldier_number                       = 43
slot_team_company3_moving_soldier_number                       = 44
slot_team_company4_moving_soldier_number                       = 45
slot_team_company5_moving_soldier_number                       = 46
slot_team_company6_moving_soldier_number                       = 47
slot_team_company7_moving_soldier_number                       = 48
slot_team_company8_moving_soldier_number                       = 49

slot_team_pai_global_tactic                       = 50
slot_team_pai_timer                               = 51

slot_team_company1_penaltytodiscipline_fromfire                       = 52
slot_team_company2_penaltytodiscipline_fromfire                       = 53
slot_team_company3_penaltytodiscipline_fromfire                       = 54
slot_team_company4_penaltytodiscipline_fromfire                       = 55
slot_team_company5_penaltytodiscipline_fromfire                       = 56
slot_team_company6_penaltytodiscipline_fromfire                       = 57
slot_team_company7_penaltytodiscipline_fromfire                       = 58
slot_team_company8_penaltytodiscipline_fromfire                       = 59
slot_team_company1_penaltytodiscipline_fromcloseenemy                       = 60
slot_team_company2_penaltytodiscipline_fromcloseenemy                       = 61
slot_team_company3_penaltytodiscipline_fromcloseenemy                       = 62
slot_team_company4_penaltytodiscipline_fromcloseenemy                       = 63
slot_team_company5_penaltytodiscipline_fromcloseenemy                       = 64
slot_team_company6_penaltytodiscipline_fromcloseenemy                       = 65
slot_team_company7_penaltytodiscipline_fromcloseenemy                       = 66
slot_team_company8_penaltytodiscipline_fromcloseenemy                       = 67
slot_team_company1_guards_number                       = 68
slot_team_company2_guards_number                       = 69
slot_team_company3_guards_number                       = 70
slot_team_company4_guards_number                       = 71
slot_team_company5_guards_number                       = 72
slot_team_company6_guards_number                       = 73
slot_team_company7_guards_number                       = 74
slot_team_company8_guards_number                       = 75
slot_team_company1_state                       = 76
slot_team_company2_state                       = 77
slot_team_company3_state                       = 78
slot_team_company4_state                       = 79
slot_team_company5_state                       = 80
slot_team_company6_state                       = 81
slot_team_company7_state                       = 82
slot_team_company8_state                       = 83
slot_team_company1_timer                       = 84
slot_team_company2_timer                       = 85
slot_team_company3_timer                       = 86
slot_team_company4_timer                       = 87
slot_team_company5_timer                       = 88
slot_team_company6_timer                       = 89
slot_team_company7_timer                       = 90
slot_team_company8_timer                       = 91
slot_team_company1_reloading_soldier_number                       = 92
slot_team_company2_reloading_soldier_number                       = 93
slot_team_company3_reloading_soldier_number                       = 94
slot_team_company4_reloading_soldier_number                       = 95
slot_team_company5_reloading_soldier_number                       = 96
slot_team_company6_reloading_soldier_number                       = 97
slot_team_company7_reloading_soldier_number                       = 98
slot_team_company8_reloading_soldier_number                       = 99
slot_team_company1_average_x                       = 100
slot_team_company2_average_x                       = 101
slot_team_company3_average_x                       = 102
slot_team_company4_average_x                       = 103
slot_team_company5_average_x                       = 104
slot_team_company6_average_x                       = 105
slot_team_company7_average_x                       = 106
slot_team_company8_average_x                       = 107
slot_team_company1_average_y                       = 108
slot_team_company2_average_y                       = 109
slot_team_company3_average_y                       = 110
slot_team_company4_average_y                       = 111
slot_team_company5_average_y                       = 112
slot_team_company6_average_y                       = 113
slot_team_company7_average_y                       = 114
slot_team_company8_average_y                       = 115
slot_team_company1_average_z_rot                       = 116
slot_team_company2_average_z_rot                       = 117
slot_team_company3_average_z_rot                       = 118
slot_team_company4_average_z_rot                       = 119
slot_team_company5_average_z_rot                       = 120
slot_team_company6_average_z_rot                       = 121
slot_team_company7_average_z_rot                       = 122
slot_team_company8_average_z_rot                       = 123
slot_team_company1_hold_order_x                       = 124
slot_team_company2_hold_order_x                       = 125
slot_team_company3_hold_order_x                       = 126
slot_team_company4_hold_order_x                       = 127
slot_team_company5_hold_order_x                       = 128
slot_team_company6_hold_order_x                       = 129
slot_team_company7_hold_order_x                       = 130
slot_team_company8_hold_order_x                       = 131
slot_team_company1_hold_order_y                       = 132
slot_team_company2_hold_order_y                       = 133
slot_team_company3_hold_order_y                       = 134
slot_team_company4_hold_order_y                       = 135
slot_team_company5_hold_order_y                       = 136
slot_team_company6_hold_order_y                       = 137
slot_team_company7_hold_order_y                       = 138
slot_team_company8_hold_order_y                       = 139
slot_team_company1_hold_order_z_rot                       = 140
slot_team_company2_hold_order_z_rot                       = 141
slot_team_company3_hold_order_z_rot                       = 142
slot_team_company4_hold_order_z_rot                       = 143
slot_team_company5_hold_order_z_rot                       = 144
slot_team_company6_hold_order_z_rot                       = 145
slot_team_company7_hold_order_z_rot                       = 146
slot_team_company8_hold_order_z_rot                       = 147
slot_team_pai_start_position_x                         = 148
slot_team_pai_start_position_y                         = 149
slot_team_pai_start_position_z_rot                     = 150
slot_team_company1_pai_state                       = 151
slot_team_company2_pai_state                       = 152
slot_team_company3_pai_state                       = 153
slot_team_company4_pai_state                       = 154
slot_team_company5_pai_state                       = 155
slot_team_company6_pai_state                       = 156
slot_team_company7_pai_state                       = 157
slot_team_company8_pai_state                       = 158
slot_team_pai_target_team                       = 159
slot_team_pai_target_company                    = 160
slot_team_pai_retreat_timer                     = 161
slot_team_company1_target_team                       = 162
slot_team_company2_target_team                       = 163
slot_team_company3_target_team                       = 164
slot_team_company4_target_team                       = 165
slot_team_company5_target_team                       = 166
slot_team_company6_target_team                       = 167
slot_team_company7_target_team                       = 168
slot_team_company8_target_team                       = 169
slot_team_company1_target_company                       = 170
slot_team_company2_target_company                       = 171
slot_team_company3_target_company                       = 172
slot_team_company4_target_company                       = 173
slot_team_company5_target_company                       = 174
slot_team_company6_target_company                       = 175
slot_team_company7_target_company                       = 176
slot_team_company8_target_company                       = 177

slot_team_cannons_amount                                = 178
YuriSlotTeam_CannonsAmount = slot_team_cannons_amount

slot_team_company1_accuracy                       = 179
slot_team_company2_accuracy                       = 180
slot_team_company3_accuracy                       = 181
slot_team_company4_accuracy                       = 182
slot_team_company5_accuracy                       = 183
slot_team_company6_accuracy                       = 184
slot_team_company7_accuracy                       = 185
slot_team_company8_accuracy                       = 186
slot_team_company1_penaltytodiscipline_fromcasualties                       = 187
slot_team_company2_penaltytodiscipline_fromcasualties                       = 188
slot_team_company3_penaltytodiscipline_fromcasualties                       = 189
slot_team_company4_penaltytodiscipline_fromcasualties                       = 190
slot_team_company5_penaltytodiscipline_fromcasualties                       = 191
slot_team_company6_penaltytodiscipline_fromcasualties                       = 192
slot_team_company7_penaltytodiscipline_fromcasualties                       = 193
slot_team_company8_penaltytodiscipline_fromcasualties                       = 194

slot_team_artllery_ammo_shells_amount                    = 195
slot_team_has_flagbearer                    = 196

slot_team_company1_discipline                       = 197
slot_team_company2_discipline                       = 198
slot_team_company3_discipline                       = 199
slot_team_company4_discipline                       = 200
slot_team_company5_discipline                       = 201
slot_team_company6_discipline                       = 202
slot_team_company7_discipline                       = 203
slot_team_company8_discipline                       = 204

slot_team_company1_formation                       = 205
slot_team_company2_formation                       = 206
slot_team_company3_formation                       = 207
slot_team_company4_formation                       = 208
slot_team_company5_formation                       = 209
slot_team_company6_formation                       = 210
slot_team_company7_formation                       = 211
slot_team_company8_formation                       = 212

slot_team_pai_attack_groups_amount                 = 213
slot_team_pai_attack_group_1_1                 = 214
slot_team_pai_attack_group_1_2                 = 215
slot_team_pai_attack_group_1_3                 = 216
slot_team_pai_attack_group_2_1                 = 217
slot_team_pai_attack_group_2_2                 = 218
slot_team_pai_attack_group_2_3                 = 219
slot_team_pai_attack_group_3_1                 = 220
slot_team_pai_attack_group_3_2                 = 221
slot_team_pai_attack_group_3_3                 = 222
slot_team_pai_cavalry_company    = 223
slot_team_pai_attack_group_1_1_state                 = 224
slot_team_pai_attack_group_2_1_state                 = 225
slot_team_pai_attack_group_3_1_state                 = 226
slot_team_pai_attack_group_1_2_state                 = 227
slot_team_pai_attack_group_2_2_state                 = 228
slot_team_pai_attack_group_3_2_state                 = 229
slot_team_pai_attack_group_1_3_state                 = 230
slot_team_pai_attack_group_2_3_state                 = 231
slot_team_pai_attack_group_3_3_state                 = 232
slot_team_pai_attack_artillery_company_number    = 233
slot_team_vo_allowed    = 234
slot_team_company1_digin_status                       = 235
slot_team_company2_digin_status                       = 236
slot_team_company3_digin_status                       = 237
slot_team_company4_digin_status                       = 238
slot_team_company5_digin_status                       = 239
slot_team_company6_digin_status                       = 240
slot_team_company7_digin_status                       = 241
slot_team_company8_digin_status                       = 242

slot_team_mg_amount                                = 243

slot_team_company1_pai_digin_timer                       = 244
slot_team_company2_pai_digin_timer                       = 245
slot_team_company3_pai_digin_timer                       = 246
slot_team_company4_pai_digin_timer                       = 247
slot_team_company5_pai_digin_timer                       = 248
slot_team_company6_pai_digin_timer                       = 249
slot_team_company7_pai_digin_timer                       = 250
slot_team_company8_pai_digin_timer                       = 251
slot_team_pai_mg_company_number    = 252
slot_team_pai_distance_between_groups    = 253
slot_team_pai_distance_between_companies_within_group    = 254
slot_team_company1_grenade_timer                       = 255
slot_team_company2_grenade_timer                       = 256
slot_team_company3_grenade_timer                       = 257
slot_team_company4_grenade_timer                       = 258
slot_team_company5_grenade_timer                       = 259
slot_team_company6_grenade_timer                       = 260
slot_team_company7_grenade_timer                       = 261
slot_team_company8_grenade_timer                       = 262
slot_team_company1_coveringfire                       = 263
slot_team_company2_coveringfire                       = 264
slot_team_company3_coveringfire                       = 265
slot_team_company4_coveringfire                       = 266
slot_team_company5_coveringfire                       = 267
slot_team_company6_coveringfire                       = 268
slot_team_company7_coveringfire                       = 269
slot_team_company8_coveringfire                       = 270
slot_team_company1_gasmasks                       = 271
slot_team_company2_gasmasks                       = 272
slot_team_company3_gasmasks                       = 273
slot_team_company4_gasmasks                       = 274
slot_team_company5_gasmasks                       = 275
slot_team_company6_gasmasks                       = 276
slot_team_company7_gasmasks                       = 277
slot_team_company8_gasmasks                       = 278
slot_team_company1_is_following_leader                       = 279
slot_team_company2_is_following_leader                       = 280
slot_team_company3_is_following_leader                       = 281
slot_team_company4_is_following_leader                       = 282
slot_team_company5_is_following_leader                       = 283
slot_team_company6_is_following_leader                       = 284
slot_team_company7_is_following_leader                       = 285
slot_team_company8_is_following_leader                       = 286

#Rebellion changes end
# character backgrounds
cb_noble = 1
cb_merchant = 2
cb_guard = 3
cb_forester = 4
cb_nomad = 5
cb_thief = 6
cb_priest = 7
cb_professor = 8
cb_manufacture = 9

cb2_page = 0
cb2_apprentice = 1
cb2_urchin  = 2
cb2_steppe_child = 3
cb2_merchants_helper = 4

cb2_schooler = cb2_page
cb2_factory = cb2_apprentice
cb2_mugger = cb2_urchin
cb2_news = cb2_merchants_helper

cb3_outlaw = 3
cb3_entrepreneur = 4
cb3_americasettler = 5
cb3_troubadour = 7
cb3_warvet = 8
cb3_lady_in_waiting = 9
cb3_student = 10
cb3_student_med = 10
cb3_student_eng = 11
cb3_student_phi = 12

cb4_revenge = 1
cb4_loss    = 2
cb4_wanderlust =  3
cb4_disown  = 5
cb4_greed  = 6

#NPC system changes end
#Encounter types
enctype_fighting_against_village_raid = 1
enctype_catched_during_village_raid   = 2


### Troop occupations slot_troop_occupation
##slto_merchant           = 1
slto_inactive           = 0 #for companions at the beginning of the game

slto_kingdom_hero       = 2

slto_player_companion   = 5 #This is specifically for companions in the employ of the player -- ie, in the party, or on a mission
slto_kingdom_lady       = 6 #Usually inactive (Europe is a traditional place). However, can be made potentially active if active_npcs are expanded to include ladies
slto_kingdom_seneschal  = 7
slto_robber_knight      = 8
slto_inactive_pretender = 9


stl_unassigned          = -1
stl_reserved_for_player = -2
stl_rejected_by_player  = -3

#NPC changes begin
slto_retirement      = 11
#slto_retirement_medium    = 12
#slto_retirement_short     = 13
#NPC changes end

########################################################
##  QUEST SLOTS            #############################
########################################################

slot_quest_target_center            = 1
slot_quest_target_troop             = 2
slot_quest_target_faction           = 3
slot_quest_object_troop             = 4
##slot_quest_target_troop_is_prisoner = 5
slot_quest_giver_troop              = 6
slot_quest_object_center            = 7
slot_quest_target_party             = 8
slot_quest_target_party_template    = 9
slot_quest_target_amount            = 10
slot_quest_current_state            = 11
slot_quest_giver_center             = 12
slot_quest_target_dna               = 13
slot_quest_target_item              = 14
slot_quest_object_faction           = 15

slot_quest_target_state             = 16
slot_quest_object_state             = 17

slot_quest_convince_value           = 19
slot_quest_importance               = 20
slot_quest_xp_reward                = 21
slot_quest_gold_reward              = 22
slot_quest_expiration_days          = 23
slot_quest_dont_give_again_period   = 24
slot_quest_dont_give_again_remaining_days = 25

slot_quest_failure_consequence      = 26
slot_quest_temp_slot      			= 27

########################################################
##  PARTY TEMPLATE SLOTS   #############################
########################################################

# Ryan BEGIN
slot_party_template_num_killed   = 1

slot_party_template_lair_type    	 	= 3
slot_party_template_lair_party    		= 4
slot_party_template_lair_spawnpoint     = 5


# Ryan END


########################################################
##  SCENE PROP SLOTS       #############################
########################################################

scene_prop_open_or_close_slot       = 1
scene_prop_smoke_effect_done        = 2
scene_prop_number_of_agents_pushing = 3 #for belfries only
scene_prop_next_entry_point_id      = 4 #for belfries only
scene_prop_belfry_platform_moved    = 5 #for belfries only
scene_prop_slots_end                = 6
#INVASION MODE START
scene_prop_ccoop_item_drop_start    = 7 #For keeping track of who has opened drop chests in Invasion mode
scene_prop_ccoop_item_drop_end      = scene_prop_ccoop_item_drop_start + 10
#INVASION MODE END

########################################################
rel_enemy   = 0
rel_neutral = 1
rel_ally    = 2


#Talk contexts
tc_town_talk                  = 0
tc_court_talk   	      	  = 1
tc_party_encounter            = 2
tc_castle_gate                = 3
tc_siege_commander            = 4
tc_join_battle_ally           = 5
tc_join_battle_enemy          = 6
tc_castle_commander           = 7
tc_hero_freed                 = 8
tc_hero_defeated              = 9
tc_entering_center_quest_talk = 10
tc_back_alley                 = 11
tc_siege_won_seneschal        = 12
tc_ally_thanks                = 13
tc_tavern_talk                = 14
tc_rebel_thanks               = 15
tc_garden            		  = 16
tc_courtship            	  = 16
tc_after_duel            	  = 17
tc_prison_break               = 18
tc_escape               	  = 19
tc_give_center_to_fief        = 20
tc_merchants_house            = 21


#Troop Commentaries begin
#Log entry types
#civilian
logent_village_raided            = 1
logent_village_extorted          = 2
logent_caravan_accosted          = 3 #in caravan accosted, center and troop object are -1, and the defender's faction is the object
logent_traveller_attacked        = 3 #in traveller attacked, origin and destination are center and troop object, and the attacker's faction is the object

logent_helped_peasants           = 4 

logent_party_traded              = 5

logent_castle_captured_by_player              = 10
logent_lord_defeated_by_player                = 11
logent_lord_captured_by_player                = 12
logent_lord_defeated_but_let_go_by_player     = 13
logent_player_defeated_by_lord                = 14
logent_player_retreated_from_lord             = 15
logent_player_retreated_from_lord_cowardly    = 16
logent_lord_helped_by_player                  = 17
logent_player_participated_in_siege           = 18
logent_player_participated_in_major_battle    = 19
logent_castle_given_to_lord_by_player         = 20

logent_pledged_allegiance          = 21
logent_liege_grants_fief_to_vassal = 22


logent_renounced_allegiance      = 23 

logent_player_claims_throne_1    		               = 24
logent_player_claims_throne_2    		               = 25


logent_troop_feels_cheated_by_troop_over_land		   = 26
logent_ruler_intervenes_in_quarrel                     = 27
logent_lords_quarrel_over_land                         = 28
logent_lords_quarrel_over_insult                       = 29
logent_marshal_vs_lord_quarrel                  	   = 30
logent_lords_quarrel_over_woman                        = 31

logent_lord_protests_marshall_appointment			   = 32
logent_lord_blames_defeat						   	   = 33

logent_player_suggestion_succeeded					   = 35
logent_player_suggestion_failed					       = 36

logent_liege_promises_fief_to_vassal				   = 37

logent_lord_insults_lord_for_cowardice                 = 38
logent_lord_insults_lord_for_rashness                  = 39
logent_lord_insults_lord_for_abandonment               = 40
logent_lord_insults_lord_for_indecision                = 41
logent_lord_insults_lord_for_cruelty                   = 42
logent_lord_insults_lord_for_dishonor                  = 43




logent_game_start                           = 45 
logent_poem_composed                        = 46 ##Not added
logent_tournament_distinguished             = 47 ##Not added
logent_tournament_won                       = 48 ##Not added

#logent courtship - lady is always actor, suitor is always troop object
logent_lady_favors_suitor                   = 51 #basically for gossip
logent_lady_betrothed_to_suitor_by_choice   = 52
logent_lady_betrothed_to_suitor_by_family   = 53
logent_lady_rejects_suitor                  = 54
logent_lady_father_rejects_suitor           = 55
logent_lady_marries_lord                    = 56
logent_lady_elopes_with_lord                = 57
logent_lady_rejected_by_suitor              = 58
logent_lady_betrothed_to_suitor_by_pressure = 59 #mostly for gossip

logent_lady_and_suitor_break_engagement		= 60
logent_lady_marries_suitor				    = 61

logent_lord_holds_lady_hostages             = 62
logent_challenger_defeats_lord_in_duel      = 63
logent_challenger_loses_to_lord_in_duel     = 64

logent_player_stole_cattles_from_village    = 66

logent_party_spots_wanted_bandits           = 70


logent_border_incident_cattle_stolen          = 72 #possibly add this to rumors for non-player faction
logent_border_incident_bride_abducted         = 73 #possibly add this to rumors for non-player faction
logent_border_incident_villagers_killed       = 74 #possibly add this to rumors for non-player faction
logent_border_incident_subjects_mistreated    = 75 #possibly add this to rumors for non-player faction

#These supplement caravans accosted and villages burnt, in that they create a provocation. So far, they only refer to the player
logent_border_incident_troop_attacks_neutral  = 76
logent_border_incident_troop_breaks_truce     = 77
logent_border_incident_troop_suborns_lord   = 78


logent_policy_ruler_attacks_without_provocation 			= 80
logent_policy_ruler_ignores_provocation         			= 81 #possibly add this to rumors for non-player factions
logent_policy_ruler_makes_peace_too_soon        			= 82
logent_policy_ruler_declares_war_with_justification         = 83
logent_policy_ruler_breaks_truce                            = 84
logent_policy_ruler_issues_indictment_just                  = 85 #possibly add this to rumors for non-player faction
logent_policy_ruler_issues_indictment_questionable          = 86 #possibly add this to rumors for non-player faction

logent_player_faction_declares_war						    = 90 #this doubles for declare war to extend power
logent_faction_declares_war_out_of_personal_enmity		    = 91
logent_faction_declares_war_to_regain_territory 		    = 92
logent_faction_declares_war_to_curb_power					= 93
logent_faction_declares_war_to_respond_to_provocation	    = 94
logent_war_declaration_types_end							= 95


#logent_lady_breaks_betrothal_with_lord      = 58
#logent_lady_betrothal_broken_by_lord        = 59

#lord reputation type, for commentaries
#"Martial" will be twice as common as the other types
lrep_none           = 0 
lrep_martial        = 1 #chivalrous but not terribly empathetic or introspective, - eg Richard Lionheart, your average 14th century French baron
lrep_quarrelsome    = 2 #spiteful, cynical, a bit paranoid, possibly hotheaded - eg Robert Graves' Tiberius, some of Charles VI's uncles
lrep_selfrighteous  = 3 #coldblooded, moralizing, often cruel - eg William the Conqueror, Timur, Octavian, Aurangzeb (although he is arguably upstanding instead, particularly after his accession)
lrep_cunning        = 4 #coldblooded, pragmatic, amoral - eg Louis XI, Guiscard, Akbar Khan, Abd al-Aziz Ibn Saud
lrep_debauched      = 5 #spiteful, amoral, sadistic - eg Caligula, Tuchman's Charles of Navarre
lrep_goodnatured    = 6 #chivalrous, benevolent, perhaps a little too decent to be a good warlord - eg Hussein ibn Ali. Few well-known historical examples maybe. because many lack the drive to rise to faction leadership. Ranjit Singh has aspects
lrep_upstanding     = 7 #moralizing, benevolent, pragmatic, - eg Bernard Cornwell's Alfred, Charlemagne, Salah al-Din, Sher Shah Suri

lrep_roguish        = 8 #used for commons, specifically ex-companions. Tries to live life as a lord to the full
lrep_benefactor     = 9 #used for commons, specifically ex-companions. Tries to improve lot of folks on land
lrep_custodian      = 10 #used for commons, specifically ex-companions. Tries to maximize fief's earning potential

#lreps specific to dependent noblewomen
lrep_conventional    = 21 #Charlotte York in SATC seasons 1-2, probably most medieval aristocrats
lrep_adventurous     = 22 #Tomboyish. However, this basically means that she likes to travel and hunt, and perhaps yearn for wider adventures. However, medieval noblewomen who fight are rare, and those that attempt to live independently of a man are rarer still, and best represented by pre-scripted individuals like companions
lrep_otherworldly    = 23 #Prone to mysticism, romantic. 
lrep_ambitious       = 24 #Lady Macbeth
lrep_moralist        = 25 #Equivalent of upstanding or benefactor -- takes nobless oblige, and her traditional role as repository of morality, very seriously. Based loosely on Christine de Pisa 

#a more complicated system of reputation could include the following...

#successful vs unlucky -- basic gauge of success
#daring vs cautious -- maybe not necessary
#honorable/pious/ideological vs unscrupulous -- character's adherance to an external code of conduct. Fails to capture complexity of people like Aurangzeb, maybe, but good for NPCs
	#(visionary/altruist and orthodox/unorthodox could be a subset of the above, or the specific external code could be another tag)
#generous/loyal vs manipulative/exploitative -- character's sense of duty to specific individuals, based on their relationship. Affects loyalty of troops, etc
#merciful vs cruel/ruthless/sociopathic -- character's general sense of compassion. Sher Shah is example of unscrupulous and merciful (the latter to a degree).
#dignified vs unconventional -- character's adherance to social conventions. Very important, given the times


courtship_poem_tragic      = 1 #Emphasizes longing, Laila and Majnoon
courtship_poem_heroic      = 2 #Norse sagas with female heroines
courtship_poem_comic       = 3 #Emphasis on witty repartee -- Contrasto (Sicilian school satire) 
courtship_poem_mystic      = 4 #Sufi poetry. Song of Songs
courtship_poem_allegoric   = 5 #Idealizes woman as a civilizing force -- the Romance of the Rose, Siege of the Castle of Love

#courtship gifts currently deprecated







#Troop Commentaries end

tutorial_fighters_begin = "trp_tutorial_fighter_1"
tutorial_fighters_end   = "trp_tutorial_archer_1"

#Walker types: 
walkert_default            = 0
walkert_needs_money        = 1
walkert_needs_money_helped = 2
walkert_spy                = 3
num_town_walkers = 8
town_walker_entries_start = 32

reinforcement_cost_easy = 600
reinforcement_cost_moderate = 450
reinforcement_cost_hard = 300

merchant_toll_duration        = 72 #Tolls are valid for 72 hours

hero_escape_after_defeat_chance = 70


raid_distance = 4

surnames_begin = "str_surname_1"
surnames_end = "str_surnames_end"
names_begin = "str_name_1"
names_end = surnames_begin
countersigns_begin = "str_countersign_1"
countersigns_end = names_begin
secret_signs_begin = "str_secret_sign_1"
secret_signs_end = countersigns_begin

kingdom_titles_male_begin = "str_faction_title_male_player"
kingdom_titles_female_begin = "str_faction_title_female_player"

kingdoms_begin = "fac_player_supporters_faction"
kingdoms_begin_int = fac_player_supporters_faction
kingdoms_end = "fac_kingdoms_end"
kingdoms_end_int = fac_kingdoms_end

npc_kingdoms_begin = "fac_kingdom_1"
npc_kingdoms_end = kingdoms_end

bandits_begin = "trp_bandit"
bandits_end = "trp_black_khergit_horseman"

kingdom_ladies_begin = "trp_knight_1_1_wife"
kingdom_ladies_end = "trp_heroes_end"

#active NPCs in order: companions, kings, lords, pretenders

pretenders_begin = "trp_kingdom_1_pretender"
pretenders_end = kingdom_ladies_begin

lords_begin = "trp_knight_1_1"
lords_end = pretenders_begin

kings_begin = "trp_kingdom_1_lord"
kings_end = lords_begin

companions_begin = "trp_npc1"
companions_end = kings_begin

active_npcs_begin = "trp_npc1"
active_npcs_end = kingdom_ladies_begin
#"active_npcs_begin replaces kingdom_heroes_begin to allow for companions to become lords. Includes anyone who may at some point lead their own party: the original kingdom heroes, companions who may become kingdom heroes, and pretenders. (slto_kingdom_hero as an occupation means that you lead a party on the map. Pretenders have the occupation "slto_inactive_pretender", even if they are part of a player's party, until they have their own independent party)
#If you're a modder and you don't want to go through and switch every kingdom_heroes to active_npcs, simply define a constant: kingdom_heroes_begin = active_npcs_begin., and kingdom_heroes_end = active_npcs_end. I haven't tested for that, but I think it should work.

active_npcs_including_player_begin = "trp_kingdom_heroes_including_player_begin"
original_kingdom_heroes_begin = "trp_kingdom_1_lord"

heroes_begin = active_npcs_begin
heroes_end = kingdom_ladies_end

soldiers_begin = "trp_farmer"
soldiers_end = "trp_town_walker_1"

#Rebellion changes

##rebel_factions_begin = "fac_kingdom_1_rebels"
##rebel_factions_end =   "fac_kingdoms_end"

pretenders_begin = "trp_kingdom_1_pretender"
pretenders_end = active_npcs_end
#Rebellion changes

tavern_minstrels_begin = "trp_tavern_minstrel_1"
tavern_minstrels_end   = "trp_kingdom_heroes_including_player_begin"

tavern_booksellers_begin = "trp_tavern_bookseller_1"
tavern_booksellers_end   = tavern_minstrels_begin

tavern_travelers_begin = "trp_tavern_traveler_1"
tavern_travelers_end   = tavern_booksellers_begin

ransom_brokers_begin = "trp_ransom_broker_1"
ransom_brokers_end   = tavern_travelers_begin

mercenary_troops_begin = "trp_watchman"
mercenary_troops_end = "trp_mercenaries_end"

multiplayer_troops_begin = "trp_swadian_crossbowman_multiplayer"
multiplayer_troops_end = "trp_multiplayer_end"

#INVASION MODE start
ccoop_companion_sounds_start = "snd_ccoop_spawn_companion_0"
ccoop_companion_sounds_end = "snd_ccoop_nobleman_taunt"

ccoop_noble_sounds_start = "snd_ccoop_nobleman_taunt"
ccoop_noble_sounds_end = "snd_ccoop_looter_taunt_0"

ccoop_looter_sounds_start = "snd_ccoop_looter_taunt_0"
ccoop_looter_sounds_end = "snd_ccoop_bandit_taunt_0"

ccoop_bandit_sounds_start = "snd_ccoop_bandit_taunt_0"
ccoop_bandit_sounds_end = "snd_ccoop_sea_raider_taunt_0"

ccoop_sea_raider_sounds_start = "snd_ccoop_sea_raider_taunt_0"
ccoop_sea_raider_sounds_end = "snd_sounds_end"

multiplayer_coop_class_templates_begin = "trp_swadian_crossbowman_multiplayer_coop_tier_1"
multiplayer_coop_class_templates_end = "trp_coop_faction_troop_templates_end"

multiplayer_coop_companion_equipment_sets_begin = "trp_npc1_1"
multiplayer_coop_companion_first_equipment_sets_end = "trp_npc1_2"
multiplayer_coop_companion_equipment_sets_end = "trp_coop_companion_equipment_sets_end"

multiplayer_coop_companion_description_strings_begin = "str_npc1_1"
#INVASION MODE end

multiplayer_ai_troops_begin = "trp_swadian_crossbowman_multiplayer_ai"
multiplayer_ai_troops_end = multiplayer_troops_begin

#INVASION MODE START
captain_multiplayer_troops_begin = "trp_farmer"
captain_multiplayer_troops_end = "trp_swadian_crossbowman"

captain_multiplayer_new_troops_begin = "trp_swadian_crossbowman"
captain_multiplayer_new_troops_end = "trp_khergit_lancer"

captain_multiplayer_coop_new_troops_begin = "trp_khergit_lancer"
captain_multiplayer_coop_new_troops_end = "trp_slaver_chief"
#INVASION MODE END

multiplayer_scenes_begin = "scn_multi_scene_1"
multiplayer_scenes_end = "scn_multiplayer_maps_end"

multiplayer_scene_names_begin = "str_multi_scene_1"
multiplayer_scene_names_end = "str_multi_scene_end"

multiplayer_flag_projections_begin = "mesh_flag_project_sw"
multiplayer_flag_projections_end = "mesh_flag_projects_end"

multiplayer_flag_taken_projections_begin = "mesh_flag_project_sw_miss"
multiplayer_flag_taken_projections_end = "mesh_flag_project_misses_end"

multiplayer_game_type_names_begin = "str_multi_game_type_1"
multiplayer_game_type_names_end = "str_multi_game_types_end"

quick_battle_troops_begin = "trp_quick_battle_troop_1"
quick_battle_troops_end = "trp_quick_battle_troops_end"

quick_battle_troop_texts_begin = "str_quick_battle_troop_1"
quick_battle_troop_texts_end = "str_quick_battle_troops_end"

quick_battle_scenes_begin = "scn_quick_battle_scene_1"
quick_battle_scenes_end = "scn_quick_battle_maps_end"

quick_battle_scene_images_begin = "mesh_cb_ui_maps_scene_01"

quick_battle_battle_scenes_begin = quick_battle_scenes_begin
quick_battle_battle_scenes_end = "scn_quick_battle_scene_4"

quick_battle_siege_scenes_begin = quick_battle_battle_scenes_end
quick_battle_siege_scenes_end = quick_battle_scenes_end

quick_battle_scene_names_begin = "str_quick_battle_scene_1"

lord_quests_begin = "qst_deliver_message"
lord_quests_end   = "qst_follow_army"

lord_quests_begin_2 = "qst_destroy_bandit_lair"
lord_quests_end_2   = "qst_blank_quest_2"

enemy_lord_quests_begin = "qst_lend_surgeon"
enemy_lord_quests_end   = lord_quests_end

village_elder_quests_begin = "qst_deliver_grain"
village_elder_quests_end = "qst_eliminate_bandits_infesting_village"

village_elder_quests_begin_2 = "qst_blank_quest_6"
village_elder_quests_end_2   = "qst_blank_quest_6"

mayor_quests_begin  = "qst_move_cattle_herd"
mayor_quests_end    = village_elder_quests_begin

mayor_quests_begin_2 = "qst_blank_quest_11"
mayor_quests_end_2   = "qst_blank_quest_11"

lady_quests_begin = "qst_rescue_lord_by_replace"
lady_quests_end   = mayor_quests_begin

lady_quests_begin_2 = "qst_blank_quest_16"
lady_quests_end_2   = "qst_blank_quest_16"

army_quests_begin = "qst_deliver_cattle_to_army"
army_quests_end   = lady_quests_begin

army_quests_begin_2 = "qst_blank_quest_21"
army_quests_end_2   = "qst_blank_quest_21"

player_realm_quests_begin = "qst_resolve_dispute"
player_realm_quests_end = "qst_blank_quest_1"

player_realm_quests_begin_2 = "qst_blank_quest_26"
player_realm_quests_end_2 = "qst_blank_quest_26"

all_items_begin = 0
all_items_end = "itm_items_end"

all_quests_begin = 0
all_quests_end = "qst_quests_end"

towns_begin = "p_town_1"
castles_begin = "p_castle_1"
villages_begin = "p_village_1"
villages_begin_int = p_village_1

towns_end = castles_begin
castles_end = villages_begin
castles_end_int = villages_begin_int
villages_end   = "p_salt_mine"

walled_centers_begin = towns_begin
walled_centers_end   = castles_end

centers_begin = towns_begin
centers_end   = villages_end

training_grounds_begin   = "p_training_ground_1"
training_grounds_end     = "p_Bridge_1"

scenes_begin = "scn_town_1_center"
scenes_end = "scn_castle_1_exterior"

spawn_points_begin = "p_zendar"
spawn_points_end = "p_spawn_points_end"

regular_troops_begin       = "trp_novice_fighter"
regular_troops_end         = "trp_tournament_master"

swadian_merc_parties_begin = "p_town_1_mercs"
swadian_merc_parties_end   = "p_town_8_mercs"

vaegir_merc_parties_begin  = "p_town_8_mercs"
vaegir_merc_parties_end    = "p_zendar"

arena_masters_begin    = "trp_town_1_arena_master"
arena_masters_end      = "trp_town_1_armorer"

training_gound_trainers_begin    = "trp_trainer_1"
training_gound_trainers_end      = "trp_ransom_broker_1"

town_walkers_begin = "trp_town_walker_1"
town_walkers_end = "trp_village_walker_1"

village_walkers_begin = "trp_village_walker_1"
village_walkers_end   = "trp_spy_walker_1"

spy_walkers_begin = "trp_spy_walker_1"
spy_walkers_end = "trp_tournament_master"

walkers_begin = town_walkers_begin
walkers_end   = spy_walkers_end

armor_merchants_begin  = "trp_town_1_armorer"
armor_merchants_end    = "trp_town_1_weaponsmith"

weapon_merchants_begin = "trp_town_1_weaponsmith"
weapon_merchants_end   = "trp_town_1_tavernkeeper"

tavernkeepers_begin    = "trp_town_1_tavernkeeper"
tavernkeepers_end      = "trp_town_1_merchant"

goods_merchants_begin  = "trp_town_1_merchant"
goods_merchants_end    = "trp_town_1_horse_merchant"

horse_merchants_begin  = "trp_town_1_horse_merchant"
horse_merchants_end    = "trp_town_1_mayor"

mayors_begin           = "trp_town_1_mayor"
mayors_end             = "trp_village_1_elder"

village_elders_begin   = "trp_village_1_elder"
village_elders_end     = "trp_merchants_end"

startup_merchants_begin = "trp_swadian_merchant"
startup_merchants_end = "trp_startup_merchants_end"

num_max_items = 10000 #used for multiplayer mode

average_price_factor = 1000
minimum_price_factor = 100
maximum_price_factor = 10000

village_prod_min = 0 #was -5
village_prod_max = 20 #was 20

trade_goods_begin = "itm_spice"
trade_goods_end = "itm_siege_supply"
food_begin = "itm_smoked_fish"
food_end = "itm_siege_supply"
reference_books_begin = "itm_book_wound_treatment_reference"
reference_books_end   = trade_goods_begin
readable_books_begin = "itm_book_tactics"
readable_books_end   = reference_books_begin
books_begin = readable_books_begin
books_end = reference_books_end
horses_begin = "itm_sumpter_horse"
horses_end = "itm_arrows"
weapons_begin = "itm_wooden_stick"
weapons_end = "itm_wooden_shield"
ranged_weapons_begin = "itm_darts"
ranged_weapons_end = "itm_torch"
armors_begin = "itm_leather_gloves"
armors_end = "itm_wooden_stick"
shields_begin = "itm_wooden_shield"
shields_end = ranged_weapons_begin

#INVASION MODE START
coop_drops_begin = "itm_javelin_bow"
coop_drops_end = "itm_javelin_bow_ammo"
coop_new_items_end = "itm_ccoop_new_items_end"

ccoop_max_num_players = 12

coop_drops_descriptions_begin = "str_javelin_bow"
coop_drops_descriptions_end = "str_npc1_1"
#INVASION MODE END


# Banner constants

banner_meshes_begin = "mesh_banner_a01"
banner_meshes_end_minus_one = "mesh_banner_f21"

arms_meshes_begin = "mesh_arms_a01"
arms_meshes_end_minus_one = "mesh_arms_f21"

custom_banner_charges_begin = "mesh_custom_banner_charge_01"
custom_banner_charges_end = "mesh_tableau_mesh_custom_banner"

custom_banner_backgrounds_begin = "mesh_custom_banner_bg"
custom_banner_backgrounds_end = custom_banner_charges_begin

custom_banner_flag_types_begin = "mesh_custom_banner_01"
custom_banner_flag_types_end = custom_banner_backgrounds_begin

custom_banner_flag_map_types_begin = "mesh_custom_map_banner_01"
custom_banner_flag_map_types_end = custom_banner_flag_types_begin

custom_banner_flag_scene_props_begin = "spr_custom_banner_01"
custom_banner_flag_scene_props_end = "spr_banner_a"

custom_banner_map_icons_begin = "icon_custom_banner_01"
custom_banner_map_icons_end = "icon_banner_01"

banner_map_icons_begin = "icon_banner_01"
banner_map_icons_end_minus_one = "icon_banner_136"

banner_scene_props_begin = "spr_banner_a"
banner_scene_props_end_minus_one = "spr_banner_f21"

khergit_banners_begin_offset = 63
khergit_banners_end_offset = 84

sarranid_banners_begin_offset = 105
sarranid_banners_end_offset = 125

banners_end_offset = 136

# Some constants for merchant invenotries
merchant_inventory_space = 30
num_merchandise_goods = 40

num_max_river_pirates = 25
num_max_zendar_peasants = 25
num_max_zendar_manhunters = 10

num_max_dp_bandits = 10
num_max_refugees = 10
num_max_deserters = 10

num_max_militia_bands = 15
num_max_armed_bands = 12

num_max_vaegir_punishing_parties = 20
num_max_rebel_peasants = 25

num_max_frightened_farmers = 50
num_max_undead_messengers  = 20

num_forest_bandit_spawn_points = 1
num_mountain_bandit_spawn_points = 1
num_steppe_bandit_spawn_points = 1
num_taiga_bandit_spawn_points = 1
num_desert_bandit_spawn_points = 1
num_black_khergit_spawn_points = 1
num_sea_raider_spawn_points = 2

peak_prisoner_trains = 4
peak_kingdom_caravans = 12
peak_kingdom_messengers = 3


# Note positions
note_troop_location = 3

#battle tactics
btactic_hold = 1
btactic_follow_leader = 2
btactic_charge = 3
btactic_stand_ground = 4

#default right mouse menu orders
cmenu_move = -7
cmenu_follow = -6

# Town center modes - resets in game menus during the options
tcm_default 		= 0
tcm_disguised 		= 1
tcm_prison_break 	= 2
tcm_escape      	= 3


# Arena battle modes
#abm_fight = 0
abm_training = 1
abm_visit = 2
abm_tournament = 3

# Camp training modes
ctm_melee    = 1
ctm_ranged   = 2
ctm_mounted  = 3
ctm_training = 4

# Village bandits attack modes
vba_normal          = 1
vba_after_training  = 2

arena_tier1_opponents_to_beat = 3
arena_tier1_prize = 5
arena_tier2_opponents_to_beat = 6
arena_tier2_prize = 10
arena_tier3_opponents_to_beat = 10
arena_tier3_prize = 25
arena_tier4_opponents_to_beat = 20
arena_tier4_prize = 60
arena_grand_prize = 250


#Additions
price_adjustment = 25 #the percent by which a trade at a center alters price

fire_duration = 4 #fires takes 4 hours

#Viking Conquest patch 1.167 parameters for try_for_prop_instances
somt_object = 1
somt_entry = 2
somt_item = 3
somt_baggage = 4
somt_flora = 5
somt_passage = 6
somt_spawned_item = 7
somt_spawned_single_ammo_item = 8
somt_spawned_unsheathed_item = 9
somt_shield = 10
somt_temporary_object = 11


#NORMAL ACHIEVEMENTS
ACHIEVEMENT_NONE_SHALL_PASS = 1,
ACHIEVEMENT_MAN_EATER = 2,
ACHIEVEMENT_THE_HOLY_HAND_GRENADE = 3,
ACHIEVEMENT_LOOK_AT_THE_BONES = 4,
ACHIEVEMENT_KHAAAN = 5,
ACHIEVEMENT_GET_UP_STAND_UP = 6,
ACHIEVEMENT_BARON_GOT_BACK = 7,
ACHIEVEMENT_BEST_SERVED_COLD = 8,
ACHIEVEMENT_TRICK_SHOT = 9,
ACHIEVEMENT_GAMBIT = 10,
ACHIEVEMENT_OLD_SCHOOL_SNIPER = 11,
ACHIEVEMENT_CALRADIAN_ARMY_KNIFE = 12,
ACHIEVEMENT_MOUNTAIN_BLADE = 13,
ACHIEVEMENT_HOLY_DIVER = 14,
ACHIEVEMENT_FORCE_OF_NATURE = 15,

#SKILL RELATED ACHIEVEMENTS:
ACHIEVEMENT_BRING_OUT_YOUR_DEAD = 16,
ACHIEVEMENT_MIGHT_MAKES_RIGHT = 17,
ACHIEVEMENT_COMMUNITY_SERVICE = 18,
ACHIEVEMENT_AGILE_WARRIOR = 19,
ACHIEVEMENT_MELEE_MASTER = 20,
ACHIEVEMENT_DEXTEROUS_DASTARD = 21,
ACHIEVEMENT_MIND_ON_THE_MONEY = 22,
ACHIEVEMENT_ART_OF_WAR = 23,
ACHIEVEMENT_THE_RANGER = 24,
ACHIEVEMENT_TROJAN_BUNNY_MAKER = 25,

#MAP RELATED ACHIEVEMENTS:
ACHIEVEMENT_MIGRATING_COCONUTS = 26,
ACHIEVEMENT_HELP_HELP_IM_BEING_REPRESSED = 27,
ACHIEVEMENT_SARRANIDIAN_NIGHTS = 28,
ACHIEVEMENT_OLD_DIRTY_SCOUNDREL = 29,
ACHIEVEMENT_THE_BANDIT = 30,
ACHIEVEMENT_GOT_MILK = 31,
ACHIEVEMENT_SOLD_INTO_SLAVERY = 32,
ACHIEVEMENT_MEDIEVAL_TIMES = 33,
ACHIEVEMENT_GOOD_SAMARITAN = 34,
ACHIEVEMENT_MORALE_LEADER = 35,
ACHIEVEMENT_ABUNDANT_FEAST = 36,
ACHIEVEMENT_BOOK_WORM = 37,
ACHIEVEMENT_ROMANTIC_WARRIOR = 38,

#POLITICALLY ORIENTED ACHIEVEMENTS:
ACHIEVEMENT_HAPPILY_EVER_AFTER = 39,
ACHIEVEMENT_HEART_BREAKER = 40,
ACHIEVEMENT_AUTONOMOUS_COLLECTIVE = 41,
ACHIEVEMENT_I_DUB_THEE = 42,
ACHIEVEMENT_SASSY = 43,
ACHIEVEMENT_THE_GOLDEN_THRONE = 44,
ACHIEVEMENT_KNIGHTS_OF_THE_ROUND = 45,
ACHIEVEMENT_TALKING_HELPS = 46,
ACHIEVEMENT_KINGMAKER = 47,
ACHIEVEMENT_PUGNACIOUS_D = 48,
ACHIEVEMENT_GOLD_FARMER = 49,
ACHIEVEMENT_ROYALITY_PAYMENT = 50,
ACHIEVEMENT_MEDIEVAL_EMLAK = 51,
ACHIEVEMENT_CALRADIAN_TEA_PARTY = 52,
ACHIEVEMENT_MANIFEST_DESTINY = 53,
ACHIEVEMENT_CONCILIO_CALRADI = 54,
ACHIEVEMENT_VICTUM_SEQUENS = 55,

#MULTIPLAYER ACHIEVEMENTS:
ACHIEVEMENT_THIS_IS_OUR_LAND = 56,
ACHIEVEMENT_SPOIL_THE_CHARGE = 57,
ACHIEVEMENT_HARASSING_HORSEMAN = 58,
ACHIEVEMENT_THROWING_STAR = 59,
ACHIEVEMENT_SHISH_KEBAB = 60,
ACHIEVEMENT_RUIN_THE_RAID = 61,
ACHIEVEMENT_LAST_MAN_STANDING = 62,
ACHIEVEMENT_EVERY_BREATH_YOU_TAKE = 63,
ACHIEVEMENT_CHOPPY_CHOP_CHOP = 64,
ACHIEVEMENT_MACE_IN_YER_FACE = 65,
ACHIEVEMENT_THE_HUSCARL = 66,
ACHIEVEMENT_GLORIOUS_MOTHER_FACTION = 67,
ACHIEVEMENT_ELITE_WARRIOR = 68,

#COMBINED ACHIEVEMENTS
ACHIEVEMENT_SON_OF_ODIN = 69,
ACHIEVEMENT_KING_ARTHUR = 70,
ACHIEVEMENT_KASSAI_MASTER = 71,
ACHIEVEMENT_IRON_BEAR = 72,
ACHIEVEMENT_LEGENDARY_RASTAM = 73,
ACHIEVEMENT_SVAROG_THE_MIGHTY = 74,

ACHIEVEMENT_MAN_HANDLER = 75,
ACHIEVEMENT_GIRL_POWER = 76,
ACHIEVEMENT_QUEEN = 77,
ACHIEVEMENT_EMPRESS = 78,
ACHIEVEMENT_TALK_OF_THE_TOWN = 79,
ACHIEVEMENT_LADY_OF_THE_LAKE = 80,



# modmerger_start version=201 type=1
try:
    from util_common import logger
    from modmerger_options import mods_active
    modcomp_name = "constants"
    for mod_name in mods_active:
        try:
            logger.info("Importing constants from mod \"%s\"..."%(mod_name))
            code = "from %s_constants import *" % mod_name
            exec code
        except ImportError:
            errstring = "Component \"%s\" not found for mod \"%s\"." % (modcomp_name, mod_name)
            logger.debug(errstring)
except:
    raise
# modmerger_end
