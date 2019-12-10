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

#0-23 - sf_clouds_0, 24-64 - sf_clouds_1, 61-100 - sf_clouds_2, rain - sf_clouds_3

sun_color_clear = (3.9/1.15, 3.5/1.15, 1.8/1.15)
sun_color_cloudy = (2.7/1.15, 2.4/1.15, 1.6/1.15)
sun_color_clear_evening = (3.9/2, 3.5/2, 1.8/2)
sun_color_cloudy_evening = (3.9/2.3, 3.5/2.3, 1.8/2.3)
sun_color_clear_dusk = (0.5/4.3, 0.75/4.3, 0.98/1.4)
sun_color_cloudy_dusk = (0.5/5, 0.75/5, 0.98/1.8)
sun_color_night = (0, 0.16, 0.55)
ambient_color_clear = (0.16, 0.23, 0.39)
ambient_color_cloudy = (0.08, 0.12, 0.14)
ambient_color_clear_evening = (0.16/2, 0.23/2, 0.39/2)
ambient_color_cloudy_evening = (0.16/2.3, 0.23/2.3, 0.39/2.3)
ambient_color_clear_dusk = (0.16/4, 0.23/4, 0.39/3)
ambient_color_cloudy_dusk = (0.16/4.5, 0.23/4.5, 0.39/3.8)
ambient_color_night = (0, 0.007, 0.025)

