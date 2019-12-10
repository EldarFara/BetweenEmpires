import string

dword      = 0x8000000000000000
dword_mask = 0xffffffffffffffff

density_bits      = 32
fkf_density_mask  = 0xFFFF #16K

#terain condition flags
fkf_plain             = 0x00000004
fkf_steppe            = 0x00000008
fkf_snow              = 0x00000010
fkf_desert            = 0x00000020
fkf_plain_forest      = 0x00000400
fkf_steppe_forest     = 0x00000800
fkf_snow_forest       = 0x00001000
fkf_desert_forest     = 0x00002000
fkf_terrain_mask      = 0x0000ffff

fkf_realtime_ligting  = 0x00010000 #deprecated
fkf_point_up          = 0x00020000 #uses auto-generated point-up(quad) geometry for the flora kind
fkf_align_with_ground = 0x00040000 #align the flora object with the ground normal
fkf_grass             = 0x00080000 #is grass
fkf_on_green_ground   = 0x00100000 #populate this flora on green ground
fkf_rock              = 0x00200000 #is rock 
fkf_tree              = 0x00400000 #is tree -> note that if you set this parameter, you should pass additional alternative tree definitions
fkf_snowy             = 0x00800000
fkf_guarantee         = 0x01000000

fkf_speedtree         = 0x02000000  #NOT FUNCTIONAL: we have removed speedtree support on M&B Warband

fkf_has_colony_props  = 0x04000000  # if fkf_has_colony_props -> then you can define colony_radius and colony_treshold of the flora kind


def density(g):
  if (g > fkf_density_mask):
    g = fkf_density_mask
  return ((dword | g) << density_bits)


fauna_kinds = [
("grass",fkf_grass|fkf_on_green_ground|fkf_guarantee|fkf_align_with_ground|fkf_point_up|fkf_plain|fkf_plain_forest|density(1000),[["grass1","0"],["grass2","0"],["grass3","0"],["grass4","0"],["grass5","0"]]),
("bush1",fkf_plain|fkf_plain_forest|fkf_steppe|fkf_steppe_forest|density(0),[["bush1","0"]]),
("bush2",fkf_plain|fkf_plain_forest|fkf_steppe|fkf_steppe_forest|density(0),[["bush2","0"]]),
("bush3",fkf_plain|fkf_plain_forest|fkf_steppe|fkf_steppe_forest|density(0),[["bush3_1","0"], ["bush3_2","0"], ["bush3_3","0"], ["bush3_4","0"], ["bush3_5","0"], ["bush3_6","0"], ["bush3_7","0"]]),
("flower1",fkf_plain|fkf_plain_forest|fkf_steppe|fkf_steppe_forest|density(0),[["flower1_1","0"], ["flower1_2","0"], ["flower1_3","0"]]),
("flower1b",fkf_plain|fkf_plain_forest|fkf_steppe|fkf_steppe_forest|density(0),[["flower1b_1","0"], ["flower1b_2","0"], ["flower1b_3","0"]]),
("flower2",fkf_plain|fkf_plain_forest|fkf_steppe|fkf_steppe_forest|density(0),[["flower2_1","0"]]),
("flower3",fkf_plain|fkf_plain_forest|fkf_steppe|fkf_steppe_forest|density(0),[["flower3_1","0"]]),
("flower4",fkf_plain|fkf_plain_forest|fkf_steppe|fkf_steppe_forest|density(0),[["flower4_1","0"]]),

]


def save_fauna_kinds():
  file = open("./flora_kinds.txt","w")
  file.write("%d\n"%len(fauna_kinds))
  for fauna_kind in fauna_kinds:
    meshes_list = fauna_kind[2]
    file.write("%s %d %d\n"%(fauna_kind[0], (dword_mask & fauna_kind[1]), len(meshes_list)))
    for m in meshes_list:
      file.write(" %s "%(m[0]))
      if (len(m) > 1):
        file.write(" %s\n"%(m[1]))
      else:
        file.write(" 0\n")
      if ( fauna_kind[1] & (fkf_tree|fkf_speedtree) ):  #if this fails make sure that you have entered the alternative tree definition (NOT FUNCTIONAL in Warband)
        speedtree_alternative = m[2]
        file.write(" %s %s\n"%(speedtree_alternative[0], speedtree_alternative[1]))
    if ( fauna_kind[1] & fkf_has_colony_props ):
      file.write(" %s %s\n"%(fauna_kind[3], fauna_kind[4]))
  file.close()

def two_to_pow(x):
  result = 1
  for i in xrange(x):
    result = result * 2
  return result

fauna_mask = 0x80000000000000000000000000000000
low_fauna_mask =             0x8000000000000000
def save_python_header():
  file = open("./fauna_codes.py","w")
  for i_fauna_kind in xrange(len(fauna_kinds)):
    file.write("%s_1 = 0x"%(fauna_kinds[i_fauna_kind][0]))
    file.write("%x\n"%(fauna_mask | two_to_pow(i_fauna_kind)))
    file.write("%s_2 = 0x"%(fauna_kinds[i_fauna_kind][0]))
    file.write("%x\n"%(fauna_mask | ((low_fauna_mask|two_to_pow(i_fauna_kind)) << 64)))
    file.write("%s_3 = 0x"%(fauna_kinds[i_fauna_kind][0]))
    file.write("%x\n"%(fauna_mask | ((low_fauna_mask|two_to_pow(i_fauna_kind)) << 64) | two_to_pow(i_fauna_kind)))
  file.close()

print "Exporting flora data..."
save_fauna_kinds()
