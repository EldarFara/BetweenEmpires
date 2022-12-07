from header_common import *
from header_scene_props import *
from header_operations import *
from header_triggers import *
from header_sounds import *
from module_constants import *
import string


# #######################################################################
# ("prop_id", flags, "mesh_name", "collider_name", [triggers]),
#
#  Each scene prop record contains the following fields:
#  1) Scene prop id: used for referencing scene props in other files. The prefix spr_ is automatically added before each scene prop id.
#  2) Scene prop flags. See header_scene_props.py for a list of available flags
#  3) Mesh name: Name of the mesh.
#  4) Physics object name:
#  5) Triggers: Simple triggers that are associated with the scene prop
# #######################################################################


scene_props = [

    # #######################################################################
	#	By clearing more scenes, I was able to remove more scene props.
	#	While I'm not confident all these are ~ h a r d c o d e d ~ per se,
	#	but I do find lowering it to this level as pretty pleasing.
	#
	#	You could probably further pair down module.ini by removing a lot
	#	of these mesh references like chest_gothic, torch, etc
    # #######################################################################
	
  ("invalid_object", 0, "question_mark", "0", []),
  ("inventory", sokf_type_container|sokf_place_at_origin, "package", "bobaggage", []),
  ("empty", 0, "0", "0", []),
  ("chest_a", sokf_type_container, "chest_gothic", "bochest_gothic", []),
  ("container_small_chest", sokf_type_container,"package","bobaggage", []),
  ("container_chest_b", sokf_type_container, "chest_b","bo_chest_b", []),
  ("container_chest_c", sokf_type_container, "chest_c", "bo_chest_c", []),
  ("player_chest", sokf_type_container, "player_chest", "bo_player_chest", []),
  ("locked_player_chest", 0, "player_chest", "bo_player_chest", []),

  ("light_sun",sokf_invisible,"light_sphere","0",  [
     (ti_on_init_scene_prop,
      [
          (neg|is_currently_night),
          (store_trigger_param_1, ":prop_instance_no"),
          (set_fixed_point_multiplier, 100),
          (prop_instance_get_scale, pos5, ":prop_instance_no"),
          (position_get_scale_x, ":scale", pos5),
          (store_time_of_day,reg(12)),
          (try_begin),
            (is_between,reg(12),5,20),
            (store_mul, ":red", 5 * 200, ":scale"),
            (store_mul, ":green", 5 * 193, ":scale"),
            (store_mul, ":blue", 5 * 180, ":scale"),
          (else_try),
            (store_mul, ":red", 5 * 90, ":scale"),
            (store_mul, ":green", 5 * 115, ":scale"),
            (store_mul, ":blue", 5 * 150, ":scale"),
          (try_end),
          (val_div, ":red", 100),
          (val_div, ":green", 100),
          (val_div, ":blue", 100),
          (set_current_color,":red", ":green", ":blue"),
          (set_position_delta,0,0,0),
          (add_point_light_to_entity, 0, 0),
      ]),
    ]),
  ("light",sokf_invisible,"light_sphere","0",  [
     (ti_on_init_scene_prop,
      [
          (store_trigger_param_1, ":prop_instance_no"),
          (set_fixed_point_multiplier, 100),
          (prop_instance_get_scale, pos5, ":prop_instance_no"),
          (position_get_scale_x, ":scale", pos5),
          (store_mul, ":red", 3 * 200, ":scale"),
          (store_mul, ":green", 3 * 145, ":scale"),
          (store_mul, ":blue", 3 * 45, ":scale"),
          (val_div, ":red", 100),
          (val_div, ":green", 100),
          (val_div, ":blue", 100),
          (set_current_color,":red", ":green", ":blue"),
          (set_position_delta,0,0,0),
          (add_point_light_to_entity, 10, 30),
      ]),
    ]),
  ("light_red",sokf_invisible,"light_sphere","0",  [
     (ti_on_init_scene_prop,
      [
          (store_trigger_param_1, ":prop_instance_no"),
          (set_fixed_point_multiplier, 100),
          (prop_instance_get_scale, pos5, ":prop_instance_no"),
          (position_get_scale_x, ":scale", pos5),
          (store_mul, ":red", 2 * 170, ":scale"),
          (store_mul, ":green", 2 * 100, ":scale"),
          (store_mul, ":blue", 2 * 30, ":scale"),
          (val_div, ":red", 100),
          (val_div, ":green", 100),
          (val_div, ":blue", 100),
          (set_current_color,":red", ":green", ":blue"),
          (set_position_delta,0,0,0),
          (add_point_light_to_entity, 20, 30),
      ]),
    ]),
  ("light_night",sokf_invisible,"light_sphere","0",  [
     (ti_on_init_scene_prop,
      [
          (is_currently_night, 0),
          (store_trigger_param_1, ":prop_instance_no"),
          (set_fixed_point_multiplier, 100),
          (prop_instance_get_scale, pos5, ":prop_instance_no"),
          (position_get_scale_x, ":scale", pos5),
          (store_mul, ":red", 3 * 160, ":scale"),
          (store_mul, ":green", 3 * 145, ":scale"),
          (store_mul, ":blue", 3 * 100, ":scale"),
          (val_div, ":red", 100),
          (val_div, ":green", 100),
          (val_div, ":blue", 100),
          (set_current_color,":red", ":green", ":blue"),
          (set_position_delta,0,0,0),
          (add_point_light_to_entity, 10, 30),
      ]),
    ]),
  ("torch",0,"torch_a","0",[]),
  ("torch_night",0,"torch_a","0",[]),
  ("barrier_20m",sokf_invisible|sokf_type_barrier,"barrier_20m","bo_barrier_20m", []),
  ("barrier_16m",sokf_invisible|sokf_type_barrier,"barrier_16m","bo_barrier_16m", []),
  ("barrier_8m" ,sokf_invisible|sokf_type_barrier,"barrier_8m" ,"bo_barrier_8m" , []),
  ("barrier_4m" ,sokf_invisible|sokf_type_barrier,"barrier_4m" ,"bo_barrier_4m" , []),
  ("barrier_2m" ,sokf_invisible|sokf_type_barrier,"barrier_2m" ,"bo_barrier_2m" , []),
  
  ("exit_4m" ,sokf_invisible|sokf_type_barrier_leave,"barrier_4m" ,"bo_barrier_4m" , []),
  ("exit_8m" ,sokf_invisible|sokf_type_barrier_leave,"barrier_8m" ,"bo_barrier_8m" , []),
  ("exit_16m" ,sokf_invisible|sokf_type_barrier_leave,"barrier_16m" ,"bo_barrier_16m" , []),

  ("ai_limiter_2m" ,sokf_invisible|sokf_type_ai_limiter,"barrier_2m" ,"bo_barrier_2m" , []),
  ("ai_limiter_4m" ,sokf_invisible|sokf_type_ai_limiter,"barrier_4m" ,"bo_barrier_4m" , []),
  ("ai_limiter_8m" ,sokf_invisible|sokf_type_ai_limiter,"barrier_8m" ,"bo_barrier_8m" , []),
  ("ai_limiter_16m",sokf_invisible|sokf_type_ai_limiter,"barrier_16m","bo_barrier_16m", []),

    # #######################################################################
    # Other 
	# #######################################################################
    
("world_map_base",0,"world_map_base","bo_world_map_base",[]),

("province0",0,"province0","0",[]),
("province1",0,"province1","0",[]),
("province2",0,"province2","0",[]),
("province3",0,"province3","0",[]),
("province4",0,"province4","0",[]),
("province5",0,"province5","0",[]),
("province6",0,"province6","0",[]),
("province7",0,"province7","0",[]),
("province8",0,"province8","0",[]),
("province9",0,"province9","0",[]),
("province10",0,"province10","0",[]),
("province11",0,"province11","0",[]),
("province12",0,"province12","0",[]),
("province13",0,"province13","0",[]),
("province14",0,"province14","0",[]),
("province15",0,"province15","0",[]),
("province16",0,"province16","0",[]),
("province17",0,"province17","0",[]),
("province18",0,"province18","0",[]),
("province19",0,"province19","0",[]),
("province20",0,"province20","0",[]),
("provinces_end",0,"province0","0",[]),
("province21",0,"province21","0",[]),
("province22",0,"province22","0",[]),
("province23",0,"province23","0",[]),
("province24",0,"province24","0",[]),
("province25",0,"province25","0",[]),
("province26",0,"province26","0",[]),
("province27",0,"province27","0",[]),
("province28",0,"province28","0",[]),
("province29",0,"province29","0",[]),
("province30",0,"province30","0",[]),
("province31",0,"province31","0",[]),
("province32",0,"province32","0",[]),
("province33",0,"province33","0",[]),
("province34",0,"province34","0",[]),
("province35",0,"province35","0",[]),
("province36",0,"province36","0",[]),
("province37",0,"province37","0",[]),
("province38",0,"province38","0",[]),
("province39",0,"province39","0",[]),
("province40",0,"province40","0",[]),
("province41",0,"province41","0",[]),
("province42",0,"province42","0",[]),
("province43",0,"province43","0",[]),
("province44",0,"province44","0",[]),
("province45",0,"province45","0",[]),
("province46",0,"province46","0",[]),
("province47",0,"province47","0",[]),
("province48",0,"province48","0",[]),
("province49",0,"province49","0",[]),
("province50",0,"province50","0",[]),
("province51",0,"province51","0",[]),
("province52",0,"province52","0",[]),
("province53",0,"province53","0",[]),
("province54",0,"province54","0",[]),
("province55",0,"province55","0",[]),
("province56",0,"province56","0",[]),
("province57",0,"province57","0",[]),
("province58",0,"province58","0",[]),
("province59",0,"province59","0",[]),
("province60",0,"province60","0",[]),
("province61",0,"province61","0",[]),
("province62",0,"province62","0",[]),
("province63",0,"province63","0",[]),
("province64",0,"province64","0",[]),
("province65",0,"province65","0",[]),
("province66",0,"province66","0",[]),
("province67",0,"province67","0",[]),
("province68",0,"province68","0",[]),
("province69",0,"province69","0",[]),
("province70",0,"province70","0",[]),
("province71",0,"province71","0",[]),
("province72",0,"province72","0",[]),
("province73",0,"province73","0",[]),
("province74",0,"province74","0",[]),
("province75",0,"province75","0",[]),
("province76",0,"province76","0",[]),
("province77",0,"province77","0",[]),
("province78",0,"province78","0",[]),
("province79",0,"province79","0",[]),
("province80",0,"province80","0",[]),
("province81",0,"province81","0",[]),
("province82",0,"province82","0",[]),
("province83",0,"province83","0",[]),
("province84",0,"province84","0",[]),
("province85",0,"province85","0",[]),
("province86",0,"province86","0",[]),
("province87",0,"province87","0",[]),
("province88",0,"province88","0",[]),
("province89",0,"province89","0",[]),
("province90",0,"province90","0",[]),
("province91",0,"province91","0",[]),
("province92",0,"province92","0",[]),
("province93",0,"province93","0",[]),
("province94",0,"province94","0",[]),
("province95",0,"province95","0",[]),
("province96",0,"province96","0",[]),
("province97",0,"province97","0",[]),
("province98",0,"province98","0",[]),
("province99",0,"province99","0",[]),
("province100",0,"province100","0",[]),
("province101",0,"province101","0",[]),
("province102",0,"province102","0",[]),
("province103",0,"province103","0",[]),
("province104",0,"province104","0",[]),
("province105",0,"province105","0",[]),
("province106",0,"province106","0",[]),
("province107",0,"province107","0",[]),
("province108",0,"province108","0",[]),
("province109",0,"province109","0",[]),
("province110",0,"province110","0",[]),
("province111",0,"province111","0",[]),
("province112",0,"province112","0",[]),
("province113",0,"province113","0",[]),
("province114",0,"province114","0",[]),
("province115",0,"province115","0",[]),
("province116",0,"province116","0",[]),
("province117",0,"province117","0",[]),
("province118",0,"province118","0",[]),
("province119",0,"province119","0",[]),
("province120",0,"province120","0",[]),
("province121",0,"province121","0",[]),
("province122",0,"province122","0",[]),
("province123",0,"province123","0",[]),
("province124",0,"province124","0",[]),
("province125",0,"province125","0",[]),
("province126",0,"province126","0",[]),
("province127",0,"province127","0",[]),
("province128",0,"province128","0",[]),
("province129",0,"province129","0",[]),
("province130",0,"province130","0",[]),
("province131",0,"province131","0",[]),
("province132",0,"province132","0",[]),
("province133",0,"province133","0",[]),
("province134",0,"province134","0",[]),
("province135",0,"province135","0",[]),
("province136",0,"province136","0",[]),
("province137",0,"province137","0",[]),
("province138",0,"province138","0",[]),
("province139",0,"province139","0",[]),
("province140",0,"province140","0",[]),
("province141",0,"province141","0",[]),
("province142",0,"province142","0",[]),
("province143",0,"province143","0",[]),
("province144",0,"province144","0",[]),
("province145",0,"province145","0",[]),
("province146",0,"province146","0",[]),
("province147",0,"province147","0",[]),
("province148",0,"province148","0",[]),
("province149",0,"province149","0",[]),
("province150",0,"province150","0",[]),
("province151",0,"province151","0",[]),
("province152",0,"province152","0",[]),
("province153",0,"province153","0",[]),
("province154",0,"province154","0",[]),
("province155",0,"province155","0",[]),
("province156",0,"province156","0",[]),
("province157",0,"province157","0",[]),
("province158",0,"province158","0",[]),
("province159",0,"province159","0",[]),
("province160",0,"province160","0",[]),
("province161",0,"province161","0",[]),
("province162",0,"province162","0",[]),
("province163",0,"province163","0",[]),
("province164",0,"province164","0",[]),
("province165",0,"province165","0",[]),
("province166",0,"province166","0",[]),
("province167",0,"province167","0",[]),
("province168",0,"province168","0",[]),
("province169",0,"province169","0",[]),
("province170",0,"province170","0",[]),
("province171",0,"province171","0",[]),
("province172",0,"province172","0",[]),
("province173",0,"province173","0",[]),
("province174",0,"province174","0",[]),
("province175",0,"province175","0",[]),
("province176",0,"province176","0",[]),
("province177",0,"province177","0",[]),
("province178",0,"province178","0",[]),
("province179",0,"province179","0",[]),
("province180",0,"province180","0",[]),
("province181",0,"province181","0",[]),
("province182",0,"province182","0",[]),
("province183",0,"province183","0",[]),
("province184",0,"province184","0",[]),
("province185",0,"province185","0",[]),
("province186",0,"province186","0",[]),
("province187",0,"province187","0",[]),
("province188",0,"province188","0",[]),
("province189",0,"province189","0",[]),
("province190",0,"province190","0",[]),
("province191",0,"province191","0",[]),
("province192",0,"province192","0",[]),
("province193",0,"province193","0",[]),
("province194",0,"province194","0",[]),
("province195",0,"province195","0",[]),
("province196",0,"province196","0",[]),
("province197",0,"province197","0",[]),
("province198",0,"province198","0",[]),
("province199",0,"province199","0",[]),
("province200",0,"province200","0",[]),
("province201",0,"province201","0",[]),
("province202",0,"province202","0",[]),
("province203",0,"province203","0",[]),
("province204",0,"province204","0",[]),
("province205",0,"province205","0",[]),
("province206",0,"province206","0",[]),
("province207",0,"province207","0",[]),
("province208",0,"province208","0",[]),
("province209",0,"province209","0",[]),
("province210",0,"province210","0",[]),
("province211",0,"province211","0",[]),
("province212",0,"province212","0",[]),
("province213",0,"province213","0",[]),
("province214",0,"province214","0",[]),
("province215",0,"province215","0",[]),
("province216",0,"province216","0",[]),
("province217",0,"province217","0",[]),
("province218",0,"province218","0",[]),
("province219",0,"province219","0",[]),
("province220",0,"province220","0",[]),
("province221",0,"province221","0",[]),
("province222",0,"province222","0",[]),
("province223",0,"province223","0",[]),
("province224",0,"province224","0",[]),
("province225",0,"province225","0",[]),
("province226",0,"province226","0",[]),
("province227",0,"province227","0",[]),
("province228",0,"province228","0",[]),
("province229",0,"province229","0",[]),
("province230",0,"province230","0",[]),
("province231",0,"province231","0",[]),
("province232",0,"province232","0",[]),
("province233",0,"province233","0",[]),
("province234",0,"province234","0",[]),
("province235",0,"province235","0",[]),
("province236",0,"province236","0",[]),
("province237",0,"province237","0",[]),
("province238",0,"province238","0",[]),
("province239",0,"province239","0",[]),
("province240",0,"province240","0",[]),
("province241",0,"province241","0",[]),
("province242",0,"province242","0",[]),
("province243",0,"province243","0",[]),
("province244",0,"province244","0",[]),
("province245",0,"province245","0",[]),
("province246",0,"province246","0",[]),
("province247",0,"province247","0",[]),
("province248",0,"province248","0",[]),
("province249",0,"province249","0",[]),
("province250",0,"province250","0",[]),
("province251",0,"province251","0",[]),
("province252",0,"province252","0",[]),
("province253",0,"province253","0",[]),
("province254",0,"province254","0",[]),
("province255",0,"province255","0",[]),
("province256",0,"province256","0",[]),
("province257",0,"province257","0",[]),
("province258",0,"province258","0",[]),
("province259",0,"province259","0",[]),
("province260",0,"province260","0",[]),
("province261",0,"province261","0",[]),
("province262",0,"province262","0",[]),
("province263",0,"province263","0",[]),
("province264",0,"province264","0",[]),
("province265",0,"province265","0",[]),
("province266",0,"province266","0",[]),
("province267",0,"province267","0",[]),
("province268",0,"province268","0",[]),
("province269",0,"province269","0",[]),
("province270",0,"province270","0",[]),
("province271",0,"province271","0",[]),
("province272",0,"province272","0",[]),
("province273",0,"province273","0",[]),
("province274",0,"province274","0",[]),
("province275",0,"province275","0",[]),
("province276",0,"province276","0",[]),
("province277",0,"province277","0",[]),
("province278",0,"province278","0",[]),
("province279",0,"province279","0",[]),
("province280",0,"province280","0",[]),
("province281",0,"province281","0",[]),
("province282",0,"province282","0",[]),
("province283",0,"province283","0",[]),
("province284",0,"province284","0",[]),
("province285",0,"province285","0",[]),
("province286",0,"province286","0",[]),
("province287",0,"province287","0",[]),
("province288",0,"province288","0",[]),
("province289",0,"province289","0",[]),
("province290",0,"province290","0",[]),
("province291",0,"province291","0",[]),
("province292",0,"province292","0",[]),
("province293",0,"province293","0",[]),
("province294",0,"province294","0",[]),
("province295",0,"province295","0",[]),
("province296",0,"province296","0",[]),
("province297",0,"province297","0",[]),
("province298",0,"province298","0",[]),
("province299",0,"province299","0",[]),
    
]
