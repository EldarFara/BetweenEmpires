from header_common import *
from header_operations import *
from header_mission_templates import *
from header_animations import *
from header_sounds import *
from header_music import *
from header_items import *
from module_constants import *

####################################################################################################################
#   Each mission-template is a tuple that contains the following fields:
#  1) Mission-template id (string): used for referencing mission-templates in other files.
#     The prefix mt_ is automatically added before each mission-template id
#
#  2) Mission-template flags (int): See header_mission-templates.py for a list of available flags
#  3) Mission-type(int): Which mission types this mission template matches.
#     For mission-types to be used with the default party-meeting system,
#     this should be 'charge' or 'charge_with_ally' otherwise must be -1.
#     
#  4) Mission description text (string).
#  5) List of spawn records (list): Each spawn record is a tuple that contains the following fields:
#    5.1) entry-no: Troops spawned from this spawn record will use this entry
#    5.2) spawn flags.
#    5.3) alter flags. which equipment will be overriden
#    5.4) ai flags.
#    5.5) Number of troops to spawn.
#    5.6) list of equipment to add to troops spawned from here (maximum 8).
#  6) List of triggers (list).
#     See module_triggers.py for infomation about triggers.
#
#  Please note that mission templates is work in progress and can be changed in the future versions.
# 
####################################################################################################################

pilgrim_disguise = [itm_pilgrim_hood,itm_pilgrim_disguise,itm_practice_staff, itm_throwing_daggers]
af_castle_lord = af_override_horse | af_override_weapons| af_require_civilian

multiplayer_server_check_belfry_movement = (
  0, 0, 0, [],
  [
    (multiplayer_is_server),
    (set_fixed_point_multiplier, 100),

    (try_for_range, ":belfry_kind", 0, 2),
      (try_begin),
        (eq, ":belfry_kind", 0),
        (assign, ":belfry_body_scene_prop", "spr_belfry_a"),
      (else_try),
        (assign, ":belfry_body_scene_prop", "spr_belfry_b"),
      (try_end),
    
      (scene_prop_get_num_instances, ":num_belfries", ":belfry_body_scene_prop"),
      (try_for_range, ":belfry_no", 0, ":num_belfries"),
        (scene_prop_get_instance, ":belfry_scene_prop_id", ":belfry_body_scene_prop", ":belfry_no"),
        (prop_instance_get_position, pos1, ":belfry_scene_prop_id"), #pos1 holds position of current belfry 
        (prop_instance_get_starting_position, pos11, ":belfry_scene_prop_id"),

        (store_add, ":belfry_first_entry_point_id", 11, ":belfry_no"), #belfry entry points are 110..119 and 120..129 and 130..139
        (try_begin),
          (eq, ":belfry_kind", 1),
          (scene_prop_get_num_instances, ":number_of_belfry_a", "spr_belfry_a"),
          (val_add, ":belfry_first_entry_point_id", ":number_of_belfry_a"),
        (try_end),        
                
        (val_mul, ":belfry_first_entry_point_id", 10),
        (store_add, ":belfry_last_entry_point_id", ":belfry_first_entry_point_id", 10),
    
        (try_for_range, ":entry_point_id", ":belfry_first_entry_point_id", ":belfry_last_entry_point_id"),
          (entry_point_is_auto_generated, ":entry_point_id"),
          (assign, ":belfry_last_entry_point_id", ":entry_point_id"),
        (try_end),
        
        (assign, ":belfry_last_entry_point_id_plus_one", ":belfry_last_entry_point_id"),
        (val_sub, ":belfry_last_entry_point_id", 1),
        (assign, reg0, ":belfry_last_entry_point_id"),
        (neg|entry_point_is_auto_generated, ":belfry_last_entry_point_id"),

        (try_begin),
          (get_sq_distance_between_positions, ":dist_between_belfry_and_its_destination", pos1, pos11),
          (ge, ":dist_between_belfry_and_its_destination", 4), #0.2 * 0.2 * 100 = 4 (if distance between belfry and its destination already less than 20cm no need to move it anymore)

          (assign, ":max_dist_between_entry_point_and_belfry_destination", -1), #should be lower than 0 to allow belfry to go last entry point
          (assign, ":belfry_next_entry_point_id", -1),
          (try_for_range, ":entry_point_id", ":belfry_first_entry_point_id", ":belfry_last_entry_point_id_plus_one"),
            (entry_point_get_position, pos4, ":entry_point_id"),
            (get_sq_distance_between_positions, ":dist_between_entry_point_and_belfry_destination", pos11, pos4),
            (lt, ":dist_between_entry_point_and_belfry_destination", ":dist_between_belfry_and_its_destination"),
            (gt, ":dist_between_entry_point_and_belfry_destination", ":max_dist_between_entry_point_and_belfry_destination"),
            (assign, ":max_dist_between_entry_point_and_belfry_destination", ":dist_between_entry_point_and_belfry_destination"),
            (assign, ":belfry_next_entry_point_id", ":entry_point_id"),
          (try_end),

          (try_begin),
            (ge, ":belfry_next_entry_point_id", 0),
            (entry_point_get_position, pos5, ":belfry_next_entry_point_id"), #pos5 holds belfry next entry point target during its path
          (else_try),
            (copy_position, pos5, pos11),    
          (try_end),
        
          (get_distance_between_positions, ":belfry_next_entry_point_distance", pos1, pos5),
        
          #collecting scene prop ids of belfry parts
          (try_begin),
            (eq, ":belfry_kind", 0),
            #belfry platform_a
            (scene_prop_get_instance, ":belfry_platform_a_scene_prop_id", "spr_belfry_platform_a", ":belfry_no"),
            #belfry platform_b
            (scene_prop_get_instance, ":belfry_platform_b_scene_prop_id", "spr_belfry_platform_b", ":belfry_no"),
          (else_try),
            #belfry platform_a
            (scene_prop_get_instance, ":belfry_platform_a_scene_prop_id", "spr_belfry_b_platform_a", ":belfry_no"),
          (try_end),
    
          #belfry wheel_1
          (store_mul, ":wheel_no", ":belfry_no", 3),
          (try_begin),
            (eq, ":belfry_body_scene_prop", "spr_belfry_b"),
            (scene_prop_get_num_instances, ":number_of_belfry_a", "spr_belfry_a"),    
            (store_mul, ":number_of_belfry_a_wheels", ":number_of_belfry_a", 3),
            (val_add, ":wheel_no", ":number_of_belfry_a_wheels"),
          (try_end),
          (scene_prop_get_instance, ":belfry_wheel_1_scene_prop_id", "spr_belfry_wheel", ":wheel_no"),
          #belfry wheel_2
          (val_add, ":wheel_no", 1),
          (scene_prop_get_instance, ":belfry_wheel_2_scene_prop_id", "spr_belfry_wheel", ":wheel_no"),
          #belfry wheel_3
          (val_add, ":wheel_no", 1),
          (scene_prop_get_instance, ":belfry_wheel_3_scene_prop_id", "spr_belfry_wheel", ":wheel_no"),

          (init_position, pos17),
          (position_move_y, pos17, -225),
          (position_transform_position_to_parent, pos18, pos1, pos17),
          (position_move_y, pos17, -225),
          (position_transform_position_to_parent, pos19, pos1, pos17),

          (assign, ":number_of_agents_around_belfry", 0),
          (get_max_players, ":num_players"),
          (try_for_range, ":player_no", 0, ":num_players"),
            (player_is_active, ":player_no"),
            (player_get_agent_id, ":agent_id", ":player_no"),
            (ge, ":agent_id", 0),
            (agent_get_team, ":agent_team", ":agent_id"),
            (eq, ":agent_team", 1), #only team2 players allowed to move belfry (team which spawns outside the castle (team1 = 0, team2 = 1))
            (agent_get_horse, ":agent_horse_id", ":agent_id"),
            (eq, ":agent_horse_id", -1),
            (agent_get_position, pos2, ":agent_id"),
            (get_sq_distance_between_positions_in_meters, ":dist_between_agent_and_belfry", pos18, pos2),

            (lt, ":dist_between_agent_and_belfry", multi_distance_sq_to_use_belfry), #must be at most 10m * 10m = 100m away from the player
            (neg|scene_prop_has_agent_on_it, ":belfry_scene_prop_id", ":agent_id"),
            (neg|scene_prop_has_agent_on_it, ":belfry_platform_a_scene_prop_id", ":agent_id"),

            (this_or_next|eq, ":belfry_kind", 1), #there is this_or_next here because belfry_b has no platform_b
            (neg|scene_prop_has_agent_on_it, ":belfry_platform_b_scene_prop_id", ":agent_id"),
    
            (neg|scene_prop_has_agent_on_it, ":belfry_wheel_1_scene_prop_id", ":agent_id"),#can be removed to make faster
            (neg|scene_prop_has_agent_on_it, ":belfry_wheel_2_scene_prop_id", ":agent_id"),#can be removed to make faster
            (neg|scene_prop_has_agent_on_it, ":belfry_wheel_3_scene_prop_id", ":agent_id"),#can be removed to make faster
            (neg|position_is_behind_position, pos2, pos19),
            (position_is_behind_position, pos2, pos1),
            (val_add, ":number_of_agents_around_belfry", 1),        
          (try_end),

          (val_min, ":number_of_agents_around_belfry", 16),

          (try_begin),
            (scene_prop_get_slot, ":pre_number_of_agents_around_belfry", ":belfry_scene_prop_id", scene_prop_number_of_agents_pushing),
            (scene_prop_get_slot, ":next_entry_point_id", ":belfry_scene_prop_id", scene_prop_next_entry_point_id),
            (this_or_next|neq, ":pre_number_of_agents_around_belfry", ":number_of_agents_around_belfry"),
            (neq, ":next_entry_point_id", ":belfry_next_entry_point_id"),

            (try_begin),
              (eq, ":next_entry_point_id", ":belfry_next_entry_point_id"), #if we are still targetting same entry point subtract 
              (prop_instance_is_animating, ":is_animating", ":belfry_scene_prop_id"),
              (eq, ":is_animating", 1),

              (store_mul, ":sqrt_number_of_agents_around_belfry", "$g_last_number_of_agents_around_belfry", 100),
              (store_sqrt, ":sqrt_number_of_agents_around_belfry", ":sqrt_number_of_agents_around_belfry"),
              (val_min, ":sqrt_number_of_agents_around_belfry", 300),
              (assign, ":distance", ":belfry_next_entry_point_distance"),
              (val_mul, ":distance", ":sqrt_number_of_agents_around_belfry"),
              (val_div, ":distance", 100), #100 is because of fixed_point_multiplier
              (val_mul, ":distance", 4), #multiplying with 4 to make belfry pushing process slower, 
                                                                 #with 16 agents belfry will go with 4 / 4 = 1 speed (max), with 1 agent belfry will go with 1 / 4 = 0.25 speed (min)    
            (try_end),

            (try_begin),
              (ge, ":belfry_next_entry_point_id", 0),

              #up down rotation of belfry's next entry point
              (init_position, pos9),
              (position_set_y, pos9, -500), #go 5.0 meters back
              (position_set_x, pos9, -300), #go 3.0 meters left
              (position_transform_position_to_parent, pos10, pos5, pos9), 
              (position_get_distance_to_terrain, ":height_to_terrain_1", pos10), #learn distance between 5 meters back of entry point(pos10) and ground level at left part of belfry
      
              (init_position, pos9),
              (position_set_y, pos9, -500), #go 5.0 meters back
              (position_set_x, pos9, 300), #go 3.0 meters right
              (position_transform_position_to_parent, pos10, pos5, pos9), 
              (position_get_distance_to_terrain, ":height_to_terrain_2", pos10), #learn distance between 5 meters back of entry point(pos10) and ground level at right part of belfry

              (store_add, ":height_to_terrain", ":height_to_terrain_1", ":height_to_terrain_2"),
              (val_mul, ":height_to_terrain", 100), #because of fixed point multiplier

              (store_div, ":rotate_angle_of_next_entry_point", ":height_to_terrain", 24), #if there is 1 meters of distance (100cm) then next target position will rotate by 2 degrees. #ac sonra
              (init_position, pos20),    
              (position_rotate_x_floating, pos20, ":rotate_angle_of_next_entry_point"),
              (position_transform_position_to_parent, pos23, pos5, pos20),

              #right left rotation of belfry's next entry point
              (init_position, pos9),
              (position_set_x, pos9, -300), #go 3.0 meters left
              (position_transform_position_to_parent, pos10, pos5, pos9), #applying 3.0 meters in -x to position of next entry point target, final result is in pos10
              (position_get_distance_to_terrain, ":height_to_terrain_at_left", pos10), #learn distance between 3.0 meters left of entry point(pos10) and ground level
              (init_position, pos9),
              (position_set_x, pos9, 300), #go 3.0 meters left
              (position_transform_position_to_parent, pos10, pos5, pos9), #applying 3.0 meters in x to position of next entry point target, final result is in pos10
              (position_get_distance_to_terrain, ":height_to_terrain_at_right", pos10), #learn distance between 3.0 meters right of entry point(pos10) and ground level
              (store_sub, ":height_to_terrain_1", ":height_to_terrain_at_left", ":height_to_terrain_at_right"),

              (init_position, pos9),
              (position_set_x, pos9, -300), #go 3.0 meters left
              (position_set_y, pos9, -500), #go 5.0 meters forward
              (position_transform_position_to_parent, pos10, pos5, pos9), #applying 3.0 meters in -x to position of next entry point target, final result is in pos10
              (position_get_distance_to_terrain, ":height_to_terrain_at_left", pos10), #learn distance between 3.0 meters left of entry point(pos10) and ground level
              (init_position, pos9),
              (position_set_x, pos9, 300), #go 3.0 meters left
              (position_set_y, pos9, -500), #go 5.0 meters forward
              (position_transform_position_to_parent, pos10, pos5, pos9), #applying 3.0 meters in x to position of next entry point target, final result is in pos10
              (position_get_distance_to_terrain, ":height_to_terrain_at_right", pos10), #learn distance between 3.0 meters right of entry point(pos10) and ground level
              (store_sub, ":height_to_terrain_2", ":height_to_terrain_at_left", ":height_to_terrain_at_right"),

              (store_add, ":height_to_terrain", ":height_to_terrain_1", ":height_to_terrain_2"),    
              (val_mul, ":height_to_terrain", 100), #100 is because of fixed_point_multiplier
              (store_div, ":rotate_angle_of_next_entry_point", ":height_to_terrain", 24), #if there is 1 meters of distance (100cm) then next target position will rotate by 25 degrees. 
              (val_mul, ":rotate_angle_of_next_entry_point", -1),

              (init_position, pos20),
              (position_rotate_y_floating, pos20, ":rotate_angle_of_next_entry_point"),
              (position_transform_position_to_parent, pos22, pos23, pos20),
            (else_try),
              (copy_position, pos22, pos5),      
            (try_end),
              
            (try_begin),
              (ge, ":number_of_agents_around_belfry", 1), #if there is any agents pushing belfry

              (store_mul, ":sqrt_number_of_agents_around_belfry", ":number_of_agents_around_belfry", 100),
              (store_sqrt, ":sqrt_number_of_agents_around_belfry", ":sqrt_number_of_agents_around_belfry"),
              (val_min, ":sqrt_number_of_agents_around_belfry", 300),
              (val_mul, ":belfry_next_entry_point_distance", 100), #100 is because of fixed_point_multiplier
              (val_mul, ":belfry_next_entry_point_distance", 3), #multiplying with 3 to make belfry pushing process slower, 
                                                                 #with 9 agents belfry will go with 3 / 3 = 1 speed (max), with 1 agent belfry will go with 1 / 3 = 0.33 speed (min)    
              (val_div, ":belfry_next_entry_point_distance", ":sqrt_number_of_agents_around_belfry"),
              #calculating destination coordinates of belfry parts
              #belfry platform_a
              (prop_instance_get_position, pos6, ":belfry_platform_a_scene_prop_id"),
              (position_transform_position_to_local, pos7, pos1, pos6),
              (position_transform_position_to_parent, pos8, pos22, pos7),
              (prop_instance_animate_to_position, ":belfry_platform_a_scene_prop_id", pos8, ":belfry_next_entry_point_distance"),    
              #belfry platform_b
              (try_begin),
                (eq, ":belfry_kind", 0),
                (prop_instance_get_position, pos6, ":belfry_platform_b_scene_prop_id"),
                (position_transform_position_to_local, pos7, pos1, pos6),
                (position_transform_position_to_parent, pos8, pos22, pos7),
                (prop_instance_animate_to_position, ":belfry_platform_b_scene_prop_id", pos8, ":belfry_next_entry_point_distance"),
              (try_end),
              #wheel rotation
              (store_mul, ":belfry_wheel_rotation", ":belfry_next_entry_point_distance", -25),
              #(val_add, "$g_belfry_wheel_rotation", ":belfry_wheel_rotation"),
              (assign, "$g_last_number_of_agents_around_belfry", ":number_of_agents_around_belfry"),

              #belfry wheel_1
              #(prop_instance_get_starting_position, pos13, ":belfry_wheel_1_scene_prop_id"),
              (prop_instance_get_position, pos13, ":belfry_wheel_1_scene_prop_id"),
              (prop_instance_get_position, pos20, ":belfry_scene_prop_id"),
              (position_transform_position_to_local, pos7, pos20, pos13),
              (position_transform_position_to_parent, pos21, pos22, pos7),
              (prop_instance_rotate_to_position, ":belfry_wheel_1_scene_prop_id", pos21, ":belfry_next_entry_point_distance", ":belfry_wheel_rotation"),
      
              #belfry wheel_2
              #(prop_instance_get_starting_position, pos13, ":belfry_wheel_2_scene_prop_id"),
              (prop_instance_get_position, pos13, ":belfry_wheel_2_scene_prop_id"),
              (prop_instance_get_position, pos20, ":belfry_scene_prop_id"),
              (position_transform_position_to_local, pos7, pos20, pos13),
              (position_transform_position_to_parent, pos21, pos22, pos7),
              (prop_instance_rotate_to_position, ":belfry_wheel_2_scene_prop_id", pos21, ":belfry_next_entry_point_distance", ":belfry_wheel_rotation"),
      
              #belfry wheel_3
              (prop_instance_get_position, pos13, ":belfry_wheel_3_scene_prop_id"),
              (prop_instance_get_position, pos20, ":belfry_scene_prop_id"),
              (position_transform_position_to_local, pos7, pos20, pos13),
              (position_transform_position_to_parent, pos21, pos22, pos7),
              (prop_instance_rotate_to_position, ":belfry_wheel_3_scene_prop_id", pos21, ":belfry_next_entry_point_distance", ":belfry_wheel_rotation"),

              #belfry main body
              (prop_instance_animate_to_position, ":belfry_scene_prop_id", pos22, ":belfry_next_entry_point_distance"),    
            (else_try),
              (prop_instance_is_animating, ":is_animating", ":belfry_scene_prop_id"),
              (eq, ":is_animating", 1),

              #belfry platform_a
              (prop_instance_stop_animating, ":belfry_platform_a_scene_prop_id"),
              #belfry platform_b
              (try_begin),
                (eq, ":belfry_kind", 0),
                (prop_instance_stop_animating, ":belfry_platform_b_scene_prop_id"),
              (try_end),
              #belfry wheel_1
              (prop_instance_stop_animating, ":belfry_wheel_1_scene_prop_id"),
              #belfry wheel_2
              (prop_instance_stop_animating, ":belfry_wheel_2_scene_prop_id"),
              #belfry wheel_3
              (prop_instance_stop_animating, ":belfry_wheel_3_scene_prop_id"),
              #belfry main body
              (prop_instance_stop_animating, ":belfry_scene_prop_id"),
            (try_end),
        
            (scene_prop_set_slot, ":belfry_scene_prop_id", scene_prop_number_of_agents_pushing, ":number_of_agents_around_belfry"),    
            (scene_prop_set_slot, ":belfry_scene_prop_id", scene_prop_next_entry_point_id, ":belfry_next_entry_point_id"),
          (try_end),
        (else_try),
          (le, ":dist_between_belfry_and_its_destination", 4),
          (scene_prop_slot_eq, ":belfry_scene_prop_id", scene_prop_belfry_platform_moved, 0),
      
          (scene_prop_set_slot, ":belfry_scene_prop_id", scene_prop_belfry_platform_moved, 1),    

          (try_begin),
            (eq, ":belfry_kind", 0),
            (scene_prop_get_instance, ":belfry_platform_a_scene_prop_id", "spr_belfry_platform_a", ":belfry_no"),
          (else_try),
            (scene_prop_get_instance, ":belfry_platform_a_scene_prop_id", "spr_belfry_b_platform_a", ":belfry_no"),
          (try_end),
    
          (prop_instance_get_starting_position, pos0, ":belfry_platform_a_scene_prop_id"),
          (prop_instance_animate_to_position, ":belfry_platform_a_scene_prop_id", pos0, 400),    
        (try_end),
      (try_end),
    (try_end),
    ])

multiplayer_server_spawn_bots = (
  0, 0, 0, [],
  [
    (multiplayer_is_server),
    (eq, "$g_multiplayer_ready_for_spawning_agent", 1),
    (store_add, ":total_req", "$g_multiplayer_num_bots_required_team_1", "$g_multiplayer_num_bots_required_team_2"),
    (try_begin),
      (gt, ":total_req", 0),

      (try_begin),
        (this_or_next|eq, "$g_multiplayer_game_type", multiplayer_game_type_battle),
        (this_or_next|eq, "$g_multiplayer_game_type", multiplayer_game_type_destroy),
        (eq, "$g_multiplayer_game_type", multiplayer_game_type_siege),

        (team_get_score, ":team_1_score", 0),
        (team_get_score, ":team_2_score", 1),

        (store_add, ":current_round", ":team_1_score", ":team_2_score"),
        (eq, ":current_round", 0),

        (store_mission_timer_a, ":round_time"),
        (val_sub, ":round_time", "$g_round_start_time"),
        (lt, ":round_time", 20),

        (assign, ":rounded_game_first_round_time_limit_past", 0),
      (else_try),
        (assign, ":rounded_game_first_round_time_limit_past", 1),
      (try_end),
    
      (eq, ":rounded_game_first_round_time_limit_past", 1),
    
      (store_random_in_range, ":random_req", 0, ":total_req"),
      (val_sub, ":random_req", "$g_multiplayer_num_bots_required_team_1"),
      (try_begin),
        (lt, ":random_req", 0),
        #add to team 1
        (assign, ":selected_team", 0),
      (else_try),
        #add to team 2
        (assign, ":selected_team", 1),
      (try_end),

      (try_begin),
        (this_or_next|eq, "$g_multiplayer_game_type", multiplayer_game_type_battle),
        (eq, "$g_multiplayer_game_type", multiplayer_game_type_destroy),

        (store_mission_timer_a, ":round_time"),
        (val_sub, ":round_time", "$g_round_start_time"),

        (try_begin),
          (le, ":round_time", 20),
          (assign, ":look_only_actives", 0),
        (else_try),
          (assign, ":look_only_actives", 1),
        (try_end),
      (else_try),
        (assign, ":look_only_actives", 1),
      (try_end),
    
      (call_script, "script_multiplayer_find_bot_troop_and_group_for_spawn", ":selected_team", ":look_only_actives"),
      (assign, ":selected_troop", reg0),
      (assign, ":selected_group", reg1),

      (team_get_faction, ":team_faction", ":selected_team"),
      (assign, ":num_ai_troops", 0),
      (try_for_range, ":cur_ai_troop", multiplayer_ai_troops_begin, multiplayer_ai_troops_end),
        (store_troop_faction, ":ai_troop_faction", ":cur_ai_troop"),
        (eq, ":ai_troop_faction", ":team_faction"),
        (val_add, ":num_ai_troops", 1),
      (try_end),

      (assign, ":number_of_active_players_wanted_bot", 0),

      (get_max_players, ":num_players"),
      (try_for_range, ":player_no", 0, ":num_players"),
        (player_is_active, ":player_no"),
        (player_get_team_no, ":player_team_no", ":player_no"),
        (eq, ":selected_team", ":player_team_no"),

        (assign, ":ai_wanted", 0),
        (store_add, ":end_cond", slot_player_bot_type_1_wanted, ":num_ai_troops"),
        (try_for_range, ":bot_type_wanted_slot", slot_player_bot_type_1_wanted, ":end_cond"),
          (player_slot_ge, ":player_no", ":bot_type_wanted_slot", 1),
          (assign, ":ai_wanted", 1),
          (assign, ":end_cond", 0), 
        (try_end),

        (ge, ":ai_wanted", 1),

        (val_add, ":number_of_active_players_wanted_bot", 1),
      (try_end),

      (try_begin),
        (this_or_next|ge, ":selected_group", 0),
        (eq, ":number_of_active_players_wanted_bot", 0),

        (troop_get_inventory_slot, ":has_item", ":selected_troop", ek_horse),
        (try_begin),
          (ge, ":has_item", 0),
          (assign, ":is_horseman", 1),
        (else_try),
          (assign, ":is_horseman", 0),
        (try_end),

        (try_begin),
          (eq, "$g_multiplayer_game_type", multiplayer_game_type_siege),

          (store_mission_timer_a, ":round_time"),
          (val_sub, ":round_time", "$g_round_start_time"),

          (try_begin),
            (lt, ":round_time", 20), #at start of game spawn at base entry point
            (try_begin),
              (eq, ":selected_team", 0),
              (call_script, "script_multiplayer_find_spawn_point", ":selected_team", 1, ":is_horseman"), 
            (else_try),
              (assign, reg0, multi_initial_spawn_point_team_2),
            (try_end),
          (else_try),
            (call_script, "script_multiplayer_find_spawn_point", ":selected_team", 0, ":is_horseman"), 
          (try_end),
        (else_try),
          (this_or_next|eq, "$g_multiplayer_game_type", multiplayer_game_type_battle),
          (eq, "$g_multiplayer_game_type", multiplayer_game_type_destroy),
      
          (try_begin),
            (eq, ":selected_team", 0),
            (assign, reg0, 0),
          (else_try),
            (assign, reg0, 32),
          (try_end),
        (else_try),
          (call_script, "script_multiplayer_find_spawn_point", ":selected_team", 0, ":is_horseman"), 
        (try_end),
      
        (store_current_scene, ":cur_scene"),
        (modify_visitors_at_site, ":cur_scene"),
        (add_visitors_to_current_scene, reg0, ":selected_troop", 1, ":selected_team", ":selected_group"),
        (assign, "$g_multiplayer_ready_for_spawning_agent", 0),

        (try_begin),
          (eq, ":selected_team", 0),
          (val_sub, "$g_multiplayer_num_bots_required_team_1", 1),
        (else_try),
          (eq, ":selected_team", 1),
          (val_sub, "$g_multiplayer_num_bots_required_team_2", 1),
        (try_end),
      (try_end),
    (try_end),    
    ])

multiplayer_server_manage_bots = (
  3, 0, 0, [],
  [
    (multiplayer_is_server),
    (try_for_agents, ":cur_agent"),
      (agent_is_non_player, ":cur_agent"),
      (agent_is_human, ":cur_agent"),
      (agent_is_alive, ":cur_agent"),
      (agent_get_group, ":agent_group", ":cur_agent"),
      (try_begin),
        (neg|player_is_active, ":agent_group"),
        (call_script, "script_multiplayer_change_leader_of_bot", ":cur_agent"),
      (else_try),
        (player_get_team_no, ":leader_team_no", ":agent_group"),
        (agent_get_team, ":agent_team", ":cur_agent"),
        (neq, ":leader_team_no", ":agent_team"),
        (call_script, "script_multiplayer_change_leader_of_bot", ":cur_agent"),
      (try_end),
    (try_end),
    ])

multiplayer_server_check_polls = (
  1, 5, 0,
  [
    (multiplayer_is_server),
    (eq, "$g_multiplayer_poll_running", 1),
    (eq, "$g_multiplayer_poll_ended", 0),
    (store_mission_timer_a, ":mission_timer"),
    (store_add, ":total_votes", "$g_multiplayer_poll_no_count", "$g_multiplayer_poll_yes_count"),
    (this_or_next|eq, ":total_votes", "$g_multiplayer_poll_num_sent"),
    (gt, ":mission_timer", "$g_multiplayer_poll_end_time"),
    (call_script, "script_cf_multiplayer_evaluate_poll"),
    ],
  [
    (assign, "$g_multiplayer_poll_running", 0),
    (try_begin),
      (this_or_next|eq, "$g_multiplayer_poll_to_show", 0), #change map
      (eq, "$g_multiplayer_poll_to_show", 3), #change map with factions
      (call_script, "script_game_multiplayer_get_game_type_mission_template", "$g_multiplayer_game_type"),
      (start_multiplayer_mission, reg0, "$g_multiplayer_poll_value_to_show", 1),
      (call_script, "script_game_set_multiplayer_mission_end"),
    (try_end),
    ])
    
multiplayer_server_check_end_map = ( 
  1, 0, 0, [],
  [
    (multiplayer_is_server),
    #checking for restarting the map
    (assign, ":end_map", 0),
#INVASION MODE START
	(try_begin),
	  (eq, "$g_multiplayer_game_type", multiplayer_game_type_captain_coop),
	  (try_begin),
		(eq, "$g_round_ended", 1),
		(assign, ":end_map", 1),
	  (try_end),
	(else_try),
#INVASION MODE END
      (this_or_next|eq, "$g_multiplayer_game_type", multiplayer_game_type_battle),
      (this_or_next|eq, "$g_multiplayer_game_type", multiplayer_game_type_destroy),
      (eq, "$g_multiplayer_game_type", multiplayer_game_type_siege),
    
      (try_begin),
        (eq, "$g_round_ended", 1),

        (store_mission_timer_a, ":seconds_past_till_round_ended"),
        (val_sub, ":seconds_past_till_round_ended", "$g_round_finish_time"),
        (store_sub, ":multiplayer_respawn_period_minus_one", "$g_multiplayer_respawn_period", 1),
        (ge, ":seconds_past_till_round_ended", ":multiplayer_respawn_period_minus_one"),
  
        (store_mission_timer_a, ":mission_timer"),    
        (try_begin),
          (this_or_next|eq, "$g_multiplayer_game_type", multiplayer_game_type_battle),
          (eq, "$g_multiplayer_game_type", multiplayer_game_type_destroy),
          (assign, ":reduce_amount", 90),
        (else_try),
          (assign, ":reduce_amount", 120),
        (try_end),
    
        (store_mul, ":game_max_seconds", "$g_multiplayer_game_max_minutes", 60),
        (store_sub, ":game_max_seconds_min_n_seconds", ":game_max_seconds", ":reduce_amount"), #when round ends if there are 60 seconds to map change time then change map without completing exact map time.
        (gt, ":mission_timer", ":game_max_seconds_min_n_seconds"),
        (assign, ":end_map", 1),
      (try_end),
      
      (eq, ":end_map", 1),
    (else_try),
      (neq, "$g_multiplayer_game_type", multiplayer_game_type_battle), #battle mod has different end map condition by time
      (neq, "$g_multiplayer_game_type", multiplayer_game_type_destroy), #fight and destroy mod has different end map condition by time
      (neq, "$g_multiplayer_game_type", multiplayer_game_type_siege), #siege mod has different end map condition by time
      (neq, "$g_multiplayer_game_type", multiplayer_game_type_headquarters), #in headquarters mod game cannot limited by time, only can be limited by score.
      (store_mission_timer_a, ":mission_timer"),
      (store_mul, ":game_max_seconds", "$g_multiplayer_game_max_minutes", 60),
      (gt, ":mission_timer", ":game_max_seconds"),
      (assign, ":end_map", 1),
    (else_try),
      #assuming only 2 teams in scene
      (team_get_score, ":team_1_score", 0),
      (team_get_score, ":team_2_score", 1),
      (try_begin),
        (neq, "$g_multiplayer_game_type", multiplayer_game_type_headquarters), #for not-headquarters mods
        (try_begin),
          (this_or_next|ge, ":team_1_score", "$g_multiplayer_game_max_points"),
          (ge, ":team_2_score", "$g_multiplayer_game_max_points"),
          (assign, ":end_map", 1),
        (try_end),
      (else_try),
        (assign, ":at_least_one_player_is_at_game", 0),
        (get_max_players, ":num_players"),
        (try_for_range, ":player_no", 0, ":num_players"),
          (player_is_active, ":player_no"),
          (player_get_agent_id, ":agent_id", ":player_no"),
          (ge, ":agent_id", 0),
          (neg|agent_is_non_player, ":agent_id"),
          (assign, ":at_least_one_player_is_at_game", 1),
          (assign, ":num_players", 0),
        (try_end),
    
        (eq, ":at_least_one_player_is_at_game", 1),

        (this_or_next|le, ":team_1_score", 0), #in headquarters game ends only if one team has 0 score.
        (le, ":team_2_score", 0),
        (assign, ":end_map", 1),
      (try_end),
    (try_end),
    (try_begin),
      (eq, ":end_map", 1),
      (call_script, "script_game_multiplayer_get_game_type_mission_template", "$g_multiplayer_game_type"),
      (start_multiplayer_mission, reg0, "$g_multiplayer_selected_map", 0),
      (call_script, "script_game_set_multiplayer_mission_end"),           
    (try_end),
    ])

multiplayer_once_at_the_first_frame = (
  0, 0, ti_once, [], [
    (start_presentation, "prsnt_multiplayer_welcome_message"),
    ])

multiplayer_battle_window_opened = (
  ti_battle_window_opened, 0, 0, [], [
    (start_presentation, "prsnt_multiplayer_team_score_display"),
    ])


common_battle_mission_start = (
  ti_before_mission_start, 0, 0, [],
  [
    (team_set_relation, 0, 2, 1),
    (team_set_relation, 1, 3, 1),
    (call_script, "script_change_banners_and_chest"),
    ])

common_battle_tab_press = (
  ti_tab_pressed, 0, 0, [],
  [
    (try_begin),
      (eq, "$g_battle_won", 1),
      (call_script, "script_count_mission_casualties_from_agents"),
      (finish_mission,0),
    (else_try),
      (call_script, "script_cf_check_enemies_nearby"),
      (question_box,"str_do_you_want_to_retreat"),
    (else_try),
      (display_message,"str_can_not_retreat"),
    (try_end),
    ])

common_battle_init_banner = (
  ti_on_agent_spawn, 0, 0, [],
  [
    (store_trigger_param_1, ":agent_no"),
    (agent_get_troop_id, ":troop_no", ":agent_no"),
    (call_script, "script_troop_agent_set_banner", "tableau_game_troop_label_banner", ":agent_no", ":troop_no"),
  ])


common_arena_fight_tab_press = (
  ti_tab_pressed, 0, 0, [],
  [
    (question_box,"str_give_up_fight"),
    ])

common_custom_battle_tab_press = (
  ti_tab_pressed, 0, 0, [],
  [
    (try_begin),
      (neq, "$g_battle_result", 0),
      (call_script, "script_custom_battle_end"),
      (finish_mission),
    (else_try),
      (question_box,"str_give_up_fight"),
      (try_end),
    ])

custom_battle_check_victory_condition = (
  1, 60, ti_once,
  [
    (store_mission_timer_a,reg(1)),
    (ge,reg(1),10),
    (all_enemies_defeated, 2),
    (neg|main_hero_fallen, 0),
    (set_mission_result,1),
    (display_message,"str_msg_battle_won"),
    (assign, "$g_battle_won",1),
    (assign, "$g_battle_result", 1),
    ],
  [
    (call_script, "script_custom_battle_end"),
    (finish_mission, 1),
    ])

custom_battle_check_defeat_condition = (
  1, 4, ti_once,
  [
    (main_hero_fallen),
    (assign,"$g_battle_result",-1),
    ],
  [
    (call_script, "script_custom_battle_end"),
    (finish_mission),
    ])

common_battle_victory_display = (
  10, 0, 0, [],
  [
    (eq,"$g_battle_won",1),
    (display_message,"str_msg_battle_won"),
    ])

common_siege_question_answered = (
  ti_question_answered, 0, 0, [],
   [
     (store_trigger_param_1,":answer"),
     (eq,":answer",0),
     (assign, "$pin_player_fallen", 0),
     (get_player_agent_no, ":player_agent"),
     (agent_get_team, ":agent_team", ":player_agent"),
     (try_begin),
       (neq, "$attacker_team", ":agent_team"),
       (neq, "$attacker_team_2", ":agent_team"),
       (str_store_string, s5, "str_siege_continues"),
       (call_script, "script_simulate_retreat", 8, 15, 0),
     (else_try),
       (str_store_string, s5, "str_retreat"),
       (call_script, "script_simulate_retreat", 5, 20, 0),
     (try_end),
     (call_script, "script_count_mission_casualties_from_agents"),
     (finish_mission,0),
     ])

common_custom_battle_question_answered = (
   ti_question_answered, 0, 0, [],
   [
     (store_trigger_param_1,":answer"),
     (eq,":answer",0),
     (assign, "$g_battle_result", -1),
     (call_script, "script_custom_battle_end"),
     (finish_mission),
     ])

common_custom_siege_init = (
  0, 0, ti_once, [],
  [
    (assign, "$g_battle_result", 0),
    (call_script, "script_music_set_situation_with_culture", mtf_sit_siege),
    ])

common_siege_init = (
  0, 0, ti_once, [],
  [
    (assign,"$g_battle_won",0),
    (assign,"$defender_reinforcement_stage",0),
    (assign,"$attacker_reinforcement_stage",0),
    (call_script, "script_music_set_situation_with_culture", mtf_sit_siege),
    ])

common_music_situation_update = (
  30, 0, 0, [],
  [
    (call_script, "script_combat_music_set_situation_with_culture"),
    ])

common_siege_ai_trigger_init = (
  0, 0, ti_once,
  [
    (assign, "$defender_team", 0),
    (assign, "$attacker_team", 1),
    (assign, "$defender_team_2", 2),
    (assign, "$attacker_team_2", 3),
    ], [])

common_siege_ai_trigger_init_2 = (
  0, 0, ti_once,
  [
    (set_show_messages, 0),
    (entry_point_get_position, pos10, 10),
    (try_for_range, ":cur_group", 0, grc_everyone),
      (neq, ":cur_group", grc_archers),
      (team_give_order, "$defender_team", ":cur_group", mordr_hold),
      (team_give_order, "$defender_team", ":cur_group", mordr_stand_closer),
      (team_give_order, "$defender_team", ":cur_group", mordr_stand_closer),
      (team_give_order, "$defender_team_2", ":cur_group", mordr_hold),
      (team_give_order, "$defender_team_2", ":cur_group", mordr_stand_closer),
      (team_give_order, "$defender_team_2", ":cur_group", mordr_stand_closer),
    (try_end),
    (team_give_order, "$defender_team", grc_archers, mordr_stand_ground),
    (team_set_order_position, "$defender_team", grc_everyone, pos10),
    (team_give_order, "$defender_team_2", grc_archers, mordr_stand_ground),
    (team_set_order_position, "$defender_team_2", grc_everyone, pos10),
    (set_show_messages, 1),
    ], [])

common_siege_ai_trigger_init_after_2_secs = (
  0, 2, ti_once, [],
  [
    (try_for_agents, ":agent_no"),
      (agent_set_slot, ":agent_no", slot_agent_is_not_reinforcement, 1),
    (try_end),
    ])

common_siege_defender_reinforcement_check = (
  3, 0, 5, [],
  [(lt, "$defender_reinforcement_stage", 7),
   (store_mission_timer_a,":mission_time"),
   (ge,":mission_time",10),
   (store_normalized_team_count,":num_defenders",0),
   (lt,":num_defenders",8),
   (add_reinforcements_to_entry,4, 7),
   (val_add,"$defender_reinforcement_stage",1),
   (try_begin),
     (gt, ":mission_time", 300), #5 minutes, don't let small armies charge
     (get_player_agent_no, ":player_agent"),
     (agent_get_team, ":player_team", ":player_agent"),
     (neq, ":player_team", "$defender_team"), #player should be the attacker
     (neq, ":player_team", "$defender_team_2"), #player should be the attacker
     (ge, "$defender_reinforcement_stage", 2),
     (set_show_messages, 0),
     (team_give_order, "$defender_team", grc_infantry, mordr_charge), #AI desperate charge:infantry!!!
     (team_give_order, "$defender_team_2", grc_infantry, mordr_charge), #AI desperate charge:infantry!!!
     (team_give_order, "$defender_team", grc_cavalry, mordr_charge), #AI desperate charge:cavalry!!!
     (team_give_order, "$defender_team_2", grc_cavalry, mordr_charge), #AI desperate charge:cavalry!!!
     (set_show_messages, 1),
     (ge, "$defender_reinforcement_stage", 4),
     (set_show_messages, 0),
     (team_give_order, "$defender_team", grc_everyone, mordr_charge), #AI desperate charge: everyone!!!
     (team_give_order, "$defender_team_2", grc_everyone, mordr_charge), #AI desperate charge: everyone!!!
     (set_show_messages, 1),
   (try_end),
   ])

common_siege_defender_reinforcement_archer_reposition = (
  2, 0, 0,
  [
    (gt, "$defender_reinforcement_stage", 0),
    ],
  [
    (call_script, "script_siege_move_archers_to_archer_positions"),
    ])

common_siege_attacker_reinforcement_check = (
  1, 0, 5,
  [
    (lt,"$attacker_reinforcement_stage",5),
    (store_mission_timer_a,":mission_time"),
    (ge,":mission_time",10),
    (store_normalized_team_count,":num_attackers",1),
    (lt,":num_attackers",6)
    ],
  [
    (add_reinforcements_to_entry, 1, 8),
    (val_add,"$attacker_reinforcement_stage", 1),
    ])

common_siege_attacker_do_not_stall = (
  5, 0, 0, [],
  [ #Make sure attackers do not stall on the ladders...
    (try_for_agents, ":agent_no"),
      (agent_is_human, ":agent_no"),
      (agent_is_alive, ":agent_no"),
      (agent_get_team, ":agent_team", ":agent_no"),
      (this_or_next|eq, ":agent_team", "$attacker_team"),
      (eq, ":agent_team", "$attacker_team_2"),
      (agent_ai_set_always_attack_in_melee, ":agent_no", 1),
    (try_end),
    ])

common_battle_check_friendly_kills = (
  2, 0, 0, [],
  [
    (call_script, "script_check_friendly_kills"),
    ])

common_battle_check_victory_condition = (
  1, 60, ti_once,
  [
    (store_mission_timer_a,reg(1)),
    (ge,reg(1),10),
    (all_enemies_defeated, 5),
    (neg|main_hero_fallen, 0),
    (set_mission_result,1),
    (display_message,"str_msg_battle_won"),
    (assign,"$g_battle_won",1),
    (assign, "$g_battle_result", 1),
    (call_script, "script_play_victorious_sound"),
    ],
  [
    (call_script, "script_count_mission_casualties_from_agents"),
    (finish_mission, 1),
    ])

common_battle_victory_display = (
  10, 0, 0, [],
  [
    (eq,"$g_battle_won",1),
    (display_message,"str_msg_battle_won"),
    ])

common_siege_refill_ammo = (
  120, 0, 0, [],
  [#refill ammo of defenders every two minutes.
    (get_player_agent_no, ":player_agent"),
    (try_for_agents,":cur_agent"),
      (neq, ":cur_agent", ":player_agent"),
      (agent_is_alive, ":cur_agent"),
      (agent_is_human, ":cur_agent"),
##      (agent_is_defender, ":cur_agent"),
      (agent_get_team, ":agent_team", ":cur_agent"),
      (this_or_next|eq, ":agent_team", "$defender_team"),
      (eq, ":agent_team", "$defender_team_2"),
      (agent_refill_ammo, ":cur_agent"),
    (try_end),
    ])

common_siege_check_defeat_condition = (
  1, 4, ti_once,
  [
    (main_hero_fallen)
    ],
  [
    (assign, "$pin_player_fallen", 1),
    (get_player_agent_no, ":player_agent"),
    (agent_get_team, ":agent_team", ":player_agent"),
    (try_begin),
      (neq, "$attacker_team", ":agent_team"),
      (neq, "$attacker_team_2", ":agent_team"),
      (str_store_string, s5, "str_siege_continues"),
      (call_script, "script_simulate_retreat", 8, 15, 0),
    (else_try),
      (str_store_string, s5, "str_retreat"),
      (call_script, "script_simulate_retreat", 5, 20, 0),
    (try_end),
    (assign, "$g_battle_result", -1),
    (set_mission_result,-1),
    (call_script, "script_count_mission_casualties_from_agents"),
    (finish_mission,0),
    ])

common_battle_order_panel = (
  0, 0, 0, [],
  [
    (game_key_clicked, gk_view_orders),
    (neg|is_presentation_active, "prsnt_battle"),
    (start_presentation, "prsnt_battle"),
    ])

common_battle_order_panel_tick = (
  0.1, 0, 0, [],
  [
    (is_presentation_active, "prsnt_battle"),
    (call_script, "script_update_order_panel_statistics_and_map"),
    ])

common_battle_inventory = (
  ti_inventory_key_pressed, 0, 0, [],
  [
    (display_message,"str_use_baggage_for_inventory"),
    ])

common_inventory_not_available = (
  ti_inventory_key_pressed, 0, 0,
  [
    (display_message, "str_cant_use_inventory_now"),
    ], [])

common_siege_init_ai_and_belfry = (
  0, 0, ti_once,
  [
    (call_script, "script_siege_init_ai_and_belfry"),
    ], [])

common_siege_move_belfry = (
  0, 0, ti_once,
  [
    (call_script, "script_cf_siege_move_belfry"),
    ], [])

common_siege_rotate_belfry = (
  0, 2, ti_once,
  [
    (call_script, "script_cf_siege_rotate_belfry_platform"),
    ],
  [
    (assign, "$belfry_positioned", 3),
    ])

common_siege_assign_men_to_belfry = (
  0, 0, ti_once,
  [
    (call_script, "script_cf_siege_assign_men_to_belfry"),
    ], [])


tournament_triggers = [
  (ti_before_mission_start, 0, 0, [], [(call_script, "script_change_banners_and_chest"),
                                       (assign, "$g_arena_training_num_agents_spawned", 0)]),
  (ti_inventory_key_pressed, 0, 0, [(display_message,"str_cant_use_inventory_arena")], []),
  (ti_tab_pressed, 0, 0, [],
   [(try_begin),
      (eq, "$g_mt_mode", abm_visit),
      (set_trigger_result, 1),
    (else_try),
      (question_box,"str_give_up_fight"),
    (try_end),
    ]),
  (ti_question_answered, 0, 0, [],
   [(store_trigger_param_1,":answer"),
    (eq,":answer",0),
    (try_begin),
      (eq, "$g_mt_mode", abm_tournament),
      (call_script, "script_end_tournament_fight", 0),
    (else_try),
      (eq, "$g_mt_mode", abm_training),
      (get_player_agent_no, ":player_agent"),
      (agent_get_kill_count, "$g_arena_training_kills", ":player_agent", 1),#use this for conversation
    (try_end),
    (finish_mission,0),
    ]),

  (1, 0, ti_once, [], [
      (eq, "$g_mt_mode", abm_visit),
      (call_script, "script_music_set_situation_with_culture", mtf_sit_travel),
      (store_current_scene, reg(1)),
      (scene_set_slot, reg(1), slot_scene_visited, 1),
      (mission_enable_talk),
      (get_player_agent_no, ":player_agent"),
      (assign, ":team_set", 0),
      (try_for_agents, ":agent_no"),
        (neq, ":agent_no", ":player_agent"),
        (agent_get_troop_id, ":troop_id", ":agent_no"),
        (is_between, ":troop_id", regular_troops_begin, regular_troops_end),
        (eq, ":team_set", 0),
        (agent_set_team, ":agent_no", 1),
        (assign, ":team_set", 1),
      (try_end),
    ]),
##
##  (0, 0, 0, [],
##   [
##      #refresh hit points for arena visit trainers
##      (eq, "$g_mt_mode", abm_visit),
##      (get_player_agent_no, ":player_agent"),
##      (try_for_agents, ":agent_no"),
##        (neq, ":agent_no", ":player_agent"),
##        (agent_get_troop_id, ":troop_id", ":agent_no"),
##        (is_between, ":troop_id", regular_troops_begin, regular_troops_end),
##        (agent_set_hit_points, ":agent_no", 100),
##      (try_end),
##    ]),
  
##      (1, 4, ti_once, [(eq, "$g_mt_mode", abm_fight),
##                       (this_or_next|main_hero_fallen),
##                       (num_active_teams_le,1)],
##       [
##           (try_begin),
##             (num_active_teams_le,1),
##             (neg|main_hero_fallen),
##             (assign,"$arena_fight_won",1),
##             #Fight won, decrease odds
##             (assign, ":player_odds_sub", 0),
##             (try_begin),
##               (ge,"$arena_bet_amount",1),
##               (store_div, ":player_odds_sub", "$arena_win_amount", 2),
##             (try_end),
##             (party_get_slot, ":player_odds", "$g_encountered_party", slot_town_player_odds),
##             (val_add, ":player_odds_sub", 5),
##             (val_sub, ":player_odds", ":player_odds_sub"),
##             (val_max, ":player_odds", 250),
##             (party_set_slot, "$g_encountered_party", slot_town_player_odds, ":player_odds"),
##           (else_try),
##             #Fight lost, increase odds
##             (assign, ":player_odds_add", 0),
##             (try_begin),
##               (ge,"$arena_bet_amount",1),
##               (store_div, ":player_odds_add", "$arena_win_amount", 2),
##             (try_end),
##             (party_get_slot, ":player_odds", "$g_encountered_party", slot_town_player_odds),
##             (val_add, ":player_odds_add", 5),
##             (val_add, ":player_odds", ":player_odds_add"),
##             (val_min, ":player_odds", 4000),
##             (party_set_slot, "$g_encountered_party", slot_town_player_odds, ":player_odds"),
##           (try_end),
##           (store_remaining_team_no,"$arena_winner_team"),
##           (assign, "$g_mt_mode", abm_visit),
##           (party_get_slot, ":arena_mission_template", "$current_town", slot_town_arena_template),
##           (set_jump_mission, ":arena_mission_template"),
##           (party_get_slot, ":arena_scene", "$current_town", slot_town_arena),
##           (modify_visitors_at_site, ":arena_scene"),
##           (reset_visitors),
##           (set_visitor, 35, "trp_veteran_fighter"),
##           (set_visitor, 36, "trp_hired_blade"),
##           (set_jump_entry, 50),
##           (jump_to_scene, ":arena_scene"),
##           ]),
  
  (0, 0, ti_once, [],
   [
     (eq, "$g_mt_mode", abm_tournament),
     (play_sound, "snd_arena_ambiance", sf_looping),
     (call_script, "script_music_set_situation_with_culture", mtf_sit_arena),
     ]),

  (1, 4, ti_once, [(eq, "$g_mt_mode", abm_tournament),
                   (this_or_next|main_hero_fallen),
                   (num_active_teams_le, 1)],
   [
       (try_begin),
         (neg|main_hero_fallen),
         (call_script, "script_end_tournament_fight", 1),
         (call_script, "script_play_victorious_sound"),
         (finish_mission),
       (else_try),
         (call_script, "script_end_tournament_fight", 0),
         (finish_mission),
       (try_end),
       ]),

  (ti_battle_window_opened, 0, 0, [], [(eq, "$g_mt_mode", abm_training),(start_presentation, "prsnt_arena_training")]),
  
  (0, 0, ti_once, [], [(eq, "$g_mt_mode", abm_training),
                       (assign, "$g_arena_training_max_opponents", 40),
                       (assign, "$g_arena_training_num_agents_spawned", 0),
                       (assign, "$g_arena_training_kills", 0),
                       (assign, "$g_arena_training_won", 0),
                       (call_script, "script_music_set_situation_with_culture", mtf_sit_arena),
                       ]),

  (1, 4, ti_once, [(eq, "$g_mt_mode", abm_training),
                   (store_mission_timer_a, ":cur_time"),
                   (gt, ":cur_time", 3),
                   (assign, ":win_cond", 0),
                   (try_begin),
                     (ge, "$g_arena_training_num_agents_spawned", "$g_arena_training_max_opponents"),#spawn at most 40 agents
                     (num_active_teams_le, 1),
                     (assign, ":win_cond", 1),
                   (try_end),
                   (this_or_next|eq, ":win_cond", 1),
                   (main_hero_fallen)],
   [
       (get_player_agent_no, ":player_agent"),
       (agent_get_kill_count, "$g_arena_training_kills", ":player_agent", 1),#use this for conversation
       (assign, "$g_arena_training_won", 0),
       (try_begin),
         (neg|main_hero_fallen),
         (assign, "$g_arena_training_won", 1),#use this for conversation
       (try_end),
       (assign, "$g_mt_mode", abm_visit),
       (set_jump_mission, "mt_arena_melee_fight"),
       (party_get_slot, ":arena_scene", "$current_town", slot_town_arena),
       (modify_visitors_at_site, ":arena_scene"),
       (reset_visitors),
       (set_visitor, 35, "trp_veteran_fighter"),
       (set_visitor, 36, "trp_hired_blade"),
       (set_jump_entry, 50),
       (jump_to_scene, ":arena_scene"),
       ]),


  (0.2, 0, 0,
   [
       (eq, "$g_mt_mode", abm_training),
       (assign, ":num_active_fighters", 0),
       (try_for_agents, ":agent_no"),
         (agent_is_human, ":agent_no"),
         (agent_is_alive, ":agent_no"),
         (agent_get_team, ":team_no", ":agent_no"),
         (is_between, ":team_no", 0 ,7),
         (val_add, ":num_active_fighters", 1),
       (try_end),
       (lt, ":num_active_fighters", 7),
       (neg|main_hero_fallen),
       (store_mission_timer_a, ":cur_time"),
       (this_or_next|ge, ":cur_time", "$g_arena_training_next_spawn_time"),
       (this_or_next|lt, "$g_arena_training_num_agents_spawned", 6),
       (num_active_teams_le, 1),
       (lt, "$g_arena_training_num_agents_spawned", "$g_arena_training_max_opponents"),
      ],
    [
       (assign, ":added_troop", "$g_arena_training_num_agents_spawned"),
       (store_div,  ":added_troop", "$g_arena_training_num_agents_spawned", 6),
       (assign, ":added_troop_sequence", "$g_arena_training_num_agents_spawned"),
       (val_mod, ":added_troop_sequence", 6),
       (val_add, ":added_troop", ":added_troop_sequence"),
       (val_min, ":added_troop", 9),
       (val_add, ":added_troop", "trp_arena_training_fighter_1"),
       (assign, ":end_cond", 10000),
       (get_player_agent_no, ":player_agent"),
       (agent_get_position, pos5, ":player_agent"),
       (try_for_range, ":unused", 0, ":end_cond"),
         (store_random_in_range, ":random_entry_point", 32, 40),
         (neq, ":random_entry_point", "$g_player_entry_point"), # make sure we don't overwrite player
         (entry_point_get_position, pos1, ":random_entry_point"),
         (get_distance_between_positions, ":dist", pos5, pos1),
         (gt, ":dist", 1200), #must be at least 12 meters away from the player
         (assign, ":end_cond", 0),
       (try_end),
       (add_visitors_to_current_scene, ":random_entry_point", ":added_troop", 1),
       (store_add, ":new_spawned_count", "$g_arena_training_num_agents_spawned", 1),
       (store_mission_timer_a, ":cur_time"),
       (store_add, "$g_arena_training_next_spawn_time", ":cur_time", 14),
       (store_div, ":time_reduction", ":new_spawned_count", 3),
       (val_sub, "$g_arena_training_next_spawn_time", ":time_reduction"),
       ]),

  (0, 0, 0,
   [
       (eq, "$g_mt_mode", abm_training)
       ],
    [
       (assign, ":max_teams", 6),
       (val_max, ":max_teams", 1),
       (get_player_agent_no, ":player_agent"),
       (try_for_agents, ":agent_no"),
         (agent_is_human, ":agent_no"),
         (agent_is_alive, ":agent_no"),
         (agent_slot_eq, ":agent_no", slot_agent_arena_team_set, 0),
         (agent_get_team, ":team_no", ":agent_no"),
         (is_between, ":team_no", 0 ,7),
         (try_begin),
           (eq, ":agent_no", ":player_agent"),
           (agent_set_team, ":agent_no", 6), #player is always team 6.
         (else_try),
           (store_random_in_range, ":selected_team", 0, ":max_teams"),
          # find strongest team
           (try_for_range, ":t", 0, 6),
             (troop_set_slot, "trp_temp_array_a", ":t", 0),
           (try_end),
           (try_for_agents, ":other_agent_no"),
             (agent_is_human, ":other_agent_no"),
             (agent_is_alive, ":other_agent_no"),
             (neq, ":agent_no", ":player_agent"),
             (agent_slot_eq, ":other_agent_no", slot_agent_arena_team_set, 1),
             (agent_get_team, ":other_agent_team", ":other_agent_no"),
             (troop_get_slot, ":count", "trp_temp_array_a", ":other_agent_team"),
             (val_add, ":count", 1),
             (troop_set_slot, "trp_temp_array_a", ":other_agent_team", ":count"),
           (try_end),
           (assign, ":strongest_team", 0),
           (troop_get_slot, ":strongest_team_count", "trp_temp_array_a", 0),
           (try_for_range, ":t", 1, 6),
             (troop_slot_ge, "trp_temp_array_a", ":t", ":strongest_team_count"),
             (troop_get_slot, ":strongest_team_count", "trp_temp_array_a", ":t"),
             (assign, ":strongest_team", ":t"),
           (try_end),
           (store_random_in_range, ":rand", 5, 100),
           (try_begin),
             (lt, ":rand", "$g_arena_training_num_agents_spawned"),
             (assign, ":selected_team", ":strongest_team"),
           (try_end),
           (agent_set_team, ":agent_no", ":selected_team"),
         (try_end),
         (agent_set_slot, ":agent_no", slot_agent_arena_team_set, 1),
         (try_begin),
           (neq, ":agent_no", ":player_agent"),
           (val_add, "$g_arena_training_num_agents_spawned", 1),
         (try_end),
       (try_end),
       ]),
  ]

mission_templates = [
  (
    "town_default",0,-1,
    "Default town visit",
    [(0,mtef_scene_source|mtef_team_0,af_override_horse,0,1,pilgrim_disguise),
     (1,mtef_scene_source|mtef_team_0,af_override_horse,0,1,[]),
     (2,mtef_scene_source|mtef_team_0,af_override_horse,0,1,[]),
     (3,mtef_scene_source|mtef_team_0,af_override_horse,0,1,[]),
     (4,mtef_scene_source|mtef_team_0,af_override_horse,0,1,[]),
     (5,mtef_scene_source|mtef_team_0,af_override_horse,0,1,[]),
     (6,mtef_scene_source|mtef_team_0,af_override_horse,0,1,[]),
     (7,mtef_scene_source|mtef_team_0,af_override_horse,0,1,[]),
     (8,mtef_scene_source,af_override_horse,0,1,[]),
     (9,mtef_scene_source,af_override_horse,0,1,[]),
     (10,mtef_scene_source,af_override_horse,0,1,[]),
     (11,mtef_scene_source,af_override_horse,0,1,[]),
     (12,mtef_scene_source,af_override_horse,0,1,[]),
     (13,mtef_scene_source,0,0,1,[]),
     (14,mtef_scene_source,0,0,1,[]),
     (15,mtef_scene_source,0,0,1,[]),
     (16,mtef_visitor_source,af_override_horse,0,1,[]),
     (17,mtef_visitor_source,af_override_horse,0,1,[]),
     (18,mtef_visitor_source,af_override_horse,0,1,[]),
     (19,mtef_visitor_source,af_override_horse,0,1,[]),
     (20,mtef_visitor_source,af_override_horse,0,1,[]),
     (21,mtef_visitor_source,af_override_horse,0,1,[]),
     (22,mtef_visitor_source,af_override_horse,0,1,[]),
     (23,mtef_visitor_source,af_override_horse,0,1,[]),
     (24,mtef_visitor_source,af_override_horse,0,1,[]),
     (25,mtef_visitor_source,af_override_horse,0,1,[]),
     (26,mtef_visitor_source,af_override_horse,0,1,[]),
     (27,mtef_visitor_source,af_override_horse,0,1,[]),
     (28,mtef_visitor_source,af_override_horse,0,1,[]),
     (29,mtef_visitor_source,af_override_horse,0,1,[]),
     (30,mtef_visitor_source,af_override_horse,0,1,[]),
     (31,mtef_visitor_source,af_override_horse,0,1,[]),
     ],     
     [
      (1, 0, ti_once, [], 
      [
        (store_current_scene, ":cur_scene"),
        (scene_set_slot, ":cur_scene", slot_scene_visited, 1),
        (try_begin),
          (eq, "$sneaked_into_town", 1),
          (call_script, "script_music_set_situation_with_culture", mtf_sit_town_infiltrate),
        (else_try),
          (eq, "$talk_context", tc_tavern_talk),
          (call_script, "script_music_set_situation_with_culture", mtf_sit_tavern),
        (else_try),
          (call_script, "script_music_set_situation_with_culture", mtf_sit_town),
        (try_end),
      ]),
	  		  	        
      (ti_before_mission_start, 0, 0, [], 
      [
        (call_script, "script_change_banners_and_chest"),
        (call_script, "script_initialize_tavern_variables"),
	  ]),

      (ti_inventory_key_pressed, 0, 0, 
      [
        (set_trigger_result,1)
      ], []),
      
      #tavern - belligerent drunk leaving/fading out
      (1, 0, 0, 
      [
        (gt, "$g_belligerent_drunk_leaving", 0),
        (entry_point_get_position, pos0, 0),
        (agent_get_position, pos1, "$g_belligerent_drunk_leaving"),
        (get_distance_between_positions, ":dist", pos0, pos1),
        (le, ":dist", 150),
      ],
      [
        (agent_fade_out, "$g_belligerent_drunk_leaving"),
        (assign, "$g_belligerent_drunk_leaving", 0),
      ]),
      
      (ti_tab_pressed, 0, 0, 
      [
        (try_begin),
          (eq, "$g_main_attacker_agent", 0),
          (set_trigger_result, 1),
        (try_end),  
      ], []),

	  #tavern brawl triggers - drunk
      (2, 0, 0, 
      [
	    (neg|conversation_screen_is_active),

		(eq, "$talk_context", tc_tavern_talk),
		
		(neg|troop_slot_eq, "trp_hired_assassin", slot_troop_cur_center, "$g_encountered_party"),		
		(troop_slot_eq, "trp_belligerent_drunk", slot_troop_cur_center, "$g_encountered_party"),		
		(eq, "$drunks_dont_pick_fights", 0),		
	  ], 
	  [	  
	    (try_begin),
	      (eq, "$g_start_belligerent_drunk_fight", 0),
	      (assign, "$g_start_belligerent_drunk_fight", 1),
	      
	      (try_for_agents, ":cur_agent"),
	        (agent_get_troop_id, ":cur_agent_troop", ":cur_agent"),
	        (eq, ":cur_agent_troop", "trp_belligerent_drunk"),
	        (assign, "$g_belligerent_drunk", ":cur_agent"),
	      (try_end),
	    (else_try),
	      (eq, "$g_start_belligerent_drunk_fight", 1),	 
	           
	      (agent_is_active, "$g_belligerent_drunk"),
	      (agent_is_alive, "$g_belligerent_drunk"),
	      (get_player_agent_no, ":player_agent"),
	      (agent_get_position, pos0, ":player_agent"),
	      (agent_get_position, pos1, "$g_belligerent_drunk"),
	      (get_distance_between_positions, ":dist", pos0, pos1),
	      (position_get_z, ":pos0_z", pos0),
	      (position_get_z, ":pos1_z", pos1),
	      (store_sub, ":z_difference", ":pos1_z", ":pos0_z"),
	      (try_begin),
	        (le, ":z_difference", 0),
	        (val_mul, ":z_difference", -1),
	      (try_end),
	      (store_mul, ":z_difference_mul_3", ":z_difference", 3),
	      (val_add, ":dist", ":z_difference_mul_3"),
	      (store_random_in_range, ":random_value", 0, 200),
	      (store_add, ":400_plus_random_200", 400, ":random_value"),
	      (le, ":dist", ":400_plus_random_200"),
	      
 		  (call_script, "script_activate_tavern_attackers"),
  		  (start_mission_conversation, "trp_belligerent_drunk"),
  		  (assign, "$g_start_belligerent_drunk_fight", 2),
	    (try_end),  
	  ]),
	  	  
	  #tavern brawl triggers - assassin
      (2, 0, 0, [
	    (neg|conversation_screen_is_active),
		(eq, "$talk_context", tc_tavern_talk),
		(troop_slot_eq, "trp_hired_assassin", slot_troop_cur_center, "$g_encountered_party"),		
	  ], 
	  [
	    (try_begin),
	      (eq, "$g_start_hired_assassin_fight", 0),
	      (assign, "$g_start_hired_assassin_fight", 1),
	      
	      (try_for_agents, ":cur_agent"),
	        (agent_get_troop_id, ":cur_agent_troop", ":cur_agent"),
	        (eq, ":cur_agent_troop", "trp_hired_assassin"),
	        (assign, "$g_hired_assassin", ":cur_agent"),
	      (try_end),	      
	    (else_try),  
	      (eq, "$g_start_hired_assassin_fight", 1),

	      (agent_is_active, "$g_hired_assassin"),
	      (agent_is_alive, "$g_hired_assassin"),
	      (get_player_agent_no, ":player_agent"),
	      (agent_get_position, pos0, ":player_agent"),
	      (agent_get_position, pos1, "$g_hired_assassin"),
	      (get_distance_between_positions, ":dist", pos0, pos1),
	      (position_get_z, ":pos0_z", pos0),
	      (position_get_z, ":pos1_z", pos1),
	      (store_sub, ":z_difference", ":pos1_z", ":pos0_z"),
	      (try_begin),
	        (le, ":z_difference", 0),
	        (val_mul, ":z_difference", -1),
	      (try_end),
	      (store_mul, ":z_difference_mul_3", ":z_difference", 3),
	      (val_add, ":dist", ":z_difference_mul_3"),
	      (store_random_in_range, ":random_value", 0, 200),
	      (store_add, ":400_plus_random_200", 400, ":random_value"),
	      (le, ":dist", ":400_plus_random_200"),

		  (call_script, "script_activate_tavern_attackers"),
		  (assign, "$g_start_hired_assassin_fight", 2),
		(try_end),  
	  ]),
	  	  
	  #Aftermath talks
      (3, 0, ti_once, 
      [
	    (neg|conversation_screen_is_active),
		(eq, "$talk_context", tc_tavern_talk),
		(gt, "$g_main_attacker_agent", 0),
				
		(this_or_next|neg|agent_is_alive, "$g_main_attacker_agent"),
		(agent_is_wounded, "$g_main_attacker_agent"),
      ],
      [
        (mission_enable_talk),
      
		(try_for_agents, ":agent"),
		  (agent_is_alive, ":agent"),
		  (agent_get_position, pos4, ":agent"),
		  (agent_set_scripted_destination, ":agent", pos4),
		(try_end),
		
		(party_get_slot, ":tavernkeeper", "$g_encountered_party", slot_town_tavernkeeper),
		(start_mission_conversation, ":tavernkeeper"),	 
	  ]),

	  
	  #Aftermath talks
      (3, 0, ti_once, 
      [
	    (neg|conversation_screen_is_active),
		(eq, "$talk_context", tc_tavern_talk),
		(gt, "$g_main_attacker_agent", 0),
		(main_hero_fallen),		
      ],
      [
	  (jump_to_menu, "mnu_lost_tavern_duel"),
	  (finish_mission,0)
	  
	  ]),	  
	  
	  
	  #No shooting in the tavern
      (1, 0, 0, 
      [
	    (neg|conversation_screen_is_active),
		(eq, "$talk_context", tc_tavern_talk),
		(gt, "$g_main_attacker_agent", 0),
		
		(get_player_agent_no, ":player_agent"),
		(agent_is_alive, ":player_agent"),
		
		(agent_get_wielded_item, ":wielded_item", ":player_agent", 0),
		(is_between, ":wielded_item", "itm_darts", "itm_torch"),
		(neq, ":wielded_item", "itm_javelin_melee"),
		(neq, ":wielded_item", "itm_throwing_spear_melee"),
		(neq, ":wielded_item", "itm_jarid_melee"),
		(neq, ":wielded_item", "itm_light_throwing_axes_melee"),
		(neq, ":wielded_item", "itm_throwing_axes_melee"),
		(neq, ":wielded_item", "itm_heavy_throwing_axes_melee"),
      ], 
      [
		(party_get_slot, ":tavernkeeper", "$g_encountered_party", slot_town_tavernkeeper),
		(start_mission_conversation, ":tavernkeeper"),	 
	  ]),
	  	  	  
	  #Check for weapon in hand of attacker, also, everyone gets out of the way
      (1, 0, 0, 
      [
		(gt, "$g_main_attacker_agent", 0),	
      ],
      [
        (agent_get_wielded_item, ":wielded_item", "$g_main_attacker_agent", 0),
        (val_max, "$g_attacker_drawn_weapon", ":wielded_item"),               
        
        (call_script, "script_neutral_behavior_in_fight"),
      ]),	  			
    ],
  ),

# This template is used in party encounters and such.
# 
  (
    "conversation_encounter",0,-1,
    "Conversation_encounter",
    [( 0,mtef_visitor_source,af_override_fullhelm,0,1,[]),( 1,mtef_visitor_source,af_override_fullhelm,0,1,[]),
     ( 2,mtef_visitor_source,af_override_fullhelm,0,1,[]),( 3,mtef_visitor_source,af_override_fullhelm,0,1,[]),( 4,mtef_visitor_source,af_override_fullhelm,0,1,[]),( 5,mtef_visitor_source,af_override_fullhelm,0,1,[]),( 6,mtef_visitor_source,af_override_fullhelm,0,1,[]),
     ( 7,mtef_visitor_source,af_override_fullhelm,0,1,[]),( 8,mtef_visitor_source,af_override_fullhelm,0,1,[]),( 9,mtef_visitor_source,af_override_fullhelm,0,1,[]),(10,mtef_visitor_source,af_override_fullhelm,0,1,[]),(11,mtef_visitor_source,af_override_fullhelm,0,1,[]),
    #prisoners now...
     (12,mtef_visitor_source,af_override_fullhelm,0,1,[]),(13,mtef_visitor_source,af_override_fullhelm,0,1,[]),(14,mtef_visitor_source,af_override_fullhelm,0,1,[]),(15,mtef_visitor_source,af_override_fullhelm,0,1,[]),(16,mtef_visitor_source,af_override_fullhelm,0,1,[]),
    #Other party
     (17,mtef_visitor_source,af_override_fullhelm,0,1,[]),(18,mtef_visitor_source,af_override_fullhelm,0,1,[]),(19,mtef_visitor_source,af_override_fullhelm,0,1,[]),(20,mtef_visitor_source,af_override_fullhelm,0,1,[]),(21,mtef_visitor_source,af_override_fullhelm,0,1,[]),
     (22,mtef_visitor_source,af_override_fullhelm,0,1,[]),(23,mtef_visitor_source,af_override_fullhelm,0,1,[]),(24,mtef_visitor_source,af_override_fullhelm,0,1,[]),(25,mtef_visitor_source,af_override_fullhelm,0,1,[]),(26,mtef_visitor_source,af_override_fullhelm,0,1,[]),
     (27,mtef_visitor_source,af_override_fullhelm,0,1,[]),(28,mtef_visitor_source,af_override_fullhelm,0,1,[]),(29,mtef_visitor_source,af_override_fullhelm,0,1,[]),(30,mtef_visitor_source,af_override_fullhelm,0,1,[]),(31,mtef_visitor_source,af_override_fullhelm,0,1,[]),
     ],
    [],
  ),
  
#----------------------------------------------------------------
#mission templates before this point are hardwired into the game.
#-----------------------------------------------------------------

  (
    "town_center",0,-1,
    "Default town visit",
    [(0,mtef_scene_source|mtef_team_0,af_override_horse,0,1,pilgrim_disguise),
     (1,mtef_scene_source|mtef_team_0,0,0,1,[]),
     (2,mtef_scene_source|mtef_team_0,af_override_horse,0,1,pilgrim_disguise),
     (3,mtef_scene_source|mtef_team_0,af_override_horse,0,1,pilgrim_disguise),
     (4,mtef_scene_source|mtef_team_0,af_override_horse,0,1,pilgrim_disguise),
     (5,mtef_scene_source|mtef_team_0,af_override_horse,0,1,pilgrim_disguise),
     (6,mtef_scene_source|mtef_team_0,af_override_horse,0,1,pilgrim_disguise),
     (7,mtef_scene_source|mtef_team_0,af_override_horse,0,1,pilgrim_disguise),     
     (8,mtef_visitor_source,af_override_horse,0,1,[]),
     (9,mtef_visitor_source,af_override_horse,0,1,[]),(10,mtef_visitor_source,af_override_horse,0,1,[]),(11,mtef_visitor_source,af_override_horse,0,1,[]),(12,mtef_visitor_source,af_override_horse,0,1,[]),(13,mtef_visitor_source,0,0,1,[]),(14,mtef_scene_source,0,0,1,[]),(15,mtef_scene_source,0,0,1,[]),
     (16,mtef_visitor_source,af_override_horse,0,1,[]),(17,mtef_visitor_source,af_override_horse,0,1,[]),(18,mtef_visitor_source,af_override_horse,0,1,[]),(19,mtef_visitor_source,af_override_horse,0,1,[]),(20,mtef_visitor_source,af_override_horse,0,1,[]),(21,mtef_visitor_source,af_override_horse,0,1,[]),(22,mtef_visitor_source,af_override_horse,0,1,[]),
	 (23,mtef_visitor_source,af_override_horse,0,1,[]), #guard
     (24,mtef_visitor_source,af_override_horse,0,1,[]), #guard
	 (25,mtef_visitor_source,af_override_horse,0,1,[]), #guard
	 (26,mtef_visitor_source,af_override_horse,0,1,[]), #guard
	 (27,mtef_visitor_source,af_override_horse,0,1,[]), #guard
	 (28,mtef_visitor_source,af_override_horse,0,1,[]), #guard
	 (29,mtef_visitor_source,af_override_horse,0,1,[]),
	 (30,mtef_visitor_source,af_override_horse,0,1,[]),
	 (31,mtef_visitor_source,af_override_horse,0,1,[]),
     (32,mtef_visitor_source,af_override_horse,0,1,[]),
	 (33,mtef_visitor_source,af_override_horse,0,1,[]),
	 (34,mtef_visitor_source,af_override_horse,0,1,[]),
	 (35,mtef_visitor_source,af_override_horse,0,1,[]),
	 (36,mtef_visitor_source,af_override_horse,0,1,[]), #town walker point
	 (37,mtef_visitor_source,af_override_horse,0,1,[]), #town walker point
	 (38,mtef_visitor_source,af_override_horse,0,1,[]),
	 (39,mtef_visitor_source,af_override_horse,0,1,[]),
     (40,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]), #in towns, can be used for guard reinforcements
	 (41,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]), #in towns, can be used for guard reinforcements
	 (42,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]), #in towns, can be used for guard reinforcements
	 (43,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]), #in towns, can be used for guard reinforcements
     (44,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
	 (45,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
	 (46,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
	 (47,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
     ],
    [
      (ti_on_agent_spawn, 0, 0, [],
      [
        (store_trigger_param_1, ":agent_no"),
        (call_script, "script_init_town_agent", ":agent_no"),
        (try_begin),
          (this_or_next|eq, "$talk_context", tc_escape),
          (eq, "$talk_context", tc_prison_break),
          (agent_get_troop_id, ":troop_no", ":agent_no"),		  
          (troop_slot_eq, ":troop_no", slot_troop_will_join_prison_break, 1),
          (agent_set_team, ":agent_no", 0),
          (agent_ai_set_aggressiveness, ":agent_no", 5),
          (troop_set_slot, ":troop_no", slot_troop_will_join_prison_break, 0),
          (try_begin),
            (troop_slot_eq, ":troop_no", slot_troop_mission_participation, mp_prison_break_stand_back),
            (agent_get_position, pos1, ":agent_no"),            
            (agent_set_scripted_destination, ":agent_no", pos1),
          (try_end),
        (try_end),         
      ]),

      (ti_before_mission_start, 0, 0, [],
      [
        (assign, "$g_main_attacker_agent", 0),
	  ]),
		 
      (1, 0, ti_once, 
      [],
      [
        (try_begin),
          (eq, "$g_mt_mode", tcm_default),
          (store_current_scene, ":cur_scene"),
          (scene_set_slot, ":cur_scene", slot_scene_visited, 1),
        (try_end),
        (call_script, "script_init_town_walker_agents"),
        (try_begin),
          (eq, "$sneaked_into_town", 1),
          (call_script, "script_music_set_situation_with_culture", mtf_sit_town_infiltrate),
        (else_try),
          (call_script, "script_music_set_situation_with_culture", mtf_sit_town),
        (try_end),
      ]),

      (ti_before_mission_start, 0, 0, 
      [], 
      [
        (call_script, "script_change_banners_and_chest")
      ]),
        
      (ti_inventory_key_pressed, 0, 0,
      [
        (try_begin),
          (eq, "$g_mt_mode", tcm_default),
          (set_trigger_result,1),
        (else_try),
          (eq, "$g_mt_mode", tcm_disguised),
          (display_message,"str_cant_use_inventory_disguised"),
        (else_try),
          (display_message, "str_cant_use_inventory_now"),
        (try_end),
      ], 
      []),
       
      (ti_tab_pressed, 0, 0,
      [
        (try_begin),
          (this_or_next|eq, "$talk_context", tc_escape),
          (eq, "$talk_context", tc_prison_break),
          (display_message, "str_cannot_leave_now"),
        (else_try),
          (this_or_next|eq, "$g_mt_mode", tcm_default),
          (eq, "$g_mt_mode", tcm_disguised),
          (mission_enable_talk),
          (set_trigger_result,1),
        (else_try),
          (display_message, "str_cannot_leave_now"),
        (try_end),
      ], 
      []),

      (ti_on_leave_area, 0, 0,
      [
        (try_begin),
          (eq, "$g_defending_against_siege", 0),
          (assign,"$g_leave_town",1),
        (try_end),			
      ], 
      [
        (try_begin),
          (eq, "$talk_context", tc_escape),
          (call_script, "script_deduct_casualties_from_garrison"),
          (jump_to_menu,"mnu_sneak_into_town_caught_dispersed_guards"),
        (try_end),
        
        (mission_enable_talk),
      ]),            

     (0, 0, ti_once, 
     [], 
     [
       (party_slot_eq, "$current_town", slot_party_type, spt_town),
       (call_script, "script_town_init_doors", 0),
       (try_begin),
         (eq, "$town_nighttime", 0),
         (play_sound, "snd_town_ambiance", sf_looping),
       (try_end),
     ]),

	(3, 0, 0, 
	[
	  (call_script, "script_tick_town_walkers")
	], 
	[]),
	
    (2, 0, 0, 
    [
      (call_script, "script_center_ambiance_sounds")
    ], 
    []),
		
	#JAILBREAK TRIGGERS 
	#Civilians get out of the way
    (1, 0, 0,
	[
	  (this_or_next|eq, "$talk_context", tc_prison_break),
      (eq, "$talk_context", tc_escape),		
	],
	[
	  #(agent_get_team, ":prisoner_agent", 0),
	  (call_script, "script_neutral_behavior_in_fight"),
	  (mission_disable_talk),	  	  
	]),

	#The game begins with the town alerted
    (1, 0, ti_once, 
      [
        #If I set this to 1, 0, ti_once, then the prisoner spawns twice
        (eq, "$talk_context", tc_escape),
	  ],	  
	  [
		(get_player_agent_no, ":player_agent"),
	    (assign, reg6, ":player_agent"),
		(call_script, "script_activate_town_guard"),		
		
		(get_player_agent_no, ":player_agent"),
		(agent_get_position, pos4, ":player_agent"),
		
		(try_for_range, ":prisoner", active_npcs_begin, kingdom_ladies_end),		
		  (troop_slot_ge, ":prisoner", slot_troop_mission_participation, mp_prison_break_fight),

		  (str_store_troop_name, s4, ":prisoner"),
		  (display_message, "str_s4_joins_prison_break"),
			
		  (store_current_scene, ":cur_scene"), #this might be a better option?
		  (modify_visitors_at_site, ":cur_scene"),
			            
          #<entry_no>,<troop_id>,<number_of_troops>, <team_no>, <group_no>), 
          #team no and group no are used in multiplayer mode only. default team in entry is used in single player mode            
          (store_current_scene, ":cur_scene"),
          (modify_visitors_at_site, ":cur_scene"),                      
          (add_visitors_to_current_scene, 24, ":prisoner", 1, 0, 0),
          (troop_set_slot, ":prisoner", slot_troop_will_join_prison_break, 1),					          
        (try_end),
	  ]),
	
   (3, 0, 0, 
   [     
     (main_hero_fallen, 0),
   ],	  
   [
     (try_begin),
       (this_or_next|eq, "$talk_context", tc_prison_break),
       (eq, "$talk_context", tc_escape),
       
       (call_script, "script_deduct_casualties_from_garrison"),
	   (jump_to_menu,"mnu_captivity_start_castle_defeat"), 
	 
	   (assign, ":end_cond", kingdom_ladies_end),
       (try_for_range, ":prisoner", active_npcs_begin, ":end_cond"),
  	     (troop_set_slot, ":prisoner", slot_troop_mission_participation, 0), #new	  
  	   (try_end),  
	 
	   (mission_enable_talk),
	   (finish_mission, 0),
	 (else_try),  
	   (set_trigger_result,1),
	 (try_end),	 	 
   ]),
		
   (3, 0, 0, 
   [
     (eq, "$talk_context", tc_escape),
	 (neg|main_hero_fallen,0),
     (store_mission_timer_a, ":time"),
     (ge, ":time", 10),
		
     (all_enemies_defeated), #1 is default enemy team for in-town battles
   ],	  
   [
     (call_script, "script_deduct_casualties_from_garrison"),
	 (try_for_agents, ":agent"),
	 (agent_get_troop_id, ":troop", ":agent"),
       (troop_slot_ge, ":troop", slot_troop_mission_participation, mp_prison_break_fight),
       (try_begin),
         (agent_is_alive, ":agent"),
         (troop_set_slot, ":troop", slot_troop_mission_participation, mp_prison_break_escaped),
       (else_try),	
         (troop_set_slot, ":troop", slot_troop_mission_participation, mp_prison_break_caught),
       (try_end),
     (try_end),
     (jump_to_menu,"mnu_sneak_into_town_caught_ran_away"),
     
     (mission_enable_talk),
     (finish_mission,0)
   ]),
   
   (ti_on_agent_killed_or_wounded, 0, 0, [],
   [
     (store_trigger_param_1, ":dead_agent_no"),
     (store_trigger_param_2, ":killer_agent_no"),
     #(store_trigger_param_3, ":is_wounded"),
        
     (agent_get_troop_id, ":dead_agent_troop_no", ":dead_agent_no"),
     (agent_get_troop_id, ":killer_agent_troop_no", ":killer_agent_no"),
                
     (try_begin), 
       (this_or_next|eq, ":dead_agent_troop_no", "trp_swadian_prison_guard"),
       (this_or_next|eq, ":dead_agent_troop_no", "trp_vaegir_prison_guard"),
       (this_or_next|eq, ":dead_agent_troop_no", "trp_khergit_prison_guard"),
       (this_or_next|eq, ":dead_agent_troop_no", "trp_nord_prison_guard"),
       (this_or_next|eq, ":dead_agent_troop_no", "trp_rhodok_prison_guard"),
       (eq, ":dead_agent_troop_no", "trp_sarranid_prison_guard"),
          
       (eq, ":killer_agent_troop_no", "trp_player"),
          
       (display_message, "@You got keys of dungeon."),
     (try_end),
   ]),     
  ]),

  (
    "village_center",0,-1,
    "village center",
    [(0,mtef_scene_source|mtef_team_0,0,0,1,[]),
     (1,mtef_scene_source|mtef_team_0,0,0,1,[]),
     (2,mtef_scene_source|mtef_team_0,af_override_horse,0,1,[]),
     (3,mtef_scene_source|mtef_team_0,af_override_horse,0,1,[]),
     (4,mtef_scene_source|mtef_team_0,af_override_horse,0,1,[]),
     (5,mtef_scene_source|mtef_team_0,af_override_horse,0,1,[]),
     (6,mtef_scene_source|mtef_team_0,af_override_horse,0,1,[]),
     (7,mtef_scene_source|mtef_team_0,af_override_horse,0,1,[]),
     
     (8,mtef_visitor_source,af_override_horse,0,1,[]),
     (9,mtef_visitor_source,af_override_horse,0,1,[]),(10,mtef_visitor_source,af_override_horse,0,1,[]),(11,mtef_visitor_source,af_override_horse,0,1,[]),(12,mtef_visitor_source,af_override_horse,0,1,[]),(13,mtef_visitor_source,0,0,1,[]),(14,mtef_visitor_source,0,0,1,[]),(15,mtef_visitor_source,0,0,1,[]),
     (16,mtef_visitor_source,af_override_horse,0,1,[]),(17,mtef_visitor_source,af_override_horse,0,1,[]),(18,mtef_visitor_source,af_override_horse,0,1,[]),(19,mtef_visitor_source,af_override_horse,0,1,[]),(20,mtef_visitor_source,af_override_horse,0,1,[]),(21,mtef_visitor_source,af_override_horse,0,1,[]),(22,mtef_visitor_source,af_override_horse,0,1,[]),(23,mtef_visitor_source,af_override_horse,0,1,[]),
     (24,mtef_visitor_source,af_override_horse,0,1,[]),(25,mtef_visitor_source,af_override_horse,0,1,[]),(26,mtef_visitor_source,af_override_horse,0,1,[]),(27,mtef_visitor_source,af_override_horse,0,1,[]),(28,mtef_visitor_source,af_override_horse,0,1,[]),(29,mtef_visitor_source,af_override_horse,0,1,[]),(30,mtef_visitor_source,af_override_horse,0,1,[]),(31,mtef_visitor_source,af_override_horse,0,1,[]),
     (32,mtef_visitor_source,af_override_horse,0,1,[]),(33,mtef_visitor_source,af_override_horse,0,1,[]),(34,mtef_visitor_source,af_override_horse,0,1,[]),(35,mtef_visitor_source,af_override_horse,0,1,[]),(36,mtef_visitor_source,af_override_horse,0,1,[]),(37,mtef_visitor_source,af_override_horse,0,1,[]),(38,mtef_visitor_source,af_override_horse,0,1,[]),(39,mtef_visitor_source,af_override_horse,0,1,[]),
     (40,mtef_visitor_source,af_override_horse,0,1,[]),(41,mtef_visitor_source,af_override_horse,0,1,[]),(42,mtef_visitor_source,af_override_horse,0,1,[]),(43,mtef_visitor_source,af_override_horse,0,1,[]),(44,mtef_visitor_source,af_override_horse,0,1,[]),(45,mtef_visitor_source,af_override_horse,0,1,[]),(46,mtef_visitor_source,af_override_horse,0,1,[]),(47,mtef_visitor_source,af_override_horse,0,1,[]),
     ],
    [
      (1, 0, ti_once, [], [
          (store_current_scene, ":cur_scene"),
          (scene_set_slot, ":cur_scene", slot_scene_visited, 1),
          (call_script, "script_init_town_walker_agents"),
          (call_script, "script_music_set_situation_with_culture", mtf_sit_travel),
        ]),
      (ti_before_mission_start, 0, 0, [], [(call_script, "script_change_banners_and_chest")]),
      (ti_inventory_key_pressed, 0, 0, [(set_trigger_result,1)], []),
      (ti_tab_pressed, 0, 0, [(try_begin),
                                (check_quest_active, "qst_hunt_down_fugitive"),
                                (neg|check_quest_succeeded, "qst_hunt_down_fugitive"),
                                (neg|check_quest_failed, "qst_hunt_down_fugitive"),
                                (quest_slot_eq, "qst_hunt_down_fugitive", slot_quest_current_state, 1),
                                (try_begin),
                                  (call_script, "script_cf_troop_agent_is_alive", "trp_fugitive"),
                                  (call_script, "script_fail_quest", "qst_hunt_down_fugitive"),
                                (else_try),
                                  (call_script, "script_succeed_quest", "qst_hunt_down_fugitive"),
                                (try_end),
                              (try_end),
                              (set_trigger_result,1)], []),
      (ti_on_leave_area, 0, 0, [
          (try_begin),
            (assign,"$g_leave_town",1),
          (try_end),
          ], []),
      (3, 0, 0, [(call_script, "script_tick_town_walkers")], []),
      (2, 0, 0, [(call_script, "script_center_ambiance_sounds")], []),

      (1, 0, ti_once, [(check_quest_active, "qst_hunt_down_fugitive"),
                       (neg|check_quest_succeeded, "qst_hunt_down_fugitive"),
                       (neg|check_quest_failed, "qst_hunt_down_fugitive"),
                       (quest_slot_eq, "qst_hunt_down_fugitive", slot_quest_current_state, 1),
                       (assign, ":not_alive", 0),
                       (try_begin),
                         (call_script, "script_cf_troop_agent_is_alive", "trp_fugitive"),
                       (else_try),
                         (assign, ":not_alive", 1),
                       (try_end),
                       (this_or_next|main_hero_fallen),
                       (eq, ":not_alive", 1),
                       ],
       [(try_begin),
          (main_hero_fallen),
          (jump_to_menu, "mnu_village_hunt_down_fugitive_defeated"),
          (call_script, "script_fail_quest", "qst_hunt_down_fugitive"),
          (finish_mission, 4),
        (else_try),
          (call_script, "script_change_player_relation_with_center", "$current_town", -2),
          (call_script, "script_succeed_quest", "qst_hunt_down_fugitive"),
        (try_end),
        ]),
    ],
  ),

  (
    "bandits_at_night",0,-1,
    "Default town visit",
    [(0,mtef_scene_source|mtef_team_0, af_override_horse, aif_start_alarmed, 1, pilgrim_disguise),
     (1,mtef_scene_source|mtef_team_0,0,0,1,[]),
     (2,mtef_scene_source|mtef_team_0,af_override_horse,0,1,[]),
     (3,mtef_scene_source|mtef_team_0,af_override_horse,0,1,[]),
     (4,mtef_visitor_source|mtef_team_0, af_override_horse, aif_start_alarmed, 1, []),
     (5,mtef_scene_source|mtef_team_0,af_override_horse,0,1,[]),
     (6,mtef_scene_source|mtef_team_0,af_override_horse,0,1,[]),
     (7,mtef_scene_source|mtef_team_0,af_override_horse,0,1,[]),
     
     (8,mtef_scene_source,af_override_horse,0,1,[]),
     (9,mtef_visitor_source,af_override_horse,0,1,[]),(10,mtef_visitor_source,af_override_horse,0,1,[]),(11,mtef_visitor_source,af_override_horse,aif_start_alarmed,1,[]),(12,mtef_visitor_source,af_override_horse,0,1,[]),(13,mtef_scene_source,0,0,1,[]),(14,mtef_scene_source,0,0,1,[]),(15,mtef_scene_source,0,0,1,[]),
     (16,mtef_visitor_source,af_override_horse,0,1,[]),(17,mtef_visitor_source,af_override_horse,0,1,[]),(18,mtef_visitor_source,af_override_horse,0,1,[]),(19,mtef_visitor_source,af_override_horse,0,1,[]),(20,mtef_visitor_source,af_override_horse,0,1,[]),(21,mtef_visitor_source,af_override_horse,0,1,[]),(22,mtef_visitor_source,af_override_horse,0,1,[]),(23,mtef_visitor_source,af_override_horse,0,1,[]),
     (24,mtef_visitor_source,af_override_horse,0,1,[]),(25,mtef_visitor_source,af_override_horse,0,1,[]),(26,mtef_visitor_source,af_override_horse,0,1,[]),(27,mtef_visitor_source,af_override_horse,aif_start_alarmed,1,[]),(28,mtef_visitor_source,af_override_horse,aif_start_alarmed,1,[]),(29,mtef_visitor_source,af_override_horse,0,1,[]),(30,mtef_visitor_source,af_override_horse,0,1,[]),(31,mtef_visitor_source,af_override_horse,0,1,[]),
     (32,mtef_visitor_source,af_override_horse,0,1,[]),(33,mtef_visitor_source,af_override_horse,0,1,[]),(34,mtef_visitor_source,af_override_horse,0,1,[]),(35,mtef_visitor_source,af_override_horse,0,1,[]),(36,mtef_visitor_source,af_override_horse,0,1,[]),(37,mtef_visitor_source,af_override_horse,0,1,[]),(38,mtef_visitor_source,af_override_horse,0,1,[]),(39,mtef_visitor_source,af_override_horse,0,1,[]),
     (40,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),(41,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),(42,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),(43,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
     (44,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),(45,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),(46,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),(47,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
     ],
    [
      (ti_on_agent_spawn, 0, 0, [],
       [
         (store_trigger_param_1, ":agent_no"),
         (agent_get_troop_id, ":troop_no", ":agent_no"),
         (neq, ":troop_no", "trp_player"),
         (agent_set_team, ":agent_no", 1),
         ]),

      (ti_before_mission_start, 0, 0, [], [(call_script, "script_change_banners_and_chest")]),

      common_inventory_not_available,
      
      (ti_tab_pressed, 0, 0,
       [
         (display_message, "str_cannot_leave_now"),
         ], []),
      (ti_on_leave_area, 0, 0,
       [
         (try_begin),
           (eq, "$g_defending_against_siege", 0),
           (assign,"$g_leave_town",1),
         (try_end),
         ], []),

      (0, 0, ti_once, [],
       [
         (call_script, "script_music_set_situation_with_culture", mtf_sit_ambushed),
         (set_party_battle_mode),
         (party_slot_eq, "$current_town", slot_party_type, spt_town),
         (call_script, "script_town_init_doors", 0),
        ]),

      (1, 4, ti_once,
       [
         (store_mission_timer_a,":cur_time"),
         (ge, ":cur_time", 5),
         (this_or_next|main_hero_fallen),
         (num_active_teams_le,1)
         ],
       [
         (try_begin),
           (main_hero_fallen),
           (jump_to_menu, "mnu_town_bandits_failed"),
         (else_try),
           (jump_to_menu, "mnu_town_bandits_succeeded"),
         (try_end),
         (finish_mission),
         ]),
      ],
    ),

  
  (
    "village_training", mtf_arena_fight, -1,
    "village_training",
    [(2,mtef_visitor_source|mtef_team_0,af_override_everything,aif_start_alarmed,1,[itm_practice_staff, itm_practice_boots]),
     (4,mtef_visitor_source|mtef_team_1,af_override_everything,aif_start_alarmed,1,[itm_practice_staff, itm_practice_boots]),
     ],
    [
      (ti_before_mission_start, 0, 0, [],
       [
         (assign, "$g_train_peasants_against_bandits_training_succeeded", 0),
         (call_script, "script_change_banners_and_chest"),
         ]),
      
      common_arena_fight_tab_press,
      
      (ti_question_answered, 0, 0, [],
       [
         (store_trigger_param_1,":answer"),
         (eq,":answer",0),
         (finish_mission),
         ]),
      
      common_inventory_not_available,

      (1, 4, ti_once,
       [
         (this_or_next|main_hero_fallen),
         (num_active_teams_le, 1)
         ],
       [
         (try_begin),
           (neg|main_hero_fallen),
           (assign, "$g_train_peasants_against_bandits_training_succeeded", 1),
         (try_end),
         (finish_mission),
         ]),
      ],
    ),
    
  (
    "visit_town_castle",0,-1,
    "You enter the halls of the lord.",
    [(0,mtef_scene_source|mtef_team_0,af_override_horse|af_override_weapons|af_override_head,0,1,[]),
     (1,mtef_scene_source|mtef_team_0,af_override_horse,0,1,[]),
     (2,mtef_scene_source|mtef_team_0,af_override_horse,0,1,[]),
     (3,mtef_scene_source|mtef_team_0,af_override_horse,0,1,[]), 
     (4,mtef_scene_source|mtef_team_0,af_override_horse,0,1,[]), #for doors
     (5,mtef_visitor_source|mtef_team_0,af_override_horse,0,1,[]),
     (6,mtef_visitor_source|mtef_team_0,af_override_horse,0,1,[]),
     (7,mtef_visitor_source|mtef_team_0,af_override_horse,0,1,[]),
     (8,mtef_visitor_source,af_override_horse,0,1,[]),
     (9,mtef_visitor_source,af_override_horse,0,1,[]),
     (10,mtef_scene_source,af_override_horse,0,1,[]),
     (11,mtef_scene_source,af_override_horse,0,1,[]),
     (12,mtef_visitor_source,af_override_horse,0,1,[]),
     (13,mtef_visitor_source,0,0,1,[]),
     (14,mtef_visitor_source,0,0,1,[]),
     (15,mtef_visitor_source,0,0,1,[]),
     (16,mtef_visitor_source,af_castle_lord,0,1,[]),
     (17,mtef_visitor_source,af_castle_lord,0,1,[]),
     (18,mtef_visitor_source,af_castle_lord,0,1,[]),
     (19,mtef_visitor_source,af_castle_lord,0,1,[]),
     (20,mtef_visitor_source,af_castle_lord,0,1,[]),
     (21,mtef_visitor_source,af_castle_lord,0,1,[]),
     (22,mtef_visitor_source,af_castle_lord,0,1,[]),
     (23,mtef_visitor_source,af_castle_lord,0,1,[]),
     (24,mtef_visitor_source,af_castle_lord,0,1,[]),
     (25,mtef_visitor_source,af_castle_lord,0,1,[]),
     (26,mtef_visitor_source,af_castle_lord,0,1,[]),
     (27,mtef_visitor_source,af_castle_lord,0,1,[]),
     (28,mtef_visitor_source,af_castle_lord,0,1,[]),
     (29,mtef_visitor_source,af_castle_lord,0,1,[]),
     (30,mtef_visitor_source,af_castle_lord,0,1,[]),
     (31,mtef_visitor_source,af_castle_lord,0,1,[])
     ],
    [
      (ti_on_agent_spawn, 0, 0, [],
      [
        (store_trigger_param_1, ":agent_no"),
        (call_script, "script_init_town_agent", ":agent_no"),
      ]),
      
      (ti_before_mission_start, 0, 0, [],
      [
        (call_script, "script_change_banners_and_chest"),
      ]),
       
      (ti_inventory_key_pressed, 0, 0, 
      [
        (set_trigger_result,1)
      ], []),
	  
	  #adjust for prison break
      (ti_tab_pressed, 0, 0,
	  [
	    (neq, "$talk_context", tc_prison_break),
	    (set_trigger_result,1)
	  ], []),
	  
      (ti_on_leave_area, 0, 0,
      [
 	    (eq, "$talk_context", tc_prison_break),
 	  ], 
	  [
	    (display_message, "str_leaving_area_during_prison_break"),
	    (set_jump_mission, "mt_sneak_caught_fight"),
	  ]),
	 	  
      (0, 0, ti_once, [], [
        #(set_fog_distance, 150, 0xFF736252)
        (try_begin),
          (eq, "$talk_context", tc_court_talk),
          (try_begin),
            (store_faction_of_party, ":center_faction", "$current_town"),
            (faction_slot_eq, ":center_faction", slot_faction_ai_state, sfai_feast),
            (faction_slot_eq, ":center_faction", slot_faction_ai_object, "$current_town"),
            (call_script, "script_music_set_situation_with_culture", mtf_sit_feast),
            #(call_script, "script_music_set_situation_with_culture", mtf_sit_lords_hall),
          (try_end),
        (else_try),
          (call_script, "script_music_set_situation_with_culture", 0), #prison
        (try_end),
        ]),
    ],
  ),

		  
  (
    "back_alley_kill_local_merchant",mtf_battle_mode,-1,
    "You enter the back alley",
    [
      (0,mtef_visitor_source|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),
      (3,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
    ],
    [
      common_inventory_not_available,
      (ti_tab_pressed, 0, 0, [(display_message,"str_cannot_leave_now")], []),
      (ti_before_mission_start, 0, 0, [], [(call_script, "script_change_banners_and_chest")]),

      (0, 0, ti_once, [],
       [
         (call_script, "script_music_set_situation_with_culture", mtf_sit_ambushed),
         ]),

      (0, 0, ti_once, [
          (store_mission_timer_a,":cur_time"),
          (ge,":cur_time",1), 
          (assign, ":merchant_hp", 0),
          (assign, ":player_hp", 0),
          (assign, ":merchant_hp", 0),
          (assign, ":merchant_agent", -1),
          (assign, ":player_agent", -1),
          (try_for_agents, ":agent_no"),
            (agent_get_troop_id, ":troop_id", ":agent_no"),
            (try_begin),
              (eq, ":troop_id", "trp_local_merchant"),
              (store_agent_hit_points, ":merchant_hp", ":agent_no"),
              (assign, ":merchant_agent", ":agent_no"),
            (else_try),
              (eq, ":troop_id", "trp_player"),
              (store_agent_hit_points, ":player_hp",":agent_no"),
              (assign, ":player_agent", ":agent_no"),
            (try_end),
          (try_end),
          (ge, ":player_agent", 0),
          (ge, ":merchant_agent", 0),
          (agent_is_alive, ":player_agent"),
          (agent_is_alive, ":merchant_agent"),
          (is_between, ":merchant_hp", 1, 30),
          (gt, ":player_hp", 50),
          (start_mission_conversation, "trp_local_merchant"),
          ], []),
      
      (1, 4, ti_once, [(assign, ":not_alive", 0),
                       (try_begin),
                         (call_script, "script_cf_troop_agent_is_alive", "trp_local_merchant"),
                       (else_try),
                         (assign, ":not_alive", 1),
                       (try_end),
                       (this_or_next|main_hero_fallen),
                       (eq, ":not_alive", 1)],
       [
           (try_begin),
             (main_hero_fallen),
             (call_script, "script_fail_quest", "qst_kill_local_merchant"),
           (else_try),
             (call_script, "script_change_player_relation_with_center", "$current_town", -4),
             (call_script, "script_succeed_quest", "qst_kill_local_merchant"),
           (try_end),
           (finish_mission),
           ]),
    ],
  ),

  (
    "back_alley_revolt",mtf_battle_mode,charge,
    "You lead your men to battle.",
    [(0,mtef_team_0|mtef_use_exact_number,af_override_horse|af_override_weapons|af_override_head,aif_start_alarmed,4,[itm_quarter_staff]),
     (3,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
     ],
    [
      common_inventory_not_available,

      common_battle_init_banner,

      (ti_tab_pressed, 0, 0, [],
       [(question_box,"str_do_you_want_to_retreat"),
        ]),
      (ti_question_answered, 0, 0, [],
       [(store_trigger_param_1,":answer"),
        (eq,":answer",0),
        (jump_to_menu, "mnu_collect_taxes_failed"),
        (finish_mission),]),

      (ti_tab_pressed, 0, 0, [(display_message,"str_cannot_leave_now")], []),
      (ti_before_mission_start, 0, 0, [], [(call_script, "script_change_banners_and_chest")]),

      (0, 0, ti_once, [],
       [
         (call_script, "script_music_set_situation_with_culture", mtf_sit_fight),
         ]),

      (1, 4, ti_once, [(this_or_next|main_hero_fallen),(num_active_teams_le,1)],
       [
           (try_begin),
             (main_hero_fallen),
             (jump_to_menu, "mnu_collect_taxes_failed"),
           (else_try),
             (jump_to_menu, "mnu_collect_taxes_rebels_killed"),
           (try_end),
           (finish_mission),
           ]),
    ],
  ),

  (
    "lead_charge",mtf_battle_mode|mtf_synch_inventory,charge,
    "You lead your men to battle.",
    [
     (1,mtef_defenders|mtef_team_0,0,aif_start_alarmed,12,[]),
     (0,mtef_defenders|mtef_team_0,0,aif_start_alarmed,0,[]),
     (4,mtef_attackers|mtef_team_1,0,aif_start_alarmed,12,[]),
     (4,mtef_attackers|mtef_team_1,0,aif_start_alarmed,0,[]),
     ],
    [
      (ti_on_agent_spawn, 0, 0, [],
       [
         (store_trigger_param_1, ":agent_no"),
         (call_script, "script_agent_reassign_team", ":agent_no"),

         (assign, ":initial_courage_score", 5000),
                  
         (agent_get_troop_id, ":troop_id", ":agent_no"),
         (store_character_level, ":troop_level", ":troop_id"),
         (val_mul, ":troop_level", 35),
         (val_add, ":initial_courage_score", ":troop_level"), #average : 20 * 35 = 700
         
         (store_random_in_range, ":randomized_addition_courage", 0, 3000), #average : 1500
         (val_add, ":initial_courage_score", ":randomized_addition_courage"), 
                   
         (agent_get_party_id, ":agent_party", ":agent_no"),         
         (party_get_morale, ":cur_morale", ":agent_party"),
         
         (store_sub, ":morale_effect_on_courage", ":cur_morale", 70),
         (val_mul, ":morale_effect_on_courage", 30), #this can effect morale with -2100..900
         (val_add, ":initial_courage_score", ":morale_effect_on_courage"), 
         
         #average = 5000 + 700 + 1500 = 7200; min : 5700, max : 8700
         #morale effect = min : -2100(party morale is 0), average : 0(party morale is 70), max : 900(party morale is 100)
         #min starting : 3600, max starting  : 9600, average starting : 7200
         (agent_set_slot, ":agent_no", slot_agent_courage_score, ":initial_courage_score"), 
         ]),

      common_battle_init_banner,
		 
      (ti_on_agent_killed_or_wounded, 0, 0, [],
       [
        (store_trigger_param_1, ":dead_agent_no"),
        (store_trigger_param_2, ":killer_agent_no"),
        (store_trigger_param_3, ":is_wounded"),

        (try_begin),
          (ge, ":dead_agent_no", 0),
          (neg|agent_is_ally, ":dead_agent_no"),
          (agent_is_human, ":dead_agent_no"),
          (agent_get_troop_id, ":dead_agent_troop_id", ":dead_agent_no"),
##          (str_store_troop_name, s6, ":dead_agent_troop_id"),
##          (assign, reg0, ":dead_agent_no"),
##          (assign, reg1, ":killer_agent_no"),
##          (assign, reg2, ":is_wounded"),
##          (agent_get_team, reg3, ":dead_agent_no"),          
          #(display_message, "@{!}dead agent no : {reg0} ; killer agent no : {reg1} ; is_wounded : {reg2} ; dead agent team : {reg3} ; {s6} is added"), 
          (party_add_members, "p_total_enemy_casualties", ":dead_agent_troop_id", 1), #addition_to_p_total_enemy_casualties
          (eq, ":is_wounded", 1),
          (party_wound_members, "p_total_enemy_casualties", ":dead_agent_troop_id", 1), 
        (try_end),

        (call_script, "script_apply_death_effect_on_courage_scores", ":dead_agent_no", ":killer_agent_no"),
       ]),

      common_battle_tab_press,

      (ti_question_answered, 0, 0, [],
       [(store_trigger_param_1,":answer"),
        (eq,":answer",0),
        (assign, "$pin_player_fallen", 0),
        (try_begin),
          (store_mission_timer_a, ":elapsed_time"),
          (gt, ":elapsed_time", 20),
          (str_store_string, s5, "str_retreat"),
          (call_script, "script_simulate_retreat", 10, 20, 1),
        (try_end),
        (call_script, "script_count_mission_casualties_from_agents"),
        (finish_mission,0),]),

      (ti_before_mission_start, 0, 0, [],
       [
         (team_set_relation, 0, 2, 1),
         (team_set_relation, 1, 3, 1),
         (call_script, "script_place_player_banner_near_inventory_bms"),

         (party_clear, "p_routed_enemies"),

         (assign, "$g_latest_order_1", 1), 
         (assign, "$g_latest_order_2", 1), 
         (assign, "$g_latest_order_3", 1), 
         (assign, "$g_latest_order_4", 1), 
         ]),

      
      (0, 0, ti_once, [], [(assign,"$g_battle_won",0),
                           (assign,"$defender_reinforcement_stage",0),
                           (assign,"$attacker_reinforcement_stage",0),
                           (call_script, "script_place_player_banner_near_inventory"),
                           (call_script, "script_combat_music_set_situation_with_culture"),
                           (assign, "$g_defender_reinforcement_limit", 2),
                           ]),

      common_music_situation_update,
      common_battle_check_friendly_kills,

      (1, 0, 5, [
                              
      #new (25.11.09) starts (sdsd = TODO : make a similar code to also helping ally encounters)
      #count all total (not dead) enemy soldiers (in battle area + not currently placed in battle area)
      (call_script, "script_party_count_members_with_full_health", "p_collective_enemy"),
      (assign, ":total_enemy_soldiers", reg0),
      
      #decrease number of agents already in battle area to find all number of reinforcement enemies
      (assign, ":enemy_soldiers_in_battle_area", 0),
      (try_for_agents,":cur_agent"),
        (agent_is_human, ":cur_agent"),
        (agent_get_party_id, ":agent_party", ":cur_agent"),
        (try_begin),
          (neq, ":agent_party", "p_main_party"),
          (neg|agent_is_ally, ":cur_agent"),
          (val_add, ":enemy_soldiers_in_battle_area", 1),
        (try_end),
      (try_end),
      (store_sub, ":total_enemy_reinforcements", ":total_enemy_soldiers", ":enemy_soldiers_in_battle_area"),

      (try_begin),
        (lt, ":total_enemy_reinforcements", 15),
        (ge, "$defender_reinforcement_stage", 2),
        (eq, "$defender_reinforcement_limit_increased", 0),
        (val_add, "$g_defender_reinforcement_limit", 1),                    
        (assign, "$defender_reinforcement_limit_increased", 1),
      (try_end),    
      #new (25.11.09) ends
      
      
      
      
      
      
      (lt,"$defender_reinforcement_stage","$g_defender_reinforcement_limit"),
                 (store_mission_timer_a,":mission_time"),
                 (ge,":mission_time",10),
                 (store_normalized_team_count,":num_defenders", 0),
                 (lt,":num_defenders",6)],
           [(add_reinforcements_to_entry,0,7),(assign, "$defender_reinforcement_limit_increased", 0),(val_add,"$defender_reinforcement_stage",1)]),
      
      (1, 0, 5, [(lt,"$attacker_reinforcement_stage",2),
                 (store_mission_timer_a,":mission_time"),
                 (ge,":mission_time",10),
                 (store_normalized_team_count,":num_attackers", 1),
                 (lt,":num_attackers",6)],
           [(add_reinforcements_to_entry,3,7),(val_add,"$attacker_reinforcement_stage",1)]),

      common_battle_check_victory_condition,
      common_battle_victory_display,

      (1, 4, ti_once, [(main_hero_fallen)],
          [
              (assign, "$pin_player_fallen", 1),
              (str_store_string, s5, "str_retreat"),
              (call_script, "script_simulate_retreat", 10, 20, 1),
              (assign, "$g_battle_result", -1),
              (set_mission_result,-1),
              (call_script, "script_count_mission_casualties_from_agents"),
              (finish_mission,0)]),

      common_battle_inventory,


      #AI Triggers
      (0, 0, ti_once, [
          (store_mission_timer_a,":mission_time"),(ge,":mission_time",2),
          ],
       [(call_script, "script_select_battle_tactic"),
        (call_script, "script_battle_tactic_init"),
        #(call_script, "script_battle_calculate_initial_powers"), #deciding run away method changed and that line is erased
        ]),
      
      (3, 0, 0, [
          (call_script, "script_apply_effect_of_other_people_on_courage_scores"),
              ], []), #calculating and applying effect of people on others courage scores

      (3, 0, 0, [
          (try_for_agents, ":agent_no"),
            (agent_is_human, ":agent_no"),
            (agent_is_alive, ":agent_no"),          
            (store_mission_timer_a,":mission_time"),
            (ge,":mission_time",3),          
            (call_script, "script_decide_run_away_or_not", ":agent_no", ":mission_time"),
          (try_end),          
              ], []), #controlling courage score and if needed deciding to run away for each agent

      (5, 0, 0, [
          (store_mission_timer_a,":mission_time"),

          (ge,":mission_time",3),
          
          (call_script, "script_battle_tactic_apply"),
          ], []), #applying battle tactic

      common_battle_order_panel,
      common_battle_order_panel_tick,

    ],
  ),

  (
    "village_attack_bandits",mtf_battle_mode|mtf_synch_inventory,charge,
    "You lead your men to battle.",
    [
     (3,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
     (1,mtef_team_0|mtef_use_exact_number,0,aif_start_alarmed, 7,[]),
     (1,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
     ],
    [
      common_battle_tab_press,
      common_battle_init_banner,

      (ti_question_answered, 0, 0, [],
       [(store_trigger_param_1,":answer"),
        (eq,":answer",0),
        (assign, "$pin_player_fallen", 0),
        (str_store_string, s5, "str_retreat"),
        (call_script, "script_simulate_retreat", 10, 20, 1),
        (assign, "$g_battle_result", -1),
        (call_script, "script_count_mission_casualties_from_agents"),
        (finish_mission,0),]),

      (0, 0, ti_once, [], [(assign, "$g_battle_won", 0),
                           (assign, "$defender_reinforcement_stage", 0),
                           (assign, "$attacker_reinforcement_stage", 0),
                           (try_begin),
                             (eq, "$g_mt_mode", vba_after_training),
                             (add_reinforcements_to_entry, 1, 6),
                           (else_try),
                             (add_reinforcements_to_entry, 1, 29),
                           (try_end),
                           (call_script, "script_combat_music_set_situation_with_culture"),
                           ]),

      common_music_situation_update,
      common_battle_check_friendly_kills,
      common_battle_check_victory_condition,
      common_battle_victory_display,

      (1, 4, ti_once, [(main_hero_fallen)],
          [
              (assign, "$pin_player_fallen", 1),
              (str_store_string, s5, "str_retreat"),
              (call_script, "script_simulate_retreat", 10, 20, 1),
              (assign, "$g_battle_result", -1),
              (set_mission_result, -1),
              (call_script, "script_count_mission_casualties_from_agents"),
              (finish_mission, 0)]),

      common_battle_inventory,      
      common_battle_order_panel,
      common_battle_order_panel_tick,
      
    ],
  ),



  (
    "village_raid",mtf_battle_mode|mtf_synch_inventory,charge,
    "You lead your men to battle.",
    [
     (3,mtef_defenders|mtef_team_0,af_override_horse,aif_start_alarmed,12,[]),
     (3,mtef_defenders|mtef_team_0,0,aif_start_alarmed,0,[]),
     (1,mtef_attackers|mtef_team_1,0,aif_start_alarmed,12,[]),
     (1,mtef_attackers|mtef_team_1,0,aif_start_alarmed,0,[]),
     ],
    [
      common_battle_tab_press,
      common_battle_init_banner,

      (ti_question_answered, 0, 0, [],
       [(store_trigger_param_1,":answer"),
        (eq,":answer",0),
        (assign, "$pin_player_fallen", 0),
        (str_store_string, s5, "str_retreat"),
        (call_script, "script_simulate_retreat", 10, 20, 1),
        (call_script, "script_count_mission_casualties_from_agents"),
        (finish_mission,0),]),

      (0, 0, ti_once, [], [(assign,"$g_battle_won",0),
                           (assign,"$defender_reinforcement_stage",0),
                           (assign,"$attacker_reinforcement_stage",0),
                           (call_script, "script_combat_music_set_situation_with_culture"),
                           ]),

      common_music_situation_update,
      common_battle_check_friendly_kills,

      (1, 0, 5, [(lt,"$defender_reinforcement_stage",2),
                 (store_mission_timer_a,":mission_time"),
                 (ge,":mission_time",10),
                 (store_normalized_team_count,":num_defenders", 0),
                 (lt,":num_defenders",6)],
           [(add_reinforcements_to_entry,0,6),(val_add,"$defender_reinforcement_stage",1)]),
      (1, 0, 5, [(lt,"$attacker_reinforcement_stage",2),
                 (store_mission_timer_a,":mission_time"),
                 (ge,":mission_time",10),
                 (store_normalized_team_count,":num_attackers", 1),
                 (lt,":num_attackers",6)],
           [(add_reinforcements_to_entry,3,6),(val_add,"$attacker_reinforcement_stage",1)]),

      (1, 60, ti_once,
       [
         (store_mission_timer_a,reg(1)),
         (ge,reg(1),10),
         (all_enemies_defeated, 5),
         (neg|main_hero_fallen, 0),
         (set_mission_result,1),
         (display_message,"str_msg_battle_won"),
         (assign,"$g_battle_won",1),
         (assign, "$g_battle_result", 1),
         (try_begin),
           (eq, "$g_village_raid_evil", 0),
           (call_script, "script_play_victorious_sound"),
         (else_try),
           (play_track, "track_victorious_evil", 1),
         (try_end),
         ],
       [
         (call_script, "script_count_mission_casualties_from_agents"),
         (finish_mission, 1),
         ]),

      common_battle_victory_display,

      (1, 4, ti_once, [(main_hero_fallen)],
          [
              (assign, "$pin_player_fallen", 1),
              (str_store_string, s5, "str_retreat"),
              (call_script, "script_simulate_retreat", 10, 20, 1),
              (assign, "$g_battle_result", -1),
              (set_mission_result,-1),
              (call_script, "script_count_mission_casualties_from_agents"),
              (finish_mission,0)]),

      common_battle_inventory,
      common_battle_order_panel,
      common_battle_order_panel_tick,

##      #AI Tiggers
##      (0, 0, ti_once, [
##          (store_mission_timer_a,reg(1)),(ge,reg(1),4),
##          (call_script, "script_select_battle_tactic"),
##          (call_script, "script_battle_tactic_init"),
##          ], []),
##      (1, 0, 0, [
##          (store_mission_timer_a,reg(1)),(ge,reg(1),4),
##          (call_script, "script_battle_tactic_apply"),
##          ], []),
    ],
  ),



##  (
##    "charge_with_allies",mtf_battle_mode,charge_with_ally,
##    "Taking a handful of fighters with you, you set off to patrol the area.",
##    [
##     (1,mtef_defenders,0,0|aif_start_alarmed,8,[]),
##     (0,mtef_defenders,0,0|aif_start_alarmed,0,[]),
##     (4,mtef_attackers,0,aif_start_alarmed,8,[]),
##     (4,mtef_attackers,0,aif_start_alarmed,0,[]),
##     ],
##    [
##      (ti_tab_pressed, 0, 0, [],
##       [
##           (try_begin),
##             (eq, "$battle_won", 1),
##             (finish_mission,0),
##           (else_try),
##             (call_script, "script_cf_check_enemies_nearby"),
##             (question_box,"str_do_you_want_to_retreat"),
##           (else_try),
##             (display_message,"str_can_not_retreat"),
##           (try_end),
##        ]),
##      (ti_question_answered, 0, 0, [],
##       [(store_trigger_param_1,":answer"),
##        (eq,":answer",0),
##        (assign, "$pin_player_fallen", 0),
##        (str_store_string, s5, "str_retreat"),
##        (call_script, "script_simulate_retreat", 10, 30),
##        (finish_mission,0),]),
##
##      (0, 0, ti_once, [], [(assign,"$battle_won",0),(assign,"$defender_reinforcement_stage",0),(assign,"$attacker_reinforcement_stage",0)]),
##      (1, 0, 5, [(lt,"$defender_reinforcement_stage",2),(store_mission_timer_a,reg(1)),(ge,reg(1),10),(store_defender_count,reg(2)),(lt,reg(2),3)],
##           [(add_reinforcements_to_entry,0,4),(val_add,"$defender_reinforcement_stage",1)]),
##      (1, 0, 5, [(lt,"$attacker_reinforcement_stage",2),(store_mission_timer_a,reg(1)),(ge,reg(1),10),(store_attacker_count,reg(2)),(lt,reg(2),3)],
##           [(add_reinforcements_to_entry,3,4),(val_add,"$attacker_reinforcement_stage",1)]),
##      (1, 60, ti_once, [(store_mission_timer_a,reg(1)),
##                        (ge,reg(1),10),(all_enemies_defeated,2),
##                        (neg|main_hero_fallen,0),
##                        (set_mission_result,1),
##                        (assign, "$g_battle_result", 1),
##                        (display_message,"str_msg_battle_won"),
##                        (assign,"$battle_won",1)],
##           [(finish_mission,1)]),
##      (10, 0, 0, [], [(eq,"$battle_won",1),(display_message,"str_msg_battle_won")]),
##
##      (1, 4, ti_once, [(main_hero_fallen)],
##          [
##              (assign, "$pin_player_fallen", 1),
##              (str_store_string, s5, "str_retreat"),
##              (call_script, "script_simulate_retreat", 20, 30),
##              (assign, "$g_battle_result", -1),
##              (set_mission_result,-1),(finish_mission,0)]),
##      (ti_inventory_key_pressed, 0, 0, [(display_message,"str_use_baggage_for_inventory")], []),
##    ],
##  ),

##  (
##    "charge_with_allies_old",mtf_battle_mode,charge_with_ally,
##    "Taking a handful of fighters with you, you set off to patrol the area.",
##    [(1,mtef_leader_only,0,0,1,[]),
##     (1,mtef_no_leader,0,0|aif_start_alarmed,2,[]),
##     (1,mtef_reverse_order|mtef_ally_party,0,0|aif_start_alarmed,3,[]),
##     (0,mtef_no_leader,0,0|aif_start_alarmed,0,[]),
##     (0,mtef_reverse_order|mtef_ally_party,0,0|aif_start_alarmed,0,[]),
##     (3,mtef_reverse_order|mtef_enemy_party,0,aif_start_alarmed,6,[]),
##     (4,mtef_reverse_order|mtef_enemy_party,0,aif_start_alarmed,0,[])],
##    [
##      (ti_tab_pressed, 0, 0, [],
##       [
##           (try_begin),
##             (eq, "$battle_won", 1),
##             (finish_mission,0),
##           (else_try),
##             (call_script, "script_cf_check_enemies_nearby"),
##             (question_box,"str_do_you_want_to_retreat"),
##           (else_try),
##             (display_message,"str_can_not_retreat"),
##           (try_end),
##        ]),
##      (ti_question_answered, 0, 0, [],
##       [(store_trigger_param_1,":answer"),(eq,":answer",0),(finish_mission,0),]),
##
##      (0, 0, ti_once, [], [(assign,"$battle_won",0),(assign,"$enemy_reinforcement_stage",0),(assign,"$friend_reinforcement_stage",0),(assign,"$ally_reinforcement_stage",0)]),
##      
##      (1, 0, 5, [(lt,"$enemy_reinforcement_stage",2),(store_mission_timer_a,reg(1)),(ge,reg(1),10),(store_enemy_count,reg(2)),(lt,reg(2),3)],
##       [(add_reinforcements_to_entry,6,3),(val_add,"$enemy_reinforcement_stage",1)]),
##      (1, 0, 5, [(lt,"$friend_reinforcement_stage",2),(store_mission_timer_a,reg(1)),(ge,reg(1),10),(store_friend_count,reg(2)),(lt,reg(2),2)],
##       [(add_reinforcements_to_entry,3,1),(val_add,"$friend_reinforcement_stage",1)]),
##      (1, 0, 5, [(lt,"$ally_reinforcement_stage",2),(store_mission_timer_a,reg(1)),(ge,reg(1),10),(store_ally_count,reg(2)),  (lt,reg(2),2)],
##       [(add_reinforcements_to_entry,4,2),(val_add,"$ally_reinforcement_stage",1)]),
##      (1, 60, ti_once, [(store_mission_timer_a,reg(1)),
##                        (ge,reg(1),10),
##                        (all_enemies_defeated,2),
##                        (neg|main_hero_fallen,0),
##                        (set_mission_result,1),
##                        (assign, "$g_battle_result", 1),
##                        (display_message,"str_msg_battle_won"),
##                        (assign,"$battle_won",1),
##                        ],
##       [(finish_mission,1)]),
##      (10, 0, 0, [], [(eq,"$battle_won",1),(display_message,"str_msg_battle_won")]),
##      (1, 4, ti_once, [(main_hero_fallen,0)],
##       [(set_mission_result,-1),(finish_mission,1)]),
##      (ti_inventory_key_pressed, 0, 0, [(display_message,"str_use_baggage_for_inventory")], []),
##    ],
##  ),
##  (
##    "lead_charge_old",mtf_battle_mode,charge,
##    "You lead your men to battle.",
##    [
##     (1,mtef_leader_only,0,0,1,[]),
##     (1,mtef_no_leader,0,0|aif_start_alarmed,5,[]),
##     (0,mtef_no_leader,0,0|aif_start_alarmed,0,[]),
##     (3,mtef_enemy_party|mtef_reverse_order,0,aif_start_alarmed,6,[]),
##     (4,mtef_enemy_party|mtef_reverse_order,0,aif_start_alarmed,0,[]),
##     ],
##    [
##      (ti_tab_pressed, 0, 0, [],
##       [
##           (try_begin),
##             (eq, "$battle_won", 1),
##             (finish_mission,0),
##           (else_try),
##             (call_script, "script_cf_check_enemies_nearby"),
##             (question_box,"str_do_you_want_to_retreat"),
##           (else_try),
##             (display_message,"str_can_not_retreat"),
##           (try_end),
##        ]),
##      (ti_question_answered, 0, 0, [],
##       [(store_trigger_param_1,":answer"),(eq,":answer",0),(finish_mission,0),]),
##
##      (0, 0, ti_once, [], [(assign,"$battle_won",0),(assign,"$enemy_reinforcement_stage",0),(assign,"$friend_reinforcement_stage",0)]),
##      (1, 0, 5, [(lt,"$enemy_reinforcement_stage",2),(store_mission_timer_a,reg(1)),(ge,reg(1),10),(store_enemy_count,reg(2)),(lt,reg(2),3)],
##           [(add_reinforcements_to_entry,4,3),(val_add,"$enemy_reinforcement_stage",1)]),
##      (1, 0, 5, [(lt,"$friend_reinforcement_stage",2),(store_mission_timer_a,reg(1)),(ge,reg(1),10),(store_friend_count,reg(2)),(lt,reg(2),3)],
##           [(add_reinforcements_to_entry,2,3),(val_add,"$friend_reinforcement_stage",1)]),
##      (1, 60, ti_once, [(store_mission_timer_a,reg(1)),
##                        (ge,reg(1),10),(all_enemies_defeated,2),
##                        (neg|main_hero_fallen,0),
##                        (set_mission_result,1),
##                        (assign, "$g_battle_result", 1),
##                        (display_message,"str_msg_battle_won"),
##                        (assign,"$battle_won",1)],
##           [(finish_mission,1)]),
##      (10, 0, 0, [], [(eq,"$battle_won",1),(display_message,"str_msg_battle_won")]),
##      (1, 4, ti_once, [(main_hero_fallen)],
##          [
##              (assign, "$g_battle_result", -1),
##              (set_mission_result,-1),(finish_mission,1)]),
##      (ti_inventory_key_pressed, 0, 0, [(display_message,"str_use_baggage_for_inventory")], []),
##    ],
##  ),



  (
    "besiege_inner_battle_castle",mtf_battle_mode,-1,
    "You attack the walls of the castle...",
    [
     (0, mtef_attackers|mtef_use_exact_number|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
     (6, mtef_attackers|mtef_use_exact_number|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
     (7, mtef_attackers|mtef_use_exact_number|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
     (16, mtef_defenders|mtef_use_exact_number|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),
     (17, mtef_defenders|mtef_use_exact_number|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),
     (18, mtef_defenders|mtef_use_exact_number|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),
     (19, mtef_defenders|mtef_use_exact_number|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),
     (20, mtef_defenders|mtef_use_exact_number|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),
     ],
    [
      (ti_before_mission_start, 0, 0, [], [(call_script, "script_change_banners_and_chest")]),

      common_battle_tab_press,
      common_battle_init_banner,

      (ti_question_answered, 0, 0, [],
       [(store_trigger_param_1,":answer"),
        (eq,":answer",0),
        (assign, "$pin_player_fallen", 0),
        (str_store_string, s5, "str_retreat"),
        (call_script, "script_simulate_retreat", 5, 20, 0),
        (assign, "$g_battle_result", -1),
        (set_mission_result,-1),
        (call_script, "script_count_mission_casualties_from_agents"),
        (finish_mission,0),
        ]),
        
      (0, 0, ti_once, [], [(assign,"$g_battle_won",0),
                           (call_script, "script_music_set_situation_with_culture", mtf_sit_ambushed),
                           ]),
      
      #AI Tiggers
      (0, 0, ti_once, [
          (assign, "$defender_team", 0),
          (assign, "$attacker_team", 1),
          (assign, "$defender_team_2", 2),
          (assign, "$attacker_team_2", 3),
          ], []),

      common_battle_check_friendly_kills,
      common_battle_check_victory_condition,
      common_battle_victory_display,

      (1, 4, ti_once, [(main_hero_fallen)],
          [
              (assign, "$pin_player_fallen", 1),
              (str_store_string, s5, "str_retreat"),
              (call_script, "script_simulate_retreat", 5, 20, 0),
              (assign, "$g_battle_result", -1),
              (set_mission_result,-1),
              (call_script, "script_count_mission_casualties_from_agents"),
              (finish_mission,0)
              ]),
      
      common_battle_order_panel,
      common_battle_order_panel_tick,
      common_battle_inventory,
    ],
  ),

  (
    "besiege_inner_battle_town_center",mtf_battle_mode,-1,
    "You attack the walls of the castle...",
    [
     (0, mtef_attackers|mtef_use_exact_number|mtef_team_1,af_override_horse,aif_start_alarmed,4,[]),
     (2, mtef_defenders|mtef_use_exact_number|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),
     (23, mtef_defenders|mtef_use_exact_number|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),
     (24, mtef_defenders|mtef_use_exact_number|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),
     (25, mtef_defenders|mtef_use_exact_number|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),
     (26, mtef_defenders|mtef_use_exact_number|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),
     (27, mtef_defenders|mtef_use_exact_number|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),
     (28, mtef_defenders|mtef_use_exact_number|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),
     ],
    [
      (ti_before_mission_start, 0, 0, [], [(call_script, "script_change_banners_and_chest")]),

      common_battle_tab_press,
      common_battle_init_banner,

      (ti_question_answered, 0, 0, [],
       [(store_trigger_param_1,":answer"),
        (eq,":answer",0),
        (assign, "$pin_player_fallen", 0),
        (str_store_string, s5, "str_retreat"),
        (call_script, "script_simulate_retreat", 5, 20, 0),
        (assign, "$g_battle_result", -1),
        (set_mission_result,-1),
        (call_script, "script_count_mission_casualties_from_agents"),
        (finish_mission,0),
        ]),
        
      (0, 0, ti_once, [], [(assign,"$g_battle_won",0),
                           (call_script, "script_music_set_situation_with_culture", mtf_sit_ambushed),
                           ]),
      
      #AI Tiggers
      (0, 0, ti_once, [
          (assign, "$defender_team", 0),
          (assign, "$attacker_team", 1),
          (assign, "$defender_team_2", 2),
          (assign, "$attacker_team_2", 3),
          ], []),

      common_battle_check_friendly_kills,
      common_battle_check_victory_condition,
      common_battle_victory_display,

      (1, 4, ti_once, [(main_hero_fallen)],
          [
              (assign, "$pin_player_fallen", 1),
              (str_store_string, s5, "str_retreat"),
              (call_script, "script_simulate_retreat", 5, 20, 0),
              (assign, "$g_battle_result", -1),
              (set_mission_result,-1),
              (call_script, "script_count_mission_casualties_from_agents"),
              (finish_mission,0)
              ]),

      common_battle_order_panel,
      common_battle_order_panel_tick,
      common_battle_inventory,
    ],
  ),

  (
    "castle_attack_walls_defenders_sally",mtf_battle_mode|mtf_synch_inventory,-1,
    "You attack the walls of the castle...",
    [
     (0,mtef_attackers|mtef_team_1,af_override_horse,aif_start_alarmed,12,[]),
     (0,mtef_attackers|mtef_team_1,af_override_horse,aif_start_alarmed,0,[]),
     (3,mtef_defenders|mtef_team_0,af_override_horse,aif_start_alarmed,12,[]),
     (3,mtef_defenders|mtef_team_0,af_override_horse,aif_start_alarmed,0,[]),
     ],
    [
      (ti_on_agent_spawn, 0, 0, [],
       [
         (store_trigger_param_1, ":agent_no"),
         (call_script, "script_agent_reassign_team", ":agent_no"),
         ]),
      
      (ti_before_mission_start, 0, 0, [],
       [
         (team_set_relation, 0, 2, 1),
         (team_set_relation, 1, 3, 1),
         (call_script, "script_change_banners_and_chest"),
         (call_script, "script_remove_siege_objects"),
         ]),

      common_battle_tab_press,
      common_battle_init_banner,

      (ti_on_agent_killed_or_wounded, 0, 0, [], #new
       [
        (store_trigger_param_1, ":dead_agent_no"),
        (store_trigger_param_2, ":killer_agent_no"),
        (store_trigger_param_3, ":is_wounded"),

        (try_begin),
          (ge, ":dead_agent_no", 0),
          (neg|agent_is_ally, ":dead_agent_no"),
          (agent_is_human, ":dead_agent_no"),
          (agent_get_troop_id, ":dead_agent_troop_id", ":dead_agent_no"),
          (str_store_troop_name, s6, ":dead_agent_troop_id"),
          (assign, reg0, ":dead_agent_no"),
          (assign, reg1, ":killer_agent_no"),
          (assign, reg2, ":is_wounded"),
          (agent_get_team, reg3, ":dead_agent_no"),          
          #(display_message, "@{!}dead agent no : {reg0} ; killer agent no : {reg1} ; is_wounded : {reg2} ; dead agent team : {reg3} ; {s6} is added"), 
          (party_add_members, "p_total_enemy_casualties", ":dead_agent_troop_id", 1), #addition_to_p_total_enemy_casualties
          (eq, ":is_wounded", 1),
          (party_wound_members, "p_total_enemy_casualties", ":dead_agent_troop_id", 1), 
        (try_end),
       ]),

      (ti_question_answered, 0, 0, [],
       [(store_trigger_param_1,":answer"),
        (eq,":answer",0),
        (assign, "$pin_player_fallen", 0),
        (str_store_string, s5, "str_retreat"),
        (call_script, "script_simulate_retreat", 5, 20, 0),
        (call_script, "script_count_mission_casualties_from_agents"),
        (finish_mission,0),]),
        
      (0, 0, ti_once, [], [(assign,"$g_battle_won",0),
                           (call_script, "script_combat_music_set_situation_with_culture"),
                           ]),
      
      common_music_situation_update,
      common_battle_check_friendly_kills,

      (1, 60, ti_once, [(store_mission_timer_a, reg(1)),
                        (ge, reg(1), 10),
                        (all_enemies_defeated, 2),
                        (neg|main_hero_fallen,0),
                        (set_mission_result,1),
                        (display_message,"str_msg_battle_won"),
                        (assign, "$g_battle_won", 1),
                        (assign, "$g_battle_result", 1),
                        (assign, "$g_siege_sallied_out_once", 1),
                        (assign, "$g_siege_method", 1), #reset siege timer
                        (call_script, "script_play_victorious_sound"),
                        ],
           [(call_script, "script_count_mission_casualties_from_agents"),
            (finish_mission,1)]),

      common_battle_victory_display,

      (1, 4, ti_once, [(main_hero_fallen)],
          [
              (assign, "$pin_player_fallen", 1),
              (str_store_string, s5, "str_retreat"),
              (call_script, "script_simulate_retreat", 5, 20, 0),
              (assign, "$g_battle_result", -1),
              (set_mission_result, -1),
              (call_script, "script_count_mission_casualties_from_agents"),
              (finish_mission,0)]),

      common_battle_order_panel,
      common_battle_order_panel_tick,
      common_battle_inventory,
    ],
  ),


  (
    "castle_attack_walls_belfry",mtf_battle_mode|mtf_synch_inventory,-1,
    "You attack the walls of the castle...",
    [
     (0,mtef_attackers|mtef_team_1,af_override_horse,aif_start_alarmed,12,[]),
     (0,mtef_attackers|mtef_team_1,af_override_horse,aif_start_alarmed,0,[]),
     (10,mtef_defenders|mtef_team_0,af_override_horse,aif_start_alarmed,0,[]),
     (11,mtef_defenders|mtef_team_0,af_override_horse,aif_start_alarmed,7,[]),
     (15,mtef_defenders|mtef_team_0,af_override_horse,aif_start_alarmed,0,[]),

     (40,mtef_defenders|mtef_team_0|mtef_archers_first,af_override_horse,aif_start_alarmed,1,[]),
     (41,mtef_defenders|mtef_team_0|mtef_archers_first,af_override_horse,aif_start_alarmed,1,[]),
     (42,mtef_defenders|mtef_team_0|mtef_archers_first,af_override_horse,aif_start_alarmed,1,[]),
     (43,mtef_defenders|mtef_team_0|mtef_archers_first,af_override_horse,aif_start_alarmed,1,[]),
     (44,mtef_defenders|mtef_team_0|mtef_archers_first,af_override_horse,aif_start_alarmed,1,[]),
     (45,mtef_defenders|mtef_team_0|mtef_archers_first,af_override_horse,aif_start_alarmed,1,[]),
     (46,mtef_defenders|mtef_team_0|mtef_archers_first,af_override_horse,aif_start_alarmed,1,[]),
     (47,mtef_defenders|mtef_team_0|mtef_archers_first,af_override_horse,aif_start_alarmed,1,[]),
     ],
    [
      common_battle_mission_start,
      common_battle_tab_press,
      common_battle_init_banner,
      common_siege_question_answered,
      common_siege_init,
      common_music_situation_update,
      common_siege_ai_trigger_init,
      common_siege_ai_trigger_init_2,

      (0, 0, ti_once,
       [
         (set_show_messages, 0),
         (team_give_order, "$attacker_team", grc_everyone, mordr_spread_out),
         (team_give_order, "$attacker_team", grc_everyone, mordr_spread_out),
         (team_give_order, "$attacker_team", grc_everyone, mordr_spread_out),
         (set_show_messages, 1),
         ], []),
      
      (ti_on_agent_killed_or_wounded, 0, 0, [],
       [
        (store_trigger_param_1, ":dead_agent_no"),
        (store_trigger_param_2, ":killer_agent_no"),
        (store_trigger_param_3, ":is_wounded"),

        (try_begin),
          (ge, ":dead_agent_no", 0),
          (neg|agent_is_ally, ":dead_agent_no"),
          (agent_is_human, ":dead_agent_no"),
          (agent_get_troop_id, ":dead_agent_troop_id", ":dead_agent_no"),
          (str_store_troop_name, s6, ":dead_agent_troop_id"),
          (assign, reg0, ":dead_agent_no"),
          (assign, reg1, ":killer_agent_no"),
          (assign, reg2, ":is_wounded"),
          (agent_get_team, reg3, ":dead_agent_no"),          
          #(display_message, "@{!}dead agent no : {reg0} ; killer agent no : {reg1} ; is_wounded : {reg2} ; dead agent team : {reg3} ; {s6} is added"), 
          (party_add_members, "p_total_enemy_casualties", ":dead_agent_troop_id", 1), #addition_to_p_total_enemy_casualties
          (eq, ":is_wounded", 1),
          (party_wound_members, "p_total_enemy_casualties", ":dead_agent_troop_id", 1), 
        (try_end),
       ]),

      common_siege_ai_trigger_init_after_2_secs,
      common_siege_defender_reinforcement_check,
      common_siege_defender_reinforcement_archer_reposition,
      common_siege_attacker_reinforcement_check,
      common_siege_attacker_do_not_stall,
      common_battle_check_friendly_kills,
      common_battle_check_victory_condition,
      common_battle_victory_display,
      common_siege_refill_ammo,
      common_siege_check_defeat_condition,
      common_battle_order_panel,
      common_battle_order_panel_tick,
      common_inventory_not_available,
      common_siege_init_ai_and_belfry,
      common_siege_move_belfry,
      common_siege_rotate_belfry,
      common_siege_assign_men_to_belfry,
    ],
  ),

  (
    "castle_attack_walls_ladder",mtf_battle_mode|mtf_synch_inventory,-1,
    "You attack the walls of the castle...",
    [
     (0,mtef_attackers|mtef_team_1,af_override_horse,aif_start_alarmed,12,[]),
     (0,mtef_attackers|mtef_team_1,af_override_horse,aif_start_alarmed,0,[]),
     (10,mtef_defenders|mtef_team_0,af_override_horse,aif_start_alarmed,0,[]),
     (11,mtef_defenders|mtef_team_0,af_override_horse,aif_start_alarmed,7,[]),
     (15,mtef_defenders|mtef_team_0,af_override_horse,aif_start_alarmed,0,[]),

     (40,mtef_defenders|mtef_team_0|mtef_archers_first,af_override_horse,aif_start_alarmed,1,[]),
     (41,mtef_defenders|mtef_team_0|mtef_archers_first,af_override_horse,aif_start_alarmed,1,[]),
     (42,mtef_defenders|mtef_team_0|mtef_archers_first,af_override_horse,aif_start_alarmed,1,[]),
     (43,mtef_defenders|mtef_team_0|mtef_archers_first,af_override_horse,aif_start_alarmed,1,[]),
     (44,mtef_defenders|mtef_team_0|mtef_archers_first,af_override_horse,aif_start_alarmed,1,[]),
     (45,mtef_defenders|mtef_team_0|mtef_archers_first,af_override_horse,aif_start_alarmed,1,[]),
     (46,mtef_defenders|mtef_team_0|mtef_archers_first,af_override_horse,aif_start_alarmed,1,[]),
     ],
    [
      common_battle_mission_start,
      common_battle_tab_press,
      common_battle_init_banner,
      common_siege_question_answered,
      common_siege_init,
      common_music_situation_update,
      common_siege_ai_trigger_init,
      common_siege_ai_trigger_init_2,
      common_siege_ai_trigger_init_after_2_secs,
      common_siege_defender_reinforcement_check,
      common_siege_defender_reinforcement_archer_reposition,
      common_siege_attacker_reinforcement_check,
      common_siege_attacker_do_not_stall,
      common_battle_check_friendly_kills,
      common_battle_check_victory_condition,
      common_battle_victory_display,
      common_siege_refill_ammo,
      common_siege_check_defeat_condition,
      common_battle_order_panel,
      common_battle_order_panel_tick,
      common_inventory_not_available,

      (ti_on_agent_killed_or_wounded, 0, 0, [],
       [
        (store_trigger_param_1, ":dead_agent_no"),
        (store_trigger_param_2, ":killer_agent_no"),
        (store_trigger_param_3, ":is_wounded"),

        (try_begin),
          (ge, ":dead_agent_no", 0),
          (neg|agent_is_ally, ":dead_agent_no"),
          (agent_is_human, ":dead_agent_no"),
          (agent_get_troop_id, ":dead_agent_troop_id", ":dead_agent_no"),
          (str_store_troop_name, s6, ":dead_agent_troop_id"),
          (assign, reg0, ":dead_agent_no"),
          (assign, reg1, ":killer_agent_no"),
          (assign, reg2, ":is_wounded"),
          (agent_get_team, reg3, ":dead_agent_no"),          
          #(display_message, "@{!}dead agent no : {reg0} ; killer agent no : {reg1} ; is_wounded : {reg2} ; dead agent team : {reg3} ; {s6} is added"), 
          (party_add_members, "p_total_enemy_casualties", ":dead_agent_troop_id", 1), #addition_to_p_total_enemy_casualties
          (eq, ":is_wounded", 1),
          (party_wound_members, "p_total_enemy_casualties", ":dead_agent_troop_id", 1), 
        (try_end),
       ]),

##      (15, 0, 0,
##       [
##         (get_player_agent_no, ":player_agent"),
##         (agent_get_team, ":agent_team", ":player_agent"),
##         (neq, "$attacker_team", ":agent_team"),
##         (assign, ":non_ranged", 0),
##         (assign, ":ranged", 0),
##         (assign, ":ranged_pos_x", 0),
##         (assign, ":ranged_pos_y", 0),
##         (set_fixed_point_multiplier, 100),
##         (try_for_agents, ":agent_no"),
##           (eq, ":non_ranged", 0),
##           (agent_is_human, ":agent_no"),
##           (agent_is_alive, ":agent_no"),
##           (neg|agent_is_defender, ":agent_no"),
##           (agent_get_class, ":agent_class", ":agent_no"),
##           (try_begin),
##             (neq, ":agent_class", grc_archers),
##             (val_add, ":non_ranged", 1),
##           (else_try),
##             (val_add, ":ranged", 1),
##             (agent_get_position, pos0, ":agent_no"),
##             (position_get_x, ":pos_x", pos0),
##             (position_get_y, ":pos_y", pos0),
##             (val_add, ":ranged_pos_x", ":pos_x"),
##             (val_add, ":ranged_pos_y", ":pos_y"),
##           (try_end),
##         (try_end),
##         (try_begin),
##           (eq, ":non_ranged", 0),
##           (gt, ":ranged", 0),
##           (val_div, ":ranged_pos_x", ":ranged"),
##           (val_div, ":ranged_pos_y", ":ranged"),
##           (entry_point_get_position, pos0, 10),
##           (init_position, pos1),
##           (position_set_x, pos1, ":ranged_pos_x"),
##           (position_set_y, pos1, ":ranged_pos_y"),
##           (position_get_z, ":pos_z", pos0),
##           (position_set_z, pos1, ":pos_z"),
##           (get_distance_between_positions, ":dist", pos0, pos1),
##           (gt, ":dist", 1000), #average position of archers is more than 10 meters far from entry point 10
##           (team_give_order, "$attacker_team", grc_archers, mordr_hold),
##           (team_set_order_position, "$attacker_team", grc_archers, pos0),
##         (else_try),
##           (team_give_order, "$attacker_team", grc_everyone, mordr_charge),
##         (try_end),
##         ],
##       []),
    ],
  ),
  

  (
    "castle_visit",0,-1,
    "Castle visit",
    [(0,mtef_scene_source|mtef_team_0,af_override_horse|af_override_weapons|af_override_head,0,1,pilgrim_disguise),
     (1,mtef_scene_source|mtef_team_0,af_override_horse,0,1,pilgrim_disguise),
     (2,mtef_scene_source|mtef_team_0,af_override_horse,0,1,pilgrim_disguise),
     (3,mtef_scene_source|mtef_team_0,af_override_horse,0,1,pilgrim_disguise), 
     (4,mtef_scene_source|mtef_team_0,af_override_horse,0,1,pilgrim_disguise), #for doors
     (5,mtef_visitor_source|mtef_team_0,af_override_horse,0,1,pilgrim_disguise),
     (6,mtef_visitor_source|mtef_team_0,af_override_horse,0,1,pilgrim_disguise),
     (7,mtef_visitor_source|mtef_team_0,af_override_horse,0,1,pilgrim_disguise),
     (8,mtef_visitor_source|mtef_team_0,af_override_horse,0,1,[]),(9,mtef_visitor_source|mtef_team_0,af_override_horse,0,1,[]),(10,mtef_visitor_source|mtef_team_0,af_override_horse,0,1,[]),(11,mtef_visitor_source|mtef_team_0,af_override_horse,0,1,[]),
     (12,mtef_visitor_source|mtef_team_0,af_override_horse,0,1,[]),(13,mtef_visitor_source|mtef_team_0,af_override_horse,0,1,[]),(14,mtef_visitor_source|mtef_team_0,af_override_horse,0,1,[]),(15,mtef_visitor_source|mtef_team_0,af_override_horse,0,1,[]),
     (16,mtef_visitor_source|mtef_team_0,af_override_horse,0,1,[]),(17,mtef_visitor_source|mtef_team_0,af_override_horse,0,1,[]),(18,mtef_visitor_source|mtef_team_0,af_override_horse,0,1,[]),(19,mtef_visitor_source|mtef_team_0,af_override_horse,0,1,[]),
     (20,mtef_visitor_source|mtef_team_0,af_override_horse,0,1,[]),(21,mtef_visitor_source|mtef_team_0,af_override_horse,0,1,[]),(22,mtef_visitor_source|mtef_team_0,af_override_horse,0,1,[]),(23,mtef_visitor_source|mtef_team_0,af_override_horse,0,1,[]),
     (24,mtef_visitor_source|mtef_team_0,af_override_horse,0,1,[]),(25,mtef_visitor_source|mtef_team_0,af_override_horse,0,1,[]),(26,mtef_visitor_source|mtef_team_0,af_override_horse,0,1,[]),(27,mtef_visitor_source|mtef_team_0,af_override_horse,0,1,[]),
     (28,mtef_visitor_source|mtef_team_0,af_override_horse,0,1,[]),(29,mtef_visitor_source|mtef_team_0,af_override_horse,0,1,[]),(30,mtef_visitor_source|mtef_team_0,af_override_horse,0,1,[]),(31,mtef_visitor_source|mtef_team_0,af_override_horse,0,1,[]),
     (32,mtef_visitor_source|mtef_team_0,af_override_horse,0,1,[]),(33,mtef_visitor_source|mtef_team_0,af_override_horse,0,1,[]),(34,mtef_visitor_source|mtef_team_0,af_override_horse,0,1,[]),(35,mtef_visitor_source|mtef_team_0,af_override_horse,0,1,[]),
     (36,mtef_visitor_source|mtef_team_0,af_override_horse,0,1,[]),(37,mtef_visitor_source|mtef_team_0,af_override_horse,0,1,[]),(38,mtef_visitor_source|mtef_team_0,af_override_horse,0,1,[]),(39,mtef_visitor_source|mtef_team_0,af_override_horse,0,1,[]),
     # Party members
     (40,mtef_visitor_source|mtef_team_0,af_override_horse,0,1,[]),
     (41,mtef_visitor_source|mtef_team_0,af_override_horse,0,1,[]),
     (42,mtef_visitor_source|mtef_team_0,af_override_horse,0,1,[]),
     (43,mtef_visitor_source|mtef_team_0,af_override_horse,0,1,[]),
     (44,mtef_visitor_source|mtef_team_0,af_override_horse,0,1,[]),
     (45,mtef_visitor_source|mtef_team_0,af_override_horse,0,1,[]),
     (46,mtef_visitor_source|mtef_team_0,af_override_horse,0,1,[]),
     ],
    [    
      (ti_on_agent_spawn, 0, 0, [],
      [
        (store_trigger_param_1, ":agent_no"),
        (call_script, "script_init_town_agent", ":agent_no"),
        (get_player_agent_no, ":player_agent"),
        (try_begin),
          (neq, ":player_agent", ":agent_no"),
          (agent_set_team, ":agent_no", 7),
        (try_end),
        
        (try_begin),
          (this_or_next|eq, "$talk_context", tc_escape),
          (eq, "$talk_context", tc_prison_break),
          (agent_get_troop_id, ":troop_no", ":agent_no"),
          (troop_get_slot, ":will_join_prison_break", ":troop_no", slot_troop_will_join_prison_break),
          (eq, ":will_join_prison_break", 1),
          (agent_set_team, ":agent_no", 0),
          (agent_ai_set_aggressiveness, ":agent_no", 5),
          (troop_set_slot, ":troop_no", slot_troop_will_join_prison_break, 0),

          (try_begin),
            (troop_slot_eq, ":troop_no", slot_troop_mission_participation, mp_prison_break_stand_back),
            (agent_get_position, pos1, ":agent_no"),                        
            (agent_set_scripted_destination, ":agent_no", pos1),
          (try_end),
        (try_end),
      ]),
      
      (ti_on_agent_killed_or_wounded, 0, 0, [],
      [
        (store_trigger_param_1, ":dead_agent_no"),
        (store_trigger_param_2, ":killer_agent_no"),
        #(store_trigger_param_3, ":is_wounded"),
        
        (agent_get_troop_id, ":dead_agent_troop_no", ":dead_agent_no"),
        (agent_get_troop_id, ":killer_agent_troop_no", ":killer_agent_no"),
                
        (try_begin), 
          (this_or_next|eq, ":dead_agent_troop_no", "trp_swadian_prison_guard"),
          (this_or_next|eq, ":dead_agent_troop_no", "trp_vaegir_prison_guard"),
          (this_or_next|eq, ":dead_agent_troop_no", "trp_khergit_prison_guard"),
          (this_or_next|eq, ":dead_agent_troop_no", "trp_nord_prison_guard"),
          (this_or_next|eq, ":dead_agent_troop_no", "trp_rhodok_prison_guard"),
          (eq, ":dead_agent_troop_no", "trp_sarranid_prison_guard"),
          
          (eq, ":killer_agent_troop_no", "trp_player"),
          
          (display_message, "@You got keys of dungeon."),
        (try_end),
      ]),     

      #JAILBREAK TRIGGERS 
      #Civilians get out of the way
      (1, 0, 0,
      [
        (this_or_next|eq, "$talk_context", tc_prison_break),
        (eq, "$talk_context", tc_escape),
      ],
      [
        #(agent_get_team, ":prisoner_agent", 0),
        (call_script, "script_neutral_behavior_in_fight"),
        (mission_disable_talk),
      ]),
      
      #The game begins with the town alerted
      (1, 0, ti_once,
      [
        #If I set this to 1, 0, ti_once, then the prisoner spawns twice
        (eq, "$talk_context", tc_escape),
      ],
      [
        (get_player_agent_no, ":player_agent"),
        (assign, reg6, ":player_agent"),
        (call_script, "script_activate_town_guard"),		
        
        (get_player_agent_no, ":player_agent"),
        (agent_get_position, pos4, ":player_agent"),
        
        (try_for_range, ":prisoner", active_npcs_begin, kingdom_ladies_end),
          (troop_slot_ge, ":prisoner", slot_troop_mission_participation, 1),
          
          (str_store_troop_name, s4, ":prisoner"),
          (display_message, "str_s4_joins_prison_break"),
          
          (store_current_scene, ":cur_scene"), #this might be a better option?
          (modify_visitors_at_site, ":cur_scene"),
          #<entry_no>,<troop_id>,<number_of_troops>, <team_no>, <group_no>), 
          #team no and group no are used in multiplayer mode only. default team in entry is used in single player mode
          (store_current_scene, ":cur_scene"),
          (modify_visitors_at_site, ":cur_scene"),
          (assign, ":nearest_entry_no", 24),
          (add_visitors_to_current_scene, ":nearest_entry_no", ":prisoner", 1, 0, 0),
          (troop_set_slot, ":prisoner", slot_troop_will_join_prison_break, 1),          
        (try_end),
	  ]),

      (ti_tab_pressed, 0, 0,
      [
        (try_begin),
          (this_or_next|eq, "$talk_context", tc_escape),
          (eq, "$talk_context", tc_prison_break),
          (display_message, "str_cannot_leave_now"),
        (else_try),
          (this_or_next|eq, "$g_mt_mode", tcm_default),
          (eq, "$g_mt_mode", tcm_disguised),
          (set_trigger_result, 1),
          (mission_enable_talk),
        (else_try),
          (display_message, "str_cannot_leave_now"),
        (try_end),
      ], 
      []),
            
      (ti_before_mission_start, 0, 0, [], 
      [
        (call_script, "script_change_banners_and_chest"),
        (call_script, "script_remove_siege_objects"),
      ]),
      
      (3, 0, 0, 
      [     
        (main_hero_fallen, 0),
      ],	  
      [
        (try_begin),
          (this_or_next|eq, "$talk_context", tc_prison_break),
          (eq, "$talk_context", tc_escape),
       
          (call_script, "script_deduct_casualties_from_garrison"),
	      (jump_to_menu,"mnu_captivity_start_castle_defeat"), 
	 
	      (assign, ":end_cond", kingdom_ladies_end),
          (try_for_range, ":prisoner", active_npcs_begin, ":end_cond"),
  	        (troop_set_slot, ":prisoner", slot_troop_mission_participation, 0), #new	  
  	      (try_end),  
	 
	      (mission_enable_talk),
	      (finish_mission, 0),
	    (else_try),  
	      (mission_enable_talk),
	      (finish_mission, 0),
	      (set_trigger_result, 1),
        (try_end),	 	 
      ]),
      
      (3, 0, 0, 
      [
        (eq, "$talk_context", tc_escape),
        (neg|main_hero_fallen,0),
        (store_mission_timer_a, ":time"),
        (ge, ":time", 10),      
        (all_enemies_defeated), #1 is default enemy team for in-town battles
      ],
      [
        (call_script, "script_deduct_casualties_from_garrison"),
        (try_for_agents, ":agent"),
          (agent_get_troop_id, ":troop", ":agent"),
          (troop_slot_ge, ":troop", slot_troop_mission_participation, mp_prison_break_fight),
          (try_begin),
            (agent_is_alive, ":agent"),
            (troop_set_slot, ":troop", slot_troop_mission_participation, mp_prison_break_escaped),
          (else_try),
            (troop_set_slot, ":troop", slot_troop_mission_participation, mp_prison_break_caught),
          (try_end),
        (try_end),
        (jump_to_menu, "mnu_sneak_into_town_caught_ran_away"),
        (mission_enable_talk),
        (finish_mission, 0),
      ]),
    ],
  ),


  (
    "training_ground_trainer_talk", 0, -1,
    "Training.",
    [
      (0,mtef_scene_source|mtef_team_0,af_override_horse|af_override_weapons,0,1,[]),
      (1,mtef_scene_source|mtef_team_0,af_override_horse|af_override_weapons,0,1,[]),
      (2,mtef_scene_source|mtef_team_0,af_override_horse|af_override_weapons,0,1,[]),
      (3,mtef_scene_source|mtef_team_0,af_override_horse|af_override_weapons,0,1,[]),
      (4,mtef_scene_source|mtef_team_0,af_override_horse|af_override_weapons,0,1,[]),
      (5,mtef_scene_source|mtef_team_0,af_override_horse|af_override_weapons,0,1,[]),
      (6,mtef_scene_source|mtef_team_0,0,0,1,[]),
    ],
    [
      (ti_before_mission_start, 0, 0, [],
       [
         (call_script, "script_change_banners_and_chest"),
         ]),
      (ti_inventory_key_pressed, 0, 0,
       [
         (set_trigger_result,1),
         ], []),
      (ti_tab_pressed, 0, 0,
       [
         (set_trigger_result,1),
         ], []),
     (0.0, 1.0, 2.0,
      [(lt, "$trainer_help_message", 2),
        ],
      [(try_begin),
         (eq, "$trainer_help_message", 0),
#         (tutorial_box, "str_trainer_help_1", "@Tutorial"),
       (else_try),
#         (tutorial_box, "str_trainer_help_2", "@Tutorial"),
       (try_end),
       (val_add, "$trainer_help_message", 1),
          ]),
      
    ],
  ),

  (
    "training_ground_trainer_training",mtf_arena_fight,-1,
    "You will fight a match in the arena.",
    [
      (16, mtef_visitor_source|mtef_team_0,af_override_everything,aif_start_alarmed,1,[itm_practice_shield,itm_practice_sword,itm_practice_boots]),
      (17, mtef_visitor_source|mtef_team_1,af_override_everything,aif_start_alarmed,1,[itm_practice_staff,itm_practice_boots]),
      (18, mtef_visitor_source|mtef_team_2,af_override_everything,aif_start_alarmed,1,[itm_practice_staff,itm_practice_boots]),
      (19, mtef_visitor_source|mtef_team_3,af_override_everything,aif_start_alarmed,1,[itm_heavy_practice_sword,itm_practice_boots]),
      (20, mtef_visitor_source,0,0,1,[]),
    ],
    [
      (ti_before_mission_start, 0, 0, [], [(call_script, "script_change_banners_and_chest")]),
      
      common_arena_fight_tab_press,
      
      (ti_question_answered, 0, 0, [],
       [
         (store_trigger_param_1, ":answer"),
         (eq, ":answer", 0),
         (set_jump_mission, "mt_training_ground_trainer_talk"),
         (modify_visitors_at_site, "$g_training_ground_melee_training_scene"),
         (reset_visitors),
         (set_jump_entry, 5),
         (jump_to_scene, "$g_training_ground_melee_training_scene"),
         ]),
      (1, 3, ti_once, [(main_hero_fallen,0)],
       [
         (set_jump_mission, "mt_training_ground_trainer_talk"),
         (modify_visitors_at_site, "$g_training_ground_melee_training_scene"),
         (reset_visitors),
         (set_jump_entry, 5),
         (jump_to_scene, "$g_training_ground_melee_training_scene"),
         ]),
      (1, 3, ti_once,
       [
         (store_mission_timer_a, reg1),
         (ge, reg1, 1),
         (num_active_teams_le, 1),
         (neg|main_hero_fallen),
         (assign, "$training_fight_won", 1),
         ],
       [
         (set_jump_mission, "mt_training_ground_trainer_talk"),
         (modify_visitors_at_site, "$g_training_ground_melee_training_scene"),
         (reset_visitors),
         (set_jump_entry, 5),
         (jump_to_scene, "$g_training_ground_melee_training_scene"),
         ]),
      (ti_inventory_key_pressed, 0, 0, [(display_message,"str_cant_use_inventory_arena")], []),
    ],
  ),


  (
    "training_ground_training", mtf_arena_fight, -1,
    "Training.",
    [
      (0,mtef_visitor_source|mtef_team_0,af_override_everything,aif_start_alarmed,1,[itm_practice_staff]),
      (1,mtef_visitor_source|mtef_team_1,af_override_everything,aif_start_alarmed,1,[itm_practice_staff]),
      (2,mtef_visitor_source|mtef_team_1,af_override_everything,aif_start_alarmed,1,[itm_practice_staff]),
      (3,mtef_visitor_source|mtef_team_1,af_override_everything,aif_start_alarmed,1,[itm_practice_staff]),
      (4,mtef_visitor_source|mtef_team_1,af_override_everything,aif_start_alarmed,1,[itm_practice_staff]),
      (8,mtef_visitor_source,af_override_weapons|af_override_horse|af_override_head,0,1,[]),
      (9,mtef_visitor_source,af_override_weapons|af_override_horse|af_override_head,0,1,[]),
      (10,mtef_visitor_source,af_override_weapons|af_override_horse|af_override_head,0,1,[]),
      (11,mtef_visitor_source,af_override_weapons|af_override_horse|af_override_head,0,1,[]),
      (12,mtef_visitor_source,af_override_weapons|af_override_horse|af_override_head,0,1,[]),
      (13,mtef_visitor_source,af_override_weapons|af_override_horse|af_override_head,0,1,[]),
      (14,mtef_visitor_source,af_override_weapons|af_override_horse|af_override_head,0,1,[]),
      (15,mtef_visitor_source,af_override_weapons|af_override_horse|af_override_head,0,1,[]),
    ],
    [
      (ti_before_mission_start, 0, 0, [],
       [
         (assign, "$g_last_destroyed_gourds", 0),
         (call_script, "script_change_banners_and_chest")]),
      
      common_arena_fight_tab_press,
      
      (ti_question_answered, 0, 0, [],
       [
         (store_trigger_param_1,":answer"),
         (eq,":answer",0),
         (assign, "$g_training_ground_training_success_ratio", 0),
         (jump_to_menu, "mnu_training_ground_training_result"),
         (finish_mission),
         ]),
      
      common_inventory_not_available,

      (0, 0, ti_once,
       [
         (try_begin),
           (eq, "$g_mt_mode", ctm_ranged),
           (set_fixed_point_multiplier, 100),
           (entry_point_get_position, pos1, 0),
           (init_position, pos2),
           (position_set_y, pos2, "$g_training_ground_ranged_distance"),
           (position_transform_position_to_parent, pos3, pos1, pos2),
           (copy_position, pos1, pos3),
           (assign, ":end_cond", 10),
           (assign, ":shift_value", 0),
           (try_for_range, ":cur_i", 0, ":end_cond"),
             (store_sub, ":cur_instance", ":cur_i", ":shift_value"),
             (scene_prop_get_instance, ":target_object", "spr_gourd", ":cur_instance"),
             (copy_position, pos2, pos1),
             (init_position, pos0),
             (store_random_in_range, ":random_no", 0, 360),
             (position_rotate_z, pos2, ":random_no"),
             (store_random_in_range, ":random_no", 50, 600),
             (position_move_x, pos2, ":random_no"),
             (store_random_in_range, ":random_no", 0, 360),
             (position_transform_position_to_local, pos3, pos1, pos2),
             (position_rotate_z, pos0, ":random_no"),
             (position_transform_position_to_parent, pos4, pos0, pos3),
             (position_transform_position_to_parent, pos2, pos1, pos4),
             (position_set_z_to_ground_level, pos2),
             (position_move_z, pos2, 150),
             (assign, ":valid", 1),
             (try_for_range, ":cur_instance_2", 0, 10),
               (eq, ":valid", 1),
               (neq, ":cur_instance", ":cur_instance_2"),
               (scene_prop_get_instance, ":target_object_2", "spr_gourd", ":cur_instance_2"),
               (prop_instance_get_position, pos3, ":target_object_2"),
               (get_distance_between_positions, ":dist", pos2, pos3),
               (lt, ":dist", 100),
               (assign, ":valid", 0),
             (try_end),
             (try_begin),
               (eq, ":valid", 0),
               (val_add, ":end_cond", 1),
               (val_add, ":shift_value", 1),
             (else_try),
               (prop_instance_set_position, ":target_object", pos2),
               (prop_instance_animate_to_position, ":target_object", pos2, 1),
               (scene_prop_get_instance, ":target_object_2", "spr_gourd_spike", ":cur_instance"),
               (position_move_z, pos2, -150), #moving back to ground level
               (prop_instance_set_position, ":target_object_2", pos2),
               (prop_instance_animate_to_position, ":target_object_2", pos2, 1),
             (try_end),
           (try_end),
         (else_try),
           (eq, "$g_mt_mode", ctm_mounted),
           (assign, ":num_gourds", 0),
           #First, placing gourds on the spikes
           (try_for_range, ":cur_i", 0, 100),
             (scene_prop_get_instance, ":target_object", "spr_gourd", ":cur_i"),
             (scene_prop_get_instance, ":target_object_2", "spr_gourd_spike", ":cur_i"),
             (ge, ":target_object", 0),
             (ge, ":target_object_2", 0),
             (val_add, ":num_gourds", 1),
             (prop_instance_get_position, pos0, ":target_object_2"),
             (position_move_z, pos0, 150),
             (prop_instance_set_position, ":target_object", pos0),
             (prop_instance_animate_to_position, ":target_object", pos0, 1),
           (try_end),
           (store_sub, ":end_cond", ":num_gourds", "$g_training_ground_training_num_gourds_to_destroy"),
           #Second, removing gourds and their spikes randomly
           (try_for_range, ":cur_i", 0, ":end_cond"),
             (store_random_in_range, ":random_instance", 0, ":num_gourds"),
             (scene_prop_get_instance, ":target_object", "spr_gourd", ":random_instance"),
             (prop_instance_get_position, pos0, ":target_object"),
             (position_get_z, ":pos_z", pos0),
             (try_begin),
               (lt, ":pos_z", -50000),
#               (val_add, ":end_cond", 1), #removed already, try again
             (else_try),
               (position_set_z, pos0, -100000),
               (prop_instance_set_position, ":target_object", pos0),
               (prop_instance_animate_to_position, ":target_object", pos0, 1),
               (scene_prop_get_instance, ":target_object_2", "spr_gourd_spike", ":random_instance"),
               (prop_instance_set_position, ":target_object_2", pos0),
               (prop_instance_animate_to_position, ":target_object_2", pos0, 1),
             (try_end),
           (try_end),
         (try_end),
         ],
       []),

      (1, 3, ti_once,
       [
         (eq, "$g_mt_mode", ctm_melee),
         (this_or_next|main_hero_fallen),
         (num_active_teams_le, 1)
         ],
       [
         (try_begin),
           (neg|main_hero_fallen),
           (assign, "$g_training_ground_training_success_ratio", 100),
         (else_try),
           (assign, ":alive_enemies", 0),
           (try_for_agents, ":agent_no"),
             (agent_is_alive, ":agent_no"),
             (agent_is_human, ":agent_no"),
             (agent_get_team, ":team_no", ":agent_no"),
             (eq, ":team_no", 1),
             (val_add, ":alive_enemies", 1),
           (try_end),
           (store_sub, ":dead_enemies", "$g_training_ground_training_num_enemies", ":alive_enemies"),
           (store_mul, "$g_training_ground_training_success_ratio", ":dead_enemies", 100),
           (val_div, "$g_training_ground_training_success_ratio", "$g_training_ground_training_num_enemies"),
         (try_end),
         (jump_to_menu, "mnu_training_ground_training_result"),
         (finish_mission),
         ]),

      (1, 3, ti_once,
       [
         (eq, "$g_mt_mode", ctm_ranged),
         (get_player_agent_no, ":player_agent"),
         (agent_get_ammo, ":ammo", ":player_agent"),
         (store_mission_timer_a, ":cur_seconds"),
         (this_or_next|main_hero_fallen),
         (this_or_next|eq, ":ammo", 0),
         (gt, ":cur_seconds", 116), 
         ],
       [
         (store_mul, "$g_training_ground_training_success_ratio", "$scene_num_total_gourds_destroyed", 10),
         (jump_to_menu, "mnu_training_ground_training_result"),
         (finish_mission),
         ]),

      (1, 3, ti_once,
       [
         (eq, "$g_mt_mode", ctm_mounted),
         (get_player_agent_no, ":player_agent"),
         (agent_get_horse, ":player_horse", ":player_agent"),
         (store_mission_timer_a, ":cur_seconds"),
         (this_or_next|lt, ":player_horse", 0),
         (this_or_next|main_hero_fallen),
         (this_or_next|ge, "$scene_num_total_gourds_destroyed", "$g_training_ground_training_num_gourds_to_destroy"),
         (gt, ":cur_seconds", 120),
         ],
       [
         (store_mul, "$g_training_ground_training_success_ratio", "$scene_num_total_gourds_destroyed", 100),
         (val_div, "$g_training_ground_training_success_ratio", "$g_training_ground_training_num_gourds_to_destroy"),
         (jump_to_menu, "mnu_training_ground_training_result"),
         (finish_mission),
         ]),

      (0, 0, 0,
       [
         (gt, "$g_last_destroyed_gourds", 0),
         (try_begin),
           (eq, "$g_mt_mode", ctm_ranged),
           (entry_point_get_position, pos1, 0),
           (position_move_y, pos1, 100, 0),
           (get_player_agent_no, ":player_agent"),
           (agent_get_position, pos2, ":player_agent"),
           (try_begin),
             (position_is_behind_position, pos2, pos1),
             (val_add, "$scene_num_total_gourds_destroyed", "$g_last_destroyed_gourds"),
           (else_try),
             (display_message, "@You must stay behind the line on the ground! Point is not counted."),
           (try_end),
         (else_try),
           (val_add, "$scene_num_total_gourds_destroyed", "$g_last_destroyed_gourds"),
         (try_end),
         (assign, "$g_last_destroyed_gourds", 0),
         ],
       []),
    ],
  ),

  (
    "sneak_caught_fight",mtf_battle_mode,-1,
    "You must fight your way out!",
    [
     (0,mtef_scene_source|mtef_team_0,af_override_all,aif_start_alarmed,1,pilgrim_disguise),
     (1,mtef_scene_source|mtef_team_0,af_override_all,aif_start_alarmed,1,pilgrim_disguise),
     (2,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
     (3,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
     (4,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
     (5,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
     (6,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
     (7,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
     (8,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
     (9,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
     (10,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
     (11,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
     (12,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
     (13,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
     (14,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
     (15,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
     (16,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
     (17,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
     (18,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
     (19,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
     (20,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
     (21,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
     (22,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
     (23,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
     (24,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
     (25,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
     (26,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
     (27,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
     (28,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
     (29,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
     (30,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
     (31,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
     (32,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
     (33,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
     (34,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
     (35,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
     (36,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
     (37,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
     (38,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
     (39,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
     (40,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
     (41,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
     (42,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
     (43,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
     (44,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
     (45,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
     (46,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
     (47,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
     (48,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
     (49,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
     (50,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
     (51,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
     (52,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
     (53,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
     (54,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
     (55,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
     (56,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
     (57,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
     (58,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
     (59,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
     (60,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
     (61,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
     (62,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
     (63,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
     (64,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
     
     # (0,mtef_visitor_source|mtef_team_0,af_override_all,aif_start_alarmed,1,pilgrim_disguise),
     # (25,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
     # (26,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
     # (27,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
     # (28,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
     # (29,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
     # (30,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
     # (31,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
     # (32,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
    ],
    [    
      (ti_before_mission_start, 0, 0, [], 
      [
        (call_script, "script_change_banners_and_chest"),
      ]),
      
      (ti_after_mission_start, 0, 0, [],
       [
        (assign, ":num_guards", 5),
        
        (try_begin),
          (party_get_slot, ":last_nearby_fire_time", "$current_town", slot_town_last_nearby_fire_time),                          
          (store_current_hours, ":cur_time"),
          (store_add, ":fire_finish_time", ":last_nearby_fire_time", 4),                          
          (is_between, ":cur_time", ":fire_finish_time", ":last_nearby_fire_time"),
          (assign, ":num_guards", 2),
        (else_try),  
          (this_or_next|eq, "$talk_context", tc_escape),
          (eq, "$talk_context", tc_prison_break),

          (assign, ":num_guards", 4),
        (try_end),
        
        (try_begin),
          (this_or_next|eq, "$talk_context", tc_escape),
          (eq, "$talk_context", tc_prison_break),
          (entry_point_get_position, pos0, 7), 
        (else_try),          
          (party_slot_eq, "$current_town", slot_party_type, spt_town),
          (entry_point_get_position, pos0, 0), 
        (else_try),  
          (entry_point_get_position, pos0, 1), 
        (try_end),
                        
        (assign, ":last_nearest_entry_distance", -1),
        (assign, ":last_nearest_entry_point", -1),
        (try_for_range, ":guard_no", 0, ":num_guards"),
          (assign, ":smallest_dist", 100000),
          (try_for_range, ":guard_entry_point", 2, 64),
            (neq, ":last_nearest_entry_point", ":guard_entry_point"),
            (entry_point_get_position, pos1, ":guard_entry_point"), 
            (get_distance_between_positions, ":dist", pos0, pos1),
            (lt, ":dist", ":smallest_dist"),
            (gt, ":dist", ":last_nearest_entry_distance"),
            (assign, ":smallest_dist", ":dist"),
            (assign, ":nearest_entry_point", ":guard_entry_point"),
          (try_end),  
          
          (store_faction_of_party, ":town_faction","$current_town"),
          (try_begin),
            (this_or_next|eq, ":guard_no", 0),
            (eq, ":guard_no", 2),
            (faction_get_slot, ":troop_of_guard", ":town_faction", slot_faction_tier_2_troop),
          (else_try),  
            (faction_get_slot, ":troop_of_guard", ":town_faction", slot_faction_tier_2_troop),
          (try_end),
          
          (assign, ":last_nearest_entry_point", ":nearest_entry_point"),
          (assign, ":last_nearest_entry_distance", ":smallest_dist"),
                    
          (add_visitors_to_current_scene, ":nearest_entry_point", ":troop_of_guard", 1, 0),                      
        (try_end),
      ]),
      
      (ti_tab_pressed, 0, 0, [],
       [(question_box,"str_do_you_wish_to_surrender")]),
       
      (ti_question_answered, 0, 0, [],
       [(store_trigger_param_1,":answer"),(eq,":answer",0),(jump_to_menu,"mnu_captivity_start_castle_defeat"),(finish_mission,0),]),
      
      (1, 0, ti_once, [],
       [
         (play_sound,"snd_sneak_town_halt"),
         (call_script, "script_music_set_situation_with_culture", mtf_sit_fight),
         ]),
         
      (0, 3, 0,
       [
          (main_hero_fallen,0),
        ],
       [
         (jump_to_menu,"mnu_captivity_start_castle_defeat"),
         (finish_mission,0),
       ]),
       
      (1, 0, 0, [], 
       [
	    (get_player_agent_no, ":player_agent"),
	    (agent_get_position, pos0, ":player_agent"),
	    	    
        (try_for_agents, ":agent_no"),
          (neq, ":agent_no", ":player_agent"),
          (agent_is_alive, ":agent_no"),
          (agent_get_team, ":agent_team", ":agent_no"),
          (eq, ":agent_team", 1),
          
          (agent_get_position, pos1, ":agent_no"),
        
          (get_distance_between_positions, ":dist", pos0, pos1),
         
          (try_begin),
            (le, ":dist", 800),
            (agent_clear_scripted_mode, ":agent_no"),
          (else_try),  
            (agent_set_scripted_destination, ":agent_no", pos0, 0),
          (try_end),
        (try_end),                  	      
       ]), 

	   (5, 1, ti_once, 
	   [
	     (num_active_teams_le,1),
	     (neg|main_hero_fallen),

         (store_mission_timer_a,":cur_time"),
         (ge, ":cur_time", 5),
	   ],
       [
         (assign,"$auto_menu",-1),
         (jump_to_menu,"mnu_sneak_into_town_caught_dispersed_guards"),
         (finish_mission,1),
       ]),
       
	   (ti_on_leave_area, 0, ti_once, [],
       [(assign,"$auto_menu",-1),(jump_to_menu,"mnu_sneak_into_town_caught_ran_away"),(finish_mission,0)]),

      (ti_inventory_key_pressed, 0, 0, [(display_message,"str_cant_use_inventory_arena")], []),
      
    ],
  ),

   (
    "ai_training",0,-1,
    "You start training.",
    [
#     (0,0,af_override_horse,aif_start_alarmed,1,[]),
     (0,0,0,aif_start_alarmed,30,[]),
#     (1,mtef_no_leader,0,0|aif_start_alarmed,5,[]),
#     (0,mtef_no_leader,0,0|aif_start_alarmed,0,[]),
#     (3,mtef_enemy_party|mtef_reverse_order,0,aif_start_alarmed,6,[]),
#     (4,mtef_enemy_party|mtef_reverse_order,0,aif_start_alarmed,0,[]),
     ],
    [
#      (ti_before_mission_start, 0, 0, [], [(set_rain, 1,100), (set_fog_distance, 10)]),
      (ti_tab_pressed, 0, 0, [],
       [(finish_mission,0)]),

      common_battle_order_panel,
      common_battle_order_panel_tick,

##      (0, 0, ti_once,
##       [
##         (key_clicked, key_numpad_7),
##        (mission_cam_set_mode,1),
##        (get_player_agent_no, ":player_agent"),
##        (mission_cam_set_target_agent, ":player_agent", 1),
##        (mission_cam_set_animation, "anim_test_cam"),], []),
    ],
  ),
   (
    "camera_test",0,-1,
    "camera Test.",
    [
#     (0,mtef_attackers,0,aif_start_alarmed,5,[]),
     ],
    [
      (1, 0, 0, [(mission_cam_set_mode,1),
          (entry_point_get_position, pos3, 3),
          (mission_cam_set_position, pos3)], []),
#      (ti_before_mission_start, 0, 0, [], [(set_rain, 1,100)]),
      (ti_tab_pressed, 0, 0, [],
       [(finish_mission,0)]),
    ],
  ),

  (
    "arena_melee_fight",mtf_arena_fight,-1,
    "You enter a melee fight in the arena.",
    [
      (0,mtef_visitor_source|mtef_team_0,af_override_all,aif_start_alarmed,1,[itm_practice_bow,itm_practice_arrows,itm_practice_horse,itm_arena_tunic_red, itm_red_tourney_helmet]),
      (1,mtef_visitor_source|mtef_team_0,af_override_all,aif_start_alarmed,1,[itm_heavy_practice_sword, itm_arena_tunic_red]),
      (2,mtef_visitor_source|mtef_team_0,af_override_all,aif_start_alarmed,1,[itm_heavy_practice_sword,itm_practice_horse,itm_arena_tunic_red, itm_red_tourney_helmet]),
      (3,mtef_visitor_source|mtef_team_0,af_override_all,aif_start_alarmed,1,[itm_practice_lance,itm_practice_shield,itm_practice_horse,itm_arena_tunic_red, itm_red_tourney_helmet]),
      (4,mtef_visitor_source|mtef_team_0,af_override_all,aif_start_alarmed,1,[itm_practice_bow,itm_practice_arrows, itm_practice_dagger, itm_arena_tunic_red]),
      (5,mtef_visitor_source|mtef_team_0,af_override_all,aif_start_alarmed,1,[itm_practice_sword,itm_practice_shield,itm_arena_tunic_red]),
      (6,mtef_visitor_source|mtef_team_0,af_override_all,aif_start_alarmed,1,[itm_heavy_practice_sword,itm_practice_horse,itm_arena_tunic_red]),
      (7,mtef_visitor_source|mtef_team_0,af_override_all,aif_start_alarmed,1,[itm_practice_lance,itm_practice_shield,itm_practice_horse,itm_arena_tunic_red, itm_red_tourney_helmet]),

      (8,mtef_visitor_source|mtef_team_1,af_override_all,aif_start_alarmed,1,[itm_practice_bow,itm_practice_arrows,itm_practice_dagger, itm_arena_tunic_blue]),
      (9,mtef_visitor_source|mtef_team_1,af_override_all,aif_start_alarmed,1,[itm_practice_lance,itm_practice_shield,itm_practice_horse,itm_arena_tunic_blue,itm_blue_tourney_helmet]),
      (10,mtef_visitor_source|mtef_team_1,af_override_all,aif_start_alarmed,1,[itm_heavy_practice_sword,itm_arena_tunic_blue]),
      (11,mtef_visitor_source|mtef_team_1,af_override_all,aif_start_alarmed,1,[itm_practice_sword,itm_practice_shield,itm_arena_tunic_blue, itm_blue_tourney_helmet]),
      (12,mtef_visitor_source|mtef_team_1,af_override_all,aif_start_alarmed,1,[itm_practice_bow,itm_practice_arrows,itm_practice_horse,itm_arena_tunic_blue]),
      (13,mtef_visitor_source|mtef_team_1,af_override_all,aif_start_alarmed,1,[itm_practice_lance,itm_practice_shield,itm_practice_horse,itm_arena_tunic_blue,itm_blue_tourney_helmet]),
      (14,mtef_visitor_source|mtef_team_1,af_override_all,aif_start_alarmed,1,[itm_heavy_practice_sword,itm_arena_tunic_blue]),
      (15,mtef_visitor_source|mtef_team_1,af_override_all,aif_start_alarmed,1,[itm_practice_sword,itm_practice_shield,itm_arena_tunic_blue]),

      (16,mtef_visitor_source|mtef_team_2,af_override_all,aif_start_alarmed,1,[itm_practice_bow,itm_practice_arrows,itm_practice_horse,itm_arena_tunic_green, itm_green_tourney_helmet]),
      (17,mtef_visitor_source|mtef_team_2,af_override_all,aif_start_alarmed,1,[itm_heavy_practice_sword,itm_arena_tunic_green, itm_green_tourney_helmet]),
      (18,mtef_visitor_source|mtef_team_2,af_override_all,aif_start_alarmed,1,[itm_heavy_practice_sword,itm_practice_horse,itm_arena_tunic_green, itm_green_tourney_helmet]),
      (19,mtef_visitor_source|mtef_team_2,af_override_all,aif_start_alarmed,1,[itm_practice_lance,itm_practice_shield,itm_practice_horse,itm_arena_tunic_green, itm_green_tourney_helmet]),
      (20,mtef_visitor_source|mtef_team_2,af_override_all,aif_start_alarmed,1,[itm_practice_bow,itm_practice_arrows,itm_practice_dagger, itm_arena_tunic_green, itm_green_tourney_helmet]),
      (21,mtef_visitor_source|mtef_team_2,af_override_all,aif_start_alarmed,1,[itm_practice_sword,itm_practice_shield,itm_arena_tunic_green]),
      (22,mtef_visitor_source|mtef_team_2,af_override_all,aif_start_alarmed,1,[itm_heavy_practice_sword,itm_practice_horse,itm_arena_tunic_green]),
      (23,mtef_visitor_source|mtef_team_2,af_override_all,aif_start_alarmed,1,[itm_practice_lance,itm_practice_shield,itm_practice_horse,itm_arena_tunic_green, itm_green_tourney_helmet]),

      (24,mtef_visitor_source|mtef_team_3,af_override_all,aif_start_alarmed,1,[itm_practice_bow,itm_practice_arrows,itm_practice_horse,itm_arena_tunic_yellow, itm_gold_tourney_helmet]),
      (25,mtef_visitor_source|mtef_team_3,af_override_all,aif_start_alarmed,1,[itm_heavy_practice_sword,itm_arena_tunic_yellow, itm_gold_tourney_helmet]),
      (26,mtef_visitor_source|mtef_team_3,af_override_all,aif_start_alarmed,1,[itm_heavy_practice_sword,itm_practice_horse,itm_arena_tunic_yellow, itm_gold_tourney_helmet]),
      (27,mtef_visitor_source|mtef_team_3,af_override_all,aif_start_alarmed,1,[itm_practice_lance,itm_practice_shield,itm_practice_horse,itm_arena_tunic_yellow, itm_gold_tourney_helmet]),
      (28,mtef_visitor_source|mtef_team_3,af_override_all,aif_start_alarmed,1,[itm_practice_bow,itm_practice_arrows,itm_practice_dagger, itm_arena_tunic_yellow, itm_gold_tourney_helmet]),
      (29,mtef_visitor_source|mtef_team_3,af_override_all,aif_start_alarmed,1,[itm_practice_sword,itm_practice_shield,itm_arena_tunic_yellow]),
      (30,mtef_visitor_source|mtef_team_3,af_override_all,aif_start_alarmed,1,[itm_heavy_practice_sword,itm_practice_horse,itm_arena_tunic_yellow]),
      (31,mtef_visitor_source|mtef_team_3,af_override_all,aif_start_alarmed,1,[itm_practice_lance,itm_practice_shield,itm_practice_horse,itm_arena_tunic_yellow, itm_gold_tourney_helmet]),
#32
      (32, mtef_visitor_source|mtef_team_1,af_override_all,aif_start_alarmed,1,[itm_heavy_practice_sword]),
      (33,mtef_visitor_source|mtef_team_2,af_override_all,aif_start_alarmed,1,[itm_practice_staff]),
      (34,mtef_visitor_source|mtef_team_3,af_override_all,aif_start_alarmed,1,[itm_practice_sword, itm_practice_shield]),
      (35,mtef_visitor_source|mtef_team_4,af_override_all,aif_start_alarmed,1,[itm_practice_staff]),
      (36, mtef_visitor_source|mtef_team_1,af_override_all,aif_start_alarmed,1,[itm_practice_bow,itm_practice_arrows, itm_practice_dagger]),
      (37,mtef_visitor_source|mtef_team_2,af_override_all,aif_start_alarmed,1,[itm_practice_sword, itm_practice_shield]),
      (38,mtef_visitor_source|mtef_team_3,af_override_all,aif_start_alarmed,1,[itm_heavy_practice_sword]),
      (39,mtef_visitor_source|mtef_team_4,af_override_all,aif_start_alarmed,1,[itm_practice_staff]),
#40-49 not used yet
      (24,mtef_visitor_source|mtef_team_3,af_override_all,aif_start_alarmed,1,[itm_practice_bow,itm_practice_arrows,itm_practice_horse,itm_arena_tunic_yellow, itm_gold_tourney_helmet]),
      (24,mtef_visitor_source|mtef_team_3,af_override_all,aif_start_alarmed,1,[itm_heavy_practice_sword,itm_arena_tunic_yellow, itm_gold_tourney_helmet]),
      (24,mtef_visitor_source|mtef_team_3,af_override_all,aif_start_alarmed,1,[itm_heavy_practice_sword,itm_practice_horse,itm_arena_tunic_yellow, itm_gold_tourney_helmet]),
      (24,mtef_visitor_source|mtef_team_3,af_override_all,aif_start_alarmed,1,[itm_practice_lance,itm_practice_shield,itm_practice_horse,itm_arena_tunic_yellow, itm_gold_tourney_helmet]),
      (24,mtef_visitor_source|mtef_team_3,af_override_all,aif_start_alarmed,1,[itm_practice_bow,itm_practice_arrows,itm_practice_dagger, itm_arena_tunic_yellow, itm_gold_tourney_helmet]),
      (24,mtef_visitor_source|mtef_team_3,af_override_all,aif_start_alarmed,1,[itm_practice_sword,itm_practice_shield,itm_arena_tunic_yellow]),
      (24,mtef_visitor_source|mtef_team_3,af_override_all,aif_start_alarmed,1,[itm_heavy_practice_sword,itm_practice_horse,itm_arena_tunic_yellow]),
      (24,mtef_visitor_source|mtef_team_3,af_override_all,aif_start_alarmed,1,[itm_practice_lance,itm_practice_shield,itm_practice_horse,itm_arena_tunic_yellow, itm_gold_tourney_helmet]),
      (24,mtef_visitor_source|mtef_team_3,af_override_all,aif_start_alarmed,1,[itm_practice_bow,itm_practice_arrows,itm_practice_horse,itm_arena_tunic_yellow, itm_gold_tourney_helmet]),
      (24,mtef_visitor_source|mtef_team_3,af_override_all,aif_start_alarmed,1,[itm_practice_bow,itm_practice_arrows,itm_practice_horse,itm_arena_tunic_yellow, itm_gold_tourney_helmet]),

      (50, mtef_scene_source,af_override_horse|af_override_weapons|af_override_head,0,1,[]),
      (51, mtef_visitor_source,af_override_horse|af_override_weapons|af_override_head,0,1,[]),
      (52, mtef_scene_source,af_override_horse,0,1,[]),
#not used yet:
      (53, mtef_scene_source,af_override_horse,0,1,[]),(54, mtef_scene_source,af_override_horse,0,1,[]),(55, mtef_scene_source,af_override_horse,0,1,[]),
#used for torunament master scene

      (56, mtef_visitor_source|mtef_team_0, af_override_all, aif_start_alarmed, 1, [itm_practice_sword, itm_practice_shield, itm_padded_cloth, itm_segmented_helmet]),
      (57, mtef_visitor_source|mtef_team_0, af_override_all, aif_start_alarmed, 1, [itm_practice_sword, itm_practice_shield, itm_padded_cloth, itm_segmented_helmet]),
    ],
    tournament_triggers
  ),

  (
    "arena_challenge_fight",mtf_arena_fight|mtf_commit_casualties,-1,
    "You enter a melee fight in the arena.",
    [
      (56, mtef_visitor_source|mtef_team_0, 0, aif_start_alarmed, 1, []),
      (58, mtef_visitor_source|mtef_team_2, 0, aif_start_alarmed, 1, []),
    ],
    [
      common_inventory_not_available,
      (ti_tab_pressed, 0, 0, [(display_message, "str_cannot_leave_now")], []),
      (ti_before_mission_start, 0, 0, [], [(call_script, "script_change_banners_and_chest")]),

      (0, 0, ti_once, [],
       [
         (call_script, "script_music_set_situation_with_culture", mtf_sit_arena),
         ]),

		 
	#NOTE -- THIS IS A VESTIGIAL SCRIPT. FOR LORD DUELS, USE THE NEXT SCRIPT DOWN 	 
      (1, 4, ti_once, [
	  (this_or_next|main_hero_fallen),
		(num_active_teams_le,1)],
       [
           (try_begin),
             (main_hero_fallen),
			 (check_quest_active, "qst_duel_for_lady"),
			 (quest_slot_eq, "qst_duel_for_lady", slot_quest_target_troop, "$g_duel_troop"),
             (call_script, "script_fail_quest", "qst_duel_for_lady"),
           (else_try),
			 (check_quest_active, "qst_duel_for_lady"),
			 (quest_slot_eq, "qst_duel_for_lady", slot_quest_target_troop, "$g_duel_troop"),
             (call_script, "script_succeed_quest", "qst_duel_for_lady"),
		   (else_try),
             (main_hero_fallen),
			 (check_quest_active, "qst_duel_courtship_rival"),
			 (quest_slot_eq, "qst_duel_courtship_rival", slot_quest_target_troop, "$g_duel_troop"),
             (call_script, "script_fail_quest", "qst_duel_courtship_rival"),
           (else_try),
			 (check_quest_active, "qst_duel_courtship_rival"),
			 (quest_slot_eq, "qst_duel_courtship_rival", slot_quest_target_troop, "$g_duel_troop"),
             (call_script, "script_succeed_quest", "qst_duel_courtship_rival"),
		   (else_try),	 
             (main_hero_fallen),
			 (check_quest_active, "qst_duel_avenge_insult"),
			 (quest_slot_eq, "qst_duel_avenge_insult", slot_quest_target_troop, "$g_duel_troop"),
             (call_script, "script_fail_quest", "qst_duel_avenge_insult"),
           (else_try),
			 (check_quest_active, "qst_duel_avenge_insult"),
			 (quest_slot_eq, "qst_duel_avenge_insult", slot_quest_target_troop, "$g_duel_troop"),
             (call_script, "script_succeed_quest", "qst_duel_avenge_insult"),
		   (else_try),	 
             (main_hero_fallen),
			 (check_quest_active, "qst_denounce_lord"),
			 (quest_slot_eq, "qst_denounce_lord", slot_quest_target_troop, "$g_duel_troop"),
             (call_script, "script_fail_quest", "qst_denounce_lord"),
           (else_try),
			 (check_quest_active, "qst_denounce_lord"),
			 (quest_slot_eq, "qst_denounce_lord", slot_quest_target_troop, "$g_duel_troop"),
             (call_script, "script_succeed_quest", "qst_denounce_lord"),
		   (else_try),
			 (quest_get_slot, ":target_troop", "qst_denounce_lord", slot_quest_target_troop),
		     (str_store_troop_name, s4, ":target_troop"),
		   (try_end),
           (finish_mission),
           ]),
    ],
  ),

  (
    "duel_with_lord",mtf_arena_fight|mtf_commit_casualties,-1,
    "You enter a melee fight in the arena.",
    [    
	  (0, mtef_visitor_source|mtef_team_0,af_override_all,aif_start_alarmed,1,[itm_sword_medieval_a,itm_arena_tunic_blue]),
	  (16, mtef_visitor_source|mtef_team_1,af_override_all,aif_start_alarmed,1,[itm_sword_medieval_a,itm_arena_tunic_blue]),
    ],
    [
      common_inventory_not_available,
      (ti_tab_pressed, 0, 0, [(display_message, "str_cannot_leave_now")], []),
      (ti_before_mission_start, 0, 0, [], [(call_script, "script_change_banners_and_chest")]),

      (0, 0, ti_once, [],
       [
         (call_script, "script_music_set_situation_with_culture", mtf_sit_arena),
         ]),


      (1, 4, ti_once, [
	  (this_or_next|main_hero_fallen),
		(num_active_teams_le,1)],
       [
           (try_begin),
             (main_hero_fallen),
			 (check_quest_active, "qst_duel_for_lady"),
			 (quest_slot_eq, "qst_duel_for_lady", slot_quest_target_troop, "$g_duel_troop"),
             (call_script, "script_fail_quest", "qst_duel_for_lady"),
           (else_try),
			 (check_quest_active, "qst_duel_for_lady"),
			 (quest_slot_eq, "qst_duel_for_lady", slot_quest_target_troop, "$g_duel_troop"),
             (call_script, "script_succeed_quest", "qst_duel_for_lady"),
		   (else_try),
             (main_hero_fallen),
			 (check_quest_active, "qst_duel_courtship_rival"),
			 (quest_slot_eq, "qst_duel_courtship_rival", slot_quest_target_troop, "$g_duel_troop"),
             (call_script, "script_fail_quest", "qst_duel_courtship_rival"),
           (else_try),
			 (check_quest_active, "qst_duel_courtship_rival"),
			 (quest_slot_eq, "qst_duel_courtship_rival", slot_quest_target_troop, "$g_duel_troop"),
             (call_script, "script_succeed_quest", "qst_duel_courtship_rival"),
		   (else_try),	 
             (main_hero_fallen),
			 (check_quest_active, "qst_duel_avenge_insult"),
			 (quest_slot_eq, "qst_duel_avenge_insult", slot_quest_target_troop, "$g_duel_troop"),
             (call_script, "script_fail_quest", "qst_duel_avenge_insult"),
           (else_try),
			 (check_quest_active, "qst_duel_avenge_insult"),
			 (quest_slot_eq, "qst_duel_avenge_insult", slot_quest_target_troop, "$g_duel_troop"),
             (call_script, "script_succeed_quest", "qst_duel_avenge_insult"),
		   (else_try),	 
             (main_hero_fallen),
			 (check_quest_active, "qst_denounce_lord"),
			 (quest_slot_eq, "qst_denounce_lord", slot_quest_target_troop, "$g_duel_troop"),
             (call_script, "script_fail_quest", "qst_denounce_lord"),
           (else_try),
			 (check_quest_active, "qst_denounce_lord"),
			 (quest_slot_eq, "qst_denounce_lord", slot_quest_target_troop, "$g_duel_troop"),
             (call_script, "script_succeed_quest", "qst_denounce_lord"),
		   (else_try),
			 (quest_get_slot, ":target_troop", "qst_denounce_lord", slot_quest_target_troop),
		     (str_store_troop_name, s4, ":target_troop"),
		   (try_end),
           (finish_mission),
           ]),
    ],
  ),  
  
  
  
  
##   (
##    "tutorial",0,-1,
##    "You enter the training ground.",
##    [
##        (1,mtef_leader_only,af_override_horse,0,1,[]), #af_override_weapons
##        (2,mtef_scene_source,af_override_horse,0,1,[]), #af_override_weapons
##     ],
##    [
##      (ti_tab_pressed, 0, 0, [],
##       [(question_box,"str_do_you_wish_to_leave_tutorial")]),
##      (ti_question_answered, 0, 0, [],
##       [(store_trigger_param_1,":answer"),
##        (eq,":answer",0),
##        (finish_mission,0),
##        (leave_encounter),
##        (change_screen_return),
##        (troop_remove_item, "trp_player", "itm_tutorial_sword"),
##        (troop_remove_item, "trp_player", "itm_tutorial_axe"),
##        (troop_remove_item, "trp_player", "itm_tutorial_spear"),
##        (troop_remove_item, "trp_player", "itm_tutorial_club"),
##        (troop_remove_item, "trp_player", "itm_tutorial_battle_axe"),
##        (troop_remove_item, "trp_player", "itm_tutorial_arrows"),
##        (troop_remove_item, "trp_player", "itm_tutorial_bolts"),
##        (troop_remove_item, "trp_player", "itm_tutorial_short_bow"),
##        (troop_remove_item, "trp_player", "itm_tutorial_crossbow"),
##        (troop_remove_item, "trp_player", "itm_tutorial_throwing_daggers"),
##        
##        (check_quest_active, "qst_destroy_dummies"),
##        (cancel_quest,"qst_destroy_dummies"),
##        ]),
###      (ti_inventory_key_pressed, 0, 0, [(display_message,"str_cant_use_inventory_tutorial")], []),
##      (ti_inventory_key_pressed, 0, 0, [(set_trigger_result,1)], []),
##
##        
##      (0, 0, ti_once, [],
##       [
##        (assign, "$tutorial_enter_melee", 0),
##        (assign, "$tutorial_enter_ranged", 0),
##        (assign, "$tutorial_enter_mounted", 0),
##        (assign, "$tutorial_camp_stage", 0),
##        (assign, "$tutorial_quest_taken", 0),
##        (assign, "$tutorial_quest_succeeded", 0),
##        (assign, "$tutorial_num_total_dummies_destroyed", 0),
##        (assign, "$tutorial_melee_chest", 0),
##        (assign, "$tutorial_ranged_chest", 0),
##        (assign, "$tutorial_award_taken", 0),
##
##           
##        (entry_point_get_position,2,2),#Trainer
##        (entry_point_get_position,16,16),#Horse
##        (set_spawn_position, 16),
##        (spawn_horse, "itm_tutorial_saddle_horse"),
##
##        (troop_remove_item, "trp_tutorial_chest_1", "itm_tutorial_sword"),
##        (troop_remove_item, "trp_tutorial_chest_1", "itm_tutorial_axe"),
##        (troop_remove_item, "trp_tutorial_chest_1", "itm_tutorial_spear"),
##        (troop_remove_item, "trp_tutorial_chest_1", "itm_tutorial_club"),
##        (troop_remove_item, "trp_tutorial_chest_1", "itm_tutorial_battle_axe"),
##        (troop_remove_item, "trp_tutorial_chest_2", "itm_tutorial_arrows"),
##        (troop_remove_item, "trp_tutorial_chest_2", "itm_tutorial_bolts"),
##        (troop_remove_item, "trp_tutorial_chest_2", "itm_tutorial_short_bow"),
##        (troop_remove_item, "trp_tutorial_chest_2", "itm_tutorial_crossbow"),
##        (troop_remove_item, "trp_tutorial_chest_2", "itm_tutorial_throwing_daggers"),
##        (troop_add_item, "trp_tutorial_chest_1", "itm_tutorial_sword"),
##        (troop_add_item, "trp_tutorial_chest_1", "itm_tutorial_axe"),
##        (troop_add_item, "trp_tutorial_chest_1", "itm_tutorial_spear"),
##        (troop_add_item, "trp_tutorial_chest_1", "itm_tutorial_club"),
##        (troop_add_item, "trp_tutorial_chest_1", "itm_tutorial_battle_axe"),
##        (troop_add_item, "trp_tutorial_chest_2", "itm_tutorial_arrows"),
##        (troop_add_item, "trp_tutorial_chest_2", "itm_tutorial_bolts"),
##        (troop_add_item, "trp_tutorial_chest_2", "itm_tutorial_short_bow"),
##        (troop_add_item, "trp_tutorial_chest_2", "itm_tutorial_crossbow"),
##        (troop_add_item, "trp_tutorial_chest_2", "itm_tutorial_throwing_daggers"),
##        ]
##       ),
##     
##      (1, 0, ti_once, [(store_character_level, ":player_level", "trp_player"),
##                       (le, ":player_level", 1),
##                       (get_player_agent_no, ":player_agent"),
##                       (ge, ":player_agent", 0),
##                       (agent_get_position, pos1, ":player_agent"),
##                       (entry_point_get_position,3,3),
##                       (get_distance_between_positions, ":distance_to_area", 1, 3),
##                       (lt, ":distance_to_area", 500),
##                       (eq, "$tutorial_enter_melee", 0),],
##       [(tutorial_box,"str_tutorial_enter_melee", "str_tutorial"), (val_add,"$tutorial_enter_melee", 1)]),
##      (1, 0, ti_once, [(store_character_level, ":player_level", "trp_player"),
##                       (le, ":player_level", 1),
##                       (get_player_agent_no, ":player_agent"),
##                       (ge, ":player_agent", 0),
##                       (neg|conversation_screen_is_active),
##                       (agent_get_position, pos1, ":player_agent"),
##                       (entry_point_get_position,4,4),
##                       (get_distance_between_positions, ":distance_to_area", 1, 4),
##                       (lt, ":distance_to_area", 500),
##                       (eq, "$tutorial_enter_ranged", 0),],
##       [(tutorial_box,"str_tutorial_enter_ranged", "str_tutorial"), (val_add,"$tutorial_enter_ranged", 1)]),
##      (1, 0, ti_once, [(store_character_level, ":player_level", "trp_player"),
##                       (le, ":player_level", 1),
##                       (get_player_agent_no, ":player_agent"),
##                       (ge, ":player_agent", 0),
##                       (neg|conversation_screen_is_active),
##                       (agent_get_position, pos1, ":player_agent"),
##                       (entry_point_get_position,5,5),
##                       (get_distance_between_positions, ":distance_to_area", 1, 5),
##                       (lt, ":distance_to_area", 500),
##                       (eq, "$tutorial_enter_mounted", 0),],
##       [(tutorial_box,"str_tutorial_enter_mounted", "str_tutorial"), (val_add,"$tutorial_enter_mounted", 1)]),
##
##
##      (2, 0, ti_once, [(store_character_level, ":player_level", "trp_player"),
##                       (le, ":player_level", 1),
##                       (get_player_agent_no, ":player_agent"),
##                       (ge, ":player_agent", 0),
##                       (neg|conversation_screen_is_active),
##                       (agent_get_position, pos1, ":player_agent"),
##                       (entry_point_get_position,6,6),
##                       (get_distance_between_positions, ":distance_to_area", 1, 6),
##                       (lt, ":distance_to_area", 300),
##                       (eq, "$tutorial_melee_chest", 0),],
##       [(tutorial_box,"str_tutorial_melee_chest", "str_tutorial"), (val_add,"$tutorial_melee_chest", 1)]),
##      (2, 0, ti_once, [(store_character_level, ":player_level", "trp_player"),
##                       (le, ":player_level", 1),
##                       (get_player_agent_no, ":player_agent"),
##                       (ge, ":player_agent", 0),
##                       (agent_get_position, pos1, ":player_agent"),
##                       (entry_point_get_position,7,7),
##                       (get_distance_between_positions, ":distance_to_area", 1, 7),
##                       (lt, ":distance_to_area", 300),
##                       (eq, "$tutorial_ranged_chest", 0),],
##       [(tutorial_box,"str_tutorial_ranged_chest", "str_tutorial"), (val_add,"$tutorial_ranged_chest", 1)]),
##
##      (2, 0, ti_once, [(store_character_level, ":player_level", "trp_player"),
##                       (le, ":player_level", 1),
##                       (eq, "$tutorial_item_equipped", 0),
##                       (try_begin),
##                         (troop_has_item_equipped, "trp_player", "itm_tutorial_sword"),
##                         (assign, "$tutorial_item_equipped", 1),
##                       (else_try),
##                         (troop_has_item_equipped, "trp_player", "itm_tutorial_axe"),
##                         (assign, "$tutorial_item_equipped", 1),
##                       (else_try),
##                         (troop_has_item_equipped, "trp_player", "itm_tutorial_spear"),
##                         (assign, "$tutorial_item_equipped", 1),
##                       (else_try),
##                         (troop_has_item_equipped, "trp_player", "itm_tutorial_club"),
##                         (assign, "$tutorial_item_equipped", 1),
##                       (else_try),
##                         (troop_has_item_equipped, "trp_player", "itm_tutorial_battle_axe"),
##                         (assign, "$tutorial_item_equipped", 1),
##                       (else_try),
##                         (troop_has_item_equipped, "trp_player", "itm_tutorial_arrows"),
##                         (assign, "$tutorial_item_equipped", 1),
##                       (else_try),
##                         (troop_has_item_equipped, "trp_player", "itm_tutorial_bolts"),
##                         (assign, "$tutorial_item_equipped", 1),
##                       (else_try),
##                         (troop_has_item_equipped, "trp_player", "itm_tutorial_short_bow"),
##                         (assign, "$tutorial_item_equipped", 1),
##                       (else_try),
##                         (troop_has_item_equipped, "trp_player", "itm_tutorial_crossbow"),
##                         (assign, "$tutorial_item_equipped", 1),
##                       (else_try),
##                         (troop_has_item_equipped, "trp_player", "itm_tutorial_throwing_daggers"),
##                         (assign, "$tutorial_item_equipped", 1),
##                       (try_end),
##                       (eq, "$tutorial_item_equipped", 1),],
##       [(tutorial_box,"str_tutorial_item_equipped", "str_tutorial")]),
##
##
##      
##
###      (2, 0, ti_once, [(get_player_agent_no, ":player_agent"),
###                       (agent_get_position, pos1, ":player_agent"),
###                       (entry_point_get_position,21,21),
###                       (get_distance_between_positions, ":distance_to_area", 1, 21),
###                       (lt, ":distance_to_area", 200),
###                       (eq, "$tutorial_group_of_weapons", 0),],
###       [(tutorial_box,"str_tutorial_group_of_weapons", "str_tutorial"), (val_add,"$tutorial_group_of_weapons", 1)]),
##
##      
##
##      (1, 5, ti_once, [(eq,"$tutorial_camp_stage",0),
##                       (neg|conversation_screen_is_active),
##                       (eq,"$tutorial_quest_award_taken",0),
##                       (store_character_level, ":player_level", "trp_player"),
##                       (le, ":player_level", 1),
##                       (tutorial_box,"str_tutorial_camp1","str_tutorial"),],
##          [(val_add,"$tutorial_camp_stage",1)]),
##      (1, 3, ti_once, [(eq,"$tutorial_camp_stage",1),
##                       (neg|conversation_screen_is_active),
##                       (tutorial_box,"str_tutorial_camp2","str_tutorial"),],
##          [(val_add,"$tutorial_camp_stage",1)]),
##      (1, 3, ti_once, [(eq,"$tutorial_camp_stage",2),
##                       (neg|conversation_screen_is_active),
##                       (tutorial_box,"str_tutorial_camp3","str_tutorial"),],
##          [(val_add,"$tutorial_camp_stage",1)]),
##      (1, 3, ti_once, [(eq,"$tutorial_camp_stage",3),(eq, "$tutorial_award_taken", 0),
##                       (neg|conversation_screen_is_active),
##                       (tutorial_box,"str_tutorial_camp4","str_tutorial"),],
##          [(val_add,"$tutorial_camp_stage",2)]),
##      
##     
##      (1, 3, ti_once, [(eq,"$tutorial_camp_stage",5),
##                       (neg|conversation_screen_is_active),
##                       (eq,"$tutorial_quest_taken",1),
##                       (tutorial_box,"str_tutorial_camp6","str_tutorial"),],
##          [(val_add,"$tutorial_camp_stage",1)]),
##
##      (1, 3, ti_once, [(eq,"$tutorial_camp_stage",6),
##                       (neg|conversation_screen_is_active),
##                       (ge,"$tutorial_num_total_dummies_destroyed",10),
##                       (tutorial_box,"str_tutorial_camp7","str_tutorial"),],
##          [(val_add,"$tutorial_camp_stage",1), (assign,"$tutorial_quest_succeeded",1),]),
##      
##      (1, 3, ti_once, [(eq,"$tutorial_camp_stage",7),
##                       (neg|conversation_screen_is_active),
##                       (eq,"$tutorial_quest_award_taken",1),
##                       (tutorial_box,"str_tutorial_camp8","str_tutorial"),
##                       (troop_add_proficiency_points, "trp_player", 10),
##                       (assign, "$tutorial_last_proficiency_sum", 0),
##                       (try_for_range, ":cur_attribute", 0, num_weapon_proficiencies),
##                         (store_proficiency_level, ":cur_attribute_point", "trp_player", ":cur_attribute"),
##                         (val_add, "$tutorial_last_proficiency_sum", ":cur_attribute_point"),
##                       (try_end),],
##       [(val_add,"$tutorial_camp_stage",1),]),
##      
##      (1, 3, ti_once, [(eq,"$tutorial_camp_stage",8),
##                       (neg|conversation_screen_is_active),
##                       (assign, ":new_proficiency_sum", 0),
##                       (try_for_range, ":cur_attribute", 0, num_weapon_proficiencies),
##                         (store_proficiency_level, ":cur_attribute_point", "trp_player", ":cur_attribute"),
##                         (val_add, ":new_proficiency_sum", ":cur_attribute_point"),
##                       (try_end),
##                       (assign, reg(48), ":new_proficiency_sum"),
##                       (assign, reg(49), "$tutorial_last_proficiency_sum"),
##                       (lt,"$tutorial_last_proficiency_sum",":new_proficiency_sum"),
##                       (tutorial_box,"str_tutorial_camp9","str_tutorial"),],
##          [(val_add,"$tutorial_camp_stage",1)]),
##
##      (2, 0, 0, [(check_quest_active,"qst_destroy_dummies"),
##                 (le, "$tutorial_num_total_dummies_destroyed", 10),],
##          [
##              (assign, ":progress", "$tutorial_num_total_dummies_destroyed"),
##              (val_mul, ":progress", 10),
##              (set_quest_progression,"qst_destroy_dummies",":progress"),
##              ]
##       ),
##
##    ],
##  ),


  (
    "wedding",0,-1,
    "Wedding",
    [
        (0,mtef_visitor_source,af_override_everything,0,1,[itm_tabard, itm_ankle_boots]),
        (1,mtef_visitor_source,af_override_everything,0,1,[itm_bride_dress, itm_bride_crown, itm_bride_shoes]),
        (2,mtef_visitor_source,af_castle_lord,0,1,[]),
        (3,mtef_visitor_source,af_override_everything,0,1,[itm_courtly_outfit, itm_blue_hose]),
        (4,mtef_visitor_source,af_castle_lord,0,1,[]),
        (5,mtef_visitor_source,af_castle_lord,0,1,[]),
        (6,mtef_visitor_source,af_castle_lord,0,1,[]),
        (7,mtef_visitor_source,af_castle_lord,0,1,[]),
        (8,mtef_visitor_source,af_castle_lord,0,1,[]),
        (9,mtef_visitor_source,af_castle_lord,0,1,[]),
        (10,mtef_visitor_source,af_castle_lord,0,1,[]),
        (11,mtef_visitor_source,af_castle_lord,0,1,[]),
        (12,mtef_visitor_source,af_castle_lord,0,1,[]),
        (13,mtef_visitor_source,af_castle_lord,0,1,[]),
        (14,mtef_visitor_source,af_castle_lord,0,1,[]),
        (15,mtef_visitor_source,af_castle_lord,0,1,[]),
        (16,mtef_visitor_source,af_castle_lord,0,1,[]),
        (17,mtef_visitor_source,af_castle_lord,0,1,[]),
        (18,mtef_visitor_source,af_castle_lord,0,1,[]),
        (19,mtef_visitor_source,af_castle_lord,0,1,[]),
        (20,mtef_visitor_source,af_castle_lord,0,1,[]),
        (21,mtef_visitor_source,af_castle_lord,0,1,[]),
        (22,mtef_visitor_source,af_castle_lord,0,1,[]),
        (23,mtef_visitor_source,af_castle_lord,0,1,[]),
        (24,mtef_visitor_source,af_castle_lord,0,1,[]),
        (25,mtef_visitor_source,af_castle_lord,0,1,[]),
        (26,mtef_visitor_source,af_castle_lord,0,1,[]),
        (27,mtef_visitor_source,af_castle_lord,0,1,[]),
        (28,mtef_visitor_source,af_castle_lord,0,1,[]),
        (29,mtef_visitor_source,af_castle_lord,0,1,[]),
        (30,mtef_visitor_source,af_castle_lord,0,1,[]),
        (31,mtef_visitor_source,af_castle_lord,0,1,[]),
     ],
    [
      (ti_tab_pressed, 0, 0, [],
       [
         (show_object_details_overlay, 1),
         (finish_mission,0),
        ]),
      (ti_question_answered, 0, 0, [],
       [(store_trigger_param_1,":answer"),
        (eq,":answer",0),
        (show_object_details_overlay, 1),
        (finish_mission,0),
        ]),

      (ti_after_mission_start, 0, 0, [],
       [
        (assign, "$g_wedding_state", 0),
        (play_track, "track_wedding", 2),
        (show_object_details_overlay, 0),
         ]),

      (ti_on_agent_spawn, 0, 0, [],
       [
         (store_trigger_param_1, ":agent_no"),
         (agent_get_troop_id, ":troop_no", ":agent_no"),
         (troop_get_type, ":gender", ":troop_no"),
         (set_fixed_point_multiplier, 100),
         (try_begin),
           (eq, ":troop_no", "$g_wedding_bishop_troop"),
         (else_try),
           (eq, ":troop_no", "$g_wedding_bride_troop"),
           (agent_set_no_dynamics, ":agent_no", 1),
           (init_position, pos1),
           (position_set_z, pos1, -1000),
           (agent_set_position, ":agent_no", pos1),
         (else_try),
           (eq, ":troop_no", "$g_wedding_brides_dad_troop"),
           (agent_set_no_dynamics, ":agent_no", 1),
           (init_position, pos1),
           (position_set_z, pos1, -1000),
           (agent_set_position, ":agent_no", pos1),
         (else_try),
           (eq, ":troop_no", "$g_wedding_groom_troop"),
           (agent_set_no_dynamics, ":agent_no", 1),
           (init_position, pos1),
           (position_move_x, pos1, 175),
           (position_move_z, pos1, 10),
           (position_rotate_z, pos1, 180),
           (agent_set_position, ":agent_no", pos1),
           (agent_set_animation, ":agent_no", "anim_wedding_groom_wait"),
         (else_try),
           (try_begin),
             (eq, ":gender", 0), #male
             (store_random_in_range, ":random_no", 0, 3),
             (try_begin),
               (eq, ":random_no", 0),
               (agent_set_slot, ":agent_no", slot_agent_cur_animation, "anim_wedding_guest_notr"),
               (agent_set_animation, ":agent_no", "anim_wedding_guest_notr"),
             (else_try),
               (agent_set_slot, ":agent_no", slot_agent_cur_animation, "anim_wedding_guest"),
               (agent_set_animation, ":agent_no", "anim_wedding_guest"),
             (try_end),
           (else_try), #female
             (agent_set_slot, ":agent_no", slot_agent_cur_animation, "anim_wedding_guest_woman"),
             (agent_set_animation, ":agent_no", "anim_wedding_guest_woman"),
           (try_end),
           (store_random_in_range, ":progress", 0, 100),
           (agent_set_animation_progress, ":agent_no", ":progress"),
         (try_end),
         ]),

      (0, 0, 0,
       [
         (store_mission_timer_a, ":cur_time"),
         (set_fixed_point_multiplier, 100),
         (try_for_agents, ":agent_no"),
           (agent_get_troop_id, ":troop_no", ":agent_no"),
           (try_begin),
             (eq, ":troop_no", "$g_wedding_groom_troop"),
           (else_try),
             (eq, ":troop_no", "$g_wedding_bride_troop"),
           (else_try),
             (eq, ":troop_no", "$g_wedding_brides_dad_troop"),
           (else_try),
             (eq, ":troop_no", "$g_wedding_bishop_troop"),
           (else_try),
             (agent_get_slot, ":cur_animation", ":agent_no", slot_agent_cur_animation),
             (agent_set_animation, ":agent_no", ":cur_animation"),
           (try_end),
         (try_end),
         (try_begin),
           (eq, "$g_wedding_state", 0),
           (mission_cam_set_mode, 1, 0, 0),
           (init_position, pos1),
           (position_rotate_z, pos1, 180),
           (position_rotate_x, pos1, 5),
           (position_set_x, pos1, -500),
           (position_set_y, pos1, 1000),
           (position_set_z, pos1, 600),
           (mission_cam_set_position, pos1),
           (init_position, pos1),
           (position_rotate_z, pos1, 180),
           (position_rotate_x, pos1, -15),
           (position_set_x, pos1, -500),
           (position_set_y, pos1, 1000),
           (position_set_z, pos1, 600),
           (mission_cam_animate_to_position, pos1, 4000, 0),
           (val_add, "$g_wedding_state", 1),
         (else_try),
           (eq, "$g_wedding_state", 1),
           (ge, ":cur_time", 4),
           (init_position, pos1),
           (position_rotate_z, pos1, 90),
           (position_rotate_x, pos1, -10),
           (position_set_x, pos1, -580),
           (position_set_y, pos1, 700),
           (position_set_z, pos1, 200),
           (mission_cam_set_position, pos1),
           (init_position, pos1),
           (position_rotate_z, pos1, 150),
           (position_rotate_x, pos1, -10),
           (position_set_x, pos1, -580),
           (position_set_y, pos1, 100),
           (position_set_z, pos1, 200),
           (mission_cam_animate_to_position, pos1, 6000, 1),
           (val_add, "$g_wedding_state", 1),
         (else_try),
           (eq, "$g_wedding_state", 2),
           (ge, ":cur_time", 9),
           (mission_cam_animate_to_screen_color, 0xFF000000, 1000),
           (val_add, "$g_wedding_state", 1),
         (else_try),
           (eq, "$g_wedding_state", 3),
           (ge, ":cur_time", 10),
           (init_position, pos1),
           (position_move_x, pos1, 175),
           (position_move_z, pos1, 10),
           (position_rotate_z, pos1, 180),
           (try_for_agents, ":agent_no"),
             (agent_get_troop_id, ":agent_troop", ":agent_no"),
             (try_begin),
               (eq, ":agent_troop", "$g_wedding_bride_troop"),
               (agent_set_position, ":agent_no", pos1),
               (agent_set_animation, ":agent_no", "anim_wedding_bride_stairs"),
             (else_try),
               (eq, ":agent_troop", "$g_wedding_brides_dad_troop"),
               (agent_set_position, ":agent_no", pos1),
               (agent_set_animation, ":agent_no", "anim_wedding_dad_stairs"),
             (try_end),
           (try_end),
           (init_position, pos1),
           (position_rotate_z, pos1, -90),
           (position_set_x, pos1, 300),
           (position_set_y, pos1, 950),
           (position_set_z, pos1, 420),
           (mission_cam_set_position, pos1),
           (position_set_x, pos1, 175),
           (position_set_y, pos1, 950),
           (position_set_z, pos1, 320),
           (mission_cam_animate_to_position, pos1, 4000, 0),
           (mission_cam_animate_to_screen_color, 0x00000000, 500),
           (val_add, "$g_wedding_state", 1),
         (else_try),
           (eq, "$g_wedding_state", 4),
           (ge, ":cur_time", 14),
           (init_position, pos1),
           (position_rotate_z, pos1, -60),
           (position_rotate_x, pos1, 10),
           (position_set_x, pos1, -400),
           (position_set_y, pos1, 200),
           (position_set_z, pos1, 115),
           (mission_cam_set_position, pos1),
           (val_add, "$g_wedding_state", 1),
         (else_try),
           (eq, "$g_wedding_state", 5),
           (ge, ":cur_time", 20),
           (init_position, pos1),
           (position_move_x, pos1, 175),
           (position_move_z, pos1, 10),
           (position_rotate_z, pos1, 180),
           (try_for_agents, ":agent_no"),
             (agent_get_troop_id, ":agent_troop", ":agent_no"),
             (try_begin),
               (eq, ":agent_troop", "$g_wedding_bride_troop"),
               (agent_set_position, ":agent_no", pos1),
               (agent_set_animation, ":agent_no", "anim_wedding_bride_walk"),
             (else_try),
               (eq, ":agent_troop", "$g_wedding_brides_dad_troop"),
               (agent_set_position, ":agent_no", pos1),
               (agent_set_animation, ":agent_no", "anim_wedding_dad_walk"),
             (try_end),
           (try_end),
           (init_position, pos1),
           (position_rotate_z, pos1, -140),
           (position_rotate_x, pos1, -15),
           (position_set_x, pos1, -625),
           (position_set_y, pos1, -530),
           (position_set_z, pos1, 180),
           (mission_cam_set_position, pos1),
           (val_add, "$g_wedding_state", 1),
         (else_try),
           (eq, "$g_wedding_state", 6),
           (ge, ":cur_time", 22),
           (init_position, pos1),
           (position_rotate_z, pos1, 45),
           (position_rotate_x, pos1, -10),
           (position_set_x, pos1, -260),
           (position_set_y, pos1, 120),
           (position_set_z, pos1, 275),
           (mission_cam_set_position, pos1),
           (position_rotate_z, pos1, 10),
           (mission_cam_animate_to_position, pos1, 2000, 0),
           (val_add, "$g_wedding_state", 1),
         (else_try),
           (eq, "$g_wedding_state", 7),
           (ge, ":cur_time", 24),
           (init_position, pos1),
           (position_move_x, pos1, 175),
           (position_move_z, pos1, 10),
           (position_rotate_z, pos1, 180),
           (try_for_agents, ":agent_no"),
             (agent_get_troop_id, ":agent_troop", ":agent_no"),
             (try_begin),
               (eq, ":agent_troop", "$g_wedding_bride_troop"),
               (agent_set_position, ":agent_no", pos1),
               (agent_set_animation, ":agent_no", "anim_wedding_bride_last"),
             (else_try),
               (eq, ":agent_troop", "$g_wedding_brides_dad_troop"),
               (agent_set_position, ":agent_no", pos1),
               (agent_set_animation, ":agent_no", "anim_wedding_dad_last"),
             (else_try),
               (eq, ":agent_troop", "$g_wedding_groom_troop"),
               (agent_set_position, ":agent_no", pos1),
               (agent_set_animation, ":agent_no", "anim_wedding_groom_last"),
             (try_end),
           (try_end),
           (init_position, pos1),
           (position_rotate_z, pos1, -45),
           (position_rotate_x, pos1, -10),
           (position_set_x, pos1, -900),
           (position_set_y, pos1, -850),
           (position_set_z, pos1, 230),
           (mission_cam_set_position, pos1),
           (val_add, "$g_wedding_state", 1),
         (else_try),
           (eq, "$g_wedding_state", 8),
           (ge, ":cur_time", 31),
           (init_position, pos1),
           (position_set_x, pos1, -550),
           (position_set_y, pos1, -625),
           (position_set_z, pos1, 1500),
           (particle_system_burst, "psys_wedding_rose", pos1, 750),
           (val_add, "$g_wedding_state", 1),
         (else_try),
           (eq, "$g_wedding_state", 9),
           (ge, ":cur_time", 33),
           (init_position, pos1),
           (position_rotate_z, pos1, 180),
           (position_set_x, pos1, -536),
           (position_set_y, pos1, -415),
           (position_set_z, pos1, 135),
           (mission_cam_set_position, pos1),
           (position_rotate_z, pos1, -8),
           (position_set_z, pos1, 350),
           (position_rotate_x, pos1, 35),
           (mission_cam_animate_to_position_and_aperture, pos1, 10, 9000, 1),
           (val_add, "$g_wedding_state", 1),
         (else_try),
           (eq, "$g_wedding_state", 10),
           (ge, ":cur_time", 41),
           (mission_cam_set_screen_color, 0x00FFFFFF),
           (mission_cam_animate_to_screen_color, 0xFFFFFFFF, 3000),
           (val_add, "$g_wedding_state", 1),
         (else_try),
           (eq, "$g_wedding_state", 11),
           (ge, ":cur_time", 48),
           (show_object_details_overlay, 1),
           (finish_mission,0),
         (try_end),
         ], []),
    ],
  ),

  (
    "tutorial_training_ground",mtf_arena_fight,-1,
    "You enter the training ground.",
    [
      (0,mtef_visitor_source|mtef_team_0,0,0,1,[]),
      (1,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (2,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (3,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (4,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (5,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (6,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (7,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),

      (8,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (9,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (10,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (11,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (12,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (13,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (14,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (15,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),

      (16,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (17,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (18,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (19,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (20,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (21,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (22,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (23,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),

      (24,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (25,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (26,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (27,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (28,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (29,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (30,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (31,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),

      (32,mtef_visitor_source|mtef_team_0,af_override_weapons,aif_start_alarmed,1,[itm_practice_sword]),
      (33,mtef_visitor_source|mtef_team_0,af_override_weapons,aif_start_alarmed,1,[itm_practice_sword]),
      (34,mtef_visitor_source|mtef_team_0,af_override_weapons,aif_start_alarmed,1,[itm_practice_sword]),
      (35,mtef_visitor_source|mtef_team_0,af_override_weapons,aif_start_alarmed,1,[itm_practice_sword]),
      (36,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (37,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (38,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (39,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),

      (40,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (41,mtef_visitor_source|mtef_team_0,af_override_weapons,aif_start_alarmed,1,[itm_practice_bow, itm_practice_arrows]),
      (42,mtef_visitor_source|mtef_team_0,af_override_weapons,aif_start_alarmed,1,[itm_practice_bow, itm_practice_arrows]),
      (43,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (44,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (45,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (46,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (47,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),

      (48,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (49,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (50,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (51,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (52,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (53,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (54,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (55,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),

      (56,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (57,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (58,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (59,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (60,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (61,mtef_visitor_source|mtef_team_0,af_override_weapons,aif_start_alarmed,1,[itm_practice_sword]),
      (62,mtef_visitor_source|mtef_team_0,af_override_weapons,aif_start_alarmed,1,[itm_practice_sword]),
      (63,mtef_visitor_source|mtef_team_0,af_override_weapons,aif_start_alarmed,1,[itm_practice_bow, itm_practice_arrows]),
      (64,mtef_visitor_source|mtef_team_0,af_override_weapons,aif_start_alarmed,1,[itm_practice_bow, itm_practice_arrows]),
      ],
    [
      (ti_tab_pressed, 0, 0, [],
       [(try_begin),
         (lt, "$g_tutorial_training_ground_state", 20),
         (question_box, "str_do_you_wish_to_leave_tutorial"),
        (else_try),
          (finish_mission,0),
        (try_end),
        ]),
      (ti_question_answered, 0, 0, [],
       [(store_trigger_param_1,":answer"),
        (eq,":answer",0),
        (finish_mission,0),
        ]),
      (ti_inventory_key_pressed, 0, 0, [(display_message, "str_cant_use_inventory_tutorial")], []),

      (ti_battle_window_opened, 0, 0, [],
       [
         (start_presentation, "prsnt_tutorial_show_mouse_movement"),
        ]),

      (ti_on_agent_spawn, 0, 0, [],
       [
         (store_trigger_param_1, ":agent_no"),
         (agent_ai_set_always_attack_in_melee, ":agent_no", 1),
         (agent_set_no_death_knock_down_only, ":agent_no", 1),
         (agent_set_invulnerable_shield, ":agent_no", 1),
         (agent_get_position, pos1, ":agent_no"),
         (agent_set_slot, ":agent_no", slot_agent_spawn_entry_point, -1),
         (get_player_agent_no, ":player_agent"),
         (try_begin),
           (eq, ":agent_no", ":player_agent"),
           (agent_set_team, ":agent_no", 7),
         (try_end),
         (try_for_range, ":cur_entry_point", 0, 64),
           (entry_point_get_position, pos2, ":cur_entry_point"),
           (get_sq_distance_between_positions, ":dist", pos1, pos2),
           (lt, ":dist", 100), #10 cm
           (agent_set_slot, ":agent_no", slot_agent_spawn_entry_point, ":cur_entry_point"),
         (try_end),
         (agent_get_troop_id, ":cur_agent_troop", ":agent_no"),
         (try_begin),
           (eq, ":cur_agent_troop", "trp_tutorial_archer_1"),
           (agent_get_position, pos1, ":agent_no"),
           (agent_set_scripted_destination, ":agent_no", pos1),
           (scene_prop_get_num_instances, ":num_instances", "spr_archery_target_with_hit_a"),
           (assign, ":shortest_dist", 10000000),
           (assign, ":best_instance", -1),
           (try_for_range, ":cur_instance", 0, ":num_instances"),
             (scene_prop_get_instance, ":spr_instance", "spr_archery_target_with_hit_a", ":cur_instance"),
             (prop_instance_get_position, pos2, ":spr_instance"),
             (get_sq_distance_between_positions, ":cur_dist", pos1, pos2),
             (lt, ":cur_dist", ":shortest_dist"),
             (assign, ":shortest_dist", ":cur_dist"),
             (assign, ":best_instance", ":spr_instance"),
           (try_end),
           (agent_set_slot, ":agent_no", slot_agent_target_prop_instance, ":best_instance"),
         (else_try),
           (this_or_next|eq, ":cur_agent_troop", "trp_tutorial_rider_1"),
           (eq, ":cur_agent_troop", "trp_tutorial_rider_2"),
           (agent_set_slot, ":agent_no", slot_agent_target_entry_point, 48),
           (agent_set_slot, ":agent_no", slot_agent_target_prop_instance, -1),
           (entry_point_get_position, pos1, 48),
           (agent_set_scripted_destination, ":agent_no", pos1),
         (try_end),
         ]),

      (ti_on_agent_knocked_down, 0, 0, [],
       [
         (store_trigger_param_1, ":agent_no"),
         (store_trigger_param_2, ":enemy_agent_no"),
         (agent_get_troop_id, ":agent_troop", ":agent_no"),
         (agent_get_troop_id, ":enemy_agent_troop", ":enemy_agent_no"),
         (try_begin),
           (ge, "$g_tutorial_training_ground_melee_trainer_attack", 0),
           #do nothing
         (else_try),
           (ge, "$g_tutorial_training_ground_melee_trainer_parry", 0),
           (try_begin),
             (eq, ":agent_troop", "trp_player"),
             (eq, ":enemy_agent_troop", "$g_tutorial_training_ground_melee_trainer_parry"),
             (assign, "$g_tutorial_training_ground_melee_state", 0),
             (agent_set_team, ":agent_no", 0),
             (agent_set_team, ":enemy_agent_no", 7),
             (tutorial_message, -1),
             (assign, "$g_tutorial_mouse_dir", -1),
             (assign, "$g_tutorial_mouse_click", -1),
             (assign, "$g_tutorial_training_ground_conversation_state", 2), #player knocked down in parry
             (play_sound, "snd_tutorial_fail"),
             (start_mission_conversation, "$g_tutorial_training_ground_melee_trainer_parry"),
             (assign, "$g_tutorial_training_ground_melee_trainer_parry", -1),
             (try_begin),
               (eq, "$g_tutorial_training_ground_melee_trainer_action_state", 1), #still in attack ready action
               (agent_set_attack_action, ":agent_no", 0, 0), #release
             (try_end),
           (else_try),
             (eq, ":enemy_agent_troop", "trp_player"),
             (eq, ":agent_troop", "$g_tutorial_training_ground_melee_trainer_parry"),
             (agent_set_team, ":agent_no", 7),
             (agent_set_team, ":enemy_agent_no", 0),
             (tutorial_message, -1),
             (assign, "$g_tutorial_mouse_dir", -1),
             (assign, "$g_tutorial_mouse_click", -1),
             (assign, "$g_tutorial_training_ground_conversation_state", 3), #trainer knocked down in parry
             (play_sound, "snd_tutorial_fail"),
             (start_mission_conversation, "$g_tutorial_training_ground_melee_trainer_parry"),
             (assign, "$g_tutorial_training_ground_melee_trainer_parry", -1),
             (try_begin),
               (eq, "$g_tutorial_training_ground_melee_trainer_action_state", 1), #still in attack ready action
               (agent_set_attack_action, ":agent_no", 0, 0), #release
             (try_end),
           (try_end),
         (else_try),
           (ge, "$g_tutorial_training_ground_melee_trainer_chamber", 0),
           (try_begin),
             (eq, ":agent_troop", "trp_player"),
             (eq, ":enemy_agent_troop", "$g_tutorial_training_ground_melee_trainer_chamber"),
             (assign, "$g_tutorial_training_ground_melee_state", 0),
             (agent_set_team, ":agent_no", 0),
             (agent_set_team, ":enemy_agent_no", 7),
             (tutorial_message, -1),
             (assign, "$g_tutorial_mouse_dir", -1),
             (assign, "$g_tutorial_mouse_click", -1),
             (assign, "$g_tutorial_training_ground_conversation_state", 7), #player knocked down in chamber
             (play_sound, "snd_tutorial_fail"),
             (start_mission_conversation, "$g_tutorial_training_ground_melee_trainer_chamber"),
             (assign, "$g_tutorial_training_ground_melee_trainer_chamber", -1),
             (try_begin),
               (eq, "$g_tutorial_training_ground_melee_trainer_action_state", 1), #still in attack ready action
               (agent_set_attack_action, ":agent_no", 0, 0), #release
             (try_end),
           (else_try),
             (eq, ":enemy_agent_troop", "trp_player"),
             (eq, ":agent_troop", "$g_tutorial_training_ground_melee_trainer_chamber"),
             (agent_set_team, ":agent_no", 7),
             (agent_set_team, ":enemy_agent_no", 0),
             (tutorial_message, -1),
             (assign, "$g_tutorial_mouse_dir", -1),
             (assign, "$g_tutorial_mouse_click", -1),
             (assign, "$g_tutorial_training_ground_conversation_state", 8), #trainer knocked down in chamber
             (play_sound, "snd_tutorial_fail"),
             (start_mission_conversation, "$g_tutorial_training_ground_melee_trainer_chamber"),
             (assign, "$g_tutorial_training_ground_melee_trainer_chamber", -1),
             (try_begin),
               (eq, "$g_tutorial_training_ground_melee_trainer_action_state", 1), #still in attack ready action
               (agent_set_attack_action, ":agent_no", 0, 0), #release
             (try_end),
           (try_end),
         (else_try),
           (ge, "$g_tutorial_training_ground_melee_trainer_combat", 0),
           (try_begin),
             (eq, ":agent_troop", "trp_player"),
             (eq, ":enemy_agent_troop", "$g_tutorial_training_ground_melee_trainer_combat"),
             (assign, "$g_tutorial_training_ground_melee_state", 0),
             (agent_set_team, ":agent_no", 0),
             (agent_set_team, ":enemy_agent_no", 7),
             (tutorial_message, -1),
             (assign, "$g_tutorial_training_ground_conversation_state", 4), #player knocked down in combat
             (play_sound, "snd_tutorial_fail"),
             (start_mission_conversation, "$g_tutorial_training_ground_melee_trainer_combat"),
             (assign, "$g_tutorial_training_ground_melee_trainer_combat", -1),
           (else_try),
             (eq, ":enemy_agent_troop", "trp_player"),
             (eq, ":agent_troop", "$g_tutorial_training_ground_melee_trainer_combat"),
             (assign, "$g_tutorial_training_ground_melee_state", 0),
             (agent_set_team, ":agent_no", 7),
             (agent_set_team, ":enemy_agent_no", 0),
##             (assign, "$g_tutorial_training_ground_melee_trainer_combat_completed", 1), #not used
             (tutorial_message, -1),
             (assign, "$g_tutorial_training_ground_conversation_state", 5), #trainer knocked down in combat
             (play_sound, "snd_tutorial_2"),
             (start_mission_conversation, "$g_tutorial_training_ground_melee_trainer_combat"),
             (assign, "$g_tutorial_training_ground_melee_trainer_combat", -1),
           (try_end),
         (else_try),
           (agent_is_human, ":agent_no"),
           (assign, "$g_tutorial_training_ground_melee_last_winner", ":enemy_agent_no"),
           (assign, "$g_tutorial_training_ground_melee_last_loser", ":agent_no"),
           (assign, "$g_tutorial_training_ground_melee_state", 0),
           (agent_set_team, "$g_tutorial_training_ground_melee_cur_fighter_1", 7),
           (agent_set_team, "$g_tutorial_training_ground_melee_cur_fighter_2", 7),
           (agent_force_rethink, "$g_tutorial_training_ground_melee_cur_fighter_1"),
           (agent_force_rethink, "$g_tutorial_training_ground_melee_cur_fighter_2"),
         (try_end),
         (agent_set_hit_points, ":agent_no", 100, 0),
         (agent_set_hit_points, ":enemy_agent_no", 100, 0),
         ]),

      (ti_before_mission_start, 0, 0, [],
       [
         (scene_set_day_time, 13),
         (team_set_relation, 0, 1, 0),
         (team_set_relation, 0, 2, 0),
         (team_set_relation, 0, 3, 0),
         (team_set_relation, 0, 7, 0),
         (team_set_relation, 7, 1, 1),
         (team_set_relation, 7, 2, 1),
         (team_set_relation, 7, 3, 1),
         (team_set_relation, 1, 2, -1),
         (team_set_relation, 1, 3, 1),
         (team_set_relation, 2, 3, 1),
         (assign, "$g_position_to_use_for_replacing_scene_items", pos8),
         (call_script, "script_replace_scene_items_with_spawn_items_before_ms"),
         (assign, "$g_tutorial_training_ground_state", 0),
         (assign, "$g_tutorial_training_ground_conversation_state", 0),
         (assign, "$g_tutorial_training_ground_melee_paused", 0),
         (assign, "$g_tutorial_training_ground_melee_state", 0),
         (assign, "$g_tutorial_training_ground_melee_next_action_time", 0),
         (assign, "$g_tutorial_training_ground_melee_last_winner", -1),
         (assign, "$g_tutorial_training_ground_melee_last_loser", -1),
         (assign, "$g_tutorial_training_ground_melee_cur_fighter_1", -1),
         (assign, "$g_tutorial_training_ground_melee_cur_fighter_2", -1),
         (assign, "$g_tutorial_training_ground_melee_trainer_attack", -1),
         (assign, "$g_tutorial_training_ground_melee_trainer_parry", -1),
         (assign, "$g_tutorial_training_ground_melee_trainer_combat", -1),
         (assign, "$g_tutorial_training_ground_melee_trainer_chamber", -1),
##         (assign, "$g_tutorial_training_ground_melee_trainer_attack_completed", 0), #not used
##         (assign, "$g_tutorial_training_ground_melee_trainer_parry_completed", 0), #not used
##         (assign, "$g_tutorial_training_ground_melee_trainer_combat_completed", 0), #not used
##         (assign, "$g_tutorial_training_ground_melee_trainer_chamber_completed", 0), #not used
         (assign, "$g_tutorial_training_ground_melee_trainer_next_action_time", 0),
         (assign, "$g_tutorial_training_ground_archer_trainer_state", 0),
         (assign, "$g_tutorial_training_ground_archer_trainer_completed_chapters", 0),
         (assign, "$g_tutorial_training_ground_horseman_trainer_state", 0),
         (assign, "$g_tutorial_training_ground_horseman_trainer_completed_chapters", 0),
         (assign, "$g_tutorial_training_ground_next_score_time", 0),
         (assign, "$g_tutorial_mouse_dir", -1),
         (assign, "$g_tutorial_mouse_click", -1),
         (assign, "$g_pointer_arrow_height_adder", -1000),
         ]),

      (0, 0, ti_once, [],
       [
         (tutorial_message_set_size, 17, 17),
         (tutorial_message_set_position, 500, 650),
         (tutorial_message_set_center_justify, 0),
         (mission_enable_talk),
         (call_script, "script_replace_scene_items_with_spawn_items_after_ms"),
         (entry_point_get_position, pos1, 59),
         (set_spawn_position, pos1),
         (spawn_horse, "itm_practice_horse", 0),
         (assign, "$g_tutorial_training_ground_intro_message_being_displayed", 1),
         (scene_spawned_item_get_instance, ":item_instance", "itm_practice_bow", 0),
         (prop_instance_get_position, pos0, ":item_instance"),
         (position_move_z, pos0, -1000, 1),
         (prop_instance_set_position, ":item_instance", pos0),
         (scene_spawned_item_get_instance, ":item_instance", "itm_practice_bow_2", 0),
         (prop_instance_get_position, pos0, ":item_instance"),
         (position_move_z, pos0, -1000, 1),
         (prop_instance_set_position, ":item_instance", pos0),
         (scene_spawned_item_get_instance, ":item_instance", "itm_practice_arrows", 0),
         (prop_instance_get_position, pos0, ":item_instance"),
         (position_move_z, pos0, -1000, 1),
         (prop_instance_set_position, ":item_instance", pos0),
         (scene_spawned_item_get_instance, ":item_instance", "itm_practice_arrows_2", 0),
         (prop_instance_get_position, pos0, ":item_instance"),
         (position_move_z, pos0, -1000, 1),
         (prop_instance_set_position, ":item_instance", pos0),
         (scene_spawned_item_get_instance, ":item_instance", "itm_practice_crossbow", 0),
         (prop_instance_get_position, pos0, ":item_instance"),
         (position_move_z, pos0, -1000, 1),
         (prop_instance_set_position, ":item_instance", pos0),
         (scene_spawned_item_get_instance, ":item_instance", "itm_practice_bolts", 0),
         (prop_instance_get_position, pos0, ":item_instance"),
         (position_move_z, pos0, -1000, 1),
         (prop_instance_set_position, ":item_instance", pos0),
         (scene_spawned_item_get_instance, ":item_instance", "itm_practice_javelin", 0),
         (prop_instance_get_position, pos0, ":item_instance"),
         (position_move_z, pos0, -1000, 1),
         (prop_instance_set_position, ":item_instance", pos0),
         (scene_spawned_item_get_instance, ":item_instance", "itm_arena_lance", 0),
         (prop_instance_get_position, pos0, ":item_instance"),
         (position_move_z, pos0, -1000, 1),
         (prop_instance_set_position, ":item_instance", pos0),
         ]),

      (0, 1, ti_once, [],
       [
         (tutorial_message_set_background, 1),
         (tutorial_message, "str_tutorial_training_ground_intro_message"),
         ]),

      (0, 0, 0,
       [
         (store_mission_timer_a, ":cur_time"),
         (try_for_agents, ":cur_agent"),
           (agent_get_troop_id, ":cur_agent_troop", ":cur_agent"),
           (eq, ":cur_agent_troop", "trp_tutorial_archer_1"),
           (try_begin),
             (agent_get_wielded_item, ":cur_wielded_item", ":cur_agent", 0),
             (neq, ":cur_wielded_item", "itm_practice_bow"),
             (agent_set_wielded_item, ":cur_agent", "itm_practice_bow"),
           (else_try),
             (agent_get_slot, ":look_spr", ":cur_agent", slot_agent_target_prop_instance),
             (prop_instance_get_position, pos1, ":look_spr"),
             (position_move_z, pos1, 10),
             (agent_set_look_target_position, ":cur_agent", pos1),
             (try_begin),
               (neg|agent_slot_ge, ":cur_agent", slot_agent_next_action_time, ":cur_time"),
               (agent_set_attack_action, ":cur_agent", 0),
               (store_random_in_range, ":next_action_time", 3, 13),
               (val_add, ":next_action_time", ":cur_time"),
               (agent_set_slot, ":cur_agent", slot_agent_next_action_time, ":next_action_time"),
             (try_end),
           (try_end),
         (try_end),
         ], []),

      (0, 0, 0,
       [
         (set_fixed_point_multiplier, 100),
         (try_for_agents, ":cur_agent"),
           (agent_get_troop_id, ":cur_agent_troop", ":cur_agent"),
           (this_or_next|eq, ":cur_agent_troop", "trp_tutorial_rider_1"),
           (eq, ":cur_agent_troop", "trp_tutorial_rider_2"),
           (agent_get_slot, ":target_entry_point", ":cur_agent", slot_agent_target_entry_point),
           (entry_point_get_position, pos1, ":target_entry_point"),
           (agent_get_position, pos2, ":cur_agent"),
           (get_sq_distance_between_positions, ":cur_dist", pos1, pos2),
           (try_begin),
             (lt, ":cur_dist", 6400),
             (val_add, ":target_entry_point", 1),
             (try_begin),
               (gt, ":target_entry_point", 57), #last entry point
               (assign, ":target_entry_point", 48), #first entry point
             (try_end),
             (agent_set_slot, ":cur_agent", slot_agent_target_entry_point, ":target_entry_point"),
             (entry_point_get_position, pos1, ":target_entry_point"),
             (agent_set_scripted_destination, ":cur_agent", pos1),
           (try_end),
           (try_begin),
             (eq, ":cur_agent_troop", "trp_tutorial_rider_2"),
             (try_begin),
               (agent_get_wielded_item, ":cur_wielded_item", ":cur_agent", 0),
               (neq, ":cur_wielded_item", "itm_practice_bow"),
               (agent_set_wielded_item, ":cur_agent", "itm_practice_bow"),
             (else_try),
               (scene_prop_get_num_instances, ":num_instances", "spr_archery_target_with_hit_a"),
               (assign, ":shortest_dist", 10000000),
               (assign, ":best_instance", -1),
               (try_for_range, ":cur_instance", 0, ":num_instances"),
                 (scene_prop_get_instance, ":spr_instance", "spr_archery_target_with_hit_a", ":cur_instance"),
                 (neg|agent_slot_eq, ":cur_agent", slot_agent_target_prop_instance, ":spr_instance"),
                 (prop_instance_get_position, pos1, ":spr_instance"),
                 (position_is_behind_position, pos2, pos1), #target is facing towards us
                 (get_sq_distance_between_positions, ":cur_dist", pos1, pos2),
                 (lt, ":cur_dist", ":shortest_dist"),
                 (assign, ":shortest_dist", ":cur_dist"),
                 (assign, ":best_instance", ":spr_instance"),
               (try_end),
               (try_begin),
                 (lt, ":shortest_dist", 40000), #20 meters
                 (prop_instance_get_position, pos1, ":best_instance"),
                 (position_move_z, pos1, 10),
                 (init_position, pos3),
                 (position_set_x, pos3, -160), #1.6 meters
                 (position_transform_position_to_parent, pos4, pos1, pos3),
                 (copy_position, pos1, pos4),
                 (agent_set_look_target_position, ":cur_agent", pos1),
                 (lt, ":shortest_dist", 22500), #15 meters
                 (agent_set_slot, ":cur_agent", slot_agent_target_prop_instance, ":best_instance"),
                 (agent_set_attack_action, ":cur_agent", 0),
               (else_try),
                 (agent_get_slot, ":last_instance", ":cur_agent", slot_agent_target_prop_instance),
                 (ge, ":last_instance", 0),
                 (prop_instance_get_position, pos1, ":last_instance"),
                 (get_sq_distance_between_positions, ":cur_dist", pos1, pos2),
                 (lt, ":cur_dist", 40000), #20 meters
                 (position_move_z, pos1, 10),
                 (init_position, pos3),
                 (position_set_x, pos3, -160), #1.6 meters
                 (position_transform_position_to_parent, pos4, pos1, pos3),
                 (copy_position, pos1, pos4),
                 (agent_set_look_target_position, ":cur_agent", pos1),
               (try_end),
             (try_end),
           (else_try),
             (eq, ":cur_agent_troop", "trp_tutorial_rider_1"),
             (try_begin),
               (agent_get_wielded_item, ":cur_wielded_item", ":cur_agent", 0),
               (neq, ":cur_wielded_item", "itm_practice_sword"),
               (agent_set_wielded_item, ":cur_agent", "itm_practice_sword"),
             (else_try),
               (scene_prop_get_num_instances, ":num_instances", "spr_dummy_a_undestructable"),
               (assign, ":shortest_dist", 10000000),
               (assign, ":best_instance", -1),
               (try_for_range, ":cur_instance", 0, ":num_instances"),
                 (scene_prop_get_instance, ":spr_instance", "spr_dummy_a_undestructable", ":cur_instance"),
                 (neg|agent_slot_eq, ":cur_agent", slot_agent_target_prop_instance, ":spr_instance"),
                 (prop_instance_get_position, pos1, ":spr_instance"),
                 (get_sq_distance_between_positions, ":cur_dist", pos1, pos2),
                 (lt, ":cur_dist", ":shortest_dist"),
                 (assign, ":shortest_dist", ":cur_dist"),
                 (assign, ":best_instance", ":spr_instance"),
               (try_end),
               (try_begin),
                 (lt, ":shortest_dist", 10000), #10 meters
                 (prop_instance_get_position, pos1, ":best_instance"),
                 (position_transform_position_to_local, pos3, pos2, pos1),
                 (position_get_x, ":local_x", pos3),
                 (position_get_y, ":local_y", pos3),
                 (is_between, ":local_x", -200, 200),
                 (gt, ":local_y", -100),
                 (init_position, pos3),
                 (try_begin),
                   (lt, ":local_x", 0),
                   (position_move_x, pos3, -100),
                   (position_move_z, pos3, 100),
                 (else_try),
                   (position_move_x, pos3, 100),
                   (position_move_z, pos3, 150),
                 (try_end),
                 (position_transform_position_to_parent, pos4, pos2, pos3),
                 (agent_set_look_target_position, ":cur_agent", pos4),
                 (try_begin),
                   (lt, ":local_x", 0),
                   (agent_set_attack_action, ":cur_agent", 2, 1), #left
                 (else_try),
                   (agent_set_attack_action, ":cur_agent", 1, 1), #right
                 (try_end),
                 (this_or_next|lt, ":shortest_dist", 900), #3 meters
                 (lt, ":local_y", 100), #1 meter
                 (agent_set_attack_action, ":cur_agent", 0, 0), #release
                 (agent_set_slot, ":cur_agent", slot_agent_target_prop_instance, ":best_instance"),
               (else_try),
                 (agent_get_slot, ":last_instance", ":cur_agent", slot_agent_target_prop_instance),
                 (ge, ":last_instance", 0),
                 (prop_instance_get_position, pos1, ":last_instance"),
                 (get_sq_distance_between_positions, ":cur_dist", pos1, pos2),
                 (lt, ":cur_dist", 10000), #10 meters
                 (position_transform_position_to_local, pos3, pos2, pos1),
                 (position_get_x, ":local_x", pos3),
                 (position_get_y, ":local_y", pos3),
                 (is_between, ":local_x", -200, 200),
                 (gt, ":local_y", -100),
                 (init_position, pos3),
                 (try_begin),
                   (lt, ":local_x", 0),
                   (position_move_x, pos3, -100),
                   (position_move_z, pos3, 100),
                 (else_try),
                   (position_move_x, pos3, 100),
                   (position_move_z, pos3, 150),
                 (try_end),
                 (position_transform_position_to_parent, pos4, pos2, pos3),
                 (agent_set_look_target_position, ":cur_agent", pos4),
               (try_end),
             (try_end),
           (try_end),
         (try_end),
         ], []),
      
      (0, 0, 0,
       [
         (store_mission_timer_a, ":cur_time"),
         (try_for_agents, ":cur_agent"),
           (agent_get_troop_id, ":cur_agent_troop", ":cur_agent"),
           (eq, ":cur_agent_troop", "trp_tutorial_archer_1"),
           (try_begin),
             (agent_get_wielded_item, ":cur_wielded_item", ":cur_agent", 0),
             (neq, ":cur_wielded_item", "itm_practice_bow"),
             (agent_set_wielded_item, ":cur_agent", "itm_practice_bow"),
           (else_try),
             (agent_get_slot, ":look_spr", ":cur_agent", slot_agent_target_prop_instance),
             (prop_instance_get_position, pos1, ":look_spr"),
             (agent_set_look_target_position, ":cur_agent", pos1),
             (try_begin),
               (neg|agent_slot_ge, ":cur_agent", slot_agent_next_action_time, ":cur_time"),
               (agent_set_attack_action, ":cur_agent", 0),
               (store_random_in_range, ":next_action_time", 3, 13),
               (val_add, ":next_action_time", ":cur_time"),
               (agent_set_slot, ":cur_agent", slot_agent_next_action_time, ":next_action_time"),
             (try_end),
           (try_end),
         (try_end),
         ], []),

      (0, 0, 0,
       [
         (call_script, "script_iterate_pointer_arrow"),
         ], []),


      (5, 0, 0,
       [
         (try_begin),
           (store_mission_timer_a, ":cur_time"),
           (ge, ":cur_time", 30),
           (eq, "$g_tutorial_training_ground_intro_message_being_displayed", 1),
           (assign, "$g_tutorial_training_ground_intro_message_being_displayed", 0),
           (tutorial_message, -1),
         (try_end),
         (get_player_agent_no, ":player_agent"),
         (try_for_agents, ":cur_agent"),
           (agent_is_human, ":cur_agent"),
           (neq, ":cur_agent", ":player_agent"),
           (agent_refill_ammo, ":cur_agent"),
         (try_end),
         ], []),

      (0, 0, 0,
       [
         (get_player_agent_no, ":player_agent"),
         (agent_get_wielded_item, ":wielded_weapon", ":player_agent", 0),
         (assign, ":refill", 0),
         (try_begin),
           (eq, ":wielded_weapon", "itm_practice_bow"),
           (agent_has_item_equipped, ":player_agent", "itm_practice_arrows"),
           (agent_get_ammo, ":cur_ammo", ":player_agent", 1),
           (eq, ":cur_ammo", 0),
           (assign, ":refill", 1),
         (else_try),
           (eq, ":wielded_weapon", "itm_practice_bow_2"),
           (agent_has_item_equipped, ":player_agent", "itm_practice_arrows_2"),
           (agent_get_ammo, ":cur_ammo", ":player_agent", 1),
           (eq, ":cur_ammo", 0),
           (assign, ":refill", 1),
         (else_try),
           (eq, ":wielded_weapon", "itm_practice_crossbow"),
           (agent_has_item_equipped, ":player_agent", "itm_practice_bolts"),
           (agent_get_ammo, ":cur_ammo", ":player_agent", 1),
           (eq, ":cur_ammo", 0),
           (assign, ":refill", 1),
         (else_try),
           (eq, ":wielded_weapon", "itm_practice_javelin"),
           (agent_get_ammo, ":cur_ammo", ":player_agent", 1),
           (le, ":cur_ammo", 1),
           (assign, ":refill", 1),
         (try_end),
         (eq, ":refill", 1),
         (agent_refill_ammo, ":player_agent"),
         (tutorial_box, "str_tutorial_training_ground_ammo_refill", "@Tutorial"),
         ], []),

      (0, 0, 0,
       [
         (get_player_agent_no, ":player_agent"),
         (neq, "$g_tutorial_training_ground_horseman_trainer_state", 0),
         (mission_disable_talk),
         (try_begin),
           (eq, "$g_tutorial_training_ground_horseman_trainer_state", 1),
           (assign, "$g_tutorial_training_ground_current_score", 0),
           (val_add, "$g_tutorial_training_ground_horseman_trainer_state", 1),
         (else_try),
           (eq, "$g_tutorial_training_ground_horseman_trainer_state", 2),
           (try_begin),
             (try_begin),
               (ge, "$g_tutorial_training_ground_horseman_trainer_item_1", 0),
               (scene_spawned_item_get_instance, ":item_instance", "$g_tutorial_training_ground_horseman_trainer_item_1", 0),
               (prop_instance_get_position, pos0, ":item_instance"),
               (position_move_z, pos0, 1000, 1),
               (prop_instance_set_position, ":item_instance", pos0),

               (scene_prop_get_instance, ":pointer_instance", "spr_pointer_arrow", 0),
               (prop_instance_set_position, ":pointer_instance", pos0),
               (assign, "$g_pointer_arrow_height_adder", 200),

               (try_begin),
                 (ge, "$g_tutorial_training_ground_horseman_trainer_item_2", 0),
                 (scene_spawned_item_get_instance, ":item_instance", "$g_tutorial_training_ground_horseman_trainer_item_2", 0),
                 (prop_instance_get_position, pos0, ":item_instance"),
                 (position_move_z, pos0, 1000, 1),
                 (prop_instance_set_position, ":item_instance", pos0),
               (try_end),
             (try_end),
             (val_add, "$g_tutorial_training_ground_horseman_trainer_state", 1),
           (try_end),
         (else_try),
           (eq, "$g_tutorial_training_ground_horseman_trainer_state", 3),
           (try_begin),
             (ge, "$g_tutorial_training_ground_horseman_trainer_item_1", 0),
             (try_begin),
               (str_store_item_name, s0, "$g_tutorial_training_ground_horseman_trainer_item_1"),
               (tutorial_message, "str_tutorial_training_ground_horseman_text_1"),
               (agent_has_item_equipped, ":player_agent", "$g_tutorial_training_ground_horseman_trainer_item_1"),
               (val_add, "$g_tutorial_training_ground_horseman_trainer_state", 1),
               (play_sound, "snd_tutorial_1"),
             (try_end),
           (else_try),
             (val_add, "$g_tutorial_training_ground_horseman_trainer_state", 1),
           (try_end),
         (else_try),
           (eq, "$g_tutorial_training_ground_horseman_trainer_state", 4),
           (try_begin),
             (ge, "$g_tutorial_training_ground_horseman_trainer_item_2", 0),
             (try_begin),
               (str_store_item_name, s0, "$g_tutorial_training_ground_horseman_trainer_item_2"),
               (tutorial_message, "str_tutorial_training_ground_horseman_text_1"),
               (agent_has_item_equipped, ":player_agent", "$g_tutorial_training_ground_horseman_trainer_item_2"),
               (val_add, "$g_tutorial_training_ground_horseman_trainer_state", 1),
               (play_sound, "snd_tutorial_1"),
             (try_end),
           (else_try),
             (val_add, "$g_tutorial_training_ground_horseman_trainer_state", 1),
           (try_end),
         (else_try),
           (eq, "$g_tutorial_training_ground_horseman_trainer_state", 5),
           (try_begin),
             (agent_get_horse, ":player_horse", ":player_agent"),
             (lt, ":player_horse", 0),
             (tutorial_message, "str_tutorial_training_ground_horseman_text_2"),
             (try_begin),
               (assign, ":horse_agent_to_mount", -1),
               (try_for_agents, ":cur_agent"),
                 (agent_get_item_id, ":cur_agent_item", ":cur_agent"),
                 (eq, ":cur_agent_item", "itm_practice_horse"),
                 (assign, ":horse_agent_to_mount", ":cur_agent"),
               (try_end),
               (agent_get_position, pos0, ":horse_agent_to_mount"),
               (scene_prop_get_instance, ":pointer_instance", "spr_pointer_arrow", 0),
               (prop_instance_get_position, pos1, ":pointer_instance"),
               (set_fixed_point_multiplier, 100),
               (position_get_x, ":x1", pos0),
               (position_get_x, ":x2", pos1),
               (position_get_y, ":y1", pos0),
               (position_get_y, ":y2", pos1),
               (this_or_next|neq, ":x1", ":x2"),
               (neq, ":y1", ":y2"),
               (prop_instance_set_position, ":pointer_instance", pos0),
               (assign, "$g_pointer_arrow_height_adder", 200),
             (try_end),
           (else_try),
             (val_add, "$g_tutorial_training_ground_horseman_trainer_state", 1),
           (try_end),
         (else_try),
           (eq, "$g_tutorial_training_ground_horseman_trainer_state", 6),
           (try_begin),
             (eq, "$g_tutorial_training_ground_horseman_trainer_completed_chapters", 0),
             (tutorial_message, "str_tutorial_training_ground_horseman_text_3"),
           (else_try),
             (eq, "$g_tutorial_training_ground_horseman_trainer_completed_chapters", 1),
             (assign, ":prop_to_search_for", "spr_dummy_a_undestructable"),
             (tutorial_message, "str_tutorial_training_ground_horseman_text_4"),
           (else_try),
             (assign, ":prop_to_search_for", "spr_archery_target_with_hit_a"),
             (tutorial_message, "str_tutorial_training_ground_horseman_text_5"),
           (try_end),
           (try_begin),
             (eq, "$g_tutorial_training_ground_horseman_trainer_completed_chapters", 0),
             (store_add, ":cur_entry_point", "$g_tutorial_training_ground_current_score", 48),
             (entry_point_get_position, pos0, ":cur_entry_point"),
             (init_position, pos2),
             (position_move_y, pos2, -800),
             (position_transform_position_to_parent, pos3, pos0, pos2),
             (copy_position, pos0, pos3),
             (agent_get_position, pos2, ":player_agent"),
             (try_begin),
               (get_distance_between_positions, ":cur_dist", pos0, pos2),
               (lt, ":cur_dist", 500), #5 meters
               (val_add, "$g_tutorial_training_ground_current_score", 1),
               (ge, "$g_tutorial_training_ground_current_score", 10),
               (assign, "$g_pointer_arrow_height_adder", -1000),
               (tutorial_message, "str_tutorial_training_ground_horseman_text_6", 0, 10),
               (assign, "$g_tutorial_training_ground_horseman_trainer_state", 0),
               (val_add, "$g_tutorial_training_ground_horseman_trainer_completed_chapters", 1),
               (play_sound, "snd_tutorial_2"),
             (try_end),
             (try_begin),
               (scene_prop_get_instance, ":pointer_instance", "spr_pointer_arrow", 0),
               (prop_instance_get_position, pos1, ":pointer_instance"),
               (set_fixed_point_multiplier, 1),
               (position_get_x, ":x1", pos0),
               (position_get_x, ":x2", pos1),
               (position_get_y, ":y1", pos0),
               (position_get_y, ":y2", pos1),
               (this_or_next|neq, ":x1", ":x2"),
               (neq, ":y1", ":y2"),
               (prop_instance_set_position, ":pointer_instance", pos0),
               (assign, "$g_pointer_arrow_height_adder", 150),
               (play_sound, "snd_tutorial_1"),
             (try_end),
           (else_try),
             (scene_prop_get_num_instances, ":end_cond", ":prop_to_search_for"),
             (try_begin),
               (lt, "$g_tutorial_training_ground_current_score", 6),
               (assign, ":next_prop_instance", -1),
               (store_add, ":var_id_to_search_for", "$g_tutorial_training_ground_current_score", 1),
               (try_for_range, ":cur_instance", 0, ":end_cond"),
                 (scene_prop_get_instance, ":prop_instance", ":prop_to_search_for", ":cur_instance"),
                 (prop_instance_get_variation_id_2, ":var_id_2", ":prop_instance"),
                 (eq, ":var_id_to_search_for", ":var_id_2"),
                 (assign, ":next_prop_instance", ":prop_instance"),
                 (assign, ":end_cond", 0),
               (try_end),
               (try_begin),
                 (prop_instance_get_position, pos0, ":next_prop_instance"),
                 (scene_prop_get_instance, ":pointer_instance", "spr_pointer_arrow", 0),
                 (prop_instance_get_position, pos1, ":pointer_instance"),
                 (set_fixed_point_multiplier, 1),
                 (position_get_x, ":x1", pos0),
                 (position_get_x, ":x2", pos1),
                 (position_get_y, ":y1", pos0),
                 (position_get_y, ":y2", pos1),
                 (this_or_next|neq, ":x1", ":x2"),
                 (neq, ":y1", ":y2"),
                 (prop_instance_set_position, ":pointer_instance", pos0),
                 (assign, "$g_pointer_arrow_height_adder", 200),
                 (play_sound, "snd_tutorial_1"),
               (try_end),
             (else_try),
               (assign, "$g_pointer_arrow_height_adder", -1000),
               (try_begin),
                 (ge, "$g_tutorial_training_ground_horseman_trainer_item_2", 0),
                 (agent_unequip_item, ":player_agent", "$g_tutorial_training_ground_horseman_trainer_item_2"),
               (try_end),
               (agent_unequip_item, ":player_agent", "$g_tutorial_training_ground_horseman_trainer_item_1"),
               (tutorial_message, "str_tutorial_training_ground_horseman_text_6", 0, 10),
               (assign, "$g_tutorial_training_ground_horseman_trainer_state", 0),
               (val_add, "$g_tutorial_training_ground_horseman_trainer_completed_chapters", 1),
               (play_sound, "snd_tutorial_2"),
             (try_end),
           (try_end),
         (try_end),
         ], []),
      
      (0, 0, 0,
       [
         (get_player_agent_no, ":player_agent"),
         (neq, "$g_tutorial_training_ground_archer_trainer_state", 0),
         (mission_disable_talk),
         (try_begin),
           (eq, "$g_tutorial_training_ground_archer_trainer_state", 1),
           (try_begin),
             (assign, "$g_last_destroyed_gourds", 0),
             (assign, "$g_tutorial_training_ground_current_score", 0),
             (scene_spawned_item_get_instance, ":item_instance", "$g_tutorial_training_ground_archer_trainer_item_1", 0),
             (prop_instance_get_position, pos0, ":item_instance"),
             (position_move_z, pos0, 1000, 1),
             (prop_instance_set_position, ":item_instance", pos0),

             (scene_prop_get_instance, ":pointer_instance", "spr_pointer_arrow", 0),
             (prop_instance_set_position, ":pointer_instance", pos0),
             (assign, "$g_pointer_arrow_height_adder", 100),

             (try_begin),
               (ge, "$g_tutorial_training_ground_archer_trainer_item_2", 0),
               (scene_spawned_item_get_instance, ":item_instance", "$g_tutorial_training_ground_archer_trainer_item_2", 0),
               (prop_instance_get_position, pos0, ":item_instance"),
               (position_move_z, pos0, 1000, 1),
               (prop_instance_set_position, ":item_instance", pos0),
             (try_end),
             (val_add, "$g_tutorial_training_ground_archer_trainer_state", 1),
           (try_end),
         (else_try),
           (eq, "$g_tutorial_training_ground_archer_trainer_state", 2),
           (try_begin),
             (str_store_item_name, s0, "$g_tutorial_training_ground_archer_trainer_item_1"),
             (tutorial_message, "str_tutorial_training_ground_archer_text_1"),
             (agent_has_item_equipped, ":player_agent", "$g_tutorial_training_ground_archer_trainer_item_1"),
             (val_add, "$g_tutorial_training_ground_archer_trainer_state", 1),
             (play_sound, "snd_tutorial_1"),
           (try_end),
         (else_try),
           (eq, "$g_tutorial_training_ground_archer_trainer_state", 3),
           (try_begin),
             (ge, "$g_tutorial_training_ground_archer_trainer_item_2", 0),
             (try_begin),
               (str_store_item_name, s0, "$g_tutorial_training_ground_archer_trainer_item_2"),
               (tutorial_message, "str_tutorial_training_ground_archer_text_1"),
               (agent_has_item_equipped, ":player_agent", "$g_tutorial_training_ground_archer_trainer_item_2"),
               (val_add, "$g_tutorial_training_ground_archer_trainer_state", 1),
               (play_sound, "snd_tutorial_1"),
             (try_end),
           (else_try),
             (val_add, "$g_tutorial_training_ground_archer_trainer_state", 1),
           (try_end),
         (else_try),
           (eq, "$g_tutorial_training_ground_archer_trainer_state", 4),
           (try_begin),
             (try_for_range, ":cur_instance", 0, 3),
               (scene_prop_get_instance, ":gourd_instance", "spr_gourd", ":cur_instance"),
               (prop_instance_refill_hit_points, ":gourd_instance"),
               (entry_point_get_position, pos0, 45),
               (init_position, pos1),
               (store_sub, ":cur_rotation", ":cur_instance", 1),
               (val_mul, ":cur_rotation", 5),
               (position_rotate_z, pos1, ":cur_rotation"),
               (try_begin),
                 (ge, "$g_tutorial_training_ground_archer_trainer_item_2", 0),
                 (position_move_y, pos1, 1300), #for bow and crossbow
               (else_try),
                 (position_move_y, pos1, 800), #for javelin
                 (val_mul, ":cur_rotation", 2),
               (try_end),
               (position_transform_position_to_parent, pos2, pos0, pos1),
               (position_set_z_to_ground_level, pos2),
               (scene_prop_get_instance, ":spike_instance", "spr_gourd_spike", ":cur_instance"),
               (prop_instance_set_position, ":spike_instance", pos2),
               (position_move_z, pos2, 150, 1),
               (prop_instance_set_position, ":gourd_instance", pos2),
             (try_end),
             (scene_prop_get_instance, ":pointer_instance", "spr_pointer_arrow", 0),
             (scene_prop_get_instance, ":spike_instance", "spr_gourd_spike", 1),
             (prop_instance_get_position, pos1, ":spike_instance"),
             (prop_instance_set_position, ":pointer_instance", pos1),
             (assign, "$g_pointer_arrow_height_adder", 200),
             (tutorial_message, "str_tutorial_training_ground_archer_text_2"),
             (val_add, "$g_tutorial_training_ground_archer_trainer_state", 1),
           (try_end),
         (else_try),
           (eq, "$g_tutorial_training_ground_archer_trainer_state", 5),
           (try_begin),
             (try_begin),
               (neq, "$g_tutorial_training_ground_current_score", "$g_last_destroyed_gourds"),
               (assign, "$g_tutorial_training_ground_current_score", "$g_last_destroyed_gourds"),
               (try_begin),
                 (lt, "$g_last_destroyed_gourds", 3),
                 (play_sound, "snd_tutorial_1"),
               (else_try),
                 (play_sound, "snd_tutorial_2"),
               (try_end),
             (try_end),
             (try_begin),
               (eq, "$g_tutorial_training_ground_archer_trainer_completed_chapters", 0),
               (eq, "$g_last_destroyed_gourds", 0),
               (entry_point_get_position, pos0, 45),
               (agent_get_position, pos1, ":player_agent"),
               (neg|position_is_behind_position, pos1, pos0),
               (tutorial_message, "str_tutorial_training_ground_archer_text_3"),
             (else_try),
               (eq, "$g_tutorial_training_ground_archer_trainer_completed_chapters", 0),
               (eq, "$g_last_destroyed_gourds", 1),
               (tutorial_message, "str_tutorial_training_ground_archer_text_4"),
             (try_end),
             (ge, "$g_last_destroyed_gourds", 3),
             (assign, "$g_pointer_arrow_height_adder", -1000),
             (val_add, "$g_tutorial_training_ground_archer_trainer_state", 1),
           (try_end),
         (else_try),
           (eq, "$g_tutorial_training_ground_archer_trainer_state", 6),
           (try_begin),
             (try_begin),
               (ge, "$g_tutorial_training_ground_archer_trainer_item_2", 0),
               (agent_unequip_item, ":player_agent", "$g_tutorial_training_ground_archer_trainer_item_2"),
             (try_end),
             (agent_unequip_item, ":player_agent", "$g_tutorial_training_ground_archer_trainer_item_1"),
             (tutorial_message, "str_tutorial_training_ground_archer_text_5", 0, 10),
             (assign, "$g_tutorial_training_ground_archer_trainer_state", 0),
             (val_add, "$g_tutorial_training_ground_archer_trainer_completed_chapters", 1),
           (try_end),
         (try_end),
         ], []),
      
      (0, 0, 0,
       [
         (get_player_agent_no, ":player_agent"),
         (neq, "$g_tutorial_training_ground_melee_trainer_attack", -1),
         (mission_disable_talk),
         (try_for_agents, ":cur_agent"),
           (agent_get_troop_id, ":cur_agent_troop", ":cur_agent"),
           (eq, ":cur_agent_troop", "$g_tutorial_training_ground_melee_trainer_attack"),
           (assign, ":trainer_agent", ":cur_agent"),
         (try_end),
         (try_begin),
           (eq, "$g_tutorial_training_ground_melee_state", 0),
           (try_begin),
             (try_for_agents, ":cur_agent"),
               (agent_get_troop_id, ":cur_agent_troop", ":cur_agent"),
               (this_or_next|eq, ":cur_agent_troop", "trp_tutorial_fighter_1"),
               (this_or_next|eq, ":cur_agent_troop", "trp_tutorial_fighter_2"),
               (this_or_next|eq, ":cur_agent_troop", "trp_tutorial_fighter_3"),
               (eq, ":cur_agent_troop", "trp_tutorial_fighter_4"),
               (agent_set_team, ":cur_agent", 7),
               (agent_get_slot, ":spawn_point", ":cur_agent", slot_agent_spawn_entry_point),
               (entry_point_get_position, pos1, ":spawn_point"),
               (agent_set_scripted_destination, ":cur_agent", pos1),
               (agent_force_rethink, ":cur_agent"),
             (try_end),
             (agent_set_wielded_item, ":trainer_agent", "itm_practice_sword"), #TODO: change this
             (store_random_in_range, "$g_tutorial_training_ground_melee_state", 1, 5), #random attack dir
             (assign, "$g_tutorial_update_mouse_presentation", 1),
             (assign, "$g_tutorial_training_ground_next_score_time", 0),
           (try_end),
         (else_try),
           (gt, "$g_tutorial_training_ground_melee_state", 0),
           (try_begin),
             (agent_set_team, ":player_agent", 1),
             (agent_set_team, ":trainer_agent", 2),
             (agent_get_position, pos1, ":player_agent"),
             (agent_set_scripted_destination_no_attack, ":trainer_agent", pos1),
             (agent_get_attack_action, ":attack_action", ":player_agent"),
             (try_begin),
               (eq, ":attack_action", 2), #release
               (agent_get_action_dir, ":action_dir_attacker", ":player_agent"),
               (try_begin),
                 (eq, ":action_dir_attacker", 0), #down
                 (agent_set_defend_action, ":trainer_agent", 0, 1),
               (else_try),
                 (eq, ":action_dir_attacker", 3), #up
                 (agent_set_defend_action, ":trainer_agent", 3, 1),
               (else_try),
                 (eq, ":action_dir_attacker", 1), #right
                 (agent_set_defend_action, ":trainer_agent", 2, 1),
               (else_try),
                 (eq, ":action_dir_attacker", 2), #left
                 (agent_set_defend_action, ":trainer_agent", 1, 1),
               (try_end),
             (try_end),
             (try_begin),
               (ge, "$g_tutorial_training_ground_current_score", 5),
               (tutorial_message, -1),
               (assign, "$g_tutorial_training_ground_melee_state", 0),
               (agent_set_team, ":player_agent", 0),
               (agent_set_team, ":trainer_agent", 7),
               (agent_set_hit_points, ":player_agent", 100, 0),
               (agent_set_hit_points, ":trainer_agent", 100, 0),
##               (assign, "$g_tutorial_training_ground_melee_trainer_attack_completed", 1), #not used
               (assign, "$g_tutorial_training_ground_conversation_state", 9), #attack complete
               (start_mission_conversation, "$g_tutorial_training_ground_melee_trainer_attack"),
               (assign, "$g_tutorial_training_ground_melee_trainer_attack", -1),
             (try_end),
           (try_end),
         (try_end),
         (try_begin),
           (agent_get_attack_action, ":attack_action", ":player_agent"),
           (eq, ":attack_action", 2), #release
           (agent_get_action_dir, ":action_dir_attacker", ":player_agent"),
           (store_add, ":attack_state", ":action_dir_attacker", 1),
           (agent_get_wielded_item, ":weapon_item", ":player_agent", 0),
           (call_script, "script_cf_is_melee_weapon_for_tutorial", ":weapon_item"),
           (store_mission_timer_a, ":cur_time"),
           (gt, ":cur_time", "$g_tutorial_training_ground_next_score_time"),
           (try_begin),
             (eq, ":attack_state", "$g_tutorial_training_ground_melee_state"),
             (val_add, "$g_tutorial_training_ground_current_score", 1),
             (try_begin),
               (ge, "$g_tutorial_training_ground_current_score", 5),
               (assign, "$g_tutorial_training_ground_melee_state", 5),
               (play_sound, "snd_tutorial_2"),
             (else_try),
               (play_sound, "snd_tutorial_1"),
               (assign, ":end_cond", 100),
               (try_for_range, ":unused", 0, ":end_cond"),
                 (store_random_in_range, ":random_no", 1, 5), #random attack dir
                 (neq, ":random_no", "$g_tutorial_training_ground_melee_state"),
                 (assign, "$g_tutorial_training_ground_melee_state", ":random_no"),
                 (assign, ":end_cond", 0), #break
               (try_end),
             (try_end),
             (assign, "$g_tutorial_update_mouse_presentation", 1),
           (else_try),
             (val_add, "$g_tutorial_training_ground_current_score_2", 1),
             (play_sound, "snd_tutorial_fail"),
           (try_end),
           (store_add, "$g_tutorial_training_ground_next_score_time", ":cur_time", 1),
         (try_end),
         (assign, reg0, "$g_tutorial_training_ground_current_score"),
         (assign, reg1, "$g_tutorial_training_ground_current_score_2"),
         (str_clear, s0),
         (assign, "$g_tutorial_mouse_dir", -1),
         (assign, "$g_tutorial_mouse_click", -1),
         (try_begin),
           (neq, "$g_tutorial_training_ground_melee_state", 5), #finished
           (store_mission_timer_a, ":cur_time"),
           (this_or_next|eq, "$g_tutorial_update_mouse_presentation", 0),
           (gt, ":cur_time", "$g_tutorial_training_ground_next_score_time"),
           (try_begin),
             (eq, "$g_tutorial_training_ground_melee_state", 1), #down
             (str_store_string, s0, "str_tutorial_training_ground_attack_training_down"),
           (else_try),
             (eq, "$g_tutorial_training_ground_melee_state", 4), #up
             (str_store_string, s0, "str_tutorial_training_ground_attack_training_up"),
           (else_try),
             (eq, "$g_tutorial_training_ground_melee_state", 2), #right
             (str_store_string, s0, "str_tutorial_training_ground_attack_training_right"),
           (else_try),
             (eq, "$g_tutorial_training_ground_melee_state", 3), #left
             (str_store_string, s0, "str_tutorial_training_ground_attack_training_left"),
           (try_end),
           (store_sub, "$g_tutorial_mouse_dir", "$g_tutorial_training_ground_melee_state", 1),
           (assign, "$g_tutorial_mouse_click", 0),
           (try_begin),
             (eq, "$g_tutorial_update_mouse_presentation", 1),
             (assign, "$g_tutorial_update_mouse_presentation", 0),
             (start_presentation, "prsnt_tutorial_show_mouse_movement"),
           (try_end),
         (try_end),
         (try_begin),
           (agent_get_wielded_item, ":weapon_item", ":player_agent", 0),
           (call_script, "script_cf_is_melee_weapon_for_tutorial", ":weapon_item"),
           (tutorial_message, "str_tutorial_training_ground_attack_training"),
         (else_try),
           (tutorial_message, "str_tutorial_training_ground_warning_melee"),
         (try_end),
         ], []),

      (0, 0, 0,
       [
         (get_player_agent_no, ":player_agent"),
         (neq, "$g_tutorial_training_ground_melee_trainer_parry", -1),
         (mission_disable_talk),
         (try_for_agents, ":cur_agent"),
           (agent_get_troop_id, ":cur_agent_troop", ":cur_agent"),
           (eq, ":cur_agent_troop", "$g_tutorial_training_ground_melee_trainer_parry"),
           (assign, ":trainer_agent", ":cur_agent"),
         (try_end),
         (try_begin),
           (eq, "$g_tutorial_training_ground_melee_state", 0),
           (try_begin),
             (try_for_agents, ":cur_agent"),
               (agent_get_troop_id, ":cur_agent_troop", ":cur_agent"),
               (this_or_next|eq, ":cur_agent_troop", "trp_tutorial_fighter_1"),
               (this_or_next|eq, ":cur_agent_troop", "trp_tutorial_fighter_2"),
               (this_or_next|eq, ":cur_agent_troop", "trp_tutorial_fighter_3"),
               (eq, ":cur_agent_troop", "trp_tutorial_fighter_4"),
               (agent_set_team, ":cur_agent", 7),
               (agent_get_slot, ":spawn_point", ":cur_agent", slot_agent_spawn_entry_point),
               (entry_point_get_position, pos1, ":spawn_point"),
               (agent_set_scripted_destination, ":cur_agent", pos1),
               (agent_force_rethink, ":cur_agent"),
             (try_end),
             (agent_set_wielded_item, ":trainer_agent", "itm_practice_sword"), #TODO: change this
             (val_add, "$g_tutorial_training_ground_melee_state", 1),
             (store_mission_timer_a, "$g_tutorial_training_ground_melee_next_action_time"),
             (val_add, "$g_tutorial_training_ground_melee_next_action_time", 1),
           (try_end),
         (else_try),
           (eq, "$g_tutorial_training_ground_melee_state", 1),
           (try_begin),
             (store_mission_timer_a, ":cur_time"),
             (gt, ":cur_time", "$g_tutorial_training_ground_melee_next_action_time"),
             (agent_set_team, ":player_agent", 1),
             (agent_set_team, ":trainer_agent", 2),
             (agent_get_position, pos1, ":player_agent"),
             (agent_set_scripted_destination_no_attack, ":trainer_agent", pos1),
             (agent_get_position, pos2, ":trainer_agent"),
             (get_sq_distance_between_positions, ":sq_dist", pos1, pos2),
             (lt, ":sq_dist", 400), #2 meters
             (try_begin),
               (eq, "$g_tutorial_training_ground_melee_trainer_action_state", 0),
               (try_begin),
                 (ge, "$g_tutorial_training_ground_current_score", 5),
                 (assign, "$g_tutorial_mouse_dir", -1),
                 (assign, "$g_tutorial_mouse_click", -1),
                 (tutorial_message, -1),
                 (assign, "$g_tutorial_training_ground_melee_state", 0),
                 (agent_set_team, ":player_agent", 0),
                 (agent_set_team, ":trainer_agent", 7),
                 (agent_set_hit_points, ":player_agent", 100, 0),
                 (agent_set_hit_points, ":trainer_agent", 100, 0),
##                 (assign, "$g_tutorial_training_ground_melee_trainer_parry_completed", 1), #not used
                 (assign, "$g_tutorial_training_ground_conversation_state", 1), #parry complete
                 (start_mission_conversation, "$g_tutorial_training_ground_melee_trainer_parry"),
                 (assign, "$g_tutorial_training_ground_melee_trainer_parry", -1),
               (else_try),
                 (store_random_in_range, ":random_no", 0, 4),
                 (agent_set_attack_action, ":trainer_agent", ":random_no", 1), #ready
                 (val_add, "$g_tutorial_training_ground_melee_trainer_action_state", 1),
                 (assign, "$g_tutorial_mouse_dir", ":random_no"),
                 (try_begin),
                   (is_between, ":random_no", 1, 3), #right or left
                   (store_sub, "$g_tutorial_mouse_dir", 3, ":random_no"), #revert sides
                 (try_end),
                 (assign, "$g_tutorial_mouse_click", 1),
                 (start_presentation, "prsnt_tutorial_show_mouse_movement"),
               (try_end),
             (else_try),
               (eq, "$g_tutorial_training_ground_melee_trainer_action_state", 1),
               (agent_get_defend_action, ":defend_action", ":player_agent"),
               (gt, ":defend_action", 0), #parrying or blocking
               (agent_get_action_dir, ":action_dir_defender", ":player_agent"),
               (agent_get_action_dir, ":action_dir_attacker", ":trainer_agent"),
               (assign, ":actions_match", 0),
               (try_begin),
                 (eq, ":action_dir_attacker", 0), #down
                 (eq, ":action_dir_defender", 0), #down
                 (assign, ":actions_match", 1),
               (else_try),
                 (eq, ":action_dir_attacker", 3), #up
                 (eq, ":action_dir_defender", 3), #up
                 (assign, ":actions_match", 1),
               (else_try),
                 (eq, ":action_dir_attacker", 1), #right
                 (eq, ":action_dir_defender", 2), #left
                 (assign, ":actions_match", 1),
               (else_try),
                 (eq, ":action_dir_attacker", 2), #left
                 (eq, ":action_dir_defender", 1), #right
                 (assign, ":actions_match", 1),
               (try_end),
               (eq, ":actions_match", 1),
               (assign, "$g_tutorial_mouse_dir", -1),
               (assign, "$g_tutorial_mouse_click", -1),
               (agent_set_attack_action, ":trainer_agent", 0, 0), #release
               (val_add, "$g_tutorial_training_ground_melee_trainer_action_state", 1),
               (store_mission_timer_a, "$g_tutorial_training_ground_melee_trainer_next_action_time"),
               (val_add, "$g_tutorial_training_ground_melee_trainer_next_action_time", 2),
             (else_try),
               (eq, "$g_tutorial_training_ground_melee_trainer_action_state", 2),
               (try_begin),
                 (store_mission_timer_a, ":cur_time"),
                 (gt, ":cur_time", "$g_tutorial_training_ground_melee_trainer_next_action_time"),
                 (assign, "$g_tutorial_training_ground_melee_trainer_action_state", 0),
               (try_end),
             (try_end),
           (try_end),
         (try_end),
         (try_begin),
           (agent_is_in_parried_animation, ":trainer_agent"),
           (agent_get_wielded_item, ":shield_item", ":player_agent", 1),
           (eq, ":shield_item", -1),
           (agent_get_wielded_item, ":weapon_item", ":player_agent", 0),
           (neq, ":weapon_item", "itm_practice_dagger"),
           (call_script, "script_cf_is_melee_weapon_for_tutorial", ":weapon_item"),
           (store_mission_timer_a, ":cur_time"),
           (gt, ":cur_time", "$g_tutorial_training_ground_next_score_time"),
           (val_add, "$g_tutorial_training_ground_current_score", 1),
           (try_begin),
             (lt, "$g_tutorial_training_ground_current_score", 5),
             (play_sound, "snd_tutorial_1"),
           (else_try),
             (play_sound, "snd_tutorial_2"),
           (try_end),
           (store_add, "$g_tutorial_training_ground_next_score_time", ":cur_time", 1),
         (try_end),
         (assign, reg0, "$g_tutorial_training_ground_current_score"),
         (try_begin),
           (agent_get_wielded_item, ":shield_item", ":player_agent", 1),
           (eq, ":shield_item", -1),
           (agent_get_wielded_item, ":weapon_item", ":player_agent", 0),
           (neq, ":weapon_item", "itm_practice_dagger"),
           (call_script, "script_cf_is_melee_weapon_for_tutorial", ":weapon_item"),
           (tutorial_message, "str_tutorial_training_ground_parry_training"),
         (else_try),
           (neq, ":shield_item", -1),
           (tutorial_message, "str_tutorial_training_ground_warning_shield"),
         (else_try),
           (tutorial_message, "str_tutorial_training_ground_warning_melee_with_parry"),
         (try_end),
         ], []),

      (0, 0, 0,
       [
         (get_player_agent_no, ":player_agent"),
         (neq, "$g_tutorial_training_ground_melee_trainer_chamber", -1),
         (mission_disable_talk),
         (try_for_agents, ":cur_agent"),
           (agent_get_troop_id, ":cur_agent_troop", ":cur_agent"),
           (eq, ":cur_agent_troop", "$g_tutorial_training_ground_melee_trainer_chamber"),
           (assign, ":trainer_agent", ":cur_agent"),
         (try_end),
         (try_begin),
           (eq, "$g_tutorial_training_ground_melee_state", 0),
           (try_begin),
             (try_for_agents, ":cur_agent"),
               (agent_get_troop_id, ":cur_agent_troop", ":cur_agent"),
               (this_or_next|eq, ":cur_agent_troop", "trp_tutorial_fighter_1"),
               (this_or_next|eq, ":cur_agent_troop", "trp_tutorial_fighter_2"),
               (this_or_next|eq, ":cur_agent_troop", "trp_tutorial_fighter_3"),
               (eq, ":cur_agent_troop", "trp_tutorial_fighter_4"),
               (agent_set_team, ":cur_agent", 7),
               (agent_get_slot, ":spawn_point", ":cur_agent", slot_agent_spawn_entry_point),
               (entry_point_get_position, pos1, ":spawn_point"),
               (agent_set_scripted_destination, ":cur_agent", pos1),
               (agent_force_rethink, ":cur_agent"),
             (try_end),
##             (entry_point_get_position, pos1, 30),
##             (agent_set_scripted_destination_no_attack, ":trainer_agent", pos1, 1),
##             (agent_get_position, pos2, ":trainer_agent"),
##             (get_sq_distance_between_positions, ":sq_dist_1", pos1, pos2),
##             (lt, ":sq_dist_1", 400), #2 meters
##             (entry_point_get_position, pos1, 31),
##             (agent_get_position, pos2, ":player_agent"),
##             (get_sq_distance_between_positions, ":sq_dist_2", pos1, pos2),
##             (lt, ":sq_dist_2", 400), #2 meters
             (agent_set_wielded_item, ":trainer_agent", "itm_practice_sword"), #TODO: change this
             (val_add, "$g_tutorial_training_ground_melee_state", 1),
             (store_mission_timer_a, "$g_tutorial_training_ground_melee_next_action_time"),
             (val_add, "$g_tutorial_training_ground_melee_next_action_time", 1),
           (try_end),
         (else_try),
           (eq, "$g_tutorial_training_ground_melee_state", 1),
           (try_begin),
             (store_mission_timer_a, ":cur_time"),
             (gt, ":cur_time", "$g_tutorial_training_ground_melee_next_action_time"),
             (agent_set_team, ":player_agent", 1),
             (agent_set_team, ":trainer_agent", 2),
             (agent_get_position, pos1, ":player_agent"),
             (agent_set_scripted_destination_no_attack, ":trainer_agent", pos1),
             (agent_get_position, pos2, ":trainer_agent"),
             (get_sq_distance_between_positions, ":sq_dist", pos1, pos2),
             (lt, ":sq_dist", 400), #2 meters
             (try_begin),
               (eq, "$g_tutorial_training_ground_melee_trainer_action_state", 0),
               (try_begin),
                 (ge, "$g_tutorial_training_ground_current_score", 5),
                 (tutorial_message, -1),
                 (assign, "$g_tutorial_training_ground_melee_state", 0),
                 (agent_set_team, ":player_agent", 0),
                 (agent_set_team, ":trainer_agent", 7),
                 (agent_set_hit_points, ":player_agent", 100, 0),
                 (agent_set_hit_points, ":trainer_agent", 100, 0),
##                 (assign, "$g_tutorial_training_ground_melee_trainer_chamber_completed", 1), #not used
                 (assign, "$g_tutorial_training_ground_conversation_state", 6), #chamber complete
                 (start_mission_conversation, "$g_tutorial_training_ground_melee_trainer_chamber"),
                 (assign, "$g_tutorial_training_ground_melee_trainer_chamber", -1),
               (else_try),
                 (store_random_in_range, "$g_tutorial_training_ground_melee_trainer_attack_dir", 0, 4),
                 (agent_set_attack_action, ":trainer_agent", "$g_tutorial_training_ground_melee_trainer_attack_dir", 1), #ready
                 (val_add, "$g_tutorial_training_ground_melee_trainer_action_state", 1),
                 (store_mission_timer_a, "$g_tutorial_training_ground_melee_trainer_next_action_time"),
                 (val_add, "$g_tutorial_training_ground_melee_trainer_next_action_time", 1),
               (try_end),
             (else_try),
               (eq, "$g_tutorial_training_ground_melee_trainer_action_state", 1),
               (try_begin),
                 (store_mission_timer_a, ":cur_time"),
                 (gt, ":cur_time", "$g_tutorial_training_ground_melee_trainer_next_action_time"),
                 (agent_set_attack_action, ":trainer_agent", -1, 0), #cancel
                 (agent_set_defend_action, ":trainer_agent", 0, 1), #cancel
                 (val_add, "$g_tutorial_training_ground_melee_trainer_action_state", 1),
                 (store_mission_timer_a, "$g_tutorial_training_ground_melee_trainer_next_action_time"),
                 (val_add, "$g_tutorial_training_ground_melee_trainer_next_action_time", 1),
               (try_end),
             (else_try),
               (eq, "$g_tutorial_training_ground_melee_trainer_action_state", 2),
               (try_begin),
                 (store_mission_timer_a, ":cur_time"),
                 (gt, ":cur_time", "$g_tutorial_training_ground_melee_trainer_next_action_time"),
                 (agent_set_attack_action, ":trainer_agent", "$g_tutorial_training_ground_melee_trainer_attack_dir", 0),
                 (val_add, "$g_tutorial_training_ground_melee_trainer_action_state", 1),
                 (store_mission_timer_a, "$g_tutorial_training_ground_melee_trainer_next_action_time"),
                 (val_add, "$g_tutorial_training_ground_melee_trainer_next_action_time", 2),
               (try_end),
             (else_try),
               (eq, "$g_tutorial_training_ground_melee_trainer_action_state", 3),
               (try_begin),
                 (store_mission_timer_a, ":cur_time"),
                 (gt, ":cur_time", "$g_tutorial_training_ground_melee_trainer_next_action_time"),
                 (assign, "$g_tutorial_training_ground_melee_trainer_action_state", 0),
               (try_end),
             (try_end),
           (try_end),
         (try_end),
         (try_begin),
           (agent_is_in_parried_animation, ":trainer_agent"),
           (agent_get_attack_action, ":attack_action", ":player_agent"),
           (store_mission_timer_a, ":cur_time"),
           (gt, ":cur_time", "$g_tutorial_training_ground_next_score_time"),
           #add first, because player might immediately start attacking after parry
           (store_add, "$g_tutorial_training_ground_next_score_time", ":cur_time", 1),
           (eq, ":attack_action", 1), #readying_attack
           (val_add, "$g_tutorial_training_ground_current_score", 1),
           (try_begin),
             (lt, "$g_tutorial_training_ground_current_score", 5),
             (play_sound, "snd_tutorial_1"),
           (else_try),
             (play_sound, "snd_tutorial_2"),
           (try_end),
         (try_end),
         (assign, reg0, "$g_tutorial_training_ground_current_score"),
         (tutorial_message, "str_tutorial_training_ground_chamber_training"),
         ], []),

      (0, 0, 0,
       [
         (get_player_agent_no, ":player_agent"),
         (neq, "$g_tutorial_training_ground_melee_trainer_combat", -1),
         (mission_disable_talk),
         (try_for_agents, ":cur_agent"),
           (agent_get_troop_id, ":cur_agent_troop", ":cur_agent"),
           (eq, ":cur_agent_troop", "$g_tutorial_training_ground_melee_trainer_combat"),
           (assign, ":trainer_agent", ":cur_agent"),
         (try_end),
         (try_begin),
           (eq, "$g_tutorial_training_ground_melee_state", 0),
           (try_begin),
             (try_for_agents, ":cur_agent"),
               (agent_get_troop_id, ":cur_agent_troop", ":cur_agent"),
               (this_or_next|eq, ":cur_agent_troop", "trp_tutorial_fighter_1"),
               (this_or_next|eq, ":cur_agent_troop", "trp_tutorial_fighter_2"),
               (this_or_next|eq, ":cur_agent_troop", "trp_tutorial_fighter_3"),
               (eq, ":cur_agent_troop", "trp_tutorial_fighter_4"),
               (agent_set_team, ":cur_agent", 7),
               (agent_get_slot, ":spawn_point", ":cur_agent", slot_agent_spawn_entry_point),
               (entry_point_get_position, pos1, ":spawn_point"),
               (agent_set_scripted_destination, ":cur_agent", pos1),
               (agent_force_rethink, ":cur_agent"),
             (try_end),
##             (entry_point_get_position, pos1, 30),
##             (agent_set_scripted_destination, ":trainer_agent", pos1, 1),
##             (agent_get_position, pos2, ":trainer_agent"),
##             (get_sq_distance_between_positions, ":sq_dist_1", pos1, pos2),
##             (lt, ":sq_dist_1", 400), #2 meters
##             (entry_point_get_position, pos1, 31),
##             (agent_get_position, pos2, ":player_agent"),
##             (get_sq_distance_between_positions, ":sq_dist_2", pos1, pos2),
##             (lt, ":sq_dist_2", 400), #2 meters
             (agent_set_wielded_item, ":trainer_agent", "itm_practice_sword"), #TODO: change this
             (val_add, "$g_tutorial_training_ground_melee_state", 1),
             (store_mission_timer_a, "$g_tutorial_training_ground_melee_next_action_time"),
             (val_add, "$g_tutorial_training_ground_melee_next_action_time", 1),
           (try_end),
         (else_try),
           (eq, "$g_tutorial_training_ground_melee_state", 1),
           (try_begin),
             (store_mission_timer_a, ":cur_time"),
             (gt, ":cur_time", "$g_tutorial_training_ground_melee_next_action_time"),
             (agent_set_team, ":player_agent", 1),
             (agent_set_team, ":trainer_agent", 2),
             (agent_clear_scripted_mode, ":trainer_agent"),
             (agent_force_rethink, ":trainer_agent"),
           (try_end),
         (try_end),
         ], []),

      (0, 0, 0,
       [
         (eq, "$g_tutorial_training_ground_melee_trainer_attack", -1),
         (eq, "$g_tutorial_training_ground_melee_trainer_parry", -1),
         (eq, "$g_tutorial_training_ground_melee_trainer_combat", -1),
         (eq, "$g_tutorial_training_ground_melee_trainer_chamber", -1),
         (eq, "$g_tutorial_training_ground_archer_trainer_state", 0),
         (eq, "$g_tutorial_training_ground_horseman_trainer_state", 0),
         (mission_enable_talk),
         ], []),

      (0, 0, 0,
       [
         (eq, "$g_tutorial_training_ground_melee_trainer_attack", -1),
         (eq, "$g_tutorial_training_ground_melee_trainer_parry", -1),
         (eq, "$g_tutorial_training_ground_melee_trainer_combat", -1),
         (eq, "$g_tutorial_training_ground_melee_trainer_chamber", -1),
         (get_player_agent_no, ":player_agent"),
         (agent_get_position, pos1, ":player_agent"),
         (assign, ":shortest_dist", 10000000),
         (try_for_agents, ":cur_agent"),
           (agent_get_troop_id, ":cur_agent_troop", ":cur_agent"),
           (this_or_next|eq, ":cur_agent_troop", "trp_tutorial_fighter_1"),
           (this_or_next|eq, ":cur_agent_troop", "trp_tutorial_fighter_2"),
           (this_or_next|eq, ":cur_agent_troop", "trp_tutorial_fighter_3"),
           (eq, ":cur_agent_troop", "trp_tutorial_fighter_4"),
           (agent_get_position, pos2, ":cur_agent"),
           (get_sq_distance_between_positions, ":cur_dist", pos1, pos2),
           (lt, ":cur_dist", ":shortest_dist"),
           (assign, ":shortest_dist", ":cur_dist"),
         (try_end),
         (try_begin),
           (le, ":shortest_dist", 1600), #4 meters
           (assign, "$g_tutorial_training_ground_melee_paused", 1),
           (try_for_agents, ":cur_agent"),
             (agent_get_troop_id, ":cur_agent_troop", ":cur_agent"),
             (this_or_next|eq, ":cur_agent_troop", "trp_tutorial_fighter_1"),
             (this_or_next|eq, ":cur_agent_troop", "trp_tutorial_fighter_2"),
             (this_or_next|eq, ":cur_agent_troop", "trp_tutorial_fighter_3"),
             (eq, ":cur_agent_troop", "trp_tutorial_fighter_4"),
             (agent_set_team, ":cur_agent", 7),
             (agent_get_position, pos2, ":cur_agent"),
             (agent_set_scripted_destination, ":cur_agent", pos2),
             (try_begin),
               (neq, ":cur_agent", "$g_tutorial_training_ground_melee_cur_fighter_1"),
               (neq, ":cur_agent", "$g_tutorial_training_ground_melee_cur_fighter_2"),
               (agent_set_wielded_item, ":cur_agent", -1),
             (try_end),
             (agent_force_rethink, ":cur_agent"),
             (agent_set_look_target_agent, ":cur_agent", ":player_agent"),
           (try_end),
         (else_try),
           (gt, "$g_tutorial_training_ground_melee_paused", 0),
           (assign, "$g_tutorial_training_ground_melee_paused", 0),
           (assign, "$g_tutorial_training_ground_melee_state", 0),
         (try_end),
         (try_begin),
           (eq, "$g_tutorial_training_ground_melee_paused", 0),
           (eq, "$g_tutorial_training_ground_melee_state", 0),
           (try_begin),
             (assign, "$g_tutorial_training_ground_melee_cur_fighter_1", -1),
             (assign, "$g_tutorial_training_ground_melee_cur_fighter_2", -1),
             (try_for_range, ":unused", 0, 2),
               (try_begin),
                 (ge, "$g_tutorial_training_ground_melee_last_winner", 0),
                 (assign, "$g_tutorial_training_ground_melee_cur_fighter_1", "$g_tutorial_training_ground_melee_last_winner"),
                 (assign, "$g_tutorial_training_ground_melee_last_winner", -1),
               (try_end),
               (this_or_next|eq, "$g_tutorial_training_ground_melee_cur_fighter_1", -1),
               (eq, "$g_tutorial_training_ground_melee_cur_fighter_2", -1),
               (assign, ":num_candidates", 0),
               (try_for_agents, ":cur_agent"),
                 (agent_get_troop_id, ":cur_agent_troop", ":cur_agent"),
                 (this_or_next|eq, ":cur_agent_troop", "trp_tutorial_fighter_1"),
                 (this_or_next|eq, ":cur_agent_troop", "trp_tutorial_fighter_2"),
                 (this_or_next|eq, ":cur_agent_troop", "trp_tutorial_fighter_3"),
                 (eq, ":cur_agent_troop", "trp_tutorial_fighter_4"),
                 (neq, ":cur_agent", "$g_tutorial_training_ground_melee_cur_fighter_1"),
                 (neq, ":cur_agent", "$g_tutorial_training_ground_melee_cur_fighter_2"),
                 (neq, ":cur_agent", "$g_tutorial_training_ground_melee_last_loser"),
                 (val_add, ":num_candidates", 1),
               (try_end),
               (store_random_in_range, ":random_candidate", 0, ":num_candidates"),
               (try_for_agents, ":cur_agent"),
                 (agent_get_troop_id, ":cur_agent_troop", ":cur_agent"),
                 (this_or_next|eq, ":cur_agent_troop", "trp_tutorial_fighter_1"),
                 (this_or_next|eq, ":cur_agent_troop", "trp_tutorial_fighter_2"),
                 (this_or_next|eq, ":cur_agent_troop", "trp_tutorial_fighter_3"),
                 (eq, ":cur_agent_troop", "trp_tutorial_fighter_4"),
                 (neq, ":cur_agent", "$g_tutorial_training_ground_melee_cur_fighter_1"),
                 (neq, ":cur_agent", "$g_tutorial_training_ground_melee_cur_fighter_2"),
                 (neq, ":cur_agent", "$g_tutorial_training_ground_melee_last_loser"),
                 (val_sub, ":random_candidate", 1),
                 (lt, ":random_candidate", 0),
                 (try_begin),
                   (eq, "$g_tutorial_training_ground_melee_cur_fighter_1", -1),
                   (assign, "$g_tutorial_training_ground_melee_cur_fighter_1", ":cur_agent"),
                 (else_try),
                   (assign, "$g_tutorial_training_ground_melee_cur_fighter_2", ":cur_agent"),
                 (try_end),
               (try_end),
             (try_end),
             (try_for_agents, ":cur_agent"),
               (agent_get_troop_id, ":cur_agent_troop", ":cur_agent"),
               (this_or_next|eq, ":cur_agent_troop", "trp_tutorial_fighter_1"),
               (this_or_next|eq, ":cur_agent_troop", "trp_tutorial_fighter_2"),
               (this_or_next|eq, ":cur_agent_troop", "trp_tutorial_fighter_3"),
               (eq, ":cur_agent_troop", "trp_tutorial_fighter_4"),
               (neq, ":cur_agent", "$g_tutorial_training_ground_melee_cur_fighter_1"),
               (neq, ":cur_agent", "$g_tutorial_training_ground_melee_cur_fighter_2"),
               (agent_set_wielded_item, ":cur_agent", -1),
             (try_end),
             (val_add, "$g_tutorial_training_ground_melee_state", 1), #fighters are chosen
             (store_mission_timer_a, "$g_tutorial_training_ground_melee_next_action_time"),
             (val_add, "$g_tutorial_training_ground_melee_next_action_time", 3),
           (try_end),
         (else_try),
           (eq, "$g_tutorial_training_ground_melee_state", 1),
           (try_begin),
             (store_mission_timer_a, ":cur_time"),
             (gt, ":cur_time", "$g_tutorial_training_ground_melee_next_action_time"),
             (try_for_agents, ":cur_agent"),
               (agent_is_human, ":cur_agent"),
               (agent_get_troop_id, ":cur_agent_troop", ":cur_agent"),
               (this_or_next|eq, ":cur_agent_troop", "trp_tutorial_fighter_1"),
               (this_or_next|eq, ":cur_agent_troop", "trp_tutorial_fighter_2"),
               (this_or_next|eq, ":cur_agent_troop", "trp_tutorial_fighter_3"),
               (eq, ":cur_agent_troop", "trp_tutorial_fighter_4"),
               (try_begin),
                 (eq, ":cur_agent", "$g_tutorial_training_ground_melee_cur_fighter_1"),
                 (entry_point_get_position, pos1, 30),
                 (agent_set_scripted_destination, ":cur_agent", pos1),
               (else_try),
                 (eq, ":cur_agent", "$g_tutorial_training_ground_melee_cur_fighter_2"),
                 (entry_point_get_position, pos1, 31),
                 (agent_set_scripted_destination, ":cur_agent", pos1),
               (else_try),
                 (agent_get_slot, ":spawn_point", ":cur_agent", slot_agent_spawn_entry_point),
                 (entry_point_get_position, pos1, ":spawn_point"),
                 (agent_set_scripted_destination, ":cur_agent", pos1),
               (try_end),
             (try_end),
             (val_add, "$g_tutorial_training_ground_melee_state", 1),
           (try_end),
         (else_try),
           (eq, "$g_tutorial_training_ground_melee_state", 2),
           (try_begin),
             (agent_set_look_target_agent, "$g_tutorial_training_ground_melee_cur_fighter_1", "$g_tutorial_training_ground_melee_cur_fighter_2"),
             (agent_set_look_target_agent, "$g_tutorial_training_ground_melee_cur_fighter_2", "$g_tutorial_training_ground_melee_cur_fighter_1"),
             (agent_get_position, pos1, "$g_tutorial_training_ground_melee_cur_fighter_1"),
             (entry_point_get_position, pos2, 30),
             (get_sq_distance_between_positions, ":sq_dist_1", pos1, pos2),
             (lt, ":sq_dist_1", 400), #2 meters
             (agent_get_position, pos1, "$g_tutorial_training_ground_melee_cur_fighter_2"),
             (entry_point_get_position, pos2, 31),
             (get_sq_distance_between_positions, ":sq_dist_2", pos1, pos2),
             (lt, ":sq_dist_2", 400), #2 meters
             (val_add, "$g_tutorial_training_ground_melee_state", 1),
             (store_mission_timer_a, "$g_tutorial_training_ground_melee_next_action_time"),
             (val_add, "$g_tutorial_training_ground_melee_next_action_time", 1),
           (try_end),
         (else_try),
           (eq, "$g_tutorial_training_ground_melee_state", 3),
           (try_begin),
             (agent_set_look_target_agent, "$g_tutorial_training_ground_melee_cur_fighter_1", "$g_tutorial_training_ground_melee_cur_fighter_2"),
             (agent_set_look_target_agent, "$g_tutorial_training_ground_melee_cur_fighter_2", "$g_tutorial_training_ground_melee_cur_fighter_1"),
             (store_mission_timer_a, ":cur_time"),
             (gt, ":cur_time", "$g_tutorial_training_ground_melee_next_action_time"),
             (agent_clear_scripted_mode, "$g_tutorial_training_ground_melee_cur_fighter_1"),
             (agent_clear_scripted_mode, "$g_tutorial_training_ground_melee_cur_fighter_2"),
             (agent_set_team, "$g_tutorial_training_ground_melee_cur_fighter_1", 1),
             (agent_set_team, "$g_tutorial_training_ground_melee_cur_fighter_2", 2),
             (agent_force_rethink, "$g_tutorial_training_ground_melee_cur_fighter_1"),
             (agent_force_rethink, "$g_tutorial_training_ground_melee_cur_fighter_2"),
             (val_add, "$g_tutorial_training_ground_melee_state", 1),
           (try_end),
         (try_end),
##         (try_begin),
##           (store_mission_timer_a, ":cur_time"),
##           (gt, ":cur_time", 0),
##           (tutorial_message, "str_talk_to_the_trainer"),
##           (assign, "$g_tutorial_training_ground_state", 1),
##         (try_end),
##         (else_try),
##           (eq, "$g_tutorial_training_ground_state", 1),
##         (else_try),
##           (eq, "$g_tutorial_training_ground_state", 2),
##         (else_try),
##           (eq, "$g_tutorial_training_ground_state", 3),
##         (else_try),
##           (eq, "$g_tutorial_training_ground_state", 4),
##         (else_try),
##           (eq, "$g_tutorial_training_ground_state", 5),
##         (try_end),
         ], []),

      
    ],
  ),

  (
    "tutorial_1",0,-1,
    "You enter the training ground.",
    [
        (0,mtef_leader_only,af_override_everything,0,1,[itm_tutorial_shield,itm_tutorial_sword,itm_tutorial_short_bow,itm_tutorial_arrows,itm_leather_jerkin,itm_leather_boots]), #af_override_weapons
     ],
    [
      (ti_tab_pressed, 0, 0, [],
       [(try_begin),
         (lt, "$tutorial_1_state", 5),
         (question_box, "str_do_you_wish_to_leave_tutorial"),
        (else_try),
          (finish_mission,0),
        (try_end),
        ]),
      (ti_question_answered, 0, 0, [],
       [(store_trigger_param_1,":answer"),
        (eq,":answer",0),
        (finish_mission,0),
        ]),
      (ti_inventory_key_pressed, 0, 0, [(display_message, "str_cant_use_inventory_tutorial")], []),

      (0, 0, ti_once, [
      	               (tutorial_message_set_size, 17, 17),
	               (tutorial_message_set_position, 500, 650),
                       (tutorial_message_set_center_justify, 0),

                       (assign, "$tutorial_1_state", 0),
                       (assign, "$tutorial_1_msg_1_displayed", 0),
                       (assign, "$tutorial_1_msg_2_displayed", 0),
                       (assign, "$tutorial_1_msg_3_displayed", 0),
                       (assign, "$tutorial_1_msg_4_displayed", 0),
                       (assign, "$tutorial_1_msg_5_displayed", 0),
                       (assign, "$tutorial_1_msg_6_displayed", 0),
                       ], []),

      (0, 0, 0, [(try_begin),
                   (eq, "$tutorial_1_state", 0),
                   (try_begin),
                     (eq, "$tutorial_1_msg_1_displayed", 0),
                     (store_mission_timer_a, ":cur_time"),
                     (gt, ":cur_time", 0),
                     (assign, "$tutorial_1_msg_1_displayed", 1),
                     (tutorial_message, "str_tutorial_1_msg_1"),
                     (scene_prop_get_instance, ":flag_object", "spr_tutorial_flag_yellow", 0),
                     (entry_point_get_position,pos1,1),
                     (prop_instance_animate_to_position, ":flag_object", pos1, 1),
                   (try_end),
                   (tutorial_message, "str_tutorial_1_msg_1"),
                   (get_player_agent_no, ":player_agent"),
                   (agent_get_position, pos1, ":player_agent"),
                   (entry_point_get_position,pos2,1),
                   (get_distance_between_positions, ":cur_distance", pos1, pos2),
                   (le, ":cur_distance", 100),
                   (val_add, "$tutorial_1_state", 1),
                   (scene_prop_get_instance, ":door_object", "spr_tutorial_door_a", 0),
                   (prop_instance_get_position, pos1, ":door_object"),
                   (position_rotate_z, pos1, -90),
                   (prop_instance_animate_to_position, ":door_object", pos1, 150),
                   (scene_prop_get_instance, ":flag_object", "spr_tutorial_flag_yellow", 0),
                   (entry_point_get_position,pos1,2),
                   (prop_instance_animate_to_position, ":flag_object", pos1, 1),
                 (else_try),
                   (eq, "$tutorial_1_state", 1),
                   (try_begin),
                     (eq, "$tutorial_1_msg_2_displayed", 0),
                     (assign, "$tutorial_1_msg_2_displayed", 1),
                     (tutorial_message, "str_tutorial_1_msg_2"),
                     (play_sound, "snd_tutorial_1"),
                   (try_end),
                   (get_player_agent_no, ":player_agent"),
                   (agent_get_position, pos1, ":player_agent"),
                   (entry_point_get_position,pos2,2),
                   (get_distance_between_positions, ":cur_distance", pos1, pos2),
                   (le, ":cur_distance", 100),
                   (val_add, "$tutorial_1_state", 1),
                   (scene_prop_get_instance, ":door_object", "spr_tutorial_door_a", 1),
                   (prop_instance_get_position, pos1, ":door_object"),
                   (position_rotate_z, pos1, 90),
                   (prop_instance_animate_to_position, ":door_object", pos1, 150),
                   (scene_prop_get_instance, ":flag_object", "spr_tutorial_flag_yellow", 0),
                   (entry_point_get_position,pos1,3),
                   (prop_instance_animate_to_position, ":flag_object", pos1, 1),
                 (else_try),
                   (eq, "$tutorial_1_state", 2),
                   (try_begin),
                     (eq, "$tutorial_1_msg_3_displayed", 0),
                     (assign, "$tutorial_1_msg_3_displayed", 1),
                     (tutorial_message, "str_tutorial_1_msg_3"),
                     (assign, "$tutorial_num_total_dummies_destroyed", 0),
                     (play_sound, "snd_tutorial_1"),
                   (try_end),
                   (ge, "$tutorial_num_total_dummies_destroyed", 4),
                   (val_add, "$tutorial_1_state", 1),
                   (scene_prop_get_instance, ":door_object", "spr_tutorial_door_a", 2),
                   (prop_instance_get_position, pos1, ":door_object"),
                   (position_rotate_z, pos1, 90),
                   (prop_instance_animate_to_position, ":door_object", pos1, 150),
                 (else_try),
                   (eq, "$tutorial_1_state", 3),
                   (try_begin),
                     (eq, "$tutorial_1_msg_4_displayed", 0),
                     (assign, "$tutorial_1_msg_4_displayed", 1),
                     (tutorial_message, "str_tutorial_1_msg_4"),
                     (store_mission_timer_a, "$tutorial_time"),
                     (play_sound, "snd_tutorial_1"),
                   (try_end),
                   (store_mission_timer_a, ":cur_time"),
                   (val_sub, ":cur_time", "$tutorial_time"),
                   (gt, ":cur_time", 10),
                   (val_add, "$tutorial_1_state", 1),
                 (else_try),
                   (eq, "$tutorial_1_state", 4),
                   (try_begin),
                     (eq, "$tutorial_1_msg_5_displayed", 0),
                     (assign, "$tutorial_1_msg_5_displayed", 1),
                     (tutorial_message, "str_tutorial_1_msg_5"),
                     (assign, "$g_last_archery_point_earned", 0),
                     (assign, "$tutorial_num_arrows_hit", 0),
                     (play_sound, "snd_tutorial_1"),
                   (try_end),
                   (try_begin),
                     (get_player_agent_no, ":player_agent"),
                     (agent_get_ammo, ":cur_ammo", ":player_agent"),
                     (le, ":cur_ammo", 0),
                     (agent_refill_ammo, ":player_agent"),
                     (tutorial_message, "str_tutorial_ammo_refilled"),
                   (try_end),
                   (gt, "$g_last_archery_point_earned", 0),
                   (assign, "$g_last_archery_point_earned", 0),
                   (val_add, "$tutorial_num_arrows_hit", 1),
                   (gt, "$tutorial_num_arrows_hit", 2),
                   (val_add, "$tutorial_1_state", 1),
                 (else_try),
                   (eq, "$tutorial_1_state", 5),
                   (eq, "$tutorial_1_msg_6_displayed", 0),
                   (assign, "$tutorial_1_msg_6_displayed", 1),
                   (tutorial_message, "str_tutorial_1_msg_6"),
                   (play_sound, "snd_tutorial_2"),
                   (assign, "$tutorial_1_finished", 1),
                 (try_end),
                 ], []),
    ],
  ),

##  (
##    "tutorial_1",0,-1,
##    "You enter the training ground.",
##    [
##        (0,mtef_leader_only|mtef_team_0,af_override_horse|af_override_weapons,0,1,[itm_tutorial_shield,itm_tutorial_sword,itm_tutorial_short_bow,itm_tutorial_arrows]), #af_override_weapons
##        (1,mtef_visitor_source|mtef_team_0,0,0,1,[]),
##        (2,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
##        (3,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
##        (4,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
##        (5,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
##        (6,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
##        (7,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
##        (8,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
##        (9,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
##        (10,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
##     ],
##    [
##      (ti_tab_pressed, 0, 0, [],
##       [(try_begin),
##         (lt, "$tutorial_1_state", 5),
##         (question_box, "str_do_you_wish_to_leave_tutorial"),
##        (else_try),
##          (finish_mission,0),
##        (try_end),
##        ]),
##      (ti_question_answered, 0, 0, [],
##       [(store_trigger_param_1,":answer"),
##        (eq,":answer",0),
##        (finish_mission,0),
##        ]),
##      (ti_inventory_key_pressed, 0, 0, [(display_message, "str_cant_use_inventory_tutorial")], []),
##
##      (0, 0, ti_once, [
##      	               (tutorial_message_set_size, 17, 17),
##	               (tutorial_message_set_position, 500, 650),
##                       (tutorial_message_set_center_justify, 0),
##                       (assign, "$tutorial_1_state", 0),
##                       ], []),
##
##      (0, 0, 0, [(try_begin),
##                   (eq, "$tutorial_1_state", 0),
##                   (try_begin),
##                     (store_mission_timer_a, ":cur_time"),
##                     (gt, ":cur_time", 0),
##                     (tutorial_message, "str_talk_to_the_trainer"),
##                     (assign, "$tutorial_1_state", 1),
##                   (try_end),
##                 (else_try),
##                   (eq, "$tutorial_1_state", 1),
##                 (else_try),
##                   (eq, "$tutorial_1_state", 2),
##                 (else_try),
##                   (eq, "$tutorial_1_state", 3),
##                 (else_try),
##                   (eq, "$tutorial_1_state", 4),
##                 (else_try),
##                   (eq, "$tutorial_1_state", 5),
##                 (try_end),
##                 ], []),
##    ],
##  ),


  (
    "tutorial_2",mtf_arena_fight,-1,
    "You enter the training ground.",
    [
        (0,mtef_leader_only|mtef_team_0,af_override_everything,0,1,[itm_tutorial_shield,itm_leather_jerkin,itm_leather_boots]),
        (2,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
        (4,mtef_visitor_source|mtef_team_1,0,0,1,[]),
     ],
    [
      (ti_tab_pressed, 0, 0, [],
       [(try_begin),
         (lt, "$tutorial_2_state", 9),
         (question_box,"str_do_you_wish_to_leave_tutorial"),
        (else_try),
          (finish_mission,0),
        (try_end),
        ]),
      (ti_question_answered, 0, 0, [],
       [(store_trigger_param_1,":answer"),
        (eq,":answer",0),
        (finish_mission,0),
        ]),
      (ti_inventory_key_pressed, 0, 0, [(display_message,"str_cant_use_inventory_tutorial")], []),
      (0, 0, ti_once, [
          (store_mission_timer_a, ":cur_time"),
          (gt, ":cur_time", 2),
          (main_hero_fallen),
          (assign, "$tutorial_2_state", 100),
        ], []),

      (0, 0, ti_once, [
      	               (tutorial_message_set_size, 17, 17),
	                   (tutorial_message_set_position, 500, 650),
                       (tutorial_message_set_center_justify, 0),
		               
                       (assign, "$tutorial_2_state", 0),
                       (assign, "$tutorial_2_msg_1_displayed", 0),
                       (assign, "$tutorial_2_msg_2_displayed", 0),
                       (assign, "$tutorial_2_msg_3_displayed", 0),
                       (assign, "$tutorial_2_msg_4_displayed", 0),
                       (assign, "$tutorial_2_msg_5_displayed", 0),
                       (assign, "$tutorial_2_msg_6_displayed", 0),
                       (assign, "$tutorial_2_msg_7_displayed", 0),
                       (assign, "$tutorial_2_msg_8_displayed", 0),
                       (assign, "$tutorial_2_msg_9_displayed", 0),
                       (assign, "$tutorial_2_melee_agent_state", 0),
                       ], []),

      (10, 0, 0, [(call_script, "script_cf_get_first_agent_with_troop_id", "trp_tutorial_archer"),
                  (agent_refill_ammo, reg0)], []),

      (0, 0, 0, [(try_begin),
                   (eq, "$tutorial_2_state", 0),
                   (try_begin),
                     (eq, "$tutorial_2_msg_1_displayed", 0),
                     (store_mission_timer_a, ":cur_time"),
                     (gt, ":cur_time", 0),
                     (assign, "$tutorial_2_msg_1_displayed", 1),
                     (tutorial_message, "str_tutorial_2_msg_1"),
                     (team_give_order, 1, grc_everyone, mordr_stand_ground),
                     (team_give_order, 1, grc_infantry, mordr_charge),
                     (call_script, "script_cf_get_first_agent_with_troop_id", "trp_tutorial_maceman"),
                     (assign, ":cur_agent", reg0),
                     (agent_get_position, pos1, ":cur_agent"),
                     (agent_set_scripted_destination, ":cur_agent", pos1, 0),
                   (try_end),
                   (get_player_agent_no, ":player_agent"),
                   (ge, ":player_agent", 0),
                   (agent_get_position, pos1, ":player_agent"),
                   (entry_point_get_position,pos2,1),
                   (get_distance_between_positions, ":cur_distance", pos1, pos2),
                   (le, ":cur_distance", 200),
                   (scene_prop_get_instance, ":door_object", "spr_tutorial_door_a", 0),
                   (prop_instance_get_position, pos1, ":door_object"),
                   (position_rotate_z, pos1, 90),
                   (prop_instance_animate_to_position, ":door_object", pos1, 150),
                   (val_add, "$tutorial_2_state", 1),
                 (else_try),
                   (eq, "$tutorial_2_state", 1),
                   (scene_prop_get_instance, ":barrier_object", "spr_barrier_4m", 0),
                   (prop_instance_get_position, pos1, ":barrier_object"),
                   (get_player_agent_no, ":player_agent"),
                   (agent_get_position, pos2, ":player_agent"),
                   (position_is_behind_position, pos2, pos1),
                   (scene_prop_get_instance, ":door_object", "spr_tutorial_door_a", 0),
                   (prop_instance_get_position, pos1, ":door_object"),
                   (position_rotate_z, pos1, -90),
                   (prop_instance_animate_to_position, ":door_object", pos1, 150),
                   (val_add, "$tutorial_2_state", 1),
                 (else_try),
                   (eq, "$tutorial_2_state", 2),
                   (get_player_agent_no, ":player_agent"),
                   (agent_set_kick_allowed, ":player_agent", 0), #don't let player kick while defending
                   (try_begin),
                     (eq, "$tutorial_2_melee_agent_state", 0),
                     (val_add, "$tutorial_2_melee_agent_state", 1),
                     (call_script, "script_cf_get_first_agent_with_troop_id", "trp_tutorial_maceman"),
                     (assign, ":cur_agent", reg0),
                     (entry_point_get_position, pos1, 3),
                     (agent_set_scripted_destination, ":cur_agent", pos1, 0),
                   (else_try),
                     (eq, "$tutorial_2_melee_agent_state", 1),
                     (call_script, "script_cf_get_first_agent_with_troop_id", "trp_tutorial_maceman"),
                     (assign, ":cur_agent", reg0),
                     (entry_point_get_position, pos1, 3),
                     (agent_get_position, pos2, ":cur_agent"),
                     (get_distance_between_positions, ":cur_distance", pos1, pos2),
                     (le, ":cur_distance", 250),
                     (agent_clear_scripted_mode, ":cur_agent"),
                     (val_add, "$tutorial_2_melee_agent_state", 1),
                     (store_mission_timer_a,"$tutorial_time"),
                   (else_try),
                     (eq, "$tutorial_2_melee_agent_state", 2),
                     (try_begin),
                       (eq, "$tutorial_2_msg_2_displayed", 0),
                       (assign, "$tutorial_2_msg_2_displayed", 1),
                       (play_sound, "snd_tutorial_1"),
                     (try_end),
                     (call_script, "script_cf_get_first_agent_with_troop_id", "trp_tutorial_maceman"),
                     (assign, ":cur_agent", reg0),
                     (store_mission_timer_a,":cur_time"),
                     (val_sub, ":cur_time", "$tutorial_time"),
                     (store_sub, reg3, 20, ":cur_time"),
                     (tutorial_message, "str_tutorial_2_msg_2"),
                     (gt, ":cur_time", 20),
                     (entry_point_get_position, pos1, 3),
                     (agent_set_scripted_destination, ":cur_agent", pos1, 0),
                     (val_add, "$tutorial_2_melee_agent_state", 1),
                   (else_try),
                     (eq, "$tutorial_2_melee_agent_state", 3),
                     (try_begin),
                       (eq, "$tutorial_2_msg_3_displayed", 0),
                       (assign, "$tutorial_2_msg_3_displayed", 1),
                       (tutorial_message, "str_tutorial_2_msg_3"),
                       (play_sound, "snd_tutorial_1"),
                     (try_end),
                     (call_script, "script_cf_get_first_agent_with_troop_id", "trp_tutorial_maceman"),
                     (assign, ":cur_agent", reg0),
                     (entry_point_get_position, pos1, 3),
                     (agent_get_position, pos2, ":cur_agent"),
                     (get_distance_between_positions, ":cur_distance", pos1, pos2),
                     (le, ":cur_distance", 250),
                     (entry_point_get_position, pos1, 2),
                     (agent_set_scripted_destination, ":cur_agent", pos1, 0),
                     (val_add, "$tutorial_2_melee_agent_state", 1),
                   (else_try),
                     (eq, "$tutorial_2_melee_agent_state", 4),
                     (call_script, "script_cf_get_first_agent_with_troop_id", "trp_tutorial_maceman"),
                     (assign, ":cur_agent", reg0),
                     (entry_point_get_position, pos1, 2),
                     (agent_get_position, pos2, ":cur_agent"),
                     (get_distance_between_positions, ":cur_distance", pos1, pos2),
                     (le, ":cur_distance", 250),
                     (entry_point_get_position, pos1, 30),
                     (agent_set_position, ":cur_agent", pos1),
                     (agent_set_scripted_destination, ":cur_agent", pos1, 0),
                     (scene_prop_get_instance, ":door_object", "spr_tutorial_door_a", 1),
                     (prop_instance_get_position, pos1, ":door_object"),
                     (position_rotate_z, pos1, 90),
                     (prop_instance_animate_to_position, ":door_object", pos1, 150),
                     (val_add, "$tutorial_2_melee_agent_state", 1),
                     (val_add, "$tutorial_2_state", 1),
                   (try_end),
                 (else_try),
                   (eq, "$tutorial_2_state", 3),
                   (scene_prop_get_instance, ":barrier_object", "spr_barrier_4m", 1),
                   (prop_instance_get_position, pos1, ":barrier_object"),
                   (get_player_agent_no, ":player_agent"),
                   (agent_set_kick_allowed, ":player_agent", 1), #reenable
                   (agent_get_position, pos2, ":player_agent"),
                   (position_is_behind_position, pos2, pos1),
                   (scene_prop_get_instance, ":door_object", "spr_tutorial_door_a", 1),
                   (prop_instance_get_position, pos1, ":door_object"),
                   (position_rotate_z, pos1, -90),
                   (prop_instance_animate_to_position, ":door_object", pos1, 150),
                   (store_mission_timer_a,"$tutorial_time"),
                   (val_add, "$tutorial_2_state", 1),
                 (else_try),
                   (eq, "$tutorial_2_state", 4),
                   (try_begin),
                     (eq, "$tutorial_2_msg_4_displayed", 0),
                     (assign, "$tutorial_2_msg_4_displayed", 1),
                     (play_sound, "snd_tutorial_1"),
                   (try_end),
                   (store_mission_timer_a,":cur_time"),
                   (val_sub, ":cur_time", "$tutorial_time"),
                   (store_sub, reg3, 20, ":cur_time"),
                   (tutorial_message, "str_tutorial_2_msg_4"),
                   (gt, ":cur_time", 20),
                   (entry_point_get_position,pos1,5),
                   (set_spawn_position, pos1),
                   (spawn_item, "itm_tutorial_sword"),
                   (call_script, "script_cf_get_first_agent_with_troop_id", "trp_tutorial_maceman"),
                   (assign, ":cur_agent", reg0),
                   (entry_point_get_position, pos1, 3),
                   (agent_set_position, ":cur_agent", pos1),
                   (agent_set_scripted_destination, ":cur_agent", pos1, 0),
                   (scene_prop_get_instance, ":door_object", "spr_tutorial_door_a", 2),
                   (prop_instance_get_position, pos1, ":door_object"),
                   (position_rotate_z, pos1, 90),
                   (prop_instance_animate_to_position, ":door_object", pos1, 150),
                   (val_add, "$tutorial_2_state", 1),
                 (else_try),
                   (eq, "$tutorial_2_state", 5),
                   (try_begin),
                     (eq, "$tutorial_2_msg_5_displayed", 0),
                     (assign, "$tutorial_2_msg_5_displayed", 1),
                     (tutorial_message, "str_tutorial_2_msg_5"),
                     (play_sound, "snd_tutorial_1"),
                   (try_end),
                   (scene_prop_get_instance, ":barrier_object", "spr_barrier_4m", 2),
                   (prop_instance_get_position, pos1, ":barrier_object"),
                   (get_player_agent_no, ":player_agent"),
                   (agent_get_position, pos2, ":player_agent"),
                   (position_is_behind_position, pos2, pos1),
                   (scene_prop_get_instance, ":door_object", "spr_tutorial_door_a", 2),
                   (prop_instance_get_position, pos1, ":door_object"),
                   (position_rotate_z, pos1, -90),
                   (prop_instance_animate_to_position, ":door_object", pos1, 150),
                   (val_add, "$tutorial_2_state", 1),
                 (else_try),
                   (eq, "$tutorial_2_state", 6),
                   (try_begin),
                     (eq, "$tutorial_2_msg_6_displayed", 0),
                     (assign, "$tutorial_2_msg_6_displayed", 1),
                     (tutorial_message, "str_tutorial_2_msg_6"),
                     (play_sound, "snd_tutorial_1"),
                   (try_end),
                   (get_player_agent_no, ":player_agent"),
                   (agent_has_item_equipped, ":player_agent", "itm_tutorial_sword"),
                   (scene_prop_get_instance, ":door_object", "spr_tutorial_door_a", 3),
                   (prop_instance_get_position, pos1, ":door_object"),
                   (position_rotate_z, pos1, -90),
                   (prop_instance_animate_to_position, ":door_object", pos1, 150),
                   (val_add, "$tutorial_2_state", 1),
                 (else_try),
                   (eq, "$tutorial_2_state", 7),
                   (try_begin),
                     (eq, "$tutorial_2_msg_7_displayed", 0),
                     (assign, "$tutorial_2_msg_7_displayed", 1),
                     (tutorial_message, "str_tutorial_2_msg_7"),
                     (play_sound, "snd_tutorial_1"),
                     (get_player_agent_no, ":player_agent"),
                     (agent_set_hit_points, ":player_agent", 100),
                   (try_end),
                   (call_script, "script_cf_get_first_agent_with_troop_id", "trp_tutorial_archer"),
                   (assign, ":cur_agent", reg0),
                   (neg|agent_is_alive, ":cur_agent"),
                   (call_script, "script_cf_get_first_agent_with_troop_id", "trp_tutorial_maceman"),
                   (assign, ":cur_agent", reg0),
                   (agent_clear_scripted_mode, ":cur_agent"),
                   (scene_prop_get_instance, ":door_object", "spr_tutorial_door_a", 4),
                   (prop_instance_get_position, pos1, ":door_object"),
                   (position_rotate_z, pos1, -90),
                   (prop_instance_animate_to_position, ":door_object", pos1, 150),
                   (val_add, "$tutorial_2_state", 1),
                 (else_try),
                   (eq, "$tutorial_2_state", 8),
                   (try_begin),
                     (eq, "$tutorial_2_msg_8_displayed", 0),
                     (assign, "$tutorial_2_msg_8_displayed", 1),
                     (tutorial_message, "str_tutorial_2_msg_8"),
                     (play_sound, "snd_tutorial_1"),
                     (get_player_agent_no, ":player_agent"),
                     (agent_set_hit_points, ":player_agent", 100),
                   (try_end),
                   (call_script, "script_cf_get_first_agent_with_troop_id", "trp_tutorial_maceman"),
                   (assign, ":cur_agent", reg0),
                   (neg|agent_is_alive, ":cur_agent"),
                   (val_add, "$tutorial_2_state", 1),
                 (else_try),
                   (eq, "$tutorial_2_state", 9),
                   (eq, "$tutorial_2_msg_9_displayed", 0),
                   (assign, "$tutorial_2_msg_9_displayed", 1),
                   (tutorial_message, "str_tutorial_2_msg_9"),
                   (play_sound, "snd_tutorial_2"),
                   (assign, "$tutorial_2_finished", 1),
                 (else_try),
                   (gt, "$tutorial_2_state", 30),
                   (tutorial_message, "str_tutorial_failed"),
                 (try_end),
                 ], []),
    ],
  ),

  (
    "tutorial_3",mtf_arena_fight,-1,
    "You enter the training ground.",
    [
        (0,mtef_leader_only|mtef_team_0,af_override_everything,0,1,[itm_leather_jerkin,itm_leather_boots]),
        (3,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
        (5,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
     ],
    [
      (ti_tab_pressed, 0, 0, [],
       [(try_begin),
         (lt, "$tutorial_3_state", 12),
         (question_box,"str_do_you_wish_to_leave_tutorial"),
        (else_try),
          (finish_mission,0),
        (try_end),
        ]),
      (ti_question_answered, 0, 0, [],
       [(store_trigger_param_1,":answer"),
        (eq,":answer",0),
        (finish_mission,0),
        ]),
      (ti_inventory_key_pressed, 0, 0, [(display_message,"str_cant_use_inventory_tutorial")], []),

      (0, 0, ti_once, [
          (store_mission_timer_a, ":cur_time"),
          (gt, ":cur_time", 2),
          (main_hero_fallen),
          (assign, "$tutorial_3_state", 100),
        ], []),

      (0, 0, ti_once, [
      	               (tutorial_message_set_size, 17, 17),
	                   (tutorial_message_set_position, 500, 650),
                       (tutorial_message_set_center_justify, 0),

                       (assign, "$tutorial_3_state", 0),
                       (assign, "$tutorial_3_msg_1_displayed", 0),
                       (assign, "$tutorial_3_msg_2_displayed", 0),
                       (assign, "$tutorial_3_msg_3_displayed", 0),
                       (assign, "$tutorial_3_msg_4_displayed", 0),
                       (assign, "$tutorial_3_msg_5_displayed", 0),
                       (assign, "$tutorial_3_msg_6_displayed", 0),
                       ], []),

      (0, 0, 0, [(try_begin),
                   (eq, "$tutorial_3_state", 0),
                   (try_begin),
                     (eq, "$tutorial_3_msg_1_displayed", 0),
                     (store_mission_timer_a, ":cur_time"),
                     (gt, ":cur_time", 0),
                     (assign, "$tutorial_3_msg_1_displayed", 1),
                     (tutorial_message, "str_tutorial_3_msg_1"),
                     (call_script, "script_cf_get_first_agent_with_troop_id", "trp_tutorial_maceman"),
                     (assign, ":cur_agent", reg0),
                     (agent_get_position, pos1, ":cur_agent"),
                     (agent_set_scripted_destination, ":cur_agent", pos1, 0),
                     (call_script, "script_cf_get_first_agent_with_troop_id", "trp_tutorial_swordsman"),
                     (assign, ":cur_agent", reg0),
                     (agent_get_position, pos1, ":cur_agent"),
                     (agent_set_scripted_destination, ":cur_agent", pos1, 0),
                     (entry_point_get_position, pos1, 1),
                     (set_spawn_position, pos1),
                     (spawn_item, "itm_tutorial_staff_no_attack"),
                   (try_end),
                   (get_player_agent_no, ":player_agent"),
                   (ge, ":player_agent", 0),
                   (agent_has_item_equipped, ":player_agent", "itm_tutorial_staff_no_attack"),
                   (val_add, "$tutorial_3_state", 1),
                 (else_try),
                   (eq, "$tutorial_3_state", 1),
                   (try_begin),
                     (eq, "$tutorial_3_msg_2_displayed", 0),
                     (assign, "$tutorial_3_msg_2_displayed", 1),
                     (tutorial_message, "str_tutorial_3_msg_2"),
                     (play_sound, "snd_tutorial_1"),
                   (try_end),
                   (get_player_agent_no, ":player_agent"),
                   (agent_get_position, pos1, ":player_agent"),
                   (entry_point_get_position,pos2,2),
                   (get_distance_between_positions, ":cur_distance", pos1, pos2),
                   (le, ":cur_distance", 200),
                   (scene_prop_get_instance, ":door_object", "spr_tutorial_door_b", 0),
                   (prop_instance_get_position, pos1, ":door_object"),
                   (position_rotate_z, pos1, -90),
                   (prop_instance_animate_to_position, ":door_object", pos1, 150),
                   (val_add, "$tutorial_3_state", 1),
                 (else_try),
                   (eq, "$tutorial_3_state", 2),
                   (scene_prop_get_instance, ":barrier_object", "spr_barrier_4m", 0),
                   (prop_instance_get_position, pos1, ":barrier_object"),
                   (get_player_agent_no, ":player_agent"),
                   (agent_get_position, pos2, ":player_agent"),
                   (position_is_behind_position, pos2, pos1),
                   (scene_prop_get_instance, ":door_object", "spr_tutorial_door_b", 0),
                   (prop_instance_get_position, pos1, ":door_object"),
                   (position_rotate_z, pos1, 90),
                   (prop_instance_animate_to_position, ":door_object", pos1, 150),
                   (val_add, "$tutorial_3_state", 1),
                 (else_try),
                   (eq, "$tutorial_3_state", 3),
                   (get_player_agent_no, ":player_agent"),
                   (agent_set_kick_allowed, ":player_agent", 0), #don't let player kick while defending
                   (call_script, "script_cf_get_first_agent_with_troop_id", "trp_tutorial_maceman"),
                   (assign, ":cur_agent", reg0),
                   (entry_point_get_position, pos1, 4),
                   (agent_set_scripted_destination, ":cur_agent", pos1, 0),
                   (val_add, "$tutorial_3_state", 1),
                 (else_try),
                   (eq, "$tutorial_3_state", 4),
                   (call_script, "script_cf_get_first_agent_with_troop_id", "trp_tutorial_maceman"),
                   (assign, ":cur_agent", reg0),
                   (entry_point_get_position, pos1, 4),
                   (agent_get_position, pos2, ":cur_agent"),
                   (get_distance_between_positions, ":cur_distance", pos1, pos2),
                   (le, ":cur_distance", 250),
                   (agent_clear_scripted_mode, ":cur_agent"),
                   (val_add, "$tutorial_3_state", 1),
                   (store_mission_timer_a,"$tutorial_time"),
                 (else_try),
                   (eq, "$tutorial_3_state", 5),
                   (try_begin),
                     (eq, "$tutorial_3_msg_3_displayed", 0),
                     (assign, "$tutorial_3_msg_3_displayed", 1),
                     (play_sound, "snd_tutorial_1"),
                   (try_end),
                   (call_script, "script_cf_get_first_agent_with_troop_id", "trp_tutorial_maceman"),
                   (assign, ":cur_agent", reg0),
                   (store_mission_timer_a,":cur_time"),
                   (val_sub, ":cur_time", "$tutorial_time"),
                   (store_sub, reg3, 20, ":cur_time"),
                   (tutorial_message, "str_tutorial_3_msg_3"),
                   (gt, ":cur_time", 20),
                   (entry_point_get_position, pos1, 4),
                   (agent_set_scripted_destination, ":cur_agent", pos1, 0),
                   (val_add, "$tutorial_3_state", 1),
                 (else_try),
                   (eq, "$tutorial_3_state", 6),
                   (try_begin),
                     (eq, "$tutorial_3_msg_4_displayed", 0),
                     (assign, "$tutorial_3_msg_4_displayed", 1),
                     (tutorial_message, "str_tutorial_3_msg_4"),
                     (play_sound, "snd_tutorial_1"),
                   (try_end),
                   (call_script, "script_cf_get_first_agent_with_troop_id", "trp_tutorial_maceman"),
                   (assign, ":cur_agent", reg0),
                   (entry_point_get_position, pos1, 4),
                   (agent_get_position, pos2, ":cur_agent"),
                   (get_distance_between_positions, ":cur_distance", pos1, pos2),
                   (le, ":cur_distance", 250),
                   (entry_point_get_position, pos1, 3),
                   (agent_set_scripted_destination, ":cur_agent", pos1, 0),
                   (val_add, "$tutorial_3_state", 1),
                 (else_try),
                   (eq, "$tutorial_3_state", 7),
                   (call_script, "script_cf_get_first_agent_with_troop_id", "trp_tutorial_maceman"),
                   (assign, ":cur_agent", reg0),
                   (entry_point_get_position, pos1, 3),
                   (agent_get_position, pos2, ":cur_agent"),
                   (get_distance_between_positions, ":cur_distance", pos1, pos2),
                   (le, ":cur_distance", 250),
                   (entry_point_get_position, pos1, 7),
                   (agent_set_scripted_destination, ":cur_agent", pos1, 0),
                   (agent_set_position, ":cur_agent", pos1),
                   (scene_prop_get_instance, ":door_object", "spr_tutorial_door_b", 1),
                   (prop_instance_get_position, pos1, ":door_object"),
                   (position_rotate_z, pos1, -90),
                   (prop_instance_animate_to_position, ":door_object", pos1, 150),
                   (scene_prop_get_instance, ":door_object", "spr_tutorial_door_b", 3),
                   (prop_instance_get_position, pos1, ":door_object"),
                   (position_rotate_z, pos1, -90),
                   (prop_instance_animate_to_position, ":door_object", pos1, 150),
                   (val_add, "$tutorial_3_state", 1),
                 (else_try),
                   (eq, "$tutorial_3_state", 8),
                   (scene_prop_get_instance, ":barrier_object", "spr_barrier_4m", 1),
                   (prop_instance_get_position, pos1, ":barrier_object"),
                   (get_player_agent_no, ":player_agent"),
                   (agent_get_position, pos2, ":player_agent"),
                   (position_is_behind_position, pos2, pos1),
                   (scene_prop_get_instance, ":door_object", "spr_tutorial_door_b", 1),
                   (prop_instance_get_position, pos1, ":door_object"),
                   (position_rotate_z, pos1, 90),
                   (prop_instance_animate_to_position, ":door_object", pos1, 150),
                   (val_add, "$tutorial_3_state", 1),
                 (else_try),
                   (eq, "$tutorial_3_state", 9),
                   (call_script, "script_cf_get_first_agent_with_troop_id", "trp_tutorial_swordsman"),
                   (assign, ":cur_agent", reg0),
                   (entry_point_get_position, pos1, 6),
                   (agent_set_scripted_destination, ":cur_agent", pos1, 0),
                   (val_add, "$tutorial_3_state", 1),
                 (else_try),
                   (eq, "$tutorial_3_state", 10),
                   (call_script, "script_cf_get_first_agent_with_troop_id", "trp_tutorial_swordsman"),
                   (assign, ":cur_agent", reg0),
                   (entry_point_get_position, pos1, 6),
                   (agent_get_position, pos2, ":cur_agent"),
                   (get_distance_between_positions, ":cur_distance", pos1, pos2),
                   (le, ":cur_distance", 250),
                   (agent_clear_scripted_mode, ":cur_agent"),
                   (val_add, "$tutorial_3_state", 1),
                   (store_mission_timer_a,"$tutorial_time"),
                 (else_try),
                   (eq, "$tutorial_3_state", 11),
                   (try_begin),
                     (eq, "$tutorial_3_msg_5_displayed", 0),
                     (assign, "$tutorial_3_msg_5_displayed", 1),
                     (play_sound, "snd_tutorial_1"),
                   (try_end),
                   (call_script, "script_cf_get_first_agent_with_troop_id", "trp_tutorial_swordsman"),
                   (assign, ":cur_agent", reg0),
                   (store_mission_timer_a,":cur_time"),
                   (val_sub, ":cur_time", "$tutorial_time"),
                   (store_sub, reg3, 20, ":cur_time"),
                   (tutorial_message, "str_tutorial_3_msg_5"),
                   (gt, ":cur_time", 20),
                   (entry_point_get_position, pos1, 6),
                   (agent_set_scripted_destination, ":cur_agent", pos1, 0),
                   (val_add, "$tutorial_3_state", 1),
                 (else_try),
                   (eq, "$tutorial_3_state", 12),
                   (try_begin),
                     (eq, "$tutorial_3_msg_6_displayed", 0),
                     (assign, "$tutorial_3_msg_6_displayed", 1),
                     (tutorial_message, "str_tutorial_3_msg_6"),
                     (play_sound, "snd_tutorial_1"),
                   (try_end),
                   (call_script, "script_cf_get_first_agent_with_troop_id", "trp_tutorial_swordsman"),
                   (assign, ":cur_agent", reg0),
                   (entry_point_get_position, pos1, 6),
                   (agent_get_position, pos2, ":cur_agent"),
                   (get_distance_between_positions, ":cur_distance", pos1, pos2),
                   (le, ":cur_distance", 250),
                   (entry_point_get_position, pos1, 5),
                   (agent_set_scripted_destination, ":cur_agent", pos1, 0),
                   (val_add, "$tutorial_3_state", 1),
                 (else_try),
                   (eq, "$tutorial_3_state", 13),
                   (call_script, "script_cf_get_first_agent_with_troop_id", "trp_tutorial_swordsman"),
                   (assign, ":cur_agent", reg0),
                   (entry_point_get_position, pos1, 5),
                   (agent_get_position, pos2, ":cur_agent"),
                   (get_distance_between_positions, ":cur_distance", pos1, pos2),
                   (le, ":cur_distance", 250),
                   (entry_point_get_position, pos1, 7),
                   (agent_set_scripted_destination, ":cur_agent", pos1, 0),
                   (agent_set_position, ":cur_agent", pos1),
                   (val_add, "$tutorial_3_state", 1),
                 (else_try),
                   (gt, "$tutorial_3_state", 30),
                   (tutorial_message, "str_tutorial_failed"),
                 (try_end),
                 ], []),
    ],
  ),

  (
    "tutorial_3_2",mtf_arena_fight,-1,
    "You enter the training ground.",
    [
        (0,mtef_leader_only|mtef_team_0,af_override_everything,0,1,[itm_tutorial_staff,itm_leather_jerkin,itm_leather_boots]), 
        (4,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
        (6,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
     ],
    [
      (ti_tab_pressed, 0, 0, [],
       [(try_begin),
         (lt, "$tutorial_3_state", 5),
         (question_box,"str_do_you_wish_to_leave_tutorial"),
        (else_try),
          (finish_mission,0),
        (try_end),
        ]),
      (ti_question_answered, 0, 0, [],
       [(store_trigger_param_1,":answer"),
        (eq,":answer",0),
        (finish_mission,0),
        ]),
      (ti_inventory_key_pressed, 0, 0, [(display_message,"str_cant_use_inventory_tutorial")], []),

      (0, 0, ti_once, [
          (store_mission_timer_a, ":cur_time"),
          (gt, ":cur_time", 2),
          (main_hero_fallen),
          (assign, "$tutorial_3_state", 100),
        ], []),


      (0, 0, ti_once, [
      	               (tutorial_message_set_size, 17, 17),
	                   (tutorial_message_set_position, 500, 650),
                       (tutorial_message_set_center_justify, 0),

                       (assign, "$tutorial_3_state", 0),
                       (assign, "$tutorial_3_msg_1_displayed", 0),
                       (assign, "$tutorial_3_msg_2_displayed", 0),
                       (assign, "$tutorial_3_msg_3_displayed", 0),
                       (assign, "$tutorial_3_msg_4_displayed", 0),
                       (assign, "$tutorial_3_msg_5_displayed", 0),
                       ], []),

      (0, 0, 0, [(try_begin),
                   (eq, "$tutorial_3_state", 0),
                   (try_begin),
                     (eq, "$tutorial_3_msg_1_displayed", 0),
                     (store_mission_timer_a, ":cur_time"),
                     (gt, ":cur_time", 0),
                     (assign, "$tutorial_3_msg_1_displayed", 1),
                     (tutorial_message, "str_tutorial_3_2_msg_1"),
                     (play_sound, "snd_tutorial_1"),
                     (call_script, "script_cf_get_first_agent_with_troop_id","trp_tutorial_maceman"),
                     (assign, ":cur_agent", reg0),
                     (agent_get_position, pos1, ":cur_agent"),
                     (agent_set_scripted_destination, ":cur_agent", pos1, 0),
                     (call_script, "script_cf_get_first_agent_with_troop_id", "trp_tutorial_swordsman"),
                     (assign, ":cur_agent", reg0),
                     (agent_get_position, pos1, ":cur_agent"),
                     (agent_set_scripted_destination, ":cur_agent", pos1, 0),
                   (try_end),
                   (get_player_agent_no, ":player_agent"),
                   (agent_get_position, pos1, ":player_agent"),
                   (entry_point_get_position,pos2,2),
                   (get_distance_between_positions, ":cur_distance", pos1, pos2),
                   (le, ":cur_distance", 200),
                   (scene_prop_get_instance, ":door_object", "spr_tutorial_door_b", 0),
                   (prop_instance_get_position, pos1, ":door_object"),
                   (position_rotate_z, pos1, -90),
                   (prop_instance_animate_to_position, ":door_object", pos1, 150),
                   (val_add, "$tutorial_3_state", 1),
                 (else_try),
                   (eq, "$tutorial_3_state", 1),
                   (try_begin),
                     (eq, "$tutorial_3_msg_2_displayed", 0),
                     (assign, "$tutorial_3_msg_2_displayed", 1),
                     (tutorial_message, "str_tutorial_3_2_msg_2"),
                     (play_sound, "snd_tutorial_1"),
                   (try_end),
                   (scene_prop_get_instance, ":barrier_object", "spr_barrier_4m", 0),
                   (prop_instance_get_position, pos1, ":barrier_object"),
                   (get_player_agent_no, ":player_agent"),
                   (agent_get_position, pos2, ":player_agent"),
                   (position_is_behind_position, pos2, pos1),
                   (scene_prop_get_instance, ":door_object", "spr_tutorial_door_b", 0),
                   (prop_instance_get_position, pos1, ":door_object"),
                   (position_rotate_z, pos1, 90),
                   (prop_instance_animate_to_position, ":door_object", pos1, 150),
                   (call_script, "script_cf_get_first_agent_with_troop_id", "trp_tutorial_maceman"),
                   (agent_clear_scripted_mode, reg0),
                   (val_add, "$tutorial_3_state", 1),
                 (else_try),
                   (eq, "$tutorial_3_state", 2),
                   (call_script, "script_cf_get_first_agent_with_troop_id", "trp_tutorial_maceman"),
                   (neg|agent_is_alive, reg0),
                   (scene_prop_get_instance, ":door_object", "spr_tutorial_door_b", 1),
                   (prop_instance_get_position, pos1, ":door_object"),
                   (position_rotate_z, pos1, -90),
                   (prop_instance_animate_to_position, ":door_object", pos1, 150),
                   (scene_prop_get_instance, ":door_object", "spr_tutorial_door_b", 3),
                   (prop_instance_get_position, pos1, ":door_object"),
                   (position_rotate_z, pos1, -90),
                   (prop_instance_animate_to_position, ":door_object", pos1, 150),
                   (val_add, "$tutorial_3_state", 1),
                 (else_try),
                   (eq, "$tutorial_3_state", 3),
                   (try_begin),
                     (eq, "$tutorial_3_msg_3_displayed", 0),
                     (assign, "$tutorial_3_msg_3_displayed", 1),
                     (tutorial_message, "str_tutorial_3_2_msg_3"),
                     (play_sound, "snd_tutorial_1"),
                   (try_end),                 
                   (scene_prop_get_instance, ":barrier_object", "spr_barrier_4m", 1),
                   (prop_instance_get_position, pos1, ":barrier_object"),
                   (get_player_agent_no, ":player_agent"),
                   (agent_get_position, pos2, ":player_agent"),
                   (position_is_behind_position, pos2, pos1),
                   (scene_prop_get_instance, ":door_object", "spr_tutorial_door_b", 1),
                   (prop_instance_get_position, pos1, ":door_object"),
                   (position_rotate_z, pos1, 90),
                   (prop_instance_animate_to_position, ":door_object", pos1, 150),
                   (call_script, "script_cf_get_first_agent_with_troop_id", "trp_tutorial_swordsman"),
                   (agent_clear_scripted_mode, reg0),
                   (val_add, "$tutorial_3_state", 1),
                 (else_try),
                   (eq, "$tutorial_3_state", 4),
                   (try_begin),
                     (eq, "$tutorial_3_msg_4_displayed", 0),
                     (assign, "$tutorial_3_msg_4_displayed", 1),
                     (tutorial_message, "str_tutorial_3_2_msg_4"),
                     (play_sound, "snd_tutorial_1"),
                   (try_end),
                   (call_script, "script_cf_get_first_agent_with_troop_id", "trp_tutorial_swordsman"),
                   (neg|agent_is_alive, reg0),
                   (val_add, "$tutorial_3_state", 1),
                 (else_try),
                   (eq, "$tutorial_3_state", 5),
                   (eq, "$tutorial_3_msg_5_displayed", 0),
                   (assign, "$tutorial_3_msg_5_displayed", 1),
                   (tutorial_message, "str_tutorial_3_2_msg_5"),
                   (play_sound, "snd_tutorial_2"),
                   (assign, "$tutorial_3_finished", 1),
                 (else_try),
                   (gt, "$tutorial_3_state", 30),
                   (tutorial_message, "str_tutorial_failed"),
                 (try_end),
                 ], []),

      
    ],
  ),

  (
    "tutorial_4",mtf_arena_fight,-1,
    "You enter the training ground.",
    [
        (0,mtef_leader_only|mtef_team_0,af_override_everything,0,1,[itm_tutorial_sword,itm_tutorial_short_bow,itm_tutorial_arrows,itm_leather_jerkin,itm_leather_boots]), #af_override_weapons
     ],
    [
      (ti_tab_pressed, 0, 0, [],
       [(try_begin),
         (lt, "$tutorial_4_state", 11),
         (question_box,"str_do_you_wish_to_leave_tutorial"),
        (else_try),
          (finish_mission,0),
        (try_end),
        ]),
      (ti_question_answered, 0, 0, [],
       [(store_trigger_param_1,":answer"),
        (eq,":answer",0),
        (finish_mission,0),
        ]),
      (ti_inventory_key_pressed, 0, 0, [(display_message,"str_cant_use_inventory_tutorial")], []),

      (ti_before_mission_start, 0, 0, [],
       [
         (scene_set_day_time, 13),
         ]),

      (0, 0, ti_once, [
      	               (tutorial_message_set_size, 17, 17),
	                   (tutorial_message_set_position, 500, 650),
                       (tutorial_message_set_center_justify, 0),

                       (assign, "$tutorial_4_state", 0),
                       (assign, "$tutorial_4_msg_1_displayed", 0),
                       (assign, "$tutorial_4_msg_2_displayed", 0),
                       (assign, "$tutorial_4_msg_3_displayed", 0),
                       (assign, "$tutorial_4_msg_4_displayed", 0),
                       (assign, "$tutorial_4_msg_5_displayed", 0),
                       (assign, "$tutorial_4_msg_6_displayed", 0),
                       (assign, "$tutorial_4_msg_7_displayed", 0),
                       ], []),

      (0, 0, 0, [(try_begin),
                   (eq, "$tutorial_4_state", 0),
                   (try_begin),
                     (eq, "$tutorial_4_msg_1_displayed", 0),
                     (store_mission_timer_a, ":cur_time"),
                     (gt, ":cur_time", 0),
                     (assign, "$tutorial_4_msg_1_displayed", 1),
                     (tutorial_message, "str_tutorial_4_msg_1"),
                     (entry_point_get_position, pos1, 1),
                     (set_spawn_position, 1),
                     (spawn_horse, "itm_tutorial_saddle_horse"),
                     (assign, "$tutorial_num_total_dummies_destroyed", 0),
                   (try_end),
                   (get_player_agent_no, ":player_agent"),
                   (agent_get_horse, ":horse_agent", ":player_agent"),
                   (ge, ":horse_agent", 0),
                   (val_add, "$tutorial_4_state", 1),
                   (entry_point_get_position, pos1, 2),
                   (scene_prop_get_instance, ":flag_object", "spr_tutorial_flag_yellow", 0),
                   (prop_instance_animate_to_position, ":flag_object", pos1, 1),
                 (else_try),
                   (eq, "$tutorial_4_state", 1),
                   (try_begin),
                     (eq, "$tutorial_4_msg_2_displayed", 0),
                     (assign, "$tutorial_4_msg_2_displayed", 1),
                     (tutorial_message, "str_tutorial_4_msg_2"),
                     (play_sound, "snd_tutorial_1"),
                   (try_end),
                   (get_player_agent_no, ":player_agent"),
                   (agent_get_position, pos1, ":player_agent"),
                   (entry_point_get_position, pos2, 2),
                   (get_distance_between_positions, ":cur_distance", pos1, pos2),
                   (le, ":cur_distance", 200),
                   (val_add, "$tutorial_4_state", 1),
                   (entry_point_get_position, pos1, 3),
                   (scene_prop_get_instance, ":flag_object", "spr_tutorial_flag_yellow", 0),
                   (prop_instance_animate_to_position, ":flag_object", pos1, 1),
                 (else_try),
                   (eq, "$tutorial_4_state", 2),
                   (get_player_agent_no, ":player_agent"),
                   (agent_get_position, pos1, ":player_agent"),
                   (entry_point_get_position, pos2, 3),
                   (get_distance_between_positions, ":cur_distance", pos1, pos2),
                   (le, ":cur_distance", 200),
                   (val_add, "$tutorial_4_state", 1),
                   (entry_point_get_position, pos1, 4),
                   (scene_prop_get_instance, ":flag_object", "spr_tutorial_flag_yellow", 0),
                   (prop_instance_animate_to_position, ":flag_object", pos1, 1),
                 (else_try),
                   (eq, "$tutorial_4_state", 3),
                   (get_player_agent_no, ":player_agent"),
                   (agent_get_position, pos1, ":player_agent"),
                   (entry_point_get_position, pos2, 4),
                   (get_distance_between_positions, ":cur_distance", pos1, pos2),
                   (le, ":cur_distance", 200),
                   (val_add, "$tutorial_4_state", 1),
                   (entry_point_get_position, pos1, 5),
                   (scene_prop_get_instance, ":flag_object", "spr_tutorial_flag_yellow", 0),
                   (prop_instance_animate_to_position, ":flag_object", pos1, 1),
                 (else_try),
                   (eq, "$tutorial_4_state", 4),
                   (get_player_agent_no, ":player_agent"),
                   (agent_get_position, pos1, ":player_agent"),
                   (entry_point_get_position, pos2, 5),
                   (get_distance_between_positions, ":cur_distance", pos1, pos2),
                   (le, ":cur_distance", 200),
                   (val_add, "$tutorial_4_state", 1),
                   (entry_point_get_position, pos1, 6),
                   (scene_prop_get_instance, ":flag_object", "spr_tutorial_flag_yellow", 0),
                   (prop_instance_animate_to_position, ":flag_object", pos1, 1),
                 (else_try),
                   (eq, "$tutorial_4_state", 5),
                   (get_player_agent_no, ":player_agent"),
                   (agent_get_position, pos1, ":player_agent"),
                   (entry_point_get_position, pos2, 6),
                   (get_distance_between_positions, ":cur_distance", pos1, pos2),
                   (le, ":cur_distance", 200),
                   (val_add, "$tutorial_4_state", 1),
                   (entry_point_get_position, pos1, 1),
                   (scene_prop_get_instance, ":flag_object", "spr_tutorial_flag_yellow", 0),
                   (prop_instance_animate_to_position, ":flag_object", pos1, 1),
                 (else_try),
                   (eq, "$tutorial_4_state", 6),
                   (get_player_agent_no, ":player_agent"),
                   (agent_get_position, pos1, ":player_agent"),
                   (entry_point_get_position, pos2, 1),
                   (get_distance_between_positions, ":cur_distance", pos1, pos2),
                   (le, ":cur_distance", 200),
                   (val_add, "$tutorial_4_state", 1),
                   (entry_point_get_position, pos1, 7),
                   (scene_prop_get_instance, ":flag_object", "spr_tutorial_flag_yellow", 0),
                   (prop_instance_animate_to_position, ":flag_object", pos1, 1),
                 (else_try),
                   (eq, "$tutorial_4_state", 7),
                   (try_begin),
                     (eq, "$tutorial_4_msg_3_displayed", 0),
                     (assign, "$tutorial_4_msg_3_displayed", 1),
                     (tutorial_message, "str_tutorial_4_msg_3"),
                     (play_sound, "snd_tutorial_1"),
                   (try_end),
                   (get_player_agent_no, ":player_agent"),
                   (agent_get_position, pos1, ":player_agent"),
                   (entry_point_get_position, pos2, 7),
                   (get_distance_between_positions, ":cur_distance", pos1, pos2),
                   (le, ":cur_distance", 200),
                   (val_add, "$tutorial_4_state", 1),
                   (entry_point_get_position, pos1, 20),
                   (scene_prop_get_instance, ":flag_object", "spr_tutorial_flag_yellow", 0),
                   (prop_instance_animate_to_position, ":flag_object", pos1, 1),
                 (else_try),
                   (eq, "$tutorial_4_state", 8),
                   (try_begin),
                     (eq, "$tutorial_4_msg_4_displayed", 0),
                     (assign, "$tutorial_4_msg_4_displayed", 1),
                     (tutorial_message, "str_tutorial_4_msg_4"),
                     (play_sound, "snd_tutorial_1"),
                   (try_end),
                   (ge, "$tutorial_num_total_dummies_destroyed", 2),
                   (val_add, "$tutorial_4_state", 1),
                   (entry_point_get_position, pos1, 8),
                   (scene_prop_get_instance, ":flag_object", "spr_tutorial_flag_yellow", 0),
                   (prop_instance_animate_to_position, ":flag_object", pos1, 1),
                 (else_try),
                   (eq, "$tutorial_4_state", 9),
                   (try_begin),
                     (eq, "$tutorial_4_msg_5_displayed", 0),
                     (assign, "$tutorial_4_msg_5_displayed", 1),
                     (tutorial_message, "str_tutorial_4_msg_5"),
                     (play_sound, "snd_tutorial_1"),
                   (try_end),
                   (get_player_agent_no, ":player_agent"),
                   (agent_get_position, pos1, ":player_agent"),
                   (entry_point_get_position, pos2, 8),
                   (get_distance_between_positions, ":cur_distance", pos1, pos2),
                   (le, ":cur_distance", 200),
                   (val_add, "$tutorial_4_state", 1),
                   (entry_point_get_position, pos1, 20),
                   (scene_prop_get_instance, ":flag_object", "spr_tutorial_flag_yellow", 0),
                   (prop_instance_animate_to_position, ":flag_object", pos1, 1),
                 (else_try),
                   (eq, "$tutorial_4_state", 10),
                   (try_begin),
                     (eq, "$tutorial_4_msg_6_displayed", 0),
                     (assign, "$tutorial_4_msg_6_displayed", 1),
                     (tutorial_message, "str_tutorial_4_msg_6"),
                     (play_sound, "snd_tutorial_1"),
                     (assign, "$g_last_archery_point_earned", 0),
                     (assign, "$tutorial_num_arrows_hit", 0),
                   (try_end),
                   (try_begin),
                     (get_player_agent_no, ":player_agent"),
                     (agent_get_ammo, ":cur_ammo", ":player_agent"),
                     (le, ":cur_ammo", 0),
                     (agent_refill_ammo, ":player_agent"),
                     (tutorial_message, "str_tutorial_ammo_refilled"),
                   (try_end),
                   (gt, "$g_last_archery_point_earned", 0),
                   (assign, "$g_last_archery_point_earned", 0),
                   (val_add, "$tutorial_num_arrows_hit", 1),
                   (gt, "$tutorial_num_arrows_hit", 2),
                   (val_add, "$tutorial_4_state", 1),
                 (else_try),
                   (eq, "$tutorial_4_state", 11),
                   (eq, "$tutorial_4_msg_7_displayed", 0),
                   (assign, "$tutorial_4_msg_7_displayed", 1),
                   (tutorial_message, "str_tutorial_4_msg_7"),
                   (play_sound, "snd_tutorial_2"),
                   (assign, "$tutorial_4_finished", 1),
                 (try_end),
                 ], []),
    ],
  ),

  (
    "tutorial_5",mtf_arena_fight,-1,
    "You enter the training ground.",
    [
        (0,mtef_visitor_source|mtef_team_0,af_override_everything,0,1,[itm_tutorial_sword,itm_tutorial_shield,itm_tutorial_short_bow,itm_tutorial_arrows,itm_tutorial_saddle_horse,itm_leather_jerkin,itm_leather_boots]),
        (1,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
        (2,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
        (3,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
        (4,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
        (8,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
        (9,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
        (10,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
        (13,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
        (14,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
        (15,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
        (16,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
     ],
    [
      (ti_tab_pressed, 0, 0, [],
       [(try_begin),
         (lt, "$tutorial_5_state", 5),
         (question_box,"str_do_you_wish_to_leave_tutorial"),
        (else_try),
          (finish_mission,0),
        (try_end),
        ]),
      (ti_question_answered, 0, 0, [],
       [(store_trigger_param_1,":answer"),
        (eq,":answer",0),
        (finish_mission,0),
        ]),
      (ti_inventory_key_pressed, 0, 0, [(display_message,"str_cant_use_inventory_tutorial")], []),


      (0, 0, ti_once, [
          (store_mission_timer_a, ":cur_time"),
          (gt, ":cur_time", 2),
          (main_hero_fallen),
          (assign, "$tutorial_5_state", 100),
        ], []),

      (0, 0, ti_once, [
      	               (tutorial_message_set_size, 17, 17),
	                   (tutorial_message_set_position, 500, 650),
                       (tutorial_message_set_center_justify, 0),

                       (assign, "$tutorial_5_state", 0),
                       (assign, "$tutorial_5_msg_1_displayed", 0),
                       (assign, "$tutorial_5_msg_2_displayed", 0),
                       (assign, "$tutorial_5_msg_3_displayed", 0),
                       (assign, "$tutorial_5_msg_4_displayed", 0),
                       (assign, "$tutorial_5_msg_5_displayed", 0),
                       (assign, "$tutorial_5_msg_6_displayed", 0),
                       ], []),

      (0, 0, ti_once, [(set_show_messages, 0),
                       (team_give_order, 0, grc_everyone, mordr_stand_ground),
                       (set_show_messages, 1),
                       (store_mission_timer_a, ":cur_time"),
                       (gt, ":cur_time", 3),
                       ], []),

      (0, 0, 0, [(call_script, "script_cf_turn_windmill_fans", 0)], []),
      
      (0, 0, 0, [(try_begin),
                   (eq, "$tutorial_5_state", 0),
                   (try_begin),
                     (eq, "$tutorial_5_msg_1_displayed", 0),
                     (store_mission_timer_a, ":cur_time"),
                     (gt, ":cur_time", 0),
                     (assign, "$tutorial_5_msg_1_displayed", 1),
                     (tutorial_message, "str_tutorial_5_msg_1"),
                     (entry_point_get_position, pos1, 5),
                     (scene_prop_get_instance, ":flag_object", "spr_tutorial_flag_yellow", 0),
                     (prop_instance_animate_to_position, ":flag_object", pos1, 1),
                   (try_end),
                   (call_script, "script_cf_team_get_average_position_of_agents_with_type_to_pos1", 0, grc_infantry),
                   (entry_point_get_position, pos2, 5),
                   (get_distance_between_positions, ":cur_distance", pos1, pos2),
                   (le, ":cur_distance", 1000),
                   (val_add, "$tutorial_5_state", 1),
                   (entry_point_get_position, pos1, 6),
                   (scene_prop_get_instance, ":flag_object", "spr_tutorial_flag_red", 0),
                   (prop_instance_animate_to_position, ":flag_object", pos1, 1),
                 (else_try),
                   (eq, "$tutorial_5_state", 1),
                   (try_begin),
                     (eq, "$tutorial_5_msg_2_displayed", 0),
                     (assign, "$tutorial_5_msg_2_displayed", 1),
                     (tutorial_message, "str_tutorial_5_msg_2"),
                     (play_sound, "snd_tutorial_1"),
                   (try_end),
                   (call_script, "script_cf_team_get_average_position_of_agents_with_type_to_pos1", 0, grc_infantry),
                   (entry_point_get_position, pos2, 5),
                   (get_distance_between_positions, ":cur_distance", pos1, pos2),
                   (le, ":cur_distance", 1000),
                   (get_player_agent_no, ":player_agent"),
                   (agent_get_position, pos1, ":player_agent"),
                   (entry_point_get_position, pos2, 6),
                   (get_distance_between_positions, ":cur_distance", pos1, pos2),
                   (le, ":cur_distance", 500),
                   (val_add, "$tutorial_5_state", 1),
                   (entry_point_get_position, pos1, 7),
                   (scene_prop_get_instance, ":flag_object", "spr_tutorial_flag_yellow", 0),
                   (prop_instance_animate_to_position, ":flag_object", pos1, 1),
                   (entry_point_get_position, pos1, 30),
                   (scene_prop_get_instance, ":flag_object", "spr_tutorial_flag_red", 0),
                   (prop_instance_animate_to_position, ":flag_object", pos1, 1),
                 (else_try),
                   (eq, "$tutorial_5_state", 2),
                   (try_begin),
                     (eq, "$tutorial_5_msg_3_displayed", 0),
                     (assign, "$tutorial_5_msg_3_displayed", 1),
                     (tutorial_message, "str_tutorial_5_msg_3"),
                     (play_sound, "snd_tutorial_1"),
                   (try_end),
                   (get_player_agent_no, ":player_agent"),
                   (agent_get_position, pos1, ":player_agent"),
                   (entry_point_get_position, pos2, 7),
                   (get_distance_between_positions, ":cur_distance", pos1, pos2),
                   (le, ":cur_distance", 500),
                   (val_add, "$tutorial_5_state", 1),
                   (modify_visitors_at_site,"scn_tutorial_5"),
                   (reset_visitors),
                   (set_visitor,5,"trp_vaegir_archer"),
                   (set_visitor,6,"trp_vaegir_archer"),
                   (set_visitor,7,"trp_vaegir_archer"),
                   (entry_point_get_position, pos1, 11),
                   (scene_prop_get_instance, ":flag_object", "spr_tutorial_flag_yellow", 0),
                   (prop_instance_animate_to_position, ":flag_object", pos1, 1),
                   (entry_point_get_position, pos1, 12),
                   (scene_prop_get_instance, ":flag_object", "spr_tutorial_flag_red", 0),
                   (prop_instance_animate_to_position, ":flag_object", pos1, 1),
                   (set_show_messages, 0),
                   (team_give_order, 0, grc_archers, mordr_stand_ground),
                   (set_show_messages, 1),
                 (else_try),
                   (eq, "$tutorial_5_state", 3),
                   (try_begin),
                     (eq, "$tutorial_5_msg_4_displayed", 0),
                     (assign, "$tutorial_5_msg_4_displayed", 1),
                     (tutorial_message, "str_tutorial_5_msg_4"),
                     (play_sound, "snd_tutorial_1"),
                   (try_end),
                   (call_script, "script_cf_team_get_average_position_of_agents_with_type_to_pos1", 0, grc_archers),
                   (entry_point_get_position, pos2, 11),
                   (get_distance_between_positions, ":cur_distance", pos1, pos2),
                   (le, ":cur_distance", 1000),
                   (call_script, "script_cf_team_get_average_position_of_agents_with_type_to_pos1", 0, grc_infantry),
                   (entry_point_get_position, pos2, 12),
                   (get_distance_between_positions, ":cur_distance", pos1, pos2),
                   (le, ":cur_distance", 1000),
                   (val_add, "$tutorial_5_state", 1),
                   (entry_point_get_position, pos1, 30),
                   (scene_prop_get_instance, ":flag_object", "spr_tutorial_flag_yellow", 0),
                   (prop_instance_animate_to_position, ":flag_object", pos1, 1),
                   (scene_prop_get_instance, ":flag_object", "spr_tutorial_flag_red", 0),
                   (prop_instance_animate_to_position, ":flag_object", pos1, 1),
                   (modify_visitors_at_site,"scn_tutorial_5"),
                   (reset_visitors),
                   (set_visitor,8,"trp_bandit"),
                   (set_visitor,9,"trp_bandit"),
                   (set_visitor,10,"trp_bandit"),
                   (set_visitor,11,"trp_bandit"),
                   (team_give_order, 1, grc_everyone, mordr_charge),
                 (else_try),
                   (eq, "$tutorial_5_state", 4),
                   (try_begin),
                     (eq, "$tutorial_5_msg_5_displayed", 0),
                     (assign, "$tutorial_5_msg_5_displayed", 1),
                     (tutorial_message, "str_tutorial_5_msg_5"),
                     (play_sound, "snd_tutorial_1"),
                   (try_end),
                   (assign, ":enemy_count", 0),
                   (try_for_agents, ":cur_agent"),
                     (agent_is_human, ":cur_agent"),
                     (agent_is_alive, ":cur_agent"),
                     (agent_get_team, ":cur_team", ":cur_agent"),
                     (eq, ":cur_team", 1),
                     (val_add, ":enemy_count", 1),
                   (try_end),
                   (eq, ":enemy_count", 0),
                   (val_add, "$tutorial_5_state", 1),
                 (else_try),
                   (eq, "$tutorial_5_state", 5),
                   (eq, "$tutorial_5_msg_6_displayed", 0),
                   (assign, "$tutorial_5_msg_6_displayed", 1),
                   (tutorial_message, "str_tutorial_5_msg_6"),
                   (play_sound, "snd_tutorial_2"),
                   (assign, "$tutorial_5_finished", 1),
                 (else_try),
                   (gt, "$tutorial_5_state", 30),
                   (tutorial_message, "str_tutorial_failed"),
                   (entry_point_get_position, pos1, 30),
                   (scene_prop_get_instance, ":flag_object", "spr_tutorial_flag_yellow", 0),
                   (prop_instance_animate_to_position, ":flag_object", pos1, 1),
                   (scene_prop_get_instance, ":flag_object", "spr_tutorial_flag_red", 0),
                   (prop_instance_animate_to_position, ":flag_object", pos1, 1),
                 (try_end),
                 ], []),
    ],
  ),

  (
    "quick_battle_battle",mtf_battle_mode,-1,
    "You lead your men to battle.",
    [
      (0,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (1,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (2,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (3,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (4,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (5,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (6,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (7,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),

      (8,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (9,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (10,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (11,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (12,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (13,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (14,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (15,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),

      (16,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (17,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (18,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (19,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (20,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (21,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (22,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (23,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),

      (24,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (25,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (26,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (27,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (28,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (29,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (30,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (31,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
     ],
    [
      common_custom_battle_tab_press,
      common_custom_battle_question_answered,
      common_inventory_not_available,

      (ti_before_mission_start, 0, 0, [],
       [
         (scene_set_day_time, 15),
         ]),

      common_battle_init_banner,
      
      (0, 0, ti_once, [],
        [
          (assign, "$g_battle_result", 0),
          (call_script, "script_combat_music_set_situation_with_culture"),
         ]),

      common_music_situation_update,
      custom_battle_check_victory_condition,
      common_battle_victory_display,
      custom_battle_check_defeat_condition,
    ],
  ),

  (
    "quick_battle_siege", mtf_battle_mode,-1,
    "You lead your men to battle.",
    [
      (0,mtef_visitor_source|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),
      (1,mtef_visitor_source|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),
      (2,mtef_visitor_source|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),
      (3,mtef_visitor_source|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),
      (4,mtef_visitor_source|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),
      (5,mtef_visitor_source|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),
      (6,mtef_visitor_source|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),
      (7,mtef_visitor_source|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),

      (8,mtef_visitor_source|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),
      (9,mtef_visitor_source|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),
      (10,mtef_visitor_source|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),
      (11,mtef_visitor_source|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),
      (12,mtef_visitor_source|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),
      (13,mtef_visitor_source|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),
      (14,mtef_visitor_source|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),
      (15,mtef_visitor_source|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),

      (16,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
      (17,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
      (18,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
      (19,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
      (20,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
      (21,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
      (22,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
      (23,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),

      (24,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
      (25,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
      (26,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
      (27,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
      (28,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
      (29,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
      (30,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
      (31,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),

      (32,mtef_visitor_source|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),
      (33,mtef_visitor_source|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),
      (34,mtef_visitor_source|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),
      (35,mtef_visitor_source|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),
      (36,mtef_visitor_source|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),
      (37,mtef_visitor_source|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),
      (38,mtef_visitor_source|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),
      (39,mtef_visitor_source|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),

      (40,mtef_visitor_source|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),
      (41,mtef_visitor_source|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),
      (42,mtef_visitor_source|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),
      (43,mtef_visitor_source|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),
      (44,mtef_visitor_source|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),
      (45,mtef_visitor_source|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),
      (46,mtef_visitor_source|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),
      (47,mtef_visitor_source|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),
     ],
    [
      common_battle_mission_start,
      common_battle_init_banner,

      (0, 0, ti_once,
       [
         (assign, "$defender_team", 0),
         (assign, "$attacker_team", 1),
         (assign, "$defender_team_2", 2),
         (assign, "$attacker_team_2", 3),
         ], []),

      (ti_before_mission_start, 0, 0, [],
       [
         (scene_set_day_time, 15),
         ]),

      common_custom_battle_tab_press,
      common_custom_battle_question_answered,
      common_inventory_not_available,
      common_custom_siege_init,
      common_music_situation_update,
      custom_battle_check_victory_condition,
      common_battle_victory_display,
      custom_battle_check_defeat_condition,
      common_siege_attacker_do_not_stall,
      common_siege_refill_ammo,
      common_siege_init_ai_and_belfry,
      common_siege_move_belfry,
      common_siege_rotate_belfry,
      common_siege_assign_men_to_belfry,
      common_siege_ai_trigger_init_2,
      ],
    ),
##
##  (
##    "quick_battle_siege_offense",mtf_battle_mode,-1,
##    "You lead your men to battle.",
##    [
##      (0,mtef_visitor_source|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),
##      (1,mtef_visitor_source|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),
##      (2,mtef_visitor_source|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),
##      (3,mtef_visitor_source|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),
##      (4,mtef_visitor_source|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),
##      (5,mtef_visitor_source|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),
##      (6,mtef_visitor_source|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),
##      (7,mtef_visitor_source|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),
##
##      (8,mtef_visitor_source|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),
##      (9,mtef_visitor_source|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),
##      (10,mtef_visitor_source|mtef_team_0,af_override_horse,aif_start_alarmed,1,[]),
##
##      (11,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
##      (12,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
##      (13,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
##      (14,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
##      (15,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
##      (40,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
##      (41,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
##      (42,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
##      (43,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
##      (44,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
##      (45,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
##      (46,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
##      (47,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
##
##     ],
##    [
##      common_custom_battle_tab_press,
##      common_battle_init_banner,
##      common_custom_battle_question_answered,
##      common_custom_siege_init,
##      common_inventory_not_available,
##      common_music_situation_update,
##      custom_battle_check_victory_condition,
##      common_battle_victory_display,
##      custom_battle_check_defeat_condition,
##      
##      (0, 0, ti_once,
##       [
##         (assign, "$defender_team", 0),
##         (assign, "$attacker_team", 1),
##         (assign, "$defender_team_2", 2),
##         (assign, "$attacker_team_2", 3),
##         ], []),
##
##      common_siege_ai_trigger_init_2,
##      common_siege_attacker_do_not_stall,
##      common_siege_refill_ammo,
##      common_siege_init_ai_and_belfry,
##      common_siege_move_belfry,
##      common_siege_rotate_belfry,
##      common_siege_assign_men_to_belfry,
##    ],
##  ),

    (
    "multiplayer_dm",mtf_battle_mode,-1, #deathmatch mode
    "You lead your men to battle.",
    [
      (0,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (1,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (2,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (3,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (4,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (5,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (6,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (7,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),

      (8,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (9,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (10,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (11,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (12,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (13,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (14,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (15,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),

      (16,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (17,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (18,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (19,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (20,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (21,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (22,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (23,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),

      (24,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (25,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (26,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (27,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (28,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (29,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (30,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (31,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),

      (32,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (33,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (34,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (35,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (36,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (37,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (38,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (39,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),

      (40,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (41,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (42,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (43,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (44,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (45,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (46,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (47,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),

      (48,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (49,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (50,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (51,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (52,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (53,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (54,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (55,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),

      (56,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (57,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (58,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (59,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (60,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (61,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (62,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (63,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
     ],
    [
      #multiplayer_server_check_belfry_movement,      
     
      multiplayer_server_check_polls,

      (ti_on_agent_spawn, 0, 0, [],
       [
         (store_trigger_param_1, ":agent_no"),
         (call_script, "script_multiplayer_server_on_agent_spawn_common", ":agent_no"),
         ]),

      (ti_server_player_joined, 0, 0, [],
       [
         (store_trigger_param_1, ":player_no"),
         (call_script, "script_multiplayer_server_player_joined_common", ":player_no"),
         ]),

      (ti_before_mission_start, 0, 0, [],
       [
         (assign, "$g_multiplayer_game_type", multiplayer_game_type_deathmatch),
         (call_script, "script_multiplayer_server_before_mission_start_common"),
         
         (multiplayer_make_everyone_enemy),

         (call_script, "script_multiplayer_init_mission_variables"),
         (call_script, "script_multiplayer_remove_destroy_mod_targets"),
         (call_script, "script_multiplayer_remove_headquarters_flags"), # close this line and open map in deathmatch mod and use all ladders firstly 
         ]),                                                            # to be able to edit maps without damaging any headquarters flags ext. 

      (ti_after_mission_start, 0, 0, [], 
       [
         (set_spawn_effector_scene_prop_kind, 0, -1), #during this mission, agents of "team 0" will try to spawn around scene props with kind equal to -1(no effector for this mod)
         (set_spawn_effector_scene_prop_kind, 1, -1), #during this mission, agents of "team 1" will try to spawn around scene props with kind equal to -1(no effector for this mod)

         (call_script, "script_initialize_all_scene_prop_slots"),
         
         (call_script, "script_multiplayer_move_moveable_objects_initial_positions"),

         (assign, "$g_multiplayer_ready_for_spawning_agent", 1),
         ]),

      (ti_on_multiplayer_mission_end, 0, 0, [],
       [
         #ELITE_WARRIOR achievement
         (try_begin),
           (multiplayer_get_my_player, ":my_player_no"),
           (is_between, ":my_player_no", 0, multiplayer_max_possible_player_id),
           (player_get_team_no, ":my_player_team", ":my_player_no"),
           (lt, ":my_player_team", multi_team_spectator),
           (player_get_kill_count, ":kill_count", ":my_player_no"),
           (player_get_death_count, ":death_count", ":my_player_no"),
           (store_mul, ":my_score_plus_death", ":kill_count", 1000),
           (val_sub, ":my_score_plus_death", ":death_count"),
           (assign, ":continue", 1),
           (get_max_players, ":num_players"),
           (assign, ":end_cond", ":num_players"),
           (try_for_range, ":player_no", 0, ":end_cond"),
             (player_is_active, ":player_no"),
             (player_get_team_no, ":player_team", ":player_no"),
             (this_or_next|eq, ":player_team", 0),
             (eq, ":player_team", 1),
             (player_get_kill_count, ":kill_count", ":player_no"),
             (player_get_death_count, ":death_count", ":player_no"), #get_death_count
             (store_mul, ":player_score_plus_death", ":kill_count", 1000),
             (val_sub, ":player_score_plus_death", ":death_count"),
             (gt, ":player_score_plus_death", ":my_score_plus_death"),
             (assign, ":continue", 0),
             (assign, ":end_cond", 0), #break
           (try_end),
           (eq, ":continue", 1),
           (unlock_achievement, ACHIEVEMENT_ELITE_WARRIOR),
         (try_end),
         #ELITE_WARRIOR achievement end

         (call_script, "script_multiplayer_event_mission_end"),

         (assign, "$g_multiplayer_stats_chart_opened_manually", 0),
         (start_presentation, "prsnt_multiplayer_stats_chart_deathmatch"),
         ]),

      (ti_on_agent_killed_or_wounded, 0, 0, [],
       [
         (store_trigger_param_1, ":dead_agent_no"), 
         (store_trigger_param_2, ":killer_agent_no"),
         (call_script, "script_multiplayer_server_on_agent_killed_or_wounded_common", ":dead_agent_no", ":killer_agent_no"),
         ]),
         
      #  Tests for set_shader_param_ operations
      #   (1, 0, 0, [],
      # [
      #  (str_store_string, s0, "@user_value_int"),
      #  (assign, ":int_param", 100),
      #  (assign, ":float_param", 100),
      #  (set_fixed_point_multiplier, 100),
      #  (set_shader_param_int, s0, ":int_param"),
      #  (set_shader_param_float, "@user_value_float", ":float_param"),
      #  (set_shader_param_float4, "@user_value_float4", 10, 20, 30, 40),
      #  (set_shader_param_float4x4, "@user_value_float4x4", 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120),
      #   ]),
      
      (1, 0, 0, [],
       [
         (multiplayer_is_server),
         (get_max_players, ":num_players"),
         (try_for_range, ":player_no", 0, ":num_players"),
           (player_is_active, ":player_no"),
           (neg|player_is_busy_with_menus, ":player_no"),

           (player_get_team_no, ":player_team", ":player_no"), #if player is currently spectator do not spawn his agent
           (lt, ":player_team", multi_team_spectator),

           (player_get_troop_id, ":player_troop", ":player_no"), #if troop is not selected do not spawn his agent
           (ge, ":player_troop", 0),

           (player_get_agent_id, ":player_agent", ":player_no"),
           (assign, ":spawn_new", 0),
           (try_begin),
             (player_get_slot, ":player_first_spawn", ":player_no", slot_player_first_spawn),
             (eq, ":player_first_spawn", 1),
             (assign, ":spawn_new", 1),
             (player_set_slot, ":player_no", slot_player_first_spawn, 0),
           (else_try),
             (try_begin),
               (lt, ":player_agent", 0),
               (assign, ":spawn_new", 1),
             (else_try),
               (neg|agent_is_alive, ":player_agent"),
               (agent_get_time_elapsed_since_removed, ":elapsed_time", ":player_agent"),
               (gt, ":elapsed_time", "$g_multiplayer_respawn_period"),
               (assign, ":spawn_new", 1),
             (try_end),             
           (try_end),
           (eq, ":spawn_new", 1),
           (call_script, "script_multiplayer_buy_agent_equipment", ":player_no"),

           (troop_get_inventory_slot, ":has_item", ":player_troop", ek_horse),
           (try_begin),
             (ge, ":has_item", 0),
             (assign, ":is_horseman", 1),
           (else_try),
             (assign, ":is_horseman", 0),
           (try_end),
         
           (call_script, "script_multiplayer_find_spawn_point", ":player_team", 0, ":is_horseman"), 
           (player_spawn_new_agent, ":player_no", reg0),
         (try_end),
         ]),

      (1, 0, 0, [], #do this in every new frame, but not at the same time
       [
         (multiplayer_is_server),
         (store_mission_timer_a, ":mission_timer"),
         (ge, ":mission_timer", 2),
         (assign, ":team_1_count", 0),
         (assign, ":team_2_count", 0),
         (try_for_agents, ":cur_agent"),
           (agent_is_non_player, ":cur_agent"),
           (agent_is_human, ":cur_agent"),
           (assign, ":will_be_counted", 0),
           (try_begin),
             (agent_is_alive, ":cur_agent"),
             (assign, ":will_be_counted", 1), #alive so will be counted
           (else_try),
             (agent_get_time_elapsed_since_removed, ":elapsed_time", ":cur_agent"),
             (le, ":elapsed_time", "$g_multiplayer_respawn_period"),
             (assign, ":will_be_counted", 1), 
           (try_end),
           (eq, ":will_be_counted", 1),
           (agent_get_team, ":cur_team", ":cur_agent"),
           (try_begin),
             (eq, ":cur_team", 0),
             (val_add, ":team_1_count", 1),
           (else_try),
             (eq, ":cur_team", 1),
             (val_add, ":team_2_count", 1),
           (try_end),
         (try_end),
         (store_sub, "$g_multiplayer_num_bots_required_team_1", "$g_multiplayer_num_bots_team_1", ":team_1_count"),
         (store_sub, "$g_multiplayer_num_bots_required_team_2", "$g_multiplayer_num_bots_team_2", ":team_2_count"),
         (val_max, "$g_multiplayer_num_bots_required_team_1", 0),
         (val_max, "$g_multiplayer_num_bots_required_team_2", 0),
         ]),

      (0, 0, 0, [],
       [
         (multiplayer_is_server),
         (eq, "$g_multiplayer_ready_for_spawning_agent", 1),
         (store_add, ":total_req", "$g_multiplayer_num_bots_required_team_1", "$g_multiplayer_num_bots_required_team_2"),
         (try_begin),
           (gt, ":total_req", 0),
           (store_random_in_range, ":random_req", 0, ":total_req"),
           (val_sub, ":random_req", "$g_multiplayer_num_bots_required_team_1"),
           (try_begin),
             (lt, ":random_req", 0),
             #add to team 1
             (assign, ":selected_team", 0),
             (val_sub, "$g_multiplayer_num_bots_required_team_1", 1),
           (else_try),
             #add to team 2
             (assign, ":selected_team", 1),
             (val_sub, "$g_multiplayer_num_bots_required_team_2", 1),
           (try_end),

           (team_get_faction, ":team_faction_no", ":selected_team"),
           (assign, ":available_troops_in_faction", 0),

           (try_for_range, ":troop_no", multiplayer_ai_troops_begin, multiplayer_ai_troops_end),
             (store_troop_faction, ":troop_faction", ":troop_no"),
             (eq, ":troop_faction", ":team_faction_no"),
             (val_add, ":available_troops_in_faction", 1),
           (try_end),

           (store_random_in_range, ":random_troop_index", 0, ":available_troops_in_faction"),
           (assign, ":end_cond", multiplayer_ai_troops_end),
           (try_for_range, ":troop_no", multiplayer_ai_troops_begin, ":end_cond"),
             (store_troop_faction, ":troop_faction", ":troop_no"),
             (eq, ":troop_faction", ":team_faction_no"),
             (val_sub, ":random_troop_index", 1),
             (lt, ":random_troop_index", 0),
             (assign, ":end_cond", 0),
             (assign, ":selected_troop", ":troop_no"),
           (try_end),
         
           (troop_get_inventory_slot, ":has_item", ":selected_troop", ek_horse),
           (try_begin),
             (ge, ":has_item", 0),
             (assign, ":is_horseman", 1),
           (else_try),
             (assign, ":is_horseman", 0),
           (try_end),

           (call_script, "script_multiplayer_find_spawn_point", ":selected_team", 0, ":is_horseman"), 
           (store_current_scene, ":cur_scene"),
           (modify_visitors_at_site, ":cur_scene"),
           (add_visitors_to_current_scene, reg0, ":selected_troop", 1, ":selected_team", -1),
           (assign, "$g_multiplayer_ready_for_spawning_agent", 0),
         (try_end),
         ]),

      (1, 0, 0, [],
       [
         (multiplayer_is_server),
         #checking for restarting the map
         (assign, ":end_map", 0),
         (try_begin),
           (store_mission_timer_a, ":mission_timer"),
           (store_mul, ":game_max_seconds", "$g_multiplayer_game_max_minutes", 60),
           (gt, ":mission_timer", ":game_max_seconds"),
           (assign, ":end_map", 1),
         (try_end),
         (try_begin),
           (eq, ":end_map", 1),
           (call_script, "script_game_multiplayer_get_game_type_mission_template", "$g_multiplayer_game_type"),
           (start_multiplayer_mission, reg0, "$g_multiplayer_selected_map", 0),
           (call_script, "script_game_set_multiplayer_mission_end"),
         (try_end),
         ]),
        
      (ti_tab_pressed, 0, 0, [],
       [
         (try_begin),
           (eq, "$g_multiplayer_mission_end_screen", 0),
           (assign, "$g_multiplayer_stats_chart_opened_manually", 1),
           (start_presentation, "prsnt_multiplayer_stats_chart_deathmatch"),
         (try_end),
         ]),

      multiplayer_once_at_the_first_frame,
      
      (ti_escape_pressed, 0, 0, [],
       [
         (neg|is_presentation_active, "prsnt_multiplayer_escape_menu"),
         (neg|is_presentation_active, "prsnt_multiplayer_stats_chart_deathmatch"),
         (eq, "$g_waiting_for_confirmation_to_terminate", 0),
         (start_presentation, "prsnt_multiplayer_escape_menu"),
         ]),
      ],
  ),

    (
    "multiplayer_tdm",mtf_battle_mode,-1, #team_deathmatch mode
    "You lead your men to battle.",
    [
      (0,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (1,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (2,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (3,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (4,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (5,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (6,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (7,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),

      (8,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (9,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (10,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (11,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (12,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (13,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (14,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (15,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),

      (16,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (17,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (18,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (19,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (20,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (21,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (22,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (23,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),

      (24,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (25,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (26,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (27,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (28,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (29,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (30,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (31,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),

      (32,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (33,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (34,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (35,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (36,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (37,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (38,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (39,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),

      (40,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (41,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (42,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (43,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (44,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (45,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (46,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (47,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),

      (48,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (49,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (50,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (51,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (52,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (53,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (54,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (55,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),

      (56,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (57,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (58,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (59,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (60,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (61,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (62,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (63,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
     ],
    [
      common_battle_init_banner,

      multiplayer_server_check_polls,

      (ti_on_agent_spawn, 0, 0, [],
       [
         (store_trigger_param_1, ":agent_no"),
         (call_script, "script_multiplayer_server_on_agent_spawn_common", ":agent_no"),
         ]),
      
      (ti_server_player_joined, 0, 0, [],
       [
         (store_trigger_param_1, ":player_no"),
         (call_script, "script_multiplayer_server_player_joined_common", ":player_no"),
         ]),

      (ti_before_mission_start, 0, 0, [],
       [
         (assign, "$g_multiplayer_game_type", multiplayer_game_type_team_deathmatch),
         (call_script, "script_multiplayer_server_before_mission_start_common"),

         (call_script, "script_multiplayer_init_mission_variables"),
         (call_script, "script_multiplayer_remove_destroy_mod_targets"),
         (call_script, "script_multiplayer_remove_headquarters_flags"),
         ]),

      (ti_after_mission_start, 0, 0, [], 
       [
         (set_spawn_effector_scene_prop_kind, 0, -1), #during this mission, agents of "team 0" will try to spawn around scene props with kind equal to -1(no effector for this mod)
         (set_spawn_effector_scene_prop_kind, 1, -1), #during this mission, agents of "team 1" will try to spawn around scene props with kind equal to -1(no effector for this mod)

         (call_script, "script_initialize_all_scene_prop_slots"),
         
         (call_script, "script_multiplayer_move_moveable_objects_initial_positions"),

         (assign, "$g_multiplayer_ready_for_spawning_agent", 1),
         ]),

      (ti_on_multiplayer_mission_end, 0, 0, [],
       [
         #GLORIOUS_MOTHER_FACTION achievement
         (try_begin),
           (multiplayer_get_my_player, ":my_player_no"),
           (is_between, ":my_player_no", 0, multiplayer_max_possible_player_id),
           (player_get_team_no, ":my_player_team", ":my_player_no"),
           (lt, ":my_player_team", multi_team_spectator),
           (team_get_score, ":team_1_score", 0),
           (team_get_score, ":team_2_score", 1),
           (assign, ":continue", 0),
           (try_begin),
             (eq, ":my_player_team", 0),
             (gt, ":team_1_score", ":team_2_score"),
             (assign, ":continue", 1),
           (else_try),
             (eq, ":my_player_team", 1),
             (gt, ":team_2_score", ":team_1_score"),
             (assign, ":continue", 1),
           (try_end),
           (eq, ":continue", 1),
           (unlock_achievement, ACHIEVEMENT_GLORIOUS_MOTHER_FACTION),
         (try_end),
         #GLORIOUS_MOTHER_FACTION achievement end

         (call_script, "script_multiplayer_event_mission_end"),
         
         (assign, "$g_multiplayer_stats_chart_opened_manually", 0),
         (start_presentation, "prsnt_multiplayer_stats_chart"),
         ]),

      (ti_on_agent_killed_or_wounded, 0, 0, [],
       [
         (store_trigger_param_1, ":dead_agent_no"), 
         (store_trigger_param_2, ":killer_agent_no"), 
         (call_script, "script_multiplayer_server_on_agent_killed_or_wounded_common", ":dead_agent_no", ":killer_agent_no"),
         #adding 1 score points to killer agent's team. (special for "headquarters" and "team deathmatch" mod)
         (try_begin),
           (ge, ":killer_agent_no", 0),
           (agent_is_human, ":dead_agent_no"),
           (agent_is_human, ":killer_agent_no"),
           (agent_get_team, ":killer_agent_team", ":killer_agent_no"),
           (le, ":killer_agent_team", 1), #0 or 1 is ok
           (agent_get_team, ":dead_agent_team", ":dead_agent_no"),
           (neq, ":killer_agent_team", ":dead_agent_team"),
           (team_get_score, ":team_score", ":killer_agent_team"),
           (val_add, ":team_score", 1),
           (team_set_score, ":killer_agent_team", ":team_score"),
         (try_end),
         ]),

      (1, 0, 0, [],
       [
         (multiplayer_is_server),
         (get_max_players, ":num_players"),
         (try_for_range, ":player_no", 0, ":num_players"),
           (player_is_active, ":player_no"),
           (neg|player_is_busy_with_menus, ":player_no"),

           (player_get_team_no, ":player_team", ":player_no"), #if player is currently spectator do not spawn his agent
           (lt, ":player_team", multi_team_spectator),

           (player_get_troop_id, ":player_troop", ":player_no"), #if troop is not selected do not spawn his agent
           (ge, ":player_troop", 0),

           (player_get_agent_id, ":player_agent", ":player_no"),
           (assign, ":spawn_new", 0),
           (try_begin),
             (player_get_slot, ":player_first_spawn", ":player_no", slot_player_first_spawn),
             (eq, ":player_first_spawn", 1),
             (assign, ":spawn_new", 1),
             (player_set_slot, ":player_no", slot_player_first_spawn, 0),
           (else_try),
             (try_begin),
               (lt, ":player_agent", 0),
               (assign, ":spawn_new", 1),
             (else_try),
               (neg|agent_is_alive, ":player_agent"),
               (agent_get_time_elapsed_since_removed, ":elapsed_time", ":player_agent"),
               (gt, ":elapsed_time", "$g_multiplayer_respawn_period"),
               (assign, ":spawn_new", 1),
             (try_end),             
           (try_end),
           (eq, ":spawn_new", 1),
           (call_script, "script_multiplayer_buy_agent_equipment", ":player_no"),

           (troop_get_inventory_slot, ":has_item", ":player_troop", ek_horse),
           (try_begin),
             (ge, ":has_item", 0),
             (assign, ":is_horseman", 1),
           (else_try),
             (assign, ":is_horseman", 0),
           (try_end),

           (call_script, "script_multiplayer_find_spawn_point", ":player_team", 1, ":is_horseman"), 
           (player_spawn_new_agent, ":player_no", reg0),
         (try_end),
         ]),

      (1, 0, 0, [], #do this in every new frame, but not at the same time
       [
         (multiplayer_is_server),
         (store_mission_timer_a, ":mission_timer"),
         (ge, ":mission_timer", 2),
         (assign, ":team_1_count", 0),
         (assign, ":team_2_count", 0),
         (try_for_agents, ":cur_agent"),
           (agent_is_non_player, ":cur_agent"),
           (agent_is_human, ":cur_agent"),
           (assign, ":will_be_counted", 0),
           (try_begin),
             (agent_is_alive, ":cur_agent"),
             (assign, ":will_be_counted", 1), #alive so will be counted
           (else_try),
             (agent_get_time_elapsed_since_removed, ":elapsed_time", ":cur_agent"),
             (le, ":elapsed_time", "$g_multiplayer_respawn_period"),
             (assign, ":will_be_counted", 1), 
           (try_end),
           (eq, ":will_be_counted", 1),
           (agent_get_team, ":cur_team", ":cur_agent"),
           (try_begin),
             (eq, ":cur_team", 0),
             (val_add, ":team_1_count", 1),
           (else_try),
             (eq, ":cur_team", 1),
             (val_add, ":team_2_count", 1),
           (try_end),
         (try_end),
         (store_sub, "$g_multiplayer_num_bots_required_team_1", "$g_multiplayer_num_bots_team_1", ":team_1_count"),
         (store_sub, "$g_multiplayer_num_bots_required_team_2", "$g_multiplayer_num_bots_team_2", ":team_2_count"),
         (val_max, "$g_multiplayer_num_bots_required_team_1", 0),
         (val_max, "$g_multiplayer_num_bots_required_team_2", 0),
         ]),
      
      multiplayer_server_spawn_bots,
      multiplayer_server_manage_bots,

      (20, 0, 0, [],
       [
         (multiplayer_is_server),
         #auto team balance control in every 20 seconds (tdm)
         (call_script, "script_check_team_balance"),
         ]),

      multiplayer_server_check_end_map,
        
      (ti_tab_pressed, 0, 0, [],
       [
         (try_begin),
           (eq, "$g_multiplayer_mission_end_screen", 0),
           (assign, "$g_multiplayer_stats_chart_opened_manually", 1),
           (start_presentation, "prsnt_multiplayer_stats_chart"),
         (try_end),
         ]),

      multiplayer_once_at_the_first_frame,
      multiplayer_battle_window_opened,

      (ti_escape_pressed, 0, 0, [],
       [
         (neg|is_presentation_active, "prsnt_multiplayer_escape_menu"),
         (neg|is_presentation_active, "prsnt_multiplayer_stats_chart"),
         (eq, "$g_waiting_for_confirmation_to_terminate", 0),
         (start_presentation, "prsnt_multiplayer_escape_menu"),
         ]),
      ],
  ),
  
  (
    "multiplayer_hq", mtf_battle_mode,-1, #headquarters mode
    "You lead your men to battle.",
    [
      (0,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (1,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (2,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (3,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (4,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (5,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (6,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (7,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),

      (8,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (9,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (10,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (11,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (12,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (13,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (14,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (15,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),

      (16,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (17,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (18,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (19,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (20,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (21,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (22,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (23,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),

      (24,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (25,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (26,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (27,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (28,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (29,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (30,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (31,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),

      (32,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (33,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (34,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (35,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (36,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (37,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (38,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (39,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),

      (40,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (41,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (42,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (43,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (44,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (45,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (46,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (47,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),

      (48,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (49,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (50,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (51,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (52,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (53,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (54,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (55,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),

      (56,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (57,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (58,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (59,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (60,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (61,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (62,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (63,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
     ],
    [
      common_battle_init_banner,

      multiplayer_server_check_polls,

      (ti_on_agent_spawn, 0, 0, [],
       [
         (store_trigger_param_1, ":agent_no"),
         (call_script, "script_multiplayer_server_on_agent_spawn_common", ":agent_no"),
         ]),
      
      (ti_server_player_joined, 0, 0, [],
       [
         (store_trigger_param_1, ":player_no"),
         (call_script, "script_multiplayer_server_player_joined_common", ":player_no"),
         ]),

      (ti_before_mission_start, 0, 0, [],
       [
         (assign, "$g_multiplayer_game_type", multiplayer_game_type_headquarters),
         (call_script, "script_multiplayer_server_before_mission_start_common"),

         (store_mul, ":initial_hq_score", "$g_multiplayer_game_max_points", 10000),
         
         (assign, "$g_score_team_1", ":initial_hq_score"),
         (assign, "$g_score_team_2", ":initial_hq_score"),

         (try_for_range, ":cur_flag_slot", multi_data_flag_owner_begin, multi_data_flag_owner_end),
           (troop_set_slot, "trp_multiplayer_data", ":cur_flag_slot", -1),
         (try_end),
           
         (try_begin),
           (multiplayer_is_server),
           (try_for_range, ":cur_flag_slot", multi_data_flag_pull_code_begin, multi_data_flag_pull_code_end),
             (troop_set_slot, "trp_multiplayer_data", ":cur_flag_slot", -1),
           (try_end),
         (try_end),

         (call_script, "script_multiplayer_init_mission_variables"),
         (call_script, "script_multiplayer_remove_destroy_mod_targets"),

         (try_begin),
           (multiplayer_is_server),
           (team_set_score, 0, "$g_multiplayer_game_max_points"),
           (team_set_score, 1, "$g_multiplayer_game_max_points"),
         (try_end),
         ]),

      (ti_after_mission_start, 0, 0, [],
       [
         (call_script, "script_determine_team_flags", 0),
         (call_script, "script_determine_team_flags", 1),         
         (set_spawn_effector_scene_prop_kind, 0, "$team_1_flag_scene_prop"), #during this mission, agents of "team 0" will try to spawn around scene props with kind equal to $team_1_flag_scene_prop
         (set_spawn_effector_scene_prop_kind, 1, "$team_2_flag_scene_prop"), #during this mission, agents of "team 1" will try to spawn around scene props with kind equal to $team_2_flag_scene_prop
         
         (try_begin),
           (multiplayer_is_server),

           (assign, "$g_multiplayer_ready_for_spawning_agent", 1),
         
           (assign, "$g_number_of_flags", 0),
         
           #place base flags
           (entry_point_get_position, pos1, multi_base_point_team_1),
           (entry_point_get_position, pos3, multi_base_point_team_1),

           (set_spawn_position, pos3),
           (spawn_scene_prop, "spr_headquarters_pole_code_only", 0),           
           (set_spawn_position, pos3),
           (spawn_scene_prop, "$team_1_flag_scene_prop", 0),           
           (set_spawn_position, pos3),
           (spawn_scene_prop, "$team_2_flag_scene_prop", 0),                    
           (set_spawn_position, pos3),
           (spawn_scene_prop, "spr_headquarters_flag_gray_code_only", 0),           
         
           (store_add, ":cur_flag_slot", multi_data_flag_owner_begin, "$g_number_of_flags"),
           (troop_set_slot, "trp_multiplayer_data", ":cur_flag_slot", 1),
           (val_add, "$g_number_of_flags", 1),

           (entry_point_get_position, pos2, multi_base_point_team_2),
           (entry_point_get_position, pos3, multi_base_point_team_2),
         
           (set_spawn_position, pos3),
           (spawn_scene_prop, "spr_headquarters_pole_code_only", 0),                    
           (set_spawn_position, pos3),
           (spawn_scene_prop, "$team_1_flag_scene_prop", 0),                    
           (set_spawn_position, pos3),
           (spawn_scene_prop, "$team_2_flag_scene_prop", 0),                    
           (set_spawn_position, pos3),
           (spawn_scene_prop, "spr_headquarters_flag_gray_code_only", 0),                    
           (store_add, ":cur_flag_slot", multi_data_flag_owner_begin, "$g_number_of_flags"),
           (troop_set_slot, "trp_multiplayer_data", ":cur_flag_slot", 2),
           (val_add, "$g_number_of_flags", 1),

           (scene_prop_get_num_instances, ":num_instances_of_red_headquarters_flag", "spr_headquarters_flag_red"),
           (scene_prop_get_num_instances, ":num_instances_of_blue_headquarters_flag", "spr_headquarters_flag_blue"),
           (scene_prop_get_num_instances, ":num_instances_of_gray_headquarters_flag", "spr_headquarters_flag_gray"),

           (store_add, ":end_cond", "spr_headquarters_flag_gray", 1),
           (try_for_range, ":headquarters_flag_no", "spr_headquarters_flag_red", ":end_cond"),
             (try_begin),
               (eq, ":headquarters_flag_no", "spr_headquarters_flag_red"),
               (assign, ":num_instances_of_headquarters_flag", ":num_instances_of_red_headquarters_flag"),
             (else_try),
               (eq, ":headquarters_flag_no", "spr_headquarters_flag_blue"),
               (assign, ":num_instances_of_headquarters_flag", ":num_instances_of_blue_headquarters_flag"),
             (else_try),
               (eq, ":headquarters_flag_no", "spr_headquarters_flag_gray"),
               (assign, ":num_instances_of_headquarters_flag", ":num_instances_of_gray_headquarters_flag"),
             (try_end),
             (gt, ":num_instances_of_headquarters_flag", 0),
             (try_for_range, ":instance_no", 0, ":num_instances_of_headquarters_flag"),
               (scene_prop_get_instance, ":flag_id", ":headquarters_flag_no", ":instance_no"),
               (prop_instance_get_position, pos0, ":flag_id"),
        
               (set_spawn_position, pos0),
               (spawn_scene_prop, "spr_headquarters_pole_code_only", 0),               
         
               #place other flags
               (try_for_range, ":headquarters_flag_no_will_be_added", "spr_headquarters_flag_red", ":end_cond"),
                 (set_spawn_position, pos0),             
                 (try_begin),
                   (eq, ":headquarters_flag_no_will_be_added", "spr_headquarters_flag_red"),
                   (spawn_scene_prop, "$team_1_flag_scene_prop"),
                 (else_try),
                   (eq, ":headquarters_flag_no_will_be_added", "spr_headquarters_flag_blue"),
                   (spawn_scene_prop, "$team_2_flag_scene_prop"),
                 (else_try),
                   (eq, ":headquarters_flag_no_will_be_added", "spr_headquarters_flag_gray"),
                   (spawn_scene_prop, "spr_headquarters_flag_gray_code_only"),
                 (try_end),                         
               (try_end),

               #assign who owns this flag values
               (store_add, ":cur_flag_slot", multi_data_flag_owner_begin, "$g_number_of_flags"),
               (try_begin),
                 (eq, ":headquarters_flag_no", "spr_headquarters_flag_red"),
                 (troop_set_slot, "trp_multiplayer_data", ":cur_flag_slot", 1),
               (else_try),
                 (eq, ":headquarters_flag_no", "spr_headquarters_flag_blue"),
                 (troop_set_slot, "trp_multiplayer_data", ":cur_flag_slot", 2),
               (else_try),
                 (eq, ":headquarters_flag_no", "spr_headquarters_flag_gray"),
                 (troop_set_slot, "trp_multiplayer_data", ":cur_flag_slot", 0),
               (try_end),
               (val_add, "$g_number_of_flags", 1),         
             (try_end),
           (try_end),

           (assign, "$g_number_of_initial_team_1_flags", 0),
           (assign, "$g_number_of_initial_team_2_flags", 0),

           (try_for_range, ":place_no", 0, "$g_number_of_flags"),
             (store_add, ":cur_flag_slot", multi_data_flag_owner_begin, ":place_no"),
             (troop_get_slot, ":current_owner", "trp_multiplayer_data", ":cur_flag_slot"),
         
             (try_begin),
               (eq, ":place_no", 0),
               (entry_point_get_position, pos0, multi_base_point_team_1),
               (scene_prop_get_instance, ":flag_id", "$team_1_flag_scene_prop", ":place_no"),
               (assign, "$g_base_flag_team_1", ":flag_id"),
             (else_try),
               (eq, ":place_no", 1),
               (entry_point_get_position, pos0, multi_base_point_team_2),
               (scene_prop_get_instance, ":flag_id", "$team_2_flag_scene_prop", ":place_no"),
               (assign, "$g_base_flag_team_2", ":flag_id"),
             (else_try),
               (assign, ":flag_start_red", 2),
               (scene_prop_get_num_instances, ":num_initial_red_flags", "spr_headquarters_flag_red"),
               (store_add, ":flag_start_blue", ":flag_start_red", ":num_initial_red_flags"),
               (scene_prop_get_num_instances, ":num_initial_blue_flags", "spr_headquarters_flag_blue"),
               (store_add, ":flag_start_gray", ":flag_start_blue", ":num_initial_blue_flags"),
               (scene_prop_get_num_instances, ":num_initial_gray_flags", "spr_headquarters_flag_gray"),         
               (try_begin),
                 (ge, ":place_no", ":flag_start_red"),
                 (gt, ":num_initial_red_flags", 0),         
                 (store_sub, ":flag_no", ":place_no", ":flag_start_red"),
                 (scene_prop_get_instance, ":flag_id", "spr_headquarters_flag_red", ":flag_no"),
               (else_try),
                 (ge, ":place_no", ":flag_start_blue"),
                 (gt, ":num_initial_blue_flags", 0),         
                 (store_sub, ":flag_no", ":place_no", ":flag_start_blue"),
                 (scene_prop_get_instance, ":flag_id", "spr_headquarters_flag_blue", ":flag_no"),
               (else_try),
                 (ge, ":place_no", ":flag_start_gray"),
                 (gt, ":num_initial_gray_flags", 0),         
                 (store_sub, ":flag_no", ":place_no", ":flag_start_gray"),
                 (scene_prop_get_instance, ":flag_id", "spr_headquarters_flag_gray", ":flag_no"),
               (try_end),             
               (prop_instance_get_position, pos0, ":flag_id"),
             (try_end),

             (scene_prop_get_instance, ":pole_id", "spr_headquarters_pole_code_only", ":place_no"),
             (prop_instance_set_position, ":pole_id", pos0),
         
             (position_move_z, pos0, multi_headquarters_pole_height),           
             (try_begin),
               (eq, ":current_owner", 0),
               (scene_prop_get_instance, ":flag_id", "$team_1_flag_scene_prop", ":place_no"),
               (prop_instance_set_position, ":flag_id", pos0),
               (scene_prop_set_visibility, ":flag_id", 0),
               (scene_prop_get_instance, ":flag_id", "$team_2_flag_scene_prop", ":place_no"),
               (prop_instance_set_position, ":flag_id", pos0),
               (scene_prop_set_visibility, ":flag_id", 0),
               (scene_prop_get_instance, ":flag_id", "spr_headquarters_flag_gray_code_only", ":place_no"),
               (prop_instance_set_position, ":flag_id", pos0),
               (scene_prop_set_visibility, ":flag_id", 1),
             (else_try),
               (eq, ":current_owner", 1),
               (scene_prop_get_instance, ":flag_id", "$team_1_flag_scene_prop", ":place_no"),
               (prop_instance_set_position, ":flag_id", pos0),
               (scene_prop_set_visibility, ":flag_id", 1),
               (scene_prop_get_instance, ":flag_id", "$team_2_flag_scene_prop", ":place_no"),
               (prop_instance_set_position, ":flag_id", pos0),
               (scene_prop_set_visibility, ":flag_id", 0),
               (scene_prop_get_instance, ":flag_id", "spr_headquarters_flag_gray_code_only", ":place_no"),
               (prop_instance_set_position, ":flag_id", pos0),
               (scene_prop_set_visibility, ":flag_id", 0),
               (val_add, "$g_number_of_initial_team_1_flags", 1),
             (else_try),
               (scene_prop_get_instance, ":flag_id", "$team_1_flag_scene_prop", ":place_no"),
               (prop_instance_set_position, ":flag_id", pos0),
               (scene_prop_set_visibility, ":flag_id", 0),
               (scene_prop_get_instance, ":flag_id", "$team_2_flag_scene_prop", ":place_no"),
               (prop_instance_set_position, ":flag_id", pos0),
               (scene_prop_set_visibility, ":flag_id", 1),
               (scene_prop_get_instance, ":flag_id", "spr_headquarters_flag_gray_code_only", ":place_no"),
               (prop_instance_set_position, ":flag_id", pos0),
               (scene_prop_set_visibility, ":flag_id", 0),
               (val_add, "$g_number_of_initial_team_2_flags", 1),
             (try_end),
           (try_end),
         (else_try),
           #these three lines both used in calculation of $g_number_of_flags and below part removing of initially placed flags
           (scene_prop_get_num_instances, ":num_instances_of_red_headquarters_flag", "spr_headquarters_flag_red"),
           (scene_prop_get_num_instances, ":num_instances_of_blue_headquarters_flag", "spr_headquarters_flag_blue"),
           (scene_prop_get_num_instances, ":num_instances_of_gray_headquarters_flag", "spr_headquarters_flag_gray"),

           (assign, "$g_number_of_flags", 2),
           (val_add, "$g_number_of_flags", ":num_instances_of_red_headquarters_flag"),
           (val_add, "$g_number_of_flags", ":num_instances_of_blue_headquarters_flag"),
           (val_add, "$g_number_of_flags", ":num_instances_of_gray_headquarters_flag"),         
         (try_end),

         #remove initially placed flags
         (try_for_range, ":flag_no", 0, ":num_instances_of_red_headquarters_flag"),
           (scene_prop_get_instance, ":flag_id", "spr_headquarters_flag_red", ":flag_no"),
           (scene_prop_set_visibility, ":flag_id", 0),
         (try_end),
         (try_for_range, ":flag_no", 0, ":num_instances_of_blue_headquarters_flag"),
           (scene_prop_get_instance, ":flag_id", "spr_headquarters_flag_blue", ":flag_no"),
           (scene_prop_set_visibility, ":flag_id", 0),
         (try_end),
         (try_for_range, ":flag_no", 0, ":num_instances_of_gray_headquarters_flag"),
           (scene_prop_get_instance, ":flag_id", "spr_headquarters_flag_gray", ":flag_no"),
           (scene_prop_set_visibility, ":flag_id", 0),
         (try_end),

         (try_for_range, ":flag_no", 0, "$g_number_of_flags"),
           (store_add, ":cur_flag_owned_seconds_counts_slot", multi_data_flag_owned_seconds_begin, ":flag_no"),
           (troop_set_slot, "trp_multiplayer_data", ":cur_flag_owned_seconds_counts_slot", 0),
         (try_end),

         (call_script, "script_initialize_all_scene_prop_slots"),
         
         (call_script, "script_multiplayer_move_moveable_objects_initial_positions"),
       ]),         

      (ti_on_multiplayer_mission_end, 0, 0, [],
       [
         #RUIN_THE_RAID achievement
         (try_begin),
           (multiplayer_get_my_player, ":my_player_no"),
           (is_between, ":my_player_no", 0, multiplayer_max_possible_player_id),
           (player_get_team_no, ":my_player_team", ":my_player_no"),
           (lt, ":my_player_team", multi_team_spectator),
           (call_script, "script_get_headquarters_scores"),
           (assign, ":team_1_num_flags", reg0),
           (assign, ":team_2_num_flags", reg1),
           (assign, ":continue", 0),
           (try_begin),
             (eq, ":my_player_team", 0),
             (gt, ":team_1_num_flags", ":team_2_num_flags"),
             (assign, ":continue", 1),
           (else_try),
             (eq, ":my_player_team", 1),
             (gt, ":team_2_num_flags", ":team_1_num_flags"),
             (assign, ":continue", 1),
           (try_end),
           (eq, ":continue", 1),
           (unlock_achievement, ACHIEVEMENT_RUIN_THE_RAID),
         (try_end),
         #RUIN_THE_RAID achievement end

         (call_script, "script_multiplayer_event_mission_end"),

         (assign, "$g_multiplayer_stats_chart_opened_manually", 0),
         (start_presentation, "prsnt_multiplayer_stats_chart"),
         ]),

      (ti_on_agent_killed_or_wounded, 0, 0, [],
       [
         (store_trigger_param_1, ":dead_agent_no"), 
         (store_trigger_param_2, ":killer_agent_no"),
         (call_script, "script_multiplayer_server_on_agent_killed_or_wounded_common", ":dead_agent_no", ":killer_agent_no"),

         #adding 1 score points to killer agent's team. (special for "headquarters" and "team deathmatch" mod)
         (try_begin), 
           (multiplayer_is_server),
           (ge, ":killer_agent_no", 0),
           (agent_is_human, ":dead_agent_no"),
           (agent_is_human, ":killer_agent_no"),
           (agent_get_team, ":killer_agent_team", ":killer_agent_no"),
           (le, ":killer_agent_team", 1), #0 or 1 is ok
           (agent_get_team, ":dead_agent_team", ":dead_agent_no"),
           (neq, ":killer_agent_team", ":dead_agent_team"),
           (team_get_score, ":team_score", ":dead_agent_team"),
           (try_begin),
             (eq, ":killer_agent_team", 0),
             (val_add, "$g_score_team_2", -10000), #if someone died from "team 2" then "team 2" loses 1 score point
           (else_try),
             (val_add, "$g_score_team_1", -10000), #if someone died from "team 1" then "team 1" loses 1 score point
           (try_end),
           (val_sub, ":team_score", 1),
           
           (get_max_players, ":num_players"),

           #for only server itself-----------------------------------------------------------------------------------------------
           (call_script, "script_team_set_score", ":dead_agent_team", ":team_score"),
           #for only server itself-----------------------------------------------------------------------------------------------
           (try_for_range, ":player_no", 1, ":num_players"), #0 is server so starting from 1
             (player_is_active, ":player_no"),
             (multiplayer_send_2_int_to_player, ":player_no", multiplayer_event_set_team_score, ":dead_agent_team", ":team_score"),             
           (try_end),
         (try_end),
         ]),

      (1, 0, 0, [],
      [
        (multiplayer_is_server),
        #trigger for (a) counting seconds of flags being owned by their owners & (b) to calculate seconds past after that flag's pull message has shown          
        (try_for_range, ":flag_no", 0, "$g_number_of_flags"),
          #part a: counting seconds of flags being owned by their owners
          (store_add, ":cur_flag_owned_seconds_counts_slot", multi_data_flag_owned_seconds_begin, ":flag_no"),
          (troop_get_slot, ":cur_flag_owned_seconds", "trp_multiplayer_data", ":cur_flag_owned_seconds_counts_slot"),
          (val_add, ":cur_flag_owned_seconds", 1),
          (troop_set_slot, "trp_multiplayer_data", ":cur_flag_owned_seconds_counts_slot", ":cur_flag_owned_seconds"),
          #part b: to calculate seconds past after that flag's pull message has shown
          (store_add, ":cur_flag_pull_code_slot", multi_data_flag_pull_code_begin, ":flag_no"),
          (troop_get_slot, ":cur_flag_pull_code", "trp_multiplayer_data", ":cur_flag_pull_code_slot"),
          (store_mod, ":cur_flag_pull_message_seconds_past", ":cur_flag_pull_code", 100),
          (try_begin),
            (ge, ":cur_flag_pull_code", 100),
            (lt, ":cur_flag_pull_message_seconds_past", 25),
            (val_add, ":cur_flag_pull_code", 1),
            (troop_set_slot, "trp_multiplayer_data", ":cur_flag_pull_code_slot", ":cur_flag_pull_code"),
          (try_end),
        (try_end),        
      ]),               
      
      (0, 0, 0, [], #if this trigger takes lots of time in the future and make server machine runs headqurters mod
                    #very slow with lots of players make period of this trigger 1 seconds, but best is 0. Currently
                    #we are testing this mod with few players and no speed program occured.
      [
        (multiplayer_is_server),
        #main trigger which controls which agent is moving/near which flag.
        (try_for_range, ":flag_no", 0, "$g_number_of_flags"),
          (store_add, ":cur_flag_owner_counts_slot", multi_data_flag_players_around_begin, ":flag_no"),
          (troop_get_slot, ":current_owner_code", "trp_multiplayer_data", ":cur_flag_owner_counts_slot"),
          (store_div, ":old_team_1_agent_count", ":current_owner_code", 100),
          (store_mod, ":old_team_2_agent_count", ":current_owner_code", 100),
        
          (assign, ":number_of_agents_around_flag_team_1", 0),
          (assign, ":number_of_agents_around_flag_team_2", 0),

          (scene_prop_get_instance, ":pole_id", "spr_headquarters_pole_code_only", ":flag_no"), 
          (prop_instance_get_position, pos0, ":pole_id"), #pos0 holds pole position.

          (get_max_players, ":num_players"),
            (try_for_range, ":player_no", 0, ":num_players"),
            (player_is_active, ":player_no"),
            (player_get_agent_id, ":cur_agent", ":player_no"),
            (ge, ":cur_agent", 0),
            (agent_is_alive, ":cur_agent"),
            (agent_get_team, ":cur_agent_team", ":cur_agent"),
            (agent_get_position, pos1, ":cur_agent"), #pos1 holds agent's position.
            (get_sq_distance_between_positions, ":squared_dist", pos0, pos1),
            (get_sq_distance_between_position_heights, ":squared_height_dist", pos0, pos1),
            (val_add, ":squared_dist", ":squared_height_dist"),
            (lt, ":squared_dist", multi_headquarters_max_distance_sq_to_raise_flags),
            (try_begin),
              (eq, ":cur_agent_team", 0),
              (val_add, ":number_of_agents_around_flag_team_1", 1),
            (else_try),
              (eq, ":cur_agent_team", 1),
              (val_add, ":number_of_agents_around_flag_team_2", 1),
            (try_end),
          (try_end),

          (try_begin),
            (this_or_next|neq, ":old_team_1_agent_count", ":number_of_agents_around_flag_team_1"),
            (neq, ":old_team_2_agent_count", ":number_of_agents_around_flag_team_2"),

            (store_add, ":cur_flag_owner_slot", multi_data_flag_owner_begin, ":flag_no"),
            (troop_get_slot, ":cur_flag_owner", "trp_multiplayer_data", ":cur_flag_owner_slot"),

            (store_add, ":cur_flag_pull_code_slot", multi_data_flag_pull_code_begin, ":flag_no"),
            (troop_get_slot, ":cur_flag_pull_code", "trp_multiplayer_data", ":cur_flag_pull_code_slot"),
            (store_mod, ":cur_flag_pull_message_seconds_past", ":cur_flag_pull_code", 100),
            (store_div, ":cur_flag_puller_team_last", ":cur_flag_pull_code", 100),

            (try_begin),        
              (assign, ":continue", 0),
              (try_begin),
                (neq, ":cur_flag_owner", 1),
                (eq, ":old_team_1_agent_count", 0),
                (gt, ":number_of_agents_around_flag_team_1", 0),
                (eq, ":number_of_agents_around_flag_team_2", 0),
                (assign, ":puller_team", 1),
                (assign, ":continue", 1),
              (else_try),
                (neq, ":cur_flag_owner", 2),
                (eq, ":old_team_2_agent_count", 0),
                (eq, ":number_of_agents_around_flag_team_1", 0),
                (gt, ":number_of_agents_around_flag_team_2", 0),
                (assign, ":puller_team", 2),
                (assign, ":continue", 1),
              (try_end),
 
              (eq, ":continue", 1),

              (store_mul, ":puller_team_multiplied_by_100", ":puller_team", 100),
              (troop_set_slot, "trp_multiplayer_data", ":cur_flag_pull_code_slot", ":puller_team_multiplied_by_100"),

              (this_or_next|neq, ":cur_flag_puller_team_last", ":puller_team"),
              (ge, ":cur_flag_pull_message_seconds_past", 25),

              (store_mul, ":flag_code", ":puller_team", 100),
              (val_add, ":flag_code", ":flag_no"),
              #for only server itself-----------------------------------------------------------------------------------------------
              (call_script, "script_show_multiplayer_message", multiplayer_message_type_flag_is_pulling, ":flag_code"), 
              #for only server itself-----------------------------------------------------------------------------------------------     
              (try_for_range, ":player_no", 1, ":num_players"), #0 is server so starting from 1
                (player_is_active, ":player_no"),
                (multiplayer_send_2_int_to_player, ":player_no", multiplayer_event_show_multiplayer_message, multiplayer_message_type_flag_is_pulling, ":flag_code"),
              (try_end),
            (try_end),

            (try_begin),
              (store_mul, ":current_owner_code", ":number_of_agents_around_flag_team_1", 100),
              (val_add, ":current_owner_code", ":number_of_agents_around_flag_team_2"),        
              (troop_set_slot, "trp_multiplayer_data", ":cur_flag_owner_counts_slot", ":current_owner_code"),

              #for only server itself-----------------------------------------------------------------------------------------------
              (call_script, "script_set_num_agents_around_flag", ":flag_no", ":current_owner_code"),
              #for only server itself-----------------------------------------------------------------------------------------------
              (get_max_players, ":num_players"),
              (try_for_range, ":player_no", 1, ":num_players"), #0 is server so starting from 1
                (player_is_active, ":player_no"),
                (multiplayer_send_2_int_to_player, ":player_no", multiplayer_event_set_num_agents_around_flag, ":flag_no", ":current_owner_code"),
              (try_end),
            (try_end),
          (try_end),
        (try_end),

        (try_for_range, ":flag_no", 0, "$g_number_of_flags"),
          (assign, ":new_flag_owner", -1),

          (scene_prop_get_instance, ":pole_id", "spr_headquarters_pole_code_only", ":flag_no"), 
          (prop_instance_get_position, pos0, ":pole_id"), #pos0 holds pole position.            

          (store_add, ":cur_flag_owner_slot", multi_data_flag_owner_begin, ":flag_no"),
          (troop_get_slot, ":cur_flag_owner", "trp_multiplayer_data", ":cur_flag_owner_slot"),

          (try_begin),
            (try_begin),
              (scene_prop_get_instance, ":flag_id", "$team_1_flag_scene_prop", ":flag_no"),
              (scene_prop_get_visibility, ":flag_visibility", ":flag_id"),
              (assign, ":cur_shown_flag", 1),
              (eq, ":flag_visibility", 0),
              (scene_prop_get_instance, ":flag_id", "$team_2_flag_scene_prop", ":flag_no"),
              (scene_prop_get_visibility, ":flag_visibility", ":flag_id"),
              (assign, ":cur_shown_flag", 2),
              (eq, ":flag_visibility", 0),                    
              (scene_prop_get_instance, ":flag_id", "spr_headquarters_flag_gray_code_only", ":flag_no"),
              (scene_prop_get_visibility, ":flag_visibility", ":flag_id"),        
              (assign, ":cur_shown_flag", 0),
            (try_end),

            #flag_id holds shown flag after this point
            (prop_instance_get_position, pos1, ":flag_id"), #pos1 holds gray/red/blue (current shown) flag position.

            (try_begin),
              (get_sq_distance_between_positions, ":squared_dist", pos0, pos1),        
              (lt, ":squared_dist", multi_headquarters_distance_sq_to_change_flag), #if distance is less than 2 meters

              (store_add, ":cur_flag_players_around_slot", multi_data_flag_players_around_begin, ":flag_no"),
              (troop_get_slot, ":cur_flag_players_around", "trp_multiplayer_data", ":cur_flag_players_around_slot"),
              (store_div, ":number_of_agents_around_flag_team_1", ":cur_flag_players_around", 100),
              (store_mod, ":number_of_agents_around_flag_team_2", ":cur_flag_players_around", 100),

              (try_begin),
                (gt, ":number_of_agents_around_flag_team_1", 0),
                (eq, ":number_of_agents_around_flag_team_2", 0),
                (assign, ":new_flag_owner", 0),
                (assign, ":new_shown_flag", 1),
              (else_try),
                (eq, ":number_of_agents_around_flag_team_1", 0),
                (gt, ":number_of_agents_around_flag_team_2", 0),
                (assign, ":new_flag_owner", 0),
                (assign, ":new_shown_flag", 2),
              (else_try),
                (eq, ":number_of_agents_around_flag_team_1", 0),
                (eq, ":number_of_agents_around_flag_team_2", 0),
                (neq, ":cur_shown_flag", 0),
                (assign, ":new_flag_owner", 0),
                (assign, ":new_shown_flag", 0),
              (try_end),
            (else_try),
              (neq, ":cur_flag_owner", ":cur_shown_flag"),      
              (get_sq_distance_between_positions, ":squared_dist", pos0, pos1),        
              (ge, ":squared_dist", multi_headquarters_distance_sq_to_set_flag), #if distance is more equal than 9 meters

              (store_add, ":cur_flag_players_around_slot", multi_data_flag_players_around_begin, ":flag_no"),
              (troop_get_slot, ":cur_flag_players_around", "trp_multiplayer_data", ":cur_flag_players_around_slot"),
              (store_div, ":number_of_agents_around_flag_team_1", ":cur_flag_players_around", 100),
              (store_mod, ":number_of_agents_around_flag_team_2", ":cur_flag_players_around", 100),

              (try_begin),
                (eq, ":cur_shown_flag", 1),
                (assign, ":new_flag_owner", 1),
                (assign, ":new_shown_flag", 1),
              (else_try),
                (eq, ":cur_shown_flag", 2),
                (assign, ":new_flag_owner", 2),
                (assign, ":new_shown_flag", 2),
              (try_end),        
            (try_end),
          (try_end),
        
          (try_begin),
            (ge, ":new_flag_owner", 0),
            (this_or_next|neq, ":new_flag_owner", ":cur_flag_owner"),
            (neq, ":cur_shown_flag", ":new_shown_flag"),

            (try_begin),
              (neq, ":cur_flag_owner", 0),
              (eq, ":new_flag_owner", 0),
              (try_begin),
                (eq, ":cur_flag_owner", 1),
                (assign, ":neutralizer_team", 2),
              (else_try),
                (eq, ":cur_flag_owner", 2),
                (assign, ":neutralizer_team", 1),
              (try_end),
              (store_mul, ":flag_code", ":neutralizer_team", 100),
              (val_add, ":flag_code", ":flag_no"),
              #for only server itself-----------------------------------------------------------------------------------------------
              (call_script, "script_show_multiplayer_message", multiplayer_message_type_flag_neutralized, ":flag_code"), 
              #for only server itself-----------------------------------------------------------------------------------------------     
              (get_max_players, ":num_players"),        
              (try_for_range, ":player_no", 1, ":num_players"), #0 is server so starting from 1
                (player_is_active, ":player_no"),
                (multiplayer_send_2_int_to_player, ":player_no", multiplayer_event_show_multiplayer_message, multiplayer_message_type_flag_neutralized, ":flag_code"),
              (try_end),              
            (try_end),
        
            (try_begin),
              (neq, ":cur_flag_owner", ":new_flag_owner"),
              (neq, ":new_flag_owner", 0),
              (store_mul, ":flag_code", ":new_flag_owner", 100),
              (val_add, ":flag_code", ":flag_no"),
              #for only server itself-----------------------------------------------------------------------------------------------
              (call_script, "script_show_multiplayer_message", multiplayer_message_type_flag_captured, ":flag_code"), 
              #for only server itself-----------------------------------------------------------------------------------------------     
              (get_max_players, ":num_players"),        
              (try_for_range, ":player_no", 1, ":num_players"), #0 is server so starting from 1
                (player_is_active, ":player_no"),
                (multiplayer_send_2_int_to_player, ":player_no", multiplayer_event_show_multiplayer_message, multiplayer_message_type_flag_captured, ":flag_code"),
              (try_end),              
            (try_end),

            #for only server itself-----------------------------------------------------------------------------------------------
            (call_script, "script_set_num_agents_around_flag", ":flag_no", ":cur_flag_players_around"),
            #for only server itself-----------------------------------------------------------------------------------------------
            (assign, ":number_of_total_players", 0),
            (get_max_players, ":num_players"),        
            (try_for_range, ":player_no", 1, ":num_players"), #0 is server so starting from 1
              (player_is_active, ":player_no"),
              (multiplayer_send_2_int_to_player, ":player_no", multiplayer_event_set_num_agents_around_flag, ":flag_no", ":cur_flag_players_around"),
              (val_add, ":number_of_total_players", 1),
            (try_end),

            (store_mul, ":owner_code", ":new_flag_owner", 100),
            (val_add, ":owner_code", ":new_shown_flag"),
            #for only server itself-----------------------------------------------------------------------------------------------
            (call_script, "script_change_flag_owner", ":flag_no", ":owner_code"),
            #for only server itself-----------------------------------------------------------------------------------------------
            (try_for_range, ":player_no", 1, ":num_players"), #0 is server so starting from 1
              (player_is_active, ":player_no"),
              (multiplayer_send_2_int_to_player, ":player_no", multiplayer_event_change_flag_owner, ":flag_no", ":owner_code"),          
            (try_end),

            (try_begin),
              (neq, ":new_flag_owner", 0),

              (try_begin),
                (eq, ":new_flag_owner", 1),
                (assign, ":number_of_players_around_flag", ":number_of_agents_around_flag_team_1"),
              (else_try),
                (assign, ":number_of_players_around_flag", ":number_of_agents_around_flag_team_2"),
              (try_end),

              (store_add, ":cur_flag_owned_seconds_counts_slot", multi_data_flag_owned_seconds_begin, ":flag_no"),
              (troop_get_slot, ":current_flag_owned_seconds", "trp_multiplayer_data", ":cur_flag_owned_seconds_counts_slot"),              
              (troop_set_slot, "trp_multiplayer_data", ":cur_flag_owned_seconds_counts_slot", 0),

              (val_min, ":current_flag_owned_seconds", 360), #360 seconds is max time for hq, this will limit money awarding by (180 x total_number_of_players)

              (scene_prop_get_instance, ":flag_of_team_1", "$team_1_flag_scene_prop", ":flag_no"),
              (scene_prop_get_instance, ":flag_of_team_2", "$team_2_flag_scene_prop", ":flag_no"),

              (try_begin),
                (this_or_next|eq, "$g_base_flag_team_1", ":flag_of_team_1"),
                (eq, "$g_base_flag_team_2", ":flag_of_team_2"),
                (assign, ":flag_value", 2),
              (else_try),
                (assign, ":flag_value", 1),
              (try_end),

              (try_begin),                                #score awarding in flag capturing is changed in hq. If only one player captured flag he get 3 points,
                (le, ":number_of_players_around_flag", 1),   #if 2 player captured they get 2 points, if <=6 players get flag all get 1 points. There is no importance of flag value at scoring.
                (assign, ":score_award_per_player", 3),
              (else_try),
                (eq, ":number_of_players_around_flag", 2),
                (assign, ":score_award_per_player", 2),
              (else_try),
                (le, ":number_of_players_around_flag", 6),
                (assign, ":score_award_per_player", 1),
              (else_try),
                (assign, ":score_award_per_player", 0),
              (try_end),
              
              (store_mul, ":total_money_award", ":current_flag_owned_seconds", ":number_of_total_players"), #total money will be shared after a flag capturing is (0.50 * seconds * number_of_players)         
              (val_mul, ":total_money_award", ":flag_value"),                                               #example: if 15 players is playing and 120 seconds past before flag captured, award is 900 golds.
              (val_div, ":total_money_award", 2),

              (try_begin),
                (gt, ":number_of_players_around_flag", 0), #if there are still any living agents around flag.
                (store_div, ":money_award_per_player", ":total_money_award", ":number_of_players_around_flag"),
              (try_end),
        
              (get_max_players, ":num_players"),
                (try_for_range, ":player_no", 0, ":num_players"),
                (player_is_active, ":player_no"),
                (player_get_agent_id, ":cur_agent", ":player_no"),
                (ge, ":cur_agent", 0),
                (agent_get_team, ":cur_agent_team", ":cur_agent"),
                (val_add, ":cur_agent_team", 1),
                (eq, ":cur_agent_team", ":new_flag_owner"),
                (agent_get_position, pos1, ":cur_agent"), 
                (prop_instance_get_position, pos0, ":pole_id"), 
                (get_sq_distance_between_positions, ":squared_dist", pos0, pos1),
                (get_sq_distance_between_position_heights, ":squared_height_dist", pos0, pos1),
                (val_add, ":squared_dist", ":squared_height_dist"),
                (lt, ":squared_dist", multi_headquarters_max_distance_sq_to_raise_flags),                
                (player_get_score, ":player_score", ":player_no"), #give score to player which helped flag to be owned by new_flag_owner team 
                (val_add, ":player_score", ":score_award_per_player"),
                (player_set_score, ":player_no", ":player_score"),                
                (player_get_gold, ":player_gold", ":player_no"), #give money to player which helped flag to be owned by new_flag_owner team 
                (val_add, ":player_gold", ":money_award_per_player"),
                (player_set_gold, ":player_no", ":player_gold", multi_max_gold_that_can_be_stored),              
              (try_end),
            (try_end),
          (try_end),
        (try_end),
        ]),

      (1, 0, 0, [],
       [
         (multiplayer_is_server),
        #trigger for increasing score in each second.
        (assign, ":number_of_team_1_flags", 0),
        (assign, ":number_of_team_2_flags", 0),

        (assign, ":owned_flag_value", 0),        
        (assign, ":not_owned_flag_value", 0),
        
        (try_for_range, ":flag_no", 0, "$g_number_of_flags"),
          (store_add, ":cur_flag_owner_slot", multi_data_flag_owner_begin, ":flag_no"),
          (troop_get_slot, ":cur_flag_owner", "trp_multiplayer_data", ":cur_flag_owner_slot"),

          (scene_prop_get_instance, ":flag_of_team_1", "$team_1_flag_scene_prop", ":flag_no"),
          (scene_prop_get_instance, ":flag_of_team_2", "$team_2_flag_scene_prop", ":flag_no"),
        
          (try_begin),
            (this_or_next|eq, "$g_base_flag_team_1", ":flag_of_team_1"),
            (eq, "$g_base_flag_team_2", ":flag_of_team_2"),
            (assign, ":flag_value", 2),
          (else_try),
            (assign, ":flag_value", 1),
          (try_end),
        
          (try_begin),
            (eq, ":cur_flag_owner", 1),
            (val_add, ":number_of_team_1_flags", ":flag_value"),
            (val_add, ":owned_flag_value", ":flag_value"),
          (else_try),
            (eq, ":cur_flag_owner", 2),
            (val_add, ":number_of_team_2_flags", ":flag_value"),
            (val_add, ":owned_flag_value", ":flag_value"),
          (else_try),
            (val_add, ":not_owned_flag_value", ":flag_value"),
          (try_end),
        (try_end),
        
        (store_add, ":all_flag_value", ":owned_flag_value", ":not_owned_flag_value"),
        (store_sub, ":cur_flag_difference", ":number_of_team_1_flags", ":number_of_team_2_flags"),
        (store_mul, ":cur_flag_difference_mul_2", ":cur_flag_difference", 2),
        (store_sub, ":initial_flag_difference", "$g_number_of_initial_team_1_flags", "$g_number_of_initial_team_2_flags"),

        (assign, ":number_of_active_players", 0),
        (get_max_players, ":end_cond"),
        (try_for_range, ":player_no", 0, ":end_cond"),
          (player_is_active, ":player_no"),
          (val_add, ":number_of_active_players", 1),
          (assign, ":end_cond", 0),
        (try_end),

        (try_begin),
          (ge, ":cur_flag_difference_mul_2", ":initial_flag_difference"),
          (store_sub, ":difference", ":cur_flag_difference_mul_2", ":initial_flag_difference"),
          (store_mul, ":score_addition_winner", ":difference", 125),
          (val_add, ":score_addition_winner", 500),
          (store_div, ":score_addition_loser", 250000, ":score_addition_winner"),
          
          (try_begin), #if number of owned flag values < all flag values give only a percentage of score to teams
            (lt, ":owned_flag_value", ":all_flag_value"),
            (val_mul, ":score_addition_loser", ":owned_flag_value"),
            (val_div, ":score_addition_loser", ":all_flag_value"),
            (val_mul, ":score_addition_winner", ":owned_flag_value"),
            (val_div, ":score_addition_winner", ":all_flag_value"),
          (try_end),

          (call_script, "script_find_number_of_agents_constant"),        
          (val_mul, ":score_addition_winner", reg0),
          (val_div, ":score_addition_winner", 100),
          (val_mul, ":score_addition_loser", reg0),
          (val_div, ":score_addition_loser", 100),
          
          (val_mul, ":score_addition_winner", "$g_multiplayer_point_gained_from_flags"),
          (val_div, ":score_addition_winner", 100),
          (val_mul, ":score_addition_loser", "$g_multiplayer_point_gained_from_flags"),
          (val_div, ":score_addition_loser", 100),

          (try_begin),
            (ge, ":number_of_active_players", 1),
            (val_sub, "$g_score_team_2", ":score_addition_winner"),
            (try_begin),
              (ge, ":number_of_team_2_flags", 1),
              (val_sub, "$g_score_team_1", ":score_addition_loser"),
            (else_try),
              (val_sub, "$g_score_team_2", ":score_addition_loser"),
            (try_end),
          (try_end),
        (else_try),
          (store_sub, ":difference", ":initial_flag_difference", ":cur_flag_difference_mul_2"),
          (store_mul, ":score_addition_winner", ":difference", 125),
          (val_add, ":score_addition_winner", 500),
          (store_div, ":score_addition_loser", 250000, ":score_addition_winner"),
          
          (try_begin), #if number of owned flag values < all flag values give only a percentage of score to teams
            (lt, ":owned_flag_value", ":all_flag_value"),
            (val_mul, ":score_addition_loser", ":owned_flag_value"),
            (val_div, ":score_addition_loser", ":all_flag_value"),
            (val_mul, ":score_addition_winner", ":owned_flag_value"),
            (val_div, ":score_addition_winner", ":all_flag_value"),
          (try_end),

          (call_script, "script_find_number_of_agents_constant"),
          (val_mul, ":score_addition_winner", reg0),
          (val_div, ":score_addition_winner", 100),
          (val_mul, ":score_addition_loser", reg0),
          (val_div, ":score_addition_loser", 100),
        
          (val_mul, ":score_addition_winner", "$g_multiplayer_point_gained_from_flags"),
          (val_div, ":score_addition_winner", 100),
          (val_mul, ":score_addition_loser", "$g_multiplayer_point_gained_from_flags"),
          (val_div, ":score_addition_loser", 100),

          (try_begin),
            (ge, ":number_of_active_players", 1),
            (try_begin),
              (ge, ":number_of_team_1_flags", 1),
              (val_sub, "$g_score_team_2", ":score_addition_loser"),
            (else_try),
              (val_sub, "$g_score_team_1", ":score_addition_loser"),
            (try_end),
            (val_sub, "$g_score_team_1", ":score_addition_winner"),
          (try_end),
        (try_end),

        (team_get_score, ":team_score_1", 0),
        (try_begin),
          (store_div, ":team_new_score_1", "$g_score_team_1", 10000),
          (neq, ":team_new_score_1", ":team_score_1"),
          (get_max_players, ":num_players"),
          #for only server itself-----------------------------------------------------------------------------------------------
          (call_script, "script_team_set_score", 0, ":team_new_score_1"),
          #for only server itself-----------------------------------------------------------------------------------------------
          (try_for_range, ":player_no", 1, ":num_players"), #0 is server so starting from 1
            (player_is_active, ":player_no"),
            (multiplayer_send_2_int_to_player, ":player_no", multiplayer_event_set_team_score, 0, ":team_new_score_1"),
          (try_end),
        (try_end),

        (team_get_score, ":team_score_2", 1),
        (try_begin),
          (store_div, ":team_new_score_2", "$g_score_team_2", 10000),
          (neq, ":team_new_score_2", ":team_score_2"),
          (get_max_players, ":num_players"),
          #for only server itself-----------------------------------------------------------------------------------------------
          (call_script, "script_team_set_score", 1, ":team_new_score_2"),
          #for only server itself-----------------------------------------------------------------------------------------------
          (try_for_range, ":player_no", 1, ":num_players"), #0 is server so starting from 1
            (player_is_active, ":player_no"),
            (multiplayer_send_2_int_to_player, ":player_no", multiplayer_event_set_team_score, 1, ":team_new_score_2"),
          (try_end),
        (try_end),
      ]),

      (1, 0, 0, [],
       [
         (multiplayer_is_server),
         (get_max_players, ":num_players"),
         (try_for_range, ":player_no", 0, ":num_players"),
           (player_is_active, ":player_no"),
           (neg|player_is_busy_with_menus, ":player_no"),

           (player_get_team_no, ":player_team", ":player_no"), #if player is currently spectator do not spawn his agent
           (lt, ":player_team", multi_team_spectator),

           (player_get_troop_id, ":player_troop", ":player_no"), #if troop is not selected do not spawn his agent
           (ge, ":player_troop", 0),

           (player_get_agent_id, ":player_agent", ":player_no"),
           (assign, ":spawn_new", 0),
           (try_begin),
             (player_get_slot, ":player_first_spawn", ":player_no", slot_player_first_spawn),
             (eq, ":player_first_spawn", 1),
             (assign, ":spawn_new", 1),
             (player_set_slot, ":player_no", slot_player_first_spawn, 0),
           (else_try),
             (try_begin),
               (lt, ":player_agent", 0),
               (assign, ":spawn_new", 1),
             (else_try),
               (neg|agent_is_alive, ":player_agent"),
               (agent_get_time_elapsed_since_removed, ":elapsed_time", ":player_agent"),
               (gt, ":elapsed_time", "$g_multiplayer_respawn_period"),
               (assign, ":spawn_new", 1),
             (try_end),             
           (try_end),
           (eq, ":spawn_new", 1),
           (call_script, "script_multiplayer_buy_agent_equipment", ":player_no"),
         
           (troop_get_inventory_slot, ":has_item", ":player_troop", ek_horse),
           (try_begin),
             (ge, ":has_item", 0),
             (assign, ":is_horseman", 1),
           (else_try),
             (assign, ":is_horseman", 0),
           (try_end),

           (call_script, "script_multiplayer_find_spawn_point", ":player_team", 0, ":is_horseman"), 
           (player_spawn_new_agent, ":player_no", reg0),
         (try_end),
         ]),

      (1, 0, 0, [], #do this in every new frame, but not at the same time
       [
         (multiplayer_is_server),
         (store_mission_timer_a, ":mission_timer"),
         (ge, ":mission_timer", 2),
         (assign, ":team_1_count", 0),
         (assign, ":team_2_count", 0),
         (try_for_agents, ":cur_agent"),
           (agent_is_non_player, ":cur_agent"),
           (agent_is_human, ":cur_agent"),
           (assign, ":will_be_counted", 0),
           (try_begin),
             (agent_is_alive, ":cur_agent"),
             (assign, ":will_be_counted", 1), #alive so will be counted
           (else_try),
             (agent_get_time_elapsed_since_removed, ":elapsed_time", ":cur_agent"),
             (le, ":elapsed_time", "$g_multiplayer_respawn_period"),
             (assign, ":will_be_counted", 1), #new died (< g_multiplayer_respawn_period) so will be counted too
           (try_end),
           (eq, ":will_be_counted", 1),
           (agent_get_team, ":cur_team", ":cur_agent"),
           (try_begin),
             (eq, ":cur_team", 0),
             (val_add, ":team_1_count", 1),
           (else_try),
             (eq, ":cur_team", 1),
             (val_add, ":team_2_count", 1),
           (try_end),
         (try_end),
         (store_sub, "$g_multiplayer_num_bots_required_team_1", "$g_multiplayer_num_bots_team_1", ":team_1_count"),
         (store_sub, "$g_multiplayer_num_bots_required_team_2", "$g_multiplayer_num_bots_team_2", ":team_2_count"),
         (val_max, "$g_multiplayer_num_bots_required_team_1", 0),
         (val_max, "$g_multiplayer_num_bots_required_team_2", 0),
         ]),

      multiplayer_server_spawn_bots,
      multiplayer_server_manage_bots,

      (20, 0, 0, [],
       [
         (multiplayer_is_server),
         #auto team balance control in every 10 seconds (hq)
         (call_script, "script_check_team_balance"),
         ]),

      multiplayer_server_check_end_map,
        
      (ti_tab_pressed, 0, 0, [],
       [
         (try_begin),
           (eq, "$g_multiplayer_mission_end_screen", 0),
           (assign, "$g_multiplayer_stats_chart_opened_manually", 1),
           (start_presentation, "prsnt_multiplayer_stats_chart"),
         (try_end),
         ]),

      multiplayer_once_at_the_first_frame,
      multiplayer_battle_window_opened,

      (ti_escape_pressed, 0, 0, [],
       [
         (neg|is_presentation_active, "prsnt_multiplayer_escape_menu"),
         (neg|is_presentation_active, "prsnt_multiplayer_stats_chart"),
         (eq, "$g_waiting_for_confirmation_to_terminate", 0),
         (start_presentation, "prsnt_multiplayer_escape_menu"),
         ]),
      ],
  ),

    (
    "multiplayer_cf",mtf_battle_mode,-1, #capture_the_flag mode
    "You lead your men to battle.",
    [
      (0,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (1,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (2,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (3,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (4,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (5,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (6,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (7,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),

      (8,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (9,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (10,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (11,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (12,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (13,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (14,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (15,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),

      (16,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (17,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (18,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (19,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (20,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (21,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (22,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (23,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),

      (24,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (25,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (26,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (27,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (28,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (29,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (30,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (31,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),

      (32,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (33,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (34,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (35,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (36,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (37,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (38,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (39,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),

      (40,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (41,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (42,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (43,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (44,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (45,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (46,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (47,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),

      (48,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (49,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (50,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (51,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (52,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (53,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (54,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (55,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),

      (56,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (57,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (58,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (59,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (60,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (61,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (62,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (63,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      
      (64,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (65,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
     ],
    [
      common_battle_init_banner,

      multiplayer_server_check_polls,

      (ti_on_agent_spawn, 0, 0, [],
       [
         (store_trigger_param_1, ":agent_no"),
         (call_script, "script_multiplayer_server_on_agent_spawn_common", ":agent_no"),
         ]),
      
      (ti_server_player_joined, 0, 0, [],
       [
         (store_trigger_param_1, ":player_no"),
         (call_script, "script_multiplayer_server_player_joined_common", ":player_no"),
         ]),

      (ti_before_mission_start, 0, 0, [],
       [
         (try_begin),
           (multiplayer_is_server),
           (store_current_scene, ":cur_scene"),
           (this_or_next|eq, ":cur_scene", "scn_random_multi_plain_medium"),
           (this_or_next|eq, ":cur_scene", "scn_random_multi_plain_large"),
           (this_or_next|eq, ":cur_scene", "scn_random_multi_steppe_medium"),
           (eq, ":cur_scene", "scn_random_multi_steppe_large"),
           (entry_point_get_position, pos0, 0),
           (entry_point_set_position, 64, pos0),
           (entry_point_get_position, pos1, 32),
           (entry_point_set_position, 65, pos1),
         (try_end),
         
         (assign, "$g_multiplayer_game_type", multiplayer_game_type_capture_the_flag),
         (call_script, "script_multiplayer_server_before_mission_start_common"),

         (assign, "$flag_1_at_ground_timer", 0),
         (assign, "$flag_2_at_ground_timer", 0),
         
         (call_script, "script_multiplayer_init_mission_variables"),
         (call_script, "script_multiplayer_remove_destroy_mod_targets"),
         (call_script, "script_multiplayer_remove_headquarters_flags"),
         ]),

      (ti_after_mission_start, 0, 0, [],
       [
         (call_script, "script_determine_team_flags", 0),
         (call_script, "script_determine_team_flags", 1),
         (set_spawn_effector_scene_prop_kind, 0, -1), #during this mission, agents of "team 0" will try to spawn around scene props with kind equal to -1(no effector for this mod)
         (set_spawn_effector_scene_prop_kind, 1, -1), #during this mission, agents of "team 1" will try to spawn around scene props with kind equal to -1(no effector for this mod)
       
         (try_begin),
           (multiplayer_is_server),

           (assign, "$g_multiplayer_ready_for_spawning_agent", 1),

           (entry_point_get_position, pos0, multi_base_point_team_1),
           (set_spawn_position, pos0),
           (spawn_scene_prop, "$team_1_flag_scene_prop", 0),
         
           (entry_point_get_position, pos0, multi_base_point_team_2),
           (set_spawn_position, pos0),
           (spawn_scene_prop, "$team_2_flag_scene_prop", 0),
         (try_end),

         (call_script, "script_initialize_all_scene_prop_slots"),
         
         (call_script, "script_multiplayer_move_moveable_objects_initial_positions"),
         ]),         

      (ti_on_multiplayer_mission_end, 0, 0, [],
       [
         (call_script, "script_multiplayer_event_mission_end"),
         (assign, "$g_multiplayer_stats_chart_opened_manually", 0),
         (start_presentation, "prsnt_multiplayer_stats_chart"),
         ]),

      (ti_on_agent_killed_or_wounded, 0, 0, [],
       [
         (store_trigger_param_1, ":dead_agent_no"), 
         (store_trigger_param_2, ":killer_agent_no"), 

         (call_script, "script_multiplayer_server_on_agent_killed_or_wounded_common", ":dead_agent_no", ":killer_agent_no"),

         (try_begin),                                 #when an agent dies which carrying a flag, assign flag position to current position with
           (agent_is_human, ":dead_agent_no"),        #ground level z and do not change it again according to dead agent's any coordinate/rotation.
           (agent_get_attached_scene_prop, ":attached_scene_prop", ":dead_agent_no"),
           (try_begin),
             (try_begin),
               (multiplayer_is_server),
  
               (ge, ":attached_scene_prop", 0), #moved from above after auto-set position

               (multiplayer_get_my_player, ":my_player_no"),
               (get_max_players, ":num_players"),
               #for only server itself-----------------------------------------------------------------------------------------------
               (call_script, "script_set_attached_scene_prop", ":dead_agent_no", -1),
               (agent_set_horse_speed_factor, ":dead_agent_no", 100),
               #for only server itself-----------------------------------------------------------------------------------------------
               (try_for_range, ":player_no", 1, ":num_players"), #0 is server so starting from 1
                 (player_is_active, ":player_no"),
                 (neq, ":my_player_no", ":player_no"),
                 (multiplayer_send_2_int_to_player, ":player_no", multiplayer_event_set_attached_scene_prop, ":dead_agent_no", -1),
               (try_end),

               (prop_instance_get_position, pos0, ":attached_scene_prop"), #moved from above to here after auto-set position
               (position_set_z_to_ground_level, pos0), #moved from above to here after auto-set position
               (prop_instance_set_position, ":attached_scene_prop", pos0), #moved from above to here after auto-set position

               (agent_get_team, ":dead_agent_team", ":dead_agent_no"),
               (try_begin),
                 (eq, ":dead_agent_team", 0),
                 (assign, ":dead_agent_rival_team", 1),
               (else_try),
                 (assign, ":dead_agent_rival_team", 0),
               (try_end),
               (team_set_slot, ":dead_agent_rival_team", slot_team_flag_situation, 2), #2-flag at ground
               (multiplayer_get_my_player, ":my_player_no"),
               (get_max_players, ":num_players"),
               #for only server itself-----------------------------------------------------------------------------------------------
               (call_script, "script_set_team_flag_situation", ":dead_agent_rival_team", 2),
               #for only server itself-----------------------------------------------------------------------------------------------         
               (try_for_range, ":player_no", 1, ":num_players"), #0 is server so starting from 1
                 (player_is_active, ":player_no"),
                 (neq, ":my_player_no", ":player_no"),
                 (multiplayer_send_2_int_to_player, ":player_no", multiplayer_event_set_team_flag_situation, ":dead_agent_rival_team", 2), #flag at ground
               (try_end),
             (try_end),
           (try_end),         
         (try_end),
         ]),

      (1, 0, 0, [], #returning flag if it is not touched by anyone in 60 seconds
       [
         (multiplayer_is_server),
         (try_for_range, ":team_no", 0, 2),           
           (try_begin),
             (team_slot_eq, ":team_no", slot_team_flag_situation, 2),

             (assign, ":flag_team_no", -1),
         
             (try_begin),
               (eq, ":team_no", 0),
               (val_add, "$flag_1_at_ground_timer", 1),
               (ge, "$flag_1_at_ground_timer", multi_max_seconds_flag_can_stay_in_ground),
               (assign, ":flag_team_no", 0),
             (else_try),
               (val_add, "$flag_2_at_ground_timer", 1),
               (ge, "$flag_2_at_ground_timer", multi_max_seconds_flag_can_stay_in_ground), 
               (assign, ":flag_team_no", 1),
             (try_end),

             (try_begin),
               (ge, ":flag_team_no", 0),

               (try_begin),
                 (eq, ":flag_team_no", 0),
                 (assign, "$flag_1_at_ground_timer", 0),
               (else_try),
                 (eq, ":flag_team_no", 1),
                 (assign, "$flag_2_at_ground_timer", 0),
               (try_end),
         
               #cur agent returned his own flag to its default position!
               (team_set_slot, ":flag_team_no", slot_team_flag_situation, 0), #0-flag at base

               #return team flag to its starting position.
               #for only server itself-----------------------------------------------------------------------------------------------
               (call_script, "script_set_team_flag_situation", ":flag_team_no", 0),
               #for only server itself-----------------------------------------------------------------------------------------------         
               (multiplayer_get_my_player, ":my_player_no"),
               (get_max_players, ":num_players"),
               (try_for_range, ":player_no", 1, ":num_players"), #0 is server so starting from 1
                 (player_is_active, ":player_no"),
                 (neq, ":my_player_no", ":player_no"),
                 (multiplayer_send_2_int_to_player, ":player_no", multiplayer_event_set_team_flag_situation, ":flag_team_no", 0),
               (try_end),

               (scene_prop_get_instance, ":flag_red_id", "$team_1_flag_scene_prop", 0),
               (scene_prop_get_instance, ":flag_blue_id", "$team_2_flag_scene_prop", 0),

               (assign, ":team_1_flag_id", ":flag_red_id"),
               (assign, ":team_1_base_entry_id", multi_base_point_team_1),

               (assign, ":team_2_flag_id", ":flag_blue_id"),
               (assign, ":team_2_base_entry_id", multi_base_point_team_2),

               #return team flag to its starting position.
               (try_begin),
                 (eq, ":flag_team_no", 0),
                 (entry_point_get_position, pos5, ":team_1_base_entry_id"), #moved from above to here after auto-set position
                 (prop_instance_set_position, ":team_1_flag_id", pos5), #moved from above to here after auto-set position
               (else_try),
                 (entry_point_get_position, pos5, ":team_2_base_entry_id"), #moved from above to here after auto-set position
                 (prop_instance_set_position, ":team_2_flag_id", pos5), #moved from above to here after auto-set position
               (try_end),

               #(team_get_faction, ":team_faction", ":flag_team_no"),
               #(str_store_faction_name, s1, ":team_faction"),
               #(tutorial_message_set_position, 500, 500),
               #(tutorial_message_set_size, 30, 30),
               #(tutorial_message_set_center_justify, 1),
               #(tutorial_message, "str_s1_returned_flag", 0xFFFFFFFF, 5),

               (store_mul, ":minus_flag_team_no", ":flag_team_no", -1),
               (val_sub, ":minus_flag_team_no", 1),

               #for only server itself
               (call_script, "script_show_multiplayer_message", multiplayer_message_type_flag_returned_home, ":minus_flag_team_no"), 
 
               #no need to send also server here
               (try_for_range, ":player_no", 0, ":num_players"),
                 (player_is_active, ":player_no"),
                 (neq, ":my_player_no", ":player_no"),
                 (multiplayer_send_2_int_to_player, ":player_no", multiplayer_event_show_multiplayer_message, multiplayer_message_type_flag_returned_home, ":minus_flag_team_no"),
               (try_end),
             (try_end),
           (else_try),
             (try_begin),
               (eq, ":team_no", 0),
               (assign, "$flag_1_at_ground_timer", 0),
             (else_try),
               (assign, "$flag_2_at_ground_timer", 0),         
             (try_end),
           (try_end),
         (try_end),           
         ]),
         
      (1, 0, 0, [],
       [
         (multiplayer_is_server),
         (get_max_players, ":num_players"),
         (try_for_range, ":player_no", 0, ":num_players"),
           (player_is_active, ":player_no"),
           (neg|player_is_busy_with_menus, ":player_no"),

           (player_get_team_no, ":player_team", ":player_no"), #if player is currently spectator do not spawn his agent
           (lt, ":player_team", multi_team_spectator),

           (player_get_troop_id, ":player_troop", ":player_no"), #if troop is not selected do not spawn his agent
           (ge, ":player_troop", 0),

           (player_get_agent_id, ":player_agent", ":player_no"),
           (assign, ":spawn_new", 0),
           (try_begin),
             (player_get_slot, ":player_first_spawn", ":player_no", slot_player_first_spawn),
             (eq, ":player_first_spawn", 1),
             (assign, ":spawn_new", 1),
             (player_set_slot, ":player_no", slot_player_first_spawn, 0),
           (else_try),
             (try_begin),
               (lt, ":player_agent", 0),
               (assign, ":spawn_new", 1),
             (else_try),
               (neg|agent_is_alive, ":player_agent"),
               (agent_get_time_elapsed_since_removed, ":elapsed_time", ":player_agent"),
               (gt, ":elapsed_time", "$g_multiplayer_respawn_period"),
               (assign, ":spawn_new", 1),
             (try_end),             
           (try_end),
           (eq, ":spawn_new", 1),
           (call_script, "script_multiplayer_buy_agent_equipment", ":player_no"),

           (troop_get_inventory_slot, ":has_item", ":player_troop", ek_horse),
           (try_begin),
             (ge, ":has_item", 0),
             (assign, ":is_horseman", 1),
           (else_try),
             (assign, ":is_horseman", 0),
           (try_end),

           (call_script, "script_multiplayer_find_spawn_point", ":player_team", 0, ":is_horseman"), 
           (player_spawn_new_agent, ":player_no", reg0),
         (try_end),
         ]),

      (1, 0, 0, [], #do this in every new frame, but not at the same time
       [
         (multiplayer_is_server),
         (store_mission_timer_a, ":mission_timer"),
         (ge, ":mission_timer", 2),
         (assign, ":team_1_count", 0),
         (assign, ":team_2_count", 0),
         (try_for_agents, ":cur_agent"),
           (agent_is_non_player, ":cur_agent"),
           (agent_is_human, ":cur_agent"),
           (assign, ":will_be_counted", 0),
           (try_begin),
             (agent_is_alive, ":cur_agent"),
             (assign, ":will_be_counted", 1), #alive so will be counted
           (else_try),
             (agent_get_time_elapsed_since_removed, ":elapsed_time", ":cur_agent"),
             (le, ":elapsed_time", "$g_multiplayer_respawn_period"),
             (assign, ":will_be_counted", 1), #new died (< g_multiplayer_respawn_period) so will be counted too
           (try_end),
           (eq, ":will_be_counted", 1),
           (agent_get_team, ":cur_team", ":cur_agent"),
           (try_begin),
             (eq, ":cur_team", 0),
             (val_add, ":team_1_count", 1),
           (else_try),
             (eq, ":cur_team", 1),
             (val_add, ":team_2_count", 1),
           (try_end),
         (try_end),
         (store_sub, "$g_multiplayer_num_bots_required_team_1", "$g_multiplayer_num_bots_team_1", ":team_1_count"),
         (store_sub, "$g_multiplayer_num_bots_required_team_2", "$g_multiplayer_num_bots_team_2", ":team_2_count"),
         (val_max, "$g_multiplayer_num_bots_required_team_1", 0),
         (val_max, "$g_multiplayer_num_bots_required_team_2", 0),
         ]),

      multiplayer_server_spawn_bots,
      multiplayer_server_manage_bots,

      (0, 0, 0, [], #control any agent captured flag or made score.
       [
         (multiplayer_is_server),
         (scene_prop_get_instance, ":flag_red_id", "$team_1_flag_scene_prop", 0),
         (prop_instance_get_position, pos1, ":flag_red_id"), #hold position of flag of team 1 (red flag) at pos1

         (scene_prop_get_instance, ":flag_blue_id", "$team_2_flag_scene_prop", 0),
         (prop_instance_get_position, pos2, ":flag_blue_id"), #hold position of flag of team 2 (blue flag) at pos2

         (multiplayer_get_my_player, ":my_player_no"),
         (get_max_players, ":num_players"),                               

         (try_for_agents, ":cur_agent"),
           (agent_is_human, ":cur_agent"), #horses cannot take flag
           (agent_is_alive, ":cur_agent"),
           (neg|agent_is_non_player, ":cur_agent"), #for now bots cannot take flag or return flags to home.
           (agent_get_horse, ":cur_agent_horse", ":cur_agent"),
           (eq, ":cur_agent_horse", -1), #horseman cannot take flag
           (agent_get_attached_scene_prop, ":attached_scene_prop", ":cur_agent"),
         
           (agent_get_team, ":cur_agent_team", ":cur_agent"),
           (try_begin),
             (eq, ":cur_agent_team", 0),
             (assign, ":cur_agent_rival_team", 1),
           (else_try),
             (assign, ":cur_agent_rival_team", 0),
           (try_end),

           (try_begin),
             (eq, ":cur_agent_team", 0), 
             (assign, ":our_flag_id", ":flag_red_id"),
             (assign, ":our_base_entry_id", multi_base_point_team_1),
           (else_try), 
             (assign, ":our_flag_id", ":flag_blue_id"),
             (assign, ":our_base_entry_id", multi_base_point_team_2),
           (try_end),

           (agent_get_position, pos3, ":cur_agent"),
           (prop_instance_get_position, pos4, ":our_flag_id"),
           (get_distance_between_positions, ":dist", pos3, pos4),
           (team_get_slot, ":cur_agent_flag_situation", ":cur_agent_team", slot_team_flag_situation),
         
           (try_begin), #control if agent can return his own flag to default position
             (eq, ":cur_agent_flag_situation", 2), #if our flag is at ground
             (lt, ":dist", 100), #if this agent is near to his team's own flag

             #cur agent returned his own flag to its default position!
             (team_set_slot, ":cur_agent_team", slot_team_flag_situation, 0), #0-flag at base

             #return team flag to its starting position.
             #for only server itself-----------------------------------------------------------------------------------------------
             (call_script, "script_set_team_flag_situation", ":cur_agent_team", 0),
             #for only server itself-----------------------------------------------------------------------------------------------         
             (try_for_range, ":player_no", 1, ":num_players"), #0 is server so starting from 1
               (player_is_active, ":player_no"),
               (neq, ":my_player_no", ":player_no"),
               (multiplayer_send_2_int_to_player, ":player_no", multiplayer_event_set_team_flag_situation, ":cur_agent_team", 0),
             (try_end),

             #return team flag to its starting position.
             (entry_point_get_position, pos5, ":our_base_entry_id"), #moved from above to here after auto-set position
             (prop_instance_set_position, ":our_flag_id", pos5), #moved from above to here after auto-set position

             (try_begin), #give 1 score points to player which returns his/her flag to team base
               (multiplayer_is_server),
               (neg|agent_is_non_player, ":cur_agent"),
               (agent_get_player_id, ":cur_agent_player_id", ":cur_agent"),
               (player_get_score, ":cur_agent_player_score", ":cur_agent_player_id"),
               (val_add, ":cur_agent_player_score", multi_capture_the_flag_score_flag_returning),
               (player_set_score, ":cur_agent_player_id", ":cur_agent_player_score"),
             (try_end),

             #(team_get_faction, ":cur_agent_faction", ":cur_agent_team"),
             #(str_store_faction_name, s1, ":cur_agent_faction"),
             #(tutorial_message_set_position, 500, 500),
             #(tutorial_message_set_size, 30, 30),
             #(tutorial_message_set_center_justify, 1),
             #(tutorial_message, "str_s1_returned_flag", 0xFFFFFFFF, 5),

             #for only server itself
             (call_script, "script_show_multiplayer_message", multiplayer_message_type_flag_returned_home, ":cur_agent"), 

             #no need to send also server here
             (try_for_range, ":player_no", 0, ":num_players"),
               (player_is_active, ":player_no"),
               (neq, ":my_player_no", ":player_no"),
               (multiplayer_send_2_int_to_player, ":player_no", multiplayer_event_show_multiplayer_message, multiplayer_message_type_flag_returned_home, ":cur_agent"),
             (try_end),         
           (try_end),
                   
           (try_begin), #control if agent carries flag and made score
             (neq, ":attached_scene_prop", -1), #if not agent is carrying anything
         
             (try_begin),
               (eq, ":cur_agent_team", 0), 
               (assign, ":rival_flag_id", ":flag_blue_id"),
               (assign, ":rival_base_entry_id", multi_base_point_team_2),
             (else_try), 
               (assign, ":rival_flag_id", ":flag_red_id"),
               (assign, ":rival_base_entry_id", multi_base_point_team_1),
             (try_end),
             
             (eq, ":attached_scene_prop", ":rival_flag_id"), #if agent is carrying rival flag
             (eq, ":cur_agent_flag_situation", 0), #if our flag is at home position         
             (lt, ":dist", 100), #if this agent (carrying rival flag) is near to his team's own

             #cur_agent's team is scored!#
             (team_get_score, ":cur_agent_team_score", ":cur_agent_team"), #this agent's team scored
             (val_add, ":cur_agent_team_score", 1),
             (team_set_score, ":cur_agent_team", ":cur_agent_team_score"),

             (try_begin), #give 5 score points to player which connects two flag and make score to his/her team
               (multiplayer_is_server),
               (neg|agent_is_non_player, ":cur_agent"),
               (agent_get_player_id, ":cur_agent_player_id", ":cur_agent"),
               (player_get_score, ":cur_agent_player_score", ":cur_agent_player_id"),
               (val_add, ":cur_agent_player_score", "$g_multiplayer_point_gained_from_capturing_flag"),
               (player_set_score, ":cur_agent_player_id", ":cur_agent_player_score"),
             (try_end),
         
             #for only server itself-----------------------------------------------------------------------------------------------
             (call_script, "script_team_set_score", ":cur_agent_team", ":cur_agent_team_score"),
             #for only server itself-----------------------------------------------------------------------------------------------
             (try_for_range, ":player_no", 1, ":num_players"), #0 is server so starting from 1
               (player_is_active, ":player_no"),
               (neq, ":my_player_no", ":player_no"),
               (multiplayer_send_2_int_to_player, ":player_no", multiplayer_event_set_team_score, ":cur_agent_team", ":cur_agent_team_score"),
             (try_end),

             (agent_set_attached_scene_prop, ":cur_agent", -1),             
             (team_set_slot, ":cur_agent_rival_team", slot_team_flag_situation, 0), #0-flag at base

             #for only server itself-----------------------------------------------------------------------------------------------
             (call_script, "script_set_attached_scene_prop", ":cur_agent", -1),
             (agent_set_horse_speed_factor, ":cur_agent", 100),
             #for only server itself-----------------------------------------------------------------------------------------------
             (try_for_range, ":player_no", 1, ":num_players"), #0 is server so starting from 1
               (player_is_active, ":player_no"),
               (neq, ":my_player_no", ":player_no"),
               (multiplayer_send_2_int_to_player, ":player_no", multiplayer_event_set_attached_scene_prop, ":cur_agent", -1),
             (try_end),

             #for only server itself-----------------------------------------------------------------------------------------------
             (call_script, "script_set_team_flag_situation", ":cur_agent_rival_team", 0),
             #for only server itself-----------------------------------------------------------------------------------------------         
             (try_for_range, ":player_no", 1, ":num_players"), #0 is server so starting from 1
               (player_is_active, ":player_no"),
               (neq, ":my_player_no", ":player_no"),
               (multiplayer_send_2_int_to_player, ":player_no", multiplayer_event_set_team_flag_situation, ":cur_agent_rival_team", 0),
             (try_end),

             #return rival flag to its starting position
             (entry_point_get_position, pos5, ":rival_base_entry_id"), #moved from above to here after auto-set position
             (prop_instance_set_position, ":rival_flag_id", pos5), #moved from above to here after auto-set position

             #(team_get_faction, ":cur_agent_faction", ":cur_agent_team"),
             #(str_store_faction_name, s1, ":cur_agent_faction"),
             #(player_get_agent_id, ":my_player_agent", ":my_player_no"),
             #(try_begin),
             #  (ge, ":my_player_agent", 0),
             #  (agent_get_team, ":my_player_team", ":my_player_agent"),
             #  (try_begin),
             #    (eq, ":my_player_team", ":cur_agent_team"),
             #    (assign, ":text_font_color", 0xFF33DDFF),
             #  (else_try),
             #    (assign, ":text_font_color", 0xFFFF0000),
             #  (try_end),
             #(else_try),
             #  (assign, ":text_font_color", 0xFFFFFFFF),
             #(try_end),    
             #(tutorial_message_set_position, 500, 500),
             #(tutorial_message_set_size, 30, 30),
             #(tutorial_message_set_center_justify, 1),
             #(tutorial_message, "str_s1_captured_flag", ":text_font_color", 5),

             #for only server itself
             (call_script, "script_show_multiplayer_message", multiplayer_message_type_capture_the_flag_score, ":cur_agent"), 
             
             #no need to send to also server here
             (try_for_range, ":player_no", 0, ":num_players"),
               (player_is_active, ":player_no"),
               (neq, ":my_player_no", ":player_no"),
               (multiplayer_send_2_int_to_player, ":player_no", multiplayer_event_show_multiplayer_message, multiplayer_message_type_capture_the_flag_score, ":cur_agent"),
             (try_end),
           (try_end),
         
           (eq, ":attached_scene_prop", -1), #agents carrying other scene prop cannot take flag.
           (agent_get_position, pos3, ":cur_agent"),
           (agent_get_team, ":cur_agent_team", ":cur_agent"),
           (try_begin),
             (eq, ":cur_agent_team", 0), #if this agent is from team 1, look its distance to blue flag.
             (get_distance_between_positions, ":dist", pos2, pos3),
             (assign, ":rival_flag_id", ":flag_blue_id"),
           (else_try), #if this agent is from team 2, look its distance to red flag.
             (get_distance_between_positions, ":dist", pos1, pos3),
             (assign, ":rival_flag_id", ":flag_red_id"),
           (try_end),

           (try_begin),  #control if agent stole enemy flag
             (le, ":dist", 100),
             (neg|team_slot_eq, ":cur_agent_rival_team", slot_team_flag_situation, 1), #if flag is not already stolen.
             
             (agent_set_attached_scene_prop, ":cur_agent", ":rival_flag_id"),
             (agent_set_attached_scene_prop_x, ":cur_agent", 20),
             (agent_set_attached_scene_prop_z, ":cur_agent", 50),

             (try_begin),
               (eq, ":cur_agent_team", 0),
               (assign, "$flag_1_at_ground_timer", 0),
             (else_try),
               (eq, ":cur_agent_team", 1),
               (assign, "$flag_2_at_ground_timer", 0),
             (try_end),

             #cur_agent stole rival team's flag!
             (team_set_slot, ":cur_agent_rival_team", slot_team_flag_situation, 1), #1-stolen flag
                      
             #for only server itself-----------------------------------------------------------------------------------------------
             (call_script, "script_set_attached_scene_prop", ":cur_agent", ":rival_flag_id"),
             (agent_set_horse_speed_factor, ":cur_agent", 75),
             #for only server itself-----------------------------------------------------------------------------------------------
             (try_for_range, ":player_no", 1, ":num_players"), #0 is server so starting from 1
               (player_is_active, ":player_no"),
               (neq, ":my_player_no", ":player_no"),
               (multiplayer_send_2_int_to_player, ":player_no", multiplayer_event_set_attached_scene_prop, ":cur_agent", ":rival_flag_id"),
             (try_end),
         
             #for only server itself-----------------------------------------------------------------------------------------------
             (call_script, "script_set_team_flag_situation", ":cur_agent_rival_team", 1),
             #for only server itself-----------------------------------------------------------------------------------------------
             (try_for_range, ":player_no", 1, ":num_players"), #0 is server so starting from 1
               (player_is_active, ":player_no"),
               (neq, ":my_player_no", ":player_no"),
               (multiplayer_send_2_int_to_player, ":player_no", multiplayer_event_set_team_flag_situation, ":cur_agent_rival_team", 1),
             (try_end),

             #(team_get_faction, ":cur_agent_faction", ":cur_agent_team"),
             #(str_store_faction_name, s1, ":cur_agent_faction"),
             #(tutorial_message_set_position, 500, 500),
             #(tutorial_message_set_size, 30, 30),
             #(tutorial_message_set_center_justify, 1),
             #(tutorial_message, "str_s1_taken_flag", 0xFFFFFFFF, 5), 

             #for only server itself
             (call_script, "script_show_multiplayer_message", multiplayer_message_type_capture_the_flag_stole, ":cur_agent"), 

             #no need to send also server here
             (try_for_range, ":player_no", 0, ":num_players"),
               (player_is_active, ":player_no"),
               (neq, ":my_player_no", ":player_no"),
               (multiplayer_send_2_int_to_player, ":player_no", multiplayer_event_show_multiplayer_message, multiplayer_message_type_capture_the_flag_stole, ":cur_agent"),
             (try_end),         
           (try_end),
         (try_end),         
         ]),

      (20, 0, 0, [],
       [
         (multiplayer_is_server),
         #auto team balance control in every 10 seconds (cf)
         (call_script, "script_check_team_balance"),
         ]),

      multiplayer_server_check_end_map,
        
      (ti_tab_pressed, 0, 0, [],
       [
         (try_begin),
           (eq, "$g_multiplayer_mission_end_screen", 0),
           (assign, "$g_multiplayer_stats_chart_opened_manually", 1),
           (start_presentation, "prsnt_multiplayer_stats_chart"),
         (try_end),
         ]),

      multiplayer_once_at_the_first_frame,

      (ti_battle_window_opened, 0, 0, [], [
        (start_presentation, "prsnt_multiplayer_team_score_display"),
        (start_presentation, "prsnt_multiplayer_flag_projection_display"),
        ]),

      (ti_escape_pressed, 0, 0, [],
       [
         (neg|is_presentation_active, "prsnt_multiplayer_escape_menu"),
         (neg|is_presentation_active, "prsnt_multiplayer_stats_chart"),
         (eq, "$g_waiting_for_confirmation_to_terminate", 0),
         (start_presentation, "prsnt_multiplayer_escape_menu"),
         ]),
      ],
  ),

    (
    "multiplayer_sg",mtf_battle_mode,-1, #siege
    "You lead your men to battle.",
    [
      (0,mtef_visitor_source|mtef_team_0|mtef_no_auto_reset,0,aif_start_alarmed,1,[]),
      (1,mtef_visitor_source|mtef_team_0|mtef_no_auto_reset,0,aif_start_alarmed,1,[]),
      (2,mtef_visitor_source,0,aif_start_alarmed,1,[]),
      (3,mtef_visitor_source,0,aif_start_alarmed,1,[]),
      (4,mtef_visitor_source,0,aif_start_alarmed,1,[]),
      (5,mtef_visitor_source,0,aif_start_alarmed,1,[]),
      (6,mtef_visitor_source,0,aif_start_alarmed,1,[]),
      (7,mtef_visitor_source,0,aif_start_alarmed,1,[]),

      (8,mtef_visitor_source,0,aif_start_alarmed,1,[]),
      (9,mtef_visitor_source,0,aif_start_alarmed,1,[]),
      (10,mtef_visitor_source,0,aif_start_alarmed,1,[]),
      (11,mtef_visitor_source,0,aif_start_alarmed,1,[]),
      (12,mtef_visitor_source,0,aif_start_alarmed,1,[]),
      (13,mtef_visitor_source,0,aif_start_alarmed,1,[]),
      (14,mtef_visitor_source,0,aif_start_alarmed,1,[]),
      (15,mtef_visitor_source,0,aif_start_alarmed,1,[]),

      (16,mtef_visitor_source,0,aif_start_alarmed,1,[]),
      (17,mtef_visitor_source,0,aif_start_alarmed,1,[]),
      (18,mtef_visitor_source,0,aif_start_alarmed,1,[]),
      (19,mtef_visitor_source,0,aif_start_alarmed,1,[]),
      (20,mtef_visitor_source,0,aif_start_alarmed,1,[]),
      (21,mtef_visitor_source,0,aif_start_alarmed,1,[]),
      (22,mtef_visitor_source,0,aif_start_alarmed,1,[]),
      (23,mtef_visitor_source,0,aif_start_alarmed,1,[]),

      (24,mtef_visitor_source,0,aif_start_alarmed,1,[]),
      (25,mtef_visitor_source,0,aif_start_alarmed,1,[]),
      (26,mtef_visitor_source,0,aif_start_alarmed,1,[]),
      (27,mtef_visitor_source,0,aif_start_alarmed,1,[]),
      (28,mtef_visitor_source,0,aif_start_alarmed,1,[]),
      (29,mtef_visitor_source,0,aif_start_alarmed,1,[]),
      (30,mtef_visitor_source,0,aif_start_alarmed,1,[]),
      (31,mtef_visitor_source,0,aif_start_alarmed,1,[]),

      (32,mtef_visitor_source|mtef_team_1|mtef_no_auto_reset,0,aif_start_alarmed,1,[]),
      (33,mtef_visitor_source|mtef_team_1|mtef_no_auto_reset,0,aif_start_alarmed,1,[]),
      (34,mtef_visitor_source,0,aif_start_alarmed,1,[]),
      (35,mtef_visitor_source,0,aif_start_alarmed,1,[]),
      (36,mtef_visitor_source,0,aif_start_alarmed,1,[]),
      (37,mtef_visitor_source,0,aif_start_alarmed,1,[]),
      (38,mtef_visitor_source,0,aif_start_alarmed,1,[]),
      (39,mtef_visitor_source,0,aif_start_alarmed,1,[]),

      (40,mtef_visitor_source,0,aif_start_alarmed,1,[]),
      (41,mtef_visitor_source,0,aif_start_alarmed,1,[]),
      (42,mtef_visitor_source,0,aif_start_alarmed,1,[]),
      (43,mtef_visitor_source,0,aif_start_alarmed,1,[]),
      (44,mtef_visitor_source,0,aif_start_alarmed,1,[]),
      (45,mtef_visitor_source,0,aif_start_alarmed,1,[]),
      (46,mtef_visitor_source,0,aif_start_alarmed,1,[]),
      (47,mtef_visitor_source,0,aif_start_alarmed,1,[]),

      (48,mtef_visitor_source,0,aif_start_alarmed,1,[]),
      (49,mtef_visitor_source,0,aif_start_alarmed,1,[]),
      (50,mtef_visitor_source,0,aif_start_alarmed,1,[]),
      (51,mtef_visitor_source,0,aif_start_alarmed,1,[]),
      (52,mtef_visitor_source,0,aif_start_alarmed,1,[]),
      (53,mtef_visitor_source,0,aif_start_alarmed,1,[]),
      (54,mtef_visitor_source,0,aif_start_alarmed,1,[]),
      (55,mtef_visitor_source,0,aif_start_alarmed,1,[]),

      (56,mtef_visitor_source,0,aif_start_alarmed,1,[]),
      (57,mtef_visitor_source,0,aif_start_alarmed,1,[]),
      (58,mtef_visitor_source,0,aif_start_alarmed,1,[]),
      (59,mtef_visitor_source,0,aif_start_alarmed,1,[]),
      (60,mtef_visitor_source,0,aif_start_alarmed,1,[]),
      (61,mtef_visitor_source,0,aif_start_alarmed,1,[]),
      (62,mtef_visitor_source,0,aif_start_alarmed,1,[]),
      (63,mtef_visitor_source,0,aif_start_alarmed,1,[]),
     ],
    [
      multiplayer_server_check_belfry_movement,      

      common_battle_init_banner,

      multiplayer_server_check_polls,
      
      (ti_server_player_joined, 0, 0, [],
       [
         (store_trigger_param_1, ":player_no"),
         (call_script, "script_multiplayer_server_player_joined_common", ":player_no"),

         (try_begin),
           (multiplayer_is_server),
           (this_or_next|player_is_active, ":player_no"),
           (eq, ":player_no", 0),
           (store_mission_timer_a, ":round_time"),
           (val_sub, ":round_time", "$g_round_start_time"),
           (try_begin),
             (lt, ":round_time", 25),
             (assign, ":number_of_respawns_spent", 0),
           (else_try),
             (lt, ":round_time", 60),
             (assign, ":number_of_respawns_spent", 1),
           (else_try),
             (lt, ":round_time", 105),
             (assign, ":number_of_respawns_spent", 2),
           (else_try),
             (lt, ":round_time", 160),
             (assign, ":number_of_respawns_spent", 3),
           (else_try),
             (assign, ":number_of_respawns_spent", "$g_multiplayer_number_of_respawn_count"),
           (try_end),
           (player_set_slot, ":player_no", slot_player_spawn_count, ":number_of_respawns_spent"),
           (multiplayer_send_int_to_player, ":player_no", multiplayer_event_return_player_respawn_spent, ":number_of_respawns_spent"),
         (try_end),
         ]),

      (ti_before_mission_start, 0, 0, [],
       [
         (assign, "$g_multiplayer_game_type", multiplayer_game_type_siege),
         (call_script, "script_multiplayer_server_before_mission_start_common"),

         (try_begin),
           (multiplayer_is_server),
           (try_for_range, ":cur_flag_slot", multi_data_flag_pull_code_begin, multi_data_flag_pull_code_end),
             (troop_set_slot, "trp_multiplayer_data", ":cur_flag_slot", -1),
           (try_end),
           (assign, "$g_my_spawn_count", 0),
         (else_try),
           (assign, "$g_my_spawn_count", 0),
         (try_end),
      
         (assign, "$g_waiting_for_confirmation_to_terminate", 0),
         (assign, "$g_round_ended", 0),
         (try_begin),
           (multiplayer_is_server),
           (assign, "$g_round_start_time", 0),
         (try_end),
         (assign, "$my_team_at_start_of_round", -1),

         (assign, "$g_flag_is_not_ready", 0),

         (call_script, "script_multiplayer_initialize_belfry_wheel_rotations"),
         (call_script, "script_multiplayer_init_mission_variables"),
         (call_script, "script_multiplayer_remove_destroy_mod_targets"),
         (call_script, "script_multiplayer_remove_headquarters_flags"),
         ]),

      (ti_after_mission_start, 0, 0, [], 
       [
         (call_script, "script_determine_team_flags", 0),
         (set_spawn_effector_scene_prop_kind, 0, -1), #during this mission, agents of "team 0" will try to spawn around scene props with kind equal to -1(no effector for this mod)
         (set_spawn_effector_scene_prop_kind, 1, -1), #during this mission, agents of "team 1" will try to spawn around scene props with kind equal to -1(no effector for this mod)
         
         (call_script, "script_initialize_all_scene_prop_slots"),
         
         (call_script, "script_multiplayer_move_moveable_objects_initial_positions"),

         (assign, "$g_number_of_flags", 0),
         (try_begin),
           (multiplayer_is_server),
           (assign, "$g_multiplayer_ready_for_spawning_agent", 1),
         
           #place base flags
           (entry_point_get_position, pos1, multi_siege_flag_point),
           (set_spawn_position, pos1),
           (spawn_scene_prop, "spr_headquarters_pole_code_only", 0),         
           (position_move_z, pos1, multi_headquarters_pole_height),         
           (set_spawn_position, pos1),
           (spawn_scene_prop, "$team_1_flag_scene_prop", 0),
           (store_add, ":cur_flag_slot", multi_data_flag_owner_begin, "$g_number_of_flags"),
           (troop_set_slot, "trp_multiplayer_data", ":cur_flag_slot", 1),
         (try_end),
         (val_add, "$g_number_of_flags", 1),

         (try_begin),
           (multiplayer_is_server),
         
           (scene_prop_get_num_instances, ":num_belfries", "spr_belfry_a"),
           (try_for_range, ":belfry_no", 0, ":num_belfries"),
             (scene_prop_get_instance, ":belfry_scene_prop_id", "spr_belfry_a", ":belfry_no"),
             (scene_prop_set_slot, ":belfry_scene_prop_id", scene_prop_belfry_platform_moved, 1),
           (try_end),
         
           (scene_prop_get_num_instances, ":num_belfries", "spr_belfry_b"),
           (try_for_range, ":belfry_no", 0, ":num_belfries"),
             (scene_prop_get_instance, ":belfry_scene_prop_id", "spr_belfry_b", ":belfry_no"),
             (scene_prop_set_slot, ":belfry_scene_prop_id", scene_prop_belfry_platform_moved, 1),
           (try_end),

           (call_script, "script_move_belfries_to_their_first_entry_point", "spr_belfry_a"),
           (call_script, "script_move_belfries_to_their_first_entry_point", "spr_belfry_b"),
         
           (scene_prop_get_num_instances, ":num_belfries", "spr_belfry_a"),
           (try_for_range, ":belfry_no", 0, ":num_belfries"),
             (scene_prop_get_instance, ":belfry_scene_prop_id", "spr_belfry_a", ":belfry_no"),
             (scene_prop_set_slot, ":belfry_scene_prop_id", scene_prop_number_of_agents_pushing, 0),
             (scene_prop_set_slot, ":belfry_scene_prop_id", scene_prop_next_entry_point_id, 0),
           (try_end),
         
           (scene_prop_get_num_instances, ":num_belfries", "spr_belfry_b"),
           (try_for_range, ":belfry_no", 0, ":num_belfries"),
             (scene_prop_get_instance, ":belfry_scene_prop_id", "spr_belfry_b", ":belfry_no"),
             (scene_prop_set_slot, ":belfry_scene_prop_id", scene_prop_number_of_agents_pushing, 0),
             (scene_prop_set_slot, ":belfry_scene_prop_id", scene_prop_next_entry_point_id, 0),
           (try_end),

           (scene_prop_get_num_instances, ":num_belfries", "spr_belfry_a"),
           (try_for_range, ":belfry_no", 0, ":num_belfries"),
             (scene_prop_get_instance, ":belfry_scene_prop_id", "spr_belfry_a", ":belfry_no"),
             (scene_prop_set_slot, ":belfry_scene_prop_id", scene_prop_belfry_platform_moved, 0),
           (try_end),

           (scene_prop_get_num_instances, ":num_belfries", "spr_belfry_b"),
           (try_for_range, ":belfry_no", 0, ":num_belfries"),
             (scene_prop_get_instance, ":belfry_scene_prop_id", "spr_belfry_b", ":belfry_no"),
             (scene_prop_set_slot, ":belfry_scene_prop_id", scene_prop_belfry_platform_moved, 0),
           (try_end),
         (try_end),
         ]),

      (ti_on_agent_spawn, 0, 0, [],
       [
         (store_trigger_param_1, ":agent_no"),
         (call_script, "script_multiplayer_server_on_agent_spawn_common", ":agent_no"),

         (try_begin), #if my initial team still not initialized, find and assign its value.
           (lt, "$my_team_at_start_of_round", 0),
           (multiplayer_get_my_player, ":my_player_no"),
           (ge, ":my_player_no", 0),
           (player_get_agent_id, ":my_agent_id", ":my_player_no"),
           (eq, ":my_agent_id", ":agent_no"),
           (ge, ":my_agent_id", 0),
           (agent_get_team, "$my_team_at_start_of_round", ":my_agent_id"),
         (try_end),

         (try_begin),
           (neg|multiplayer_is_server),
           (try_begin),
             (eq, "$g_round_ended", 1),
             (assign, "$g_round_ended", 0),
             (assign, "$g_my_spawn_count", 0),

             #initialize scene object slots at start of new round at clients.
             (call_script, "script_initialize_all_scene_prop_slots"),

             #these lines are done in only clients at start of each new round.
             (call_script, "script_multiplayer_initialize_belfry_wheel_rotations"),
             (call_script, "script_initialize_objects_clients"),
             #end of lines
           (try_end),  
         (try_end),         

         (try_begin), 
           (multiplayer_get_my_player, ":my_player_no"),
           (ge, ":my_player_no", 0),
           (player_get_agent_id, ":my_agent_id", ":my_player_no"),
           (eq, ":my_agent_id", ":agent_no"),

           (val_add, "$g_my_spawn_count", 1),
         
           (try_begin),
             (ge, "$g_my_spawn_count", "$g_multiplayer_number_of_respawn_count"),
             (gt, "$g_multiplayer_number_of_respawn_count", 0),
             (multiplayer_get_my_player, ":my_player_no"),
             (player_get_team_no, ":my_player_team_no", ":my_player_no"),
             (eq, ":my_player_team_no", 0),
             (assign, "$g_my_spawn_count", 999),
           (try_end),
         (try_end),
         ]),

      (ti_on_agent_killed_or_wounded, 0, 0, [],
       [
         (store_trigger_param_1, ":dead_agent_no"),
         (store_trigger_param_2, ":killer_agent_no"),

         (call_script, "script_multiplayer_server_on_agent_killed_or_wounded_common", ":dead_agent_no", ":killer_agent_no"),

         (try_begin), #if my initial team still not initialized, find and assign its value.
           (lt, "$my_team_at_start_of_round", 0),
           (multiplayer_get_my_player, ":my_player_no"),
           (ge, ":my_player_no", 0),
           (player_get_agent_id, ":my_agent_id", ":my_player_no"),
           (ge, ":my_agent_id", 0),
           (agent_get_team, "$my_team_at_start_of_round", ":my_agent_id"),
         (try_end),         
         
         (try_begin),
           (multiplayer_is_server),
           (agent_is_human, ":dead_agent_no"),
           (neg|agent_is_non_player, ":dead_agent_no"),
           (agent_get_player_id, ":dead_agent_player_id", ":dead_agent_no"),
           (player_set_slot, ":dead_agent_player_id", slot_player_spawned_this_round, 0),
         (try_end),
         ]),

      (ti_on_multiplayer_mission_end, 0, 0, [],
       [
         (call_script, "script_multiplayer_event_mission_end"),
         (assign, "$g_multiplayer_stats_chart_opened_manually", 0),
         (start_presentation, "prsnt_multiplayer_stats_chart"),
         ]),
      
      (0, 0, 0, [], #if this trigger takes lots of time in the future and make server machine runs siege mod
                    #very slow with lots of players make period of this trigger 1 seconds, but best is 0. Currently
                    #we are testing this mod with few players and no speed problem occured.
      [
        (multiplayer_is_server),
        (eq, "$g_round_ended", 0),
        #main trigger which controls which agent is moving/near which flag.
        (try_for_range, ":flag_no", 0, "$g_number_of_flags"),
          (store_add, ":cur_flag_owner_counts_slot", multi_data_flag_players_around_begin, ":flag_no"),
          (troop_get_slot, ":current_owner_code", "trp_multiplayer_data", ":cur_flag_owner_counts_slot"),
          (store_div, ":old_team_1_agent_count", ":current_owner_code", 100),
          (store_mod, ":old_team_2_agent_count", ":current_owner_code", 100),
        
          (assign, ":number_of_agents_around_flag_team_1", 0),
          (assign, ":number_of_agents_around_flag_team_2", 0),

          (scene_prop_get_instance, ":pole_id", "spr_headquarters_pole_code_only", ":flag_no"), 
          (prop_instance_get_position, pos0, ":pole_id"), #pos0 holds pole position.

          (get_max_players, ":num_players"),
            (try_for_range, ":player_no", 0, ":num_players"),
            (player_is_active, ":player_no"),
            (player_get_agent_id, ":cur_agent", ":player_no"),            
            (ge, ":cur_agent", 0),
            (agent_is_alive, ":cur_agent"),
            (agent_get_team, ":cur_agent_team", ":cur_agent"),
            (agent_get_position, pos1, ":cur_agent"), #pos1 holds agent's position.
            (get_sq_distance_between_positions, ":squared_dist", pos0, pos1),
            (get_sq_distance_between_position_heights, ":squared_height_dist", pos0, pos1),
            (val_add, ":squared_dist", ":squared_height_dist"),
            (lt, ":squared_dist", multi_headquarters_max_distance_sq_to_raise_flags),
            (try_begin),
              (eq, ":cur_agent_team", 0),
              (val_add, ":number_of_agents_around_flag_team_1", 1),
            (else_try),
              (eq, ":cur_agent_team", 1),
              (val_add, ":number_of_agents_around_flag_team_2", 1),
            (try_end),
          (try_end),

          (try_begin),
            (this_or_next|neq, ":old_team_1_agent_count", ":number_of_agents_around_flag_team_1"),
            (neq, ":old_team_2_agent_count", ":number_of_agents_around_flag_team_2"),

            (store_add, ":cur_flag_pull_code_slot", multi_data_flag_pull_code_begin, ":flag_no"),
            (troop_get_slot, ":cur_flag_pull_code", "trp_multiplayer_data", ":cur_flag_pull_code_slot"),
            (store_mod, ":cur_flag_pull_message_seconds_past", ":cur_flag_pull_code", 100),
            (store_div, ":cur_flag_puller_team_last", ":cur_flag_pull_code", 100),

            (try_begin),        
              (eq, ":old_team_2_agent_count", 0),
              (gt, ":number_of_agents_around_flag_team_2", 0),
              (eq, ":number_of_agents_around_flag_team_1", 0),
              (assign, ":puller_team", 2),

              (store_mul, ":puller_team_multiplied_by_100", ":puller_team", 100),
              (troop_set_slot, "trp_multiplayer_data", ":cur_flag_pull_code_slot", ":puller_team_multiplied_by_100"),

              (this_or_next|neq, ":cur_flag_puller_team_last", ":puller_team"),
              (ge, ":cur_flag_pull_message_seconds_past", 25),

              (store_mul, ":flag_code", ":puller_team", 100),
              (val_add, ":flag_code", ":flag_no"),
            (try_end),

            (try_begin),
              (store_mul, ":current_owner_code", ":number_of_agents_around_flag_team_1", 100),
              (val_add, ":current_owner_code", ":number_of_agents_around_flag_team_2"),        
              (troop_set_slot, "trp_multiplayer_data", ":cur_flag_owner_counts_slot", ":current_owner_code"),
              (get_max_players, ":num_players"),
              #for only server itself-----------------------------------------------------------------------------------------------
              (call_script, "script_set_num_agents_around_flag", ":flag_no", ":current_owner_code"),
              #for only server itself-----------------------------------------------------------------------------------------------
              (try_for_range, ":player_no", 1, ":num_players"), #0 is server so starting from 1
                (player_is_active, ":player_no"),
                (multiplayer_send_2_int_to_player, ":player_no", multiplayer_event_set_num_agents_around_flag, ":flag_no", ":current_owner_code"),
              (try_end),
            (try_end),
          (try_end),
        (try_end),

        (try_for_range, ":flag_no", 0, "$g_number_of_flags"),
          (eq, "$g_round_ended", 0), #if round still continues and any team did not sucseed yet
          (eq, "$g_flag_is_not_ready", 0), #if round still continues and any team did not sucseed yet
        
          (scene_prop_get_instance, ":pole_id", "spr_headquarters_pole_code_only", ":flag_no"), 
          (prop_instance_get_position, pos0, ":pole_id"), #pos0 holds pole position.            

          (try_begin),
            (scene_prop_get_instance, ":flag_id", "$team_1_flag_scene_prop", ":flag_no"),

            #flag_id holds shown flag after this point
            (prop_instance_get_position, pos1, ":flag_id"), #pos1 holds gray/red/blue (current shown) flag position.
            (try_begin),
              (get_sq_distance_between_positions, ":squared_dist", pos0, pos1),        
              (lt, ":squared_dist", multi_headquarters_distance_sq_to_change_flag), #if distance is less than 2 meters
              
              (prop_instance_is_animating, ":is_animating", ":flag_id"),
              (eq, ":is_animating", 1),

              #end of round, attackers win
              (assign, "$g_winner_team", 1),
              (prop_instance_stop_animating, ":flag_id"),        
        
              (get_max_players, ":num_players"), 
              #for only server itself-----------------------------------------------------------------------------------------------
              (call_script, "script_draw_this_round", "$g_winner_team"),
              #for only server itself-----------------------------------------------------------------------------------------------
              (try_for_range, ":player_no", 1, ":num_players"), #0 is server so starting from 1
                (player_is_active, ":player_no"),
                (multiplayer_send_int_to_player, ":player_no", multiplayer_event_draw_this_round, "$g_winner_team"),
              (try_end),

              (assign, "$g_flag_is_not_ready", 1),
            (try_end),        
          (try_end),
        (try_end),
        ]),

      (0, 0, 0, [], #if there is nobody in any teams do not reduce round time.
       [
         #(multiplayer_is_server),
         (assign, ":human_agents_spawned_at_team_1", "$g_multiplayer_num_bots_team_1"),
         (assign, ":human_agents_spawned_at_team_2", "$g_multiplayer_num_bots_team_2"),
         
         (get_max_players, ":num_players"),
         (try_for_range, ":player_no", 0, ":num_players"),
           (player_is_active, ":player_no"),
           (player_get_team_no, ":player_team", ":player_no"), 
           (try_begin),
             (eq, ":player_team", 0),
             (val_add, ":human_agents_spawned_at_team_1", 1),
           (else_try),
             (eq, ":player_team", 1),
             (val_add, ":human_agents_spawned_at_team_2", 1),
           (try_end),
         (try_end),

         (try_begin),
           (this_or_next|eq, ":human_agents_spawned_at_team_1", 0),
           (eq, ":human_agents_spawned_at_team_2", 0),

           (store_mission_timer_a, ":seconds_past_since_round_started"),
           (val_sub, ":seconds_past_since_round_started", "$g_round_start_time"),
           (le, ":seconds_past_since_round_started", 2),
                  
           (store_mission_timer_a, "$g_round_start_time"),
         (try_end),
       ]),

      (1, 0, 0, [(multiplayer_is_server),
                 (eq, "$g_round_ended", 0),
                 (eq, "$g_flag_is_not_ready", 0),
                 (store_mission_timer_a, ":current_time"),
                 (store_sub, ":seconds_past_in_round", ":current_time", "$g_round_start_time"),
                 (ge, ":seconds_past_in_round", "$g_multiplayer_round_max_seconds")],
       [
         (assign, ":flag_no", 0),
         (store_add, ":cur_flag_owner_counts_slot", multi_data_flag_players_around_begin, ":flag_no"),
         (troop_get_slot, ":current_owner_code", "trp_multiplayer_data", ":cur_flag_owner_counts_slot"),
         (store_mod, ":team_2_agent_count_around_flag", ":current_owner_code", 100),

         (try_begin),
           (eq, ":team_2_agent_count_around_flag", 0),
         
           (store_mission_timer_a, "$g_round_finish_time"),
           (assign, "$g_round_ended", 1),

           (assign, "$g_flag_is_not_ready", 1),
        
           (assign, "$g_winner_team", 0),

           (get_max_players, ":num_players"),
           #for only server itself-----------------------------------------------------------------------------------------------
           (call_script, "script_draw_this_round", "$g_winner_team"),
           #for only server itself-----------------------------------------------------------------------------------------------
           (try_for_range, ":player_no", 1, ":num_players"), #0 is server so starting from 1
             (player_is_active, ":player_no"),
             (multiplayer_send_int_to_player, ":player_no", multiplayer_event_draw_this_round, "$g_winner_team"),
           (try_end),
         (try_end),
         ]),          

      (1, 0, 0, [],
      [
        (multiplayer_is_server),
        #trigger for calculating seconds past after that flag's pull message has shown          
        (try_for_range, ":flag_no", 0, "$g_number_of_flags"),
          (store_add, ":cur_flag_pull_code_slot", multi_data_flag_pull_code_begin, ":flag_no"),
          (troop_get_slot, ":cur_flag_pull_code", "trp_multiplayer_data", ":cur_flag_pull_code_slot"),
          (store_mod, ":cur_flag_pull_message_seconds_past", ":cur_flag_pull_code", 100),
          (try_begin),
            (ge, ":cur_flag_pull_code", 100),
            (lt, ":cur_flag_pull_message_seconds_past", 25),
            (val_add, ":cur_flag_pull_code", 1),
            (troop_set_slot, "trp_multiplayer_data", ":cur_flag_pull_code_slot", ":cur_flag_pull_code"),
          (try_end),
        (try_end),        
      ]),               

      (10, 0, 0, [(multiplayer_is_server)],
       [
         #auto team balance control during the round         
         (assign, ":number_of_players_at_team_1", 0),
         (assign, ":number_of_players_at_team_2", 0),
         (get_max_players, ":num_players"),
         (try_for_range, ":cur_player", 0, ":num_players"),
           (player_is_active, ":cur_player"),
           (player_get_team_no, ":player_team", ":cur_player"),
           (try_begin),
             (eq, ":player_team", 0),
             (val_add, ":number_of_players_at_team_1", 1),
           (else_try),
             (eq, ":player_team", 1),
             (val_add, ":number_of_players_at_team_2", 1),
           (try_end),         
         (try_end),
         #end of counting active players per team.
         (store_sub, ":difference_of_number_of_players", ":number_of_players_at_team_1", ":number_of_players_at_team_2"),
         (assign, ":number_of_players_will_be_moved", 0),
         (try_begin),
           (try_begin),
             (store_mul, ":checked_value", "$g_multiplayer_auto_team_balance_limit", -1),
             (le, ":difference_of_number_of_players", ":checked_value"),
             (store_div, ":number_of_players_will_be_moved", ":difference_of_number_of_players", -2),
           (else_try),
             (ge, ":difference_of_number_of_players", "$g_multiplayer_auto_team_balance_limit"),
             (store_div, ":number_of_players_will_be_moved", ":difference_of_number_of_players", 2),
           (try_end),          
         (try_end),         
         #number of players will be moved calculated. (it is 0 if no need to make team balance)
         (try_begin),
           (gt, ":number_of_players_will_be_moved", 0),
           (try_begin),
             (eq, "$g_team_balance_next_round", 0),
         
             (assign, "$g_team_balance_next_round", 1),

             #for only server itself-----------------------------------------------------------------------------------------------
             (call_script, "script_show_multiplayer_message", multiplayer_message_type_auto_team_balance_next, 0), #0 is useless here
             #for only server itself-----------------------------------------------------------------------------------------------     
             (get_max_players, ":num_players"),                               
             (try_for_range, ":player_no", 1, ":num_players"), #0 is server so starting from 1
               (player_is_active, ":player_no"),
               (multiplayer_send_int_to_player, ":player_no", multiplayer_event_show_multiplayer_message, multiplayer_message_type_auto_team_balance_next),
             (try_end),
             
             (call_script, "script_warn_player_about_auto_team_balance"),
           (try_end),
         (try_end),           
         #team balance check part finished
         ]),          

      (1, 0, 3, [(multiplayer_is_server),
                 (eq, "$g_round_ended", 1),
                 (store_mission_timer_a, ":seconds_past_till_round_ended"),
                 (val_sub, ":seconds_past_till_round_ended", "$g_round_finish_time"),
                 (ge, ":seconds_past_till_round_ended", "$g_multiplayer_respawn_period")],
       [
         #auto team balance control at the end of round         
         (assign, ":number_of_players_at_team_1", 0),
         (assign, ":number_of_players_at_team_2", 0),
         (get_max_players, ":num_players"),
         (try_for_range, ":cur_player", 0, ":num_players"),
           (player_is_active, ":cur_player"),
           (player_get_team_no, ":player_team", ":cur_player"),
           (try_begin),
             (eq, ":player_team", 0),
             (val_add, ":number_of_players_at_team_1", 1),
           (else_try),
             (eq, ":player_team", 1),
             (val_add, ":number_of_players_at_team_2", 1),
           (try_end),         
         (try_end),
         #end of counting active players per team.
         (store_sub, ":difference_of_number_of_players", ":number_of_players_at_team_1", ":number_of_players_at_team_2"),
         (assign, ":number_of_players_will_be_moved", 0),
         (try_begin),
           (try_begin),
             (store_mul, ":checked_value", "$g_multiplayer_auto_team_balance_limit", -1),
             (le, ":difference_of_number_of_players", ":checked_value"),
             (store_div, ":number_of_players_will_be_moved", ":difference_of_number_of_players", -2),
             (assign, ":team_with_more_players", 1),
             (assign, ":team_with_less_players", 0),
           (else_try),
             (ge, ":difference_of_number_of_players", "$g_multiplayer_auto_team_balance_limit"),
             (store_div, ":number_of_players_will_be_moved", ":difference_of_number_of_players", 2),
             (assign, ":team_with_more_players", 0),
             (assign, ":team_with_less_players", 1),
           (try_end),          
         (try_end),         
         #number of players will be moved calculated. (it is 0 if no need to make team balance)
         (try_begin),
           (gt, ":number_of_players_will_be_moved", 0),
           (try_begin),
             (try_for_range, ":unused", 0, ":number_of_players_will_be_moved"), 
               (assign, ":max_player_join_time", 0),
               (assign, ":latest_joined_player_no", -1),
               (get_max_players, ":num_players"),                               
               (try_for_range, ":player_no", 0, ":num_players"),
                 (player_is_active, ":player_no"),
                 (player_get_team_no, ":player_team", ":player_no"),
                 (eq, ":player_team", ":team_with_more_players"),
                 (player_get_slot, ":player_join_time", ":player_no", slot_player_join_time),
                 (try_begin),
                   (gt, ":player_join_time", ":max_player_join_time"),
                   (assign, ":max_player_join_time", ":player_join_time"),
                   (assign, ":latest_joined_player_no", ":player_no"),
                 (try_end),
               (try_end),
               (try_begin),
                 (ge, ":latest_joined_player_no", 0),
                 (try_begin),
                   #if player is living add +1 to his kill count because he will get -1 because of team change while living.
                   (player_get_agent_id, ":latest_joined_agent_id", ":latest_joined_player_no"), 
                   (ge, ":latest_joined_agent_id", 0),
                   (agent_is_alive, ":latest_joined_agent_id"),

                   (player_get_kill_count, ":player_kill_count", ":latest_joined_player_no"), #adding 1 to his kill count, because he will lose 1 undeserved kill count for dying during team change
                   (val_add, ":player_kill_count", 1),
                   (player_set_kill_count, ":latest_joined_player_no", ":player_kill_count"),

                   (player_get_death_count, ":player_death_count", ":latest_joined_player_no"), #subtracting 1 to his death count, because he will gain 1 undeserved death count for dying during team change
                   (val_sub, ":player_death_count", 1),
                   (player_set_death_count, ":latest_joined_player_no", ":player_death_count"),

                   (player_get_score, ":player_score", ":latest_joined_player_no"), #adding 1 to his score count, because he will lose 1 undeserved score for dying during team change
                   (val_add, ":player_score", 1),
                   (player_set_score, ":latest_joined_player_no", ":player_score"),

                   (try_for_range, ":player_no", 1, ":num_players"), #0 is server so starting from 1
                     (player_is_active, ":player_no"),
                     (multiplayer_send_4_int_to_player, ":player_no", multiplayer_event_set_player_score_kill_death, ":latest_joined_player_no", ":player_score", ":player_kill_count", ":player_death_count"),
                   (try_end),         

                   (player_get_value_of_original_items, ":old_items_value", ":latest_joined_player_no"),
                   (player_get_gold, ":player_gold", ":latest_joined_player_no"),
                   (val_add, ":player_gold", ":old_items_value"),
                   (player_set_gold, ":latest_joined_player_no", ":player_gold", multi_max_gold_that_can_be_stored),
                 (end_try),

                 (player_set_troop_id, ":latest_joined_player_no", -1),
                 (player_set_team_no, ":latest_joined_player_no", ":team_with_less_players"),
                 (multiplayer_send_message_to_player, ":latest_joined_player_no", multiplayer_event_force_start_team_selection),
               (try_end),
             (try_end),
             #tutorial message (after team balance)
             
             #(tutorial_message_set_position, 500, 500),
             #(tutorial_message_set_size, 30, 30),
             #(tutorial_message_set_center_justify, 1),
             #(tutorial_message, "str_auto_team_balance_done", 0xFFFFFFFF, 5),
             
             #for only server itself
             (call_script, "script_show_multiplayer_message", multiplayer_message_type_auto_team_balance_done, 0), 

             #no need to send also server here
             (multiplayer_get_my_player, ":my_player_no"),
             (get_max_players, ":num_players"),                               
             (try_for_range, ":player_no", 0, ":num_players"),
               (player_is_active, ":player_no"),
               (neq, ":my_player_no", ":player_no"),
               (multiplayer_send_int_to_player, ":player_no", multiplayer_event_show_multiplayer_message, multiplayer_message_type_auto_team_balance_done),
             (try_end),
             (assign, "$g_team_balance_next_round", 0),
           (try_end),
         (try_end),           
         #team balance check part finished
         (assign, "$g_team_balance_next_round", 0),

         (get_max_players, ":num_players"),
         (try_for_range, ":player_no", 0, ":num_players"),
           (player_is_active, ":player_no"),
           (player_set_slot, ":player_no", slot_player_spawned_this_round, 0),
           (player_set_slot, ":player_no", slot_player_spawned_at_siege_round, 0),           
           (player_get_agent_id, ":player_agent", ":player_no"),
           (ge, ":player_agent", 0),
           (agent_is_alive, ":player_agent"),
           (player_save_picked_up_items_for_next_spawn, ":player_no"),
           (player_get_value_of_original_items, ":old_items_value", ":player_no"),
           (player_set_slot, ":player_no", slot_player_last_rounds_used_item_earnings, ":old_items_value"),
         (try_end),

         #money management
         (assign, ":per_round_gold_addition", multi_battle_round_team_money_add),
         (val_mul, ":per_round_gold_addition", "$g_multiplayer_round_earnings_multiplier"),
         (val_div, ":per_round_gold_addition", 100),
         (get_max_players, ":num_players"),
         (try_for_range, ":player_no", 0, ":num_players"),
           (player_is_active, ":player_no"),
           (player_get_gold, ":player_gold", ":player_no"),
           (player_get_team_no, ":player_team", ":player_no"),
         
           (try_begin),
             (this_or_next|eq, ":player_team", 0),
             (eq, ":player_team", 1),
             (val_add, ":player_gold", ":per_round_gold_addition"), 
           (try_end),

           #(below lines added new at 25.11.09 after Armagan decided new money system)
           (try_begin),
             (player_get_slot, ":old_items_value", ":player_no", slot_player_last_rounds_used_item_earnings),
             (store_add, ":player_total_potential_gold", ":player_gold", ":old_items_value"),
             (store_mul, ":minimum_gold", "$g_multiplayer_initial_gold_multiplier", 10),
             (lt, ":player_total_potential_gold", ":minimum_gold"),
             (store_sub, ":additional_gold", ":minimum_gold", ":player_total_potential_gold"),
             (val_add, ":player_gold", ":additional_gold"),
           (try_end),
           #new money system addition end

           (player_set_gold, ":player_no", ":player_gold", multi_max_gold_that_can_be_stored),
         (try_end),

         #initialize my team at start of round (it will be assigned again at next round's first death)
         (assign, "$my_team_at_start_of_round", -1),

         #clear scene and end round
         (multiplayer_clear_scene),
         
         #assigning everbody's spawn counts to 0
         (assign, "$g_my_spawn_count", 0),
         (get_max_players, ":num_players"),
         (try_for_range, ":player_no", 0, ":num_players"),
           (player_is_active, ":player_no"),
           (player_set_slot, ":player_no", slot_player_spawn_count, 0),
         (try_end),

         #(call_script, "script_multiplayer_initialize_belfry_wheel_rotations"),
         (call_script, "script_initialize_objects"),

         #initialize moveable object positions
         (call_script, "script_multiplayer_initialize_belfry_wheel_rotations"),
         (call_script, "script_multiplayer_close_gate_if_it_is_open"),
         (call_script, "script_multiplayer_move_moveable_objects_initial_positions"),
         (call_script, "script_move_belfries_to_their_first_entry_point", "spr_belfry_a"),
         (call_script, "script_move_belfries_to_their_first_entry_point", "spr_belfry_b"),
         
         (scene_prop_get_num_instances, ":num_belfries", "spr_belfry_a"),
         (try_for_range, ":belfry_no", 0, ":num_belfries"),
           (scene_prop_get_instance, ":belfry_scene_prop_id", "spr_belfry_a", ":belfry_no"),
           (scene_prop_set_slot, ":belfry_scene_prop_id", scene_prop_number_of_agents_pushing, 0),
           (scene_prop_set_slot, ":belfry_scene_prop_id", scene_prop_next_entry_point_id, 0),
         (try_end),

         (scene_prop_get_num_instances, ":num_belfries", "spr_belfry_a"),
         (try_for_range, ":belfry_no", 0, ":num_belfries"),
           (scene_prop_get_instance, ":belfry_scene_prop_id", "spr_belfry_a", ":belfry_no"),
           (scene_prop_set_slot, ":belfry_scene_prop_id", scene_prop_belfry_platform_moved, 0),
         (try_end),

         (scene_prop_get_num_instances, ":num_belfries", "spr_belfry_b"),
         (try_for_range, ":belfry_no", 0, ":num_belfries"),
           (scene_prop_get_instance, ":belfry_scene_prop_id", "spr_belfry_b", ":belfry_no"),
           (scene_prop_set_slot, ":belfry_scene_prop_id", scene_prop_number_of_agents_pushing, 0),
           (scene_prop_set_slot, ":belfry_scene_prop_id", scene_prop_next_entry_point_id, 0),
         (try_end),

         (scene_prop_get_num_instances, ":num_belfries", "spr_belfry_b"),
         (try_for_range, ":belfry_no", 0, ":num_belfries"),
           (scene_prop_get_instance, ":belfry_scene_prop_id", "spr_belfry_b", ":belfry_no"),
           (scene_prop_set_slot, ":belfry_scene_prop_id", scene_prop_belfry_platform_moved, 0),
         (try_end),

         #initialize flag coordinates (move up the flag at pole)
         (try_for_range, ":flag_no", 0, "$g_number_of_flags"),
           (scene_prop_get_instance, ":pole_id", "spr_headquarters_pole_code_only", ":flag_no"),
           (prop_instance_get_position, pos1, ":pole_id"),
           (position_move_z, pos1, multi_headquarters_pole_height),
           (scene_prop_get_instance, ":flag_id", "$team_1_flag_scene_prop", ":flag_no"),
           (prop_instance_stop_animating, ":flag_id"),
           (prop_instance_set_position, ":flag_id", pos1),
         (try_end),
         
         (assign, "$g_round_ended", 0),
         
         (store_mission_timer_a, "$g_round_start_time"),
         (call_script, "script_initialize_all_scene_prop_slots"),

         #initialize round start time for clients
         (get_max_players, ":num_players"),
         (try_for_range, ":player_no", 0, ":num_players"),
           (player_is_active, ":player_no"),
           (multiplayer_send_int_to_player, ":player_no", multiplayer_event_set_round_start_time, -9999),
         (try_end),         

         (assign, "$g_flag_is_not_ready", 0),
       ]),
           
      (1, 0, 0, [],
       [
         (multiplayer_is_server),
         (get_max_players, ":num_players"),
         (try_for_range, ":player_no", 0, ":num_players"),
           (player_is_active, ":player_no"),
           (neg|player_is_busy_with_menus, ":player_no"),
           (player_slot_eq, ":player_no", slot_player_spawned_this_round, 0),

           (player_get_team_no, ":player_team", ":player_no"), #if player is currently spectator do not spawn his agent
           (lt, ":player_team", multi_team_spectator),
           (player_get_troop_id, ":player_troop", ":player_no"), #if troop is not selected do not spawn his agent
           (ge, ":player_troop", 0),
           (player_get_agent_id, ":player_agent", ":player_no"), #new added for siege mod
         
           (assign, ":spawn_new", 0), 
           (assign, ":num_active_players_in_team_0", 0),
           (assign, ":num_active_players_in_team_1", 0),
           (try_begin),
             (assign, ":num_active_players", 0),
             (get_max_players, ":num_players"),
             (try_for_range, ":cur_player", 0, ":num_players"),
               (player_is_active, ":cur_player"),

               (player_get_team_no, ":cur_player_team", ":cur_player"),
               (try_begin),
                 (eq, ":cur_player_team", 0),
                 (val_add, ":num_active_players_in_team_0", 1),
               (else_try),
                 (eq, ":cur_player_team", 1),
                 (val_add, ":num_active_players_in_team_1", 1),
               (try_end),

               (val_add, ":num_active_players", 1),
             (try_end),
             (store_mission_timer_a, ":round_time"),
             (val_sub, ":round_time", "$g_round_start_time"),
                  
             (eq, "$g_round_ended", 0),
         
             (try_begin), #addition for siege mod to allow players spawn more than once (begin)
               (lt, ":player_agent", 0), 

               (try_begin), #new added begin, to avoid siege-crack (rejoining of defenders when they die)
                 (eq, ":player_team", 0), 
                 (player_get_slot, ":player_last_team_select_time", ":player_no", slot_player_last_team_select_time),
                 (store_mission_timer_a, ":current_time"),
                 (store_sub, ":elapsed_time", ":current_time", ":player_last_team_select_time"),
                 
                 (assign, ":player_team_respawn_period", "$g_multiplayer_respawn_period"), 
                 (val_add, ":player_team_respawn_period", multiplayer_siege_mod_defender_team_extra_respawn_time), #new added for siege mod
                 (lt, ":elapsed_time", ":player_team_respawn_period"),

                 (store_sub, ":round_time", ":current_time", "$g_round_start_time"),
                 (ge, ":round_time", multiplayer_new_agents_finish_spawning_time),
                 (gt, ":num_active_players", 2),
                 (store_mul, ":multipication_of_num_active_players_in_teams", ":num_active_players_in_team_0", ":num_active_players_in_team_1"),
                 (neq, ":multipication_of_num_active_players_in_teams", 0),
         
                 (assign, ":spawn_new", 0),
               (else_try), #new added end         
                 (assign, ":spawn_new", 1),
               (try_end),
             (else_try), 
               (agent_get_time_elapsed_since_removed, ":elapsed_time", ":player_agent"), 
               (assign, ":player_team_respawn_period", "$g_multiplayer_respawn_period"), 
               (try_begin), 
                 (eq, ":player_team", 0), 
                 (val_add, ":player_team_respawn_period", multiplayer_siege_mod_defender_team_extra_respawn_time), 
               (try_end), 
               (this_or_next|gt, ":elapsed_time", ":player_team_respawn_period"), 
               (player_slot_eq, ":player_no", slot_player_spawned_at_siege_round, 0), 
               (assign, ":spawn_new", 1),
             (try_end), 
           (try_end), #addition for siege mod to allow players spawn more than once (end)

           (player_get_slot, ":spawn_count", ":player_no", slot_player_spawn_count),

           (try_begin),
             (gt, "$g_multiplayer_number_of_respawn_count", 0),
             (try_begin),
               (eq, ":spawn_new", 1),
               (eq, ":player_team", 0),
               (ge, ":spawn_count", "$g_multiplayer_number_of_respawn_count"),
               (assign, ":spawn_new", 0),
             (else_try),
               (eq, ":spawn_new", 1),
               (eq, ":player_team", 1),      
               (ge, ":spawn_count", 999),
               (assign, ":spawn_new", 0),
             (try_end),
           (try_end),

           (eq, ":spawn_new", 1),

           (call_script, "script_multiplayer_buy_agent_equipment", ":player_no"),

           (player_get_slot, ":spawn_count", ":player_no", slot_player_spawn_count),
           (val_add, ":spawn_count", 1),
           (player_set_slot, ":player_no", slot_player_spawn_count, ":spawn_count"),

           (try_begin),
             (ge, ":spawn_count", "$g_multiplayer_number_of_respawn_count"),
             (gt, "$g_multiplayer_number_of_respawn_count", 0),
             (eq, ":player_team", 0),
             (assign, ":spawn_count", 999),
             (player_set_slot, ":player_no", slot_player_spawn_count, ":spawn_count"),
           (try_end),

           (assign, ":player_is_horseman", 0),
           (player_get_item_id, ":item_id", ":player_no", ek_horse),
           (try_begin),
             (this_or_next|is_between, ":item_id", horses_begin, horses_end),
             (this_or_next|eq, ":item_id", "itm_warhorse_sarranid"),
             (eq, ":item_id", "itm_warhorse_steppe"),
             (assign, ":player_is_horseman", 1),
           (try_end),

           (try_begin),
             (lt, ":round_time", 20), #at start of game spawn at base entry point (only enemies)
             (try_begin),         
               (eq, ":player_team", 0), #defenders in siege mod at start of round
               (call_script, "script_multiplayer_find_spawn_point", ":player_team", 1, ":player_is_horseman"),
               (assign, ":entry_no", reg0),             
             (else_try),
               (eq, ":player_team", 1), #attackers in siege mod at start of round
               (assign, ":entry_no", multi_initial_spawn_point_team_2), #change later
             (try_end),
           (else_try),
             (call_script, "script_multiplayer_find_spawn_point", ":player_team", 0, ":player_is_horseman"),
             (assign, ":entry_no", reg0),             
           (try_end),
         
           (player_spawn_new_agent, ":player_no", ":entry_no"),
           (player_set_slot, ":player_no", slot_player_spawned_this_round, 1),
           (player_set_slot, ":player_no", slot_player_spawned_at_siege_round, 1),         
         (try_end),
         ]),

      (1, 0, 0, [], #do this in every new frame, but not at the same time
       [
         (multiplayer_is_server),
         (store_mission_timer_a, ":mission_timer"),
         (ge, ":mission_timer", 2),
         (assign, ":team_1_count", 0),
         (assign, ":team_2_count", 0),
         (try_for_agents, ":cur_agent"),
           (agent_is_non_player, ":cur_agent"),
           (agent_is_human, ":cur_agent"),
           (assign, ":will_be_counted", 0),
           (try_begin),
             (agent_is_alive, ":cur_agent"),
             (assign, ":will_be_counted", 1), #alive so will be counted
           (else_try),
             (agent_get_time_elapsed_since_removed, ":elapsed_time", ":cur_agent"),
             (le, ":elapsed_time", "$g_multiplayer_respawn_period"),
             (assign, ":will_be_counted", 1), 
           (try_end),
           (eq, ":will_be_counted", 1),
           (agent_get_team, ":cur_team", ":cur_agent"),
           (try_begin),
             (eq, ":cur_team", 0),
             (val_add, ":team_1_count", 1),
           (else_try),
             (eq, ":cur_team", 1),
             (val_add, ":team_2_count", 1),
           (try_end),
         (try_end),
         (store_sub, "$g_multiplayer_num_bots_required_team_1", "$g_multiplayer_num_bots_team_1", ":team_1_count"),
         (store_sub, "$g_multiplayer_num_bots_required_team_2", "$g_multiplayer_num_bots_team_2", ":team_2_count"),
         (val_max, "$g_multiplayer_num_bots_required_team_1", 0),
         (val_max, "$g_multiplayer_num_bots_required_team_2", 0),
         ]),

      multiplayer_server_spawn_bots, 
      multiplayer_server_manage_bots, 

      multiplayer_server_check_end_map,
        
      (ti_tab_pressed, 0, 0, [],
       [
         (try_begin),
           (eq, "$g_multiplayer_mission_end_screen", 0),
           (assign, "$g_multiplayer_stats_chart_opened_manually", 1),
           (start_presentation, "prsnt_multiplayer_stats_chart"),
         (try_end),
         ]),

      multiplayer_once_at_the_first_frame,

      (ti_battle_window_opened, 0, 0, [], [
        (start_presentation, "prsnt_multiplayer_round_time_counter"),
        (start_presentation, "prsnt_multiplayer_team_score_display"),
        ]),

      (ti_escape_pressed, 0, 0, [],
       [
         (neg|is_presentation_active, "prsnt_multiplayer_escape_menu"),
         (neg|is_presentation_active, "prsnt_multiplayer_stats_chart"),
         (eq, "$g_waiting_for_confirmation_to_terminate", 0),
         (start_presentation, "prsnt_multiplayer_escape_menu"),
         ]),
      ],
  ),

    (
    "multiplayer_bt",mtf_battle_mode,-1, #battle mode
    "You lead your men to battle.",
    [
      (0,mtef_visitor_source|mtef_team_0|mtef_no_auto_reset,0,aif_start_alarmed,1,[]),
      (1,mtef_visitor_source|mtef_team_0|mtef_no_auto_reset,0,aif_start_alarmed,1,[]),
      (2,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (3,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (4,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (5,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (6,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (7,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),

      (8,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (9,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (10,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (11,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (12,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (13,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (14,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (15,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),

      (16,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (17,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (18,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (19,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (20,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (21,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (22,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (23,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),

      (24,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (25,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (26,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (27,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (28,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (29,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (30,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (31,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),

      (32,mtef_visitor_source|mtef_team_0|mtef_no_auto_reset,0,aif_start_alarmed,1,[]),
      (33,mtef_visitor_source|mtef_team_0|mtef_no_auto_reset,0,aif_start_alarmed,1,[]),
      (34,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (35,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (36,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (37,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (38,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (39,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),

      (40,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (41,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (42,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (43,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (44,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (45,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (46,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (47,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),

      (48,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (49,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (50,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (51,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (52,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (53,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (54,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (55,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),

      (56,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (57,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (58,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (59,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (60,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (61,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (62,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (63,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
     ],
    [
      common_battle_init_banner,

      multiplayer_server_check_polls,
      
      (ti_server_player_joined, 0, 0, [],
       [
         (store_trigger_param_1, ":player_no"),
         (call_script, "script_multiplayer_server_player_joined_common", ":player_no"),
         ]),

      (ti_before_mission_start, 0, 0, [],
       [
         (assign, "$g_multiplayer_game_type", multiplayer_game_type_battle),
         (call_script, "script_multiplayer_server_before_mission_start_common"),
         
         (assign, "$g_waiting_for_confirmation_to_terminate", 0),
         (assign, "$g_round_ended", 0),
         (assign, "$g_battle_death_mode_started", 0),
         (assign, "$g_reduced_waiting_seconds", 0),

         (try_begin),
           (multiplayer_is_server),
           (assign, "$server_mission_timer_while_player_joined", 0),
           (assign, "$g_round_start_time", 0),
         (try_end),
         (assign, "$my_team_at_start_of_round", -1),

         (call_script, "script_multiplayer_init_mission_variables"),
         (call_script, "script_multiplayer_remove_destroy_mod_targets"),
         (call_script, "script_multiplayer_remove_headquarters_flags"),
         ]),

      (ti_after_mission_start, 0, 0, [], 
       [
         (call_script, "script_determine_team_flags", 0),
         (call_script, "script_determine_team_flags", 1),
         (set_spawn_effector_scene_prop_kind, 0, -1), #during this mission, agents of "team 0" will try to spawn around scene props with kind equal to -1(no effector for this mod)
         (set_spawn_effector_scene_prop_kind, 1, -1), #during this mission, agents of "team 1" will try to spawn around scene props with kind equal to -1(no effector for this mod)

         (try_begin),
           (multiplayer_is_server),

           (assign, "$g_multiplayer_ready_for_spawning_agent", 1),
         
           (entry_point_get_position, pos0, multi_death_mode_point),
           (position_set_z_to_ground_level, pos0),
           (position_move_z, pos0, -2000),

           (position_move_x, pos0, 100), 
           (set_spawn_position, pos0),
           (spawn_scene_prop, "spr_headquarters_pole_code_only", 0),

           (position_move_x, pos0, -200), 
           (set_spawn_position, pos0),
           (spawn_scene_prop, "spr_headquarters_pole_code_only", 0),

           (scene_prop_get_instance, ":pole_1_id", "spr_headquarters_pole_code_only", 0),
           (prop_instance_get_position, pos0, ":pole_1_id"),
           (spawn_scene_prop, "$team_1_flag_scene_prop", 0),
           (position_move_z, pos0, multi_headquarters_flag_initial_height),
           (prop_instance_set_position, reg0, pos0),
         
           (scene_prop_get_instance, ":pole_2_id", "spr_headquarters_pole_code_only", 1),
           (prop_instance_get_position, pos0, ":pole_2_id"),
           (spawn_scene_prop, "$team_2_flag_scene_prop", 0),
           (position_move_z, pos0, multi_headquarters_flag_initial_height),
           (prop_instance_set_position, reg0, pos0),

           (assign, "$g_multiplayer_num_bots_required_team_1", "$g_multiplayer_num_bots_team_1"), 
           (assign, "$g_multiplayer_num_bots_required_team_2", "$g_multiplayer_num_bots_team_2"), 
         (try_end),

         (call_script, "script_initialize_all_scene_prop_slots"),
         
         (call_script, "script_multiplayer_initialize_belfry_wheel_rotations"),
         (call_script, "script_multiplayer_move_moveable_objects_initial_positions"),
         ]),

      (ti_on_agent_spawn, 0, 0, [],
       [
         (store_trigger_param_1, ":agent_no"),
         (call_script, "script_multiplayer_server_on_agent_spawn_common", ":agent_no"),
         
         (try_begin), #if my initial team still not initialized, find and assign its value.
           (lt, "$my_team_at_start_of_round", 0),
           (multiplayer_get_my_player, ":my_player_no"),
           (ge, ":my_player_no", 0),
           (player_get_agent_id, ":my_agent_id", ":my_player_no"),
           (eq, ":my_agent_id", ":agent_no"),
           (ge, ":my_agent_id", 0),
           (agent_get_team, "$my_team_at_start_of_round", ":my_agent_id"),		   
         (try_end),

         #Equipment cost fix
         (agent_set_slot, ":agent_no", slot_agent_bought_horse, -1),
         (try_begin),
		     (multiplayer_is_server),
             (neg|agent_is_human, ":agent_no"),  #Spawned agent is horse
             (agent_get_rider, ":rider_agent_id", ":agent_no"),
             (agent_is_active, ":rider_agent_id"),
             (neg|agent_is_non_player, ":rider_agent_id"),
             (agent_get_player_id, ":rider_player_id", ":rider_agent_id"), 
             (neg|player_item_slot_is_picked_up, ":rider_player_id", ek_horse),
             (agent_set_slot, ":rider_agent_id", slot_agent_bought_horse, ":agent_no"),

             #Debugging
             #(str_store_player_username, s0, ":rider_player_id"), #used in multiplayer mode only
             #(agent_get_item_id, ":my_mount_type", ":agent_no"), #(works only for horses, returns -1 otherwise)
             #(str_store_item_name, s1, ":my_mount_type"),
             #(multiplayer_send_string_to_player, ":rider_player_id", multiplayer_event_show_server_message, "@{s0} bought a {s1}"),
             ##
         (try_end),
         ###
         
         (call_script, "script_calculate_new_death_waiting_time_at_death_mod"),
 
         (try_begin),
           (neg|multiplayer_is_server),
           (try_begin),
             (eq, "$g_round_ended", 1),
             (assign, "$g_round_ended", 0),

             #initialize scene object slots at start of new round at clients.
             (call_script, "script_initialize_all_scene_prop_slots"),

             #these lines are done in only clients at start of each new round.
             (call_script, "script_multiplayer_initialize_belfry_wheel_rotations"),
             (call_script, "script_initialize_objects_clients"),
             #end of lines
             (try_begin),
               (eq, "$g_team_balance_next_round", 1),
               (assign, "$g_team_balance_next_round", 0),
             (try_end),
           (try_end),  
         (try_end),         
         ]),

      (ti_on_agent_killed_or_wounded, 0, 0, [],
       [
         (store_trigger_param_1, ":dead_agent_no"),
         (store_trigger_param_2, ":killer_agent_no"),

         (call_script, "script_multiplayer_server_on_agent_killed_or_wounded_common", ":dead_agent_no", ":killer_agent_no"),

         (try_begin), #if my initial team still not initialized, find and assign its value.
           (lt, "$my_team_at_start_of_round", 0),
           (multiplayer_get_my_player, ":my_player_no"),
           (ge, ":my_player_no", 0),
           (player_get_agent_id, ":my_agent_id", ":my_player_no"),
           (ge, ":my_agent_id", 0),
           (agent_get_team, "$my_team_at_start_of_round", ":my_agent_id"),
         (try_end),         
         
         (try_begin), #count players and if round ended understand this.
           (agent_is_human, ":dead_agent_no"),
           (assign, ":team1_living_players", 0),
           (assign, ":team2_living_players", 0),
           (try_for_agents, ":cur_agent"),
             (agent_is_human, ":cur_agent"),         
             (try_begin),
               (agent_is_alive, ":cur_agent"),  
               (agent_get_team, ":cur_agent_team", ":cur_agent"),
               (try_begin),
                 (eq, ":cur_agent_team", 0),
               (val_add, ":team1_living_players", 1),
               (else_try),
                 (eq, ":cur_agent_team", 1),
                 (val_add, ":team2_living_players", 1),
               (try_end),
             (try_end),
           (try_end),                    
           (try_begin),         
             (eq, "$g_round_ended", 0),
             (try_begin),
               (this_or_next|eq, ":team1_living_players", 0),
               (eq, ":team2_living_players", 0),                
               (assign, "$g_winner_team", -1),
               (assign, reg0, "$g_multiplayer_respawn_period"),
               (try_begin),
                 (eq, ":team1_living_players", 0),
                 (try_begin),
                   (neq, ":team2_living_players", 0),
                   (team_get_score, ":team_2_score", 1),
                   (val_add, ":team_2_score", 1),
                   (team_set_score, 1, ":team_2_score"),
                   (assign, "$g_winner_team", 1),
                 (try_end),

                 (call_script, "script_show_multiplayer_message", multiplayer_message_type_round_result_in_battle_mode, "$g_winner_team"), #1 is winner team
                 (call_script, "script_check_achievement_last_man_standing", "$g_winner_team"),
               (else_try),
                 (try_begin),
                   (neq, ":team1_living_players", 0),
                   (team_get_score, ":team_1_score", 0),
                   (val_add, ":team_1_score", 1),
                   (team_set_score, 0, ":team_1_score"),
                   (assign, "$g_winner_team", 0),
                 (try_end),

                 (call_script, "script_show_multiplayer_message", multiplayer_message_type_round_result_in_battle_mode, "$g_winner_team"), #0 is winner team  
                 (call_script, "script_check_achievement_last_man_standing", "$g_winner_team"),       
               (try_end),
               (store_mission_timer_a, "$g_round_finish_time"),
               (assign, "$g_round_ended", 1),
             (try_end),
           (try_end),
         (try_end),

         (try_begin),
           (multiplayer_is_server),
           (agent_is_human, ":dead_agent_no"),
           (neg|agent_is_non_player, ":dead_agent_no"),

           (ge, ":dead_agent_no", 0),
           (agent_get_player_id, ":dead_agent_player_id", ":dead_agent_no"),
           (ge, ":dead_agent_player_id", 0),

           (set_fixed_point_multiplier, 100),

           (agent_get_player_id, ":dead_agent_player_id", ":dead_agent_no"),
           (agent_get_position, pos0, ":dead_agent_no"),

           (position_get_x, ":x_coor", pos0),
           (position_get_y, ":y_coor", pos0),
           (position_get_z, ":z_coor", pos0),
         
           (player_set_slot, ":dead_agent_player_id", slot_player_death_pos_x, ":x_coor"),
           (player_set_slot, ":dead_agent_player_id", slot_player_death_pos_y, ":y_coor"),
           (player_set_slot, ":dead_agent_player_id", slot_player_death_pos_z, ":z_coor"),
         (try_end),    
         ]),

      (ti_on_multiplayer_mission_end, 0, 0, [],
       [
         (call_script, "script_multiplayer_event_mission_end"),
         (assign, "$g_multiplayer_stats_chart_opened_manually", 0),
         (start_presentation, "prsnt_multiplayer_stats_chart"),
         ]),
      
      (1, 0, 0, [(multiplayer_is_server), 
                 (eq, "$g_round_ended", 0),
                 (store_mission_timer_a, ":current_time"),
                 (store_sub, ":seconds_past_in_round", ":current_time", "$g_round_start_time"),
                 (ge, ":seconds_past_in_round", "$g_multiplayer_round_max_seconds"),

                 (assign, ":overtime_needed", 0), #checking for if overtime is needed. Overtime happens when lower heighted flag is going up
                 (try_begin),
                   (eq, "$g_battle_death_mode_started", 2), #if death mod is currently open
                    
                   (scene_prop_get_instance, ":pole_1_id", "spr_headquarters_pole_code_only", 0),
                   (scene_prop_get_instance, ":pole_2_id", "spr_headquarters_pole_code_only", 1),
                   (scene_prop_get_instance, ":flag_1_id", "$team_1_flag_scene_prop", 0),
                   (scene_prop_get_instance, ":flag_2_id", "$team_2_flag_scene_prop", 0),

                   (prop_instance_get_position, pos1, ":pole_1_id"),
                   (prop_instance_get_position, pos2, ":pole_2_id"),
                   (prop_instance_get_position, pos3, ":flag_1_id"),
                   (prop_instance_get_position, pos4, ":flag_2_id"),

                   (get_distance_between_positions, ":height_of_flag_1", pos1, pos3),
                   (get_distance_between_positions, ":height_of_flag_2", pos2, pos4),
                   (store_add, ":height_of_flag_1_plus", ":height_of_flag_1", min_allowed_flag_height_difference_to_make_score),
                   (store_add, ":height_of_flag_2_plus", ":height_of_flag_2", min_allowed_flag_height_difference_to_make_score),

                   (try_begin),
                     (le, ":height_of_flag_1", ":height_of_flag_2_plus"),
                     (prop_instance_is_animating, ":is_animating", ":flag_1_id"),
                     (eq, ":is_animating", 1),
                     (prop_instance_get_animation_target_position, pos5, ":flag_1_id"),
                     (position_get_z, ":flag_2_animation_target_z", pos5),
                     (position_get_z, ":flag_1_cur_z", pos3),
                     (ge, ":flag_2_animation_target_z", ":flag_1_cur_z"),
                     (assign, ":overtime_needed", 1),
                   (try_end),
                   
                   (try_begin),
                     (le, ":height_of_flag_2", ":height_of_flag_1_plus"),
                     (prop_instance_is_animating, ":is_animating", ":flag_2_id"),
                     (eq, ":is_animating", 1),
                     (prop_instance_get_animation_target_position, pos5, ":flag_2_id"),
                     (position_get_z, ":flag_2_animation_target_z", pos5),
                     (position_get_z, ":flag_2_cur_z", pos4),
                     (ge, ":flag_2_animation_target_z", ":flag_2_cur_z"),
                     (assign, ":overtime_needed", 1),
                   (try_end),
                 (try_end),
                 (eq, ":overtime_needed", 0),
                 ],
       [ #round time is up
         (store_mission_timer_a, "$g_round_finish_time"),                          
         (assign, "$g_round_ended", 1),
         (assign, "$g_winner_team", -1),
         
         (try_begin), #checking for winning by death mod
           (eq, "$g_battle_death_mode_started", 2), #if death mod is currently open

           (scene_prop_get_instance, ":pole_1_id", "spr_headquarters_pole_code_only", 0),
           (scene_prop_get_instance, ":pole_2_id", "spr_headquarters_pole_code_only", 1),
           (scene_prop_get_instance, ":flag_1_id", "$team_1_flag_scene_prop", 0),
           (scene_prop_get_instance, ":flag_2_id", "$team_2_flag_scene_prop", 0),

           (prop_instance_get_position, pos1, ":pole_1_id"),
           (prop_instance_get_position, pos2, ":pole_2_id"),
           (prop_instance_get_position, pos3, ":flag_1_id"),
           (prop_instance_get_position, pos4, ":flag_2_id"),

           (get_distance_between_positions, ":height_of_flag_1", pos1, pos3),
           (get_distance_between_positions, ":height_of_flag_2", pos2, pos4),

           (try_begin),
             (ge, ":height_of_flag_1", ":height_of_flag_2"), #if flag_1 is higher than flag_2
             (store_sub, ":difference_of_heights", ":height_of_flag_1", ":height_of_flag_2"), 
             (ge, ":difference_of_heights", min_allowed_flag_height_difference_to_make_score), #if difference between flag heights is greater than 
             (assign, "$g_winner_team", 0),                                                    #"min_allowed_flag_height_difference_to_make_score" const value
           (else_try), #if flag_2 is higher than flag_1
             (store_sub, ":difference_of_heights", ":height_of_flag_2", ":height_of_flag_1"),
             (ge, ":difference_of_heights", min_allowed_flag_height_difference_to_make_score), #if difference between flag heights is greater than 
             (assign, "$g_winner_team", 1),                                                    #"min_allowed_flag_height_difference_to_make_score" const value
           (try_end),
         (try_end),
    
         (multiplayer_get_my_player, ":my_player_no"), #send all players draw information of round.
         #for only server itself-----------------------------------------------------------------------------------------------
         (call_script, "script_draw_this_round", "$g_winner_team"),
         #for only server itself-----------------------------------------------------------------------------------------------
         (get_max_players, ":num_players"), 
         (try_for_range, ":player_no", 1, ":num_players"), #0 is server so starting from 1
           (player_is_active, ":player_no"),
           (neq, ":player_no", ":my_player_no"),
           (multiplayer_send_int_to_player, ":player_no", multiplayer_event_draw_this_round, "$g_winner_team"),
         (try_end),
        ]),          

      (10, 0, 0, [(multiplayer_is_server)],
       [
         #auto team balance control during the round         
         (assign, ":number_of_players_at_team_1", 0),
         (assign, ":number_of_players_at_team_2", 0),
         (get_max_players, ":num_players"),
         (try_for_range, ":cur_player", 0, ":num_players"),
           (player_is_active, ":cur_player"),
           (player_get_team_no, ":player_team", ":cur_player"),
           (try_begin),
             (eq, ":player_team", 0),
             (val_add, ":number_of_players_at_team_1", 1),
           (else_try),
             (eq, ":player_team", 1),
             (val_add, ":number_of_players_at_team_2", 1),
           (try_end),         
         (try_end),
         #end of counting active players per team.
         (store_sub, ":difference_of_number_of_players", ":number_of_players_at_team_1", ":number_of_players_at_team_2"),
         (assign, ":number_of_players_will_be_moved", 0),
         (try_begin),
           (try_begin),
             (store_mul, ":checked_value", "$g_multiplayer_auto_team_balance_limit", -1),
             (le, ":difference_of_number_of_players", ":checked_value"),
             (store_div, ":number_of_players_will_be_moved", ":difference_of_number_of_players", -2),
           (else_try),
             (ge, ":difference_of_number_of_players", "$g_multiplayer_auto_team_balance_limit"),
             (store_div, ":number_of_players_will_be_moved", ":difference_of_number_of_players", 2),
           (try_end),          
         (try_end),         
         #number of players will be moved calculated. (it is 0 if no need to make team balance)
         (try_begin),
           (gt, ":number_of_players_will_be_moved", 0),
           (try_begin),
             (eq, "$g_team_balance_next_round", 0),
         
             (assign, "$g_team_balance_next_round", 1),

             #for only server itself-----------------------------------------------------------------------------------------------
             (call_script, "script_show_multiplayer_message", multiplayer_message_type_auto_team_balance_next, 0), #0 is useless here
             #for only server itself-----------------------------------------------------------------------------------------------     
             (get_max_players, ":num_players"),                               
             (try_for_range, ":player_no", 1, ":num_players"), #0 is server so starting from 1
               (player_is_active, ":player_no"),
               (multiplayer_send_int_to_player, ":player_no", multiplayer_event_show_multiplayer_message, multiplayer_message_type_auto_team_balance_next),
             (try_end),
             
             (call_script, "script_warn_player_about_auto_team_balance"),
           (try_end),
         (try_end),           
         #team balance check part finished
         ]),

      #checking for starting "death mode part 1"
      (1, 0, 0, [(multiplayer_is_server),
                 (eq, "$g_round_ended", 0),
                 (eq, "$g_battle_death_mode_started", 0),
                 (store_mission_timer_a, ":seconds_past_till_round_started"),
                 (val_sub, ":seconds_past_till_round_started", "$g_round_start_time"),
                 (store_div, "$g_multiplayer_round_max_seconds_div_2", "$g_multiplayer_round_max_seconds", 2),
                 (ge, ":seconds_past_till_round_started", "$g_multiplayer_round_max_seconds_div_2")],
       [
         (call_script, "script_calculate_new_death_waiting_time_at_death_mod"),
         (assign, "$g_battle_death_mode_started", 1),
         ]),

      #checking during "death mode part 1" for entering "death mode part 2"
      (1, 0, 0, [(multiplayer_is_server),
                 (eq, "$g_round_ended", 0),
                 (eq, "$g_battle_death_mode_started", 1),
                 (store_mission_timer_a, ":seconds_past_till_death_mode_part_1_started"),
                 (val_sub, ":seconds_past_till_death_mode_part_1_started", "$g_death_mode_part_1_start_time"),
                 (store_add, ":g_battle_waiting_seconds_plus_reduced_waiting_seconds", "$g_battle_waiting_seconds", "$g_reduced_waiting_seconds"),
                 (ge, ":seconds_past_till_death_mode_part_1_started", ":g_battle_waiting_seconds_plus_reduced_waiting_seconds"), #death mod start if anybody did not dies in "$g_battle_waiting_seconds" seconds
                 (store_mission_timer_a, ":current_time"),
                 (store_sub, ":seconds_past_in_round", ":current_time", "$g_round_start_time"),
                 (store_sub, ":g_multiplayer_round_max_seconds_sub_15", "$g_multiplayer_round_max_seconds", 15),
                 (lt, ":seconds_past_in_round", ":g_multiplayer_round_max_seconds_sub_15")], #death mod cannot start at last 15 seconds
       [
         (assign, "$g_battle_death_mode_started", 2),
         #for only server itself-----------------------------------------------------------------------------------------------
         (call_script, "script_start_death_mode"),
         #for only server itself-----------------------------------------------------------------------------------------------
         (get_max_players, ":num_players"),
         (try_for_range, ":player_no", 1, ":num_players"), #0 is server so starting from 1
           (player_is_active, ":player_no"),
           (multiplayer_send_int_to_player, ":player_no", multiplayer_event_start_death_mode),
         (try_end),

         (scene_prop_get_instance, ":pole_1_id", "spr_headquarters_pole_code_only", 0),
         (scene_prop_get_instance, ":pole_2_id", "spr_headquarters_pole_code_only", 1),
         (scene_prop_get_instance, ":flag_1_id", "$team_1_flag_scene_prop", 0),
         (scene_prop_get_instance, ":flag_2_id", "$team_2_flag_scene_prop", 0),

         #death mode started make 4 item related to death mode visible.
         (store_random_in_range, "$g_random_entry_point", 0, 3),
         (val_add, "$g_random_entry_point", multi_death_mode_point),

         (entry_point_get_position, pos0, "$g_random_entry_point"),
         (position_set_z_to_ground_level, pos0),
         
         (position_move_x, pos0, 100), 
         (prop_instance_set_position, ":pole_1_id", pos0),

         (position_move_x, pos0, -200), 
         (prop_instance_set_position, ":pole_2_id", pos0),

         (prop_instance_get_position, pos0, ":pole_1_id"),
         (position_move_z, pos0, multi_headquarters_flag_initial_height),
         (prop_instance_set_position, ":flag_1_id", pos0),
         
         (prop_instance_get_position, pos0, ":pole_2_id"),
         (position_move_z, pos0, multi_headquarters_flag_initial_height),
         (prop_instance_set_position, ":flag_2_id", pos0),

         (start_presentation, "prsnt_multiplayer_flag_projection_display_bt"),
         ]),

      (3, 0, 0, [(multiplayer_is_server),  #this trigger is to reduce "$g_battle_waiting_seconds" at between last 66th and last 24th seconds 1 per 3 seconds, total 14 seconds.
                 (eq, "$g_round_ended", 0),                 
                 (eq, "$g_battle_death_mode_started", 1),
                 
                 (store_mission_timer_a, ":seconds_past_till_death_mode_part_1_started"),
                 (val_sub, ":seconds_past_till_death_mode_part_1_started", "$g_death_mode_part_1_start_time"),
                 (store_add, ":g_battle_waiting_seconds_plus_reduced_waiting_seconds", "$g_battle_waiting_seconds", "$g_reduced_waiting_seconds"),
                 (val_sub, ":g_battle_waiting_seconds_plus_reduced_waiting_seconds", 20), #in last 20 seconds to master of field below code effects
                 (ge, ":seconds_past_till_death_mode_part_1_started", ":g_battle_waiting_seconds_plus_reduced_waiting_seconds"),], #death mod start if anybody did not dies in "$g_battle_waiting_seconds" seconds            
        [
                 (assign, ":there_are_fighting_agents", 0),

                 (try_for_agents, ":agent_no_1"),
                   (eq, ":there_are_fighting_agents", 0),
                   (agent_is_human, ":agent_no_1"),
                   (try_for_agents, ":agent_no_2"),
                     (agent_is_human, ":agent_no_2"),
                     (neq, ":agent_no_1", ":agent_no_2"),

                     (agent_get_team, ":agent_no_1_team", ":agent_no_1"),
                     (agent_get_team, ":agent_no_2_team", ":agent_no_2"),

                     (neq, ":agent_no_1_team", ":agent_no_2_team"),
                 
                     (agent_get_position, pos1, ":agent_no_1"),
                     (agent_get_position, pos2, ":agent_no_2"),

                     (get_sq_distance_between_positions_in_meters, ":sq_dist_in_meters", pos1, pos2),

                     (le, ":sq_dist_in_meters", multi_max_sq_dist_between_agents_to_longer_mof_time),

                     (assign, ":there_are_fighting_agents", 1),
                   (try_end),   
                 (try_end),

                 (try_begin),
                   (eq, ":there_are_fighting_agents", 1),
                   (val_add, "$g_reduced_waiting_seconds", 3),
                   #(display_message, "@{!}DEBUG : there are fighting agents"),
                 (try_end),
        ]),

      (3, 0, 0, [(multiplayer_is_server),  #this trigger is to reduce "$g_battle_waiting_seconds" at between last 66th and last 24th seconds 1 per 3 seconds, total 14 seconds.
                 (eq, "$g_round_ended", 0),                 
                 (eq, "$g_battle_death_mode_started", 1),
                 
                 (store_mission_timer_a, ":current_time"),
                 (store_sub, ":seconds_past_in_round", ":current_time", "$g_round_start_time"),
                 (store_sub, ":g_multiplayer_round_max_seconds_sub_60", "$g_multiplayer_round_max_seconds", 66),
                 (ge, ":seconds_past_in_round", ":g_multiplayer_round_max_seconds_sub_60"),

                 (store_mission_timer_a, ":current_time"),
                 (store_sub, ":seconds_past_in_round", ":current_time", "$g_round_start_time"),
                 (store_sub, ":g_multiplayer_round_max_seconds_sub_20", "$g_multiplayer_round_max_seconds", 24),
                 (le, ":seconds_past_in_round", ":g_multiplayer_round_max_seconds_sub_20"),
                 ],
       [
         (val_add, "$g_reduced_waiting_seconds", 1),
         ]),

      (0, 0, 0, [(multiplayer_is_server),  
                 (eq, "$g_round_ended", 0),                 
                 (eq, "$g_battle_death_mode_started", 2)],
       [
         (set_fixed_point_multiplier, 100),
         (scene_prop_get_instance, ":pole_1_id", "spr_headquarters_pole_code_only", 0),
         (scene_prop_get_instance, ":pole_2_id", "spr_headquarters_pole_code_only", 1),
         (scene_prop_get_instance, ":flag_1_id", "$team_1_flag_scene_prop", 0),
         (scene_prop_get_instance, ":flag_2_id", "$team_2_flag_scene_prop", 0),

         (prop_instance_get_position, pos1, ":pole_1_id"),
         (prop_instance_get_position, pos2, ":pole_2_id"),
         (prop_instance_get_position, pos3, ":flag_1_id"),
         (prop_instance_get_position, pos4, ":flag_2_id"),

         (copy_position, pos7, pos1),
         (position_move_z, pos7, multi_headquarters_flag_initial_height),
         (copy_position, pos8, pos2),
         (position_move_z, pos8, multi_headquarters_flag_initial_height),

         (get_distance_between_positions, ":dist_1", pos1, pos3),
         (get_distance_between_positions, ":dist_2", pos2, pos4),

         (assign, ":there_are_agents_from_only_team_1_around_their_flag", 0),
         (assign, ":there_are_agents_from_only_team_2_around_their_flag", 0),
         (get_max_players, ":num_players"),
         (try_for_range, ":player_no", 0, ":num_players"),
           (player_is_active, ":player_no"),
           (player_get_agent_id, ":agent_id", ":player_no"),
           (ge, ":agent_id", 0),
           (agent_is_human, ":agent_id"),
           (agent_is_alive, ":agent_id"),
           (agent_get_team, ":agent_team", ":agent_id"),
           (agent_get_position, pos0, ":agent_id"),

           (agent_get_horse, ":agent_horse", ":agent_id"),
           (eq, ":agent_horse", -1), #horseman cannot move flag
         
           (try_begin),
             (eq, ":agent_team", 0),
             (try_begin),
               (get_sq_distance_between_positions, ":squared_dist", pos0, pos1),
               (lt, ":squared_dist", multi_headquarters_max_distance_sq_to_raise_flags),
               (try_begin), #we found a team_1 agent in the flag_1 area, so flag_1 situation can be 1 or -2
                 (this_or_next|eq, ":there_are_agents_from_only_team_1_around_their_flag", 0),
                 (eq, ":there_are_agents_from_only_team_1_around_their_flag", 1),
                 (assign, ":there_are_agents_from_only_team_1_around_their_flag", 1), #there are agents from only our team
               (else_try),                 
                 (assign, ":there_are_agents_from_only_team_1_around_their_flag", -2), #there are agents from both teams
               (try_end),
             (try_end),
             (try_begin),
               (get_sq_distance_between_positions, ":squared_dist", pos0, pos2),
               (lt, ":squared_dist", multi_headquarters_max_distance_sq_to_raise_flags),
               (try_begin), #we found a team_1 agent in the flag_2 area, so flag_2 situation can be -1 or -2
                 (eq, ":there_are_agents_from_only_team_2_around_their_flag", 0),
                 (assign, ":there_are_agents_from_only_team_2_around_their_flag", -1), #there are agents from only rival team
               (else_try),
                 (eq, ":there_are_agents_from_only_team_2_around_their_flag", 1),
                 (assign, ":there_are_agents_from_only_team_2_around_their_flag", -2), #there are agents from both teams
               (try_end),
             (try_end),
           (else_try),
             (eq, ":agent_team", 1),
             (try_begin),
               (get_sq_distance_between_positions, ":squared_dist", pos0, pos2),
               (lt, ":squared_dist", multi_headquarters_max_distance_sq_to_raise_flags),
               (try_begin), #we found a team_2 agent in the flag 2 area, so flag_2 situation can be 1 or -2
                 (this_or_next|eq, ":there_are_agents_from_only_team_2_around_their_flag", 0),
                 (eq, ":there_are_agents_from_only_team_2_around_their_flag", 1),
                 (assign, ":there_are_agents_from_only_team_2_around_their_flag", 1), #there are agents from only our team
               (else_try),                 
                 (assign, ":there_are_agents_from_only_team_2_around_their_flag", -2), #there are agents from both teams
               (try_end),
             (try_end),
             (try_begin),
               (get_sq_distance_between_positions, ":squared_dist", pos0, pos1),
               (lt, ":squared_dist", multi_headquarters_max_distance_sq_to_raise_flags),
               (try_begin), #we found a team_2 agent in the flag_1 area, so flag_1 situation can be -1 or -2
                 (eq, ":there_are_agents_from_only_team_1_around_their_flag", 0),
                 (assign, ":there_are_agents_from_only_team_1_around_their_flag", -1), #there are agents from only rival team
               (else_try),
                 (eq, ":there_are_agents_from_only_team_1_around_their_flag", 1),
                 (assign, ":there_are_agents_from_only_team_1_around_their_flag", -2), #there are agents from both teams
               (try_end),
             (try_end),
           (try_end),
         (try_end),

         #controlling battle win by death mode conditions
         (try_begin),
           (ge, ":dist_1", multi_headquarters_flag_height_to_win),           
           (assign, "$g_winner_team", 0),

           (get_max_players, ":num_players"), 
           #for only server itself-----------------------------------------------------------------------------------------------
           (call_script, "script_draw_this_round", "$g_winner_team"),
           #for only server itself-----------------------------------------------------------------------------------------------
           (try_for_range, ":player_no", 1, ":num_players"), #0 is server so starting from 1
             (player_is_active, ":player_no"),
             (multiplayer_send_int_to_player, ":player_no", multiplayer_event_draw_this_round, "$g_winner_team"),
           (try_end),

           (team_get_score, ":team_1_score", 0),
           #for only server itself-----------------------------------------------------------------------------------------------
           (call_script, "script_team_set_score", 0, ":team_1_score"),
           #for only server itself-----------------------------------------------------------------------------------------------
           (try_for_range, ":player_no", 1, ":num_players"), #0 is server so starting from 1
             (player_is_active, ":player_no"),
             (multiplayer_send_2_int_to_player, ":player_no", multiplayer_event_set_team_score, 0, ":team_1_score"),             
           (try_end),

           (store_mission_timer_a, "$g_round_finish_time"),
           (assign, "$g_round_ended", 1),
         (else_try),
           (ge, ":dist_2", multi_headquarters_flag_height_to_win),
           (assign, "$g_winner_team", 1),

           (get_max_players, ":num_players"), 
           #for only server itself-----------------------------------------------------------------------------------------------
           (call_script, "script_draw_this_round", "$g_winner_team"),
           #for only server itself-----------------------------------------------------------------------------------------------
           (try_for_range, ":player_no", 1, ":num_players"), #0 is server so starting from 1
             (player_is_active, ":player_no"),
             (multiplayer_send_int_to_player, ":player_no", multiplayer_event_draw_this_round, "$g_winner_team"),
           (try_end),

           (team_get_score, ":team_2_score", 1),
           #for only server itself-----------------------------------------------------------------------------------------------
           (call_script, "script_team_set_score", 1, ":team_2_score"),
           #for only server itself-----------------------------------------------------------------------------------------------
           (try_for_range, ":player_no", 1, ":num_players"), #0 is server so starting from 1
             (player_is_active, ":player_no"),
             (multiplayer_send_2_int_to_player, ":player_no", multiplayer_event_set_team_score, 1, ":team_2_score"),             
           (try_end),

           (call_script, "script_show_multiplayer_message", multiplayer_message_type_round_result_in_battle_mode, 0), #0 is winner team		
           (call_script, "script_check_achievement_last_man_standing", "$g_winner_team"),     

           (store_mission_timer_a, "$g_round_finish_time"),
           (assign, "$g_round_ended", 1),
         (try_end),

         (try_begin),
           (eq, "$g_round_ended", 0),

           (position_get_z, ":flag_1_cur_z", pos3),       
           (prop_instance_is_animating, ":is_animating", ":flag_1_id"),         
           (try_begin), #if flag_1 is going down or up and there are agents from both teams
             (eq, ":there_are_agents_from_only_team_1_around_their_flag", -2), #if there are agents from both teams
             (eq, ":is_animating", 1),
             (prop_instance_stop_animating, ":flag_1_id"), #stop flag_1
           (else_try), #if flag_1 is going down
             (this_or_next|eq, ":there_are_agents_from_only_team_1_around_their_flag", 0), #if there is no one
             (eq, ":there_are_agents_from_only_team_1_around_their_flag", -1), #if there are agents from only team_2 (enemy of team_1)
             (prop_instance_get_animation_target_position, pos9, ":flag_1_id"),
             (position_get_z, ":flag_1_animation_target_z", pos9),
             (this_or_next|eq, ":is_animating", 0), #if flag_1 is stopping
             (gt, ":flag_1_animation_target_z", ":flag_1_cur_z"), #if flag_1 is going up         
             (get_distance_between_positions, ":time_1", pos3, pos7),
             (gt, ":time_1", 0),
             (val_mul, ":time_1", 16),
             (prop_instance_animate_to_position, ":flag_1_id", pos7, ":time_1"), #move flag_1 down
           (else_try), #if flag_1 is going down or stopping
             (eq, ":there_are_agents_from_only_team_1_around_their_flag", 1), #if there is agents from only team_1 (current team)
             (prop_instance_get_animation_target_position, pos9, ":flag_1_id"),
             (position_get_z, ":flag_1_animation_target_z", pos9),
             (this_or_next|eq, ":is_animating", 0), #if flag_1 is stopping
             (lt, ":flag_1_animation_target_z", ":flag_1_cur_z"), #if flag_1 is going down
             (copy_position, pos5, pos1),
             (position_move_z, pos5, multi_headquarters_flag_height_to_win),
             (get_distance_between_positions, ":time_1", pos3, pos5),
             (gt, ":time_1", 0),
             (val_mul, ":time_1", 8),
             (prop_instance_animate_to_position, ":flag_1_id", pos5, ":time_1"), #move flag_1 up
           (try_end),

           (position_get_z, ":flag_2_cur_z", pos4),       
           (prop_instance_is_animating, ":is_animating", ":flag_2_id"),         
           (try_begin), #if flag is going down or up and there are agents from both teams
             (eq, ":there_are_agents_from_only_team_2_around_their_flag", -2), #if there are agents from both teams
             (eq, ":is_animating", 1),
             (prop_instance_stop_animating, ":flag_2_id"), #stop flag_2
           (else_try), #if flag_2 is going down
             (this_or_next|eq, ":there_are_agents_from_only_team_2_around_their_flag", 0), #if there is no one
             (eq, ":there_are_agents_from_only_team_2_around_their_flag", -1), #if there are agents from only team_1 (enemy of team_1)
             (prop_instance_get_animation_target_position, pos9, ":flag_2_id"),
             (position_get_z, ":flag_2_animation_target_z", pos9),
             (this_or_next|eq, ":is_animating", 0), #if flag_2 is stopping
             (gt, ":flag_2_animation_target_z", ":flag_2_cur_z"), #if flag_2 is going up         
             (get_distance_between_positions, ":time_2", pos4, pos8),
             (gt, ":time_2", 0),
             (val_mul, ":time_2", 16),
             (prop_instance_animate_to_position, ":flag_2_id", pos8, ":time_2"), #move flag_2 down
           (else_try), #if flag_2 is going down or stopping
             (eq, ":there_are_agents_from_only_team_2_around_their_flag", 1), #if there is agents from only team_2 (current team)
             (prop_instance_get_animation_target_position, pos9, ":flag_2_id"),
             (position_get_z, ":flag_2_animation_target_z", pos9),
             (this_or_next|eq, ":is_animating", 0), #if flag_2 is stopping
             (lt, ":flag_2_animation_target_z", ":flag_2_cur_z"), #if flag_2 is going down
             (copy_position, pos6, pos2),
             (position_move_z, pos6, multi_headquarters_flag_height_to_win),
             (get_distance_between_positions, ":time_2", pos4, pos6),
             (gt, ":time_2", 0),
             (val_mul, ":time_2", 8),
             (prop_instance_animate_to_position, ":flag_2_id", pos6, ":time_2"), #move flag_2 up
           (try_end),
         (try_end),
         ]),
                
      (1, 0, 3, [(multiplayer_is_server),
                 (eq, "$g_round_ended", 1),
                 (store_mission_timer_a, ":seconds_past_till_round_ended"),
                 (val_sub, ":seconds_past_till_round_ended", "$g_round_finish_time"),
                 (ge, ":seconds_past_till_round_ended", "$g_multiplayer_respawn_period")],
       [
         #auto team balance control at the end of round         
         (assign, ":number_of_players_at_team_1", 0),
         (assign, ":number_of_players_at_team_2", 0),
         (get_max_players, ":num_players"),
         (try_for_range, ":cur_player", 0, ":num_players"),
           (player_is_active, ":cur_player"),
           (player_get_team_no, ":player_team", ":cur_player"),
           (try_begin),
             (eq, ":player_team", 0),
             (val_add, ":number_of_players_at_team_1", 1),
           (else_try),
             (eq, ":player_team", 1),
             (val_add, ":number_of_players_at_team_2", 1),
           (try_end),         
         (try_end),
         #end of counting active players per team.
         (store_sub, ":difference_of_number_of_players", ":number_of_players_at_team_1", ":number_of_players_at_team_2"),
         (assign, ":number_of_players_will_be_moved", 0),
         (try_begin),
           (try_begin),
             (store_mul, ":checked_value", "$g_multiplayer_auto_team_balance_limit", -1),
             (le, ":difference_of_number_of_players", ":checked_value"),
             (store_div, ":number_of_players_will_be_moved", ":difference_of_number_of_players", -2),
             (assign, ":team_with_more_players", 1),
             (assign, ":team_with_less_players", 0),
           (else_try),
             (ge, ":difference_of_number_of_players", "$g_multiplayer_auto_team_balance_limit"),
             (store_div, ":number_of_players_will_be_moved", ":difference_of_number_of_players", 2),
             (assign, ":team_with_more_players", 0),
             (assign, ":team_with_less_players", 1),
           (try_end),
         (try_end),         
         #number of players will be moved calculated. (it is 0 if no need to make team balance)
         (try_begin),
           (gt, ":number_of_players_will_be_moved", 0),
           (try_begin),
             #(eq, "$g_team_balance_next_round", 1), #control if at pre round players are warned about team change.

             (try_for_range, ":unused", 0, ":number_of_players_will_be_moved"), 
               (assign, ":max_player_join_time", 0),
               (assign, ":latest_joined_player_no", -1),
               (get_max_players, ":num_players"),                               
               (try_for_range, ":player_no", 0, ":num_players"),
                 (player_is_active, ":player_no"),
                 (player_get_team_no, ":player_team", ":player_no"),
                 (eq, ":player_team", ":team_with_more_players"),
                 (player_get_slot, ":player_join_time", ":player_no", slot_player_join_time),
                 (try_begin),
                   (gt, ":player_join_time", ":max_player_join_time"),
                   (assign, ":max_player_join_time", ":player_join_time"),
                   (assign, ":latest_joined_player_no", ":player_no"),
                 (try_end),
               (try_end),
               (try_begin),
                 (ge, ":latest_joined_player_no", 0),
                 (try_begin),
                   #if player is living add +1 to his kill count because he will get -1 because of team change while living.
                   (player_get_agent_id, ":latest_joined_agent_id", ":latest_joined_player_no"), 
                   (ge, ":latest_joined_agent_id", 0),
                   (agent_is_alive, ":latest_joined_agent_id"),

                   (player_get_kill_count, ":player_kill_count", ":latest_joined_player_no"), #adding 1 to his kill count, because he will lose 1 undeserved kill count for dying during team change
                   (val_add, ":player_kill_count", 1),
                   (player_set_kill_count, ":latest_joined_player_no", ":player_kill_count"),

                   (player_get_death_count, ":player_death_count", ":latest_joined_player_no"), #subtracting 1 to his death count, because he will gain 1 undeserved death count for dying during team change
                   (val_sub, ":player_death_count", 1),
                   (player_set_death_count, ":latest_joined_player_no", ":player_death_count"),

                   (player_get_score, ":player_score", ":latest_joined_player_no"), #adding 1 to his score count, because he will lose 1 undeserved score for dying during team change
                   (val_add, ":player_score", 1),
                   (player_set_score, ":latest_joined_player_no", ":player_score"),

                   (try_for_range, ":player_no", 1, ":num_players"), #0 is server so starting from 1
                     (player_is_active, ":player_no"),
                     (multiplayer_send_4_int_to_player, ":player_no", multiplayer_event_set_player_score_kill_death, ":latest_joined_player_no", ":player_score", ":player_kill_count", ":player_death_count"),
                   (try_end),         

                   (player_get_value_of_original_items, ":old_items_value", ":latest_joined_player_no"),
                   (player_get_gold, ":player_gold", ":latest_joined_player_no"),
                   (val_add, ":player_gold", ":old_items_value"),
                   (player_set_gold, ":latest_joined_player_no", ":player_gold", multi_max_gold_that_can_be_stored),
                 (end_try),

                 (player_set_troop_id, ":latest_joined_player_no", -1),
                 (player_set_team_no, ":latest_joined_player_no", ":team_with_less_players"),
                 (multiplayer_send_message_to_player, ":latest_joined_player_no", multiplayer_event_force_start_team_selection),
               (try_end),
             (try_end),
             #tutorial message (after team balance)
             
             #(tutorial_message_set_position, 500, 500),
             #(tutorial_message_set_size, 30, 30),
             #(tutorial_message_set_center_justify, 1),
             #(tutorial_message, "str_auto_team_balance_done", 0xFFFFFFFF, 5),

             #for only server itself
             (call_script, "script_show_multiplayer_message", multiplayer_message_type_auto_team_balance_done, 0), 

             #no need to send also server here
             (multiplayer_get_my_player, ":my_player_no"),
             (get_max_players, ":num_players"),                               
             (try_for_range, ":player_no", 0, ":num_players"),
               (player_is_active, ":player_no"),
               (neq, ":my_player_no", ":player_no"),
               (multiplayer_send_int_to_player, ":player_no", multiplayer_event_show_multiplayer_message, multiplayer_message_type_auto_team_balance_done),
             (try_end),
             (assign, "$g_team_balance_next_round", 0),
           (try_end),
         (try_end),           
         #team balance check part finished
         (assign, "$g_team_balance_next_round", 0),

         (get_max_players, ":num_players"),
         (try_for_range, ":player_no", 0, ":num_players"),
               (neq, ":player_no", -1), ##
               (player_is_active, ":player_no"),
               (player_get_agent_id, ":player_agent", ":player_no"),
               (ge, ":player_agent", 0),
               (agent_is_alive, ":player_agent"),
               (player_save_picked_up_items_for_next_spawn, ":player_no"),
               #(player_get_value_of_original_items, ":old_items_value", ":player_no"),
               #(player_set_slot, ":player_no", slot_player_last_rounds_used_item_earnings, ":old_items_value"),
               #Equipment cost fix
               (assign, reg0, 0),
               (player_get_troop_id, ":player_no_troop_id", ":player_no"),
               (call_script, "script_player_get_value_of_original_items", ":player_no", ":player_agent", ":player_no_troop_id"),
               (assign, ":old_items_value", reg0),
               (player_set_slot, ":player_no", slot_player_last_rounds_used_item_earnings, ":old_items_value"),
               #Debugging 
               #(multiplayer_send_string_to_player, ":player_no", multiplayer_event_show_server_message, "@{reg0}g for your old items value added to your total gold"),
               ###
         (try_end),

         #money management
         (assign, ":per_round_gold_addition", multi_battle_round_team_money_add),
         (val_mul, ":per_round_gold_addition", "$g_multiplayer_round_earnings_multiplier"),
         (val_div, ":per_round_gold_addition", 100),
         (get_max_players, ":num_players"),
         (try_for_range, ":player_no", 0, ":num_players"),
           (player_is_active, ":player_no"),		   
		   (player_slot_eq, ":player_no", slot_player_spawned_this_round, 1),

           (player_get_gold, ":player_gold", ":player_no"),
           (player_get_team_no, ":player_team", ":player_no"),

           (try_begin),
             (this_or_next|eq, ":player_team", 0),
             (eq, ":player_team", 1),
             (val_add, ":player_gold", ":per_round_gold_addition"), 
           (try_end),

           #(below lines added new at 25.11.09 after Armagan decided new money system)
           (try_begin),
             (player_get_slot, ":old_items_value", ":player_no", slot_player_last_rounds_used_item_earnings),
             (store_add, ":player_total_potential_gold", ":player_gold", ":old_items_value"),
             (store_mul, ":minimum_gold", "$g_multiplayer_initial_gold_multiplier", 10),
             (lt, ":player_total_potential_gold", ":minimum_gold"),
             (store_sub, ":additional_gold", ":minimum_gold", ":player_total_potential_gold"),
             (val_add, ":player_gold", ":additional_gold"),
           (try_end),
           #new money system addition end
           #(get_max_players, ":num_players"),
	       #(try_for_range, ":player_no", 0, ":num_players"),
           #  (neq, ":player_no", -1), ##
           #  (player_is_active, ":player_no"),
           #  (player_set_slot, ":player_no", slot_player_spawned_this_round, 0),
           #  (player_get_agent_id, ":player_agent", ":player_no"),
           #  (ge, ":player_agent", 0),
           #  (agent_is_alive, ":player_agent"),
           #  (player_save_picked_up_items_for_next_spawn, ":player_no"),
           #  #(player_get_value_of_original_items, ":old_items_value", ":player_no"),
           #  #(player_set_slot, ":player_no", slot_player_last_rounds_used_item_earnings, ":old_items_value"),
           #  #Equipment cost fix
           #  (player_get_agent_id, ":agent_no", ":player_no"),
           #  (neq, ":agent_no", -1),
           #  #(display_message, "@Calculating value of original items!"),
           #  (player_get_troop_id, ":player_no_troop_id", ":player_no"),
           #  (call_script, "script_player_get_value_of_original_items", ":player_no", ":agent_no", ":player_no_troop_id"),
           #  (assign, ":old_items_value", reg0),
           #  (player_set_slot, ":player_no", slot_player_last_rounds_used_item_earnings, ":old_items_value"),
           #  ###
           #(try_end),
           (player_set_gold, ":player_no", ":player_gold", multi_max_gold_that_can_be_stored),
         (try_end),

         (try_for_range, ":player_no", 0, ":num_players"),
           (player_is_active, ":player_no"),
           (player_set_slot, ":player_no", slot_player_spawned_this_round, 0),
         (try_end),

         #initialize my team at start of round (it will be assigned again at next round's first death)
         (assign, "$my_team_at_start_of_round", -1),

         #clear scene and end round
         (multiplayer_clear_scene),

         (call_script, "script_multiplayer_initialize_belfry_wheel_rotations"),

         (try_begin),
           (eq, "$g_battle_death_mode_started", 2),
           (call_script, "script_move_death_mode_flags_down"),
         (try_end),

         (assign, "$g_battle_death_mode_started", 0),
         (assign, "$g_reduced_waiting_seconds", 0),
         
         #initialize moveable object positions
         (call_script, "script_multiplayer_close_gate_if_it_is_open"),
         (call_script, "script_multiplayer_move_moveable_objects_initial_positions"),
                  
         (assign, "$g_round_ended", 0), 

         (assign, "$g_multiplayer_num_bots_required_team_1", "$g_multiplayer_num_bots_team_1"), 
         (assign, "$g_multiplayer_num_bots_required_team_2", "$g_multiplayer_num_bots_team_2"), 

         (store_mission_timer_a, "$g_round_start_time"),
         (call_script, "script_initialize_all_scene_prop_slots"),

         #initialize round start times for clients
         (get_max_players, ":num_players"),
         (try_for_range, ":player_no", 0, ":num_players"),
           (player_is_active, ":player_no"),
           (multiplayer_send_int_to_player, ":player_no", multiplayer_event_set_round_start_time, -9999), #this will also initialize moveable object slots.
         (try_end),         
       ]),

      (0, 0, 0, [], #if there is nobody in any teams do not reduce round time.
       [
         #(multiplayer_is_server),
         (assign, ":human_agents_spawned_at_team_1", "$g_multiplayer_num_bots_team_1"),
         (assign, ":human_agents_spawned_at_team_2", "$g_multiplayer_num_bots_team_2"),
         
         (get_max_players, ":num_players"),
         (try_for_range, ":player_no", 0, ":num_players"),
           (player_is_active, ":player_no"),
           (player_get_team_no, ":player_team", ":player_no"), 
           (try_begin),
             (eq, ":player_team", 0),
             (val_add, ":human_agents_spawned_at_team_1", 1),
           (else_try),
             (eq, ":player_team", 1),
             (val_add, ":human_agents_spawned_at_team_2", 1),
           (try_end),
         (try_end),

         (try_begin),
           (this_or_next|eq, ":human_agents_spawned_at_team_1", 0),
           (eq, ":human_agents_spawned_at_team_2", 0),

           (store_mission_timer_a, ":seconds_past_since_round_started"),
           (val_sub, ":seconds_past_since_round_started", "$g_round_start_time"),
           (le, ":seconds_past_since_round_started", 2),
                  
           (store_mission_timer_a, "$g_round_start_time"),
         (try_end),
       ]),    
           
      (1, 0, 0, [],
       [
         (multiplayer_is_server),
         (get_max_players, ":num_players"),
         (try_for_range, ":player_no", 0, ":num_players"),
           (player_is_active, ":player_no"),
           (neg|player_is_busy_with_menus, ":player_no"),
           (try_begin),
             (player_slot_eq, ":player_no", slot_player_spawned_this_round, 0),

             (player_get_team_no, ":player_team", ":player_no"), #if player is currently spectator do not spawn his agent
             (lt, ":player_team", multi_team_spectator),

             (player_get_troop_id, ":player_troop", ":player_no"), #if troop is not selected do not spawn his agent
             (ge, ":player_troop", 0),

             (assign, ":spawn_new", 0), 
             (assign, ":num_active_players_in_team_0", 0),
             (assign, ":num_active_players_in_team_1", 0),
             (try_begin),
               (assign, ":num_active_players", 0),
               (get_max_players, ":num_players"),
               (try_for_range, ":player_no_2", 0, ":num_players"),
                 (player_is_active, ":player_no_2"),
                 (val_add, ":num_active_players", 1),
                 (player_get_team_no, ":player_team_2", ":player_no_2"),
                 (try_begin),
                   (eq, ":player_team_2", 0),
                   (val_add, ":num_active_players_in_team_0", 1),
                 (else_try),
                   (eq, ":player_team_2", 1),
                   (val_add, ":num_active_players_in_team_1", 1),
                 (try_end),
               (try_end),

               (store_mul, ":multipication_of_num_active_players_in_teams", ":num_active_players_in_team_0", ":num_active_players_in_team_1"),

               (store_mission_timer_a, ":round_time"),
               (val_sub, ":round_time", "$g_round_start_time"),

               (this_or_next|lt, ":round_time", multiplayer_new_agents_finish_spawning_time),
               (this_or_next|le, ":num_active_players", 2),
               (eq, ":multipication_of_num_active_players_in_teams", 0),
         
               (eq, "$g_round_ended", 0),
               (assign, ":spawn_new", 1),
             (try_end),
             (eq, ":spawn_new", 1),
             (try_begin),
               (eq, ":player_team", 0),
               (assign, ":entry_no", multi_initial_spawn_point_team_1),
             (else_try),
               (eq, ":player_team", 1),
               (assign, ":entry_no", multi_initial_spawn_point_team_2),
             (try_end),
             (call_script, "script_multiplayer_buy_agent_equipment", ":player_no"),
             (player_spawn_new_agent, ":player_no", ":entry_no"),
             (player_set_slot, ":player_no", slot_player_spawned_this_round, 1),
           (else_try), #spawning as a bot (if option ($g_multiplayer_player_respawn_as_bot) is 1)
             (eq, "$g_multiplayer_player_respawn_as_bot", 1),
             (player_get_agent_id, ":player_agent", ":player_no"),
             (ge, ":player_agent", 0),
             (neg|agent_is_alive, ":player_agent"),
             (agent_get_time_elapsed_since_removed, ":elapsed_time", ":player_agent"),
             (gt, ":elapsed_time", "$g_multiplayer_respawn_period"),

             (player_get_team_no, ":player_team", ":player_no"),
             (assign, ":is_found", 0),
             (try_for_agents, ":cur_agent"),
               (eq, ":is_found", 0),
               (agent_is_alive, ":cur_agent"),
               (agent_is_human, ":cur_agent"),
               (agent_is_non_player, ":cur_agent"),
               (agent_get_team ,":cur_team", ":cur_agent"),
               (eq, ":cur_team", ":player_team"),
               (assign, ":is_found", 1),
               #(player_control_agent, ":player_no", ":cur_agent"),
             (try_end),

             (try_begin),
               (eq, ":is_found", 1),
               (call_script, "script_find_most_suitable_bot_to_control", ":player_no"),
               (player_control_agent, ":player_no", reg0),

               (player_get_slot, ":num_spawns", ":player_no", slot_player_spawned_this_round),
               (val_add, ":num_spawns", 1),
               (player_set_slot, ":player_no", slot_player_spawned_this_round, ":num_spawns"),
             (try_end),
           (try_end),
         (try_end),
         ]),

      multiplayer_server_spawn_bots, 
      multiplayer_server_manage_bots, 

      multiplayer_server_check_end_map,
        
      (ti_tab_pressed, 0, 0, [],
       [
         (try_begin),
           (eq, "$g_multiplayer_mission_end_screen", 0),
           (assign, "$g_multiplayer_stats_chart_opened_manually", 1),
           (start_presentation, "prsnt_multiplayer_stats_chart"),
         (try_end),
         ]),

      multiplayer_once_at_the_first_frame,

      (ti_battle_window_opened, 0, 0, [], [
        (start_presentation, "prsnt_multiplayer_round_time_counter"),
        (start_presentation, "prsnt_multiplayer_team_score_display"),
        (try_begin),
          (eq, "$g_battle_death_mode_started", 2),
          (start_presentation, "prsnt_multiplayer_flag_projection_display_bt"),
        (try_end),
        ]),

      (ti_escape_pressed, 0, 0, [],
       [
         (neg|is_presentation_active, "prsnt_multiplayer_escape_menu"),
         (neg|is_presentation_active, "prsnt_multiplayer_stats_chart"),
         (eq, "$g_waiting_for_confirmation_to_terminate", 0),
         (start_presentation, "prsnt_multiplayer_escape_menu"),
         ]),
      ],
  ),


    (
    "multiplayer_fd",mtf_battle_mode,-1, #fight and destroy mode
    "You lead your men to battle.",
    [
      (0,mtef_visitor_source|mtef_team_0|mtef_no_auto_reset,0,aif_start_alarmed,1,[]),
      (1,mtef_visitor_source|mtef_team_0|mtef_no_auto_reset,0,aif_start_alarmed,1,[]),
      (2,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (3,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (4,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (5,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (6,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (7,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),

      (8,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (9,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (10,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (11,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (12,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (13,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (14,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (15,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),

      (16,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (17,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (18,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (19,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (20,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (21,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (22,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (23,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),

      (24,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (25,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (26,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (27,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (28,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (29,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (30,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (31,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),

      (32,mtef_visitor_source|mtef_team_0|mtef_no_auto_reset,0,aif_start_alarmed,1,[]),
      (33,mtef_visitor_source|mtef_team_0|mtef_no_auto_reset,0,aif_start_alarmed,1,[]),
      (34,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (35,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (36,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (37,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (38,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (39,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),

      (40,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (41,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (42,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (43,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (44,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (45,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (46,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (47,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),

      (48,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (49,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (50,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (51,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (52,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (53,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (54,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (55,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),

      (56,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (57,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (58,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (59,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (60,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (61,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (62,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (63,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
     ],
    [
      common_battle_init_banner,

      multiplayer_server_check_polls,
      
      (ti_server_player_joined, 0, 0, [],
       [
         (store_trigger_param_1, ":player_no"),
         (call_script, "script_multiplayer_server_player_joined_common", ":player_no"),
         ]),

      (ti_before_mission_start, 0, 0, [],
       [
         (assign, "$g_multiplayer_game_type", multiplayer_game_type_destroy),
         (call_script, "script_multiplayer_server_before_mission_start_common"),

         (assign, "$g_waiting_for_confirmation_to_terminate", 0),
         (assign, "$g_round_ended", 0),
         (assign, "$g_reduced_waiting_seconds", 0),

         (try_begin),
           (multiplayer_is_server),
           (assign, "$g_round_start_time", 0),
         (try_end),
         (assign, "$my_team_at_start_of_round", -1),

         (call_script, "script_multiplayer_init_mission_variables"),
         (call_script, "script_multiplayer_remove_headquarters_flags"),         
         ]),

      (ti_after_mission_start, 0, 0, [], 
       [
         (call_script, "script_determine_team_flags", 0),
         (call_script, "script_determine_team_flags", 1),
         (set_spawn_effector_scene_prop_kind, 0, -1), #during this mission, agents of "team 0" will try to spawn around scene props with kind equal to -1(no effector for this mod)
         (set_spawn_effector_scene_prop_kind, 1, -1), #during this mission, agents of "team 1" will try to spawn around scene props with kind equal to -1(no effector for this mod)

         (call_script, "script_initialize_all_scene_prop_slots"),
         
         (call_script, "script_multiplayer_initialize_belfry_wheel_rotations"),
         (call_script, "script_multiplayer_move_moveable_objects_initial_positions"),

         (assign, "$g_destructible_target_1", "spr_catapult_destructible"),
         (assign, "$g_destructible_target_2", "spr_trebuchet_destructible"),

         #assigning destructible object team nos to 0. (0 is also used for showing defender team in siege mode)
         (scene_prop_get_num_instances, ":num_destructible_target_1", "$g_destructible_target_1"),
         (try_for_range, ":destructible_target_1_no", 0, ":num_destructible_target_1"),
           (scene_prop_get_instance, ":destructible_target_1_id", "$g_destructible_target_1", ":destructible_target_1_no"),
           (ge, ":destructible_target_1_id", 0),
           (scene_prop_set_team, ":destructible_target_1_id", 0),
         (try_end),

         (scene_prop_get_num_instances, ":num_destructible_target_2", "$g_destructible_target_2"),
         (try_for_range, ":destructible_target_2_no", 0, ":num_destructible_target_2"),
           (scene_prop_get_instance, ":destructible_target_2_id", "$g_destructible_target_2", ":destructible_target_2_no"),
           (ge, ":destructible_target_2_id", 0),
           (scene_prop_set_team, ":destructible_target_2_id", 0),
         (try_end),

         (try_begin),
           (scene_prop_get_num_instances, ":num_catapults", "spr_catapult_destructible"),
           (ge, ":num_catapults", 1),
           (scene_prop_get_instance, ":catapult_scene_prop_id", "spr_catapult_destructible", 0),
           (scene_prop_get_team, "$g_defender_team", ":catapult_scene_prop_id"),
         (else_try),         
           (scene_prop_get_num_instances, ":num_trebuchets", "spr_trebuchet_destructible"),
           (ge, ":num_trebuchets", 1),
           (scene_prop_get_instance, ":trebuchet_scene_prop_id", "spr_trebuchet_destructible", 0),
           (scene_prop_get_team, "$g_defender_team", ":trebuchet_scene_prop_id"),
         (try_end),

         (assign, "$g_number_of_targets_destroyed", 0),

         (try_begin),
           (assign, "$g_multiplayer_num_bots_required_team_1", "$g_multiplayer_num_bots_team_1"), 
           (assign, "$g_multiplayer_num_bots_required_team_2", "$g_multiplayer_num_bots_team_2"), 
         (try_end),

         (start_presentation, "prsnt_multiplayer_destructible_targets_display"),

         (assign, "$g_multiplayer_ready_for_spawning_agent", 1),
        ]),

      (ti_on_agent_spawn, 0, 0, [],
       [
         (store_trigger_param_1, ":agent_no"),
         (call_script, "script_multiplayer_server_on_agent_spawn_common", ":agent_no"),
         
         (try_begin), #if my initial team still not initialized, find and assign its value.
           (lt, "$my_team_at_start_of_round", 0),
           (multiplayer_get_my_player, ":my_player_no"),
           (ge, ":my_player_no", 0),
           (player_get_agent_id, ":my_agent_id", ":my_player_no"),
           (eq, ":my_agent_id", ":agent_no"),
           (ge, ":my_agent_id", 0),
           (agent_get_team, "$my_team_at_start_of_round", ":my_agent_id"),
         (try_end),         
          
         (try_begin),
           (neg|multiplayer_is_server),
           (try_begin),
             (eq, "$g_round_ended", 1),
             (assign, "$g_round_ended", 0),

             #initialize scene object slots at start of new round at clients.
             (call_script, "script_initialize_all_scene_prop_slots"),

             #these lines are done in only clients at start of each new round.
             (call_script, "script_multiplayer_initialize_belfry_wheel_rotations"),
             (call_script, "script_initialize_objects_clients"),
             #end of lines
        
             (start_presentation, "prsnt_multiplayer_destructible_targets_display"),
             (try_begin),
               (eq, "$g_team_balance_next_round", 1),
               (assign, "$g_team_balance_next_round", 0),
             (try_end),
           (try_end),  
         (try_end),         
         ]),

      (ti_on_agent_killed_or_wounded, 0, 0, [],
       [
         (store_trigger_param_1, ":dead_agent_no"),
         (store_trigger_param_2, ":killer_agent_no"),

         (call_script, "script_multiplayer_server_on_agent_killed_or_wounded_common", ":dead_agent_no", ":killer_agent_no"),

         (try_begin), #if my initial team still not initialized, find and assign its value.
           (lt, "$my_team_at_start_of_round", 0),
           (multiplayer_get_my_player, ":my_player_no"),
           (ge, ":my_player_no", 0),
           (player_get_agent_id, ":my_agent_id", ":my_player_no"),
           (ge, ":my_agent_id", 0),
           (agent_get_team, "$my_team_at_start_of_round", ":my_agent_id"),
         (try_end),         
         
         (try_begin), #count players and if round ended understand this.
           (agent_is_human, ":dead_agent_no"),
           (assign, ":team1_living_players", 0),
           (assign, ":team2_living_players", 0),
           (try_for_agents, ":cur_agent"),
             (agent_is_human, ":cur_agent"),         
             (try_begin),
               (agent_is_alive, ":cur_agent"),  
               (agent_get_team, ":cur_agent_team", ":cur_agent"),
               (try_begin),
                 (eq, ":cur_agent_team", 0),
               (val_add, ":team1_living_players", 1),
               (else_try),
                 (eq, ":cur_agent_team", 1),
                 (val_add, ":team2_living_players", 1),
               (try_end),
             (try_end),
           (try_end),                    
           (try_begin),         
             (eq, "$g_round_ended", 0),
             (try_begin),
               (this_or_next|eq, ":team1_living_players", 0),
               (eq, ":team2_living_players", 0),                
               (assign, "$g_winner_team", -1),
               (assign, reg0, "$g_multiplayer_respawn_period"),
               (try_begin),
                 (eq, ":team1_living_players", 0),
                 (try_begin),
                   (neq, ":team2_living_players", 0),
                   (assign, "$g_winner_team", 1),
                 (try_end),

                 (try_begin),
                   (eq, "$g_winner_team", -1),
                 (else_try),
                   (eq, "$g_defender_team", 1), #if defender team killed all attackers
                   (try_begin),
                     (neg|multiplayer_is_server),
                     (call_script, "script_calculate_number_of_targets_destroyed"),
                   (try_end),
                   (store_sub, ":num_targets_saved", 2, "$g_number_of_targets_destroyed"),
                   (call_script, "script_show_multiplayer_message", multiplayer_message_type_defenders_saved_n_targets, ":num_targets_saved"), #1 or -1 is winner team
                 (else_try),
                   (call_script, "script_show_multiplayer_message", multiplayer_message_type_attackers_won_the_round, 0), #1 or -1 is winner team
                 (try_end),        
               (else_try),
                 (try_begin),
                   (neq, ":team1_living_players", 0),
                   (assign, "$g_winner_team", 0),
                 (try_end),

                 (try_begin),
                   (eq, "$g_winner_team", -1),         
                 (else_try),
                   (eq, "$g_defender_team", 0), #if defender team killed all attackers
                   (try_begin),
                     (neg|multiplayer_is_server),
                     (call_script, "script_calculate_number_of_targets_destroyed"),
                   (try_end),
                   (store_sub, ":num_targets_saved", 2, "$g_number_of_targets_destroyed"),
                   (call_script, "script_show_multiplayer_message", multiplayer_message_type_defenders_saved_n_targets, ":num_targets_saved"), #0 or -1 is winner team
                 (else_try),
                   (call_script, "script_show_multiplayer_message", multiplayer_message_type_attackers_won_the_round, 0), #0 or -1 is winner team
                 (try_end),         
               (try_end),
               (store_mission_timer_a, "$g_round_finish_time"),
               (assign, "$g_round_ended", 1),


               (try_begin), #destroy score (condition : remained no one)
                 (multiplayer_is_server),
                 (ge, "$g_winner_team", 0),
                 (lt, "$g_winner_team", 2),
                 (neq, "$g_winner_team", -1),

                 (team_get_score, ":team_score", "$g_winner_team"),
                 (store_sub, ":num_targets_remained", 2, "$g_number_of_targets_destroyed"),
                 (val_add, ":team_score", ":num_targets_remained"),

                 #for only server itself-----------------------------------------------------------------------------------------------
                 (call_script, "script_team_set_score", "$g_winner_team", ":team_score"),
                 #for only server itself-----------------------------------------------------------------------------------------------
                 (get_max_players, ":num_players"),
                 (try_for_range, ":player_no", 1, ":num_players"), #0 is server so starting from 1
                   (player_is_active, ":player_no"),
                   (multiplayer_send_2_int_to_player, ":player_no", multiplayer_event_set_team_score, "$g_winner_team", ":team_score"),
                 (try_end),
               (try_end), #destroy score end

         
               (try_begin),
                 (neq, "$g_defender_team", "$g_winner_team"),
                 (neq, "$g_winner_team", -1),
                 (assign, "$g_number_of_targets_destroyed", 2),              
               (try_end),
             (try_end),
           (try_end),
         (try_end),

         (try_begin),
           (multiplayer_is_server),
           (agent_is_human, ":dead_agent_no"),
           (neg|agent_is_non_player, ":dead_agent_no"),

           (ge, ":dead_agent_no", 0),
           (agent_get_player_id, ":dead_agent_player_id", ":dead_agent_no"),
           (ge, ":dead_agent_player_id", 0),

           (set_fixed_point_multiplier, 100),

           (agent_get_player_id, ":dead_agent_player_id", ":dead_agent_no"),
           (agent_get_position, pos0, ":dead_agent_no"),

           (position_get_x, ":x_coor", pos0),
           (position_get_y, ":y_coor", pos0),
           (position_get_z, ":z_coor", pos0),
         
           (player_set_slot, ":dead_agent_player_id", slot_player_death_pos_x, ":x_coor"),
           (player_set_slot, ":dead_agent_player_id", slot_player_death_pos_y, ":y_coor"),
           (player_set_slot, ":dead_agent_player_id", slot_player_death_pos_z, ":z_coor"),
         (try_end),    
         ]),

      (ti_on_multiplayer_mission_end, 0, 0, [],
       [
         (call_script, "script_multiplayer_event_mission_end"),
         (assign, "$g_multiplayer_stats_chart_opened_manually", 0),
         (start_presentation, "prsnt_multiplayer_stats_chart"),
         ]),

      
      (1, 0, 0, [(multiplayer_is_server), 
                 (eq, "$g_round_ended", 0),
                 (eq, "$g_number_of_targets_destroyed", 2),
                 ],
       [
         (store_mission_timer_a, "$g_round_finish_time"),
         (assign, "$g_round_ended", 1),         

         (multiplayer_get_my_player, ":my_player_no"), #send all players draw information of round.
         #for only server itself-----------------------------------------------------------------------------------------------
         (call_script, "script_draw_this_round", -9),
         #for only server itself-----------------------------------------------------------------------------------------------
         (get_max_players, ":num_players"), 
         (try_for_range, ":player_no", 1, ":num_players"), #0 is server so starting from 1
           (player_is_active, ":player_no"),
           (neq, ":player_no", ":my_player_no"),
           (multiplayer_send_int_to_player, ":player_no", multiplayer_event_draw_this_round, -9),
         (try_end),
         ]),
      
      (1, 0, 0, [(multiplayer_is_server), 
                 (eq, "$g_round_ended", 0),
                 (store_mission_timer_a, ":current_time"),
                 (store_sub, ":seconds_past_in_round", ":current_time", "$g_round_start_time"),
                 (ge, ":seconds_past_in_round", "$g_multiplayer_round_max_seconds"),
                 ],
       [ #round time is up
         (store_mission_timer_a, "$g_round_finish_time"),                          
         (assign, "$g_round_ended", 1),
         (assign, "$g_winner_team", -9),
         
         (multiplayer_get_my_player, ":my_player_no"), #send all players draw information of round.

         (store_sub, ":num_targets_saved", 2, "$g_number_of_targets_destroyed"),
         #for only server itself-----------------------------------------------------------------------------------------------
         (call_script, "script_show_multiplayer_message", multiplayer_message_type_defenders_saved_n_targets, ":num_targets_saved"), 
         #for only server itself-----------------------------------------------------------------------------------------------     
         (get_max_players, ":num_players"),
         (try_for_range, ":player_no", 1, ":num_players"), #0 is server so starting from 1
           (player_is_active, ":player_no"),
           (multiplayer_send_2_int_to_player, ":player_no", multiplayer_event_show_multiplayer_message, multiplayer_message_type_defenders_saved_n_targets, ":num_targets_saved"),
         (try_end),

         #for only server itself-----------------------------------------------------------------------------------------------
         (call_script, "script_draw_this_round", "$g_winner_team"),
         #for only server itself-----------------------------------------------------------------------------------------------
         (get_max_players, ":num_players"), 
         (try_for_range, ":player_no", 1, ":num_players"), #0 is server so starting from 1
           (player_is_active, ":player_no"),
           (neq, ":player_no", ":my_player_no"),
           (multiplayer_send_int_to_player, ":player_no", multiplayer_event_draw_this_round, "$g_winner_team"),
         (try_end),
                         
         (try_begin), #destroy score (condition : time is up)
           (multiplayer_is_server),
           (assign, "$g_winner_team", "$g_defender_team"),         
         
           (team_get_score, ":team_score", "$g_winner_team"),
           (store_sub, ":num_targets_remained", 2, "$g_number_of_targets_destroyed"),
           (val_add, ":team_score", ":num_targets_remained"),

           #for only server itself-----------------------------------------------------------------------------------------------
           (call_script, "script_team_set_score", "$g_winner_team", ":team_score"),
           #for only server itself-----------------------------------------------------------------------------------------------
           (try_for_range, ":player_no", 1, ":num_players"), #0 is server so starting from 1
             (player_is_active, ":player_no"),
             (multiplayer_send_2_int_to_player, ":player_no", multiplayer_event_set_team_score, "$g_winner_team", ":team_score"),
           (try_end),
         (try_end), #destroy score end        
        ]),          

      (10, 0, 0, [(multiplayer_is_server)],
       [
         #auto team balance control during the round         
         (assign, ":number_of_players_at_team_1", 0),
         (assign, ":number_of_players_at_team_2", 0),
         (get_max_players, ":num_players"),
         (try_for_range, ":cur_player", 0, ":num_players"),
           (player_is_active, ":cur_player"),
           (player_get_team_no, ":player_team", ":cur_player"),
           (try_begin),
             (eq, ":player_team", 0),
             (val_add, ":number_of_players_at_team_1", 1),
           (else_try),
             (eq, ":player_team", 1),
             (val_add, ":number_of_players_at_team_2", 1),
           (try_end),         
         (try_end),
         #end of counting active players per team.
         (store_sub, ":difference_of_number_of_players", ":number_of_players_at_team_1", ":number_of_players_at_team_2"),
         (assign, ":number_of_players_will_be_moved", 0),
         (try_begin),
           (try_begin),
             (store_mul, ":checked_value", "$g_multiplayer_auto_team_balance_limit", -1),
             (le, ":difference_of_number_of_players", ":checked_value"),
             (store_div, ":number_of_players_will_be_moved", ":difference_of_number_of_players", -2),
           (else_try),
             (ge, ":difference_of_number_of_players", "$g_multiplayer_auto_team_balance_limit"),
             (store_div, ":number_of_players_will_be_moved", ":difference_of_number_of_players", 2),
           (try_end),          
         (try_end),         
         #number of players will be moved calculated. (it is 0 if no need to make team balance)
         (try_begin),
           (gt, ":number_of_players_will_be_moved", 0),
           (try_begin),
             (eq, "$g_team_balance_next_round", 0),
         
             (assign, "$g_team_balance_next_round", 1),

             #for only server itself-----------------------------------------------------------------------------------------------
             (call_script, "script_show_multiplayer_message", multiplayer_message_type_auto_team_balance_next, 0), #0 is useless here
             #for only server itself-----------------------------------------------------------------------------------------------     
             (get_max_players, ":num_players"),                               
             (try_for_range, ":player_no", 1, ":num_players"), #0 is server so starting from 1
               (player_is_active, ":player_no"),
               (multiplayer_send_int_to_player, ":player_no", multiplayer_event_show_multiplayer_message, multiplayer_message_type_auto_team_balance_next),
             (try_end),
             
             (call_script, "script_warn_player_about_auto_team_balance"),
           (try_end),
         (try_end),           
         #team balance check part finished
         ]),

      (0, 0, 0, [(multiplayer_is_server),  
                 (eq, "$g_round_ended", 0),                 
                 (eq, "$g_battle_death_mode_started", 2)],
       [
         (set_fixed_point_multiplier, 100),
         (scene_prop_get_instance, ":pole_1_id", "spr_headquarters_pole_code_only", 0),
         (scene_prop_get_instance, ":pole_2_id", "spr_headquarters_pole_code_only", 1),
         (scene_prop_get_instance, ":flag_1_id", "$team_1_flag_scene_prop", 0),
         (scene_prop_get_instance, ":flag_2_id", "$team_2_flag_scene_prop", 0),

         (prop_instance_get_position, pos1, ":pole_1_id"),
         (prop_instance_get_position, pos2, ":pole_2_id"),
         (prop_instance_get_position, pos3, ":flag_1_id"),
         (prop_instance_get_position, pos4, ":flag_2_id"),

         (copy_position, pos7, pos1),
         (position_move_z, pos7, multi_headquarters_flag_initial_height),
         (copy_position, pos8, pos2),
         (position_move_z, pos8, multi_headquarters_flag_initial_height),

         (get_distance_between_positions, ":dist_1", pos1, pos3),
         (get_distance_between_positions, ":dist_2", pos2, pos4),

         (assign, ":there_are_agents_from_only_team_1_around_their_flag", 0),
         (assign, ":there_are_agents_from_only_team_2_around_their_flag", 0),
         (get_max_players, ":num_players"),
         (try_for_range, ":player_no", 0, ":num_players"),
           (player_is_active, ":player_no"),
           (player_get_agent_id, ":agent_id", ":player_no"),
           (ge, ":agent_id", 0),
           (agent_is_human, ":agent_id"),
           (agent_is_alive, ":agent_id"),
           (agent_get_team, ":agent_team", ":agent_id"),
           (agent_get_position, pos0, ":agent_id"),

           (agent_get_horse, ":agent_horse", ":agent_id"),
           (eq, ":agent_horse", -1), #horseman cannot move flag
         
           (try_begin),
             (eq, ":agent_team", 0),
             (try_begin),
               (get_sq_distance_between_positions, ":squared_dist", pos0, pos1),
               (lt, ":squared_dist", multi_headquarters_max_distance_sq_to_raise_flags),
               (try_begin), #we found a team_1 agent in the flag_1 area, so flag_1 situation can be 1 or -2
                 (eq, ":there_are_agents_from_only_team_1_around_their_flag", 0),
                 (assign, ":there_are_agents_from_only_team_1_around_their_flag", 1), #there are agents from only our team
               (else_try),
                 (eq, ":there_are_agents_from_only_team_1_around_their_flag", -1),
                 (assign, ":there_are_agents_from_only_team_1_around_their_flag", -2), #there are agents from both teams
               (try_end),
             (try_end),
             (try_begin),
               (get_sq_distance_between_positions, ":squared_dist", pos0, pos2),
               (lt, ":squared_dist", multi_headquarters_max_distance_sq_to_raise_flags),
               (try_begin), #we found a team_1 agent in the flag_2 area, so flag_2 situation can be -1 or -2
                 (eq, ":there_are_agents_from_only_team_2_around_their_flag", 0),
                 (assign, ":there_are_agents_from_only_team_2_around_their_flag", -1), #there are agents from only rival team
               (else_try),
                 (eq, ":there_are_agents_from_only_team_2_around_their_flag", 1),
                 (assign, ":there_are_agents_from_only_team_2_around_their_flag", -2), #there are agents from both teams
               (try_end),
             (try_end),
           (else_try),
             (eq, ":agent_team", 1),
             (try_begin),
               (get_sq_distance_between_positions, ":squared_dist", pos0, pos2),
               (lt, ":squared_dist", multi_headquarters_max_distance_sq_to_raise_flags),
               (try_begin), #we found a team_2 agent in the flag 2 area, so flag_2 situation can be 1 or -2
                 (eq, ":there_are_agents_from_only_team_2_around_their_flag", 0),
                 (assign, ":there_are_agents_from_only_team_2_around_their_flag", 1), #there are agents from only our team
               (else_try),
                 (assign, ":there_are_agents_from_only_team_2_around_their_flag", -2), #there are agents from both teams
               (try_end),
             (try_end),
             (try_begin),
               (get_sq_distance_between_positions, ":squared_dist", pos0, pos1),
               (lt, ":squared_dist", multi_headquarters_max_distance_sq_to_raise_flags),
               (try_begin), #we found a team_2 agent in the flag_1 area, so flag_1 situation can be -1 or -2
                 (eq, ":there_are_agents_from_only_team_1_around_their_flag", 0),
                 (assign, ":there_are_agents_from_only_team_1_around_their_flag", -1), #there are agents from only rival team
               (else_try),
                 (eq, ":there_are_agents_from_only_team_1_around_their_flag", 1),
                 (assign, ":there_are_agents_from_only_team_1_around_their_flag", -2), #there are agents from both teams
               (try_end),
             (try_end),
           (try_end),
         (try_end),

         #controlling battle win by death mode conditions
         (try_begin),
           (ge, ":dist_1", multi_headquarters_flag_height_to_win),           
           (assign, "$g_winner_team", 0),

           (get_max_players, ":num_players"), 
           #for only server itself-----------------------------------------------------------------------------------------------
           (call_script, "script_draw_this_round", "$g_winner_team"),
           #for only server itself-----------------------------------------------------------------------------------------------
           (try_for_range, ":player_no", 1, ":num_players"), #0 is server so starting from 1
             (player_is_active, ":player_no"),
             (multiplayer_send_int_to_player, ":player_no", multiplayer_event_draw_this_round, "$g_winner_team"),
           (try_end),

           (team_get_score, ":team_1_score", 0),
           #for only server itself-----------------------------------------------------------------------------------------------
           (call_script, "script_team_set_score", 0, ":team_1_score"),
           #for only server itself-----------------------------------------------------------------------------------------------
           (try_for_range, ":player_no", 1, ":num_players"), #0 is server so starting from 1
             (player_is_active, ":player_no"),
             (multiplayer_send_2_int_to_player, ":player_no", multiplayer_event_set_team_score, 0, ":team_1_score"),             
           (try_end),

           (store_mission_timer_a, "$g_round_finish_time"),
           (assign, "$g_round_ended", 1),
         (else_try),
           (ge, ":dist_2", multi_headquarters_flag_height_to_win),
           (assign, "$g_winner_team", 1),

           (get_max_players, ":num_players"), 
           #for only server itself-----------------------------------------------------------------------------------------------
           (call_script, "script_draw_this_round", "$g_winner_team"),
           #for only server itself-----------------------------------------------------------------------------------------------
           (try_for_range, ":player_no", 1, ":num_players"), #0 is server so starting from 1
             (player_is_active, ":player_no"),
             (multiplayer_send_int_to_player, ":player_no", multiplayer_event_draw_this_round, "$g_winner_team"),
           (try_end),

           (team_get_score, ":team_2_score", 1),
           #for only server itself-----------------------------------------------------------------------------------------------
           (call_script, "script_team_set_score", 1, ":team_2_score"),
           #for only server itself-----------------------------------------------------------------------------------------------
           (try_for_range, ":player_no", 1, ":num_players"), #0 is server so starting from 1
             (player_is_active, ":player_no"),
             (multiplayer_send_2_int_to_player, ":player_no", multiplayer_event_set_team_score, 1, ":team_2_score"),             
           (try_end),
	
           (call_script, "script_show_multiplayer_message", multiplayer_message_type_round_result_in_battle_mode, 0), #0 is winner team     
           (call_script, "script_check_achievement_last_man_standing", "$g_winner_team"),    

           (store_mission_timer_a, "$g_round_finish_time"),
           (assign, "$g_round_ended", 1),
         (try_end),

         (try_begin),
           (eq, "$g_round_ended", 0),

           (position_get_z, ":flag_1_cur_z", pos3),       
           (prop_instance_is_animating, ":is_animating", ":flag_1_id"),         
           (try_begin), #if flag_1 is going down or up and there are agents from both teams
             (eq, ":there_are_agents_from_only_team_1_around_their_flag", -2), #if there are agents from both teams
             (eq, ":is_animating", 1),
             (prop_instance_stop_animating, ":flag_1_id"), #stop flag_1
           (else_try), #if flag_1 is going down
             (this_or_next|eq, ":there_are_agents_from_only_team_1_around_their_flag", 0), #if there is no one
             (eq, ":there_are_agents_from_only_team_1_around_their_flag", -1), #if there are agents from only team_2 (enemy of team_1)
             (prop_instance_get_animation_target_position, pos9, ":flag_1_id"),
             (position_get_z, ":flag_1_animation_target_z", pos9),
             (this_or_next|eq, ":is_animating", 0), #if flag_1 is stopping
             (gt, ":flag_1_animation_target_z", ":flag_1_cur_z"), #if flag_1 is going up         
             (get_distance_between_positions, ":time_1", pos3, pos7),
             (gt, ":time_1", 0),
             (val_mul, ":time_1", 16),
             (prop_instance_animate_to_position, ":flag_1_id", pos7, ":time_1"), #move flag_1 down
           (else_try), #if flag_1 is going down or stopping
             (eq, ":there_are_agents_from_only_team_1_around_their_flag", 1), #if there is agents from only team_1 (current team)
             (prop_instance_get_animation_target_position, pos9, ":flag_1_id"),
             (position_get_z, ":flag_1_animation_target_z", pos9),
             (this_or_next|eq, ":is_animating", 0), #if flag_1 is stopping
             (lt, ":flag_1_animation_target_z", ":flag_1_cur_z"), #if flag_1 is going down
             (copy_position, pos5, pos1),
             (position_move_z, pos5, multi_headquarters_flag_height_to_win),
             (get_distance_between_positions, ":time_1", pos3, pos5),
             (gt, ":time_1", 0),
             (val_mul, ":time_1", 8),
             (prop_instance_animate_to_position, ":flag_1_id", pos5, ":time_1"), #move flag_1 up
           (try_end),

           (position_get_z, ":flag_2_cur_z", pos4),       
           (prop_instance_is_animating, ":is_animating", ":flag_2_id"),         
           (try_begin), #if flag is going down or up and there are agents from both teams
             (eq, ":there_are_agents_from_only_team_2_around_their_flag", -2), #if there are agents from both teams
             (eq, ":is_animating", 1),
             (prop_instance_stop_animating, ":flag_2_id"), #stop flag_2
           (else_try), #if flag_2 is going down
             (this_or_next|eq, ":there_are_agents_from_only_team_2_around_their_flag", 0), #if there is no one
             (eq, ":there_are_agents_from_only_team_2_around_their_flag", -1), #if there are agents from only team_1 (enemy of team_1)
             (prop_instance_get_animation_target_position, pos9, ":flag_2_id"),
             (position_get_z, ":flag_2_animation_target_z", pos9),
             (this_or_next|eq, ":is_animating", 0), #if flag_2 is stopping
             (gt, ":flag_2_animation_target_z", ":flag_2_cur_z"), #if flag_2 is going up         
             (get_distance_between_positions, ":time_2", pos4, pos8),
             (gt, ":time_2", 0),
             (val_mul, ":time_2", 16),
             (prop_instance_animate_to_position, ":flag_2_id", pos8, ":time_2"), #move flag_2 down
           (else_try), #if flag_2 is going down or stopping
             (eq, ":there_are_agents_from_only_team_2_around_their_flag", 1), #if there is agents from only team_2 (current team)
             (prop_instance_get_animation_target_position, pos9, ":flag_2_id"),
             (position_get_z, ":flag_2_animation_target_z", pos9),
             (this_or_next|eq, ":is_animating", 0), #if flag_2 is stopping
             (lt, ":flag_2_animation_target_z", ":flag_2_cur_z"), #if flag_2 is going down
             (copy_position, pos6, pos2),
             (position_move_z, pos6, multi_headquarters_flag_height_to_win),
             (get_distance_between_positions, ":time_2", pos4, pos6),
             (gt, ":time_2", 0),
             (val_mul, ":time_2", 8),
             (prop_instance_animate_to_position, ":flag_2_id", pos6, ":time_2"), #move flag_2 up
           (try_end),
         (try_end),
         ]),
                
      (1, 0, 3, [(multiplayer_is_server),
                 (eq, "$g_round_ended", 1),
                 (store_mission_timer_a, ":seconds_past_till_round_ended"),
                 (val_sub, ":seconds_past_till_round_ended", "$g_round_finish_time"),
                 (ge, ":seconds_past_till_round_ended", "$g_multiplayer_respawn_period")],
       [
         #auto team balance control at the end of round         
         (assign, ":number_of_players_at_team_1", 0),
         (assign, ":number_of_players_at_team_2", 0),
         (get_max_players, ":num_players"),
         (try_for_range, ":cur_player", 0, ":num_players"),
           (player_is_active, ":cur_player"),
           (player_get_team_no, ":player_team", ":cur_player"),
           (try_begin),
             (eq, ":player_team", 0),
             (val_add, ":number_of_players_at_team_1", 1),
           (else_try),
             (eq, ":player_team", 1),
             (val_add, ":number_of_players_at_team_2", 1),
           (try_end),         
         (try_end),
         #end of counting active players per team.
         (store_sub, ":difference_of_number_of_players", ":number_of_players_at_team_1", ":number_of_players_at_team_2"),
         (assign, ":number_of_players_will_be_moved", 0),
         (try_begin),
           (try_begin),
             (store_mul, ":checked_value", "$g_multiplayer_auto_team_balance_limit", -1),
             (le, ":difference_of_number_of_players", ":checked_value"),
             (store_div, ":number_of_players_will_be_moved", ":difference_of_number_of_players", -2),
             (assign, ":team_with_more_players", 1),
             (assign, ":team_with_less_players", 0),
           (else_try),
             (ge, ":difference_of_number_of_players", "$g_multiplayer_auto_team_balance_limit"),
             (store_div, ":number_of_players_will_be_moved", ":difference_of_number_of_players", 2),
             (assign, ":team_with_more_players", 0),
             (assign, ":team_with_less_players", 1),
           (try_end),          
         (try_end),         
         #number of players will be moved calculated. (it is 0 if no need to make team balance)
         (try_begin),
           (gt, ":number_of_players_will_be_moved", 0),
           (try_begin),
             #(eq, "$g_team_balance_next_round", 1), #control if at pre round players are warned about team change.

             (try_for_range, ":unused", 0, ":number_of_players_will_be_moved"), 
               (assign, ":max_player_join_time", 0),
               (assign, ":latest_joined_player_no", -1),
               (get_max_players, ":num_players"),                               
               (try_for_range, ":player_no", 0, ":num_players"),
                 (player_is_active, ":player_no"),
                 (player_get_team_no, ":player_team", ":player_no"),
                 (eq, ":player_team", ":team_with_more_players"),
                 (player_get_slot, ":player_join_time", ":player_no", slot_player_join_time),
                 (try_begin),
                   (gt, ":player_join_time", ":max_player_join_time"),
                   (assign, ":max_player_join_time", ":player_join_time"),
                   (assign, ":latest_joined_player_no", ":player_no"),
                 (try_end),
               (try_end),
               (try_begin),
                 (ge, ":latest_joined_player_no", 0),
                 (try_begin),
                   #if player is living add +1 to his kill count because he will get -1 because of team change while living.
                   (player_get_agent_id, ":latest_joined_agent_id", ":latest_joined_player_no"), 
                   (ge, ":latest_joined_agent_id", 0),
                   (agent_is_alive, ":latest_joined_agent_id"),

                   (player_get_kill_count, ":player_kill_count", ":latest_joined_player_no"), #adding 1 to his kill count, because he will lose 1 undeserved kill count for dying during team change
                   (val_add, ":player_kill_count", 1),
                   (player_set_kill_count, ":latest_joined_player_no", ":player_kill_count"),

                   (player_get_death_count, ":player_death_count", ":latest_joined_player_no"), #subtracting 1 to his death count, because he will gain 1 undeserved death count for dying during team change
                   (val_sub, ":player_death_count", 1),
                   (player_set_death_count, ":latest_joined_player_no", ":player_death_count"),

                   (player_get_score, ":player_score", ":latest_joined_player_no"), #adding 1 to his score count, because he will lose 1 undeserved score for dying during team change
                   (val_add, ":player_score", 1),
                   (player_set_score, ":latest_joined_player_no", ":player_score"),

                   (try_for_range, ":player_no", 1, ":num_players"), #0 is server so starting from 1
                     (player_is_active, ":player_no"),
                     (multiplayer_send_4_int_to_player, ":player_no", multiplayer_event_set_player_score_kill_death, ":latest_joined_player_no", ":player_score", ":player_kill_count", ":player_death_count"),
                   (try_end),         

                   (player_get_value_of_original_items, ":old_items_value", ":latest_joined_player_no"),
                   (player_get_gold, ":player_gold", ":latest_joined_player_no"),
                   (val_add, ":player_gold", ":old_items_value"),
                   (player_set_gold, ":latest_joined_player_no", ":player_gold", multi_max_gold_that_can_be_stored),
                 (end_try),

                 (player_set_troop_id, ":latest_joined_player_no", -1),
                 (player_set_team_no, ":latest_joined_player_no", ":team_with_less_players"),
                 (multiplayer_send_message_to_player, ":latest_joined_player_no", multiplayer_event_force_start_team_selection),
               (try_end),
             (try_end),
             #tutorial message (after team balance)
             
             #(tutorial_message_set_position, 500, 500),
             #(tutorial_message_set_size, 30, 30),
             #(tutorial_message_set_center_justify, 1),
             #(tutorial_message, "str_auto_team_balance_done", 0xFFFFFFFF, 5),

             #for only server itself
             (call_script, "script_show_multiplayer_message", multiplayer_message_type_auto_team_balance_done, 0), 

             #no need to send also server here
             (multiplayer_get_my_player, ":my_player_no"),
             (get_max_players, ":num_players"),                               
             (try_for_range, ":player_no", 0, ":num_players"),
               (player_is_active, ":player_no"),
               (neq, ":my_player_no", ":player_no"),
               (multiplayer_send_int_to_player, ":player_no", multiplayer_event_show_multiplayer_message, multiplayer_message_type_auto_team_balance_done),
             (try_end),
             (assign, "$g_team_balance_next_round", 0),
           (try_end),
         (try_end),           
         #team balance check part finished
         (assign, "$g_team_balance_next_round", 0),

         (get_max_players, ":num_players"),
         (try_for_range, ":player_no", 0, ":num_players"),
           (player_is_active, ":player_no"),           
           (player_get_agent_id, ":player_agent", ":player_no"),
           (ge, ":player_agent", 0),
           (agent_is_alive, ":player_agent"),
           (player_save_picked_up_items_for_next_spawn, ":player_no"),
           (player_get_value_of_original_items, ":old_items_value", ":player_no"),
           (player_set_slot, ":player_no", slot_player_last_rounds_used_item_earnings, ":old_items_value"),
         (try_end),

         #money management
         (assign, ":per_round_gold_addition", multi_battle_round_team_money_add),
         (val_mul, ":per_round_gold_addition", "$g_multiplayer_round_earnings_multiplier"),
         (val_div, ":per_round_gold_addition", 100),
         
         (store_sub, ":num_targets_remained", 2, "$g_number_of_targets_destroyed"),
         (store_mul, ":defender_money_add", ":num_targets_remained", multi_destroy_save_or_destroy_target_money_add),
         (store_mul, ":attacker_money_add", "$g_number_of_targets_destroyed", multi_destroy_save_or_destroy_target_money_add),
         (val_add, ":defender_money_add", 100), #defenders cannot get money from destroying catapult thats why they get more money per round.
         (val_sub, ":attacker_money_add", 100), #attackers also get money from destroying catapult thats why they get less money per round.
         (get_max_players, ":num_players"),

         (val_mul, ":defender_money_add", "$g_multiplayer_round_earnings_multiplier"),
         (val_div, ":defender_money_add", 100),
         (val_mul, ":attacker_money_add", "$g_multiplayer_round_earnings_multiplier"),
         (val_div, ":attacker_money_add", 100),

         (try_for_range, ":player_no", 0, ":num_players"),
           (player_is_active, ":player_no"),
		   (player_slot_eq, ":player_no", slot_player_spawned_this_round, 1),
           (player_get_gold, ":player_gold", ":player_no"),
           (player_get_team_no, ":player_team", ":player_no"),           
           (val_add, ":player_gold", ":per_round_gold_addition"), #standard           
           (try_begin), 
             (eq, ":player_team", "$g_defender_team"),
             (val_add, ":player_gold", ":defender_money_add"),
           (else_try), 
             (val_add, ":player_gold", ":attacker_money_add"),
           (try_end),
         
           #(below lines added new at 25.11.09 after Armagan decided new money system)
           (try_begin),
             (player_get_slot, ":old_items_value", ":player_no", slot_player_last_rounds_used_item_earnings),
             (store_add, ":player_total_potential_gold", ":player_gold", ":old_items_value"),
             (store_mul, ":minimum_gold", "$g_multiplayer_initial_gold_multiplier", 10),
             (lt, ":player_total_potential_gold", ":minimum_gold"),
             (store_sub, ":additional_gold", ":minimum_gold", ":player_total_potential_gold"),
             (val_add, ":player_gold", ":additional_gold"),
           (try_end),
           #new money system addition end

           (player_set_gold, ":player_no", ":player_gold", multi_max_gold_that_can_be_stored),
         (try_end),

         (try_for_range, ":player_no", 0, ":num_players"),
           (player_is_active, ":player_no"),
           (player_set_slot, ":player_no", slot_player_spawned_this_round, 0),
         (try_end),

         #initialize my team at start of round (it will be assigned again at next round's first death)
         (assign, "$my_team_at_start_of_round", -1),

         #clear scene and end round
         (multiplayer_clear_scene),
         
         (get_max_players, ":num_players"),                               
         (try_for_range, ":player_no", 1, ":num_players"), #0 is server so starting from 1
           (player_is_active, ":player_no"),
           (player_set_slot, ":player_no", slot_player_damage_given_to_target_1, 0),
           (player_set_slot, ":player_no", slot_player_damage_given_to_target_2, 0),
         (try_end),
         
         #initialize moveable object positions
         (call_script, "script_multiplayer_initialize_belfry_wheel_rotations"),
         (call_script, "script_multiplayer_close_gate_if_it_is_open"),
         (call_script, "script_multiplayer_move_moveable_objects_initial_positions"),
                  
         (assign, "$g_round_ended", 0),

         (assign, "$g_multiplayer_num_bots_required_team_1", "$g_multiplayer_num_bots_team_1"), 
         (assign, "$g_multiplayer_num_bots_required_team_2", "$g_multiplayer_num_bots_team_2"), 

         (start_presentation, "prsnt_multiplayer_destructible_targets_display"),

         #initializing catapult & trebuchet positions and hit points for destroy mod.
         (call_script, "script_initialize_objects"),

         (store_mission_timer_a, "$g_round_start_time"),
         (call_script, "script_initialize_all_scene_prop_slots"),

         #initialize round start times for clients
         (get_max_players, ":num_players"),
         (try_for_range, ":player_no", 0, ":num_players"),
           (player_is_active, ":player_no"),
           (multiplayer_send_int_to_player, ":player_no", multiplayer_event_set_round_start_time, -9999), #this will also initialize moveable object slots.
         (try_end),         
       ]),

      (0, 0, 0, [], #if there is nobody in any teams do not reduce round time.
       [
         #(multiplayer_is_server),
         (assign, ":human_agents_spawned_at_team_1", "$g_multiplayer_num_bots_team_1"),
         (assign, ":human_agents_spawned_at_team_2", "$g_multiplayer_num_bots_team_2"),
         
         (get_max_players, ":num_players"),
         (try_for_range, ":player_no", 0, ":num_players"),
           (player_is_active, ":player_no"),
           (player_get_team_no, ":player_team", ":player_no"), 
           (try_begin),
             (eq, ":player_team", 0),
             (val_add, ":human_agents_spawned_at_team_1", 1),
           (else_try),
             (eq, ":player_team", 1),
             (val_add, ":human_agents_spawned_at_team_2", 1),
           (try_end),
         (try_end),

         (try_begin),
           (this_or_next|eq, ":human_agents_spawned_at_team_1", 0),
           (eq, ":human_agents_spawned_at_team_2", 0),

           (store_mission_timer_a, ":seconds_past_since_round_started"),
           (val_sub, ":seconds_past_since_round_started", "$g_round_start_time"),
           (le, ":seconds_past_since_round_started", 2),
                  
           (store_mission_timer_a, "$g_round_start_time"),
         (try_end),
       ]),    
           
      (1, 0, 0, [],
       [
         (multiplayer_is_server),
         (get_max_players, ":num_players"),
         (try_for_range, ":player_no", 0, ":num_players"),
           (player_is_active, ":player_no"),
           (neg|player_is_busy_with_menus, ":player_no"),
           (try_begin),
             (player_slot_eq, ":player_no", slot_player_spawned_this_round, 0),

             (player_get_team_no, ":player_team", ":player_no"), #if player is currently spectator do not spawn his agent
             (lt, ":player_team", multi_team_spectator),

             (player_get_troop_id, ":player_troop", ":player_no"), #if troop is not selected do not spawn his agent
             (ge, ":player_troop", 0),

             (assign, ":spawn_new", 0), 
             (assign, ":num_active_players_in_team_0", 0),
             (assign, ":num_active_players_in_team_1", 0),
             (try_begin),
               (assign, ":num_active_players", 0),
               (get_max_players, ":num_players"),
               (try_for_range, ":player_no_2", 0, ":num_players"),
                 (player_is_active, ":player_no_2"),
                 (val_add, ":num_active_players", 1),
                 (player_get_team_no, ":player_team_2", ":player_no_2"),
                 (try_begin),
                   (eq, ":player_team_2", 0),
                   (val_add, ":num_active_players_in_team_0", 1),
                 (else_try),
                   (eq, ":player_team_2", 1),
                   (val_add, ":num_active_players_in_team_1", 1),
                 (try_end),
               (try_end),

               (store_mul, ":multipication_of_num_active_players_in_teams", ":num_active_players_in_team_0", ":num_active_players_in_team_1"),

               (store_mission_timer_a, ":round_time"),
               (val_sub, ":round_time", "$g_round_start_time"),

               (this_or_next|lt, ":round_time", multiplayer_new_agents_finish_spawning_time),
               (this_or_next|le, ":num_active_players", 2),
               (eq, ":multipication_of_num_active_players_in_teams", 0),
         
               (eq, "$g_round_ended", 0),
               (assign, ":spawn_new", 1),
             (try_end),
             (eq, ":spawn_new", 1),
             (try_begin),
               (eq, ":player_team", 0),
               (assign, ":entry_no", multi_initial_spawn_point_team_1),
             (else_try),
               (eq, ":player_team", 1),
               (assign, ":entry_no", multi_initial_spawn_point_team_2),
             (try_end),
             (call_script, "script_multiplayer_buy_agent_equipment", ":player_no"),
             (player_spawn_new_agent, ":player_no", ":entry_no"),
             (player_set_slot, ":player_no", slot_player_spawned_this_round, 1),
           (else_try), #spawning as a bot (if option ($g_multiplayer_player_respawn_as_bot) is 1)
             (eq, "$g_multiplayer_player_respawn_as_bot", 1),
             (player_get_agent_id, ":player_agent", ":player_no"),
             (ge, ":player_agent", 0),
             (neg|agent_is_alive, ":player_agent"),
             (agent_get_time_elapsed_since_removed, ":elapsed_time", ":player_agent"),
             (gt, ":elapsed_time", "$g_multiplayer_respawn_period"),

             (player_get_team_no, ":player_team", ":player_no"),
             (assign, ":is_found", 0),
             (try_for_agents, ":cur_agent"),
               (eq, ":is_found", 0),
               (agent_is_alive, ":cur_agent"),
               (agent_is_human, ":cur_agent"),
               (agent_is_non_player, ":cur_agent"),
               (agent_get_team ,":cur_team", ":cur_agent"),
               (eq, ":cur_team", ":player_team"),
               (assign, ":is_found", 1),
             (try_end),

             (try_begin),
               (eq, ":is_found", 1),
               (call_script, "script_find_most_suitable_bot_to_control", ":player_no"),
               (player_control_agent, ":player_no", reg0),

               (player_get_slot, ":num_spawns", ":player_no", slot_player_spawned_this_round),
               (val_add, ":num_spawns", 1),
               (player_set_slot, ":player_no", slot_player_spawned_this_round, ":num_spawns"),
             (try_end),
           (try_end),
         (try_end),
         ]),

      multiplayer_server_spawn_bots, 
      multiplayer_server_manage_bots, 
      
      multiplayer_server_check_end_map,
        
      (ti_tab_pressed, 0, 0, [],
       [
         (try_begin),
           (eq, "$g_multiplayer_mission_end_screen", 0),
           (assign, "$g_multiplayer_stats_chart_opened_manually", 1),
           (start_presentation, "prsnt_multiplayer_stats_chart"),
         (try_end),
         ]),

      multiplayer_once_at_the_first_frame,

      (ti_battle_window_opened, 0, 0, [], [
        (start_presentation, "prsnt_multiplayer_round_time_counter"),
        (start_presentation, "prsnt_multiplayer_team_score_display"),
        ]),

      (ti_escape_pressed, 0, 0, [],
       [
         (neg|is_presentation_active, "prsnt_multiplayer_escape_menu"),
         (neg|is_presentation_active, "prsnt_multiplayer_stats_chart"),
         (eq, "$g_waiting_for_confirmation_to_terminate", 0),
         (start_presentation, "prsnt_multiplayer_escape_menu"),
         ]),
      ],
  ),
#INVASION MODE START
    ###############################################
  ####################################  WAVE MODE
  ###############################################
  
  
	( 	"multiplayer_ccoop",mtf_battle_mode,-1, #captain_coop mode, aka "Invasion"
		"You lead your men to battle.",
    [
		  (0,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
		  (1,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
		  (2,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
		  (3,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
		  (4,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
		  (5,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
		  (6,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
		  (7,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
          
		  (8,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
		  (9,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
		  (10,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
		  (11,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
		  (12,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
		  (13,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
		  (14,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
		  (15,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
          
		  (16,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
		  (17,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
		  (18,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
		  (19,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
		  (20,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
		  (21,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
		  (22,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
		  (23,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
          
		  (24,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
		  (25,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
		  (26,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
		  (27,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
		  (28,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
		  (29,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
		  (30,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
		  (31,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
          
		  (32,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
		  (33,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
		  (34,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
		  (35,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
		  (36,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
		  (37,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
		  (38,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
		  (39,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
          
		  (40,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
		  (41,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
		  (42,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
		  (43,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
		  (44,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
		  (45,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
		  (46,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
		  (47,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
          
		  (48,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
		  (49,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
		  (50,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
		  (51,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
		  (52,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
		  (53,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
		  (54,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
		  (55,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
          
		  (56,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
		  (57,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
		  (58,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
		  (59,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
		  (60,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
		  (61,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
		  (62,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
		  (63,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
		  
		  
		  (64,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
		  (65,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
		  (66,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
		  (67,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
		  (68,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
		  (69,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
		  
		  # prison cart entry points
		  (70,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
		  (71,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
		  (72,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
		  (73,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
		  (74,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),	
          
		  # empty slots
		  (75,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
		  (76,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
		  (77,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
		  (78,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
		  (79,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
		  
		  # enemy wave spawn points
		  (80,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
		  (81,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
		  (82,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
		  (83,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
		  (84,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),	
		  (85,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
		  (86,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
		  (87,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),	
	],
	
    [      
		common_battle_init_banner,

		multiplayer_server_check_polls,

		(ti_on_agent_spawn, 0, 0, [],
		[
			(store_trigger_param_1, ":agent_no"),
			(call_script, "script_multiplayer_server_on_agent_spawn_common", ":agent_no"),
			##check team and multipliers to enemies after certain wave
			(agent_get_team, ":agent_team_no", ":agent_no"),
            #(try_begin),
            #  (eq, "$g_mp_coop_last_king_wave", "$g_multiplayer_ccoop_wave_no"),
            #  (store_sub, ":elite_checker", "$g_mp_coop_king_waves", 1),
            #(else_try),
            #  (assign, ":elite_checker", "$g_mp_coop_king_waves"),
            #(try_end),
			(try_begin),
                (multiplayer_is_server),
			#	(eq, ":agent_team_no", 1), # enemies
			#	(agent_set_max_hit_points, ":agent_no", 1),
			#	(agent_set_damage_modifier, ":agent_no", 1),
            #
            #(else_try),
				(eq, ":agent_team_no", 1), # enemies
                (try_begin),
                  (eq, "$g_multiplayer_ccoop_difficulty", 0),
                  (assign, ":hp_boost", 50),
                  (assign, ":dmg_boost", 50),
				  (agent_set_max_hit_points, ":agent_no", ":hp_boost"),
				  (agent_set_damage_modifier, ":agent_no", ":dmg_boost"),
                (else_try),
				  (ge, "$g_mp_coop_king_waves", 1), # wave++
				  #(neq, "$g_mp_coop_last_king_wave", "$g_multiplayer_ccoop_wave_no"), # wave++
                  (store_mul, ":hp_boost", "$g_mp_coop_king_waves", 35),
                  (val_add, ":hp_boost", 100),
                  (store_mul, ":dmg_boost", "$g_mp_coop_king_waves", 25),
                  (val_add, ":dmg_boost", 100),
				  (agent_set_max_hit_points, ":agent_no", ":hp_boost"),
				  (agent_set_damage_modifier, ":agent_no", ":dmg_boost"),
				  #(agent_set_max_hit_points, ":agent_no", 10),
				  #(agent_set_damage_modifier, ":agent_no", 10),
                (try_end),
			#(else_try),
			#	(eq, ":agent_team_no", 1), # enemies
			#	(gt, "$g_multiplayer_ccoop_wave_no", 10), # wave+
			#	(agent_set_max_hit_points, ":agent_no", 175),
			#	(agent_set_damage_modifier, ":agent_no", 150),
			(try_end),
            
            (try_begin),
              (multiplayer_is_server),
              (eq, ":agent_team_no", 0),
              (agent_is_active, ":agent_no"),
              (agent_is_alive, ":agent_no"),
              (agent_is_non_player, ":agent_no"),
              (agent_get_group, ":agent_group", ":agent_no"),
              (player_is_active, ":agent_group"),
              (agent_get_troop_id, ":troop_no", ":agent_no"),
              (try_begin),
                (troop_get_slot, ":horse_no", ":troop_no", slot_troop_coop_lord_spawned),
                (gt, ":horse_no", 0),
                (troop_add_item, ":troop_no", ":horse_no"),
              (try_end),
              (call_script, "script_cf_multiplayer_upgrade_companion_equipment", ":agent_no"),
              (troop_get_type, ":is_female", ":troop_no"),
              (try_begin),
                (eq, ":is_female", 0),
                (store_add, ":random_max", ccoop_companion_sounds_end, 20),
                (store_random_in_range, ":sound_id", ccoop_companion_sounds_start, ":random_max"),
                (lt, ":sound_id", ccoop_companion_sounds_end),
                (agent_get_position, pos60, ":agent_no"),
                (call_script, "script_multiplayer_server_play_sound_at_position", ":sound_id"),
              (try_end),
            (try_end),

            
            (try_begin),
              (multiplayer_is_server),
              (eq, ":agent_team_no", 0),
              (agent_is_active, ":agent_no"),
              (agent_is_alive, ":agent_no"),
              (agent_is_human, ":agent_no"),
              (neg|agent_is_non_player, ":agent_no"),
              (agent_get_player_id, ":player_no", ":agent_no"),
              #(player_get_slot, ":player_spawn_status", ":player_no", slot_player_companion_ids_locked),
              (player_set_slot, ":player_no", slot_player_companion_ids_locked, 1),
              (multiplayer_send_2_int_to_player, ":player_no", multiplayer_event_other_events, multiplayer_event_other_event_ccoop_lock_companions, 1),
                
            (try_end),

		]),

		(ti_server_player_joined, 0, 0, [],
		[
			(store_trigger_param_1, ":player_no"),
			(call_script, "script_multiplayer_server_player_joined_common", ":player_no"),
			
			# player has to wait for next round to respawn (make it -1 instead of 0 to prevent the player from spawning from prison cart this round)
			(player_set_slot, ":player_no", slot_player_first_spawn, -1),
            #(player_get_slot, ":player_spawn_status", ":player_no", slot_player_first_spawn),
            (player_set_slot, ":player_no", slot_player_companion_ids_locked, 0),
            (multiplayer_send_2_int_to_player, ":player_no", multiplayer_event_other_events, multiplayer_event_other_event_ccoop_lock_companions, 0),

			# clear squad info
			#(call_script, "script_mp_clear_squad_info", ":player_no"),
			
			(call_script, "script_multiplayer_ccoop_send_troop_data_to_client", ":player_no"),
			
			(try_begin),
				(gt, "$g_multiplayer_ccoop_game_started", 0),
				
				(try_begin),
					(le, "$g_multiplayer_ccoop_enemy_respawn_secs", 45), # if 45 secs left to respawn
					(multiplayer_send_3_int_to_player, ":player_no", multiplayer_event_other_events, multiplayer_event_other_event_ccoop_count_down_visible, "$g_multiplayer_ccoop_enemy_respawn_secs", "$g_multiplayer_ccoop_wave_no"),
				(else_try),
					(multiplayer_send_3_int_to_player, ":player_no", multiplayer_event_other_events, multiplayer_event_other_event_ccoop_count_down_invisible, "$g_multiplayer_ccoop_enemy_respawn_secs", "$g_multiplayer_ccoop_wave_no"),
				(try_end),
			(try_end),			
            
            #Frank
            (try_begin),
              (multiplayer_is_server),
              #Frank
              #Reset levels for player companions
              (try_for_range, ":cur_slot", slot_player_companion_levels_begin, slot_player_companion_levels_end),
                (player_set_slot, ":player_no", ":cur_slot", 0),
              (try_end),
              
              #Reset chest opened data
              (try_for_range, ":cur_slot", slot_player_coop_opened_chests_begin, slot_player_coop_opened_chests_end),
                (player_set_slot, ":player_no", ":cur_slot", 0),
              (try_end),
            (try_end),
		]),

		(ti_before_mission_start, 0, 0, [],
		[
			(assign, "$g_multiplayer_game_type", multiplayer_game_type_captain_coop),	
            
            
            (store_current_scene, ":cur_scene"),
            (scene_get_slot, "$g_ccoop_disallow_horses", ":cur_scene", slot_scene_ccoop_disallow_horses),
            (try_begin),
              (eq, "$g_ccoop_disallow_horses", 1),
              (try_for_range, ":cur_entry", 0, 100),
                (mission_tpl_entry_set_override_flags, "mt_multiplayer_ccoop", ":cur_entry", af_override_horse),
              (try_end),
            (else_try),
              (try_for_range, ":cur_entry", 0, 100),
                (mission_tpl_entry_set_override_flags, "mt_multiplayer_ccoop", ":cur_entry", 0),
              (try_end),
            (try_end),
            
			(call_script, "script_multiplayer_server_before_mission_start_common"),

			(call_script, "script_multiplayer_init_mission_variables"),
			(call_script, "script_multiplayer_remove_destroy_mod_targets"),
			(call_script, "script_multiplayer_remove_headquarters_flags"),
		]),

		(ti_after_mission_start, 0, 0, [], 
		[
			(set_spawn_effector_scene_prop_kind, 0, -1), #during this mission, agents of "team 0" will try to spawn around scene props with kind equal to -1(no effector for this mod)
			(set_spawn_effector_scene_prop_kind, 1, -1), #during this mission, agents of "team 1" will try to spawn around scene props with kind equal to -1(no effector for this mod)

			(call_script, "script_initialize_all_scene_prop_slots"),         
			(call_script, "script_multiplayer_move_moveable_objects_initial_positions"),
			
            (store_random_in_range, "$g_presentation_obj_coop_companion_0", multiplayer_coop_companion_equipment_sets_begin, multiplayer_coop_companion_first_equipment_sets_end),
            (store_random_in_range, "$g_presentation_obj_coop_companion_1", multiplayer_coop_companion_equipment_sets_begin, multiplayer_coop_companion_first_equipment_sets_end),
            (try_begin),
              (eq, "$g_presentation_obj_coop_companion_1", "$g_presentation_obj_coop_companion_0"),
              (val_add, "$g_presentation_obj_coop_companion_1", 1),
            (try_end),
            (try_begin),
              (ge, "$g_presentation_obj_coop_companion_1", multiplayer_coop_companion_first_equipment_sets_end),
              (assign, "$g_presentation_obj_coop_companion_1", multiplayer_coop_companion_equipment_sets_begin),
            (try_end),
            
            (store_sub, ":value", "$g_presentation_obj_coop_companion_0", multiplayer_coop_companion_equipment_sets_begin),
            (val_add, ":value", multiplayer_coop_companion_equipment_sets_begin),
            #(val_add, ":value", 1),
            (assign, "$g_presentation_obj_coop_companion_class_0", ":value"),
            
            (store_sub, ":value", "$g_presentation_obj_coop_companion_1", multiplayer_coop_companion_equipment_sets_begin),
            (val_add, ":value", multiplayer_coop_companion_equipment_sets_begin),
            #(val_add, ":value", 1),
            (assign, "$g_presentation_obj_coop_companion_class_1", ":value"),
            
            (try_for_range, ":cur_troop", lords_begin, lords_end),
              (troop_set_slot, ":cur_troop", slot_troop_coop_lord_spawned, 0),
            (try_end),

            (try_for_range, ":cur_troop", quick_battle_troops_begin, quick_battle_troops_end),
              (troop_set_slot, ":cur_troop", slot_troop_coop_lord_spawned, 0),
            (try_end),

            (assign, "$g_mp_coop_lord_waves", 0),
            (assign, "$g_mp_coop_king_waves", 0),
            (assign, "$g_mp_coop_last_king_wave", 0),

            
            #Frank
            (try_begin),
              (multiplayer_is_server),
			  (get_max_players, ":max_players"),
			  (try_for_range, ":cur_player", 0, ":max_players"),
			  	(player_is_active, ":cur_player"),
                  #Frank
                  #Reset levels for player companions
                  (try_for_range, ":cur_slot", slot_player_companion_levels_begin, slot_player_companion_levels_end),
                    (player_set_slot, ":cur_player", ":cur_slot", 0),
                    (multiplayer_send_3_int_to_player, ":cur_player", multiplayer_event_other_events, multiplayer_event_other_events_change_companion_level, ":cur_slot", 0),
                  (try_end),
                  
                  #Reset chest opened data
                  (try_for_range, ":cur_slot", slot_player_coop_opened_chests_begin, slot_player_coop_opened_chests_end),
                    (player_set_slot, ":cur_player", ":cur_slot", 0),
                  (try_end),
		      (try_end),
            (try_end),
            

            
			(try_begin),
				(multiplayer_is_server),

				#(assign, "$g_multiplayer_ccoop_enemy_respawn_secs", multi_captain_coop_round_duration_in_sec), #count down time: 10mins
				(assign, "$g_multiplayer_ccoop_spawn_prison_cart_counter", 0),
				(assign, "$g_multiplayer_ccoop_spawn_player_and_squad_counter", 0),
				(assign, "$g_multiplayer_ccoop_spawn_alive_player_squad_and_minus_one_first_spawn_slots_and_minus_one_first_spawn_slots", -1),
                
			(try_end),
			
			(assign, "$g_multiplayer_ccoop_wave_no", 0),
			(assign, "$g_multiplayer_ccoop_game_started", 0),
			(assign, "$g_multiplayer_ccoop_enable_count_down", 0),
			(assign, "$g_multiplayer_ccoop_change_map", 0),
			(assign, "$g_round_ended", 0),

			# destroy prison cart (since it is invisible when mission starts)
			(call_script, "script_multiplayer_ccoop_destroy_prison_cart"),
            
            (get_max_players, ":max_players"),
            (try_for_range, ":cur_player", 0, ":max_players"),
                (player_is_active, ":cur_player"),
                (player_set_slot, ":cur_player", slot_player_companion_ids_locked, 0),
                (multiplayer_send_2_int_to_player, ":cur_player", multiplayer_event_other_events, multiplayer_event_other_event_ccoop_lock_companions, 0),
			(try_end),
                
           
		]),

		(ti_on_multiplayer_mission_end, 0, 0, [],
		[
			# disable count down
			(assign, "$g_multiplayer_ccoop_enable_count_down", 0),
			(assign, "$g_multiplayer_ccoop_enemy_respawn_secs", 100000),
			(assign, "$g_multiplayer_ccoop_game_started", 0),
			
			
			(assign, "$g_multiplayer_stats_chart_opened_manually", 0),
			(start_presentation, "prsnt_multiplayer_stats_chart_deathmatch"),			
		]),
		
		(ti_on_player_exit, 0, 0, [],
		[
			# force kill all squad agents of the exiting player
			(store_trigger_param_1, ":exiting_player_no"),
			(call_script, "script_cf_multiplayer_event_team_change", ":exiting_player_no"),
		]),

		(ti_on_agent_killed_or_wounded, 0, 0, [],
		[
			(store_trigger_param_1, ":dead_agent_no"), 
			(store_trigger_param_2, ":killer_agent_no"), 
            
            
			(call_script, "script_multiplayer_server_on_agent_killed_or_wounded_common", ":dead_agent_no", ":killer_agent_no"),
			
			(agent_get_team, ":dead_agent_team", ":dead_agent_no"),			
            
            #Frank 
            #level down dead companions                    
            (try_begin),
              (multiplayer_is_server),
              (agent_is_non_player, ":dead_agent_no"),
              (agent_get_group, ":dead_agent_group", ":dead_agent_no"),
              (player_is_active, ":dead_agent_group"),
              (agent_get_troop_id, ":dead_agent_troop", ":dead_agent_no"),
              
              (try_for_range, ":cur_slot", slot_player_companion_ids_begin, slot_player_companion_ids_end),
                (player_get_slot, ":companion_no", ":dead_agent_group", ":cur_slot"),
                (eq, ":dead_agent_troop", ":companion_no"),
                (val_sub, ":cur_slot", slot_player_companion_ids_begin),
                (val_add, ":cur_slot", slot_player_companion_levels_begin),
                (player_get_slot, ":companion_level", ":dead_agent_group", ":cur_slot"),
                (val_sub, ":companion_level", 1),
                (val_max, ":companion_level", 0),
                (player_set_slot, ":dead_agent_group", ":cur_slot", ":companion_level"),
                (multiplayer_send_3_int_to_player, ":dead_agent_group", multiplayer_event_other_events, multiplayer_event_other_events_change_companion_level, ":cur_slot", ":companion_level"),
                #(call_script, "script_multiplayer_upgrade_companion_equipment", ":cur_agent"),
              (try_end),
            (try_end),
            
            (agent_get_troop_id, ":dead_agent_troop_no", ":dead_agent_no"),       
            (try_begin),
              (neq, ":dead_agent_troop_no", -1),
              (eq, ":dead_agent_troop_no", "$g_ccoop_king_troop"),
              (assign, "$g_mp_coop_last_king_wave", "$g_multiplayer_ccoop_wave_no"),
              (val_add, "$g_mp_coop_king_waves", 1),
            (try_end),
            
            (try_begin),
              (multiplayer_is_server),
              
              (try_begin),
                (try_begin),
                  (eq, ":dead_agent_team", 1),
                  (store_random_in_range, ":random", 0, 15),
                (else_try),
                  (assign, ":random", 0),
                (try_end),
                (this_or_next|eq, ":random", 14),
                (this_or_next|is_between, ":dead_agent_troop_no", lords_begin, lords_end),
                (this_or_next|is_between, ":dead_agent_troop_no", kings_begin, kings_end),
                (is_between, ":dead_agent_troop_no", quick_battle_troops_begin, quick_battle_troops_end),
                (agent_get_position, pos0, ":dead_agent_no"),
                #(position_move_z, pos0, -15),
                (set_spawn_position, pos0),
                (spawn_scene_prop, "spr_multiplayer_coop_item_drop"),
                #(display_message, "@{reg0}"),
                
                (scene_prop_get_instance, ":prison_cart_instance", "spr_prison_cart", 0),
                
                (assign, ":overwrite", 1),
                (try_for_range, ":cur_slot", scene_prop_ccoop_item_drop_start, scene_prop_ccoop_item_drop_end),
                  (eq, ":overwrite", 1),
                  (scene_prop_get_slot, ":cur_instance", ":prison_cart_instance", ":cur_slot"),
                  (eq, ":cur_instance", 0),
                  (scene_prop_set_slot, ":prison_cart_instance", ":cur_slot", reg0),
                  (assign, ":overwrite", 0),
                (try_end),
                (try_begin),
                  (eq, ":overwrite", 1),
                  (scene_prop_get_slot, ":culled_instance", ":prison_cart_instance", scene_prop_ccoop_item_drop_start),
                  (prop_instance_get_position, pos1, ":culled_instance"),
                  (position_move_z, pos1, -2000), 
                  (prop_instance_set_position, ":culled_instance", pos1),
                  (try_for_range, ":cur_slot", scene_prop_ccoop_item_drop_start, scene_prop_ccoop_item_drop_end),
                    (store_add, ":cur_slot_plus_one", ":cur_slot", 1),
                    (try_begin),
                      (eq, ":cur_slot_plus_one", scene_prop_ccoop_item_drop_end),
                      (assign, ":overwriting_instance", reg0),
                    (else_try),
                      (scene_prop_get_slot, ":overwriting_instance", ":prison_cart_instance", ":cur_slot_plus_one"),
                    (try_end),
                    (scene_prop_set_slot, ":prison_cart_instance", ":cur_slot", ":overwriting_instance"),
                  (try_end),
                  (get_max_players, ":max_players"),
                  (try_for_range, ":cur_player", 0, ":max_players"),
                    (player_is_active, ":cur_player"),
                    (try_for_range, ":cur_slot", slot_player_coop_opened_chests_begin, slot_player_coop_opened_chests_end),
                      (player_slot_eq, ":cur_player", ":cur_slot", ":culled_instance"),
                      (player_set_slot, ":cur_player", ":cur_slot", 0),
                      (multiplayer_send_2_int_to_player, ":cur_player", multiplayer_event_coop_chest_opened, ":cur_slot", 0),
                    (try_end),
                  (try_end),
                (try_end),
                  
                #(prop_instance_set_position, reg0, pos0),
              (try_end),
            (try_end),
			
			#add 1 score points to killer agent's team.
			(try_begin),
				(ge, ":killer_agent_no", 0),
				(agent_is_human, ":dead_agent_no"),
				(agent_is_human, ":killer_agent_no"),
				(agent_get_team, ":killer_agent_team", ":killer_agent_no"),
				(le, ":killer_agent_team", 1), #0 or 1 is ok
				(team_get_score, ":team_score", ":killer_agent_team"),
				(neq, ":killer_agent_team", ":dead_agent_team"),
				(val_add, ":team_score", 1),
				(team_set_score, ":killer_agent_team", ":team_score"),
			(try_end),
			 
			# if dead agent is in wave team
			(try_begin),
				(multiplayer_is_server),				
				(eq, ":dead_agent_team", 1),  # enemy (wave) side
				
				#(call_script, "script_multiplayer_ccoop_check_reinforcement"),
				
                
                
                (assign, ":has_agents", 0),
                (try_for_agents, ":cur_agent"),
                    (try_begin),
                        (agent_is_human, ":cur_agent"),
                        (agent_is_alive, ":cur_agent"),
                        (agent_get_team, ":cur_agent_team", ":cur_agent"),
                        (eq, ":cur_agent_team", 1),
                        (val_add, ":has_agents", 1),
                    (try_end),
                    (gt, ":has_agents", 0), # break
                (try_end),				
                
                (eq, ":has_agents", 0), # if all enemies are dead
				
                (try_begin),
                    (agent_is_human, ":dead_agent_no"),
                    (play_sound, "snd_team_scored_a_point"), # play victory sound
                (try_end),				
			    
                
                (try_begin),
                    (neq, "$g_multiplayer_ccoop_difficulty", 2),
                    (eq, "$g_multiplayer_ccoop_wave_no", "$g_mp_coop_last_king_wave"),
                    (assign, "$g_multiplayer_ccoop_change_map", 10),
                    (set_cheer_at_no_enemy, 1),
                    (get_max_players, ":max_players"),
                    (team_get_faction, ":wave_faction", 1),
                    (str_store_faction_name, s0, ":wave_faction"),
                    (store_add, ":difficulty_string_i", "str_ccoop_easy", "$g_multiplayer_ccoop_difficulty"),
                    (str_store_string, s1, ":difficulty_string_i"),
                    (try_begin),
                      (is_between, ":wave_faction", kingdoms_begin, kingdoms_end),
                      (assign, reg1, 0),
                    (else_try),
                      (assign, reg1, 1),
                    (try_end),
                    
                    (str_store_string, s2, "str_ccoop_s0_enemy_defeated_s1"),
                    
                    (try_for_range, ":cur_player", 0, ":max_players"),
                      (player_is_active, ":cur_player"),
                      (multiplayer_send_int_to_player, ":cur_player", multiplayer_event_ccoop_victory_message, ":difficulty_string_i"),
                    (try_end),
                (else_try),
				
                    # round cleared
                    (assign, "$g_multiplayer_ccoop_enemy_respawn_secs", 32), # set 32 secs left for next wave
                    
                    # refill everyone's health (for refilling players' and squad members' health)
                    (try_for_agents, ":cur_agent"),
                        (agent_is_alive, ":cur_agent"),
                        (agent_is_human, ":cur_agent"),
                        
                        # refill agent heath and ammo
                        (agent_set_hit_points, ":cur_agent", 100),
                        (agent_refill_wielded_shield_hit_points, ":cur_agent"),
                        (agent_refill_ammo, ":cur_agent"),
                        
                        #Frank 
                        #level up living companions                    
                        (try_begin),
                          (agent_is_non_player, ":cur_agent"),
                          (agent_get_group, ":cur_agent_group", ":cur_agent"),
                          (gt, ":cur_agent_group", -1),
                          (player_is_active, ":cur_agent_group"),
                          (agent_get_troop_id, ":cur_troop", ":cur_agent"),
                          
                          (try_for_range, ":cur_slot", slot_player_companion_ids_begin, slot_player_companion_ids_end),
                              (player_get_slot, ":companion_no", ":cur_agent_group", ":cur_slot"),
                              (eq, ":cur_troop", ":companion_no"),
                              (val_sub, ":cur_slot", slot_player_companion_ids_begin),
                              (val_add, ":cur_slot", slot_player_companion_levels_begin),
                              (player_get_slot, ":companion_level", ":cur_agent_group", ":cur_slot"),
                              (val_add, ":companion_level", 1),
                              (val_min, ":companion_level", 3),
                              (player_set_slot, ":cur_agent_group", ":cur_slot", ":companion_level"),
                              #(assign, reg0, ":cur_agent_group"),
                              #(assign, reg1, ":cur_slot"),
                              #(assign, reg2, ":companion_level"),
                              #(display_message, "@levelling up companion of player: {reg0}  slot: {reg1}  level: {reg2}"),
                              (multiplayer_send_3_int_to_player, ":cur_agent_group", multiplayer_event_other_events, multiplayer_event_other_events_change_companion_level, ":cur_slot", ":companion_level"),
                              (call_script, "script_cf_multiplayer_upgrade_companion_equipment", ":cur_agent"),
                          (try_end),
                        (try_end),
                        
                        
                        
                        (try_begin),
                            # if agent has a horse
                            (agent_get_horse, ":horse_agent", ":cur_agent"), 
                            (gt, ":horse_agent", -1), 
                            (agent_is_alive, ":horse_agent"),
                            # refill horse health
                            (agent_set_hit_points, ":horse_agent", 100),
                        #(else_try),
                            # if player's horse is dead, we cannot respawn the horse due to restrictions in the engine
                        (try_end),
                        
                        
                        
                    (try_end),
                    (try_begin),
                        (eq, "$g_multiplayer_ccoop_difficulty", 2),
                        (eq, "$g_multiplayer_ccoop_wave_no", "$g_mp_coop_last_king_wave"),
                        (val_add, "$g_multiplayer_ccoop_enemy_respawn_secs", 10),
                        (get_max_players, ":max_players"),
                        (team_get_faction, ":wave_faction", 1),
                        (str_store_faction_name, s0, ":wave_faction"),
                        (assign, reg0, "$g_mp_coop_king_waves"),
                        (try_begin),
                          (is_between, ":wave_faction", kingdoms_begin, kingdoms_end),
                          (assign, reg1, 0),
                        (else_try),
                          (assign, reg1, 1),
                        (try_end),
                        (str_store_string, s2, "str_ccoop_s0_enemy_defeated_endless_reg0"),
                        
                        (try_for_range, ":cur_player", 0, ":max_players"),
                          (player_is_active, ":cur_player"),
                          (multiplayer_send_string_to_player, ":cur_player", multiplayer_event_ccoop_victory_message, -1),
                        (try_end),
                    (try_end),
                (try_end),
				
			(else_try),				
				(multiplayer_is_server),
				(eq, ":dead_agent_team", 0),  # players side
				
				#(display_debug_message, "@{!}dead agent is on our team!"),
				
				(assign, ":has_agents", 0),
				(try_for_agents, ":cur_agent"),
					(try_begin),
						(agent_is_human, ":cur_agent"),
						(agent_is_alive, ":cur_agent"),
						(agent_get_team, ":cur_agent_team", ":cur_agent"),
						(eq, ":cur_agent_team", 0),
						(val_add, ":has_agents", 1),						
					(try_end),
					(gt, ":has_agents", 0), #break
				(try_end),
				
				(eq, ":has_agents", 0),  # no player and bots left alive		

				
				(assign, "$g_multiplayer_ccoop_change_map", 5), #5 secs
                (set_cheer_at_no_enemy, 1),
				
			(else_try),	
				(neg|multiplayer_is_server), # client side
				
				(eq, ":dead_agent_team", 1),
                (agent_is_human, ":dead_agent_no"),
                
				(assign, ":has_agents", 0),
				(try_for_agents, ":cur_agent"),
					(try_begin),
						(agent_is_human, ":cur_agent"),
						(agent_is_alive, ":cur_agent"),
						(agent_get_team, ":cur_agent_team", ":cur_agent"),
						(eq, ":cur_agent_team", 1),
						(val_add, ":has_agents", 1),
					(try_end),
					(gt, ":has_agents", 0), # break
				(try_end),				
				
				(eq, ":has_agents", 0), # if all enemies are dead
				
                (play_sound, "snd_team_scored_a_point"), # play victory sound
				
			(try_end),
		]),
		 
		# one time execute
		(0, 0, ti_once, [],
		[
			(set_cheer_at_no_enemy, 0), # no cheer after all enemies are dead
		]),

		# if count down is enabled
		(1, 0, 0, [(gt, "$g_multiplayer_ccoop_enable_count_down", 0)],
		[
			(try_begin),
				(gt, "$g_multiplayer_ccoop_change_map", 0),
				
				(try_begin),
					(eq, "$g_multiplayer_ccoop_change_map", 4),
					(call_script, "script_multiplayer_ccoop_destroy_prison_cart"),
				(try_end),
				
				(val_sub, "$g_multiplayer_ccoop_change_map", 1),
				(eq, "$g_multiplayer_ccoop_change_map", 0),				
				(assign, "$g_multiplayer_ccoop_enable_count_down", 0),
				(assign, "$g_round_ended", 1),
                
                # #Frank
				#(get_max_players, ":max_players"),
				#(try_for_range, ":cur_player", 0, ":max_players"),
				#	(player_is_active, ":cur_player"),
                #    #Frank
                #    #Reset levels for player companions
                #    (try_for_range, ":cur_slot", slot_player_companion_levels_begin, slot_player_companion_levels_end),
                #      (assign, reg0, ":cur_slot"),
                #      (display_message, "@cleaning slot {reg0}"),
                #      (player_set_slot, ":cur_player", ":cur_slot", 0),
                #    (try_end),
                #    
                #    #Reset chest opened data
                #    (try_for_range, ":cur_slot", slot_player_coop_opened_chests_begin, slot_player_coop_opened_chests_end),
                #      (player_set_slot, ":cur_player", ":cur_slot", 0),
                #    (try_end),
			    #(try_end),
                
			(else_try),
				(gt, "$g_multiplayer_ccoop_enemy_respawn_secs", 0),
				(val_sub, "$g_multiplayer_ccoop_enemy_respawn_secs", 1),

				(try_begin),
					(gt, "$g_multiplayer_ccoop_enemy_respawn_secs", 59),
					(store_mod, ":mod", "$g_multiplayer_ccoop_enemy_respawn_secs", 60),
					(eq, ":mod", 0),
					(store_div, reg0, "$g_multiplayer_ccoop_enemy_respawn_secs", 60),
					(neg|multiplayer_is_dedicated_server),
					(display_message, "str_next_wave_in_reg0_mins", 0xFFDE6300),
				(try_end),
				
				(try_begin),
					(eq, "$g_multiplayer_ccoop_enemy_respawn_secs", 30), #if 30secs left to next wave
					(multiplayer_is_server),

					# give round bonus gold at the start of each wave (whether the previous wave is cleared or it is timed out)
					(call_script, "script_multiplayer_ccoop_give_round_bonus_gold"),
					
					(val_add, "$g_multiplayer_ccoop_wave_no", 1), # increment wave no

					#(try_begin),
					#	(eq, "$g_multiplayer_ccoop_wave_no", 31),
					#	# game end win condition
					#	# initiate round end/change map duration
					#	(assign, "$g_multiplayer_ccoop_change_map", 5), #5 secs
                    #    (set_cheer_at_no_enemy, 1),
					#(try_end),
					
					# destroy prison cart (since current wave is timed out and next wave is coming in 30 seconds) or
					# destroy prison cart (since round is cleared and everyone will respawn automatically)
					(call_script, "script_multiplayer_ccoop_destroy_prison_cart"),
					
					# respawn all dead players (with some delay)
					(call_script, "script_multiplayer_ccoop_start_player_and_squad_respawn_period", 1),
										
					# sync clients count down counter
					(get_max_players, ":max_players"),
					(store_sub, ":respawn_secs", "$g_multiplayer_ccoop_enemy_respawn_secs", 1), # send to clients as 1 sec decreased					
					(try_for_range, ":cur_player", 1, ":max_players"),						
						(player_is_active, ":cur_player"),
						(multiplayer_send_3_int_to_player, ":cur_player", multiplayer_event_other_events, multiplayer_event_other_event_ccoop_count_down_visible, ":respawn_secs", "$g_multiplayer_ccoop_wave_no"),
					(try_end),
					
					(call_script, "script_multiplayer_ccoop_prepare_spawn_wave"),
					
					(store_mission_timer_a, "$g_multiplayer_ccoop_next_wave_start_time"),
					(val_add, "$g_multiplayer_ccoop_next_wave_start_time", "$g_multiplayer_ccoop_enemy_respawn_secs"),
					(start_presentation, "prsnt_multiplayer_ccoop_next_wave_time_counter"),
					(start_presentation, "prsnt_multiplayer_flag_projection_display_ccoop_wave"),
				(else_try),
					(lt, "$g_multiplayer_ccoop_enemy_respawn_secs", 1),
					(multiplayer_is_server),
					
					# generate count down
					(call_script, "script_multiplayer_ccoop_calculate_round_duration"),
					
					# spawn wave
					(call_script, "script_multiplayer_ccoop_spawn_wave", 1000),
				(try_end),
				
			(try_end),
		]),
				
		# prison cart and player&bot spawn management
		(1, 0, 0, [(multiplayer_is_server),],		
		[
			(get_max_players, ":max_players"),
			
			# prison cart management
			(try_begin),
				# if move underground is initiated
				(gt, "$g_multiplayer_ccoop_move_prison_cart", 0),  
					
				(store_mission_timer_a, ":current_time"),
				(store_sub, ":time_left", "$g_multiplayer_ccoop_move_prison_cart", ":current_time"),
				
				(try_begin),
					(le, ":time_left", 0),
					
					(display_debug_message, "@{!}sending prisoner cart 6 feet underground!"),
					
					(set_fixed_point_multiplier, 100), 
					
					(scene_prop_get_instance, ":prison_cart", "spr_prison_cart", 0),
					(scene_prop_get_instance, ":prison_cart_door_left", "spr_prison_cart_door_left", 0),
					(scene_prop_get_instance, ":prison_cart_door_right", "spr_prison_cart_door_right", 0),
					
					(prop_instance_get_position, pos1, ":prison_cart"),
					(position_set_z, pos1, -4000), #40m down
					(prop_instance_set_position, ":prison_cart", pos1),	
					(prop_instance_set_position, ":prison_cart_door_left", pos1),
					(prop_instance_set_position, ":prison_cart_door_right", pos1),
					
					(assign, "$g_multiplayer_ccoop_move_prison_cart", 0),
				(try_end),
			
			(else_try),
				(gt, "$g_prison_cart_point", 0), # if visible				
				
				(scene_prop_get_instance, ":prison_cart_door_left", "spr_prison_cart_door_left", 0),
				(scene_prop_get_hit_points, ":left_door", ":prison_cart_door_left"),
				
				(scene_prop_get_instance, ":prison_cart_door_right", "spr_prison_cart_door_right", 0),
				(scene_prop_get_hit_points, ":right_door", ":prison_cart_door_right"),
					
				(try_begin),
					(this_or_next|lt, ":left_door", 1),  # left door's broken
					(lt, ":right_door", 1),  # right door's broken
										
					# destroy prison cart (since doors are cracked)
					(call_script, "script_multiplayer_ccoop_destroy_prison_cart"),
					
					# respawn all dead players (with some delay)
					(call_script, "script_multiplayer_ccoop_start_player_and_squad_respawn_period", 0),
					
				(try_end),
				
				# check if prison cart is spawned and there is no dead player (may occur if dead players quit the game or change their faction to spectator)
				(assign, ":is_anyone_dead", 0),
				(try_for_range, ":cur_player", 0, ":max_players"),
					(eq, ":is_anyone_dead", 0),
					(player_is_active, ":cur_player"),
					(player_get_team_no, ":player_team", ":cur_player"),
					(eq, ":player_team", 0),
					(player_get_agent_id, ":player_agent", ":cur_player"),
					(try_begin),
						(ge, ":player_agent", 0),
						(try_begin),
							(neg|agent_is_alive, ":player_agent"),
							(assign, ":is_anyone_dead", 1),
						(try_end),
					(else_try),
						(assign, ":is_anyone_dead", 1),
					(end_try),
				(try_end),
				(try_begin),
					(eq, ":is_anyone_dead", 0),
					# destroy prison cart (since there is no dead player left in the game)
					(call_script, "script_multiplayer_ccoop_destroy_prison_cart"),
				(try_end),
				
			(else_try),
			
				# if prison cart is not spawned and there is a dead player, then spawn the prison cart
				(assign, ":is_anyone_dead", 0),
				(try_for_range, ":cur_player", 0, ":max_players"),
					(eq, ":is_anyone_dead", 0),				
					(player_is_active, ":cur_player"),
					(player_get_team_no, ":player_team", ":cur_player"),
					(eq, ":player_team", 0),
					(player_get_agent_id, ":player_agent", ":cur_player"),
					(ge, ":player_agent", 0),
					(neg|agent_is_alive, ":player_agent"),
					(assign, ":is_anyone_dead", 1),
				(try_end),
				(try_begin),
					(eq, ":is_anyone_dead", 1),
					(eq, "$g_multiplayer_ccoop_spawn_alive_player_squad_and_minus_one_first_spawn_slots_and_minus_one_first_spawn_slots", 1), # if cart is not spawned before in this round, otherwise that value would be 0
					# spawn prison cart with 5 second delay
					(le, "$g_multiplayer_ccoop_spawn_player_and_squad_counter", 0), # if not in player spawn period
					(eq, "$g_multiplayer_ccoop_spawn_prison_cart_counter", 0), # if not in prison cart spawn period
					(assign, "$g_multiplayer_ccoop_spawn_prison_cart_counter", 5),
					(display_debug_message, "@{!}spawn prison cart 5 secs initiated!"),
				(try_end),
				
				(try_begin),
					(gt, "$g_multiplayer_ccoop_spawn_prison_cart_counter", 0),
					(val_sub, "$g_multiplayer_ccoop_spawn_prison_cart_counter", 1),
					(display_debug_message, "@{!}spawn prison cart!"),
					(try_begin),
						(eq, "$g_multiplayer_ccoop_spawn_prison_cart_counter", 0),
						(call_script, "script_multiplayer_ccoop_spawn_prison_cart"),
					(try_end),
				(try_end),
				
			(try_end),
			
			# player&bot spawn management
			(try_begin),
				(multiplayer_is_server),
				(gt, "$g_multiplayer_ccoop_spawn_player_and_squad_counter", 0),
				(val_sub, "$g_multiplayer_ccoop_spawn_player_and_squad_counter", 1),
				(try_begin),
					(lt, "$g_multiplayer_ccoop_spawn_player_and_squad_counter", 25),
					
					# respawn all dead players
					(get_max_players, ":max_players"),
					(try_for_range, ":cur_player", 0, ":max_players"),
						(player_is_active, ":cur_player"),
						(player_get_team_no, ":player_team", ":cur_player"), # if player is not spectator
						(lt, ":player_team", multi_team_spectator),
						(player_get_agent_id, ":player_agent", ":cur_player"),
						
						(try_begin),
							(this_or_next|lt, ":player_agent", 0), #if not spawned or
							(neg|agent_is_alive, ":player_agent"), #if agent is dead
							
							(try_begin),
								# if first spawn this round
								(player_get_slot, ":player_first_spawn", ":cur_player", slot_player_first_spawn),
								(eq, ":player_first_spawn", 1),
                                
								
								(call_script, "script_multiplayer_ccoop_spawn_player_and_bots", ":cur_player"),
								
								# if spawned
								(try_begin),
									(eq, reg0, 1),
									(player_set_slot, ":cur_player", slot_player_first_spawn, 0),
								(try_end),
								
							(try_end),
							
						(else_try),
							(assign, reg0, "$g_multiplayer_ccoop_spawn_alive_player_squad_and_minus_one_first_spawn_slots_and_minus_one_first_spawn_slots"),
							(display_debug_message, "@{!}g_multiplayer_ccoop_spawn_alive_player_squad: {reg0}"),
						
							(eq, "$g_multiplayer_ccoop_spawn_alive_player_squad_and_minus_one_first_spawn_slots_and_minus_one_first_spawn_slots", 1),
							(neg|player_is_busy_with_menus, ":cur_player"), # if player is not busy with menus
							(player_get_troop_id, ":player_troop", ":cur_player"), # if troop is not selected do not spawn his bots	
							(ge, ":player_troop", 0),
							
							# buy squads of alive player
							(call_script, "script_multiplayer_spawn_player_bot_squad_at_point", ":cur_player", 0, reg0),
							(call_script, "script_multiplayer_upgrade_player_equipment", ":cur_player"),
                            (try_for_agents, ":cur_agent"),
                              (agent_is_active, ":cur_agent"),
                              (agent_is_alive, ":cur_agent"),
                              (agent_is_non_player, ":cur_agent"),
                              (agent_get_group, ":cur_agent_group", ":cur_agent"),
                              (eq, ":cur_agent_group", ":cur_player"),
							  (call_script, "script_cf_multiplayer_upgrade_companion_equipment", ":cur_agent"),
                            (try_end),
							#(call_script, "script_multiplayer_get_spawn_point_close_to_bots", ":cur_player"),
							(call_script, "script_multiplayer_get_spawn_point_close_to_player", ":cur_player"),
						(try_end),
						
						
					(try_end),
					
					
					
				(try_end),
				
			(try_end),
		]),

				
		# first spawn
		(1, 0, 0, 
		[			
			(eq, "$g_multiplayer_ccoop_game_started", 0),
			(multiplayer_is_server),
		],
		
		[			
			(assign, ":any_player_spawned", 0),
			
			(get_max_players, ":num_players"),
			(try_for_range, ":player_no", 0, ":num_players"),
				(player_is_active, ":player_no"),
				
				(call_script, "script_multiplayer_ccoop_spawn_player_and_bots", ":player_no"),
                

				
				(try_begin),
					(eq, ":any_player_spawned", 0),
					(gt, reg0, 0),
					(assign, ":any_player_spawned", 1),
				(try_end),
			(try_end),
			
			(try_begin),
				(ge, ":any_player_spawned", 1),
                
			
				#(display_debug_message, "@{!}first spawn" ),
				(assign, "$g_multiplayer_ccoop_game_started", 1),
				
				(assign, "$g_multiplayer_ccoop_enemy_respawn_secs", 31), # set 31 secs left for next wave
				(assign, "$g_multiplayer_ccoop_enable_count_down", 1), # enable count down
				
				(call_script, "script_multiplayer_ccoop_start_player_and_squad_respawn_period", 1),
			(try_end),
		]),
    
		multiplayer_server_check_end_map,

		(ti_tab_pressed, 0, 0, [],
		[
			(try_begin),
				(eq, "$g_multiplayer_mission_end_screen", 0),
				(assign, "$g_multiplayer_stats_chart_opened_manually", 1),
				(start_presentation, "prsnt_multiplayer_stats_chart_deathmatch"),
			(try_end),
		]),

		multiplayer_once_at_the_first_frame,
		#multiplayer_battle_window_opened,
		(ti_battle_window_opened, 0, 0, [], [
			#(start_presentation, "prsnt_multiplayer_round_time_counter"),
			#(start_presentation, "prsnt_multiplayer_team_score_display"),
			(start_presentation, "prsnt_multiplayer_flag_projection_display_ccoop"),
			(start_presentation, "prsnt_multiplayer_flag_projection_display_ccoop_wave"),
			(start_presentation, "prsnt_multiplayer_ccoop_next_wave_time_counter"),
        ]),

		(ti_escape_pressed, 0, 0, [],
		[
			(neg|is_presentation_active, "prsnt_multiplayer_escape_menu"),
			(neg|is_presentation_active, "prsnt_multiplayer_stats_chart_deathmatch"),
			(eq, "$g_waiting_for_confirmation_to_terminate", 0),
			(start_presentation, "prsnt_multiplayer_escape_menu"),
		]),
        
		(ti_on_agent_hit, 0, 0, [(multiplayer_is_server),],
		[
            (multiplayer_is_server),
            
            (store_trigger_param_1, ":agent_no"),
            (store_trigger_param_2, ":attacker_no"),
            (store_trigger_param_3, ":damage"),
                        
            (agent_get_troop_id, ":attacker_troop_id", ":agent_no"),
            (try_begin),
              (this_or_next|is_between, ":attacker_troop_id", lords_begin, lords_end),
              (is_between, ":attacker_troop_id", kings_begin, kings_end),
              (store_random_in_range, ":random", 0, 10),
              (try_begin),
                (eq, ":random", 0),
                (agent_get_position, pos60, ":attacker_no"),
                (call_script, "script_multiplayer_server_play_sound_at_position", ccoop_noble_sounds_start),
              (try_end),
            (else_try),
              (is_between, ":attacker_troop_id", multiplayer_coop_companion_equipment_sets_begin, multiplayer_coop_companion_first_equipment_sets_end),
              (store_random_in_range, ":random", 0, 30),
              (try_begin),
                (eq, ":random", 0),
                (agent_get_position, pos60, ":attacker_no"),
                (store_random_in_range, ":sound_id", ccoop_companion_sounds_start, ccoop_companion_sounds_end),
                (call_script, "script_multiplayer_server_play_sound_at_position", ":sound_id"),
              (try_end),
            (else_try),
              (this_or_next|eq, ":attacker_troop_id", "trp_sea_raider"),
              (eq, ":attacker_troop_id", "trp_sea_raider_leader"),
              (store_random_in_range, ":random", 0, 30),
              (try_begin),
                (eq, ":random", 0),
                (agent_get_position, pos60, ":attacker_no"),
                (store_random_in_range, ":sound_id", ccoop_sea_raider_sounds_start, ccoop_sea_raider_sounds_end),
                (call_script, "script_multiplayer_server_play_sound_at_position", ":sound_id"),
              (try_end),
            (else_try),
              (eq, ":attacker_troop_id", "trp_looter"),
              (store_random_in_range, ":random", 0, 20),
              (try_begin),
                (eq, ":random", 0),
                (agent_get_position, pos60, ":attacker_no"),
                (store_random_in_range, ":sound_id", ccoop_looter_sounds_start, ccoop_looter_sounds_end),
                (call_script, "script_multiplayer_server_play_sound_at_position", ":sound_id"),
              (try_end),
            (else_try),
              (is_between, ":attacker_troop_id", bandits_begin, bandits_end),
              (store_random_in_range, ":random", 0, 60),
              (try_begin),
                (eq, ":random", 0),
                (agent_get_position, pos60, ":attacker_no"),
                (store_random_in_range, ":sound_id", ccoop_bandit_sounds_start, ccoop_bandit_sounds_end),
                (call_script, "script_multiplayer_server_play_sound_at_position", ":sound_id"),
              (try_end),
            (try_end),
        
			(try_begin),
              (eq, reg0, "itm_knockdown_mace"),
              (agent_is_human, ":agent_no"),
              (agent_get_horse, ":horse", ":agent_no"),
              (le, ":horse", -1),
              (agent_set_animation, ":agent_no", "anim_strike_fall_back_rise"),
            (else_try),
              (eq, reg0, "itm_blood_drain_throwing_knives"),
              (store_agent_hit_points, ":agent_health", ":attacker_no", 1),
              (val_add, ":agent_health", ":damage"),
              (agent_set_hit_points, ":attacker_no", ":agent_health", 1),
              (store_agent_hit_points, ":agent_health", ":attacker_no", 0),
              (ge, ":agent_health", 100),
              (agent_set_hit_points, ":attacker_no", ":agent_health", 100),
            (else_try),
              (eq, reg0, "itm_instakill_knife"),
              #(store_trigger_param_2, ":attacker_no"),
              #(store_agent_hit_points, ":agent_health", ":agent_no", 1),
              (agent_set_hit_points, ":agent_no", 0),
            (else_try),
              (eq, reg0, "itm_backstabber"),
              (try_begin),
                (agent_get_action_dir, ":attacker_action_dir", ":attacker_no"),
                (eq, ":attacker_action_dir", 0),
                (agent_get_position, pos0, ":agent_no"),
                (agent_get_position, pos1, ":attacker_no"),
                (position_is_behind_position, pos1, pos0),
                #(store_agent_hit_points, ":agent_health", ":agent_no", 1),
                (agent_set_hit_points, ":agent_no", 0),
              (try_end),
            (else_try),
              (eq, reg0, "itm_disarming_throwing_axe"),
              (try_begin),
                (agent_is_human, ":agent_no"),
                (try_for_range, ":hand_no", 0, 2),
                  (agent_get_wielded_item, ":item_no", ":agent_no", ":hand_no"),
                  (neq, ":item_no", -1),
                  (agent_unequip_item, ":agent_no", ":item_no"),
                  (agent_get_position, pos0, ":agent_no"),
                  (set_spawn_position, pos0),
                  (spawn_item, ":item_no"),
                (try_end),
              (try_end),
            (else_try),
              (eq, reg0, -1),
              (try_begin),
                (agent_is_human, ":attacker_no"),
                (agent_is_human, ":agent_no"),
                (agent_get_item_slot, ":agent_boots", ":attacker_no", 6),
                (eq, ":agent_boots", "itm_kicking_boots"),
                (store_agent_hit_points, ":agent_health", ":agent_no", 1),
                (assign, reg2, ":agent_health"),
                (val_max, ":damage", 2),
                (val_mul, ":damage", 6),
                (val_sub, ":agent_health", ":damage"),
                (val_max, ":agent_health", 0),
                (agent_set_hit_points, ":agent_no", ":agent_health", 1),
                (agent_get_item_id, ":horse", ":agent_no"),
                (eq, ":horse", -1),
                (agent_set_animation, ":agent_no", "anim_strike_fall_back_rise"),
              (try_end),
            (else_try),
              (eq, reg0, "itm_doom_javelins"),
              (agent_get_slot, ":num_doom_javs", ":agent_no", slot_agent_doom_javelin_count),
              (val_add, ":num_doom_javs", 1),
              (agent_set_slot, ":agent_no", slot_agent_doom_javelin_count, ":num_doom_javs"),
              #(agent_get_player_id, ":player_no", ":attacker_no"),
              #(agent_set_slot, ":agent_no", slot_agent_doom_javelin_attacker, ":player_no"),
            (else_try),
              (eq, reg0, "itm_team_change_dart"),
              (try_begin),
                (agent_is_non_player, ":agent_no"),
                (agent_get_team, ":agent_team", ":agent_no"),
                (assign, ":team_has_other_agents", 0),
                (try_for_agents, ":cur_agent"),
                  (neq, ":cur_agent", ":agent_no"),
                  (agent_is_active, ":cur_agent"),
                  (agent_is_alive, ":cur_agent"),
                  (agent_is_human, ":cur_agent"),
                  (agent_get_team, ":cur_agent_team", ":cur_agent"),
                  (eq, ":cur_agent_team", 1),
                  (assign, ":team_has_other_agents", 1),
                (try_end),
                (eq, ":team_has_other_agents", 1),
                (try_begin),
                  (eq, ":agent_team", 0),
                  (agent_set_team, ":agent_no", 1),
                (else_try),
                  (eq, ":agent_team", 1),
                  (agent_set_team, ":agent_no", 0),
                (try_end),
                (try_begin),
                  (agent_is_non_player, ":attacker_no"),
                  (agent_get_group, ":group_no", ":attacker_no"),
                (else_try),
                  (agent_get_player_id, ":group_no", ":attacker_no"),
                (try_end),
                (try_begin),
                  (player_is_active, ":group_no"),
                  (agent_set_group, ":agent_no", ":group_no"),
                (try_end),
                (agent_get_team, ":agent_new_team", ":agent_no"),
                (get_max_players, ":num_players"),						
                (try_for_range, ":cur_player", 1, ":num_players"),						
                  (player_is_active, ":cur_player"),
                  (multiplayer_send_4_int_to_player, ":cur_player", multiplayer_event_other_events, multiplayer_event_coop_set_agent_team_and_group,
                    ":agent_no", ":agent_new_team", ":attacker_no"),							
                (try_end),        
                (agent_force_rethink, ":agent_no"),              
              (try_end),
            (else_try),
              (eq, reg0, "itm_weak_beserker_dart"),
              #(store_trigger_param_2, ":attacker_no"),
              (agent_ai_set_aggressiveness, ":agent_no", 1000),
              (agent_set_speed_modifier, ":agent_no", 150),
              (agent_set_damage_modifier, ":agent_no", 200),
              (agent_set_hit_points, ":agent_no", 10, 0),
            #(else_try),
            #  (eq, reg0, "itm_scatter_crossbow"),
            #  (store_trigger_param_1, ":agent_no"),
            #  (store_trigger_param_2, ":attacker_no"),
            #  #(assign, ":min_dist", 1000),
            #  #(try_for_range, ":cur_bone_no", 0, 20),
            #  #  (agent_get_bone_position, pos1, ":agent_no", ":cur_bone_no"),
            #  #  (get_distance_between_positions, ":dist", pos0, pos1),
            #  #  (lt, ":dist", ":min_dist"),
            #  #  (assign, ":hit_bone", ":cur_bone_no"),
            #  #  (val_min, ":min_dist", ":dist"),
            #  #(try_end),
            #  (try_begin),
            #    #(eq, ":hit_bone", 9),
            #    (copy_position, pos1, pos0),
            #    (try_for_agents, ":cur_agent", pos1, 5),
            #      (agent_is_active, ":cur_agent"),
            #      (agent_is_alive, ":cur_agent"),
            #      (agent_get_team, ":cur_agent_team", ":cur_agent"),
            #      (eq, ":cur_agent_team", 1),
            #      (agent_set_look_target_agent, ":agent_no", ":cur_agent"),
            #      #(agent_get_bone_position, pos2, ":agent_no", 9),
            #      (agent_get_look_position, pos2, ":agent_no"),
            #      (add_missile, ":attacker_no", pos2, 90, "itm_scatter_crossbow", 0, "itm_scatter_bolts", 0),
            #      
            #    (try_end),
            #  (try_end),
            (try_end),
		]),
        
		# for leeching effects such as the doom jav and healing armour.
		(2, 0, 0, [(multiplayer_is_server),],
		[
          (multiplayer_is_server),
          (try_for_agents, ":agent_no"),
            (agent_is_active, ":agent_no"),
            (agent_is_alive, ":agent_no"),
            (agent_is_human, ":agent_no"),
            (agent_get_item_slot, ":body_armour", ":agent_no", 5),
            (try_begin),
              (eq, ":body_armour", "itm_restore_health_armour"),
              (store_agent_hit_points, ":agent_health", ":agent_no", 1),
              (val_add, ":agent_health", 5),
              (agent_set_hit_points, ":agent_no", ":agent_health", 1),
              (store_agent_hit_points, ":agent_health", ":agent_no", 0),
              (val_min, ":agent_health", 100),
              (agent_set_hit_points, ":agent_no", ":agent_health", 0),
            (try_end),
              
            (agent_get_slot, ":num_doom_javs", ":agent_no", slot_agent_doom_javelin_count),
            (try_begin),
              (gt, ":num_doom_javs", 0),
              (assign, reg1, ":num_doom_javs"),
              (store_mul, ":damage", ":num_doom_javs", 5),
              #(agent_get_slot, ":player_no", ":agent_no", slot_agent_doom_javelin_attacker),
              #(try_begin),
              ##  (player_is_active, ":player_no"),
              ##  (player_get_agent_id, ":attacker_no", ":player_no"),
              ##(else_try),
              #  (assign, ":attacker_no", ":agent_no"),
              #(try_end),
              (store_agent_hit_points, ":agent_health", ":agent_no", 1),
              (assign, reg2, ":agent_health"),
              (val_sub, ":agent_health", ":damage"),
              (val_max, ":agent_health", 0),
              (agent_set_hit_points, ":agent_no", ":agent_health", 1),
              #(assign, reg3, ":agent_health"),
              #(assign, reg0, ":agent_no"),
              #(display_message, "@agent no {reg0} - num javs {reg1} - initial health {reg2} - resulting health {reg3}"),
              (try_begin),
                (eq, ":agent_health", 0),
                (agent_deliver_damage_to_agent, ":agent_no", ":agent_no", 1),
              (try_end),
            (try_end),
          (try_end),
            

		]),
        
	]),
  
  
  
  #############################  END OF WAVE MODE
  ###############################################
#INVASION MODE END
  
  (
	"bandit_lair",mtf_battle_mode|mtf_synch_inventory,charge,
    "Ambushing a bandit lair",
    [
      (0,mtef_team_0|mtef_use_exact_number,af_override_horse, aif_start_alarmed, 7,[]),
      (1,mtef_visitor_source|mtef_team_1,af_override_horse, aif_start_alarmed,20,[]),
      (2,mtef_visitor_source|mtef_team_1,af_override_horse, aif_start_alarmed,20,[]),
      (3,mtef_visitor_source|mtef_team_1,af_override_horse, aif_start_alarmed,20,[]),
      (4,mtef_visitor_source|mtef_team_1,af_override_horse, aif_start_alarmed,20,[]),
      (5,mtef_visitor_source|mtef_team_1,af_override_horse, aif_start_alarmed,20,[]),
      (6,mtef_visitor_source|mtef_team_1,af_override_horse, aif_start_alarmed,20,[]),
      (7,mtef_visitor_source|mtef_team_1,af_override_horse, aif_start_alarmed,20,[]),
      (8,mtef_visitor_source|mtef_team_1,af_override_horse, aif_start_alarmed,20,[]),
      (9,mtef_visitor_source|mtef_team_1,af_override_horse, aif_start_alarmed,20,[]),
      (10,mtef_visitor_source|mtef_team_1,af_override_horse, aif_start_alarmed,20,[]),
    ],
    [
      common_battle_init_banner,
    
      common_inventory_not_available,
      
      (ti_on_agent_spawn, 0, 0, [],
      [
        (store_trigger_param_1, ":agent_no"),
        
        (assign, "$relative_of_merchant_is_found", 0),
              
        (try_begin),
          (agent_is_human, ":agent_no"),
          (agent_is_alive, ":agent_no"),
          (agent_get_team, ":agent_team", ":agent_no"),
          (eq, ":agent_team", 1),

          (agent_get_position, pos4, ":agent_no"),
          (agent_set_scripted_destination, ":agent_no", pos4, 1),
        (try_end),  
        
        (try_begin),
          (agent_get_troop_id, ":troop_no", ":agent_no"),
          (is_between, ":troop_no", "trp_relative_of_merchant", "trp_relative_of_merchants_end"),
          (agent_set_team, ":agent_no", 7),
          (team_set_relation, 0, 7, 0),          
        (try_end),                
        ]),
        
	   (0, 0, 0, 
	   [	     
         (party_get_template_id, ":template", "$g_encountered_party"),
         (eq, ":template", "pt_looter_lair"),
         (check_quest_active, "qst_save_relative_of_merchant"),	   
         (eq, "$relative_of_merchant_is_found", 0),
	   ],
	   [
        (get_player_agent_no, ":player_agent"),
        (agent_get_position, pos0, ":player_agent"),

        (try_for_agents, ":agent_no"),
          (agent_get_troop_id, ":troop_no", ":agent_no"),
          (is_between, ":troop_no", "trp_relative_of_merchant", "trp_relative_of_merchants_end"),    
          (agent_set_scripted_destination, ":agent_no", pos0),
          (agent_get_position, pos1, ":agent_no"),
          (get_distance_between_positions, ":dist", pos0, pos1),
          (le, ":dist", 200),
          #(assign, "$g_talk_troop", "trp_relative_of_merchant"),
          (start_mission_conversation, "trp_relative_of_merchant"),
        (try_end),
	   ]),
        
      (ti_tab_pressed, 0, 0,
       [
        (display_message, "str_cannot_leave_now"),
       ], []),
     
      (1, 0, ti_once, [],
       [
        (assign, "$defender_reinforcement_stage", 0),
        (assign, "$bandits_spawned_extra", 0),
	   ]),
	   
	   (1, 0, 0, [],
	   [
        (try_for_agents, ":bandit_id"),
          (agent_is_alive, ":bandit_id"),          
          (agent_get_team, ":agent_team_1", ":bandit_id"),
          (eq, ":agent_team_1", 1),
          (agent_is_in_special_mode, ":bandit_id"),
          (agent_is_human, ":bandit_id"),
          
          (agent_get_position, pos0, ":bandit_id"),
          (try_for_agents, ":player_team_agent_id"),
            (agent_is_alive, ":player_team_agent_id"),
            (agent_get_team, ":agent_team_2", ":player_team_agent_id"),
            (eq, ":agent_team_2", 0),
            (agent_is_human, ":player_team_agent_id"),
                      
            (store_agent_hit_points, ":bandit_hit_points", ":bandit_id"),
            
            (assign, ":continue", 0),
            (try_begin),
              (lt, ":bandit_hit_points", 100),
                            
              (try_for_agents, ":bandit_2_id"),
                (agent_is_alive, ":bandit_2_id"),  
                (agent_get_team, ":bandit_2_team", ":bandit_2_id"),
                (eq, ":bandit_2_team", 1),
                (neq, ":bandit_id", ":bandit_2_id"),
                (agent_is_in_special_mode, ":bandit_2_id"),
                (agent_is_human, ":bandit_2_id"),
                
                (agent_get_position, pos1, ":bandit_id"),
                (agent_get_position, pos2, ":bandit_2_id"),                        
                (get_distance_between_positions, ":distance", pos1, pos2),
                (le, ":distance", 1000),

                (agent_clear_scripted_mode, ":bandit_2_id"),  
              (try_end),                             
              
              (assign, ":continue", 1),
            (else_try),  
              (agent_get_position, pos1, ":bandit_id"),
              (agent_get_position, pos2, ":player_team_agent_id"),                        
              (get_distance_between_positions, ":distance", pos1, pos2),                                                                        
              (le, ":distance", 4000),
              
              (try_for_agents, ":bandit_2_id"),
                (agent_is_alive, ":bandit_2_id"),  
                (agent_get_team, ":bandit_2_team", ":bandit_2_id"),
                (eq, ":bandit_2_team", 1),
                (neq, ":bandit_id", ":bandit_2_id"),
                (agent_is_in_special_mode, ":bandit_2_id"),
                (agent_is_human, ":bandit_2_id"),
                
                (agent_get_position, pos1, ":bandit_id"),
                (agent_get_position, pos2, ":bandit_2_id"),                        
                (get_distance_between_positions, ":distance", pos1, pos2),
                (le, ":distance", 1000),
                
                (agent_clear_scripted_mode, ":bandit_2_id"),  
              (try_end),                

              (assign, ":continue", 1),
            (try_end),  
            
            (eq, ":continue", 1),
            
            (agent_clear_scripted_mode, ":bandit_id"),            
          (try_end),
        (try_end),
	   ]),
	   
	   (30, 0, 0, 
	   [
	     (le, "$defender_reinforcement_stage", 1),
	   ],
	   [          
          (store_character_level, ":player_level", "trp_player"),                   
          (store_add, ":number_of_bandits_will_be_spawned_at_each_period", 5, ":player_level"),
          (val_div, ":number_of_bandits_will_be_spawned_at_each_period", 3),

          (lt, "$bandits_spawned_extra", ":number_of_bandits_will_be_spawned_at_each_period"),
          (val_add, "$bandits_spawned_extra", 1),                   

          (party_get_template_id, ":template", "$g_encountered_party"),
          (store_random_in_range, ":random_value", 0, 2),
          
          (try_begin),
            (eq, ":template", "pt_sea_raider_lair"),
            (eq, ":random_value", 0),
            (assign, ":bandit_troop", "trp_sea_raider"),
          (else_try),
            (eq, ":template", "pt_forest_bandit_lair"),
            (eq, ":random_value", 0),
            (assign, ":bandit_troop", "trp_forest_bandit"),
          (else_try),
            (eq, ":template", "pt_desert_bandit_lair"),
            (eq, ":random_value", 0),
            (assign, ":bandit_troop", "trp_desert_bandit"),
          (else_try),
            (eq, ":template", "pt_mountain_bandit_lair"),
            (eq, ":random_value", 0),
            (assign, ":bandit_troop", "trp_mountain_bandit"),
          (else_try),
            (eq, ":template", "pt_taiga_bandit_lair"),
            (eq, ":random_value", 0),
            (assign, ":bandit_troop", "trp_taiga_bandit"),
          (else_try),
            (eq, ":template", "pt_steppe_bandit_lair"),
            (eq, ":random_value", 0),
            (assign, ":bandit_troop", "trp_steppe_bandit"),
          (else_try),
            (this_or_next|eq, ":template", "pt_looter_lair"),
            (neq, ":random_value", 0),
            (assign, ":bandit_troop", "trp_looter"),
          (try_end),

          (store_current_scene, ":cur_scene"), 
          (modify_visitors_at_site, ":cur_scene"),
          (store_random_in_range, ":random_entry_point", 2, 11),
          (add_visitors_to_current_scene, ":random_entry_point", ":bandit_troop", 1),
       ]),	   	   

      (ti_on_agent_killed_or_wounded, 0, 0, [],
       [
        (store_trigger_param_1, ":dead_agent_no"),
        #(store_trigger_param_2, ":killer_agent_no"),
        (store_trigger_param_3, ":is_wounded"),

        (try_begin),
          (ge, ":dead_agent_no", 0),
          (agent_is_human, ":dead_agent_no"),
          (agent_get_troop_id, ":dead_agent_troop_id", ":dead_agent_no"),
          (str_store_troop_name, s6, ":dead_agent_troop_id"),
          (try_begin),
            (neg|agent_is_ally, ":dead_agent_no"),
            (party_add_members, "p_total_enemy_casualties", ":dead_agent_troop_id", 1), #addition_to_p_total_enemy_casualties            
            (try_begin),
              (eq, ":is_wounded", 1),
              (party_wound_members, "p_total_enemy_casualties", ":dead_agent_troop_id", 1), 
            (try_end),  
          (try_end),  
          
          (party_add_members, "p_temp_casualties", ":dead_agent_troop_id", 1), #addition_to_p_total_enemy_casualties            
          
          (eq, ":is_wounded", 1),
          (party_wound_members, "p_temp_casualties", ":dead_agent_troop_id", 1), 
        (try_end),
        
        (assign, ":number_of_enemies", 0),
        (try_for_agents, ":cur_agent"),
          (agent_is_non_player, ":cur_agent"),
          (agent_is_human, ":cur_agent"),
          (agent_is_alive, ":cur_agent"),
          (neg|agent_is_ally, ":cur_agent"),
          (val_add, ":number_of_enemies", 1),
        (try_end),
        
        (try_begin),
          (le, ":number_of_enemies", 2),
          (le, "$defender_reinforcement_stage", 1),
          (val_add, "$defender_reinforcement_stage", 1),

          (store_character_level, ":player_level", "trp_player"),                   
          (store_add, ":number_of_bandits_will_be_spawned_at_each_period", 5, ":player_level"),
          (val_div, ":number_of_bandits_will_be_spawned_at_each_period", 3),
          (try_begin),
            (ge, "$defender_reinforcement_stage", 2),
            (val_sub, ":number_of_bandits_will_be_spawned_at_each_period", "$bandits_spawned_extra"),
          (try_end),
          
          (party_get_template_id, ":template", "$g_encountered_party"),          
          (store_random_in_range, ":random_value", 0, 2),
          
          (try_begin),
            (eq, ":template", "pt_sea_raider_lair"),
            (eq, ":random_value", 0),
            (assign, ":bandit_troop", "trp_sea_raider"),
          (else_try),
            (eq, ":template", "pt_forest_bandit_lair"),
            (eq, ":random_value", 0),
            (assign, ":bandit_troop", "trp_forest_bandit"),
          (else_try),
            (eq, ":template", "pt_desert_bandit_lair"),
            (eq, ":random_value", 0),
            (assign, ":bandit_troop", "trp_desert_bandit"),
          (else_try),
            (eq, ":template", "pt_mountain_bandit_lair"),
            (eq, ":random_value", 0),
            (assign, ":bandit_troop", "trp_mountain_bandit"),
          (else_try),
            (eq, ":template", "pt_taiga_bandit_lair"),
            (eq, ":random_value", 0),
            (assign, ":bandit_troop", "trp_taiga_bandit"),
          (else_try),
            (eq, ":template", "pt_steppe_bandit_lair"),
            (eq, ":random_value", 0),
            (assign, ":bandit_troop", "trp_steppe_bandit"),
          (else_try),
            (this_or_next|eq, ":template", "pt_looter_lair"),
            (neq, ":random_value", 0),
            (assign, ":bandit_troop", "trp_looter"),
          (try_end),
                                                                       
          (store_current_scene, ":cur_scene"), 
          (modify_visitors_at_site, ":cur_scene"),
          (try_for_range, ":unused", 0, ":number_of_bandits_will_be_spawned_at_each_period"),            
            (store_random_in_range, ":random_entry_point", 2, 11),
            (add_visitors_to_current_scene, ":random_entry_point", ":bandit_troop", 1),
          (try_end),
        (try_end),

        #no need to adjust courage in bandit lair for now
        #(call_script, "script_apply_death_effect_on_courage_scores", ":dead_agent_no", ":killer_agent_no"),
       ]),

      (0, 0, ti_once, [],
       [
         (call_script, "script_music_set_situation_with_culture", mtf_sit_ambushed),
         (set_party_battle_mode),
        ]),

      (2, 0, ti_once, 
       [
         (neg|main_hero_fallen),
         (num_active_teams_le, 1),         
       ],
       [
         (party_get_template_id, ":template", "$g_encountered_party"),
         (try_begin),
           (eq, ":template", "pt_looter_lair"),
           (check_quest_active, "qst_save_relative_of_merchant"),

           (store_faction_of_party, ":starting_town_faction", "$g_starting_town"),
           
           (try_begin),
             (eq, ":starting_town_faction", "fac_kingdom_1"),
             (assign, ":troop_of_merchant", "trp_relative_of_merchant"),
           (else_try),  
             (eq, ":starting_town_faction", "fac_kingdom_2"),
             (assign, ":troop_of_merchant", "trp_relative_of_merchant"),
           (else_try),                   
             (eq, ":starting_town_faction", "fac_kingdom_3"),
             (assign, ":troop_of_merchant", "trp_relative_of_merchant"),
           (else_try),  
             (eq, ":starting_town_faction", "fac_kingdom_4"),
             (assign, ":troop_of_merchant", "trp_relative_of_merchant"),
           (else_try),  
             (eq, ":starting_town_faction", "fac_kingdom_5"),
             (assign, ":troop_of_merchant", "trp_relative_of_merchant"),
           (else_try),  
             (eq, ":starting_town_faction", "fac_kingdom_6"),
             (assign, ":troop_of_merchant", "trp_relative_of_merchant"),
           (try_end),
           
           (get_player_agent_no, ":player_agent"),
           (agent_get_position, pos0, ":player_agent"),
           (assign, ":minimum_distance", 100000),
           (try_for_range, ":entry_no", 1, 10),
             (entry_point_get_position, pos1, ":entry_no"),
             (get_distance_between_positions, ":dist", pos0, pos1),
             (le, ":dist", ":minimum_distance"),
             (ge, ":dist", 1000),
             (assign, ":nearest_entry_point", ":entry_no"),
             (assign, ":minimum_distance", ":dist"),
           (try_end),                     
                          
           (add_visitors_to_current_scene, ":nearest_entry_point", ":troop_of_merchant", 1, 0),                      
         (try_end),
       ]),

       common_battle_order_panel,
       common_battle_order_panel_tick,

       (1, 4, ti_once,
       [
         (assign, ":continue", 0),
       
         (party_get_template_id, ":template", "$g_encountered_party"),
         (try_begin),       
           (eq, ":template", "pt_looter_lair"),
           (check_quest_active, "qst_save_relative_of_merchant"),
           
           (this_or_next|main_hero_fallen),
           (eq, "$relative_of_merchant_is_found", 1),
           
           (assign, ":continue", 1),
         (else_try),
           (this_or_next|neq|eq, ":template", "pt_looter_lair"),
           (neg|check_quest_active, "qst_save_relative_of_merchant"),

           (store_mission_timer_a,":cur_time"),
           (ge, ":cur_time", 5),
           
           (this_or_next|main_hero_fallen),
           (num_active_teams_le, 1),
           
           (assign, ":continue", 1),
         (try_end),  
         
         (eq, ":continue", 1),
       ],
       [
         (try_begin),
           (main_hero_fallen),
         (else_try),
           (party_set_slot, "$g_encountered_party", slot_party_ai_substate, 2),
         (try_end),
         
         (finish_mission),
         ]),
      ]),
        
  (
	"alley_fight", mtf_battle_mode,charge,
    "Alley fight",
    [    
      (0,mtef_team_0|mtef_use_exact_number,af_override_horse,aif_start_alarmed,7,[]),
      (1,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,20,[]),
      (2,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,20,[]),
      (3,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,20,[]),
    ],    
    [
      common_battle_init_banner,
    
      common_inventory_not_available,
      
      (ti_on_agent_spawn, 0, 0, [],
      [              
        (store_trigger_param_1, ":agent_no"),
        (get_player_agent_no, ":player_agent"),
        (neq, ":agent_no", ":player_agent"),
        (assign, "$g_main_attacker_agent", ":agent_no"),
        (agent_ai_set_aggressiveness, ":agent_no", 199),
        
        (try_begin),
          (agent_get_troop_id, ":troop_no", ":agent_no"),
          (is_between, ":troop_no", "trp_swadian_merchant", "trp_startup_merchants_end"),
          (agent_set_team, ":agent_no", 7),          
          (team_set_relation, 0, 7, 0), 
        (try_end),                
      ]),
              
	   (0, 0, 0, 
	   [
	     (eq, "$talked_with_merchant", 0), 
	   ],
	   [
        (get_player_agent_no, ":player_agent"),
        (agent_get_position, pos0, ":player_agent"),

        (try_for_agents, ":agent_no"),
          (agent_get_troop_id, ":troop_no", ":agent_no"),
          (is_between, ":troop_no", "trp_swadian_merchant", "trp_startup_merchants_end"),
          (agent_set_scripted_destination, ":agent_no", pos0),
          (agent_get_position, pos1, ":agent_no"),
          (get_distance_between_positions, ":dist", pos0, pos1),
          (le, ":dist", 200),     
          (assign, "$talk_context", tc_back_alley),     
          (start_mission_conversation, ":troop_no"),
        (try_end),
	   ]),
     
      (1, 0, 0, [], 
      [      
        (get_player_agent_no, ":player_agent"),       
        (ge, "$g_main_attacker_agent", 0),
        (ge, ":player_agent", 0),
        (agent_is_active, "$g_main_attacker_agent"),
        (agent_is_active, ":player_agent"),
        (agent_get_position, pos0, ":player_agent"),
        (agent_get_position, pos1, "$g_main_attacker_agent"),
        (get_distance_between_positions, ":dist", pos0, pos1),
        (ge, ":dist", 5),
        (agent_set_scripted_destination, "$g_main_attacker_agent", pos0),
      ]),

      (ti_tab_pressed, 0, 0, [], 
      [
        (display_message, "str_cannot_leave_now"),
      ]),

      (0, 0, ti_once, [],
       [
         (call_script, "script_music_set_situation_with_culture", mtf_sit_ambushed),
         (set_party_battle_mode),
        ]),

      (0, 0, ti_once, 
       [
         (neg|main_hero_fallen),
         (num_active_teams_le, 1),
       ],
       [
         (store_faction_of_party, ":starting_town_faction", "$g_starting_town"),
           
         (try_begin),
           (eq, ":starting_town_faction", "fac_kingdom_1"),
           (assign, ":troop_of_merchant", "trp_swadian_merchant"),
         (else_try),  
           (eq, ":starting_town_faction", "fac_kingdom_2"),
           (assign, ":troop_of_merchant", "trp_vaegir_merchant"),
         (else_try),                   
           (eq, ":starting_town_faction", "fac_kingdom_3"),
           (assign, ":troop_of_merchant", "trp_khergit_merchant"),
         (else_try),  
           (eq, ":starting_town_faction", "fac_kingdom_4"),
           (assign, ":troop_of_merchant", "trp_nord_merchant"),
         (else_try),  
           (eq, ":starting_town_faction", "fac_kingdom_5"),
           (assign, ":troop_of_merchant", "trp_rhodok_merchant"),
         (else_try),  
           (eq, ":starting_town_faction", "fac_kingdom_6"),
           (assign, ":troop_of_merchant", "trp_sarranid_merchant"),
         (try_end),
                                     
         (add_visitors_to_current_scene, 3, ":troop_of_merchant", 1, 0),                      
       ]),
       
      (1, 0, ti_once,
       [        
         (eq, "$talked_with_merchant", 1),         
       ],
       [         
         (try_begin),
           (main_hero_fallen),
           (assign, "$g_killed_first_bandit", 0),
         (else_try),  
           (assign, "$g_killed_first_bandit", 1),
         (try_end),

         (finish_mission),
         (assign, "$g_main_attacker_agent", 0),
         (assign, "$talked_with_merchant", 1),  
         
         (assign, "$current_startup_quest_phase", 1),                  
                  
         (change_screen_return),
         (set_trigger_result, 1),
         
         (get_player_agent_no, ":player_agent"),
         (store_agent_hit_points, ":hit_points", ":player_agent"),
         
         (try_begin),
           (lt, ":hit_points", 90),
           (agent_set_hit_points, ":player_agent", 90),
         (try_end),  
       ]),

      (1, 3, ti_once,
       [        
         (main_hero_fallen),         
       ],
       [         
         (try_begin),
           (main_hero_fallen),
           (assign, "$g_killed_first_bandit", 0),
         (else_try),  
           (assign, "$g_killed_first_bandit", 1),
         (try_end),

         (finish_mission),
         (assign, "$g_main_attacker_agent", 0),
         (assign, "$talked_with_merchant", 1),  
         
         (assign, "$current_startup_quest_phase", 1),                  
                  
         (change_screen_return),
         (set_trigger_result, 1),    
         
         (get_player_agent_no, ":player_agent"),
         (store_agent_hit_points, ":hit_points", ":player_agent"),
         
         (try_begin),
           (lt, ":hit_points", 90),
           (agent_set_hit_points, ":player_agent", 90),
         (try_end),                
       ]),
     ]),
     
  (
    "meeting_merchant",0,-1,
    "Meeting with the merchant",
    [
      (0,mtef_team_0,af_override_horse,0,1,[]),
      (1,mtef_visitor_source|mtef_team_0,af_override_horse,0,1,[]),
      (2,mtef_visitor_source|mtef_team_0,af_override_horse,0,1,[]),
      (3,mtef_visitor_source|mtef_team_0,af_override_horse,0,1,[]),
      (4,mtef_visitor_source|mtef_team_0,af_override_horse,0,1,[]),
      (5,mtef_visitor_source|mtef_team_0,af_override_horse,0,1,[]),
      (6,mtef_visitor_source|mtef_team_0,af_override_horse,0,1,[]),
      (7,mtef_visitor_source|mtef_team_0,af_override_horse,0,1,[]),
      (8,mtef_visitor_source|mtef_team_0,af_override_horse,0,1,[]),
      (9,mtef_visitor_source|mtef_team_0,af_override_horse,0,1,[]),
    ],
    [
      (ti_on_agent_spawn, 0, 0, [],
      [              
        (store_trigger_param_1, ":agent_no"),

        (try_begin),
          (agent_get_troop_id, ":troop_no", ":agent_no"),
          (is_between, ":troop_no", "trp_swadian_merchant", "trp_startup_merchants_end"),
          (agent_set_team, ":agent_no", 7),          
          (team_set_relation, 0, 7, 0), 
        (try_end),                
      ]),

      (1, 0, ti_once, [], 
      [
        (assign, "$dialog_with_merchant_ended", 0),
        (store_current_scene, ":cur_scene"),
        (scene_set_slot, ":cur_scene", slot_scene_visited, 1),
        (try_begin),
          (eq, "$sneaked_into_town", 1),
          (call_script, "script_music_set_situation_with_culture", mtf_sit_town_infiltrate),
        (else_try),
          (eq, "$talk_context", tc_tavern_talk),
          (call_script, "script_music_set_situation_with_culture", mtf_sit_tavern),
        (else_try),
          (call_script, "script_music_set_situation_with_culture", mtf_sit_town),
        (try_end),
      ]),
      
      (1, 0, 0, 
      [        
        (assign, ":continue", 0),
        (try_begin),
          (ge, "$dialog_with_merchant_ended", 6),
          (assign, ":continue", 1),
        (else_try),
          (ge, "$dialog_with_merchant_ended", 1),
		  (neg|conversation_screen_is_active),          

          (try_begin),
            (eq, "$dialog_with_merchant_ended", 1),
            (check_quest_active, "qst_collect_men"),
            (tutorial_box, "str_start_up_first_quest", "@Tutorial"),
          (try_end),  

          (val_add, "$dialog_with_merchant_ended", 1),
          (assign, ":continue", 0),
        (try_end),  
        
        (try_begin),
          (conversation_screen_is_active), 
          (tutorial_message, -1),
          (assign, ":continue", 0),
        (try_end),
        
        (eq, ":continue", 1),                        
      ],
      [
        (tutorial_message_set_size, 17, 17),
        (tutorial_message_set_position, 500, 650),
        (tutorial_message_set_center_justify, 0),
        (tutorial_message_set_background, 1),
        (tutorial_message, "str_press_tab_to_exit_from_town"),
      ]),
      	  	
      (ti_before_mission_start, 0, 0, [], 
      [      
        #(call_script, "script_change_banners_and_chest"),
	  ]),

      (ti_inventory_key_pressed, 0, 0, 
      [
        (set_trigger_result, 1),        
      ], []),           
            
      (ti_tab_pressed, 0, 0, 
      [ 
        (try_begin),          
          (gt, "$dialog_with_merchant_ended", 0),          

          (assign, ":max_dist", 0),
          (party_get_position, pos1, "$current_town"),
          (try_for_range, ":unused", 0, 10),
            (map_get_random_position_around_position, pos0, pos1, 2),
            (get_distance_between_positions, ":dist", pos0, pos1),
            (ge, ":dist", ":max_dist"),
            (assign, ":max_dist", ":dist"),
            (copy_position, pos2, pos0),
          (try_end),  
    
          (party_set_position, "p_main_party", pos2),          
                            
          (finish_mission),
          
          (assign, "$current_startup_quest_phase", 2),
          
          (tutorial_message, -1),
          
          (tutorial_message_set_background, 0),
          
          (change_screen_map),
          
          (try_begin),
            (check_quest_finished, "qst_save_town_from_bandits"),
            (assign, "$g_do_one_more_meeting_with_merchant", 1),
          (else_try),  
            #will do this at first spawning in the map          
            (set_spawn_radius, 50),
            (try_for_range, ":unused", 0, 20),
              (spawn_around_party, "p_main_party", "pt_looters"),
            (try_end),          
          (try_end),  

          (set_trigger_result, 1),
        (else_try),
          (display_message, "str_cannot_leave_now"),
        (try_end),
      ], []),
    ]),

  (
    "town_fight",0,-1,
    "Town Fight",
    [
      (0,mtef_scene_source|mtef_team_0,af_override_horse,0,1,[]),
      (1,mtef_scene_source|mtef_team_0,af_override_horse,0,1,[]),
      (2,mtef_visitor_source|mtef_team_0,af_override_horse,0,1,[]),
      (3,mtef_visitor_source|mtef_team_0,af_override_horse,0,1,[]),
      (4,mtef_visitor_source|mtef_team_0,af_override_horse,0,1,[]),
      (5,mtef_visitor_source|mtef_team_0,af_override_horse,0,1,[]),
      (6,mtef_visitor_source|mtef_team_0,af_override_horse,0,1,[]),
      (7,mtef_visitor_source|mtef_team_0,af_override_horse,0,1,[]),          
      (8,mtef_visitor_source|mtef_team_0,af_override_horse,0,1,[]),
      (9,mtef_visitor_source,af_override_horse,0,1,[]),
      (10,mtef_visitor_source,af_override_horse,0,1,[]),
      (11,mtef_visitor_source|mtef_team_1,af_override_horse,0,1,[]),
      (12,mtef_visitor_source|mtef_team_1,af_override_horse,0,1,[]),
      (13,mtef_visitor_source|mtef_team_1,af_override_horse,0,1,[]),
      (14,mtef_visitor_source,af_override_horse,0,1,[]),
      (15,mtef_visitor_source,af_override_horse,0,1,[]),
      (16,mtef_visitor_source,af_override_horse,0,1,[]),
      (17,mtef_visitor_source,af_override_horse,0,1,[]),
      (18,mtef_visitor_source,af_override_horse,0,1,[]),
      (19,mtef_visitor_source,af_override_horse,0,1,[]),
      (20,mtef_visitor_source,af_override_horse,0,1,[]),
      (21,mtef_visitor_source|mtef_team_1,af_override_horse,0,1,[]),
      (22,mtef_visitor_source|mtef_team_1,af_override_horse,0,1,[]),
	  (23,mtef_visitor_source|mtef_team_0,af_override_horse,0,1,[]), #guard
      (24,mtef_visitor_source|mtef_team_0,af_override_horse,0,1,[]), #guard
	  (25,mtef_visitor_source|mtef_team_0,af_override_horse,0,1,[]), #guard
	  (26,mtef_visitor_source|mtef_team_0,af_override_horse,0,1,[]), #guard
	  (27,mtef_visitor_source|mtef_team_0,af_override_horse,0,1,[]), #guard
	  (28,mtef_visitor_source|mtef_team_0,af_override_horse,0,1,[]), #guard
	  (29,mtef_visitor_source,af_override_horse,0,1,[]),
	  (30,mtef_visitor_source,af_override_horse,0,1,[]), 
	  (31,mtef_visitor_source,af_override_horse,0,1,[]), 
      (32,mtef_visitor_source|mtef_team_0,af_override_horse,0,1,[]), #town walker point
	  (33,mtef_visitor_source|mtef_team_0,af_override_horse,0,1,[]), #town walker point
	  (34,mtef_visitor_source|mtef_team_0,af_override_horse,0,1,[]), #town walker point
	  (35,mtef_visitor_source|mtef_team_0,af_override_horse,0,1,[]), #town walker point
	  (36,mtef_visitor_source|mtef_team_0,af_override_horse,0,1,[]), #town walker point
	  (37,mtef_visitor_source|mtef_team_0,af_override_horse,0,1,[]), #town walker point
	  (38,mtef_visitor_source|mtef_team_0,af_override_horse,0,1,[]), #town walker point
	  (39,mtef_visitor_source|mtef_team_0,af_override_horse,0,1,[]), #town walker point
      (40,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]), #in towns, can be used for guard reinforcements
	  (41,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]), #in towns, can be used for guard reinforcements
	  (42,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]), #in towns, can be used for guard reinforcements
	  (43,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]), #in towns, can be used for guard reinforcements
      (44,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
	  (45,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
	  (46,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
	  (47,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
    ],
    [
      common_battle_init_banner,
    
      (ti_on_agent_spawn, 0, 0, [],
      [
        (store_trigger_param_1, ":agent_no"),
        
        (agent_set_team, ":agent_no", 0),
      ]),

      (ti_before_mission_start, 0, 0, [],
      [
        (mission_disable_talk),        
      
        (assign, "$g_main_attacker_agent", 0),
        (set_party_battle_mode),
        
        (assign, "$number_of_bandits_killed_by_player", 0),
        (assign, "$number_of_civilian_loses", 0),
        
        (set_fixed_point_multiplier, 100),
	  ]),
		 
      (1, 0, ti_once, 
      [
        (call_script, "script_init_town_walker_agents"),
      ], 
      []),
      
      (ti_on_agent_killed_or_wounded, 0, 0, [],
      [
        (store_trigger_param_1, ":dead_agent_no"),
        (store_trigger_param_2, ":killer_agent_no"),
        #(store_trigger_param_3, ":is_wounded"),
        
        (try_begin),
          (agent_get_team, ":dead_agent_team_no", ":dead_agent_no"),
          (eq, ":dead_agent_team_no", 1),

          (get_player_agent_no, ":player_agent"),
          (eq, ":player_agent", ":killer_agent_no"),
                
          (val_add, "$number_of_bandits_killed_by_player", 1),
        (else_try),
          (eq, ":dead_agent_team_no", 0),
          
          (val_add, "$number_of_civilian_loses", 1),
        (try_end),  
      ]),
            
      (1, 0, 0, 
      [
        (lt, "$merchant_sign_count", 8),
  	    (val_add, "$merchant_sign_count", 1),
  	    
  	    (try_begin),
  	      (eq, "$merchant_sign_count", 2),
          (get_player_agent_no, ":player_agent"),
  	      (try_for_agents, ":agent_no"),
  	        (agent_get_troop_id, ":agent_troop_id", ":agent_no"),
  	        (ge, ":agent_troop_id", "trp_swadian_merchant"),
  	        (lt, ":agent_troop_id", "trp_startup_merchants_end"),
  	        
  	        (assign, "$g_city_merchant_troop_id", ":agent_troop_id"),
  	        (assign, "$g_city_merchant_agent_id", ":agent_no"),
  	        
  	        (agent_get_position, pos0, ":player_agent"),
  	        (agent_get_position, pos1, ":agent_no"),
  	                    
  	        (assign, ":max_dif", -1000),
            (try_for_range, ":target_entry_point", 0, 64),
              #(neg|entry_point_is_auto_generated, ":target_entry_point"),
              (entry_point_get_position, pos6, ":target_entry_point"),
              (get_distance_between_positions, ":dist_to_player", pos0, pos6),
              (get_distance_between_positions, ":dist_to_merchant", pos1, pos6),
              (store_sub, ":dif", ":dist_to_merchant", ":dist_to_player"),
              (ge, ":dist_to_merchant", 15),
              (ge, ":dif", ":max_dif"),
              (copy_position, pos2, pos6),
              (assign, ":max_dif", ":dif"),
            (try_end),
  	      	    
    	    (agent_set_scripted_destination, ":agent_no", pos2, 0),
            (agent_set_speed_limit, ":agent_no", 10),
          (try_end),
        (else_try),
  	      (eq, "$merchant_sign_count", 5),
  	                 
          (get_player_agent_no, ":player_agent"),
	      (agent_get_position, pos0, ":player_agent"),

  	      (agent_set_scripted_destination, "$g_city_merchant_agent_id", pos0, 0),
          (agent_set_speed_limit, "$g_city_merchant_agent_id", 10),
        (else_try),
  	      (eq, "$merchant_sign_count", 7),
  	      
  	      (agent_clear_scripted_mode, "$g_city_merchant_agent_id"),
  	                 
  	      (assign, "$talk_context", tc_town_talk),
  	      (start_mission_conversation, "$g_city_merchant_troop_id"),  	        	      
  	    (try_end),  	      
  	  ], 
	  []),
	  
	  (1, 0, 0, [],
	  [	  
	    (ge, "$merchant_sign_count", 8),
	   
	    (get_player_agent_no, ":player_agent"),
	    	    
        (try_for_agents, ":agent_no"),
          (neq, ":agent_no", ":player_agent"),
          (agent_is_alive, ":agent_no"),
          (agent_get_team, ":agent_team", ":agent_no"),
          (eq, ":agent_team", 0),
          
          (agent_get_position, pos0, ":agent_no"),
        
          (assign, ":minimum_distance", 10000),  
          (try_for_agents, ":bandit_no"),
            (agent_is_alive, ":bandit_no"),
            (agent_get_team, ":bandit_team", ":bandit_no"),
            (eq, ":bandit_team", 1),
            
            (agent_get_position, pos1, ":bandit_no"),
  
            (get_distance_between_positions, ":dist", pos0, pos1),
            (le, ":dist", ":minimum_distance"),
            (assign, ":minimum_distance", ":dist"),
            (copy_position, pos2, pos1),
          (try_end),
         
          (assign, reg1, ":dist"),
          (try_begin),
            (le, ":minimum_distance", 500),
            (agent_clear_scripted_mode, ":agent_no"),
          (else_try),  
            (lt, ":minimum_distance", 10000),
            (agent_set_scripted_destination, ":agent_no", pos2, 0),
          (try_end),
        (try_end),                  	      
      ]),

      (3, 0, 0, 
      [
        (lt, "$merchant_sign_count", 8),
  	    (call_script, "script_tick_town_walkers")
  	  ], 
	  []),	  	  
	
      (2, 0, 0, 
      [
        (call_script, "script_center_ambiance_sounds")
      ], 
      []),
    
      (ti_before_mission_start, 0, 0, 
      [], 
      [
        (call_script, "script_change_banners_and_chest")
      ]),
        
      (1, 4, ti_once,
       [                  
         (this_or_next|main_hero_fallen),
         (num_active_teams_le, 1),
         
         (ge, "$merchant_sign_count", 8),
       ],
       [         
         (try_begin),
           (main_hero_fallen),
           (assign, "$g_killed_first_bandit", 0),
         (else_try),  
           (assign, "$g_killed_first_bandit", 1),
         (try_end),
         
         (assign, "$current_startup_quest_phase", 4),

         (mission_enable_talk),        

         (finish_mission),         
         
         (unlock_achievement, ACHIEVEMENT_GET_UP_STAND_UP),        
                  
         (change_screen_return),
         (set_trigger_result, 1),         
       ]),

      (ti_inventory_key_pressed, 0, 0,
      [
        (try_begin),
          (eq, "$g_mt_mode", tcm_default),
          (set_trigger_result,1),
        (else_try),
          (eq, "$g_mt_mode", tcm_disguised),
          (display_message,"str_cant_use_inventory_disguised"),
        (else_try),
          (display_message, "str_cant_use_inventory_now"),
        (try_end),
      ], []),
       
      (ti_tab_pressed, 0, 0,
      [
        (display_message, "str_cannot_leave_now"),
      ], []),
  ]),
    
    (
    "multiplayer_duel",mtf_battle_mode,-1, #duel mode
    "You lead your men to battle.",
    [
      (0,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (1,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (2,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (3,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (4,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (5,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (6,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (7,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),

      (8,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (9,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (10,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (11,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (12,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (13,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (14,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (15,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),

      (16,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (17,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (18,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (19,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (20,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (21,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (22,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (23,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),

      (24,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (25,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (26,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (27,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (28,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (29,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (30,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (31,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),

      (32,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (33,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (34,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (35,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (36,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (37,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (38,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (39,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),

      (40,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (41,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (42,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (43,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (44,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (45,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (46,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (47,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),

      (48,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (49,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (50,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (51,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (52,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (53,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (54,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (55,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),

      (56,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (57,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (58,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (59,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (60,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (61,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (62,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (63,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
     ],
    [
      multiplayer_server_check_polls,

      (ti_on_agent_spawn, 0, 0, [],
       [
         (store_trigger_param_1, ":agent_no"),
         (call_script, "script_multiplayer_server_on_agent_spawn_common", ":agent_no"),
         ]),
      
      (ti_server_player_joined, 0, 0, [],
       [
         (store_trigger_param_1, ":player_no"),
         (call_script, "script_multiplayer_server_player_joined_common", ":player_no"),
         ]),

      (ti_before_mission_start, 0, 0, [],
       [
         (assign, "$g_multiplayer_game_type", multiplayer_game_type_duel),
         (call_script, "script_multiplayer_server_before_mission_start_common"),
         #make everyone see themselves as allies, no friendly fire
         (team_set_relation, 0, 0, 1),
         (team_set_relation, 0, 1, 1),
         (team_set_relation, 1, 1, 1),
         (mission_set_duel_mode, 1),
         (call_script, "script_multiplayer_init_mission_variables"),
         (call_script, "script_multiplayer_remove_destroy_mod_targets"),
         (call_script, "script_multiplayer_remove_headquarters_flags"), # close this line and open map in deathmatch mod and use all ladders firstly 
         ]),                                                            # to be able to edit maps without damaging any headquarters flags ext. 

      (ti_after_mission_start, 0, 0, [], 
       [
         (set_spawn_effector_scene_prop_kind, 0, -1), #during this mission, agents of "team 0" will try to spawn around scene props with kind equal to -1(no effector for this mod)
         (set_spawn_effector_scene_prop_kind, 1, -1), #during this mission, agents of "team 1" will try to spawn around scene props with kind equal to -1(no effector for this mod)
         (call_script, "script_initialize_all_scene_prop_slots"),
         (call_script, "script_multiplayer_move_moveable_objects_initial_positions"),
         (assign, "$g_multiplayer_ready_for_spawning_agent", 1),
         ]),

      (ti_on_multiplayer_mission_end, 0, 0, [],
       [
         (call_script, "script_multiplayer_event_mission_end"),
         (assign, "$g_multiplayer_stats_chart_opened_manually", 0),
         (start_presentation, "prsnt_multiplayer_stats_chart_deathmatch"),
         ]),

      (ti_on_agent_killed_or_wounded, 0, 0, [],
       [
         (store_trigger_param_1, ":dead_agent_no"), 
         (store_trigger_param_2, ":killer_agent_no"), 

         (call_script, "script_multiplayer_server_on_agent_killed_or_wounded_common", ":dead_agent_no", ":killer_agent_no"),

         (try_begin),
           (get_player_agent_no, ":player_agent"),
           (agent_is_active, ":player_agent"),
           (agent_slot_ge, ":player_agent", slot_agent_in_duel_with, 0),
           (try_begin),
             (eq, ":dead_agent_no", ":player_agent"),
             (display_message, "str_you_have_lost_a_duel"),
           (else_try),
             (agent_slot_eq, ":player_agent", slot_agent_in_duel_with, ":dead_agent_no"),
             (display_message, "str_you_have_won_a_duel"),
           (try_end),
         (try_end),
         (try_begin),
           (agent_slot_ge, ":dead_agent_no", slot_agent_in_duel_with, 0),
           (agent_get_slot, ":duelist_agent_no", ":dead_agent_no", slot_agent_in_duel_with),
           (agent_set_slot, ":dead_agent_no", slot_agent_in_duel_with, -1),
           (try_begin),
             (agent_is_active, ":duelist_agent_no"),
             (agent_set_slot, ":duelist_agent_no", slot_agent_in_duel_with, -1),
             (agent_clear_relations_with_agents, ":duelist_agent_no"),
             (try_begin),
               (agent_get_player_id, ":duelist_player_no", ":duelist_agent_no"),
               (neg|player_is_active, ":duelist_player_no"), #might be AI
               (agent_force_rethink, ":duelist_agent_no"),
             (try_end),
           (try_end),
         (try_end),
         ]),
      
      (1, 0, 0, [],
       [
         (multiplayer_is_server),
         (get_max_players, ":num_players"),
         (try_for_range, ":player_no", 0, ":num_players"),
           (player_is_active, ":player_no"),
           (neg|player_is_busy_with_menus, ":player_no"),

           (player_get_team_no, ":player_team", ":player_no"), #if player is currently spectator do not spawn his agent
           (lt, ":player_team", multi_team_spectator),

           (player_get_troop_id, ":player_troop", ":player_no"), #if troop is not selected do not spawn his agent
           (ge, ":player_troop", 0),

           (player_get_agent_id, ":player_agent", ":player_no"),
           (assign, ":spawn_new", 0),
           (try_begin),
             (player_get_slot, ":player_first_spawn", ":player_no", slot_player_first_spawn),
             (eq, ":player_first_spawn", 1),
             (assign, ":spawn_new", 1),
             (player_set_slot, ":player_no", slot_player_first_spawn, 0),
           (else_try),
             (try_begin),
               (lt, ":player_agent", 0),
               (assign, ":spawn_new", 1),
             (else_try),
               (neg|agent_is_alive, ":player_agent"),
               (agent_get_time_elapsed_since_removed, ":elapsed_time", ":player_agent"),
               (gt, ":elapsed_time", "$g_multiplayer_respawn_period"),
               (assign, ":spawn_new", 1),
             (try_end),             
           (try_end),
           (eq, ":spawn_new", 1),
           (call_script, "script_multiplayer_buy_agent_equipment", ":player_no"),

           (troop_get_inventory_slot, ":has_item", ":player_troop", ek_horse),
           (try_begin),
             (ge, ":has_item", 0),
             (assign, ":is_horseman", 1),
           (else_try),
             (assign, ":is_horseman", 0),
           (try_end),
         
           (call_script, "script_multiplayer_find_spawn_point", ":player_team", 0, ":is_horseman"), 
           (player_spawn_new_agent, ":player_no", reg0),
         (try_end),
         ]),

      (1, 0, 0, [], #do this in every new frame, but not at the same time
       [
         (multiplayer_is_server),
         (store_mission_timer_a, ":mission_timer"),
         (ge, ":mission_timer", 2),
         (assign, ":team_1_count", 0),
         (assign, ":team_2_count", 0),
         (try_for_agents, ":cur_agent"),
           (agent_is_non_player, ":cur_agent"),
           (agent_is_human, ":cur_agent"),
           (assign, ":will_be_counted", 0),
           (try_begin),
             (agent_is_alive, ":cur_agent"),
             (assign, ":will_be_counted", 1), #alive so will be counted
           (else_try),
             (agent_get_time_elapsed_since_removed, ":elapsed_time", ":cur_agent"),
             (le, ":elapsed_time", "$g_multiplayer_respawn_period"),
             (assign, ":will_be_counted", 1), 
           (try_end),
           (eq, ":will_be_counted", 1),
           (agent_get_team, ":cur_team", ":cur_agent"),
           (try_begin),
             (eq, ":cur_team", 0),
             (val_add, ":team_1_count", 1),
           (else_try),
             (eq, ":cur_team", 1),
             (val_add, ":team_2_count", 1),
           (try_end),
         (try_end),
         (store_sub, "$g_multiplayer_num_bots_required_team_1", "$g_multiplayer_num_bots_team_1", ":team_1_count"),
         (store_sub, "$g_multiplayer_num_bots_required_team_2", "$g_multiplayer_num_bots_team_2", ":team_2_count"),
         (val_max, "$g_multiplayer_num_bots_required_team_1", 0),
         (val_max, "$g_multiplayer_num_bots_required_team_2", 0),
         ]),

      (0, 0, 0, [],
       [
         (multiplayer_is_server),
         (eq, "$g_multiplayer_ready_for_spawning_agent", 1),
         (store_add, ":total_req", "$g_multiplayer_num_bots_required_team_1", "$g_multiplayer_num_bots_required_team_2"),
         (try_begin),
           (gt, ":total_req", 0),
           (store_random_in_range, ":random_req", 0, ":total_req"),
           (val_sub, ":random_req", "$g_multiplayer_num_bots_required_team_1"),
           (try_begin),
             (lt, ":random_req", 0),
             #add to team 1
             (assign, ":selected_team", 0),
             (val_sub, "$g_multiplayer_num_bots_required_team_1", 1),
           (else_try),
             #add to team 2
             (assign, ":selected_team", 1),
             (val_sub, "$g_multiplayer_num_bots_required_team_2", 1),
           (try_end),

           (team_get_faction, ":team_faction_no", ":selected_team"),
           (assign, ":available_troops_in_faction", 0),

           (try_for_range, ":troop_no", multiplayer_ai_troops_begin, multiplayer_ai_troops_end),
             (store_troop_faction, ":troop_faction", ":troop_no"),
             (eq, ":troop_faction", ":team_faction_no"),
             (val_add, ":available_troops_in_faction", 1),
           (try_end),

           (store_random_in_range, ":random_troop_index", 0, ":available_troops_in_faction"),
           (assign, ":end_cond", multiplayer_ai_troops_end),
           (try_for_range, ":troop_no", multiplayer_ai_troops_begin, ":end_cond"),
             (store_troop_faction, ":troop_faction", ":troop_no"),
             (eq, ":troop_faction", ":team_faction_no"),
             (val_sub, ":random_troop_index", 1),
             (lt, ":random_troop_index", 0),
             (assign, ":end_cond", 0),
             (assign, ":selected_troop", ":troop_no"),
           (try_end),
         
           (troop_get_inventory_slot, ":has_item", ":selected_troop", ek_horse),
           (try_begin),
             (ge, ":has_item", 0),
             (assign, ":is_horseman", 1),
           (else_try),
             (assign, ":is_horseman", 0),
           (try_end),

           (call_script, "script_multiplayer_find_spawn_point", ":selected_team", 0, ":is_horseman"), 
           (store_current_scene, ":cur_scene"),
           (modify_visitors_at_site, ":cur_scene"),
           (add_visitors_to_current_scene, reg0, ":selected_troop", 1, ":selected_team", -1),
           (assign, "$g_multiplayer_ready_for_spawning_agent", 0),
         (try_end),
         ]),

      (1, 0, 0, [],
       [
         (multiplayer_is_server),
         #checking for restarting the map
         (assign, ":end_map", 0),
         (try_begin),
           (store_mission_timer_a, ":mission_timer"),
           (store_mul, ":game_max_seconds", "$g_multiplayer_game_max_minutes", 60),
           (gt, ":mission_timer", ":game_max_seconds"),
           (assign, ":end_map", 1),
         (try_end),
         (try_begin),
           (eq, ":end_map", 1),
           (call_script, "script_game_multiplayer_get_game_type_mission_template", "$g_multiplayer_game_type"),
           (start_multiplayer_mission, reg0, "$g_multiplayer_selected_map", 0),
           (call_script, "script_game_set_multiplayer_mission_end"),
         (try_end),
         ]),
        
      (ti_tab_pressed, 0, 0, [],
       [
         (try_begin),
           (eq, "$g_multiplayer_mission_end_screen", 0),
           (assign, "$g_multiplayer_stats_chart_opened_manually", 1),
           (start_presentation, "prsnt_multiplayer_stats_chart_deathmatch"),
         (try_end),
         ]),

      multiplayer_once_at_the_first_frame,
      
      (ti_escape_pressed, 0, 0, [],
       [
         (neg|is_presentation_active, "prsnt_multiplayer_escape_menu"),
         (neg|is_presentation_active, "prsnt_multiplayer_stats_chart_deathmatch"),
         (eq, "$g_waiting_for_confirmation_to_terminate", 0),
         (start_presentation, "prsnt_multiplayer_escape_menu"),
         ]),

      (1, 0, 0, [],
       [
         (store_mission_timer_a, ":mission_timer"),
         (store_sub, ":duel_start_time", ":mission_timer", 3),
         (try_for_agents, ":cur_agent"),
           (agent_slot_ge, ":cur_agent", slot_agent_in_duel_with, 0),
           (agent_get_slot, ":duel_time", ":cur_agent", slot_agent_duel_start_time),
           (ge, ":duel_time", 0),
           (le, ":duel_time", ":duel_start_time"),
           (agent_set_slot, ":cur_agent", slot_agent_duel_start_time, -1),
           (agent_get_slot, ":opponent_agent", ":cur_agent", slot_agent_in_duel_with),
           (agent_is_active, ":opponent_agent"),
           (agent_add_relation_with_agent, ":cur_agent", ":opponent_agent", -1),
           (agent_force_rethink, ":cur_agent"),
         (try_end),
         ]),
      ],
  ),


]
