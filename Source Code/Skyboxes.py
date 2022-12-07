sf_day        = 0x00000000
sf_dawn       = 0x00000001
sf_night      = 0x00000002

sf_clouds_0   = 0x00000000
sf_clouds_1   = 0x00000010
sf_clouds_2   = 0x00000020
sf_clouds_3   = 0x00000030

sf_no_shadows = 0x10000000
sf_HDR        = 0x20000000  # this will generate HDR-shaded skyboxes, you should make a LDR version of your skybox for compatibility

# mesh_name, flags, sun_heading, sun_altitude, flare_strength, postfx, sun_color, hemi_color, ambient_color, (fog_start, fog_color),

# to generate new skybox textures with hdr option:
# hdr images are required to generate our RGBE coded skybox images


# To add a skybox, you should first edit this file and put new skyboxes.txt file into the "Data/" folder of your module. 
# The first "mesh_name" parameter is the name of the skybox mesh to be used for that entry. 
# You can check our meshes from the "skyboxes.brf" file with OpenBRF and copy them, 
# just replace the material's textures with yours. And you will also have to change the 
# specular color parameters for correct hdr rendering. of course specular color does not 
# corresponds to specular lighting, those parameters are used as compression values 
# for RGBE decoding and should be generated while you generate RGBE textures. 
# (specular.red = Scale component, specular.green = Bias component) 
# You can check our materials for the instances of this usage. 
#
# For skybox textures, we are using uncompressed *.hdr files to generate *_rgb.dds and *_exp.dds files. 
# its just a RGBE encoding of the skybox for hdr lighting. here is an example: 
# "skybox.dds" -> simple non-hdr (LDR) image, used when you dont use hdr (DXT1 format is good)
# "skybox_rgb.dds" -> RGB components of the HDR image (DXT1 format is preffered)
# "skybox_exp.dds" -> E (exponent) component of the HDR image (L16 format is good, you can use half resolution for this texture)
# We are using our own command line tool to generete those files from "skybox.hdr" image. 
# But you can generate them with some of the hdr-image editors too. The images should be gamma corrected and should not have mipmaps. 
# You can use Photoshop with DDS plug-ins or DirectX Texture Viewer to see the contents of our dds images. 
# 
# ..visit Taleworlds Forums for more information..

skyboxes = [

  ("sky_world_map", sf_day, 179.0, 52.0, 0.85, "pfx_sunny", (1.39*1.32,1.39*1.21,1.39*1.08), (0.0, 0.0, 0.0), (0.96*16.0/255,0.96*23.5/255,0.96*44.5/255), (300, 0xFF8CA2AD)),
]



def save_skyboxes():
  file = open("C:\Users\Lily\Desktop\Between Empires\Between Empires 2.0\Modules\Between Empires\Data\skyboxes.txt","w")
  file.write("%d\n"%len(skyboxes))
  for skybox in  skyboxes:
    file.write("%s %d %f %f %f %s\n"%(skybox[0],skybox[1],skybox[2],skybox[3],skybox[4],skybox[5]))
    file.write(" %f %f %f "%skybox[6])
    file.write(" %f %f %f "%skybox[7])
    file.write(" %f %f %f "%skybox[8])
    file.write(" %f %d\n"%skybox[9])
  file.close()

print "Exporting skyboxes..."
save_skyboxes()
print "Finished."
  