skyboxes = [
  ("sky1_day", sf_HDR, 0, 50, 1, "pfx_sunny", sun_color_clear, (0, 0, 0), ambient_color_clear, (0, 0xFF97B6CC)),
  
  ("sky1_day", sf_day|sf_clouds_0|sf_HDR, 0, 50, 1, "pfx_sunny", sun_color_clear, (0, 0, 0), ambient_color_clear, (0, 0xFF97B6CC)),
  ("sky2_day", sf_day|sf_clouds_0|sf_HDR, 0, 50, 1, "pfx_sunny", sun_color_clear, (0, 0, 0), ambient_color_clear, (0, 0xFF97B6CC)),
  ("sky3_day", sf_day|sf_clouds_0|sf_HDR, 0, 50, 1, "pfx_sunny", sun_color_clear, (0, 0, 0), ambient_color_clear, (0, 0xFF97B6CC)),
  ("sky4_day", sf_day|sf_clouds_0|sf_HDR, 0, 50, 1, "pfx_sunny", sun_color_clear, (0, 0, 0), ambient_color_clear, (0, 0xFF97CFE5)),
  ("sky5_day", sf_day|sf_clouds_0|sf_no_shadows|sf_HDR, 0, 50, 0, "pfx_cloudy", sun_color_cloudy, (0, 0, 0), ambient_color_cloudy, (0, 0xFF78828C)),
  ("sky6_day", sf_day|sf_clouds_0|sf_HDR, 0, 50, 1, "pfx_sunny", sun_color_clear, (0, 0, 0), ambient_color_clear, (0, 0xFF79a8cb)),
  ("sky7_day", sf_day|sf_clouds_1|sf_no_shadows|sf_HDR, 0, 50, 0, "pfx_cloudy", sun_color_cloudy, (0, 0, 0), ambient_color_cloudy, (0, 0xFF78828C)),
  ("sky8_day", sf_day|sf_clouds_1|sf_HDR, 0, 50, 1, "pfx_sunny", sun_color_clear, (0, 0, 0), ambient_color_clear, (0, 0xFF86B5D2)),
  ("sky9_day", sf_day|sf_clouds_1|sf_no_shadows|sf_HDR, 0, 50, 0, "pfx_heavy_cloudy", sun_color_cloudy, (0, 0, 0), ambient_color_cloudy, (0, 0xFF78828C)),
  ("sky10_day", sf_day|sf_clouds_1|sf_no_shadows|sf_HDR, 0, 50, 0, "pfx_heavy_cloudy", sun_color_cloudy, (0, 0, 0), ambient_color_cloudy, (0, 0xFF78828C)),
  ("sky11_day", sf_day|sf_clouds_1|sf_no_shadows|sf_HDR, 0, 50, 0, "pfx_cloudy", sun_color_cloudy, (0, 0, 0), ambient_color_cloudy, (0, 0xFF555C63)),
  ("sky12_day", sf_day|sf_clouds_1|sf_no_shadows|sf_HDR, 0, 50, 0, "pfx_heavy_cloudy", sun_color_cloudy, (0, 0, 0), ambient_color_cloudy, (0, 0xFF78828C)),
  ("sky13_day", sf_day|sf_clouds_2|sf_no_shadows|sf_HDR, 0, 50, 0, "pfx_heavy_cloudy", sun_color_cloudy, (0, 0, 0), ambient_color_cloudy, (0, 0xFF5c6870)),
  ("sky14_day", sf_day|sf_clouds_2|sf_no_shadows|sf_HDR, 0, 50, 0, "pfx_heavy_cloudy", sun_color_cloudy, (0, 0, 0), ambient_color_cloudy, (0, 0xFF7E9EC6)),
  ("sky15_day", sf_day|sf_clouds_3|sf_no_shadows|sf_HDR, 0, 50, 0, "pfx_heavy_cloudy_dark", sun_color_cloudy, (0, 0, 0), ambient_color_cloudy, (0, 0xFF383D43)),
  ("sky16_day", sf_day|sf_clouds_3|sf_no_shadows|sf_HDR, 0, 50, 0, "pfx_heavy_cloudy_dark", sun_color_cloudy, (0, 0, 0), ambient_color_cloudy, (0, 0xFF393E48)),
  ("sky17_day", sf_day|sf_clouds_3|sf_HDR, 0, 50, 1, "pfx_sunny", sun_color_clear, (0, 0, 0), ambient_color_clear, (0, 0xFF84B3DE)),
  ("sky18_day", sf_day|sf_clouds_3|sf_no_shadows|sf_HDR, 0, 50, 0, "pfx_cloudy", sun_color_cloudy, (0, 0, 0), ambient_color_cloudy, (0, 0xFF555C63)),
  ("sky19_night", sf_night|sf_clouds_0|sf_no_shadows|sf_HDR, 0, 35, 0, "pfx_night", sun_color_night, (0, 0, 0), ambient_color_night, (400, 0xFF1E1E1E)),
  ("sky20_night", sf_night|sf_clouds_1|sf_no_shadows|sf_HDR, 0, 35, 0, "pfx_night", sun_color_night, (0, 0, 0), ambient_color_night, (400, 0xFF1E1E1E)),
  ("sky21_night", sf_night|sf_clouds_2|sf_no_shadows|sf_HDR, 0, 35, 0, "pfx_night", sun_color_night, (0, 0, 0), ambient_color_night, (400, 0xFF1E1E1E)),
  ("sky22_night", sf_night|sf_clouds_2|sf_no_shadows|sf_HDR, 0, 51, 0, "pfx_night", sun_color_night, (0, 0, 0), ambient_color_night, (400, 0xFF1E1E1E)),
  ("sky23_night", sf_night|sf_clouds_3|sf_no_shadows|sf_HDR, 0, 51, 0, "pfx_night", sun_color_night, (0, 0, 0), ambient_color_night, (400, 0xFF1E1E1E)),
  ("sky24_sunset", sf_dawn|sf_clouds_0|sf_HDR, 0, 12, 0.7, "pfx_sunset_dark", (3.467742/1.8, 1.129032/1.8, 0.096774/1.8), (0, 0, 0), (0.070588/1.8, 0.098039/1.8, 0.176471/1.8), (300, 0xFF3C3332)),
  ("sky25_sunset", sf_dawn|sf_clouds_0|sf_HDR, 0, 12, 0.7, "pfx_sunset", (3.467742, 1.129032, 0.096774), (0, 0, 0), (0.070588, 0.098039, 0.176471), (300, 0xFF3C3332)),
  ("sky26_sunset", sf_dawn|sf_clouds_0|sf_HDR, 0, 12, 0.7, "pfx_sunset_dark", (3.467742/1.8, 1.129032/1.8, 0.096774/1.8), (0, 0, 0), (0.070588/1.8, 0.098039/1.8, 0.176471/1.8), (300, 0xFF3C3332)),
  ("sky27_sunset", sf_dawn|sf_clouds_1|sf_HDR, 0, 12, 0.7, "pfx_sunset_dark", (3.467742/1.8, 1.129032/1.8, 0.096774/1.8), (0, 0, 0), (0.070588/1.8, 0.098039/1.8, 0.176471/1.8), (300, 0xFF3C3332)),
  ("sky28_sunset", sf_dawn|sf_clouds_2|sf_HDR, 0, 12, 0.7, "pfx_sunset", (3.467742, 1.129032, 0.096774), (0, 0, 0), (0.070588, 0.098039, 0.176471), (300, 0xFF3C3332)),
  ("sky29_sunset", sf_dawn|sf_clouds_0|sf_HDR, 0, 12, 0.7, "pfx_sunset", (3.467742, 1.129032, 0.096774), (0, 0, 0), (0.070588, 0.098039, 0.176471), (300, 0xFF3C3332)),
  ("sky30_sunset", sf_dawn|sf_clouds_0|sf_HDR, 0, 12, 0.7, "pfx_sunset_dark", (3.467742/1.8, 1.129032/1.8, 0.096774/1.8), (0, 0, 0), (0.070588/1.8, 0.098039/1.8, 0.176471/1.8), (300, 0xFF3C3332)),
  ("sky31_sunset", sf_dawn|sf_clouds_3|sf_HDR, 0, 12, 0, "pfx_sunset_dark", (3.467742/1.8, 1.129032/1.8, 0.096774/1.8), (0, 0, 0), (0.070588/1.8, 0.098039/1.8, 0.176471/1.8), (300, 0xFF3C3332)),
  ("sky32_evening", sf_day|sf_clouds_3|sf_HDR, 0, 40, 1, "pfx_evening_clear", sun_color_clear_evening, (0, 0, 0), ambient_color_clear_evening, (0, 0xFF4f687a)),
  ("sky33_evening", sf_day|sf_clouds_3|sf_HDR, 0, 40, 1, "pfx_evening_clear", sun_color_clear_evening, (0, 0, 0), ambient_color_clear_evening, (0, 0xFF4f687a)),
  ("sky34_evening", sf_day|sf_clouds_3|sf_HDR, 0, 40, 1, "pfx_evening_clear", sun_color_clear_evening, (0, 0, 0), ambient_color_clear_evening, (0, 0xFF56717e)),
  ("sky35_evening", sf_day|sf_clouds_3|sf_HDR, 0, 40, 1, "pfx_evening_clear", sun_color_clear_evening, (0, 0, 0), ambient_color_clear_evening, (0, 0xFF4f687a)),
  ("sky36_evening", sf_day|sf_clouds_3|sf_no_shadows|sf_HDR, 0, 40, 0, "pfx_evening_cloudy", sun_color_cloudy_evening, (0, 0, 0), ambient_color_cloudy_evening, (0, 0xFF4b5f77)),
  ("sky37_evening", sf_day|sf_clouds_3|sf_no_shadows|sf_HDR, 0, 40, 0, "pfx_evening_cloudy", sun_color_cloudy_evening, (0, 0, 0), ambient_color_cloudy_evening, (0, 0xFF485c72)),
  ("sky38_dusk", sf_night|sf_clouds_3|sf_no_shadows|sf_HDR, 0, 50, 0, "pfx_dusk_clear", sun_color_clear_dusk, (0, 0, 0), ambient_color_clear_dusk, (0, 0xFF2a3036)),
  ("sky39_dusk", sf_night|sf_clouds_3|sf_no_shadows|sf_HDR, 0, 50, 0, "pfx_dusk_cloudy", sun_color_cloudy_dusk, (0, 0, 0), ambient_color_cloudy_dusk, (0, 0xFF2a3036)),
  ("sky40_dusk", sf_night|sf_clouds_3|sf_no_shadows|sf_HDR, 0, 50, 0, "pfx_dusk_clear", sun_color_clear_dusk, (0, 0, 0), ambient_color_clear_dusk, (0, 0xFF1f2a3b)),
  ("sky41_day", sf_day|sf_clouds_3|sf_no_shadows|sf_HDR, 0, 50, 0, "pfx_heavy_cloudy", sun_color_cloudy, (0, 0, 0), ambient_color_cloudy, (0, 0xFF7d8383)),
  ("sky42_evening", sf_day|sf_clouds_3|sf_no_shadows|sf_HDR, 0, 40, 0, "pfx_evening_cloudy", sun_color_cloudy_evening, (0, 0, 0), ambient_color_cloudy_evening, (0, 0xFF4b5f77)),
  ("sky43_dusk", sf_night|sf_clouds_3|sf_no_shadows|sf_HDR, 0, 0, 0, "pfx_dusk_cloudy", sun_color_cloudy_dusk, (0, 0, 0), ambient_color_cloudy_dusk, (0, 0xFF2a3036)),
  ("sky44_evening", sf_day|sf_clouds_3|sf_HDR, 0, 40, 1, "pfx_evening_cloudy", sun_color_clear_evening, (0, 0, 0), ambient_color_clear_evening, (0, 0xFF455263)),
  ("sky45_dusk", sf_night|sf_clouds_3|sf_no_shadows|sf_HDR, 0, 50, 0, "pfx_dusk_cloudy", sun_color_clear_dusk, (0, 0, 0), ambient_color_clear_dusk, (0, 0xFF28323b)),

]



def save_skyboxes():
  file = open("./skyboxes.txt","w")
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
  
