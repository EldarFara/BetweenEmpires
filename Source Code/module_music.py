from header_music import *

# #######################################################################
#	("track_id", "track_file.type", flags, continue_flags),
#  Each track record contains the following fields:
#  1) Track id: used for referencing tracks.
#  2) Track file: filename of the track
#  3) Track flags. See header_music.py for a list of available flags
#  4) Continue Track flags: Shows in which situations or cultures the track can continue playing. See header_music.py for a list of available flags
# #######################################################################

# WARNING: You MUST add mtf_module_track flag to the flags of the tracks located under module directory

tracks = [

	# #######################################################################
	#	Anyways, I don't actually think any of them are truly hardcoded, 
	#	but better to have three and zero errors. I see no references to
	#	the way music is loaded, so I doubt this increases load time in any
	#	significant way.
	# #######################################################################

    ("bogus", "cant_find_this.ogg", 0, 0),
    ("mount_and_blade_title_screen", "mount_and_blade_title_screen.ogg", mtf_sit_main_title|mtf_start_immediately, 0),
    ("ambushed_by_neutral", "ambushed_by_neutral.ogg", mtf_sit_ambushed|mtf_sit_siege, mtf_sit_fight|mtf_sit_multiplayer_fight),  
]
