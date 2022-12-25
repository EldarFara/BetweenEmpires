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
	
  ("invalid_object", 0, "invisible", "0", []),
  ("inventory", sokf_type_container|sokf_place_at_origin, "invisible", "0", []),
  ("empty", 0, "0", "0", []),
  ("chest_a", sokf_type_container, "invisible", "0", []),
  ("container_small_chest", sokf_type_container,"invisible","0", []),
  ("container_chest_b", sokf_type_container, "invisible","0", []),
  ("container_chest_c", sokf_type_container, "invisible", "0", []),
  ("player_chest", sokf_type_container, "invisible", "0", []),
  ("locked_player_chest", 0, "invisible", "0", []),

  ("light_sun",sokf_invisible,"invisible","0",  [
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
  ("light",sokf_invisible,"invisible","0",  [
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
  ("light_red",sokf_invisible,"invisible","0",  [
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
  ("light_night",sokf_invisible,"invisible","0",  [
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
  ("torch",0,"invisible","0",[]),
  ("torch_night",0,"invisible","0",[]),
  ("barrier_20m",sokf_invisible|sokf_type_barrier,"invisible","0", []),
  ("barrier_16m",sokf_invisible|sokf_type_barrier,"invisible","0", []),
  ("barrier_8m" ,sokf_invisible|sokf_type_barrier,"invisible" ,"0" , []),
  ("barrier_4m" ,sokf_invisible|sokf_type_barrier,"invisible" ,"0" , []),
  ("barrier_2m" ,sokf_invisible|sokf_type_barrier,"invisible" ,"0" , []),
  
  ("exit_4m" ,sokf_invisible|sokf_type_barrier_leave,"invisible" ,"0" , []),
  ("exit_8m" ,sokf_invisible|sokf_type_barrier_leave,"invisible" ,"0" , []),
  ("exit_16m" ,sokf_invisible|sokf_type_barrier_leave,"invisible" ,"0" , []),

  ("ai_limiter_2m" ,sokf_invisible|sokf_type_ai_limiter,"invisible" ,"0" , []),
  ("ai_limiter_4m" ,sokf_invisible|sokf_type_ai_limiter,"invisible" ,"0" , []),
  ("ai_limiter_8m" ,sokf_invisible|sokf_type_ai_limiter,"invisible" ,"0" , []),
  ("ai_limiter_16m",sokf_invisible|sokf_type_ai_limiter,"invisible","0", []),

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
("province300",0,"province300","0",[]),
("province301",0,"province301","0",[]),
("province302",0,"province302","0",[]),
("province303",0,"province303","0",[]),
("province304",0,"province304","0",[]),
("province305",0,"province305","0",[]),
("province306",0,"province306","0",[]),
("province307",0,"province307","0",[]),
("province308",0,"province308","0",[]),
("province309",0,"province309","0",[]),
("province310",0,"province310","0",[]),
("province311",0,"province311","0",[]),
("province312",0,"province312","0",[]),
("province313",0,"province313","0",[]),
("province314",0,"province314","0",[]),
("province315",0,"province315","0",[]),
("province316",0,"province316","0",[]),
("province317",0,"province317","0",[]),
("province318",0,"province318","0",[]),
("province319",0,"province319","0",[]),
("province320",0,"province320","0",[]),
("province321",0,"province321","0",[]),
("province322",0,"province322","0",[]),
("province323",0,"province323","0",[]),
("province324",0,"province324","0",[]),
("province325",0,"province325","0",[]),
("province326",0,"province326","0",[]),
("province327",0,"province327","0",[]),
("province328",0,"province328","0",[]),
("province329",0,"province329","0",[]),
("province330",0,"province330","0",[]),
("province331",0,"province331","0",[]),
("province332",0,"province332","0",[]),
("province333",0,"province333","0",[]),
("province334",0,"province334","0",[]),
("province335",0,"province335","0",[]),
("province336",0,"province336","0",[]),
("province337",0,"province337","0",[]),
("province338",0,"province338","0",[]),
("province339",0,"province339","0",[]),
("province340",0,"province340","0",[]),
("province341",0,"province341","0",[]),
("province342",0,"province342","0",[]),
("province343",0,"province343","0",[]),
("province344",0,"province344","0",[]),
("province345",0,"province345","0",[]),
("province346",0,"province346","0",[]),
("province347",0,"province347","0",[]),
("province348",0,"province348","0",[]),
("province349",0,"province349","0",[]),
("province350",0,"province350","0",[]),
("province351",0,"province351","0",[]),
("province352",0,"province352","0",[]),
("province353",0,"province353","0",[]),
("province354",0,"province354","0",[]),
("province355",0,"province355","0",[]),
("province356",0,"province356","0",[]),
("province357",0,"province357","0",[]),
("province358",0,"province358","0",[]),
("province359",0,"province359","0",[]),
("province360",0,"province360","0",[]),
("province361",0,"province361","0",[]),
("province362",0,"province362","0",[]),
("province363",0,"province363","0",[]),
("province364",0,"province364","0",[]),
("province365",0,"province365","0",[]),
("province366",0,"province366","0",[]),
("province367",0,"province367","0",[]),
("province368",0,"province368","0",[]),
("province369",0,"province369","0",[]),
("province370",0,"province370","0",[]),
("province371",0,"province371","0",[]),
("province372",0,"province372","0",[]),
("province373",0,"province373","0",[]),
("province374",0,"province374","0",[]),
("province375",0,"province375","0",[]),
("province376",0,"province376","0",[]),
("province377",0,"province377","0",[]),
("province378",0,"province378","0",[]),
("province379",0,"province379","0",[]),
("province380",0,"province380","0",[]),
("province381",0,"province381","0",[]),
("province382",0,"province382","0",[]),
("province383",0,"province383","0",[]),
("province384",0,"province384","0",[]),
("province385",0,"province385","0",[]),
("province386",0,"province386","0",[]),
("province387",0,"province387","0",[]),
("province388",0,"province388","0",[]),
("province389",0,"province389","0",[]),
("province390",0,"province390","0",[]),
("province391",0,"province391","0",[]),
("province392",0,"province392","0",[]),
("province393",0,"province393","0",[]),
("province394",0,"province394","0",[]),
("province395",0,"province395","0",[]),
("province396",0,"province396","0",[]),
("province397",0,"province397","0",[]),
("province398",0,"province398","0",[]),
("province399",0,"province399","0",[]),
("province400",0,"province400","0",[]),
("province401",0,"province401","0",[]),
("province402",0,"province402","0",[]),
("province403",0,"province403","0",[]),
("province404",0,"province404","0",[]),
("province405",0,"province405","0",[]),
("province406",0,"province406","0",[]),
("province407",0,"province407","0",[]),
("province408",0,"province408","0",[]),
("province409",0,"province409","0",[]),
("province410",0,"province410","0",[]),
("province411",0,"province411","0",[]),
("province412",0,"province412","0",[]),
("province413",0,"province413","0",[]),
("province414",0,"province414","0",[]),
("province415",0,"province415","0",[]),
("province416",0,"province416","0",[]),
("province417",0,"province417","0",[]),
("province418",0,"province418","0",[]),
("province419",0,"province419","0",[]),
("province420",0,"province420","0",[]),
("province421",0,"province421","0",[]),
("province422",0,"province422","0",[]),
("province423",0,"province423","0",[]),
("province424",0,"province424","0",[]),
("province425",0,"province425","0",[]),
("province426",0,"province426","0",[]),
("province427",0,"province427","0",[]),
("province428",0,"province428","0",[]),
("province429",0,"province429","0",[]),
("province430",0,"province430","0",[]),
("province431",0,"province431","0",[]),
("province432",0,"province432","0",[]),
("province433",0,"province433","0",[]),
("province434",0,"province434","0",[]),
("province435",0,"province435","0",[]),
("province436",0,"province436","0",[]),
("province437",0,"province437","0",[]),
("province438",0,"province438","0",[]),
("province439",0,"province439","0",[]),
("province440",0,"province440","0",[]),
("province441",0,"province441","0",[]),
("province442",0,"province442","0",[]),
("province443",0,"province443","0",[]),
("province444",0,"province444","0",[]),
("province445",0,"province445","0",[]),
("province446",0,"province446","0",[]),
("province447",0,"province447","0",[]),
("province448",0,"province448","0",[]),
("province449",0,"province449","0",[]),
("province450",0,"province450","0",[]),
("province451",0,"province451","0",[]),
("province452",0,"province452","0",[]),
("province453",0,"province453","0",[]),
("province454",0,"province454","0",[]),
("province455",0,"province455","0",[]),
("province456",0,"province456","0",[]),
("province457",0,"province457","0",[]),
("province458",0,"province458","0",[]),
("province459",0,"province459","0",[]),
("province460",0,"province460","0",[]),
("province461",0,"province461","0",[]),
("province462",0,"province462","0",[]),
("province463",0,"province463","0",[]),
("province464",0,"province464","0",[]),
("province465",0,"province465","0",[]),
("province466",0,"province466","0",[]),
("province467",0,"province467","0",[]),
("province468",0,"province468","0",[]),
("province469",0,"province469","0",[]),
("province470",0,"province470","0",[]),
("province471",0,"province471","0",[]),
("province472",0,"province472","0",[]),
("province473",0,"province473","0",[]),
("province474",0,"province474","0",[]),
("province475",0,"province475","0",[]),
("province476",0,"province476","0",[]),
("province477",0,"province477","0",[]),
("province478",0,"province478","0",[]),
("province479",0,"province479","0",[]),
("province480",0,"province480","0",[]),
("province481",0,"province481","0",[]),
("province482",0,"province482","0",[]),
("province483",0,"province483","0",[]),
("province484",0,"province484","0",[]),
("province485",0,"province485","0",[]),
("province486",0,"province486","0",[]),
("province487",0,"province487","0",[]),
("province488",0,"province488","0",[]),
("province489",0,"province489","0",[]),
("province490",0,"province490","0",[]),
("province491",0,"province491","0",[]),
("province492",0,"province492","0",[]),
("province493",0,"province493","0",[]),
("province494",0,"province494","0",[]),
("province495",0,"province495","0",[]),
("province496",0,"province496","0",[]),
("province497",0,"province497","0",[]),
("province498",0,"province498","0",[]),
("province499",0,"province499","0",[]),
("province500",0,"province500","0",[]),
("province501",0,"province501","0",[]),
("province502",0,"province502","0",[]),
("province503",0,"province503","0",[]),
("province504",0,"province504","0",[]),
("province505",0,"province505","0",[]),
("province506",0,"province506","0",[]),
("province507",0,"province507","0",[]),
("province508",0,"province508","0",[]),
("province509",0,"province509","0",[]),
("province510",0,"province510","0",[]),
("province511",0,"province511","0",[]),
("province512",0,"province512","0",[]),
("province513",0,"province513","0",[]),
("province514",0,"province514","0",[]),
("province515",0,"province515","0",[]),
("province516",0,"province516","0",[]),
("province517",0,"province517","0",[]),
("province518",0,"province518","0",[]),
("province519",0,"province519","0",[]),
("province520",0,"province520","0",[]),
("province521",0,"province521","0",[]),
("province522",0,"province522","0",[]),
("province523",0,"province523","0",[]),
("province524",0,"province524","0",[]),
("province525",0,"province525","0",[]),
("province526",0,"province526","0",[]),
("province527",0,"province527","0",[]),
("province528",0,"province528","0",[]),
("province529",0,"province529","0",[]),
("province530",0,"province530","0",[]),
("province531",0,"province531","0",[]),
("province532",0,"province532","0",[]),
]
