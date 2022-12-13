from header_meshes import *

# #######################################################################
# ("mesh_id", flags, "actual_mesh_in_brf_name", x_axis, y_axis, z_axis, x_rot, y_rot, z_rot, x_scale, y_scale, z_scale),
#
#  Each mesh record contains the following fields:
#  1) Mesh id: used for referencing meshes in other files. The prefix mesh_ is automatically added before each mesh id.
#  2) Mesh flags. See header_meshes.py for a list of available flags
#  3) Mesh resource name: Resource name of the mesh
#  4) Mesh translation on x axis: Will be done automatically when the mesh is loaded
#  5) Mesh translation on y axis: Will be done automatically when the mesh is loaded
#  6) Mesh translation on z axis: Will be done automatically when the mesh is loaded
#  7) Mesh rotation angle over x axis: Will be done automatically when the mesh is loaded
#  8) Mesh rotation angle over y axis: Will be done automatically when the mesh is loaded
#  9) Mesh rotation angle over z axis: Will be done automatically when the mesh is loaded
#  10) Mesh x scale: Will be done automatically when the mesh is loaded
#  11) Mesh y scale: Will be done automatically when the mesh is loaded
#  12) Mesh z scale: Will be done automatically when the mesh is loaded
# #######################################################################



meshes = [
	# #######################################################################
	#	The hardcodedness of these two is debateable, but lacking them does
	#	cause rgl_log to print warnings. It defaults to these same two meshes
	#	if they are missing, so it's more of ~warning avoidance system~
	# #######################################################################
	("main_menu_background", -0x00000001, "main_menu_nord", 0, 0, 0, 0, 0, 0, 1, 1, 1),
	("loading_background", 0, "load_screen_2", 0, 0, 0, 0, 0, 0, 1, 1, 1),
    
    
("black_dot", 0, "black_dot", 0, 0, 0, 0, 0, 0, 1, 1, 1),
("ui_background", 0, "ui_background", 0, 0, 0, 0, 0, 0, 1, 1, 1),
]
