///////////////////////////////////////////////////////////////////////////////////
//
// SHADERS FOR VIKING CONQUEST
// LA_GRANDMASTER
//
//
///////////////////////////////////////////////////////////////////////////////////
// APOLOGIES IN ADVANCE - DUE TO THE RUSH OF THE LAST FEW DAYS THIS HAS BECOME A BIT MESSY 
// IT WILL BE TIDIED UP BY ME AS I GO ALONG BUG FIXING
//
///////////////////////////////////////////////////////////////////////////////////
//
//
//
// Mount&Blade Warband Shaders
// You can add edit main shaders and lighting system with this file.
// You cannot change fx_configuration.h file since it holds application dependent 
// configration parameters. Sorry its not well documented. 
// Please send your feedbacks to our forums.
//
// All rights reserved.
// www.taleworlds.com
//
//
///////////////////////////////////////////////////////////////////////////////////
// compile_fx.bat:
// ------------------------------
// @echo off
// fxc /D PS_2_X=ps_2_a /T fx_2_0 /Fo mb_2a.fxo mb.fx
// fxc /D PS_2_X=ps_2_b /T fx_2_0 /Fo mb_2b.fxo mb.fx
// pause>nul
///////////////////////////////////////////////////////////////////////////////////


#if !defined (PS_2_X)
	#error "define high quality shader profile: PS_2_X ( ps_2_b or ps_2_a )"
#endif

#include "fx_configuration.h"	// source code dependent configration definitions..

////////////////////////////////////////////////////////////////////////////////
//definitions: 
#define NUM_LIGHTS					10
#define NUM_SIMUL_LIGHTS			4
#define NUM_WORLD_MATRICES			32

#define PCF_NONE					0
#define PCF_DEFAULT					1
#define PCF_NVIDIA					2


#define INCLUDE_VERTEX_LIGHTING
#define VERTEX_LIGHTING_SCALER   1.0f	//used for diffuse calculation
#define VERTEX_LIGHTING_SPECULAR_SCALER   1.0f

#define USE_PRECOMPILED_SHADER_LISTS


//put this to un-reachable code blocks..
#define GIVE_ERROR_HERE {for(int i = 0; i < 1000; i++)		{Output.RGBColor *= Output.RGBColor;}}
#define GIVE_ERROR_HERE_VS {for(int i = 0; i < 1000; i++)		{Out.Pos *= Out.Pos;}}

//#define NO_GAMMA_CORRECTIONS

#ifdef NO_GAMMA_CORRECTIONS
	#define INPUT_TEX_GAMMA(col_rgb) (col_rgb) = (col_rgb)
	#define INPUT_OUTPUT_GAMMA(col_rgb) (col_rgb) = (col_rgb)
	#define OUTPUT_GAMMA(col_rgb) (col_rgb) = (col_rgb)
#else
	#define INPUT_TEX_GAMMA(col_rgb) (col_rgb) = pow((col_rgb), input_gamma.x) 
	#define INPUT_OUTPUT_GAMMA(col_rgb) (col_rgb) = pow((col_rgb), output_gamma.x) 
	#define OUTPUT_GAMMA(col_rgb) (col_rgb) = pow((col_rgb), output_gamma_inv.x) 
#endif
	
#ifdef DONT_INIT_OUTPUTS
	#pragma warning( disable : 4000)
	#define INITIALIZE_OUTPUT(structure, var)	structure var;
#else
	#define INITIALIZE_OUTPUT(structure, var)	structure var = (structure)0;
#endif

#pragma warning( disable : 3571)	//pow(f,e)


//Categories..
#define OUTPUT_STRUCTURES
#define FUNCTIONS

//Constant categories
#define PER_MESH_CONSTANTS
#define PER_FRAME_CONSTANTS
#define PER_SCENE_CONSTANTS
#define APPLICATION_CONSTANTS

//Shader categories
#define MISC_SHADERS
#define UI_SHADERS
#define SHADOW_RELATED_SHADERS
#define WATER_SHADERS
#define SKYBOX_SHADERS
#define HAIR_SHADERS
#define FACE_SHADERS
#define FLORA_SHADERS
#define MAP_SHADERS
#define SOFT_PARTICLE_SHADERS
#define STANDART_SHADERS
#define STANDART_RELATED_SHADER
#define OCEAN_SHADERS
#ifdef USE_NEW_TREE_SYSTEM
#define NEWTREE_SHADERS
#endif

/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#ifdef PER_MESH_CONSTANTS
	float4x4 matWorldViewProj;
	float4x4 matWorldView;
	float4x4 matWorld;

	float4x4 matWaterWorldViewProj;
	float4x4 matWorldArray[NUM_WORLD_MATRICES] : WORLDMATRIXARRAY;
	//float4   matBoneOriginArray[NUM_WORLD_MATRICES];

	float4 vMaterialColor = float4(255.f/255.f, 230.f/255.f, 200.f/255.f, 1.0f);
	float4 vMaterialColor2;
	float fMaterialPower = 16.f;
	float4 vSpecularColor = float4(5, 5, 5, 5);
	float4 texture_offset = {0,0,0,0};

	int iLightPointCount;
	int	   iLightIndices[NUM_SIMUL_LIGHTS] = { 0, 1, 2, 3 };
	
	bool bUseMotionBlur = false;
	float4x4 matMotionBlur;
#endif

////////////////////////////////////////
#ifdef PER_FRAME_CONSTANTS
	float time_var = 0.0f;
	float4x4 matWaterViewProj;
	

#endif

////////////////////////////////////////
#ifdef PER_SCENE_CONSTANTS
	float vTimer = 0.0f;
	
	float vSeason = 1.0f;
	
	
	
	
//WAVE CONSTANTS
	float4 vWaveInfo = 0.0;
	float4 vWaveOrigin = 0.0;
	
//WIND VARIABLES
	float vWindStrength = 0.01f;
	float vWindDirection = 0.01f;
//
	float fFogDensity = 0.05f;

	float3 vSkyLightDir;
	float4 vSkyLightColor;
	float3 vSunDir;
	float4 vSunColor;
	
	float4 vAmbientColor = float4(64.f/255.f, 64.f/255.f, 64.f/255.f, 1.0f);
	float4 vGroundAmbientColor = float4(84.f/255.f, 44.f/255.f, 54.f/255.f, 1.0f);

	float4 vCameraPos;
	float4x4 matSunViewProj;
	float4x4 matView;
	float4x4 matViewProj;
	
	float3 vLightPosDir[NUM_LIGHTS];
	float4 vLightDiffuse[NUM_LIGHTS];
	float4 vPointLightColor;	//agerage color of lights
	
	float reflection_factor;
#endif

////////////////////////////////////////
#ifdef APPLICATION_CONSTANTS
	bool use_depth_effects = false;
	float far_clip_Inv;
	float4 vDepthRT_HalfPixel_ViewportSizeInv;

	float fShadowMapNextPixel = 1.0f / 4096;
	float fShadowMapSize = 4096;

	static const float input_gamma = 2.2f;
	float4 output_gamma = float4(2.2f, 2.2f, 2.2f, 2.2f);			//STR: float4 yapyldy
	float4 output_gamma_inv = float4(1.0f / 2.2f, 1.0f / 2.2f, 1.0f / 2.2f, 1.0f / 2.2f);

	float4 debug_vector = {0,0,0,1};
	
	float spec_coef = 1.0f;	//valid value after module_data!
	
	
	static const float map_normal_detail_factor = 1.4f;
	static const float uv_2_scale = 1.237;
	static const float fShadowBias = 0.00002f;//-0.000002f;
	
	#ifdef USE_NEW_TREE_SYSTEM
		float flora_detail = 40.0f;
		#define flora_detail_fade 		(flora_detail*FLORA_DETAIL_FADE_MUL)
		#define flora_detail_fade_inv 	(flora_detail-flora_detail_fade)
		#define flora_detail_clip 		(max(0,flora_detail_fade - 20.0f))
	#endif

#endif

/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// Texture&Samplers
#if defined(USE_SHARED_DIFFUSE_MAP) || !defined(USE_DEVICE_TEXTURE_ASSIGN)
	texture diffuse_texture;
#endif

#ifndef USE_DEVICE_TEXTURE_ASSIGN
	texture diffuse_texture_2;
	texture specular_texture;
	texture normal_texture;
	texture env_texture;
	texture shadowmap_texture;

	texture cubic_texture;
	
	texture depth_texture;
	texture screen_texture;

	#ifdef USE_REGISTERED_SAMPLERS
	sampler ReflectionTextureSampler 	: register(fx_ReflectionTextureSampler_RegisterS 		) = sampler_state	{  Texture = env_texture;		}; 
	sampler EnvTextureSampler			: register(fx_EnvTextureSampler_RegisterS				) = sampler_state	{  Texture = env_texture;		}; 
	sampler Diffuse2Sampler 			: register(fx_Diffuse2Sampler_RegisterS 				) = sampler_state	{  Texture = diffuse_texture_2;	}; 
	sampler NormalTextureSampler		: register(fx_NormalTextureSampler_RegisterS			) = sampler_state	{  Texture = normal_texture;	}; 
	sampler SpecularTextureSampler 		: register(fx_SpecularTextureSampler_RegisterS 			) = sampler_state	{  Texture = specular_texture;	}; 
	sampler DepthTextureSampler 		: register(fx_DepthTextureSampler_RegisterS 			) = sampler_state	{  Texture = depth_texture;	    }; 
	sampler CubicTextureSampler 		: register(fx_CubicTextureSampler_RegisterS 			) = sampler_state	{  Texture = cubic_texture;	    }; 
	sampler ShadowmapTextureSampler 	: register(fx_ShadowmapTextureSampler_RegisterS 		) = sampler_state	{  Texture = shadowmap_texture;	};
	sampler ScreenTextureSampler 		: register(fx_ScreenTextureSampler_RegisterS			) = sampler_state	{  Texture = screen_texture;	};
	sampler MeshTextureSampler 			: register(fx_MeshTextureSampler_RegisterS 				) = sampler_state	{  Texture = diffuse_texture;	}; 
	sampler ClampedTextureSampler 		: register(fx_ClampedTextureSampler_RegisterS 			) = sampler_state	{  Texture = diffuse_texture;	}; 
	sampler FontTextureSampler 			: register(fx_FontTextureSampler_RegisterS 				) = sampler_state	{  Texture = diffuse_texture;	}; 
	sampler CharacterShadowTextureSampler:register(fx_CharacterShadowTextureSampler_RegisterS	) = sampler_state	{  Texture = diffuse_texture;	}; 
	sampler MeshTextureSamplerNoFilter 	: register(fx_MeshTextureSamplerNoFilter_RegisterS 		) = sampler_state	{  Texture = diffuse_texture;	}; 
	sampler DiffuseTextureSamplerNoWrap : register(fx_DiffuseTextureSamplerNoWrap_RegisterS 	) = sampler_state	{  Texture = diffuse_texture;	};
	sampler GrassTextureSampler 		: register(fx_GrassTextureSampler_RegisterS 			) = sampler_state	{  Texture = diffuse_texture;	}; 
	#else 
	
	
	sampler ReflectionTextureSampler 	= sampler_state	{  Texture = env_texture;		AddressU = CLAMP; AddressV = CLAMP; MinFilter = LINEAR; MagFilter = LINEAR;	}; 
	sampler EnvTextureSampler			= sampler_state	{  Texture = env_texture;		AddressU = WRAP;  AddressV = WRAP;  MinFilter = LINEAR; MagFilter = LINEAR;	}; 
	sampler Diffuse2Sampler 			= sampler_state	{  Texture = diffuse_texture_2;	AddressU = WRAP; AddressV = WRAP; MinFilter = LINEAR; MagFilter = LINEAR;	}; 
	sampler NormalTextureSampler		= sampler_state	{  Texture = normal_texture;	AddressU = WRAP; AddressV = WRAP; MinFilter = LINEAR; MagFilter = LINEAR;	}; 
	sampler SpecularTextureSampler 		= sampler_state	{  Texture = specular_texture;	AddressU = WRAP; AddressV = WRAP; MinFilter = LINEAR; MagFilter = LINEAR;	}; 
	sampler DepthTextureSampler 		= sampler_state	{  Texture = depth_texture;		AddressU = CLAMP; AddressV = CLAMP; MinFilter = LINEAR; MagFilter = LINEAR;    }; 
	sampler CubicTextureSampler 		= sampler_state	{  Texture = cubic_texture;	 	AddressU = CLAMP; AddressV = CLAMP; MinFilter = LINEAR; MagFilter = LINEAR;   }; 
	sampler ShadowmapTextureSampler 	= sampler_state	{  Texture = shadowmap_texture;	AddressU = CLAMP; AddressV = CLAMP; MinFilter = NONE; MagFilter = NONE;	};
	sampler ScreenTextureSampler 		= sampler_state	{  Texture = screen_texture;	AddressU = CLAMP; AddressV = CLAMP; MinFilter = LINEAR; MagFilter = LINEAR;	};
	sampler MeshTextureSampler 			= sampler_state	{  Texture = diffuse_texture;	AddressU = WRAP; AddressV = WRAP; MinFilter = LINEAR; MagFilter = LINEAR;	}; 
	sampler ClampedTextureSampler 		= sampler_state	{  Texture = diffuse_texture;	AddressU = CLAMP; AddressV = CLAMP; MinFilter = LINEAR; MagFilter = LINEAR;	}; 
	sampler FontTextureSampler 			= sampler_state	{  Texture = diffuse_texture;	AddressU = WRAP; AddressV = WRAP; MinFilter = LINEAR; MagFilter = LINEAR;	}; 
	sampler CharacterShadowTextureSampler= sampler_state	{  Texture = diffuse_texture;	AddressU = BORDER; AddressV = BORDER; MinFilter = LINEAR; MagFilter = LINEAR;	}; 
	sampler MeshTextureSamplerNoFilter 	= sampler_state	{  Texture = diffuse_texture;	AddressU = WRAP; AddressV = WRAP; MinFilter = NONE; MagFilter = NONE;	}; 
	sampler DiffuseTextureSamplerNoWrap = sampler_state	{  Texture = diffuse_texture;	AddressU = CLAMP; AddressV = CLAMP; MinFilter = LINEAR; MagFilter = LINEAR;	};
	sampler GrassTextureSampler 		= sampler_state	{  Texture = diffuse_texture;	AddressU = CLAMP; AddressV = CLAMP; MinFilter = LINEAR; MagFilter = LINEAR;	}; 
	
	#endif
	
#else 

	sampler ReflectionTextureSampler 	: register(fx_ReflectionTextureSampler_RegisterS 		); 
	sampler EnvTextureSampler			: register(fx_EnvTextureSampler_RegisterS				); 
	sampler Diffuse2Sampler 			: register(fx_Diffuse2Sampler_RegisterS 				); 
	sampler NormalTextureSampler		: register(fx_NormalTextureSampler_RegisterS			); 
	sampler SpecularTextureSampler 		: register(fx_SpecularTextureSampler_RegisterS 			); 
	sampler DepthTextureSampler 		: register(fx_DepthTextureSampler_RegisterS 			);  
	sampler DepthTextureSampler 		: register(fx_CubicTextureSampler_RegisterS 			);
	sampler ShadowmapTextureSampler 	: register(fx_ShadowmapTextureSampler_RegisterS 		);
	sampler ScreenTextureSampler 		: register(fx_ScreenTextureSampler_RegisterS			);
		
	#ifdef USE_SHARED_DIFFUSE_MAP
		sampler MeshTextureSampler 			: register(fx_MeshTextureSampler_RegisterS 				) = sampler_state	{  Texture = diffuse_texture;	}; 
		sampler ClampedTextureSampler 		: register(fx_ClampedTextureSampler_RegisterS 			) = sampler_state	{  Texture = diffuse_texture;	}; 
		sampler FontTextureSampler 			: register(fx_FontTextureSampler_RegisterS 				) = sampler_state	{  Texture = diffuse_texture;	}; 
		sampler CharacterShadowTextureSampler:register(fx_CharacterShadowTextureSampler_RegisterS	) = sampler_state	{  Texture = diffuse_texture;	}; 
		sampler MeshTextureSamplerNoFilter 	: register(fx_MeshTextureSamplerNoFilter_RegisterS 		) = sampler_state	{  Texture = diffuse_texture;	}; 
		sampler DiffuseTextureSamplerNoWrap : register(fx_DiffuseTextureSamplerNoWrap_RegisterS 	) = sampler_state	{  Texture = diffuse_texture;	};
		sampler GrassTextureSampler 		: register(fx_GrassTextureSampler_RegisterS 			) = sampler_state	{  Texture = diffuse_texture;	}; 
	#else   
		sampler MeshTextureSampler 			: register(fx_MeshTextureSampler_RegisterS 				); 
		sampler ClampedTextureSampler 		: register(fx_ClampedTextureSampler_RegisterS 			); 
		sampler FontTextureSampler 			: register(fx_FontTextureSampler_RegisterS 				); 
		sampler CharacterShadowTextureSampler:register(fx_CharacterShadowTextureSampler_RegisterS	); 
		sampler MeshTextureSamplerNoFilter 	: register(fx_MeshTextureSamplerNoFilter_RegisterS 		); 
		sampler DiffuseTextureSamplerNoWrap : register(fx_DiffuseTextureSamplerNoWrap_RegisterS 	);
		sampler GrassTextureSampler 		: register(fx_GrassTextureSampler_RegisterS 			); 
	#endif
#endif

/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#ifdef OUTPUT_STRUCTURES

struct PS_OUTPUT
{
	float4 RGBColor : COLOR;
};

#endif

/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#ifdef FUNCTIONS

//WAVE&OCEAN FUNCTIONS
float GetTimer(float e)
{	
	return vTimer * (10*e); 
}

float4 GetWaveInfo()
{	
	return vWaveInfo; 
}

float4 GetWaveOrigin()
{	
	return vWaveOrigin; 
}


float GetSeason()
{	
	//float Season = 3;//vSeason +1;
	return vSeason; 
}

float GetSeasonWindFactor()	//!
{	
	if ((vSeason > 2.5)) //3= winter
	{
		return 0.25f;
	}
	return 1.0f;
}


//ROTATE 
float2 rotatevector (float2 originalvector, float d)
{
	float radians = d * 0.0174532925; //convert degrees to radians
	//ROTATE
	float2 newvector;
	newvector.x = (cos(radians)*originalvector.x) - (sin(radians)*originalvector.y);
	newvector.y = (sin(radians)*originalvector.x) + (cos(radians)*originalvector.y);
	return newvector;
}




//GET WIND FUNCTIONS
float GetWindAmount(float e)
{	
	float wind = vWindStrength * e; 
	wind = max(1.5,wind);

	return wind; 
}

float GetWindAmountNew(float e, float position_z)
{	
	float wind = vWindStrength * e; 
	wind = max(1.5,wind);

	float z_factor = clamp(position_z * 0.03 - 0.01, 0.0, 0.5);
	
	return wind * z_factor; //!
}

float GetWindDirection(float e)
{	
	return vWindDirection * e; 
}
/////////////////


float GetSunAmount(uniform const int PcfMode, float4 ShadowTexCoord, float2 ShadowTexelPos)
{
	float sun_amount;
	if (PcfMode == PCF_NVIDIA)
	{
		//sun_amount = tex2D(ShadowmapTextureSampler, ShadowTexCoord).r;
		sun_amount = tex2Dproj(ShadowmapTextureSampler, ShadowTexCoord).r;
	}
	else
	{
		float2 lerps = frac(ShadowTexelPos);
		//read in bilerp stamp, doing the shadow checks
		float sourcevals[4];
		sourcevals[0] = (tex2D(ShadowmapTextureSampler, ShadowTexCoord.xy).r < ShadowTexCoord.z)? 0.0f: 1.0f;
		sourcevals[1] = (tex2D(ShadowmapTextureSampler, ShadowTexCoord.xy + float2(fShadowMapNextPixel, 0)).r < ShadowTexCoord.z)? 0.0f: 1.0f;
		sourcevals[2] = (tex2D(ShadowmapTextureSampler, ShadowTexCoord.xy + float2(0, fShadowMapNextPixel)).r < ShadowTexCoord.z)? 0.0f: 1.0f;
		sourcevals[3] = (tex2D(ShadowmapTextureSampler, ShadowTexCoord.xy + float2(fShadowMapNextPixel, fShadowMapNextPixel)).r < ShadowTexCoord.z)? 0.0f: 1.0f;

		// lerp between the shadow values to calculate our light amount
		sun_amount = lerp(lerp(sourcevals[0], sourcevals[1], lerps.x), lerp(sourcevals[2], sourcevals[3], lerps.x), lerps.y);
	}
	return sun_amount;
}

////////////////////////////////////////
float get_fog_amount(float d)
{
	//return 1/(d * fFogDensity * 20);
	//   return saturate((fFogEnd - d) / (fFogEnd - fFogStart));
	return 1.0f / exp2(d * fFogDensity);
	//return 1.0f / exp ((d * fFogDensity) * (d * fFogDensity));
}

float get_fog_amount_new(float d, float wz)
{
	//you can implement world.z based algorithms here
	return get_fog_amount(d);
}

////////////////////////////////////////
static const float2 specularShift = float2(0.138 - 0.5, 0.254 - 0.5);
static const float2 specularExp = float2(256.0, 32.0)*0.7;
static const float3 specularColor0 = float3(0.9, 1.0, 1.0)*0.898 * 0.99;
static const float3 specularColor1 = float3(1.0, 0.9, 1.0)*0.74 * 0.99;

float HairSingleSpecularTerm(float3 T, float3 H, float exponent)
{
    float dotTH = dot(T, H);
    float sinTH = sqrt(1.0 - dotTH*dotTH);
    return pow(sinTH, exponent);
}

float3 ShiftTangent(float3 T, float3 N, float shiftAmount)
{
    return normalize(T + shiftAmount * N);
}

float3 calculate_hair_specular(float3 normal, float3 tangent, float3 lightVec, float3 viewVec, float2 tc)
{
	// shift tangents
	float shiftTex = tex2D(Diffuse2Sampler, tc).a;
	
	float3 T1 = ShiftTangent(tangent, normal, specularShift.x + shiftTex);
	float3 T2 = ShiftTangent(tangent, normal, specularShift.y + shiftTex);

	float3 H = normalize(lightVec + viewVec);
	float3 specular = vSunColor.rgb * specularColor0 * HairSingleSpecularTerm(T1, H, specularExp.x);
	float3 specular2 = vSunColor.rgb * specularColor1 * HairSingleSpecularTerm(T2, H, specularExp.y);
	float specularMask = tex2D(Diffuse2Sampler, tc * 10.0f).a;	// modulate secondary specular term with noise
	specular2 *= specularMask;
	float specularAttenuation = saturate(1.75 * dot(normal, lightVec) + 0.25);
	specular = (specular + specular2) * specularAttenuation;
	
	return specular;
}

float HairDiffuseTerm(float3 N, float3 L)
{
    return saturate(0.75 * dot(N, L) + 0.25);
}

float face_NdotL(float3 n, float3 l) 
{

	float wNdotL = dot(n.xyz, l.xyz);
	return saturate(max(0.2f * (wNdotL + 0.9f),wNdotL));
}

float4 calculate_point_lights_diffuse(const float3 vWorldPos, const float3 vWorldN, const bool face_like_NdotL, const bool exclude_0) 
{
	const int exclude_index = 0;
	
	float4 total = 0;
	for(int j = 0; j < iLightPointCount; j++)
	{
		if(!exclude_0 || j != exclude_index)
		{
			int i = iLightIndices[j];
			float3 point_to_light = vLightPosDir[i]-vWorldPos;
			float LD = dot(point_to_light, point_to_light);
			float3 L = normalize(point_to_light);
			float wNdotL = dot(vWorldN, L);
			
			float fAtten = VERTEX_LIGHTING_SCALER / LD;
			//compute diffuse color
			if(face_like_NdotL) {
				total += max(0.2f * (wNdotL + 0.9f), wNdotL) * vLightDiffuse[i] * fAtten;
			}
			else {
				total += saturate(wNdotL) * vLightDiffuse[i] * fAtten;
	}
		}
	}
	return total;
}

float4 calculate_point_lights_specular(const float3 vWorldPos, const float3 vWorldN, const float3 vWorldView, const bool exclude_0)
{
	//const int exclude_index = 0;
	
	float4 total = 0;
	for(int i = 0; i < iLightPointCount; i++)
	{
		//if(!exclude_0 || j != exclude_index)	//commenting out exclude_0 will introduce double effect of light0, but prevents loop bug of fxc
		{
			//int i = iLightIndices[j];
			float3 point_to_light = vLightPosDir[i]-vWorldPos;
			float LD = dot(point_to_light, point_to_light);
			float3 L = normalize(point_to_light);
					
			float fAtten = VERTEX_LIGHTING_SPECULAR_SCALER / LD;
				
			float3 vHalf = normalize( vWorldView + L );
			total += fAtten * vLightDiffuse[i] * pow( saturate(dot(vHalf, vWorldN)), fMaterialPower); 
		}
	}
	return total;
}


float4 get_ambientTerm( int ambientTermType, float3 normal, float3 DirToSky, float sun_amount )
{
	float4 ambientTerm;
	if(ambientTermType == 0)	//constant
	{
		ambientTerm = vAmbientColor;
	}
	else if(ambientTermType == 1)	//hemisphere
	{
		float4 g_vGroundColorTEMP = vGroundAmbientColor * sun_amount;
		float4 g_vSkyColorTEMP = vAmbientColor;
		
		float lerpFactor = (dot(normal, DirToSky) + 1.0f) * 0.5f;
		
		float4 hemiColor = lerp( g_vGroundColorTEMP, g_vSkyColorTEMP, lerpFactor);
		ambientTerm = hemiColor;
	}
	else //if(ambientTermType == 2)	//ambient cube 
	{
		float4 cubeColor = texCUBE(CubicTextureSampler, normal);
		ambientTerm = vAmbientColor * cubeColor;
	}
	return ambientTerm;
}

float4x4 build_instance_frame_matrix(float3 vInstanceData0, float3 vInstanceData1, float3 vInstanceData2, float3 vInstanceData3) 
{
	const float3 position = vInstanceData0.xyz;
	//const float  scale = vInstanceData0.w;
	
	
	float3 frame_s = vInstanceData1;
	float3 frame_f = vInstanceData2;
	float3 frame_u = vInstanceData3;//cross(frame_s, frame_f);;
	
	float4x4 matWorldOfInstance  = {float4(frame_s.x, frame_f.x, frame_u.x, position.x ), 
									float4(frame_s.y, frame_f.y, frame_u.y, position.y ), 
									float4(frame_s.z, frame_f.z, frame_u.z, position.z ), 
									float4(0.0f, 0.0f, 0.0f, 1.0f )  };

	return matWorldOfInstance;
}


float4 skinning_deform(float4 vPosition, float4 vBlendWeights, float4 vBlendIndices )
{
	return 	  mul(matWorldArray[vBlendIndices.x], vPosition /*- matBoneOriginArray[vBlendIndices.x]*/) * vBlendWeights.x
			+ mul(matWorldArray[vBlendIndices.y], vPosition /*- matBoneOriginArray[vBlendIndices.y]*/) * vBlendWeights.y
			+ mul(matWorldArray[vBlendIndices.z], vPosition /*- matBoneOriginArray[vBlendIndices.z]*/) * vBlendWeights.z
			+ mul(matWorldArray[vBlendIndices.w], vPosition /*- matBoneOriginArray[vBlendIndices.w]*/) * vBlendWeights.w;
}


#define DEFINE_TECHNIQUES(tech_name, vs_name, ps_name)	\
				technique tech_name	\
				{ pass P0 { VertexShader = compile vs_2_0 vs_name(PCF_NONE); \
							PixelShader = compile PS_2_X ps_name(PCF_NONE);} } \
				technique tech_name##_SHDW	\
				{ pass P0 { VertexShader = compile vs_2_0 vs_name(PCF_DEFAULT); \
							PixelShader = compile PS_2_X ps_name(PCF_DEFAULT);} } \
				technique tech_name##_SHDWNVIDIA	\
				{ pass P0 { VertexShader = compile vs_2_0 vs_name(PCF_NVIDIA); \
							PixelShader = compile PS_2_X ps_name(PCF_NVIDIA);} } 

#endif

/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

#define	DEFINE_LIGHTING_TECHNIQUE(tech_name, use_dxt5, use_bumpmap, use_skinning, use_specularfactor, use_specularmap)
							

/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#ifdef MISC_SHADERS	//notexture, clear_floating_point_buffer, diffuse_no_shadow, simple_shading, simple_shading_no_filter, no_shading, no_shading_no_alpha

//shared vs_font
struct VS_OUTPUT_FONT
{
	float4 Pos					: POSITION;
	float  Fog				    : FOG;
	
	float4 Color				: COLOR0;
	float2 Tex0					: TEXCOORD0;
};
VS_OUTPUT_FONT vs_font(float4 vPosition : POSITION, float4 vColor : COLOR, float2 tc : TEXCOORD0)
{
	VS_OUTPUT_FONT Out;

	Out.Pos = mul(matWorldViewProj, vPosition);

	float3 P = mul(matWorldView, vPosition).xyz; //position in view space

	Out.Tex0 = tc;
	Out.Color = vColor * vMaterialColor;

	//apply fog
	float d = length(P);
	float4 vWorldPos = (float4)mul(matWorld,vPosition);
	Out.Fog = get_fog_amount_new(d, vWorldPos.z);

	return Out;
}
VertexShader vs_font_compiled_2_0 = compile vs_2_0 vs_font();

//---
struct VS_OUTPUT_NOTEXTURE
{
	float4 Pos           : POSITION;
	float4 Color         : COLOR0;
	float  Fog           : FOG;
};
VS_OUTPUT_NOTEXTURE vs_main_notexture(float4 vPosition : POSITION, float4 vColor : COLOR)
{
	VS_OUTPUT_NOTEXTURE Out;

	Out.Pos = mul(matWorldViewProj, vPosition);
	Out.Color = vColor * vMaterialColor;
	float3 P = mul(matWorldView, vPosition).xyz; //position in view space
	//apply fog
	float d = length(P);
	float4 vWorldPos = (float4)mul(matWorld,vPosition);
	Out.Fog = get_fog_amount_new(d, vWorldPos.z);

	return Out;
}
PS_OUTPUT ps_main_notexture( VS_OUTPUT_NOTEXTURE In ) 
{ 
	PS_OUTPUT Output;
	Output.RGBColor = In.Color;
	return Output;
}
technique notexture
{
	pass P0
	{
		VertexShader = compile vs_2_0 vs_main_notexture();
		PixelShader = compile ps_2_0 ps_main_notexture();
	}
}

//---
struct VS_OUTPUT_CLEAR_FLOATING_POINT_BUFFER
{
	float4 Pos			: POSITION;
};
VS_OUTPUT_CLEAR_FLOATING_POINT_BUFFER vs_clear_floating_point_buffer(float4 vPosition : POSITION)
{
	VS_OUTPUT_CLEAR_FLOATING_POINT_BUFFER Out;

	Out.Pos = mul(matWorldViewProj, vPosition);

	return Out;
}
PS_OUTPUT ps_clear_floating_point_buffer()
{
	PS_OUTPUT Out;
	Out.RGBColor = float4(0.0f, 0.0f, 0.0f, 0.0f);
	return Out;
}
technique clear_floating_point_buffer
{
	pass P0
	{
		VertexShader = compile vs_2_0 vs_clear_floating_point_buffer();
		PixelShader = compile ps_2_0 ps_clear_floating_point_buffer();
	}
}

//---
struct VS_OUTPUT_FONT_X
{
	float4 Pos					: POSITION;
	float4 Color					: COLOR0;
	float2 Tex0					: TEXCOORD0;
	float  Fog				    : FOG;
};

VS_OUTPUT_FONT_X vs_main_no_shadow(float4 vPosition : POSITION, float3 vNormal : NORMAL, float2 tc : TEXCOORD0, float4 vColor : COLOR0, float4 vLightColor : COLOR1)
{
	VS_OUTPUT_FONT_X Out;

	Out.Pos = mul(matWorldViewProj, vPosition);

	float4 vWorldPos = (float4)mul(matWorld,vPosition);
	float3 vWorldN = normalize(mul((float3x3)matWorld, vNormal)); //normal in world space
	float3 P = mul(matWorldView, vPosition).xyz; //position in view space

	Out.Tex0 = tc;

	float4 diffuse_light = vAmbientColor + vLightColor;
	diffuse_light += saturate(dot(vWorldN, -vSkyLightDir)) * vSkyLightColor;
	diffuse_light += saturate(dot(vWorldN, -vSunDir)) * vSunColor;
	Out.Color = (vMaterialColor * vColor * diffuse_light);

	//apply fog
	float d = length(P);

	Out.Fog = get_fog_amount_new(d, vWorldPos.z);

	return Out;
}

PS_OUTPUT ps_main_no_shadow(VS_OUTPUT_FONT_X In) 
{ 
	PS_OUTPUT Output;
	float4 tex_col = tex2D(MeshTextureSampler, In.Tex0);
	INPUT_TEX_GAMMA(tex_col.rgb);
	Output.RGBColor =  In.Color * tex_col;
	OUTPUT_GAMMA(Output.RGBColor.rgb);
	return Output;
}

PS_OUTPUT ps_main_no_shadow_season(VS_OUTPUT_FONT_X In) 
{ 
	PS_OUTPUT Output;
	float4 tex_col = tex2D(MeshTextureSampler, In.Tex0);
		
	INPUT_TEX_GAMMA(tex_col.rgb);
	
	float season = GetSeason();
	
	if (season < 0.5) //0= spring
	{
		tex_col.rgb *= float3(0.9,1.1,0.9);
	}
	else if ((season > 0.5)&&(season < 1.5)) //1= summer
	{
		tex_col.rgb *= float3(1.0,1.0,1.0);
	}
	else if ((season > 1.5)&&(season < 2.5)) //2= autumn
	{
		tex_col.rgb *= float3(1.1,0.9,0.9);
	}
	else if ((season > 2.5)) //3= winter
	{
		tex_col = tex2D(SpecularTextureSampler, In.Tex0);
	}
////
	
	

	Output.RGBColor =  In.Color * tex_col;
	OUTPUT_GAMMA(Output.RGBColor.rgb);
	return Output;
}



struct VS_OUTPUT_FONT_X_BUMP
{
	float4 Pos					: POSITION;
	//float4 Color				: COLOR0;
	float2 Tex0					: TEXCOORD0;
	float3 SkyDir				: TEXCOORD1;
	float3 SunDir				: TEXCOORD2;
	float4 vColor				: TEXCOORD3;
	float  Fog				    : FOG;
};


VS_OUTPUT_FONT_X_BUMP vs_main_no_shadow_bump(float4 vPosition : POSITION, float3 vNormal : NORMAL, float2 tc : TEXCOORD0, float4 vColor : COLOR0, float3 vTangent : TANGENT, float3 vBinormal : BINORMAL)
{
	VS_OUTPUT_FONT_X_BUMP Out;

	Out.Pos = mul(matWorldViewProj, vPosition);

	float4 vWorldPos = (float4)mul(matWorld,vPosition);
	float3 vWorldN = normalize(mul((float3x3)matWorld, vNormal)); //normal in world space

	float3 vWorld_binormal = normalize(mul((float3x3)matWorld, vBinormal)); //normal in world space
	float3 vWorld_tangent  = normalize(mul((float3x3)matWorld, vTangent)); //normal in world space

	float3x3 TBNMatrix = float3x3(vWorld_tangent, vWorld_binormal, vWorldN); 

	Out.Tex0 = tc;
	
	Out.SkyDir = mul(TBNMatrix, -vSkyLightDir);
	Out.SunDir = mul(TBNMatrix, -vSunDir);
	Out.vColor = vColor;

	//apply fog
	float3 P = mul(matWorldView, vPosition).xyz; //position in view space
	float d = length(P);

	Out.Fog = get_fog_amount_new(d, vWorldPos.z);

	return Out;
}

PS_OUTPUT ps_main_no_shadow_season_bump(VS_OUTPUT_FONT_X_BUMP In) 
{ 
	PS_OUTPUT Output;
	float4 tex_col = tex2D(MeshTextureSampler, In.Tex0);
		
	INPUT_TEX_GAMMA(tex_col.rgb);
	
	float3 normal = (2.0f * tex2D(NormalTextureSampler, In.Tex0).rgb - 1.0f);
	float3 sky_light_dir = In.SkyDir;
	float3 sun_dir = In.SunDir;
	float4 vColor = In.vColor;
	
	//computation copy from vertex shader
	float4 Out_Color;
	{
		float lighting_factor = 1.0f;
		float4 diffuse_light = vAmbientColor;
		diffuse_light += saturate(dot(normal, sky_light_dir)) * vSkyLightColor * lighting_factor;
		diffuse_light += saturate(dot(normal, sun_dir)) * vSunColor * lighting_factor;
		Out_Color = saturate(vMaterialColor * vColor * diffuse_light);
	}
	
	float4 In_Color = Out_Color;
	
	float season = GetSeason();
	
	if (season < 0.5) //0= spring
	{
		tex_col.rgb *= float3(0.9,1.1,0.9);
	}
	else if ((season > 0.5)&&(season < 1.5)) //1= summer
	{
		tex_col.rgb *= float3(1.0,1.0,1.0);
	}
	else if ((season > 1.5)&&(season < 2.5)) //2= autumn
	{
		tex_col.rgb *= float3(1.1,0.9,0.9);
	}
	else if ((season > 2.5)) //3= winter
	{
		tex_col = tex2D(SpecularTextureSampler, In.Tex0);
	}
	

	Output.RGBColor =  In_Color * tex_col;
	OUTPUT_GAMMA(Output.RGBColor.rgb);
	
	return Output;
}

PS_OUTPUT ps_simple_no_filtering(VS_OUTPUT_FONT_X In) 
{ 
	PS_OUTPUT Output;
	float4 tex_col = tex2D(MeshTextureSamplerNoFilter, In.Tex0);
	INPUT_TEX_GAMMA(tex_col.rgb);
	Output.RGBColor =  In.Color * tex_col;
	OUTPUT_GAMMA(Output.RGBColor.rgb);
	return Output;
}
PS_OUTPUT ps_no_shading(VS_OUTPUT_FONT In) 
{ 
	PS_OUTPUT Output;
	Output.RGBColor =  In.Color;
	//Output.RGBColor *= tex2D(DiffuseTextureSamplerNoWrap, In.Tex0);
	Output.RGBColor *= tex2D(MeshTextureSampler, In.Tex0);
	
//	Output.RGBColor = float4(1,0,0,1);
	return Output;
}
PS_OUTPUT ps_no_shading_no_alpha(VS_OUTPUT_FONT In) 
{ 
	PS_OUTPUT Output;
	Output.RGBColor =  In.Color;
	Output.RGBColor *= tex2D(MeshTextureSamplerNoFilter, In.Tex0);
	Output.RGBColor.a = 1.0f;
	return Output;
}

technique diffuse_no_shadow
{
	pass P0
	{
		VertexShader = compile vs_2_0 vs_main_no_shadow();
		PixelShader = compile ps_2_0 ps_main_no_shadow();
	}
}

technique diffuse_no_shadow_season //Uses gamma 
{
	pass P0
	{
		VertexShader = compile vs_2_0  vs_main_no_shadow();
		PixelShader = compile ps_2_0 ps_main_no_shadow_season();
	}
}

technique diffuse_no_shadow_season_bump //Uses gamma 
{
	pass P0
	{
		// VertexShader = compile vs_2_0  vs_main_no_shadow();
		// PixelShader = compile ps_2_0 ps_main_no_shadow_season();
		VertexShader = compile vs_2_0  vs_main_no_shadow_bump();
		PixelShader = compile ps_2_0 ps_main_no_shadow_season_bump();
	}
}

technique simple_shading //Uses gamma
{
	pass P0
	{
		VertexShader = vs_font_compiled_2_0;
		PixelShader = compile ps_2_0 ps_main_no_shadow();
	}
}


technique simple_shading_season //Uses gamma
{
	pass P0
	{
		VertexShader = vs_font_compiled_2_0;
		PixelShader = compile ps_2_0 ps_main_no_shadow_season();
	}
}

technique simple_shading_no_filter //Uses gamma
{
	pass P0
	{
		VertexShader = vs_font_compiled_2_0;
		PixelShader = compile ps_2_0 ps_simple_no_filtering();
	}
}
technique no_shading
{
	pass P0
	{
		VertexShader = vs_font_compiled_2_0;
		PixelShader = compile ps_2_0 ps_no_shading();
	}
}
technique no_shading_no_alpha
{
	pass P0
	{
		VertexShader = vs_font_compiled_2_0;
		PixelShader = compile ps_2_0 ps_no_shading_no_alpha();
	}
}

#endif

///////////////////////////////////////////////
#ifdef UI_SHADERS
PS_OUTPUT ps_font_uniform_color(VS_OUTPUT_FONT In) 
{ 
	PS_OUTPUT Output;
	Output.RGBColor =  In.Color;
	Output.RGBColor.a *= tex2D(FontTextureSampler, In.Tex0).a;
	return Output;
}
PS_OUTPUT ps_font_background(VS_OUTPUT_FONT In) 
{ 
	PS_OUTPUT Output;
	Output.RGBColor.a = 1.0f; //In.Color.a;
	Output.RGBColor.rgb = tex2D(FontTextureSampler, In.Tex0).rgb + In.Color.rgb;
	//	Output.RGBColor.rgb += 1.0f - In.Color.a;
	
	return Output;
}
PS_OUTPUT ps_font_outline(VS_OUTPUT_FONT In) 
{ 
	float4 sample = tex2D(FontTextureSampler, In.Tex0);
	PS_OUTPUT Output;
	Output.RGBColor =  In.Color;
	Output.RGBColor.a = (1.0f - sample.r) + sample.a;
	
	Output.RGBColor.rgb *= sample.a + 0.05f;
	
	Output.RGBColor	= saturate(Output.RGBColor);
	
	return Output;
}

technique font_uniform_color
{
	pass P0
	{
		VertexShader = vs_font_compiled_2_0;
		PixelShader = compile ps_2_0 ps_font_uniform_color();
	}
}
technique font_background
{
	pass P0
	{
		VertexShader = vs_font_compiled_2_0;
		PixelShader = compile ps_2_0 ps_font_background();
	}
}
technique font_outline
{
	pass P0
	{
		VertexShader = vs_font_compiled_2_0;
		PixelShader = compile ps_2_0 ps_font_outline();
	}
}







//////MAP FONT SCRIBBLER
//vs world map labels - ocean names ect

struct VS_OUTPUT_MAP_FONT
{
	float4 Pos					: POSITION;
	float  Fog				    : FOG;
	
	float4 Color				: COLOR0;
	float2 Tex0					: TEXCOORD0;
	float Map					:TEXCOORD1;
};



VS_OUTPUT_MAP_FONT vs_map_font(float4 vPosition : POSITION, float3 vNormal : NORMAL, float2 tc : TEXCOORD0, float4 vColor : COLOR0, float4 vLightColor : COLOR1)
{
	VS_OUTPUT_MAP_FONT Out;

	Out.Pos = mul(matWorldViewProj, vPosition);

	float4 vWorldPos = (float4)mul(matWorld,vPosition);
	float3 vWorldN = normalize(mul((float3x3)matWorld, vNormal)); //normal in world space
	float3 P = mul(matWorldView, vPosition); //position in view space

	Out.Tex0 = tc;

	float4 diffuse_light = vAmbientColor + vLightColor;
	diffuse_light += saturate(dot(vWorldN, -vSkyLightDir)) * vSkyLightColor;
	diffuse_light += saturate(dot(vWorldN, -vSunDir)) * vSunColor;
	Out.Color = (vMaterialColor * vColor * diffuse_light);

	//apply fog
	float d = length(P);

	Out.Fog = get_fog_amount_new(d, vWorldPos.z);
	
	//extra for fading out txt on world map
	float3 view_vec2 = (vCameraPos.xyz - vWorldPos.xyz);
	Out.Map = length(view_vec2);
	return Out;
}

//ps world map labels - ocean names ect
PS_OUTPUT ps_map_font(VS_OUTPUT_MAP_FONT In) 
{ 
	PS_OUTPUT Output;
	float4 tex_col = tex2D(MeshTextureSampler, In.Tex0);
	INPUT_TEX_GAMMA(tex_col.rgb);
	Output.RGBColor =  In.Color * tex_col;

	
	//extra for fading out txt on map
	float dist = In.Map;
	dist = saturate(dist/100);
	
	if(dist > 0.4) // if far away
	{
	float alphaval = dist -0.15;
	alphaval *= 1+alphaval;
	alphaval = min(alphaval,0.85);
	Output.RGBColor.a *= saturate(alphaval); //make visible
	}
	else
	{
	Output.RGBColor.a = 0.0;
	}
	
//	Output.RGBColor = float4(1,0,0,1);
	OUTPUT_GAMMA(Output.RGBColor.rgb);
	return Output;
}


technique map_font
{
	pass P0
	{
		VertexShader = compile vs_2_0 vs_map_font();
		PixelShader = compile ps_2_0 ps_map_font();
	}
}






#endif

/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#ifdef SHADOW_RELATED_SHADERS

struct VS_OUTPUT_SHADOWMAP
{

	float4 Pos          : POSITION;
	float2 Tex0			: TEXCOORD0;
	float  Depth		: TEXCOORD1;
};
VS_OUTPUT_SHADOWMAP vs_main_shadowmap_skin (float4 vPosition : POSITION, float2 tc : TEXCOORD0, float4 vBlendWeights : BLENDWEIGHT, float4 vBlendIndices : BLENDINDICES)
{
	VS_OUTPUT_SHADOWMAP Out;

	float4 vObjectPos = skinning_deform(vPosition, vBlendWeights, vBlendIndices);
	
	Out.Pos = mul(matWorldViewProj, vObjectPos);
	Out.Depth = Out.Pos.z/ Out.Pos.w;
	Out.Tex0 = tc;

	return Out;
}
VS_OUTPUT_SHADOWMAP vs_main_shadowmap (float4 vPosition : POSITION, float3 vNormal : NORMAL, float2 tc : TEXCOORD0)
{
	VS_OUTPUT_SHADOWMAP Out;
	Out.Pos = mul(matWorldViewProj, vPosition);
	Out.Depth = Out.Pos.z/Out.Pos.w;
	
	if (1)
	{
		float3 vScreenNormal = mul((float3x3)matWorldViewProj, vNormal); //normal in screen space
		Out.Depth -= vScreenNormal.z * (fShadowBias);
	}

	Out.Tex0 = tc;
	return Out;
}
VS_OUTPUT_SHADOWMAP vs_main_shadowmap_biased (float4 vPosition : POSITION, float3 vNormal : NORMAL, float2 tc : TEXCOORD0)
{
	VS_OUTPUT_SHADOWMAP Out;
	Out.Pos = mul(matWorldViewProj, vPosition);
	Out.Depth = Out.Pos.z/Out.Pos.w;
	
	if (1)
	{
		float3 vScreenNormal = mul((float3x3)matWorldViewProj, vNormal); //normal in screen space
		Out.Depth -= vScreenNormal.z * (fShadowBias);
		
		Out.Pos.z += (0.0025f);	//extra bias!
	}

	Out.Tex0 = tc;
	return Out;
}

PS_OUTPUT ps_main_shadowmap(VS_OUTPUT_SHADOWMAP In)
{ 
	PS_OUTPUT Output;
	Output.RGBColor.a = tex2D(MeshTextureSampler, In.Tex0).a;
	Output.RGBColor.a -= 0.5f;
	clip(Output.RGBColor.a);
	
	Output.RGBColor.rgb = In.Depth;// + fShadowBias;

	return Output;
}
VS_OUTPUT_SHADOWMAP vs_main_shadowmap_light(uniform const bool skinning, float4 vPosition : POSITION, float3 vNormal : NORMAL, float2 tc : TEXCOORD0,
											float4 vBlendWeights : BLENDWEIGHT, float4 vBlendIndices : BLENDINDICES)
{
	INITIALIZE_OUTPUT(VS_OUTPUT_SHADOWMAP, Out);

	return Out;
}
PS_OUTPUT ps_main_shadowmap_light(VS_OUTPUT_SHADOWMAP In)
{ 
	PS_OUTPUT Output;
	
	Output.RGBColor = float4(1,0,0,1);
	
	return Output;
}
PS_OUTPUT ps_render_character_shadow(VS_OUTPUT_SHADOWMAP In)
{ 
	PS_OUTPUT Output;
	Output.RGBColor = 1.0f;
	//!! Output.RGBColor.rgb = In.Depth;
	//!! Output.RGBColor.a = 1.0f;
	return Output;
}

VertexShader vs_main_shadowmap_compiled = compile vs_2_0 vs_main_shadowmap();
VertexShader vs_main_shadowmap_skin_compiled = compile vs_2_0 vs_main_shadowmap_skin();

PixelShader ps_main_shadowmap_compiled = compile ps_2_0 ps_main_shadowmap();
PixelShader ps_main_shadowmap_light_compiled = compile ps_2_0 ps_main_shadowmap_light();
PixelShader ps_render_character_shadow_compiled = compile ps_2_0 ps_render_character_shadow();


technique renderdepth
{
	pass P0
	{
		VertexShader = vs_main_shadowmap_compiled;
		PixelShader = ps_main_shadowmap_compiled;
	}
}
technique renderdepth_biased
{
	pass P0
	{
		VertexShader = compile vs_2_0 vs_main_shadowmap_biased();
		PixelShader = ps_main_shadowmap_compiled;
	}
}

technique renderdepthwithskin
{
	pass P0
	{
		VertexShader = vs_main_shadowmap_skin_compiled;
		PixelShader = ps_main_shadowmap_compiled;
	}
}
technique renderdepth_light
{
	pass P0
	{
		VertexShader = compile vs_2_0 vs_main_shadowmap_light(false);
		PixelShader = ps_main_shadowmap_light_compiled;
	}
}
technique renderdepthwithskin_light
{
	pass P0
	{
		VertexShader = compile vs_2_0 vs_main_shadowmap_light(true);
		PixelShader = ps_main_shadowmap_light_compiled;
	}
}

technique render_character_shadow
{
	pass P0
	{
		VertexShader = vs_main_shadowmap_compiled;
		PixelShader = ps_render_character_shadow_compiled;
	}
}
technique render_character_shadow_with_skin
{
	pass P0
	{
		VertexShader = vs_main_shadowmap_skin_compiled;
		PixelShader = ps_render_character_shadow_compiled;
	}
}

//--
float blurred_read_alpha(float2 texCoord)
{
	float3 sample_start = tex2D(CharacterShadowTextureSampler, texCoord).rgb;
	
	static const int SAMPLE_COUNT = 4;
	static const float2 offsets[SAMPLE_COUNT] = {
		-1, 1,
		 1, 1,
		0, 2,
		0, 3,
	};
	
	float blur_amount = saturate(1.0f - texCoord.y);
	blur_amount*=blur_amount;
	float sampleDist = (6.0f / 256.0f) * blur_amount;
	float sample = sample_start;
	
	for (int i = 0; i < SAMPLE_COUNT; i++) {
		float2 sample_pos = texCoord + sampleDist * offsets[i];
		float sample_here = tex2D(CharacterShadowTextureSampler, sample_pos).a;
		sample += sample_here;
	}

	sample /= SAMPLE_COUNT+1;
	return sample;
}
struct VS_OUTPUT_CHARACTER_SHADOW
{
	float4 Pos				    : POSITION;
	float  Fog                  : FOG;
	
	float2 Tex0					: TEXCOORD0;
	float4 Color			    : COLOR0;
	float4 SunLight				: TEXCOORD1;
	float4 ShadowTexCoord		: TEXCOORD2;
	float2 ShadowTexelPos		: TEXCOORD3;
};
VS_OUTPUT_CHARACTER_SHADOW vs_character_shadow (uniform const int PcfMode, float4 vPosition : POSITION, float3 vNormal : NORMAL, float2 tc : TEXCOORD0, float4 vColor : COLOR)
{
	INITIALIZE_OUTPUT(VS_OUTPUT_CHARACTER_SHADOW, Out);
	
	float4 vWorldPos = (float4)mul(matWorld,vPosition);
	if (PcfMode != PCF_NONE)
	{
		//shadow mapping variables
		float3 vWorldN = normalize(mul((float3x3)matWorld, vNormal));

		float wNdotSun = max(-0.0001, dot(vWorldN, -vSunDir));
		Out.SunLight = ( wNdotSun) * vSunColor;

		float4 ShadowPos = mul(matSunViewProj, vWorldPos);
		Out.ShadowTexCoord = ShadowPos;
		Out.ShadowTexCoord.z /= ShadowPos.w;
		Out.ShadowTexCoord.w = 1.0f;
		Out.ShadowTexelPos = Out.ShadowTexCoord * fShadowMapSize;
		//shadow mapping variables end
	}

	Out.Pos = mul(matWorldViewProj, vPosition);
	Out.Tex0 = tc;
	Out.Color = vColor * vMaterialColor;
	
	float3 P = mul(matWorldView, vPosition); //position in view space
	float d = length(P);
	Out.Fog = get_fog_amount_new(d, vWorldPos.z);

	return Out;
}
PS_OUTPUT ps_character_shadow(uniform const int PcfMode, VS_OUTPUT_CHARACTER_SHADOW In)
{ 
	PS_OUTPUT Output;
	
	if (PcfMode == PCF_NONE)
	{
		Output.RGBColor.a = blurred_read_alpha(In.Tex0) * In.Color.a;
	}
	else
	{
		float sun_amount = 0.05f + GetSunAmount(PcfMode, In.ShadowTexCoord, In.ShadowTexelPos);
		//		sun_amount *= sun_amount;
		Output.RGBColor.a = saturate(blurred_read_alpha(In.Tex0) * In.Color.a * sun_amount);
	}
	Output.RGBColor.rgb = In.Color.rgb;
	//Output.RGBColor = float4(tex2D(CharacterShadowTextureSampler, In.Tex0).a, 0, 0, 1);

	//!! Output.RGBColor.a *= 0.1f;
	return Output;
}

DEFINE_TECHNIQUES(character_shadow, vs_character_shadow, ps_character_shadow)


PS_OUTPUT ps_character_shadow_new(uniform const int PcfMode, VS_OUTPUT_CHARACTER_SHADOW In)
{ 
	PS_OUTPUT Output;
	
	if (PcfMode == PCF_NONE)
	{
		Output.RGBColor.a = tex2D(CharacterShadowTextureSampler, In.Tex0).r * In.Color.a;
	}
	else
	{
		float sun_amount = 0.05f + GetSunAmount(PcfMode, In.ShadowTexCoord, In.ShadowTexelPos);
		//		sun_amount *= sun_amount;
		Output.RGBColor.a = saturate(tex2D(CharacterShadowTextureSampler, In.Tex0).r * In.Color.a * sun_amount);
	}
	Output.RGBColor.rgb = In.Color.rgb;
	//Output.RGBColor = float4(tex2D(CharacterShadowTextureSampler, In.Tex0).a, 0, 0, 1);
	return Output;
}

DEFINE_TECHNIQUES(character_shadow_new, vs_character_shadow, ps_character_shadow_new)

#endif

/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#ifdef WATER_SHADERS
struct VS_OUTPUT_WATER
{
	float4 Pos          :  SV_POSITION0;//POSITION;
	float2 Tex0         : TEXCOORD0;
	float4 LightDir_Alpha	: TEXCOORD1;//light direction for bump
	float4 LightDif		: TEXCOORD2;//light diffuse for bump
	float3 CameraDir	: TEXCOORD3;//camera direction for bump
	float4 PosWater		: TEXCOORD4;//position according to the water camera
	float  Fog          : FOG;
	
	float4 projCoord 	: TEXCOORD5;
	float  Depth    	: TEXCOORD6; 
	float2 ViewDir		: TEXCOORD7;
};
VS_OUTPUT_WATER vs_main_water(float4 vPosition : POSITION, float3 vNormal : NORMAL, float4 vColor : COLOR, float2 tc : TEXCOORD0,  float3 vTangent : TANGENT, float3 vBinormal : BINORMAL)
{
	VS_OUTPUT_WATER Out = (VS_OUTPUT_WATER) 0;

	//Waves
//	Float WindFactor = 1.0;
	//vPosition.z += ((WindFactor/5)) * sin(1.5* vPosition.y + (1.6 * WindFactor) * time_var);
	//Waves
	
	Out.Pos = mul(matWorldViewProj, vPosition);
	//!Out.Pos = mul(matViewProj, vPosition);
	
	Out.PosWater = mul(matWaterWorldViewProj, vPosition);

	float3 vWorldPos = (float3)mul(matWorld,vPosition);
	float3 point_to_camera_normal = normalize(vCameraPos - vWorldPos);

	float3 vWorldN = normalize(mul((float3x3)matWorld, vNormal)); //normal in world space
	float3 vWorld_binormal = normalize(mul((float3x3)matWorld, vBinormal)); //normal in world space
	float3 vWorld_tangent  = normalize(mul((float3x3)matWorld, vTangent)); //normal in world space
	
	float3 P = mul(matWorldView, vPosition); //position in view space

	float3x3 TBNMatrix = float3x3(vWorld_tangent, vWorld_binormal, vWorldN); 

	Out.CameraDir = mul(TBNMatrix, point_to_camera_normal);

	Out.Tex0 = tc + texture_offset.xy;

	Out.LightDif = 0; //vAmbientColor;
	float totalLightPower = 0;

	//directional lights, compute diffuse color
	Out.LightDir_Alpha.xyz = mul(TBNMatrix, -vSunDir);
	Out.LightDif += vSunColor * vColor;
	totalLightPower += length(vSunColor.xyz);
	
	Out.LightDir_Alpha.a = vColor.a;

	//apply fog
	float d = length(P);
	Out.Fog = get_fog_amount_new(d, vWorldPos.z);
	
	if(use_depth_effects) 
	{
		Out.projCoord.xy = (float2(Out.Pos.x, -Out.Pos.y)+Out.Pos.w)/2;
		Out.projCoord.xy += (vDepthRT_HalfPixel_ViewportSizeInv.xy * Out.Pos.w);
		Out.projCoord.zw = Out.Pos.zw;
		Out.Depth = Out.Pos.z * far_clip_Inv;
	}
	
	
	
	float3 vViewDir = normalize(vCameraPos.xyz - vWorldPos.xyz); //normalize(mul(TBNMatrix, (vCameraPos.xyz - vWorldPos.xyz) ));	// 
    vViewDir = normalize(mul(TBNMatrix, vViewDir));
    // only return viewdir for parallax.
    Out.ViewDir = vViewDir.xy;
	
	return Out;
}
PS_OUTPUT ps_main_water( VS_OUTPUT_WATER In, uniform const bool use_high, uniform const bool apply_depth, uniform const bool mud_factor )
{ 
	PS_OUTPUT Output;
	
	const bool rgb_normalmap = false; //!apply_depth;
	
	float3 normal;
	if(rgb_normalmap)
	{
		normal = (2.0f * tex2D(SpecularTextureSampler, In.Tex0).rgb - 1.0f);
	}
	else
	{
		normal.xy = (2.0f * tex2D(NormalTextureSampler, In.Tex0).ag - 1.0f);
		normal.z = sqrt(1.0f - dot(normal.xy, normal.xy));
	}
	
	if(!apply_depth)
	{
		normal = float3(0,0,1);
	}
	
	float NdotL = saturate(dot(normal, In.LightDir_Alpha.xyz));
	//float NdotL = saturate(dot(detail_normal, In.LightDir));
	
	//float3 scaledNormal = normalize(normal * float3(0.2f, 0.2f, 1.0f));
	//float light_amount = (0.1f + NdotL) * 0.6f;
	
	float3 vView = normalize(In.CameraDir);
	
	float4 tex;
	if(apply_depth)
	{
		tex = tex2D(ReflectionTextureSampler, (0.25f * normal.xy) + float2(0.5f + 0.5f * (In.PosWater.x / In.PosWater.w), 0.5f - 0.5f * (In.PosWater.y / In.PosWater.w)));
	}
	else
	{
		//for objects use env map (they use same texture register)
		tex = tex2D(EnvTextureSampler, (vView - normal).yx * 3.4f);
	}
	INPUT_OUTPUT_GAMMA(tex.rgb);
	
	Output.RGBColor = 0.01f * NdotL * In.LightDif;
	if(mud_factor)
	{
	   Output.RGBColor *= 0.125f;
	}
	
	//float fresnel = saturate( 1 - dot(In.CameraDir + 0.45, normal) ) + 0.01;
	//fresnel = saturate(fresnel * 2);
	// Fresnel term
	float fresnel = 1-(saturate(dot(vView, normal)));
	fresnel = 0.0204f + 0.9796 * (fresnel * fresnel * fresnel * fresnel * fresnel);

	if(!apply_depth)
	{
		fresnel = min(fresnel, 0.01f);
	}
	if(mud_factor)
	{
		Output.RGBColor.rgb += lerp( tex.rgb*float3(0.105, 0.175, 0.160)*fresnel, tex.rgb, fresnel);
	}
	else
	{
		Output.RGBColor.rgb += (tex.rgb * fresnel);
	}
	Output.RGBColor.a = 1.0f - 0.3f * In.CameraDir.z;
	
	float vertex_alpha = In.LightDir_Alpha.a;
	Output.RGBColor.a *= vertex_alpha;
	
	if(mud_factor)
	{
		Output.RGBColor.a = 1.0f;
	}
	
	
	//static float3 g_cDownWaterColor = {12.0f/255.0f, 26.0f/255.0f, 36.0f/255.0f};
	//static float3 g_cUpWaterColor   = {33.0f/255.0f, 52.0f/255.0f, 77.0f/255.0f};
	const float3 g_cDownWaterColor = mud_factor ? float3(4.5f/255.0f, 8.0f/255.0f, 6.0f/255.0f) : float3(1.0f/255.0f, 4.0f/255.0f, 6.0f/255.0f);
	const float3 g_cUpWaterColor   = mud_factor ? float3(5.0f/255.0f, 7.0f/255.0f, 7.0f/255.0f) : float3(1.0f/255.0f, 5.0f/255.0f, 10.0f/255.0f);
	
	float3 cWaterColor = lerp( g_cUpWaterColor, g_cDownWaterColor,  saturate(dot(vView, normal)));

	if(!apply_depth)
	{
		cWaterColor = In.LightDif.xyz;
	}
	
	float fog_fresnel_factor = saturate(dot(In.CameraDir, normal));
	fog_fresnel_factor *= fog_fresnel_factor;
	fog_fresnel_factor *= fog_fresnel_factor;
	if(!apply_depth)
	{
		fog_fresnel_factor *= 0.1f;
		fog_fresnel_factor += 0.05f;
	}
	Output.RGBColor.rgb += cWaterColor * fog_fresnel_factor;
	
	if(mud_factor)
	{
		Output.RGBColor.rgb += float3(0.022f, 0.02f, 0.005f) * (1.0f - saturate(dot(vView, normal)));
	}
	
	
	if(apply_depth && use_depth_effects) {
	
		float depth = tex2Dproj(DepthTextureSampler, In.projCoord).r;
	
		float alpha_factor;
		if((depth+0.0005) < In.Depth) {
			alpha_factor = 1;
		}else {
			alpha_factor = saturate(/*max(0, */(depth - In.Depth) * 2048);
		}
		
		Output.RGBColor.w *= alpha_factor;
		
		
		//add some alpha to deep areas?
		Output.RGBColor.w += saturate((depth - In.Depth) * 32);
		
		
		static const bool use_refraction = true;
		
		if(use_refraction && use_high) {
			float4 coord_start = In.projCoord; //float2(0.5f + 0.5f * (In.PosWater.x / In.PosWater.w), 0.45 + 0.5f * (In.PosWater.y / In.PosWater.w));
			float4 coord_disto = coord_start;
			coord_disto.xy += (normal.xy * saturate(Output.RGBColor.w) * 0.1f);
			float depth_here = tex2D(DepthTextureSampler, coord_disto).r;
			float4 refraction;
			if(depth_here < depth)
				refraction = tex2Dproj(ScreenTextureSampler, coord_disto);
			else
				refraction = tex2Dproj(ScreenTextureSampler, coord_start);
			INPUT_OUTPUT_GAMMA(refraction.rgb);
	
			Output.RGBColor.rgb = lerp(Output.RGBColor.rgb, refraction.rgb, /*0.145f * fog_fresnel_factor*/ saturate(1.0f - Output.RGBColor.w) * 0.55f);
			if(Output.RGBColor.a>0.1f)
			{
				Output.RGBColor.a *= 1.75f;
			}
			if(mud_factor)
			{
				Output.RGBColor.a *= 1.25f;
			}
		}
	}

	
	//float3 H = normalize(In.LightDir + In.CameraDir); //half vector
	//float4 ColorSpec = fresnel * tex * pow(saturate(dot(H, normalize(normal + float3(normal.xy,0)) )), 100.0f) * In.LightDif;
	//Output.RGBColor.rgb += ColorSpec.rgb;
			
	OUTPUT_GAMMA(Output.RGBColor.rgb);
	Output.RGBColor.a = saturate(Output.RGBColor.a)*0.001;
	if(!apply_depth)
	{
		Output.RGBColor.a = 1.0f;
	}
	
	return Output;
}
technique watermap
{
	pass P0
	{
		VertexShader = compile vs_2_0 vs_main_water();
		PixelShader = compile PS_2_X ps_main_water(false, true, false);
	}
}
technique watermap_high
{
	pass P0
	{
		VertexShader = compile vs_2_0 vs_main_water();
		PixelShader = compile PS_2_X ps_main_water(true, true, false);
	}
}
technique watermap_mud
{
	pass P0
	{
		VertexShader = compile vs_2_0 vs_main_water();
		PixelShader = compile PS_2_X ps_main_water(false, true, true);
	}
}
technique watermap_mud_high
{
	pass P0
	{
		VertexShader = compile vs_2_0 vs_main_water();
		PixelShader = compile PS_2_X ps_main_water(true, true, true);
	}
}
/*technique watermap_for_objects
{
	pass P0
	{
		VertexShader = compile vs_2_0 vs_main_water();
		PixelShader = compile PS_2_X ps_main_water(true, false);
	}
}*/


////PARALLAX SHADER

//-----

struct VS_OUTPUT_PARALLAX_WATER
{
	float4 Pos          : POSITION; //////////////
	float2 Tex0         : TEXCOORD0;//////////////////
	
	float4 LightDir_Alpha	: TEXCOORD1;//light direction for bump
	float4 LightDif		: TEXCOORD2;//light diffuse for bump
	
	float3 ViewDir		: TEXCOORD3; //view dir.z is fresnel
	float3 CameraDir	: TEXCOORD4;//camera direction for bump////////////
	float4 PosWater		: TEXCOORD5;//position according to the water camera//////////////
	
	
	float4 projCoord 	: TEXCOORD6;
	float  Depth    	: TEXCOORD7; 
	float  Fog          : FOG;///////////////
};


VS_OUTPUT_PARALLAX_WATER vs_parallax_water(float4 vPosition : POSITION, float3 vNormal : NORMAL, float4 vColor : COLOR, float2 tc : TEXCOORD0,  float3 vTangent : TANGENT, float3 vBinormal : BINORMAL)
{
	VS_OUTPUT_PARALLAX_WATER Out = (VS_OUTPUT_PARALLAX_WATER) 0;

	
	
	//CUSTOM TIME VARIABLE - SET BY PHAIK
	float Timer = GetTimer(1.0f);
	
	//WAVE INFORMATION - SET BY PHAIK
	float4 WaveInfo = GetWaveInfo();
		float2 Amplitude = WaveInfo.xy;
		float2 Period = WaveInfo.zw;
	
	//INITIAL WAVE ORIGIN - SET BY PHAIK	
	float4 Origin = GetWaveOrigin();

	// Waves on y axis
  // vPosition.z = ((vPosition.z + Amplitude.y * sin(Period.y *  vPosition.y + Timer)) + Origin.y); //
   vPosition.z = (vPosition.z + Amplitude.y * sin((Period.y *  vPosition.y) + Timer) + Origin.y); //
   // Waves on x axis
  // vPosition.z = ((vPosition.z + Amplitude.x * sin(Period.x *  vPosition.x + Timer)) + Origin.x); //
   vPosition.z = (vPosition.z + Amplitude.x * sin((Period.x *  vPosition.x) + Timer) + Origin.x); //
	//OVERALL SEA LEVEL
   vPosition.z = vPosition.z + Origin.z;
	
	
	Out.Pos = mul(matWorldViewProj, vPosition);
	
	
	
	//!Out.Pos = mul(matViewProj, vPosition);
	
	Out.PosWater = mul(matWaterWorldViewProj, vPosition);

	float3 vWorldPos = (float3)mul(matWorld,vPosition);
	float3 point_to_camera_normal = normalize(vCameraPos - vWorldPos);

	float3 vWorldN = normalize(mul((float3x3)matWorld, vNormal)); //normal in world space
	float3 vWorld_binormal = normalize(mul((float3x3)matWorld, vBinormal)); //normal in world space
	float3 vWorld_tangent  = normalize(mul((float3x3)matWorld, vTangent)); //normal in world space
	
	float3 P = mul(matWorldView, vPosition); //position in view space

	float3x3 TBNMatrix = float3x3(vWorld_tangent, vWorld_binormal, vWorldN); 

	Out.CameraDir = mul(TBNMatrix, point_to_camera_normal);
	
	
	//insert from parallax shader
	float3 vViewDir = normalize(vCameraPos.xyz - vWorldPos.xyz); //normalize(mul(TBNMatrix, (vCameraPos.xyz - vWorldPos.xyz) ));	// 
	
    float fresnel = 1-(saturate(dot(vViewDir, vWorldN)));
    fresnel*=fresnel+0.1h;
  
    //Out.ViewDir.z = vPosition.x; //view dir.z is fresnel
    // yay for TBN space
    vViewDir = normalize(mul(TBNMatrix, vViewDir));
    // only return viewdir for parallax.
    Out.ViewDir.xy = vViewDir.xy;
	 
	Out.Tex0 = tc * 1.75;

	Out.LightDif = 0; //vAmbientColor;
	float totalLightPower = 0;

	//directional lights, compute diffuse color
	Out.LightDir_Alpha.xyz = mul(TBNMatrix, -vSunDir);
	Out.LightDif += vSunColor * vColor;
	totalLightPower += length(vSunColor.xyz);
	
	Out.LightDir_Alpha.a = vColor.a;

	//apply fog
	float d = length(P);
	Out.Fog = get_fog_amount_new(d, vWorldPos.z);
	
	if(use_depth_effects) 
	{
		Out.projCoord.xy = (float2(Out.Pos.x, -Out.Pos.y)+Out.Pos.w)/2;
		Out.projCoord.xy += (vDepthRT_HalfPixel_ViewportSizeInv.xy * Out.Pos.w);
		Out.projCoord.zw = Out.Pos.zw;
		Out.Depth.x = Out.Pos.z * far_clip_Inv;
	}
	
	
	float3 view_vector = (vCameraPos.xyz - vWorldPos.xyz);
	//Out.Depth.y = length(view_vector);
	
	
	return Out;
}

	

PS_OUTPUT ps_parallax_water( VS_OUTPUT_PARALLAX_WATER In, uniform const bool use_high, uniform const bool apply_depth, uniform const bool mud_factor )
{ 
	PS_OUTPUT Output;
	
	const bool rgb_normalmap = false; //!apply_depth;
	
//SHADER VALUES/CONTSNTS
	In.Tex0 = In.Tex0*0.5;

	float Timer = GetTimer(1.0f);

	float time_variable = 0.5*time_var;//Timer;//
	float2 TexOffsetA =In.Tex0;
	float2 TexOffsetB =In.Tex0;
	
	
	
//PARALLAX SECTION
	float3 viewVec = normalize(In.ViewDir);
	{
     float factor = (0.01f * vSpecularColor.x);
     float volume = (factor * 5.0);//0.04;
     float bias = (factor * -2.5f);//-0.02; 

	//PARALLAX TEX A
	TexOffsetA = float2(In.Tex0.x,In.Tex0.y + (0.1*time_variable));
	float height = tex2D(MeshTextureSampler, TexOffsetA).a;
	//height *= sin(0.5*time_variable + 10*In.Tex0.x);
	float offset = height * volume + bias;
	
	//PARALLAX TEX B
	TexOffsetB = float2(In.Tex0.x + (0.15*time_variable),In.Tex0.y+ (0.25*time_variable));
	float height2 = tex2D(SpecularTextureSampler, TexOffsetB).a;
	float offset2 = (height2) * (0.5*volume) + (0.5*bias);
	
	//APPLY PARALLAX TO TEXCOORDS
	In.Tex0 += offset * viewVec.xy;
	In.Tex0 += offset2 * viewVec.xy;
	}
//PARALLAX END
	
	
	
	
//NORMAL CALCULATED (USING PARALLAXED TEX COORDS)
	float3 normal;
	float3 normal2;
	if(rgb_normalmap)
	{
		normal = (2.0f * tex2D(Diffuse2Sampler, In.Tex0).rgb - 1.0f);
	}
	else
	{   //Normalmap A
		TexOffsetA = float2(In.Tex0.x,In.Tex0.y + (0.1*time_variable));
		normal.xy = (2.0f * tex2D(Diffuse2Sampler, TexOffsetA).ag - 1.0f);
		normal.z = sqrt(1.0f - dot(normal.xy, normal.xy));
		
		//Normalmap b
		TexOffsetB = float2(In.Tex0.x,In.Tex0.y+ (0.25*time_variable));// + (0.15*time_variable)
		normal2.xy = (2.0f * tex2D(NormalTextureSampler, TexOffsetB).ag - 1.0f);
		normal2.z = sqrt(1.0f - dot(normal2.xy, normal2.xy));
		
		normal = lerp (normal,normal2,0.35);
	}
	
	if(!apply_depth)
	{
		normal = float3(0,0,1);
	}
//END NORMAL CALCULATIONS
	
	
	
//CALCULATE LIGHT (USING NORMALS & PARA ABOVE)
	float NdotL = saturate(dot(normal, In.LightDir_Alpha.xyz));
	
	float3 vView = normalize(In.CameraDir);
	
	float4 tex;
	if(apply_depth)
	{
		tex = tex2D(ReflectionTextureSampler, (0.25f * normal.xy) + float2(0.5f + 0.5f * (In.PosWater.x / In.PosWater.w), 0.5f - 0.5f * (In.PosWater.y / In.PosWater.w)));
	}
	else
	{
		//for objects use env map (they use same texture register)
		tex = tex2D(EnvTextureSampler, (vView - normal).yx * 3.4f);
	}
	
	INPUT_OUTPUT_GAMMA(tex.rgb);
	
	Output.RGBColor = 0.01f * NdotL * In.LightDif;
	if(mud_factor)
	{
	   Output.RGBColor *= 0.125f;
	}
	
	//float fresnel = saturate( 1 - dot(In.CameraDir + 0.45, normal) ) + 0.01;
	//fresnel = saturate(fresnel * 2);
	// Fresnel term
	float fresnel = 1-(saturate(dot(vView, normal)));
	fresnel = 0.0204f + 0.9796 * (fresnel * fresnel * fresnel * fresnel * fresnel* fresnel * fresnel * fresnel * fresnel);
	//fresnel *= 0.95;
	
	//float fresnel_b = saturate(fresnel);
	//fresnel_b = saturate(pow(fresnel_b,(0.08*In.Depth.y)));
	
	//fresnel = lerp(fresnel,fresnel_b,0.5);
	
	//whether to correct fresnel for dist or not?
	//add foam? non textur4ed just white?
	//rate of wave movement
	// add wind parameters
	
	if(!apply_depth)
	{
		fresnel = min(fresnel, 0.01f);
	}
	if(mud_factor)
	{
		Output.RGBColor.rgb += lerp( tex.rgb*float3(0.105, 0.175, 0.160)*fresnel, tex.rgb, fresnel);
	}
	else
	{
		Output.RGBColor.rgb += (tex.rgb * fresnel);
	}
	Output.RGBColor.a = 1.0f - 0.3f * In.CameraDir.z;
	
	float vertex_alpha = In.LightDir_Alpha.a;
	Output.RGBColor.a *= vertex_alpha;
	
	if(mud_factor)
	{
		Output.RGBColor.a = 1.0f;
	}
	
	
	//static float3 g_cDownWaterColor = {12.0f/255.0f, 26.0f/255.0f, 36.0f/255.0f};
	//static float3 g_cUpWaterColor   = {33.0f/255.0f, 52.0f/255.0f, 77.0f/255.0f};
	const float3 g_cDownWaterColor = mud_factor ? float3(4.5f/255.0f, 8.0f/255.0f, 6.0f/255.0f) : float3(1.0f/255.0f, 4.0f/255.0f, 6.0f/255.0f);
	const float3 g_cUpWaterColor   = mud_factor ? float3(5.0f/255.0f, 7.0f/255.0f, 7.0f/255.0f) : float3(1.0f/255.0f, 5.0f/255.0f, 10.0f/255.0f);
	
	float3 cWaterColor = lerp( g_cUpWaterColor, g_cDownWaterColor,  saturate(dot(vView, normal)));

	if(!apply_depth)
	{
		cWaterColor = In.LightDif.xyz;
	}
	
	float fog_fresnel_factor = saturate(dot(In.CameraDir, normal));
	fog_fresnel_factor *= fog_fresnel_factor;
	fog_fresnel_factor *= fog_fresnel_factor;
	if(!apply_depth)
	{
		fog_fresnel_factor *= 0.1f;
		fog_fresnel_factor += 0.05f;
	}
	Output.RGBColor.rgb += cWaterColor * fog_fresnel_factor;
	
	if(mud_factor)
	{
		Output.RGBColor.rgb += float3(0.022f, 0.02f, 0.005f) * (1.0f - saturate(dot(vView, normal)));
	}
	
	
	if(apply_depth && use_depth_effects) {
	
		float depth = tex2Dproj(DepthTextureSampler, In.projCoord).r;
	
		float alpha_factor;
		if((depth+0.0005) < In.Depth.x) {
			alpha_factor = 1;
		}else {
			alpha_factor = saturate(/*max(0, */(depth - In.Depth.x) * 2048);
		}
		
		Output.RGBColor.w *= alpha_factor;
		
		
		//add some alpha to deep areas?
		Output.RGBColor.w += saturate((depth - In.Depth.x) * 32);
		
		
		static const bool use_refraction = true;
		
		if(use_refraction && use_high) {
			float4 coord_start = In.projCoord; //float2(0.5f + 0.5f * (In.PosWater.x / In.PosWater.w), 0.45 + 0.5f * (In.PosWater.y / In.PosWater.w));
			float4 coord_disto = coord_start;
			coord_disto.xy += (normal.xy * saturate(Output.RGBColor.w) * 0.1f);
			float depth_here = tex2D(DepthTextureSampler, coord_disto).r;
			float4 refraction;
			if(depth_here < depth)
				refraction = tex2Dproj(ScreenTextureSampler, coord_disto);
			else
				refraction = tex2Dproj(ScreenTextureSampler, coord_start);
			INPUT_OUTPUT_GAMMA(refraction.rgb);
	
			Output.RGBColor.rgb = lerp(Output.RGBColor.rgb, refraction.rgb, /*0.145f * fog_fresnel_factor*/ saturate(1.0f - Output.RGBColor.w) * 0.55f);
			if(Output.RGBColor.a>0.1f)
			{
				Output.RGBColor.a *= 1.75f;
			}
			if(mud_factor)
			{
				Output.RGBColor.a *= 1.25f;
			}
		}
	}

	
	//float3 H = normalize(In.LightDir + In.CameraDir); //half vector
	//float4 ColorSpec = fresnel * tex * pow(saturate(dot(H, normalize(normal + float3(normal.xy,0)) )), 100.0f) * In.LightDif;
	//Output.RGBColor.rgb += ColorSpec.rgb;
			
	OUTPUT_GAMMA(Output.RGBColor.rgb);
	Output.RGBColor.a = saturate(Output.RGBColor.a);
	if(!apply_depth)
	{
		Output.RGBColor.a = 1.0f;
	}
	
	return Output;
}	
	



VS_OUTPUT_PARALLAX_WATER vs_outer_terrain_water(float4 vPosition : POSITION, float3 vNormal : NORMAL, float4 vColor : COLOR, float2 tc : TEXCOORD0,  float3 vTangent : TANGENT, float3 vBinormal : BINORMAL)
{
	VS_OUTPUT_PARALLAX_WATER Out = (VS_OUTPUT_PARALLAX_WATER) 0;

//	float WindFactor = GetWindAmount(1.50f);
	
	
	vPosition.z = vPosition.z+ 2.7;
	
	/*if(WindFactor > (1.6*1.50))
	{
	vPosition.z = vPosition.z- (WindFactor*0.20);
	}
	
	// Waves on y axis (move in direction of texture "waves" movement
	float ZPosA = vPosition.z + ((WindFactor/5)*vColor.r) * sin(4*  -vPosition.y + time_var); // actual movement waves	
	float ZPosB = vPosition.z + ((WindFactor/5)*vColor.r) * sin(4*  -vPosition.y + 0.5 + time_var); // actual movement waves		
	vPosition.z = max(ZPosA,ZPosB); //merges two waves so that they basically form an elongated sine wave
	
	// Waves on x axis (move in direction of texture "waves" movement
	vPosition.z = vPosition.z + ((WindFactor/5)*vColor.r) * sin(4*  -vPosition.x + time_var); // actual movement waves	
*/
	
	
	Out.Pos = mul(matWorldViewProj, vPosition);
	//!Out.Pos = mul(matViewProj, vPosition);
	
	Out.PosWater = mul(matWaterWorldViewProj, vPosition);

	float3 vWorldPos = (float3)mul(matWorld,vPosition);
	float3 point_to_camera_normal = normalize(vCameraPos - vWorldPos);

	float3 vWorldN = normalize(mul((float3x3)matWorld, vNormal)); //normal in world space
	float3 vWorld_binormal = normalize(mul((float3x3)matWorld, vBinormal)); //normal in world space
	float3 vWorld_tangent  = normalize(mul((float3x3)matWorld, vTangent)); //normal in world space
	
	float3 P = mul(matWorldView, vPosition); //position in view space

	float3x3 TBNMatrix = float3x3(vWorld_tangent, vWorld_binormal, vWorldN); 

	Out.CameraDir = mul(TBNMatrix, point_to_camera_normal);
	
	
	//insert from parallax shader
	float3 vViewDir = normalize(vCameraPos.xyz - vWorldPos.xyz); //normalize(mul(TBNMatrix, (vCameraPos.xyz - vWorldPos.xyz) ));	// 
	
    float fresnel = 1-(saturate(dot(vViewDir, vWorldN)));
    fresnel*=fresnel+0.1h;
  
    //Out.ViewDir.z = vPosition.x; //view dir.z is fresnel
    // yay for TBN space
    vViewDir = normalize(mul(TBNMatrix, vViewDir));
    // only return viewdir for parallax.
    Out.ViewDir.xy = vViewDir.xy;
	 
	Out.Tex0 = tc;

	Out.LightDif = 0; //vAmbientColor;
	float totalLightPower = 0;

	//directional lights, compute diffuse color
	Out.LightDir_Alpha.xyz = mul(TBNMatrix, -vSunDir);
	Out.LightDif += vSunColor * vColor;
	totalLightPower += length(vSunColor.xyz);
	
	Out.LightDir_Alpha.a = vColor.a;

	//apply fog
	float d = length(P);
	Out.Fog = get_fog_amount_new(d, vWorldPos.z);
	
	if(use_depth_effects) 
	{
		Out.projCoord.xy = (float2(Out.Pos.x, -Out.Pos.y)+Out.Pos.w)/2;
		Out.projCoord.xy += (vDepthRT_HalfPixel_ViewportSizeInv.xy * Out.Pos.w);
		Out.projCoord.zw = Out.Pos.zw;
		Out.Depth.x = Out.Pos.z * far_clip_Inv;
	}
	
	
	float3 view_vector = (vCameraPos.xyz - vWorldPos.xyz);
	//Out.Depth.y = length(view_vector);
	
	
	return Out;
}


	
PS_OUTPUT ps_parallax_water2( VS_OUTPUT_PARALLAX_WATER In, uniform const bool use_high, uniform const bool apply_depth, uniform const bool mud_factor )
{ 
	PS_OUTPUT Output;
	
	const bool rgb_normalmap = false; //!apply_depth;
	
//SHADER VALUES/CONTSNTS
	In.Tex0 = In.Tex0*0.5;


	float time_variable = 0.5*time_var;
	float2 TexOffsetA =In.Tex0;
	float2 TexOffsetB =In.Tex0;
	
	
	
//PARALLAX SECTION
	float3 viewVec = normalize(In.ViewDir);
	{
     float factor = (0.01f * vSpecularColor.x);
     float bias = (factor * -2.5f);//-0.02; 
     float volume = (factor * 5.0);//0.04;

	//PARALLAX TEX A
	TexOffsetA = float2(In.Tex0.x,In.Tex0.y + (0.1*time_variable));
	float height = tex2D(MeshTextureSampler, TexOffsetA).a;
	//height *= sin(0.5*time_variable + 10*In.Tex0.x);
	float offset = height * volume + bias;
	
	//PARALLAX TEX B
	TexOffsetB = float2(In.Tex0.x + (0.15*time_variable),In.Tex0.y+ (0.25*time_variable));
	float height2 = tex2D(SpecularTextureSampler, TexOffsetB).a;
	float offset2 = (height2) * (0.5*volume) + (0.5*bias);
	
	//APPLY PARALLAX TO TEXCOORDS
	In.Tex0 += offset * viewVec.xy;
	In.Tex0 += offset2 * viewVec.xy;
	}
//PARALLAX END
	
	
	
	
//NORMAL CALCULATED (USING PARALLAXED TEX COORDS)
	float3 normal;
	float3 normal2;
	if(rgb_normalmap)
	{
		normal = (2.0f * tex2D(Diffuse2Sampler, In.Tex0).rgb - 1.0f);
	}
	else
	{   //Normalmap A
		TexOffsetA = float2(In.Tex0.x,In.Tex0.y + (0.1*time_variable));
		normal.xy = (2.0f * tex2D(Diffuse2Sampler, TexOffsetA).ag - 1.0f);
		normal.z = sqrt(1.0f - dot(normal.xy, normal.xy));
		
		//Normalmap b
		TexOffsetB = float2(In.Tex0.x,In.Tex0.y+ (0.25*time_variable));// + (0.15*time_variable)
		normal2.xy = (2.0f * tex2D(NormalTextureSampler, TexOffsetB).ag - 1.0f);
		normal2.z = sqrt(1.0f - dot(normal2.xy, normal2.xy));
		
		normal = lerp (normal,normal2,0.35);
	}
	
	if(!apply_depth)
	{
		normal = float3(0,0,1);
	}
//END NORMAL CALCULATIONS
	
	
	
//CALCULATE LIGHT (USING NORMALS & PARA ABOVE)
	float NdotL = saturate(dot(normal, In.LightDir_Alpha.xyz));
	
	float3 vView = normalize(In.CameraDir);
	
	float4 tex;
	if(apply_depth)
	{
		tex = tex2D(ReflectionTextureSampler, (0.25f * normal.xy) + float2(0.5f + 0.5f * (In.PosWater.x / In.PosWater.w), 0.5f - 0.5f * (In.PosWater.y / In.PosWater.w)));
	}
	else
	{
		//for objects use env map (they use same texture register)
		tex = tex2D(EnvTextureSampler, (vView - normal).yx * 3.4f);
	}
	
	INPUT_OUTPUT_GAMMA(tex.rgb);
	
	Output.RGBColor = 0.01f * NdotL * In.LightDif;
	if(mud_factor)
	{
	   Output.RGBColor *= 0.125f;
	}
	
	//float fresnel = saturate( 1 - dot(In.CameraDir + 0.45, normal) ) + 0.01;
	//fresnel = saturate(fresnel * 2);
	// Fresnel term
	float fresnel = 1-(saturate(dot(vView, normal)));
	fresnel = 0.0204f + 0.9796 * (fresnel * fresnel * fresnel * fresnel * fresnel* fresnel * fresnel * fresnel * fresnel);
	//fresnel *= 0.95;
	
	//float fresnel_b = saturate(fresnel);
	//fresnel_b = saturate(pow(fresnel_b,(0.08*In.Depth.y)));
	
	//fresnel = lerp(fresnel,fresnel_b,0.5);
	
	//whether to correct fresnel for dist or not?
	//add foam? non textur4ed just white?
	//rate of wave movement
	// add wind parameters
	
	if(!apply_depth)
	{
		fresnel = min(fresnel, 0.01f);
	}
	if(mud_factor)
	{
		Output.RGBColor.rgb += lerp( tex.rgb*float3(0.105, 0.175, 0.160)*fresnel, tex.rgb, fresnel);
	}
	else
	{
		Output.RGBColor.rgb += (tex.rgb * fresnel);
	}
	Output.RGBColor.a = 1.0f - 0.3f * In.CameraDir.z;
	
	float vertex_alpha = In.LightDir_Alpha.a;
	Output.RGBColor.a *= vertex_alpha;
	
	if(mud_factor)
	{
		Output.RGBColor.a = 1.0f;
	}
	
	
	//static float3 g_cDownWaterColor = {12.0f/255.0f, 26.0f/255.0f, 36.0f/255.0f};
	//static float3 g_cUpWaterColor   = {33.0f/255.0f, 52.0f/255.0f, 77.0f/255.0f};
	const float3 g_cDownWaterColor = mud_factor ? float3(4.5f/255.0f, 8.0f/255.0f, 6.0f/255.0f) : float3(1.0f/255.0f, 4.0f/255.0f, 6.0f/255.0f);
	const float3 g_cUpWaterColor   = mud_factor ? float3(5.0f/255.0f, 7.0f/255.0f, 7.0f/255.0f) : float3(1.0f/255.0f, 5.0f/255.0f, 10.0f/255.0f);
	
	float3 cWaterColor = lerp( g_cUpWaterColor, g_cDownWaterColor,  saturate(dot(vView, normal)));

	if(!apply_depth)
	{
		cWaterColor = In.LightDif.xyz;
	}
	
	float fog_fresnel_factor = saturate(dot(In.CameraDir, normal));
	fog_fresnel_factor *= fog_fresnel_factor;
	fog_fresnel_factor *= fog_fresnel_factor;
	if(!apply_depth)
	{
		fog_fresnel_factor *= 0.1f;
		fog_fresnel_factor += 0.05f;
	}
	Output.RGBColor.rgb += cWaterColor * fog_fresnel_factor;
	
	if(mud_factor)
	{
		Output.RGBColor.rgb += float3(0.022f, 0.02f, 0.005f) * (1.0f - saturate(dot(vView, normal)));
	}
	
	
	if(apply_depth && use_depth_effects) {
	
		float depth = tex2Dproj(DepthTextureSampler, In.projCoord).r;
	
		float alpha_factor;
		if((depth+0.0005) < In.Depth.x) {
			alpha_factor = 1;
		}else {
			alpha_factor = saturate(/*max(0, */(depth - In.Depth.x) * 2048);
		}
		
		Output.RGBColor.w *= alpha_factor;
		
		
		//add some alpha to deep areas?
		Output.RGBColor.w += saturate((depth - In.Depth.x) * 32);
		
		
		static const bool use_refraction = true;
		
		if(use_refraction && use_high) {
			float4 coord_start = In.projCoord; //float2(0.5f + 0.5f * (In.PosWater.x / In.PosWater.w), 0.45 + 0.5f * (In.PosWater.y / In.PosWater.w));
			float4 coord_disto = coord_start;
			coord_disto.xy += (normal.xy * saturate(Output.RGBColor.w) * 0.1f);
			float depth_here = tex2D(DepthTextureSampler, coord_disto).r;
			float4 refraction;
			if(depth_here < depth)
				refraction = tex2Dproj(ScreenTextureSampler, coord_disto);
			else
				refraction = tex2Dproj(ScreenTextureSampler, coord_start);
			INPUT_OUTPUT_GAMMA(refraction.rgb);
	
			Output.RGBColor.rgb = lerp(Output.RGBColor.rgb, refraction.rgb, /*0.145f * fog_fresnel_factor*/ saturate(1.0f - Output.RGBColor.w) * 0.55f);
			if(Output.RGBColor.a>0.1f)
			{
				Output.RGBColor.a *= 1.75f;
			}
			if(mud_factor)
			{
				Output.RGBColor.a *= 1.25f;
			}
		}
	}

	
	//float3 H = normalize(In.LightDir + In.CameraDir); //half vector
	//float4 ColorSpec = fresnel * tex * pow(saturate(dot(H, normalize(normal + float3(normal.xy,0)) )), 100.0f) * In.LightDif;
	//Output.RGBColor.rgb += ColorSpec.rgb;
			
	OUTPUT_GAMMA(Output.RGBColor.rgb);
	Output.RGBColor.a = saturate(Output.RGBColor.a);
	if(!apply_depth)
	{
		Output.RGBColor.a = 1.0f;
	}
	
	
	//Output.RGBColor.a = 0.3f;
	
	return Output;
}	
	
	
	
	
	
	
	
	
	
	
	
	
	
	








VertexShader vs_parallax_water_compiled_PCF_NONE = compile vs_2_0 vs_parallax_water(); //(PCF_NONE);
VertexShader vs_parallax_water_compiled_PCF_DEFAULT = compile vs_2_0 vs_parallax_water(); //(PCF_DEFAULT);
VertexShader vs_parallax_water_compiled_PCF_NVIDIA = compile vs_2_a vs_parallax_water(); //(PCF_NVIDIA);


technique parallax_water
{
	pass P0
	{
		VertexShader = vs_parallax_water_compiled_PCF_NONE;
		PixelShader = compile PS_2_X ps_parallax_water(false, true, false);//(PCF_NONE);
	}
}
technique parallax_water_SHDW
{
	pass P0
	{
		VertexShader = vs_parallax_water_compiled_PCF_DEFAULT;
		PixelShader = compile PS_2_X ps_parallax_water(true, true, false);//(PCF_DEFAULT);
	}
}
technique parallax_water_SHDWNVIDIA
{
	pass P0
	{
		VertexShader = vs_parallax_water_compiled_PCF_NVIDIA;
		PixelShader = compile ps_2_a ps_parallax_water(true, true, false);//(PCF_NVIDIA);
	}
}
DEFINE_LIGHTING_TECHNIQUE(parallax_water, 0, 1, 0, 0, 0)




VertexShader vs_outer_terrain_water_compiled_PCF_NONE = compile vs_2_0 vs_outer_terrain_water(); //(PCF_NONE);
VertexShader vs_outer_terrain_water_compiled_PCF_DEFAULT = compile vs_2_0 vs_outer_terrain_water(); //(PCF_DEFAULT);
VertexShader vs_outer_terrain_water_compiled_PCF_NVIDIA = compile vs_2_a vs_outer_terrain_water(); //(PCF_NVIDIA);


technique outer_terrain_water
{
	pass P0
	{
		VertexShader = vs_outer_terrain_water_compiled_PCF_NONE;
		PixelShader = compile PS_2_X ps_parallax_water2(false, true, false);//(PCF_NONE);
	}
}
technique outer_terrain_water_SHDW
{
	pass P0
	{
		VertexShader = vs_outer_terrain_water_compiled_PCF_DEFAULT;
		PixelShader = compile PS_2_X ps_parallax_water2(true, true, false);//(PCF_DEFAULT);
	}
}
technique outer_terrain_water_SHDWNVIDIA
{
	pass P0
	{
		VertexShader = vs_outer_terrain_water_compiled_PCF_NVIDIA;
		PixelShader = compile ps_2_a ps_parallax_water2(true, true, false);//(PCF_NVIDIA);
	}
}
DEFINE_LIGHTING_TECHNIQUE(outer_terrain_water, 0, 1, 0, 0, 0)










#endif

/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#ifdef SKYBOX_SHADERS

struct VS_OUTPUT_SKYBOX
{
	float4 Pos					: POSITION;
	float  Fog				    : FOG;
	
	float4 Color				: COLOR0;
	float2 Tex0					: TEXCOORD0;
	float VertHeight				: TEXCOORD1;
};

PS_OUTPUT ps_skybox_shading(VS_OUTPUT_SKYBOX In) 
{ 
	PS_OUTPUT Output;
	Output.RGBColor =  In.Color;
	
	Output.RGBColor *= tex2D(MeshTextureSampler, In.Tex0);

	
	return Output;
}

PS_OUTPUT ps_skybox_shading_new(uniform bool use_hdr, VS_OUTPUT_SKYBOX In) 
{ 
	PS_OUTPUT Output;
	
	if(use_hdr) {
		
		Output.RGBColor =  In.Color;
		Output.RGBColor *= tex2D(Diffuse2Sampler, In.Tex0);
		
		// expand to floating point.. (RGBE)
		float2 scaleBias = float2(vSpecularColor.x, vSpecularColor.y);
		
		//float exFactor16 = dot(tex2D(MeshTextureSampler, In.Tex0).rgb, 0.25);	//fake.
		float exFactor16 = tex2D(EnvTextureSampler, In.Tex0).r;
		float exFactor8 = floor(exFactor16*255)/255;
		Output.RGBColor.rgb *= exp2(exFactor16 * scaleBias.x + scaleBias.y);
		
		//Output.RGBColor.rgb = tex2D(EnvTextureSampler, In.Tex0);
		
	}else {
		//switch to old style
		Output.RGBColor =  In.Color;
		float4 tex_col = tex2D(MeshTextureSampler, In.Tex0);
		INPUT_TEX_GAMMA(tex_col.rgb);
		Output.RGBColor *= tex_col;
	}
	
	Output.RGBColor.a = 1;
	
	//gamma correct?
	OUTPUT_GAMMA(Output.RGBColor.rgb);
	
	if(In.Color.a == 0.0f)
	{
		Output.RGBColor.rgb = saturate(Output.RGBColor.rgb);
	}
	
	//worldmap sea level bit
	if(In.VertHeight < 150.0) //if vert is below sea level
	Output.RGBColor.rgb *= saturate((In.VertHeight+7)*0.1);
	//
	
	return Output;
}

VS_OUTPUT_SKYBOX vs_skybox(float4 vPosition : POSITION, float4 vColor : COLOR, float2 tc : TEXCOORD0)
{
	VS_OUTPUT_SKYBOX Out;
	//float4 RotatedPos = vPosition;
	//RotatedPos.xy = rotatevector(vPosition.xy, time_var*0.4);//
	Out.Pos = mul(matWorldViewProj, vPosition);
	Out.VertHeight = vPosition.z;
	Out.Pos.z = Out.Pos.w;

	float3 P = vPosition; //position in view space

	//La Grandmaster movement
	//float2 Texcoor = tc;
	//Texcoor.x += (time_var * 0.001);	
	//La Grandmaster movement end
	
	Out.Tex0 = tc;//Texcoor;
	Out.Color = vColor * vMaterialColor;

	//apply fog
	P.z *= 0.2f;
	float d = length(P);
	float4 vWorldPos = (float4)mul(matWorld,vPosition);
	Out.Fog = get_fog_amount_new(d, vWorldPos.z);
	
	Out.Color.a = (vWorldPos.z < -10.0f) ? 0.0f : 1.0f;
	
	return Out;
}

VertexShader vs_skybox_compiled = compile vs_2_0 vs_skybox();

technique skybox
{
	pass P0
	{
		VertexShader = vs_skybox_compiled;
		PixelShader = compile ps_2_0 ps_skybox_shading();
	}
}

technique skybox_new
{
	pass P0
	{
		VertexShader = vs_skybox_compiled;
		PixelShader = compile ps_2_0 ps_skybox_shading_new(false);
	}
}

technique skybox_new_HDR
{
	pass P0
	{
		VertexShader = vs_skybox_compiled;
		PixelShader = compile ps_2_0 ps_skybox_shading_new(true);
	}
}
#endif

/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#ifdef STANDART_RELATED_SHADER //these are going to be same with standart!

struct VS_OUTPUT
{
	float4 Pos					: POSITION;
	float  Fog				    : FOG;
	
	float4 Color				: COLOR0;
	float2 Tex0					: TEXCOORD0;
	float4 SunLight				: TEXCOORD1;
	float4 ShadowTexCoord		: TEXCOORD2;
	float2 ShadowTexelPos		: TEXCOORD3;
};

VS_OUTPUT vs_main(uniform const int PcfMode, uniform const bool UseSecondLight, float4 vPosition : POSITION, float3 vNormal : NORMAL, float2 tc : TEXCOORD0, float4 vColor : COLOR0, float4 vLightColor : COLOR1)
{
	INITIALIZE_OUTPUT(VS_OUTPUT, Out);

	Out.Pos = mul(matWorldViewProj, vPosition);

	float4 vWorldPos = (float4)mul(matWorld,vPosition);
	float3 vWorldN = normalize(mul((float3x3)matWorld, vNormal)); //normal in world space


	Out.Tex0 = tc;

	float4 diffuse_light = vAmbientColor;
	//   diffuse_light.rgb *= gradient_factor * (gradient_offset + vWorldN.z);

	if (UseSecondLight)
	{
		diffuse_light += vLightColor;
	}

	//directional lights, compute diffuse color
	diffuse_light += saturate(dot(vWorldN, -vSkyLightDir)) * vSkyLightColor;

	//point lights
	#ifndef USE_LIGHTING_PASS
	diffuse_light += calculate_point_lights_diffuse(vWorldPos, vWorldN, false, false);
	#endif
	
	//apply material color
	//	Out.Color = min(1, vMaterialColor * vColor * diffuse_light);
	Out.Color = (vMaterialColor * vColor * diffuse_light);

	//shadow mapping variables
	float wNdotSun = saturate(dot(vWorldN, -vSunDir));
	Out.SunLight = (wNdotSun) * vSunColor * vMaterialColor * vColor;
	if (PcfMode != PCF_NONE)
	{
		float4 ShadowPos = mul(matSunViewProj, vWorldPos);
		Out.ShadowTexCoord = ShadowPos;
		Out.ShadowTexCoord.z /= ShadowPos.w;
		Out.ShadowTexCoord.w = 1.0f;
		Out.ShadowTexelPos = Out.ShadowTexCoord * fShadowMapSize;
		//shadow mapping variables end
	}
	
	//apply fog
	float3 P = mul(matWorldView, vPosition); //position in view space
	float d = length(P);

	Out.Fog = get_fog_amount_new(d, vWorldPos.z);
	return Out;
}

VS_OUTPUT vs_main_Instanced(uniform const int PcfMode, uniform const bool UseSecondLight, float4 vPosition : POSITION, float3 vNormal : NORMAL, float2 tc : TEXCOORD0, float4 vColor : COLOR0, float4 vLightColor : COLOR1,
							 //instance data:
						   float3   vInstanceData0 : TEXCOORD1,
						   float3   vInstanceData1 : TEXCOORD2,
						   float3   vInstanceData2 : TEXCOORD3,
						   float3   vInstanceData3 : TEXCOORD4)
{
	INITIALIZE_OUTPUT(VS_OUTPUT, Out);

	float4x4 matWorldOfInstance = build_instance_frame_matrix(vInstanceData0, vInstanceData1, vInstanceData2, vInstanceData3);
	
	//-- Out.Pos = mul(matWorldViewProj, vPosition);
    Out.Pos = mul(matWorldOfInstance, float4(vPosition.xyz, 1.0f));
    Out.Pos = mul(matViewProj, Out.Pos);

	float4 vWorldPos = (float4)mul(matWorldOfInstance,vPosition);
	float3 vWorldN = normalize(mul((float3x3)matWorldOfInstance, vNormal)); //normal in world space

	Out.Tex0 = tc;

	float4 diffuse_light = vAmbientColor;
	//   diffuse_light.rgb *= gradient_factor * (gradient_offset + vWorldN.z);

	if (UseSecondLight)
	{
		diffuse_light += vLightColor;
	}

	//directional lights, compute diffuse color
	diffuse_light += saturate(dot(vWorldN, -vSkyLightDir)) * vSkyLightColor;

	//point lights
	#ifndef USE_LIGHTING_PASS
	diffuse_light += calculate_point_lights_diffuse(vWorldPos, vWorldN, false, false);
	#endif
	
	//apply material color
	//	Out.Color = min(1, vMaterialColor * vColor * diffuse_light);
	Out.Color = (vMaterialColor * vColor * diffuse_light);

	//shadow mapping variables
	float wNdotSun = saturate(dot(vWorldN, -vSunDir));
	Out.SunLight = (wNdotSun) * vSunColor * vMaterialColor * vColor;
	if (PcfMode != PCF_NONE)
	{
		float4 ShadowPos = mul(matSunViewProj, vWorldPos);
		Out.ShadowTexCoord = ShadowPos;
		Out.ShadowTexCoord.z /= ShadowPos.w;
		Out.ShadowTexCoord.w = 1.0f;
		Out.ShadowTexelPos = Out.ShadowTexCoord * fShadowMapSize;
		//shadow mapping variables end
	}
	
	//apply fog
	float4 P = mul(matView, vWorldPos); //position in view space
	float d = length(P.xyz);

	Out.Fog = get_fog_amount_new(d, vWorldPos.z);
	return Out;
}


PS_OUTPUT ps_main(VS_OUTPUT In, uniform const int PcfMode)
{
	PS_OUTPUT Output;
	
	float4 tex_col = tex2D(MeshTextureSampler, In.Tex0);
	INPUT_TEX_GAMMA(tex_col.rgb);
	
	float sun_amount = 1.0f; 
	if ((PcfMode != PCF_NONE))
	{
		sun_amount = GetSunAmount(PcfMode, In.ShadowTexCoord, In.ShadowTexelPos);
	}
	Output.RGBColor =  tex_col * ((In.Color + In.SunLight * sun_amount));
	
	// gamma correct
	OUTPUT_GAMMA(Output.RGBColor.rgb);
	
	return Output;
}

VertexShader vs_main_compiled_PCF_NONE_true = compile vs_2_0 vs_main(PCF_NONE, true);
VertexShader vs_main_compiled_PCF_DEFAULT_true = compile vs_2_0 vs_main(PCF_DEFAULT, true);
VertexShader vs_main_compiled_PCF_NVIDIA_true = compile vs_2_a vs_main(PCF_NVIDIA, true);

VertexShader vs_main_compiled_PCF_NONE_false = compile vs_2_0 vs_main(PCF_NONE, false);
VertexShader vs_main_compiled_PCF_DEFAULT_false = compile vs_2_0 vs_main(PCF_DEFAULT, false);
VertexShader vs_main_compiled_PCF_NVIDIA_false = compile vs_2_a vs_main(PCF_NVIDIA, false);

PixelShader ps_main_compiled_PCF_NONE = compile ps_2_0 ps_main(PCF_NONE);
PixelShader ps_main_compiled_PCF_DEFAULT = compile ps_2_0 ps_main(PCF_DEFAULT);
PixelShader ps_main_compiled_PCF_NVIDIA = compile ps_2_a ps_main(PCF_NVIDIA);


technique diffuse
{
	pass P0
	{
		VertexShader = vs_main_compiled_PCF_NONE_true;
		PixelShader = ps_main_compiled_PCF_NONE;
	}
}
technique diffuse_SHDW
{
	pass P0
	{
		VertexShader = vs_main_compiled_PCF_DEFAULT_true;
		PixelShader = ps_main_compiled_PCF_DEFAULT;
	}
}
technique diffuse_SHDWNVIDIA
{
	pass P0
	{
		VertexShader = vs_main_compiled_PCF_NVIDIA_true;
		PixelShader = ps_main_compiled_PCF_NVIDIA;
	}
}
DEFINE_LIGHTING_TECHNIQUE(diffuse, 0, 0, 0, 0, 0)

technique diffuse_dynamic
{
	pass P0
	{
		VertexShader = vs_main_compiled_PCF_NONE_false;
		PixelShader = ps_main_compiled_PCF_NONE;
	}
}
technique diffuse_dynamic_SHDW
{
	pass P0
	{
		VertexShader = vs_main_compiled_PCF_DEFAULT_false;
		PixelShader = ps_main_compiled_PCF_DEFAULT;
	}
}
technique diffuse_dynamic_SHDWNVIDIA
{
	pass P0
	{
		VertexShader = vs_main_compiled_PCF_NVIDIA_false;
		PixelShader = ps_main_compiled_PCF_NVIDIA;
	}
}
DEFINE_LIGHTING_TECHNIQUE(diffuse_dynamic, 0, 0, 0, 0, 0)


technique diffuse_dynamic_Instanced
{
	pass P0
	{
		VertexShader = compile vs_2_0 vs_main_Instanced(PCF_NONE, false);
		PixelShader = ps_main_compiled_PCF_NONE;
	}
}

technique diffuse_dynamic_Instanced_SHDW
{
	pass P0
	{
		VertexShader = compile vs_2_0 vs_main_Instanced(PCF_DEFAULT, false);
		PixelShader = ps_main_compiled_PCF_DEFAULT;
	}
}

technique diffuse_dynamic_Instanced_SHDWNVIDIA
{
	pass P0
	{
		VertexShader = compile vs_2_0 vs_main_Instanced(PCF_NVIDIA, false);
		PixelShader = ps_main_compiled_PCF_NVIDIA;
	}
}

technique envmap_metal
{
	pass P0
	{
		VertexShader = vs_main_compiled_PCF_NONE_true;
		PixelShader = ps_main_compiled_PCF_NONE;
	}
}
technique envmap_metal_SHDW
{
	pass P0
	{
		VertexShader = vs_main_compiled_PCF_DEFAULT_true;
		PixelShader = ps_main_compiled_PCF_DEFAULT;
	}
}
technique envmap_metal_SHDWNVIDIA
{
	pass P0
	{
		VertexShader = vs_main_compiled_PCF_NVIDIA_true;
		PixelShader = ps_main_compiled_PCF_NVIDIA;
	}
}
DEFINE_LIGHTING_TECHNIQUE(envmap_metal, 0, 0, 0, 0, 0)






struct VS_OUTPUT_ICON_SEASONAL
{
	float4 Pos					: POSITION;
	float  Fog				    : FOG;
	
	float4 Color				: COLOR0;
	float4 Tex0					: TEXCOORD0;
	float4 SunLight				: TEXCOORD1;
	float4 ShadowTexCoord		: TEXCOORD2;
	float2 ShadowTexelPos		: TEXCOORD3;
	float4 WorldPos		: TEXCOORD4;
};

VS_OUTPUT_ICON_SEASONAL vs_main_icon_seasonal(uniform const int PcfMode, uniform const bool UseSecondLight, float4 vPosition : POSITION, float3 vNormal : NORMAL, float2 tc : TEXCOORD0, float4 vColor : COLOR0, float4 vLightColor : COLOR1)
{
	INITIALIZE_OUTPUT(VS_OUTPUT_ICON_SEASONAL, Out);

	Out.Pos = mul(matWorldViewProj, vPosition);

	float4 vWorldPos = (float4)mul(matWorld,vPosition);
	float3 vWorldN = normalize(mul((float3x3)matWorld, vNormal)); //normal in world space

	
	
	

	Out.Tex0.xy = tc;
	
	Out.Tex0.z = (0.7f * (vWorldPos.z - 1.5f));
	Out.Tex0.w = vWorldPos.x;

	

	float4 diffuse_light = vAmbientColor;
	//   diffuse_light.rgb *= gradient_factor * (gradient_offset + vWorldN.z);

	if (UseSecondLight)
	{
		diffuse_light += vLightColor;
	}

	//directional lights, compute diffuse color
	diffuse_light += saturate(dot(vWorldN, -vSkyLightDir)) * vSkyLightColor;

	//point lights
	#ifndef USE_LIGHTING_PASS
	diffuse_light += calculate_point_lights_diffuse(vWorldPos, vWorldN, false, false);
	#endif
	
	//apply material color
	//	Out.Color = min(1, vMaterialColor * vColor * diffuse_light);
	Out.Color = (vMaterialColor * vColor * diffuse_light);

	//shadow mapping variables
	float wNdotSun = saturate(dot(vWorldN, -vSunDir));
	Out.SunLight = (wNdotSun) * vSunColor * vMaterialColor * vColor;
	if (PcfMode != PCF_NONE)
	{
		float4 ShadowPos = mul(matSunViewProj, vWorldPos);
		Out.ShadowTexCoord = ShadowPos;
		Out.ShadowTexCoord.z /= ShadowPos.w;
		Out.ShadowTexCoord.w = 1.0f;
		Out.ShadowTexelPos = Out.ShadowTexCoord * fShadowMapSize;
		//shadow mapping variables end
	}
	
	//apply fog
	float3 P = mul(matWorldView, vPosition); //position in view space
	float d = length(P);

	Out.Fog = get_fog_amount_new(d, vWorldPos.z);
	return Out;
}




PS_OUTPUT ps_main_icon_seasonal(VS_OUTPUT_ICON_SEASONAL In, uniform const int PcfMode)
{
	PS_OUTPUT Output;
	
	float4 tex_col = tex2D(Diffuse2Sampler, In.Tex0.xy);
	INPUT_TEX_GAMMA(tex_col.rgb);
	float4 tex_col_snow = tex2D(MeshTextureSampler, In.Tex0);
	float snow_amount = tex2D(SpecularTextureSampler, In.Tex0.xy).a;
	

	float season = GetSeason();
	float height = In.Tex0.z;
	if (season > 2.5) //3= winter
	{
	
	height *= 2;
	height += 1;
	}
	else
	{
	height *=1;
	}
	
	snow_amount = saturate(height * (snow_amount) - 1.5f);
	float snow_present = tex2D(NormalTextureSampler, In.Tex0).r;
	snow_amount *= snow_present;
	tex_col = lerp(tex_col,tex_col_snow,snow_amount);

	
	float sun_amount = 1.0f; 
	if ((PcfMode != PCF_NONE))
	{
		sun_amount = GetSunAmount(PcfMode, In.ShadowTexCoord, In.ShadowTexelPos);
	}
	Output.RGBColor =  tex_col * ((In.Color + In.SunLight * sun_amount));
	
	// gamma correct
	OUTPUT_GAMMA(Output.RGBColor.rgb);
	
	return Output;
}



VertexShader vs_main_icon_seasonal_compiled_PCF_NONE_true = compile vs_2_0 vs_main_icon_seasonal(PCF_NONE, true);
VertexShader vs_main_icon_seasonal_compiled_PCF_DEFAULT_true = compile vs_2_0 vs_main_icon_seasonal(PCF_DEFAULT, true);
VertexShader vs_main_icon_seasonal_compiled_PCF_NVIDIA_true = compile vs_2_a vs_main_icon_seasonal(PCF_NVIDIA, true);

PixelShader ps_main_icon_seasonal_compiled_PCF_NONE = compile ps_2_0 ps_main_icon_seasonal(PCF_NONE);
PixelShader ps_main_icon_seasonal_compiled_PCF_DEFAULT = compile ps_2_0 ps_main_icon_seasonal(PCF_DEFAULT);
PixelShader ps_main_icon_seasonal_compiled_PCF_NVIDIA = compile ps_2_a ps_main_icon_seasonal(PCF_NVIDIA);



technique diffuse_icon_seasonal
{
	pass P0
	{
		VertexShader = vs_main_icon_seasonal_compiled_PCF_NONE_true;
		PixelShader = ps_main_icon_seasonal_compiled_PCF_NONE;
	}
}
technique diffuse_icon_seasonal_SHDW
{
	pass P0
	{
		VertexShader = vs_main_icon_seasonal_compiled_PCF_DEFAULT_true;
		PixelShader = ps_main_icon_seasonal_compiled_PCF_DEFAULT;
	}
}
technique diffuse_icon_seasonal_SHDWNVIDIA
{
	pass P0
	{
		VertexShader = vs_main_icon_seasonal_compiled_PCF_NVIDIA_true;
		PixelShader = ps_main_icon_seasonal_compiled_PCF_NVIDIA;
	}
}
DEFINE_LIGHTING_TECHNIQUE(diffuse_icon_seasonal, 0, 0, 0, 0, 0)






struct VS_OUTPUT_SEA_FOAM
{
	float4 Pos					: POSITION;
	float  Fog				    : FOG;
	
	float4 Color				: COLOR0;
	float4 Tex0					: TEXCOORD0;
	float4 SunLight				: TEXCOORD1;
	float4 ShadowTexCoord		: TEXCOORD2;
	float2 ShadowTexelPos		: TEXCOORD3;
	float4 WorldPos		: TEXCOORD4;
};

VS_OUTPUT_SEA_FOAM vs_main_sea_foam(uniform const int PcfMode, uniform const bool UseSecondLight, float4 vPosition : POSITION, float3 vNormal : NORMAL, float2 tc : TEXCOORD0, float4 vColor : COLOR0, float4 vLightColor : COLOR1)
{
	INITIALIZE_OUTPUT(VS_OUTPUT_SEA_FOAM, Out);

	
	
		//CUSTOM TIME VARIABLE - SET BY PHAIK
	float Timer = GetTimer(1.0f);
	
	//WAVE INFORMATION - SET BY PHAIK
	float4 WaveInfo = GetWaveInfo();
		float2 Amplitude = WaveInfo.xy;
		float2 Period = WaveInfo.zw;
	
	//INITIAL WAVE ORIGIN - SET BY PHAIK	
	float4 Origin = GetWaveOrigin();

	// Waves on y axis
  // vPosition.z = ((vPosition.z + Amplitude.y * sin(Period.y *  vPosition.y + Timer)) + Origin.y); //
   vPosition.z = (vPosition.z + Amplitude.y * sin((Period.y *  vPosition.y) + Timer) + Origin.y); //
   // Waves on x axis
  // vPosition.z = ((vPosition.z + Amplitude.x * sin(Period.x *  vPosition.x + Timer)) + Origin.x); //
   vPosition.z = (vPosition.z + Amplitude.x * sin((Period.x *  vPosition.x) + Timer) + Origin.x); //
	//OVERALL SEA LEVEL
   vPosition.z = vPosition.z + Origin.z;
	
	Out.Pos = mul(matWorldViewProj, vPosition);


	float4 vWorldPos = (float4)mul(matWorld,vPosition);
	float3 vWorldN = normalize(mul((float3x3)matWorld, vNormal)); //normal in world space

	
	
	

	Out.Tex0.xy = tc;
	
	Out.Tex0.z = (0.7f * (vWorldPos.z - 1.5f));
	Out.Tex0.w = vWorldPos.x;

	

	float4 diffuse_light = vAmbientColor;
	//   diffuse_light.rgb *= gradient_factor * (gradient_offset + vWorldN.z);

	if (UseSecondLight)
	{
		diffuse_light += vLightColor;
	}

	//directional lights, compute diffuse color
	diffuse_light += saturate(dot(vWorldN, -vSkyLightDir)) * vSkyLightColor;

	//point lights
	#ifndef USE_LIGHTING_PASS
	diffuse_light += calculate_point_lights_diffuse(vWorldPos, vWorldN, false, false);
	#endif
	
	//apply material color
	//	Out.Color = min(1, vMaterialColor * vColor * diffuse_light);
	Out.Color = (vMaterialColor * vColor * diffuse_light);

	//shadow mapping variables
	float wNdotSun = saturate(dot(vWorldN, -vSunDir));
	Out.SunLight = (wNdotSun) * vSunColor * vMaterialColor * vColor;
	if (PcfMode != PCF_NONE)
	{
		float4 ShadowPos = mul(matSunViewProj, vWorldPos);
		Out.ShadowTexCoord = ShadowPos;
		Out.ShadowTexCoord.z /= ShadowPos.w;
		Out.ShadowTexCoord.w = 1.0f;
		Out.ShadowTexelPos = Out.ShadowTexCoord * fShadowMapSize;
		//shadow mapping variables end
	}
	
	//apply fog
	float3 P = mul(matWorldView, vPosition); //position in view space
	float d = length(P);

	Out.Fog = get_fog_amount_new(d, vWorldPos.z);
	return Out;
}




PS_OUTPUT ps_main_sea_foam(VS_OUTPUT_SEA_FOAM In, uniform const int PcfMode)
{
	PS_OUTPUT Output;
	
	float4 tex_col = tex2D(MeshTextureSampler, In.Tex0.xy);
	INPUT_TEX_GAMMA(tex_col.rgb);
	
	
	
	float sun_amount = 1.0f; 
	if ((PcfMode != PCF_NONE))
	{
		sun_amount = GetSunAmount(PcfMode, In.ShadowTexCoord, In.ShadowTexelPos);
	}
	Output.RGBColor =  tex_col * ((In.Color + In.SunLight * sun_amount));
	
	// gamma correct
	OUTPUT_GAMMA(Output.RGBColor.rgb);
	
	return Output;
}



VertexShader vs_main_sea_foam_compiled_PCF_NONE_true = compile vs_2_0 vs_main_sea_foam(PCF_NONE, true);
VertexShader vs_main_sea_foam_compiled_PCF_DEFAULT_true = compile vs_2_0 vs_main_sea_foam(PCF_DEFAULT, true);
VertexShader vs_main_sea_foam_compiled_PCF_NVIDIA_true = compile vs_2_a vs_main_sea_foam(PCF_NVIDIA, true);

PixelShader ps_main_sea_foam_compiled_PCF_NONE = compile ps_2_0 ps_main_sea_foam(PCF_NONE);
PixelShader ps_main_sea_foam_compiled_PCF_DEFAULT = compile ps_2_0 ps_main_sea_foam(PCF_DEFAULT);
PixelShader ps_main_sea_foam_compiled_PCF_NVIDIA = compile ps_2_a ps_main_sea_foam(PCF_NVIDIA);



technique diffuse_sea_foam
{
	pass P0
	{
		VertexShader = vs_main_sea_foam_compiled_PCF_NONE_true;
		PixelShader = ps_main_sea_foam_compiled_PCF_NONE;
	}
}
technique diffuse_sea_foam_SHDW
{
	pass P0
	{
		VertexShader = vs_main_sea_foam_compiled_PCF_DEFAULT_true;
		PixelShader = ps_main_sea_foam_compiled_PCF_DEFAULT;
	}
}
technique diffuse_sea_foam_SHDWNVIDIA
{
	pass P0
	{
		VertexShader = vs_main_sea_foam_compiled_PCF_NVIDIA_true;
		PixelShader = ps_main_sea_foam_compiled_PCF_NVIDIA;
	}
}
DEFINE_LIGHTING_TECHNIQUE(diffuse_sea_foam, 0, 0, 0, 0, 0)






//-----
struct VS_OUTPUT_BUMP
{
	float4 Pos					: POSITION;
	float4 VertexColor			: COLOR0;
	float2 Tex0					: TEXCOORD0;
	float3 SunLightDir			: TEXCOORD1;//sun light dir in pixel coordinates
	float3 SkyLightDir			: TEXCOORD2;//light diffuse for bump
	float4 PointLightDir		: TEXCOORD3;//light ambient for bump
	float4 ShadowTexCoord		: TEXCOORD4;
	float2 ShadowTexelPos		: TEXCOORD5;
	float  Fog					: FOG;
	
	float3 ViewDir				: TEXCOORD6;
	float3 WorldNormal			: TEXCOORD7;
};
VS_OUTPUT_BUMP vs_main_bump (uniform const int PcfMode, float4 vPosition : POSITION, float3 vNormal : NORMAL, float2 tc : TEXCOORD0,  float3 vTangent : TANGENT, float3 vBinormal : BINORMAL, float4 vVertexColor : COLOR0, float4 vPointLightDir : COLOR1)
{
	INITIALIZE_OUTPUT(VS_OUTPUT_BUMP, Out);

	Out.Pos = mul(matWorldViewProj, vPosition);
	Out.Tex0 = tc;


	float3 vWorldN = normalize(mul((float3x3)matWorld, vNormal)); //normal in world space
	float3 vWorld_binormal = normalize(mul((float3x3)matWorld, vBinormal)); //normal in world space
	float3 vWorld_tangent  = normalize(mul((float3x3)matWorld, vTangent)); //normal in world space

	float3 P = mul(matWorldView, vPosition); //position in view space

	float3x3 TBNMatrix = float3x3(vWorld_tangent, vWorld_binormal, vWorldN); 

	float4 vWorldPos = (float4)mul(matWorld,vPosition);
	if (PcfMode != PCF_NONE)
	{	
		float4 ShadowPos = mul(matSunViewProj, vWorldPos);
		Out.ShadowTexCoord = ShadowPos;
		Out.ShadowTexCoord.z /= ShadowPos.w;
		Out.ShadowTexCoord.w = 1.0f;
		Out.ShadowTexelPos = Out.ShadowTexCoord * fShadowMapSize;
		//shadow mapping variables end
	}

	Out.SunLightDir = mul(TBNMatrix, -vSunDir);
	Out.SkyLightDir = mul(TBNMatrix, -vSkyLightDir);
	
	#ifdef USE_LIGHTING_PASS
	Out.PointLightDir = vWorldPos;
	#else
	Out.PointLightDir.rgb = 2.0f * vPointLightDir.rgb - 1.0f;
	Out.PointLightDir.a = vPointLightDir.a;
	#endif
	
	Out.VertexColor = vVertexColor;
	
	//STR: note that these are not in TBN space.. (used for fresnel only..)
	Out.ViewDir = normalize(vCameraPos.xyz - vWorldPos.xyz); //normalize(mul(TBNMatrix, (vCameraPos.xyz - vWorldPos.xyz) ));	// 
	//Out.ViewDir = mul(TBNMatrix, Out.ViewDir);

	Out.WorldNormal = vWorldN;
	//Out.WorldNormal = mul(TBNMatrix, Out.WorldNormal);

	//apply fog
	float d = length(P);
	Out.Fog = get_fog_amount_new(d, vWorldPos.z);

	return Out;
}
PS_OUTPUT ps_main_bump( VS_OUTPUT_BUMP In, uniform const int PcfMode )
{ 
	PS_OUTPUT Output;
	
	float4 total_light = vAmbientColor;//In.LightAmbient;
	
	float3 normal;
	normal.xy = (2.0f * tex2D(NormalTextureSampler, In.Tex0).ag - 1.0f);
	normal.z = sqrt(1.0f - dot(normal.xy, normal.xy));
	
	/*
	const bool use_detail_normalmap = debug_vector.z > 1.0f;
	if(use_detail_normalmap)
	{
		float3 detail_normal = tex2D(Diffuse2Sampler, In.Tex0*debug_vector.y).rgb;
		//normal = lerp(normal, detail_normal, debug_vector.z);
		//normal = normalize(normal);
		
		float3x3 normal_frame; 
		normal_frame[2] = normal;
		normal_frame[1] = float3(0,1,0);
		normal_frame[0] = cross(normal_frame[1], normal_frame[2]);
		//normal_frame[0] = normalize(normal_frame[0]);
		normal_frame[1] = cross(normal_frame[2], normal_frame[0]);
		
		normal = mul(detail_normal, normal_frame);
	}
	*/

	if (PcfMode != PCF_NONE)
	{
		float sun_amount = 0.03f + GetSunAmount(PcfMode, In.ShadowTexCoord, In.ShadowTexelPos);
		total_light += ((saturate(dot(In.SunLightDir.xyz, normal.xyz)) * (sun_amount))) * vSunColor;
	}
	else
	{
		total_light += saturate(dot(In.SunLightDir.xyz, normal.xyz)) * vSunColor;
	}
	total_light += saturate(dot(In.SkyLightDir.xyz, normal.xyz)) * vSkyLightColor;
	
	#ifndef USE_LIGHTING_PASS
		total_light += saturate(dot(In.PointLightDir.xyz, normal.xyz)) * vPointLightColor;
	#endif

	Output.RGBColor.rgb = total_light.rgb;
	Output.RGBColor.a = 1.0f;
	Output.RGBColor *= vMaterialColor;
	
	float4 tex_col = tex2D(MeshTextureSampler, In.Tex0);
	INPUT_TEX_GAMMA(tex_col.rgb);

	Output.RGBColor *= tex_col;
	Output.RGBColor *= In.VertexColor;
	
	//	Output.RGBColor = saturate(Output.RGBColor);
	OUTPUT_GAMMA(Output.RGBColor.rgb);

	return Output;
}
PS_OUTPUT ps_main_bump_simple( VS_OUTPUT_BUMP In, uniform const int PcfMode )
{ 
	PS_OUTPUT Output;
	
	float4 total_light = vAmbientColor;//In.LightAmbient;
/*-	//Parallax mapping:
	//float viewVec_len = length(In.ViewDir);
	//float3 viewVec = In.ViewDir / viewVec_len;
	float3 viewVec = normalize(In.ViewDir);
	{
		float2 plxCoeffs = float2(0.04, -0.02) * debug_vector.w;
		float height = tex2D(NormalTextureSampler, In.Tex0).a;
		float offset = height * plxCoeffs.x + plxCoeffs.y;
		In.Tex0 = In.Tex0 + offset * viewVec.xy;
	}
*/
	
	float3 normal = (2.0f * tex2D(NormalTextureSampler, In.Tex0).rgb - 1.0f);

	float sun_amount = 1.0f;
	if (PcfMode != PCF_NONE)
	{
		if (PcfMode == PCF_NVIDIA)
			sun_amount = saturate( 0.15f + GetSunAmount(PcfMode, In.ShadowTexCoord, In.ShadowTexelPos) );
		else
			sun_amount = GetSunAmount(PcfMode, In.ShadowTexCoord, In.ShadowTexelPos);	//cannot fit 64 instruction
	}
	total_light += ((saturate(dot(In.SunLightDir.xyz, normal.xyz)) * (sun_amount * sun_amount))) * vSunColor;
	
	total_light += saturate(dot(In.SkyLightDir.xyz, normal.xyz)) * vSkyLightColor;
	#ifndef USE_LIGHTING_PASS
		total_light += saturate(dot(In.PointLightDir.xyz, normal.xyz)) * vPointLightColor;
	#endif

	Output.RGBColor.rgb = total_light.rgb;
	Output.RGBColor.a = 1.0f;
	Output.RGBColor *= vMaterialColor;
	
	float4 tex_col = tex2D(MeshTextureSampler, In.Tex0);
	INPUT_TEX_GAMMA(tex_col.rgb);

	Output.RGBColor *= tex_col;
	Output.RGBColor *= In.VertexColor;
	
	//	Output.RGBColor = saturate(Output.RGBColor);
	
	
	float fresnel = 1-(saturate(dot( In.ViewDir, In.WorldNormal)));
	//-float fresnel = 1-(saturate(dot( viewVec, In.WorldNormal)));

	// Output.RGBColor.rgb *= fresnel; 
	Output.RGBColor.rgb *= max(0.6,fresnel*fresnel+0.1); 
	
	Output.RGBColor.rgb = OUTPUT_GAMMA(Output.RGBColor.rgb);


	return Output;
}


PS_OUTPUT ps_main_bump_season( VS_OUTPUT_BUMP In, uniform const int PcfMode )
{ 
	PS_OUTPUT Output;
	
	float4 total_light = vAmbientColor;//In.LightAmbient;
/*-	//Parallax mapping:
	//float viewVec_len = length(In.ViewDir);
	//float3 viewVec = In.ViewDir / viewVec_len;
	float3 viewVec = normalize(In.ViewDir);
	{
		float2 plxCoeffs = float2(0.04, -0.02) * debug_vector.w;
		float height = tex2D(NormalTextureSampler, In.Tex0).a;
		float offset = height * plxCoeffs.x + plxCoeffs.y;
		In.Tex0 = In.Tex0 + offset * viewVec.xy;
	}
*/
	
	float3 normal = (2.0f * tex2D(NormalTextureSampler, In.Tex0).rgb - 1.0f);

	float sun_amount = 1.0f;
	if (PcfMode != PCF_NONE)
	{
		if (PcfMode == PCF_NVIDIA)
			sun_amount = saturate( 0.15f + GetSunAmount(PcfMode, In.ShadowTexCoord, In.ShadowTexelPos) );
		else
			sun_amount = GetSunAmount(PcfMode, In.ShadowTexCoord, In.ShadowTexelPos);	//cannot fit 64 instruction
	}
	total_light += ((saturate(dot(In.SunLightDir.xyz, normal.xyz)) * (sun_amount * sun_amount))) * vSunColor;
	
	total_light += saturate(dot(In.SkyLightDir.xyz, normal.xyz)) * vSkyLightColor;
	#ifndef USE_LIGHTING_PASS
		total_light += saturate(dot(In.PointLightDir.xyz, normal.xyz)) * vPointLightColor;
	#endif

	Output.RGBColor.rgb = total_light.rgb;
	Output.RGBColor.a = 1.0f;
	Output.RGBColor *= vMaterialColor;
	
	float4 tex_col = tex2D(MeshTextureSampler, In.Tex0);
	
	float season = GetSeason();
	
	if (season < 0.5) //0= spring
	{
	tex_col.rgb *= float3(0.9,1.1,0.9);
	}
	else if ((season > 0.5)&&(season < 1.5)) //1= summer
	{
	tex_col.rgb *= float3(1.0,1.0,1.0);
	}
	else if ((season > 1.5)&&(season < 2.5)) //2= autumn
	{
	tex_col.rgb *= float3(1.1,0.9,0.9);
	}
	else if ((season > 2.5)) //3= winter
	{
	tex_col = tex2D(SpecularTextureSampler, In.Tex0);
	}
////
	
	
	INPUT_TEX_GAMMA(tex_col.rgb);

	Output.RGBColor *= tex_col;
	Output.RGBColor *= In.VertexColor;
	
	//	Output.RGBColor = saturate(Output.RGBColor);
	
	
	float fresnel = 1-(saturate(dot( In.ViewDir, In.WorldNormal)));
	//-float fresnel = 1-(saturate(dot( viewVec, In.WorldNormal)));

	// Output.RGBColor.rgb *= fresnel; 
	Output.RGBColor.rgb *= max(0.6,fresnel*fresnel+0.1); 
	
	Output.RGBColor.rgb = OUTPUT_GAMMA(Output.RGBColor.rgb);


	return Output;
}



PS_OUTPUT ps_main_bump_simple_multitex( VS_OUTPUT_BUMP In, uniform const int PcfMode )
{ 
	PS_OUTPUT Output;
	
	float4 total_light = vAmbientColor;//In.LightAmbient;
	
	float4 tex_col = tex2D(MeshTextureSampler, In.Tex0);
	float4 tex_col2 = tex2D(Diffuse2Sampler, In.Tex0 * uv_2_scale);
	
	float4 multi_tex_col = tex_col;
	float inv_alpha = (1.0f - In.VertexColor.a);
	multi_tex_col.rgb *= inv_alpha;
	multi_tex_col.rgb += tex_col2.rgb * In.VertexColor.a;
	
	//!!
	INPUT_TEX_GAMMA(multi_tex_col.rgb);

	float3 normal = (2.0f * tex2D(NormalTextureSampler, In.Tex0).rgb - 1.0f);

	float sun_amount = 1.0f;
	if (PcfMode != PCF_NONE)
	{
		if (PcfMode == PCF_NVIDIA)
			sun_amount = saturate( 0.15f + GetSunAmount(PcfMode, In.ShadowTexCoord, In.ShadowTexelPos) );
		else
			sun_amount = GetSunAmount(PcfMode, In.ShadowTexCoord, In.ShadowTexelPos);	//cannot fit 64 instruction
	}
	total_light += (saturate(dot(In.SunLightDir.xyz, normal.xyz)) * (sun_amount)) * vSunColor;
	
	total_light += saturate(dot(In.SkyLightDir.xyz, normal.xyz)) * vSkyLightColor;
	#ifndef USE_LIGHTING_PASS
		total_light += saturate(dot(In.PointLightDir.xyz, normal.xyz)) * vPointLightColor;
	#endif

	Output.RGBColor.rgb = total_light.rgb;
	Output.RGBColor.a = 1.0f;
	//	Output.RGBColor *= vMaterialColor;
	

	
	Output.RGBColor *= multi_tex_col;
	Output.RGBColor.rgb *= In.VertexColor.rgb;
	Output.RGBColor.a *= In.PointLightDir.a;
	
	
	float fresnel = 1-(saturate(dot( normalize(In.ViewDir), normalize(In.WorldNormal))));
	// Output.RGBColor.rgb *= fresnel; 
	Output.RGBColor.rgb *= max(0.6,fresnel*fresnel+0.1); 
	OUTPUT_GAMMA(Output.RGBColor.rgb);
	
	
	return Output;
}








const float2 TreeAmplitude = float2(0.9,1);
const float2 TreePeriod = float2(0.025,100);
const float tree_rate = float(1.5);

VS_OUTPUT_BUMP vs_main_bump_bark (uniform const int PcfMode, float4 vPosition : POSITION, float3 vNormal : NORMAL, float2 tc : TEXCOORD0,  float3 vTangent : TANGENT, float3 vBinormal : BINORMAL, float4 vVertexColor : COLOR0, float4 vPointLightDir : COLOR1)
{
	INITIALIZE_OUTPUT(VS_OUTPUT_BUMP, Out);

	float4 WorldPosit = (float4)mul(matWorld,vPosition);
	float WindFactor = 0.333 * GetWindAmountNew(1.0f, vPosition.z); //range of 0 to 3
	
	
	if(tc.y < 0.90)
	{
	float timer_variable = tree_rate * time_var;
	float2 WorldPosition = float2(WorldPosit.z,WorldPosit.y);//float2((matWorldViewProj,vPosition.x),(matWorldViewProj,vPosition.y));
	float2 OriginalPosition = float2(vPosition.x,vPosition.y);
	//(1-tc.y)+0.2 //1 at highest point, 0 at lowest -  ( +0.2)
	//saturate(pow((1-tc.y)+0.2,3)); //factor effects conrtast
	

	float treeamp = (saturate(pow((1-tc.y)+0.2,2))) * TreeAmplitude.x;
	treeamp *= WindFactor;
	//treeamp = lerp(TreeAmplitude.x,treeamp,float4(mul(matWorldViewProj, vPosition)).z);
	vPosition.x = vPosition.x + treeamp * sin(TreePeriod.x *  WorldPosition.x + (timer_variable)); //
	
	vPosition.x = vPosition.x + treeamp * sin((TreePeriod.x * 0.5)  * WorldPosition.x + (0.2*timer_variable)); //
	vPosition.y = vPosition.y + treeamp * sin((TreePeriod.x * 0.76)  * WorldPosition.x + (1.1*timer_variable)); //
	
	vPosition.z -= 0.3*sqrt(pow((OriginalPosition.x-vPosition.x),2));
	//vPosition.z = vPosition.z + TreeAmplitude.x * sin(TreePeriod.x *  WorldPosition.x + timer_variable); //
	}
	
	Out.Pos = mul(matWorldViewProj, vPosition);
	Out.Tex0 = tc;

	float4 vWorldPos = (float4)mul(matWorld,vPosition);
	
	float3 vWorldN = normalize(mul((float3x3)matWorld, vNormal)); //normal in world space
	float3 vWorld_binormal = normalize(mul((float3x3)matWorld, vBinormal)); //normal in world space
	float3 vWorld_tangent  = normalize(mul((float3x3)matWorld, vTangent)); //normal in world space

	float3 P = mul(matWorldView, vPosition); //position in view space

	float3x3 TBNMatrix = float3x3(vWorld_tangent, vWorld_binormal, vWorldN); 

	if (PcfMode != PCF_NONE)
	{	
		float4 ShadowPos = mul(matSunViewProj, vWorldPos);
		Out.ShadowTexCoord = ShadowPos;
		Out.ShadowTexCoord.z /= ShadowPos.w;
		Out.ShadowTexCoord.w = 1.0f;
		Out.ShadowTexelPos = Out.ShadowTexCoord * fShadowMapSize;
		//shadow mapping variables end
	}

	Out.SunLightDir = mul(TBNMatrix, -vSunDir);
	Out.SkyLightDir = mul(TBNMatrix, -vSkyLightDir);
	
	#ifdef USE_LIGHTING_PASS
	Out.PointLightDir = vWorldPos;
	#else
	Out.PointLightDir.rgb = 2.0f * vPointLightDir.rgb - 1.0f;
	Out.PointLightDir.a = vPointLightDir.a;
	#endif
	
	Out.VertexColor = vVertexColor;
	
	//STR: note that these are not in TBN space.. (used for fresnel only..)
	Out.ViewDir = normalize(vCameraPos.xyz - vWorldPos.xyz); //normalize(mul(TBNMatrix, (vCameraPos.xyz - vWorldPos.xyz) ));	// 
	//Out.ViewDir = mul(TBNMatrix, Out.ViewDir);

	Out.WorldNormal = vWorldN;
	//Out.WorldNormal = mul(TBNMatrix, Out.WorldNormal);

	//apply fog
	float d = length(P);
	Out.Fog = get_fog_amount_new(d, vWorldPos.z);

	return Out;
}




PS_OUTPUT ps_main_bump_bark( VS_OUTPUT_BUMP In, uniform const int PcfMode )
{ 
	PS_OUTPUT Output;
	
	float4 total_light = vAmbientColor;//In.LightAmbient;
/*-	//Parallax mapping:
	//float viewVec_len = length(In.ViewDir);
	//float3 viewVec = In.ViewDir / viewVec_len;
	float3 viewVec = normalize(In.ViewDir);
	{
		float2 plxCoeffs = float2(0.04, -0.02) * debug_vector.w;
		float height = tex2D(NormalTextureSampler, In.Tex0).a;
		float offset = height * plxCoeffs.x + plxCoeffs.y;
		In.Tex0 = In.Tex0 + offset * viewVec.xy;
	}
*/
	
	float3 normal = 0.25*(2.0f * tex2D(NormalTextureSampler, In.Tex0).rgb - 1.0f);

	float sun_amount = 1.0f;
	if (PcfMode != PCF_NONE)
	{
		if (PcfMode == PCF_NVIDIA)
			sun_amount = saturate( 0.15f + GetSunAmount(PcfMode, In.ShadowTexCoord, In.ShadowTexelPos) );
		else
			sun_amount = GetSunAmount(PcfMode, In.ShadowTexCoord, In.ShadowTexelPos);	//cannot fit 64 instruction
	}
	total_light += ((saturate(dot(In.SunLightDir.xyz, normal.xyz)) * (sun_amount * sun_amount))) * vSunColor;
	
	total_light += saturate(dot(In.SkyLightDir.xyz, normal.xyz)) * vSkyLightColor;
	#ifndef USE_LIGHTING_PASS
		total_light += saturate(dot(In.PointLightDir.xyz, normal.xyz)) * vPointLightColor;
	#endif

	Output.RGBColor.rgb = total_light.rgb;
	Output.RGBColor.a = 1.0f;
	Output.RGBColor *= vMaterialColor;
	
	float4 tex_col = tex2D(MeshTextureSampler, In.Tex0);
	INPUT_TEX_GAMMA(tex_col.rgb);

	Output.RGBColor *= tex_col;
	Output.RGBColor *= In.VertexColor;
	
	//	Output.RGBColor = saturate(Output.RGBColor);
	
	
	float fresnel = 1-(saturate(dot( In.ViewDir, In.WorldNormal)));
	//-float fresnel = 1-(saturate(dot( viewVec, In.WorldNormal)));

	// Output.RGBColor.rgb *= fresnel; 
	Output.RGBColor.rgb *= max(0.6,fresnel*fresnel+0.1); 
	
	Output.RGBColor.rgb = OUTPUT_GAMMA(Output.RGBColor.rgb);


	return Output;
}




VertexShader vs_main_bump_compiled_PCF_NONE = compile vs_2_0 vs_main_bump(PCF_NONE);
VertexShader vs_main_bump_compiled_PCF_DEFAULT = compile vs_2_0 vs_main_bump(PCF_DEFAULT);
VertexShader vs_main_bump_compiled_PCF_NVIDIA = compile vs_2_a vs_main_bump(PCF_NVIDIA);

VertexShader vs_main_bump_bark_compiled_PCF_NONE = compile vs_2_0 vs_main_bump_bark(PCF_NONE);
VertexShader vs_main_bump_bark_compiled_PCF_DEFAULT = compile vs_2_0 vs_main_bump_bark(PCF_DEFAULT);
VertexShader vs_main_bump_bark_compiled_PCF_NVIDIA = compile vs_2_a vs_main_bump_bark(PCF_NVIDIA);


technique bumpmap
{
	pass P0
	{
		VertexShader = vs_main_bump_compiled_PCF_NONE;
		PixelShader = compile ps_2_0 ps_main_bump(PCF_NONE);
	}
}
technique bumpmap_SHDW
{
	pass P0
	{
		VertexShader = vs_main_bump_compiled_PCF_DEFAULT;
		PixelShader = compile ps_2_0 ps_main_bump(PCF_DEFAULT);
	}
}
technique bumpmap_SHDWNVIDIA
{
	pass P0
	{
		VertexShader = vs_main_bump_compiled_PCF_NVIDIA;
		PixelShader = compile ps_2_a ps_main_bump(PCF_NVIDIA);
	}
}

DEFINE_LIGHTING_TECHNIQUE(bumpmap, 1, 1, 0, 0, 0)

//-----
technique dot3
{
	pass P0
	{
		VertexShader = vs_main_bump_compiled_PCF_NONE;
		PixelShader = compile ps_2_0 ps_main_bump_simple(PCF_NONE);
	}
}
technique dot3_SHDW
{
	pass P0
	{
		VertexShader = vs_main_bump_compiled_PCF_DEFAULT;
		PixelShader = compile ps_2_0 ps_main_bump_simple(PCF_DEFAULT);
	}
}
technique dot3_SHDWNVIDIA
{
	pass P0
	{
		VertexShader = vs_main_bump_compiled_PCF_NVIDIA;
		PixelShader = compile ps_2_a ps_main_bump_simple(PCF_NVIDIA);
	}
}
DEFINE_LIGHTING_TECHNIQUE(dot3, 0, 1, 0, 0, 0)
//-----
technique dot3_multitex
{
	pass P0
	{
		VertexShader = vs_main_bump_compiled_PCF_NONE;
		PixelShader = compile ps_2_0 ps_main_bump_simple_multitex(PCF_NONE);
	}
}
technique dot3_multitex_SHDW
{
	pass P0
	{
		VertexShader = vs_main_bump_compiled_PCF_DEFAULT;
		PixelShader = compile ps_2_0 ps_main_bump_simple_multitex(PCF_DEFAULT);
	}
}
technique dot3_multitex_SHDWNVIDIA
{
	pass P0
	{
		VertexShader = vs_main_bump_compiled_PCF_NVIDIA;
		PixelShader = compile ps_2_a ps_main_bump_simple_multitex(PCF_NVIDIA);
	}
}
DEFINE_LIGHTING_TECHNIQUE(dot3_multitex, 0, 1, 0, 0, 0)


//-----
technique dot3_season
{
	pass P0
	{
		VertexShader = vs_main_bump_compiled_PCF_NONE;
		PixelShader = compile ps_2_0 ps_main_bump_season(PCF_NONE);
	}
}
technique dot3_season_SHDW
{
	pass P0
	{
		VertexShader = vs_main_bump_compiled_PCF_DEFAULT;
		PixelShader = compile ps_2_0 ps_main_bump_season(PCF_DEFAULT);
	}
}
technique dot3_season_SHDWNVIDIA
{
	pass P0
	{
		VertexShader = vs_main_bump_compiled_PCF_NVIDIA;
		PixelShader = compile ps_2_a ps_main_bump_season(PCF_NVIDIA);
	}
}
DEFINE_LIGHTING_TECHNIQUE(dot3_season, 0, 1, 0, 0, 0)
//-----








///
/////////////TREE BARK SHADER
//-----
technique dot3_bark
{
	pass P0
	{
		VertexShader = vs_main_bump_bark_compiled_PCF_NONE;
		PixelShader = compile ps_2_0 ps_main_bump_bark(PCF_NONE);
	}
}
technique dot3_bark_SHDW
{
	pass P0
	{
		VertexShader = vs_main_bump_bark_compiled_PCF_DEFAULT;
		PixelShader = compile ps_2_0 ps_main_bump_bark(PCF_DEFAULT);
	}
}
technique dot3_bark_SHDWNVIDIA
{
	pass P0
	{
		VertexShader = vs_main_bump_bark_compiled_PCF_NVIDIA;
		PixelShader = compile ps_2_a ps_main_bump_bark(PCF_NVIDIA);
	}
}
DEFINE_LIGHTING_TECHNIQUE(dot3_bark, 0, 1, 0, 0, 0)
//-----











//-----
struct VS_OUTPUT_PARALLAX
{
	float4 Pos					: POSITION;
	float4 VertexColor			: COLOR0;
	float2 Tex0					: TEXCOORD0;
	float3 SunLightDir			: TEXCOORD1;//sun light dir in pixel coordinates
	float3 SkyLightDir			: TEXCOORD2;//light diffuse for bump
	float4 PointLightDir		: TEXCOORD3;//light ambient for bump
	float4 ShadowTexCoord		: TEXCOORD4;
	float2 ShadowTexelPos		: TEXCOORD5;
	
	float3 ViewDir				: TEXCOORD6;
	float4 WorldNormal			: TEXCOORD7;
	float  Fog					: FOG;
};
VS_OUTPUT_PARALLAX vs_main_parallax (uniform const int PcfMode, float4 vPosition : POSITION, float3 vNormal : NORMAL, float2 tc : TEXCOORD0,  float3 vTangent : TANGENT, float3 vBinormal : BINORMAL, float4 vVertexColor : COLOR0, float4 vPointLightDir : COLOR1)
{
	INITIALIZE_OUTPUT(VS_OUTPUT_PARALLAX, Out);

	Out.Pos = mul(matWorldViewProj, vPosition);
	Out.Tex0 = tc;


	float3 vWorldN = normalize(mul((float3x3)matWorld, vNormal)); //normal in world space
	float3 vWorld_binormal = normalize(mul((float3x3)matWorld, vBinormal)); //normal in world space
	float3 vWorld_tangent  = normalize(mul((float3x3)matWorld, vTangent)); //normal in world space

	float3 P = mul(matWorldView, vPosition); //position in view space

	float3x3 TBNMatrix = float3x3(vWorld_tangent, vWorld_binormal, vWorldN); 

	float4 vWorldPos = (float4)mul(matWorld,vPosition);
	if (PcfMode != PCF_NONE)
	{	
		float4 ShadowPos = mul(matSunViewProj, vWorldPos);
		Out.ShadowTexCoord = ShadowPos;
		Out.ShadowTexCoord.z /= ShadowPos.w;
		Out.ShadowTexCoord.w = 1.0f;
		Out.ShadowTexelPos = Out.ShadowTexCoord * fShadowMapSize;
		//shadow mapping variables end
	}

	Out.SunLightDir = mul(TBNMatrix, -vSunDir);
	Out.SkyLightDir = mul(TBNMatrix, -vSkyLightDir);
	
	#ifdef USE_LIGHTING_PASS
	Out.PointLightDir = vWorldPos;
	#else
	Out.PointLightDir.rgb = 2.0f * vPointLightDir.rgb - 1.0f;
	Out.PointLightDir.a = vPointLightDir.a;
	#endif
	
	Out.VertexColor = vVertexColor;
	
	//insert from parallax shader
	//float3 vViewDir = normalize(vCameraPos.xyz - vWorldPos.xyz); //normalize(mul(TBNMatrix, (vCameraPos.xyz - vWorldPos.xyz) ));	// 
    // yay for TBN space
   // vViewDir = (mul(TBNMatrix, vViewDir));
   // Out.ViewDir = vViewDir;
	
	float3 vViewDir = normalize(vCameraPos.xyz - vWorldPos.xyz); //normalize(mul(TBNMatrix, (vCameraPos.xyz - vWorldPos.xyz) ));	// 

    vViewDir = normalize(mul(TBNMatrix, vViewDir));
    // only return viewdir for parallax.
    Out.ViewDir = vViewDir;

	Out.WorldNormal.xyz = vWorldN;
	Out.WorldNormal.w = 1-(saturate(dot(vViewDir, vWorldN))); //.z is fresnel

	//apply fog
	float d = length(P);
	Out.Fog = get_fog_amount_new(d, vWorldPos.z);

	return Out;
}








PS_OUTPUT ps_main_parallax( VS_OUTPUT_PARALLAX In, uniform const int PcfMode )
{ 
	PS_OUTPUT Output;
	
	float4 total_light = vAmbientColor;//In.LightAmbient;

	
	//float HeightMapScale = 0.01;
		
	//float2 ParallaxOffsetTangentSpace = In.ViewTangentSpace.xy / In.ViewTangentSpace.z;	
	//ParallaxOffsetTangentSpace *= HeightMapScale;
	
	
	
//PARALLAX SECTION
	
	float2 viewpara = In.ViewDir.xy;
  {
    float factor = (0.01f * 6.3);//vSpecularColor.x);
    float BIAS = (factor * -0.5f);//-0.02; 
    float SCALE = factor;//0.04;
    
    // Parallax with offset limiting, Using the normal blue channel to take slope information into account.
    float4 Normal = tex2D(SpecularTextureSampler, In.Tex0);
    float h = Normal.a * SCALE + BIAS;
    In.Tex0.xy += h * Normal.z * viewpara; 
  }
  
//PARALLAX END


	
	
	
	
	

//NORMALMAPPING
	float3 normal;
	//normalmap type
	float rgb_or_green = tex2D(NormalTextureSampler, float2(0.5,0.5)).r;
		if (rgb_or_green > 0.005)
			{
				normal = (2.0f * tex2D(NormalTextureSampler, In.Tex0).rgb - 1.0f);
			}
		else
			{
				normal.xy = (2.0h * tex2D(NormalTextureSampler, In.Tex0).ag - 1.0h);
				normal.z = sqrt(1.0f - dot(normal.xy, normal.xy));
			}


//LIGHTING////			
	float sun_amount = 1.0f;
	if (PcfMode != PCF_NONE)
	{
		if (PcfMode == PCF_NVIDIA)
			sun_amount = saturate( 0.15f + GetSunAmount(PcfMode, In.ShadowTexCoord, In.ShadowTexelPos) );
		else
			sun_amount = GetSunAmount(PcfMode, In.ShadowTexCoord, In.ShadowTexelPos);	//cannot fit 64 instruction
	}
	total_light += ((saturate(dot(In.SunLightDir.xyz, normal.xyz)) * (sun_amount * sun_amount))) * vSunColor;
	
	total_light += saturate(dot(In.SkyLightDir.xyz, normal.xyz)) * vSkyLightColor;
	#ifndef USE_LIGHTING_PASS
		total_light += saturate(dot(In.PointLightDir.xyz, normal.xyz)) * vPointLightColor;
	#endif

	//fresnel
	
	float3 vView = normalize(In.ViewDir);
	float3 fresnel = 1-(saturate(dot(vView, normal)));
	fresnel = 0.0204f + 0.9796 * (fresnel * fresnel * fresnel* fresnel * fresnel);
	total_light.rgb += 0.5*(total_light*fresnel); 
	total_light = saturate(total_light);
	
///////////	
	
	
	Output.RGBColor.rgb = total_light.rgb;
	Output.RGBColor.a = 1.0f;
	Output.RGBColor *= vMaterialColor;
	
	float4 tex_col = tex2D(MeshTextureSampler, In.Tex0);
	
/////
	float season = GetSeason();
	
	if (season < 0.5) //0= spring
	{
	tex_col.rgb *= float3(0.9,1.1,0.9);
	}
	else if ((season > 0.5)&&(season < 1.5)) //1= summer
	{
	tex_col.rgb *= float3(1.0,1.0,1.0);
	}
	else if ((season > 1.5)&&(season < 2.5)) //2= autumn
	{
	tex_col.rgb *= float3(1.1,0.9,0.9);
	}
	else if ((season > 2.5)) //3= winter
	{
	float greyscale = dot(tex_col.rgb, float3(0.3, 0.59, 0.11));
	tex_col.rgb = lerp(greyscale,tex_col.rgb,0.75);
	float h = pow(tex2D(SpecularTextureSampler, In.Tex0).a,2);
	h = saturate(h + 0.5);
	  h = 1;
	float3 snow = tex2D(EnvTextureSampler, In.Tex0).rgb;
	tex_col.rgb = lerp(tex_col.rgb,snow,h);
	}
////

	INPUT_TEX_GAMMA(tex_col.rgb);

	Output.RGBColor *= tex_col;
	Output.RGBColor *= In.VertexColor;
	
	//	Output.RGBColor = saturate(Output.RGBColor);
	
	if ((season < 2.5)) //  not winter (3= winter)
	{
	//parallax height darkening
	float light_intenisty = dot(total_light.rgb, float3(0.3, 0.59, 0.11));
	Output.RGBColor.rgb = lerp(Output.RGBColor.rgb,	(Output.RGBColor.rgb * (0.35+fresnel)),light_intenisty);
	
	
	float h = tex2D(SpecularTextureSampler, In.Tex0).a;
	Output.RGBColor.rgb = lerp(Output.RGBColor.rgb*0.75,Output.RGBColor.rgb*1.2,h);
	}
	else
	{
	float light_intenisty = dot(total_light.rgb, float3(0.3, 0.59, 0.11));
	float3 outcolour = lerp(Output.RGBColor.rgb,	(Output.RGBColor.rgb * (0.35+fresnel)),light_intenisty);
	Output.RGBColor.rgb = lerp(Output.RGBColor.rgb,	outcolour,0.5);
	
	float h = tex2D(SpecularTextureSampler, In.Tex0).a;
	Output.RGBColor.rgb = lerp(Output.RGBColor.rgb,Output.RGBColor.rgb*1.2,h);
	}

	//
	
	
	
	Output.RGBColor.rgb = OUTPUT_GAMMA(Output.RGBColor.rgb);


	return Output;
}
PS_OUTPUT ps_main_parallax_multitex( VS_OUTPUT_BUMP In, uniform const int PcfMode )
{ 
	PS_OUTPUT Output;
	
	float4 total_light = vAmbientColor;//In.LightAmbient;
	
	
	
	
//PARALLAX SECTION
	
	float2 viewpara = In.ViewDir.xy;
  {
    float factor = (0.01f * 6.3);//vSpecularColor.x);
    float BIAS = (factor * -0.5f);//-0.02; 
    float SCALE = factor;//0.04;
    
    // Parallax with offset limiting, Using the normal blue channel to take slope information into account.
    float4 Normal = tex2D(SpecularTextureSampler, In.Tex0);
    float h = Normal.a * SCALE + BIAS;
    In.Tex0.xy += h * Normal.z * viewpara; 
  }
  
//PARALLAX END
	
	

//NORMALMAPPING
	float3 normal;
	//normalmap type
	float rgb_or_green = tex2D(NormalTextureSampler, float2(0.5,0.5)).r;
		if (rgb_or_green > 0.005)
			{
				normal = (2.0f * tex2D(NormalTextureSampler, In.Tex0).rgb - 1.0f);
			}
		else
			{
				normal.xy = (2.0h * tex2D(NormalTextureSampler, In.Tex0).ag - 1.0h);
				normal.z = sqrt(1.0f - dot(normal.xy, normal.xy));
			}


//LIGHTING////			
	
	float4 tex_col = tex2D(MeshTextureSampler, In.Tex0);
	float4 tex_col2 = tex2D(Diffuse2Sampler, In.Tex0 * uv_2_scale);
	
	float4 multi_tex_col = tex_col;
	float inv_alpha = (1.0f - In.VertexColor.a);
	multi_tex_col.rgb *= inv_alpha;
	multi_tex_col.rgb += tex_col2.rgb * In.VertexColor.a;
	
	//!!
	INPUT_TEX_GAMMA(multi_tex_col.rgb);
/////
	float season = GetSeason();
	
	if (season < 0.5) //0= spring
	{
	multi_tex_col.rgb *= float3(0.9,1.1,0.9);
	}
	else if ((season > 0.5)&&(season < 1.5)) //1= summer
	{
	multi_tex_col.rgb *= float3(1.0,1.0,1.0);
	}
	else if ((season > 1.5)&&(season < 2.5)) //2= autumn
	{
	multi_tex_col.rgb *= float3(1.1,0.9,0.9);
	}
	else if ((season > 2.5)) //3= winter
	{
	float greyscale = dot(multi_tex_col.rgb, float3(0.3, 0.59, 0.11));
	multi_tex_col.rgb = lerp(greyscale,multi_tex_col.rgb,0.75);
	float h = tex2D(SpecularTextureSampler, In.Tex0*0.5).a;
	 h *= tex2D(SpecularTextureSampler, In.Tex0).a;
	 h += 0.5;
	  h = 1;
	float3 snow = tex2D(EnvTextureSampler, In.Tex0).rgb;
	multi_tex_col.rgb = lerp(multi_tex_col.rgb,snow,saturate(h));
	}
////
	
	
	

	float sun_amount = 1.0f;
	if (PcfMode != PCF_NONE)
	{
		if (PcfMode == PCF_NVIDIA)
			sun_amount = saturate( 0.15f + GetSunAmount(PcfMode, In.ShadowTexCoord, In.ShadowTexelPos) );
		else
			sun_amount = GetSunAmount(PcfMode, In.ShadowTexCoord, In.ShadowTexelPos);	//cannot fit 64 instruction
	}
	total_light += (saturate(dot(In.SunLightDir.xyz, normal.xyz)) * (sun_amount)) * vSunColor;
	
	total_light += saturate(dot(In.SkyLightDir.xyz, normal.xyz)) * vSkyLightColor;
	#ifndef USE_LIGHTING_PASS
		total_light += saturate(dot(In.PointLightDir.xyz, normal.xyz)) * vPointLightColor;
	#endif

	//fresnel
	float3 vView = normalize(In.ViewDir);
	float3 fresnel = 1-(saturate(dot(vView, normal)));
	fresnel = 0.0204f + 0.9796 * (fresnel * fresnel * fresnel* fresnel * fresnel);
	total_light.rgb += 0.5*(total_light*fresnel); 
	total_light = saturate(total_light);
///////////	
	
	Output.RGBColor.rgb = total_light.rgb;
	Output.RGBColor.a = 1.0f;
	
	Output.RGBColor *= multi_tex_col;
	Output.RGBColor.rgb *= In.VertexColor.rgb;
	Output.RGBColor.a *= In.PointLightDir.a;
	
	if ((season < 2.5)) //  not winter (3= winter)
	{
	//parallax height darkening
	float light_intenisty = dot(total_light.rgb, float3(0.3, 0.59, 0.11));
	Output.RGBColor.rgb = lerp(Output.RGBColor.rgb,	(Output.RGBColor.rgb * (0.35+fresnel)),light_intenisty);
	
	
	float h = tex2D(SpecularTextureSampler, In.Tex0).a;
	Output.RGBColor.rgb = lerp(Output.RGBColor.rgb*0.75,Output.RGBColor.rgb*1.2,h);
	//
	}
else
	{
	float light_intenisty = dot(total_light.rgb, float3(0.3, 0.59, 0.11));
	float3 outcolour = lerp(Output.RGBColor.rgb,	(Output.RGBColor.rgb * (0.35+fresnel)),light_intenisty);
	Output.RGBColor.rgb = lerp(Output.RGBColor.rgb,	outcolour,0.5);
	
	float h = tex2D(SpecularTextureSampler, In.Tex0).a;
	Output.RGBColor.rgb = lerp(Output.RGBColor.rgb,Output.RGBColor.rgb*1.2,h);

	}

	
	
	OUTPUT_GAMMA(Output.RGBColor.rgb);
	
	
	return Output;
}



VertexShader vs_main_parallax_compiled_PCF_NONE = compile vs_2_0 vs_main_parallax(PCF_NONE);
VertexShader vs_main_parallax_compiled_PCF_DEFAULT = compile vs_2_0 vs_main_parallax(PCF_DEFAULT);
VertexShader vs_main_parallax_compiled_PCF_NVIDIA = compile vs_2_0 vs_main_parallax(PCF_NVIDIA);


//-----
technique parallax_ground
{
	pass P0
	{
		VertexShader = vs_main_parallax_compiled_PCF_NONE;
		PixelShader = compile PS_2_X ps_main_parallax(PCF_NONE);
	}
}
technique parallax_ground_SHDW
{
	pass P0
	{
		VertexShader = vs_main_parallax_compiled_PCF_DEFAULT;
		PixelShader = compile PS_2_X ps_main_parallax(PCF_DEFAULT);
	}
}
technique parallax_ground_SHDWNVIDIA
{
	pass P0
	{
		VertexShader = vs_main_parallax_compiled_PCF_NVIDIA;
		PixelShader = compile PS_2_X ps_main_parallax(PCF_NVIDIA);
	}
}
DEFINE_LIGHTING_TECHNIQUE(parallax_ground, 0, 1, 0, 0, 0)
//-----
technique parallax_ground_multitex
{
	pass P0
	{
		VertexShader = vs_main_parallax_compiled_PCF_NONE;
		PixelShader = compile PS_2_X ps_main_parallax_multitex(PCF_NONE);
	}
}
technique parallax_ground_multitex_SHDW
{
	pass P0
	{
		VertexShader = vs_main_parallax_compiled_PCF_DEFAULT;
		PixelShader = compile PS_2_X ps_main_parallax_multitex(PCF_DEFAULT);
	}
}
technique parallax_ground_multitex_SHDWNVIDIA
{
	pass P0
	{
		VertexShader = vs_main_parallax_compiled_PCF_NVIDIA;
		PixelShader = compile PS_2_X ps_main_parallax_multitex(PCF_NVIDIA);
	}
}
DEFINE_LIGHTING_TECHNIQUE(parallax_ground_multitex, 0, 1, 0, 0, 0)



















//---
struct VS_OUTPUT_ENVMAP_SPECULAR
{
	float4 Pos					: POSITION;
	float  Fog				    : FOG;
	
	float4 Color				: COLOR0;
	float4 Tex0					: TEXCOORD0;
	float4 SunLight				: TEXCOORD1;
	float4 ShadowTexCoord		: TEXCOORD2;
	float2 ShadowTexelPos		: TEXCOORD3;
	float3 vSpecular            : TEXCOORD4;
};
VS_OUTPUT_ENVMAP_SPECULAR vs_envmap_specular(uniform const int PcfMode, float4 vPosition : POSITION, float3 vNormal : NORMAL, float2 tc : TEXCOORD0, float4 vColor : COLOR0)
{
	INITIALIZE_OUTPUT(VS_OUTPUT_ENVMAP_SPECULAR, Out);

	float4 vWorldPos = (float4)mul(matWorld,vPosition);
	float3 vWorldN = normalize(mul((float3x3)matWorld, vNormal)); //normal in world space
	
	if(bUseMotionBlur)	//motion blur flag!?!
	{
		float4 vWorldPos1 = mul(matMotionBlur, vPosition);
		float3 delta_vector = vWorldPos1 - vWorldPos;
		float maxMoveLength = length(delta_vector);
		float3 moveDirection = delta_vector / maxMoveLength; //normalize(delta_vector);
		
		if(maxMoveLength > 0.25f)
		{
			maxMoveLength = 0.25f;
			vWorldPos1.xyz = vWorldPos.xyz + delta_vector * maxMoveLength;
		}
		
		float delta_coefficient_sharp = (dot(vWorldN, moveDirection) > 0.12f) ? 1 : 0;

		float y_factor = saturate(vPosition.y+0.15);
		vWorldPos = lerp(vWorldPos, vWorldPos1, delta_coefficient_sharp * y_factor);

		float delta_coefficient_smooth = saturate(dot(vWorldN, moveDirection) + 0.5f);

		float extra_alpha = 0.1f;
		float start_alpha = (1.0f+extra_alpha);
		float end_alpha = start_alpha - 1.8f;
		float alpha = saturate(lerp(start_alpha, end_alpha, delta_coefficient_smooth));
		vColor.a = saturate(0.5f - vPosition.y) + alpha + 0.25;
		
		Out.Pos = mul(matViewProj, vWorldPos);
	}
	else 
	{
		Out.Pos = mul(matWorldViewProj, vPosition);
	}

	Out.Tex0.xy = tc;

	float3 relative_cam_pos = normalize(vCameraPos - vWorldPos);
	float2 envpos;
	float3 tempvec = relative_cam_pos - vWorldN;
	float3 vHalf = normalize(relative_cam_pos - vSunDir);
	float3 fSpecular = spec_coef * vSunColor * vSpecularColor * pow( saturate( dot( vHalf, vWorldN) ), fMaterialPower);
	Out.vSpecular = fSpecular;
	Out.vSpecular *= vColor.rgb;

	envpos.x = (tempvec.y);// + tempvec.x);
	envpos.y = tempvec.z;
	envpos += 1.0f;
	//   envpos *= 0.5f;

	Out.Tex0.zw = envpos;

	float4 diffuse_light = vAmbientColor;
	//   diffuse_light.rgb *= gradient_factor * (gradient_offset + vWorldN.z);


	//directional lights, compute diffuse color
	diffuse_light += saturate(dot(vWorldN, -vSkyLightDir)) * vSkyLightColor;

	//point lights
	#ifndef USE_LIGHTING_PASS
	diffuse_light += calculate_point_lights_diffuse(vWorldPos, vWorldN, false, false);
	#endif
	
	//apply material color
	//	Out.Color = min(1, vMaterialColor * vColor * diffuse_light);
	Out.Color = (vMaterialColor * vColor * diffuse_light);
	//shadow mapping variables
	float wNdotSun = max(-0.0001f,dot(vWorldN, -vSunDir));
	Out.SunLight = (wNdotSun) * vSunColor * vMaterialColor * vColor;
	Out.SunLight.a = vColor.a;

	if (PcfMode != PCF_NONE)
	{
		float4 ShadowPos = mul(matSunViewProj, vWorldPos);
		Out.ShadowTexCoord = ShadowPos;
		Out.ShadowTexCoord.z /= ShadowPos.w;
		Out.ShadowTexCoord.w = 1.0f;
		Out.ShadowTexelPos = Out.ShadowTexCoord * fShadowMapSize;
		//shadow mapping variables end
	}
	
	//apply fog
	float3 P = mul(matWorldView, vPosition); //position in view space
	float d = length(P);
	Out.Fog = get_fog_amount_new(d, vWorldPos.z);

	return Out;
}


VS_OUTPUT_ENVMAP_SPECULAR vs_envmap_specular_Instanced(uniform const int PcfMode, float4 vPosition : POSITION, float3 vNormal : NORMAL, 
														float2 tc : TEXCOORD0, float4 vColor : COLOR0,
														 //instance data:
													   float3   vInstanceData0 : TEXCOORD1, float3   vInstanceData1 : TEXCOORD2,
													   float3   vInstanceData2 : TEXCOORD3, float3   vInstanceData3 : TEXCOORD4)
{
	INITIALIZE_OUTPUT(VS_OUTPUT_ENVMAP_SPECULAR, Out);

	float4x4 matWorldOfInstance = build_instance_frame_matrix(vInstanceData0, vInstanceData1, vInstanceData2, vInstanceData3);

	float4 vWorldPos = mul(matWorldOfInstance, vPosition);
	float3 vWorldN = normalize(mul((float3x3)matWorldOfInstance, vNormal));	
	
	
	if(bUseMotionBlur)	//motion blur flag!?!
	{
		float4 vWorldPos1;
		float3 moveDirection;
		if(true)	//instanced meshes dont have valid matMotionBlur!
		{
			const float blur_len = 0.2f;
			moveDirection = -normalize( float3(matWorldOfInstance[0][0],matWorldOfInstance[1][0],matWorldOfInstance[2][0]) );	//using x axis !
			moveDirection.y -= blur_len * 0.285;	//low down blur for big blur_lens (show more like a spline)
			vWorldPos1 = vWorldPos + float4(moveDirection,0) * blur_len;
		}
		else
		{
			vWorldPos1 = mul(matMotionBlur, vPosition);
			moveDirection = normalize(vWorldPos1 - vWorldPos);
		}
		
		   
		float delta_coefficient_sharp = (dot(vWorldN, moveDirection) > 0.12f) ? 1 : 0;

		float y_factor = saturate(vPosition.y+0.15);
		vWorldPos = lerp(vWorldPos, vWorldPos1, delta_coefficient_sharp * y_factor);

		float delta_coefficient_smooth = saturate(dot(vWorldN, moveDirection) + 0.5f);

		float extra_alpha = 0.1f;
		float start_alpha = (1.0f+extra_alpha);
		float end_alpha = start_alpha - 1.8f;
		float alpha = saturate(lerp(start_alpha, end_alpha, delta_coefficient_smooth));
		vColor.a = saturate(0.5f - vPosition.y) + alpha + 0.25;
	}
	
	Out.Pos = mul(matViewProj, vWorldPos);

	Out.Tex0.xy = tc;

	float3 relative_cam_pos = normalize(vCameraPos - vWorldPos);
	float2 envpos;
	float3 tempvec = relative_cam_pos - vWorldN;
	float3 vHalf = normalize(relative_cam_pos - vSunDir);
	float3 fSpecular = spec_coef * vSunColor * vSpecularColor * pow( saturate( dot( vHalf, vWorldN) ), fMaterialPower);
	Out.vSpecular = fSpecular;
	Out.vSpecular *= vColor.rgb;

	envpos.x = (tempvec.y);// + tempvec.x);
	envpos.y = tempvec.z;
	envpos += 1.0f;
	//   envpos *= 0.5f;

	Out.Tex0.zw = envpos;

	float4 diffuse_light = vAmbientColor;
	//   diffuse_light.rgb *= gradient_factor * (gradient_offset + vWorldN.z);


	//directional lights, compute diffuse color
	diffuse_light += saturate(dot(vWorldN, -vSkyLightDir)) * vSkyLightColor;

	//point lights
	#ifndef USE_LIGHTING_PASS
	diffuse_light += calculate_point_lights_diffuse(vWorldPos, vWorldN, false, false);
	#endif
	
	//apply material color
	//	Out.Color = min(1, vMaterialColor * vColor * diffuse_light);
	Out.Color = (vMaterialColor * vColor * diffuse_light);
	//shadow mapping variables
	float wNdotSun = max(-0.0001f,dot(vWorldN, -vSunDir));
	Out.SunLight = (wNdotSun) * vSunColor * vMaterialColor * vColor;
	Out.SunLight.a = vColor.a;

	if (PcfMode != PCF_NONE)
	{
		float4 ShadowPos = mul(matSunViewProj, vWorldPos);
		Out.ShadowTexCoord = ShadowPos;
		Out.ShadowTexCoord.z /= ShadowPos.w;
		Out.ShadowTexCoord.w = 1.0f;
		Out.ShadowTexelPos = Out.ShadowTexCoord * fShadowMapSize;
		//shadow mapping variables end
	}
	
	//apply fog
	float3 P = mul(matView, vWorldPos); //position in view space
	float d = length(P);
	Out.Fog = get_fog_amount_new(d, vWorldPos.z);

	return Out;
}

PS_OUTPUT ps_envmap_specular(VS_OUTPUT_ENVMAP_SPECULAR In, uniform const int PcfMode)
{
	PS_OUTPUT Output;
	
	// Compute half vector for specular lighting
	//   float3 vHalf = normalize(normalize(-ViewPos) + normalize(g_vLight - ViewPos));
	float4 texColor = tex2D(MeshTextureSampler, In.Tex0.xy);
	INPUT_TEX_GAMMA(texColor.rgb);
	
	float3 specTexture = tex2D(SpecularTextureSampler, In.Tex0.xy).rgb;
	float3 fSpecular = specTexture * In.vSpecular.rgb;
	
	//	float3 relative_cam_pos = normalize(vCameraPos - In.worldPos);
	//	float3 vHalf = normalize(relative_cam_pos - vSunDir);
	/*	
	float2 envpos;
	float3 tempvec =relative_cam_pos -  In.worldNormal ;
//	envpos.x = tempvec.x;
//	envpos.y = tempvec.z;
	envpos.xy = tempvec.xz;
	envpos += 1.0f;
	envpos *= 0.5f;
*/	
	float3 envColor = tex2D(EnvTextureSampler, In.Tex0.zw).rgb;
	
	// Compute normal dot half for specular light
	//	float4 fSpecular = 4.0f * specColor * vSpecularColor * pow( saturate( dot( vHalf, normalize( In.worldNormal) ) ), fMaterialPower);

	
	if ((PcfMode != PCF_NONE))
	{
		
		float sun_amount = 0.1f + GetSunAmount(PcfMode, In.ShadowTexCoord, In.ShadowTexelPos);
		//		sun_amount *= sun_amount;
		float4 vcol = In.Color;
		vcol.rgb += (In.SunLight.rgb + fSpecular) * sun_amount;
		Output.RGBColor = (texColor * vcol);
		Output.RGBColor.rgb += (In.SunLight * sun_amount + 0.3f) * (In.Color.rgb * envColor.rgb * specTexture);
	}
	else
	{
		float4 vcol = In.Color;
		vcol.rgb += (In.SunLight.rgb + fSpecular);
		Output.RGBColor = (texColor * vcol);
		Output.RGBColor.rgb += (In.SunLight + 0.3f) * (In.Color.rgb * envColor.rgb * specTexture);
	}

	OUTPUT_GAMMA(Output.RGBColor.rgb);
	
	Output.RGBColor.a = 1.0f;
	
	if(bUseMotionBlur)
		Output.RGBColor.a = In.SunLight.a;
		
	return Output;
}


PS_OUTPUT ps_envmap_specular_singlespec(VS_OUTPUT_ENVMAP_SPECULAR In, uniform const int PcfMode)	//only differs by black-white specular texture usage
{
	PS_OUTPUT Output;
	
	// Compute half vector for specular lighting
	
	float2 spectex_Col = tex2D(SpecularTextureSampler, In.Tex0.xy).ag;
	float specTexture = dot(spectex_Col, spectex_Col) * 0.5;
	float3 fSpecular = specTexture * In.vSpecular.rgb;
	
	float4 texColor = saturate( (saturate(In.Color+0.5f)*specTexture)*2.0f+0.25f);
	// INPUT_TEX_GAMMA(texColor.rgb);
	
	//	float3 relative_cam_pos = normalize(vCameraPos - In.worldPos);
	//	float3 vHalf = normalize(relative_cam_pos - vSunDir);
	/*	
	float2 envpos;
	float3 tempvec =relative_cam_pos -  In.worldNormal ;
//	envpos.x = tempvec.x;
//	envpos.y = tempvec.z;
	envpos.xy = tempvec.xz;
	envpos += 1.0f;
	envpos *= 0.5f;
*/	
	float3 envColor = tex2D(EnvTextureSampler, In.Tex0.zw).rgb;
	
	// Compute normal dot half for specular light
	//	float4 fSpecular = 4.0f * specColor * vSpecularColor * pow( saturate( dot( vHalf, normalize( In.worldNormal) ) ), fMaterialPower);

	
	if ((PcfMode != PCF_NONE))
	{
		float sun_amount = 0.1f + GetSunAmount(PcfMode, In.ShadowTexCoord, In.ShadowTexelPos);
		//		sun_amount *= sun_amount;
		float4 vcol = In.Color;
		vcol.rgb += (In.SunLight.rgb + fSpecular) * sun_amount;
		Output.RGBColor = (texColor * vcol);
		Output.RGBColor.rgb += (In.SunLight * sun_amount + 0.3f) * (In.Color.rgb * envColor.rgb * specTexture);
	}
	else
	{
		float4 vcol = In.Color;
		vcol.rgb += (In.SunLight.rgb + fSpecular);
		Output.RGBColor = (texColor * vcol);
		Output.RGBColor.rgb += (In.SunLight + 0.3f) * (In.Color.rgb * envColor.rgb * specTexture);
	}

	OUTPUT_GAMMA(Output.RGBColor.rgb);
	
	Output.RGBColor.a = 1.0f;
	/*
	if(bUseMotionBlur)
		Output.RGBColor.a = In.SunLight.a;
	*/
	
	return Output;
}

DEFINE_TECHNIQUES(envmap_specular_diffuse, vs_envmap_specular, ps_envmap_specular)
DEFINE_TECHNIQUES(envmap_specular_diffuse_Instanced, vs_envmap_specular_Instanced, ps_envmap_specular)
DEFINE_TECHNIQUES(watermap_for_objects, vs_envmap_specular, ps_envmap_specular_singlespec)

//---
struct VS_OUTPUT_BUMP_DYNAMIC
{
	float4 Pos					: POSITION;
	float4 VertexColor			: COLOR0;
	float2 Tex0					: TEXCOORD0;
	#ifndef USE_LIGHTING_PASS
	float3 vec_to_light_0		: TEXCOORD1;
	float3 vec_to_light_1		: TEXCOORD2;
	float3 vec_to_light_2		: TEXCOORD3;
	#endif
	//    float4 vec_to_light_3		: TEXCOORD4;
	//    float4 vec_to_light_4		: TEXCOORD5;
	//    float4 vec_to_light_5		: TEXCOORD6;
	//    float4 vec_to_light_6		: TEXCOORD7;
	float  Fog					: FOG;
};
VS_OUTPUT_BUMP_DYNAMIC vs_main_bump_interior (float4 vPosition : POSITION, float3 vNormal : NORMAL, float2 tc : TEXCOORD0,  float3 vTangent : TANGENT, float3 vBinormal : BINORMAL, float4 vVertexColor : COLOR0)
{
	INITIALIZE_OUTPUT(VS_OUTPUT_BUMP_DYNAMIC, Out);

	float4 vWorldPos = (float4)mul(matWorld,vPosition);
   Out.Pos = mul(matWorldViewProj, vPosition);
   Out.Tex0 = tc;
   
   float3 vWorldN = normalize(mul((float3x3)matWorld, vNormal)); //normal in world space
   float3 vWorld_binormal = normalize(mul((float3x3)matWorld, vBinormal)); //normal in world space
   float3 vWorld_tangent  = normalize(mul((float3x3)matWorld, vTangent)); //normal in world space


   float3x3 TBNMatrix = float3x3(vWorld_tangent, vWorld_binormal, vWorldN); 

	#ifndef USE_LIGHTING_PASS
	float3 point_to_light = vLightPosDir[iLightIndices[0]]-vWorldPos.xyz;
	Out.vec_to_light_0.xyz =  mul(TBNMatrix, point_to_light);
	point_to_light = vLightPosDir[iLightIndices[1]]-vWorldPos.xyz;
	Out.vec_to_light_1.xyz =  mul(TBNMatrix, point_to_light);
	point_to_light = vLightPosDir[iLightIndices[2]]-vWorldPos.xyz;
	Out.vec_to_light_2.xyz =  mul(TBNMatrix, point_to_light);
	#endif
	
   	Out.VertexColor = vVertexColor;

   //apply fog
   float3 P = mul(matWorldView, vPosition); //position in view space
   float d = length(P);
	Out.Fog = get_fog_amount_new(d, vWorldPos.z);
   return Out;
}
PS_OUTPUT ps_main_bump_interior( VS_OUTPUT_BUMP_DYNAMIC In)
{ 
    PS_OUTPUT Output;
    
    float4 total_light = vAmbientColor;//In.LightAmbient;
    

	#ifndef USE_LIGHTING_PASS
	float3 normal;
	normal.xy = (2.0f * tex2D(NormalTextureSampler, In.Tex0).ag - 1.0f);
	normal.z = sqrt(1.0f - dot(normal.xy, normal.xy));
 
//	float3 abs_min_vec_to_light = float3(100000, 100000, 100000);
    
//	float LD = In.vec_to_light_0.w;
	float LD = dot(In.vec_to_light_0.xyz,In.vec_to_light_0.xyz);
	float3 L = normalize(In.vec_to_light_0.xyz);
	float wNdotL = dot(normal, L);
	total_light += saturate(wNdotL) * vLightDiffuse[iLightIndices[0]] /(LD);
	
//	LD = In.vec_to_light_1.w;
	LD = dot(In.vec_to_light_1.xyz,In.vec_to_light_1.xyz);
	L = normalize(In.vec_to_light_1.xyz);
	wNdotL = dot(normal, L);
	total_light += saturate(wNdotL) * vLightDiffuse[iLightIndices[1]] /(LD);

//	LD = In.vec_to_light_2.w;
	LD = dot(In.vec_to_light_2.xyz,In.vec_to_light_2.xyz);
	L = normalize(In.vec_to_light_2.xyz);
	wNdotL = dot(normal, L);
	total_light += saturate(wNdotL) * vLightDiffuse[iLightIndices[2]] /(LD);
	#endif

//	Output.RGBColor = saturate(total_light * 0.6f) * 1.66f;
	Output.RGBColor = float4(total_light.rgb, 1.0);
	float4 tex_col = tex2D(MeshTextureSampler, In.Tex0);
    INPUT_TEX_GAMMA(tex_col.rgb);

	Output.RGBColor *= tex_col;
	Output.RGBColor *= In.VertexColor;
	
//	Output.RGBColor = saturate(Output.RGBColor);
    Output.RGBColor.rgb = saturate(OUTPUT_GAMMA(Output.RGBColor.rgb));
    Output.RGBColor.a = In.VertexColor.a;

	return Output;
}

technique bumpmap_interior
{
	pass P0
	{
		VertexShader = compile vs_2_0 vs_main_bump_interior();
		PixelShader = compile ps_2_0 ps_main_bump_interior();
	}
}

struct VS_OUTPUT_BUMP_DYNAMIC_NEW
{
	float4 Pos					: POSITION;
	float4 VertexColor			: COLOR0;
	float2 Tex0					: TEXCOORD0;
	#ifndef USE_LIGHTING_PASS
	float3 vec_to_light_0		: TEXCOORD1;
	float3 vec_to_light_1		: TEXCOORD2;
	float3 vec_to_light_2		: TEXCOORD3;
	#endif
	float3 ViewDir				: TEXCOORD4;
	
	float  Fog					: FOG;
};


VS_OUTPUT_BUMP_DYNAMIC_NEW vs_main_bump_interior_new (float4 vPosition : POSITION, float3 vNormal : NORMAL, float2 tc : TEXCOORD0,  float3 vTangent : TANGENT, float3 vBinormal : BINORMAL, float4 vVertexColor : COLOR0)
{
	INITIALIZE_OUTPUT(VS_OUTPUT_BUMP_DYNAMIC_NEW, Out);

	float4 vWorldPos = (float4)mul(matWorld,vPosition);
	Out.Pos = mul(matWorldViewProj, vPosition);
	Out.Tex0 = tc;

	float3 vWorldN = normalize(mul((float3x3)matWorld, vNormal)); //normal in world space
	float3 vWorld_binormal = normalize(mul((float3x3)matWorld, vBinormal)); //normal in world space
	float3 vWorld_tangent  = normalize(mul((float3x3)matWorld, vTangent)); //normal in world space


	float3x3 TBNMatrix = float3x3(vWorld_tangent, vWorld_binormal, vWorldN); 

	#ifndef USE_LIGHTING_PASS
	float3 point_to_light = vLightPosDir[iLightIndices[0]]-vWorldPos.xyz;
	Out.vec_to_light_0.xyz =  mul(TBNMatrix, point_to_light);
	point_to_light = vLightPosDir[iLightIndices[1]]-vWorldPos.xyz;
	Out.vec_to_light_1.xyz =  mul(TBNMatrix, point_to_light);
	point_to_light = vLightPosDir[iLightIndices[2]]-vWorldPos.xyz;
	Out.vec_to_light_2.xyz =  mul(TBNMatrix, point_to_light);
	#endif
	
	Out.VertexColor = vVertexColor;
	
	float3 viewdir = normalize(vCameraPos.xyz - vWorldPos.xyz);
	Out.ViewDir =  mul(TBNMatrix, viewdir);

	//apply fog
	float3 P = mul(matWorldView, vPosition); //position in view space
	float d = length(P);
	Out.Fog = get_fog_amount_new(d, vWorldPos.z);
	return Out;
}

//uses standart-style normal maps
PS_OUTPUT ps_main_bump_interior_new( VS_OUTPUT_BUMP_DYNAMIC_NEW In, uniform const bool use_specularmap ) //ps_main_bump_interior with std normalmaps
{ 
	PS_OUTPUT Output;
	
	float4 total_light = vAmbientColor;

	// effective lights!?

	#ifndef USE_LIGHTING_PASS
	float3 normal = 2.0f * tex2D(NormalTextureSampler, In.Tex0).rgb - 1.0f;
	
	
	//	float LD = In.vec_to_light_0.w;
	float LD_0 = saturate(1.0f / dot(In.vec_to_light_0.xyz,In.vec_to_light_0.xyz));
	float3 L_0 = normalize(In.vec_to_light_0.xyz);
	float wNdotL_0 = dot(normal, L_0);
	total_light += saturate(wNdotL_0) * vLightDiffuse[ iLightIndices[0] ] * (LD_0);

	//	LD = In.vec_to_light_1.w;
	float LD_1 = saturate(1.0f / dot(In.vec_to_light_1.xyz,In.vec_to_light_1.xyz));
	float3 L_1 = normalize(In.vec_to_light_1.xyz);
	float wNdotL_1 = dot(normal, L_1);
	total_light += saturate(wNdotL_1) * vLightDiffuse[ iLightIndices[1] ] * (LD_1);

	//	LD = In.vec_to_light_2.w;
	float LD_2 = saturate(1.0f / dot(In.vec_to_light_2.xyz,In.vec_to_light_2.xyz));
	float3 L_2 = normalize(In.vec_to_light_2.xyz);
	float wNdotL_2 = dot(normal, L_2);
	total_light += saturate(wNdotL_2) * vLightDiffuse[ iLightIndices[2] ] * (LD_2);
	#endif
	
	//	Output.RGBColor = saturate(total_light * 0.6f) * 1.66f;
	Output.RGBColor = float4(total_light.rgb, 1.0);
	float4 tex_col = tex2D(MeshTextureSampler, In.Tex0);
	INPUT_TEX_GAMMA(tex_col.rgb);

	Output.RGBColor *= tex_col;
	Output.RGBColor *= In.VertexColor;
	
	if(use_specularmap)
	{
		float4 fSpecular = 0;
		
		//light0 specular
		float4 light0_specColor = vLightDiffuse[ iLightIndices[0] ] * LD_0;
		float3 vHalf_0 = normalize( In.ViewDir + L_0 );
		fSpecular = light0_specColor * pow( saturate(dot(vHalf_0, normal)), fMaterialPower);
		
		/* makes 65 instruction:
		//light1 specular
		float4 light1_specColor = vLightDiffuse[ iLightIndices[1] ] * LD_1;
		float3 vHalf_1 = normalize( In.ViewDir + L_1 );
		fSpecular += light1_specColor * pow( saturate(dot(vHalf_1, normal)), fMaterialPower);
		*/
		//light2 specular
		//float4 light2_specColor = vLightDiffuse[2] * LD_2;
		//float3 vHalf_2 = normalize( In.ViewDir + L_2 );
		//fSpecular += light2_specColor * pow( saturate(dot(vHalf_2, normal)), fMaterialPower);
		
		float4 specColor = 0.1 * spec_coef * vSpecularColor;
		float spec_tex_factor = dot(tex2D(SpecularTextureSampler, In.Tex0).rgb,0.33);	//get more precision from specularmap
		specColor *= spec_tex_factor;
		
		Output.RGBColor += specColor * fSpecular;
	}
	
	OUTPUT_GAMMA(Output.RGBColor.rgb);
	Output.RGBColor = saturate(Output.RGBColor);
	Output.RGBColor.a = In.VertexColor.a;
	
	return Output;
}

technique bumpmap_interior_new
{
	pass P0
	{
		VertexShader = compile vs_2_0 vs_main_bump_interior_new();
		PixelShader = compile ps_2_0 ps_main_bump_interior_new(false);
	}
}

technique bumpmap_interior_new_specmap
{
	pass P0
	{
		VertexShader = compile vs_2_0 vs_main_bump_interior_new();
		PixelShader = compile ps_2_0 ps_main_bump_interior_new(true);
	}
}

DEFINE_LIGHTING_TECHNIQUE(bumpmap_interior, 1, 1, 0, 0, 0)
#endif

/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#ifdef STANDART_SHADERS


struct VS_OUTPUT_STANDART 
{
	float4 Pos					: POSITION;
	float  Fog					: FOG;
	
	float4 VertexColor			: COLOR0;
	#ifdef INCLUDE_VERTEX_LIGHTING 
	float3 VertexLighting		: COLOR1;
	#endif
	
	float2 Tex0					: TEXCOORD0;
	float3 SunLightDir			: TEXCOORD1;
	float3 SkyLightDir			: TEXCOORD2;
	#ifndef USE_LIGHTING_PASS 
	float4 PointLightDir		: TEXCOORD3;
	#endif
	float4 ShadowTexCoord		: TEXCOORD4;
	float2 ShadowTexelPos		: TEXCOORD5;
	float3 ViewDir				: TEXCOORD6;
};

VS_OUTPUT_STANDART vs_main_standart (uniform const int PcfMode, uniform const bool use_bumpmap, uniform const bool use_skinning, 
										float4 vPosition : POSITION, float3 vNormal : NORMAL, float2 tc : TEXCOORD0,  float3 vTangent : TANGENT, float3 vBinormal : BINORMAL, 
										float4 vVertexColor : COLOR0, float4 vBlendWeights : BLENDWEIGHT, float4 vBlendIndices : BLENDINDICES)
{
	INITIALIZE_OUTPUT(VS_OUTPUT_STANDART, Out);
	
	float4 vObjectPos;
	float3 vObjectN, vObjectT, vObjectB;
	
	if(use_skinning) {
		vObjectPos = skinning_deform(vPosition, vBlendWeights, vBlendIndices);
		
		vObjectN = normalize(  mul((float3x3)matWorldArray[vBlendIndices.x], vNormal) * vBlendWeights.x
									+ mul((float3x3)matWorldArray[vBlendIndices.y], vNormal) * vBlendWeights.y
									+ mul((float3x3)matWorldArray[vBlendIndices.z], vNormal) * vBlendWeights.z
									+ mul((float3x3)matWorldArray[vBlendIndices.w], vNormal) * vBlendWeights.w);
									
		if(use_bumpmap)
		{
			vObjectT = normalize(  mul((float3x3)matWorldArray[vBlendIndices.x], vTangent) * vBlendWeights.x
										+ mul((float3x3)matWorldArray[vBlendIndices.y], vTangent) * vBlendWeights.y
										+ mul((float3x3)matWorldArray[vBlendIndices.z], vTangent) * vBlendWeights.z
										+ mul((float3x3)matWorldArray[vBlendIndices.w], vTangent) * vBlendWeights.w);
			
			// vObjectB = normalize(  mul((float3x3)matWorldArray[vBlendIndices.x], vBinormal) * vBlendWeights.x
			// 				+ mul((float3x3)matWorldArray[vBlendIndices.y], vBinormal) * vBlendWeights.y
			// 				+ mul((float3x3)matWorldArray[vBlendIndices.z], vBinormal) * vBlendWeights.z
			// 				+ mul((float3x3)matWorldArray[vBlendIndices.w], vBinormal) * vBlendWeights.w);
			vObjectB = /*normalize*/( cross( vObjectN, vObjectT ));	
			bool left_handed = (dot(cross(vNormal,vTangent),vBinormal) < 0.0f);
			if(left_handed) {
				vObjectB = -vObjectB;
			}
		}
	}
	else {
		vObjectPos = vPosition;
		
		vObjectN = vNormal;
									
		if(use_bumpmap)
		{
			vObjectT = vTangent;
			vObjectB = vBinormal;
		}
	}
	
	float4 vWorldPos = mul(matWorld, vObjectPos);
	float3 vWorldN = normalize(mul((float3x3)matWorld, vObjectN));	
	
	const bool use_motion_blur = bUseMotionBlur && (!use_skinning);
	
	if(use_motion_blur)	//motion blur flag!?!
	{
		#ifdef STATIC_MOVEDIR //(used in instanced rendering )
			const float blur_len = 0.25f;
			float3 moveDirection = -normalize( float3(matWorld[0][0],matWorld[1][0],matWorld[2][0]) );
			moveDirection.y -= blur_len * 0.285;	//low down blur for big blur_lens (show more like a spline)
			float4 vWorldPos1 = vWorldPos + float4(moveDirection,0) * blur_len;
		#else 
			float4 vWorldPos1 = mul(matMotionBlur, vObjectPos);
			float3 moveDirection = normalize(vWorldPos1 - vWorldPos);
		#endif
		
		   
		float delta_coefficient_sharp = (dot(vWorldN, moveDirection) > 0.1f) ? 1 : 0;

		float y_factor = saturate(vObjectPos.y+0.15);
		vWorldPos = lerp(vWorldPos, vWorldPos1, delta_coefficient_sharp * y_factor);

		float delta_coefficient_smooth = saturate(dot(vWorldN, moveDirection) + 0.5f);

		float extra_alpha = 0.1f;
		float start_alpha = (1.0f+extra_alpha);
		float end_alpha = start_alpha - 1.8f;
		float alpha = saturate(lerp(start_alpha, end_alpha, delta_coefficient_smooth));
		vVertexColor.a = saturate(0.5f - vObjectPos.y) + alpha + 0.25;
	}

	if(use_motion_blur)
	{
		Out.Pos = mul(matViewProj, vWorldPos);
	}
	else 
	{
		Out.Pos = mul(matWorldViewProj, vObjectPos);
	}

	Out.Tex0 = tc;
	
	
	if(use_bumpmap)
	{
		float3 vWorld_binormal = normalize(mul((float3x3)matWorld, vObjectB));
		float3 vWorld_tangent  = normalize(mul((float3x3)matWorld, vObjectT));
		float3x3 TBNMatrix = float3x3(vWorld_tangent, vWorld_binormal, vWorldN); 

		Out.SunLightDir = normalize(mul(TBNMatrix, -vSunDir));
		//Out.SkyLightDir = mul(TBNMatrix, -vSkyLightDir);
		Out.SkyLightDir = mul(TBNMatrix, float3(0,0,1)); //STR_TEMP!?
		Out.VertexColor = vVertexColor;
		
		
		//point lights
		#ifdef INCLUDE_VERTEX_LIGHTING
		Out.VertexLighting = calculate_point_lights_diffuse(vWorldPos, vWorldN, false, true);
		#endif
		
		#ifndef USE_LIGHTING_PASS 
		const int effective_light_index = iLightIndices[0];
		float3 point_to_light = vLightPosDir[effective_light_index]-vWorldPos.xyz;
		Out.PointLightDir.xyz = mul(TBNMatrix, normalize(point_to_light));
		
		float LD = dot(point_to_light, point_to_light);
		Out.PointLightDir.a = saturate(1.0f/LD);	//prevent bloom for 1 meters
		#endif
		
		float3 viewdir = normalize(vCameraPos.xyz - vWorldPos.xyz);
		Out.ViewDir =  mul(TBNMatrix, viewdir);
		
		#ifndef USE_LIGHTING_PASS
		if (PcfMode == PCF_NONE)
		{
			Out.ShadowTexCoord = calculate_point_lights_specular(vWorldPos, vWorldN, viewdir, true);
		}
		#endif
	}
	else {

		Out.VertexColor = vVertexColor;
		#ifdef INCLUDE_VERTEX_LIGHTING
		Out.VertexLighting = calculate_point_lights_diffuse(vWorldPos, vWorldN, false, false);
		#endif
		
		Out.ViewDir =  normalize(vCameraPos.xyz - vWorldPos.xyz);
		
		Out.SunLightDir = vWorldN;
		#ifndef USE_LIGHTING_PASS
		Out.SkyLightDir = calculate_point_lights_specular(vWorldPos, vWorldN, Out.ViewDir, false);
		#endif
	}
	Out.VertexColor.a *= vMaterialColor.a;

	

	if (PcfMode != PCF_NONE)
	{
		float4 ShadowPos = mul(matSunViewProj, vWorldPos);
		Out.ShadowTexCoord = ShadowPos;
		Out.ShadowTexCoord.z /= ShadowPos.w;
		Out.ShadowTexCoord.w = 1.0f;
		Out.ShadowTexelPos = Out.ShadowTexCoord * fShadowMapSize;
		//shadow mapping variables end
	}
	
	//apply fog
	float3 P = mul(matWorldView, vObjectPos); //position in view space
	float d = length(P);
	Out.Fog = get_fog_amount_new(d, vWorldPos.z);
		
	return Out;
}


VS_OUTPUT_STANDART vs_main_standart_Instanced (uniform const int PcfMode, uniform const bool use_bumpmap, uniform const bool use_skinning, 
										float4 vPosition : POSITION, float3 vNormal : NORMAL, float2 tc : TEXCOORD0,  float3 vTangent : TANGENT, float3 vBinormal : BINORMAL, 
										float4 vVertexColor : COLOR0, float4 vBlendWeights : BLENDWEIGHT, float4 vBlendIndices : BLENDINDICES,
									   //instance data:
									   float3   vInstanceData0 : TEXCOORD1, float3   vInstanceData1 : TEXCOORD2,
									   float3   vInstanceData2 : TEXCOORD3, float3   vInstanceData3 : TEXCOORD4)
{
	INITIALIZE_OUTPUT(VS_OUTPUT_STANDART, Out);
	
	float4 vObjectPos;
	float3 vObjectN, vObjectT, vObjectB;
	
	if(use_skinning) {
		//no skinned instancing support yet!
		GIVE_ERROR_HERE_VS;
	}
	else {
		vObjectPos = vPosition;
		
		vObjectN = vNormal;
									
		if(use_bumpmap)
		{
			vObjectT = vTangent;
			vObjectB = vBinormal;
		}
	}
	
	float4x4 matWorldOfInstance = build_instance_frame_matrix(vInstanceData0, vInstanceData1, vInstanceData2, vInstanceData3);

	float4 vWorldPos = mul(matWorldOfInstance, vObjectPos);
	float3 vWorldN = normalize(mul((float3x3)matWorldOfInstance, vObjectN));	
	
	
	const bool use_motion_blur = bUseMotionBlur && (!use_skinning);
	
	if(use_motion_blur)	//motion blur flag!?!
	{
		float4 vWorldPos1;
		float3 moveDirection;
		if(true)	//instanced meshes dont have valid matMotionBlur!
		{
			const float blur_len = 0.2f;
			moveDirection = -normalize( float3(matWorldOfInstance[0][0],matWorldOfInstance[1][0],matWorldOfInstance[2][0]) );	//using x axis !
			moveDirection.y -= blur_len * 0.285;	//low down blur for big blur_lens (show more like a spline)
			vWorldPos1 = vWorldPos + float4(moveDirection,0) * blur_len;
		}
		else
		{		
			vWorldPos1 = mul(matMotionBlur, vObjectPos);
			moveDirection = normalize(vWorldPos1 - vWorldPos);
		}
		
		   
		float delta_coefficient_sharp = (dot(vWorldN, moveDirection) > 0.1f) ? 1 : 0;

		float y_factor = saturate(vObjectPos.y+0.15);
		vWorldPos = lerp(vWorldPos, vWorldPos1, delta_coefficient_sharp * y_factor);

		float delta_coefficient_smooth = saturate(dot(vWorldN, moveDirection) + 0.5f);

		float extra_alpha = 0.1f;
		float start_alpha = (1.0f+extra_alpha);
		float end_alpha = start_alpha - 1.8f;
		float alpha = saturate(lerp(start_alpha, end_alpha, delta_coefficient_smooth));
		vVertexColor.a = saturate(0.5f - vObjectPos.y) + alpha + 0.25;
	}
	
	
	//-- Out.Pos = mul(matWorldViewProj, vObjectPos);
    Out.Pos = mul(matViewProj, vWorldPos);
	
	Out.Tex0 = tc;
	
	
	if(use_bumpmap)
	{
		float3 vWorld_binormal = normalize(mul((float3x3)matWorldOfInstance, vObjectB));
		float3 vWorld_tangent  = normalize(mul((float3x3)matWorldOfInstance, vObjectT));
		float3x3 TBNMatrix = float3x3(vWorld_tangent, vWorld_binormal, vWorldN); 

		Out.SunLightDir = normalize(mul(TBNMatrix, -vSunDir));
		//Out.SkyLightDir = mul(TBNMatrix, -vSkyLightDir);
		Out.SkyLightDir = mul(TBNMatrix, float3(0,0,1)); //STR_TEMP!?
		Out.VertexColor = vVertexColor;
		
		
		//point lights
		#ifdef INCLUDE_VERTEX_LIGHTING
		Out.VertexLighting = calculate_point_lights_diffuse(vWorldPos, vWorldN, false, true);
		#endif
		
		#ifndef USE_LIGHTING_PASS 
		const int effective_light_index = iLightIndices[0];
		float3 point_to_light = vLightPosDir[effective_light_index]-vWorldPos.xyz;
		Out.PointLightDir.xyz = mul(TBNMatrix, normalize(point_to_light));
		
		float LD = dot(point_to_light, point_to_light);
		Out.PointLightDir.a = saturate(1.0f/LD);	//prevent bloom for 1 meters
		#endif
		
		float3 viewdir = normalize(vCameraPos.xyz - vWorldPos.xyz);
		Out.ViewDir =  mul(TBNMatrix, viewdir);
		
		#ifndef USE_LIGHTING_PASS
		if (PcfMode == PCF_NONE)
		{
			Out.ShadowTexCoord = calculate_point_lights_specular(vWorldPos, vWorldN, viewdir, true);
		}
		#endif
	}
	else {

		Out.VertexColor = vVertexColor;
		#ifdef INCLUDE_VERTEX_LIGHTING
		Out.VertexLighting = calculate_point_lights_diffuse(vWorldPos, vWorldN, false, false);
		#endif
		
		Out.ViewDir =  normalize(vCameraPos.xyz - vWorldPos.xyz);
		
		Out.SunLightDir = vWorldN;
		#ifndef USE_LIGHTING_PASS
		Out.SkyLightDir = calculate_point_lights_specular(vWorldPos, vWorldN, Out.ViewDir, false);
		#endif
	}

	Out.VertexColor.a *= vMaterialColor.a;
	

	if (PcfMode != PCF_NONE)
	{
		float4 ShadowPos = mul(matSunViewProj, vWorldPos);
		Out.ShadowTexCoord = ShadowPos;
		Out.ShadowTexCoord.z /= ShadowPos.w;
		Out.ShadowTexCoord.w = 1.0f;
		Out.ShadowTexelPos = Out.ShadowTexCoord * fShadowMapSize;
		//shadow mapping variables end
	}
	
	//apply fog
	float3 P = mul(matView, vWorldPos); //position in view space
	float d = length(P);
	Out.Fog = get_fog_amount_new(d, vWorldPos.z);
	
	return Out;
}


//FOR SAILS - SAME AS vs_main_standart but has movement for sails
VS_OUTPUT_STANDART vs_main_standart_sails (uniform const int PcfMode, uniform const bool use_bumpmap, uniform const bool use_skinning, 
										float4 vPosition : POSITION, float3 vNormal : NORMAL, float2 tc : TEXCOORD0,  float3 vTangent : TANGENT, float3 vBinormal : BINORMAL, 
										float4 vVertexColor : COLOR0, float4 vBlendWeights : BLENDWEIGHT, float4 vBlendIndices : BLENDINDICES)
{
	INITIALIZE_OUTPUT(VS_OUTPUT_STANDART, Out);
	
	float4 vPos_without_movement = vPosition;
	//LAGRANDMASTER SAIL MVOEMENT
	float WindFactor = GetWindAmount(1.0f);
	float WindRotation = GetWindDirection(1.0f);
	float2 UV;
	UV.x = tc.x;
	UV.y = 1-tc.y;
	
    // below line defines 9 sections/ points where the vertices should not move
	// left bottom (actually top) 		|| left middle 										|| left top 							|| middle bottom  									|| middle middle 													|| middle top 											|| and so on
	if(((UV.y < 0.05) && (UV.x < 0.05)) || ((UV.x > 0.95) && (UV.y < 0.05)) || (UV.y > 0.95))
	{
		vPosition.x = 	vPosition.x;
	}
	else //if not in the fixed sections of uv map then we can wave
	{
	float3 vecObjectPos = vNormal;
	float4 vecWorldPositiom = (float4)mul(matWorld,vPosition);
	float4 vecObjPositiom = (float4)mul(matWorld,vPosition);
	float3 vecWorldN = normalize(mul((float3x3)matWorld, vNormal)); //normal in world space
	float3 vecWorld_binormal = normalize(mul((float3x3)matWorld, vBinormal)); //normal in world space
	float3 vecWorld_tangent  = normalize(mul((float3x3)matWorld, vTangent)); //normal in world space
	float3x3 TBNMatrix = float3x3(vecWorld_tangent, vecWorld_binormal, vecWorldN); 
	
	
	//define north
	float3 NorthDir;
	NorthDir.x = 0.001;
	NorthDir.y = 0.99;
	NorthDir.z = 0.001;
	
	//initially set wind direction to north
	float4 WindDir = 1;
	WindDir.xyz = NorthDir;
	
	//get degrees to rotate wind direction
	float radians = WindRotation * 0.0174532925; //convert degrees to radians
	
	
	//ROTATE Wind direction from north to actual direction of wind // ROTATE VECTOR ON Z AXIS EQUATION
	WindDir.x = (cos(radians)*NorthDir.x) - (sin(radians)*NorthDir.y);
	WindDir.y = (sin(radians)*NorthDir.x) + (cos(radians)*NorthDir.y);
	
	float4 WindDirection = 1;
	WindDirection.xyz= mul(TBNMatrix, WindDir);
	

	float ObjdotWind = (dot(vecObjectPos.xy, WindDirection.xy)); // gets angle between object and wind direction
	//  1 and minus 1 - face normal is perpendicular to wind dir, 0 - face normal is parallel to wind dir
	
	float inflate = ObjdotWind;
	if (inflate < 0) //takes negatives and makes them positive so scale is from 0 (normal is parallel to wind dir) to 1 (normal is perpendicular to wind dir)
	{
	inflate = 0- inflate;
	}

	inflate *= WindFactor;
	 
	vPosition.x += ((inflate/6)) * sin(1.5* vPosition.y + (1.6 * WindFactor) * time_var);//inflate is 0 (normal is parallel to wind dir) to 1 (normal is perpendicular to wind dir)
    vPosition.x += ((inflate/4)) * sin(0.6* vPosition.y +  WindFactor * time_var); //creates wave moving along sails on y axis (side to side)
	
	inflate = 1 - inflate; //inverse so that inflate is 0 (normal is perpendicular to wind dir) to 1 (normal is parallel to wind dir)
	vPosition.x += ((inflate/4)) * sin(0.6* vPosition.z + WindFactor * time_var); //creates wave moving down sails on z axis
}

		
		
	float4 vObjectPos;
	float3 vObjectN, vObjectT, vObjectB;
	
	if(use_skinning) {
		vObjectPos = skinning_deform(vPosition, vBlendWeights, vBlendIndices);
		
		vObjectN = normalize(  mul((float3x3)matWorldArray[vBlendIndices.x], vNormal) * vBlendWeights.x
									+ mul((float3x3)matWorldArray[vBlendIndices.y], vNormal) * vBlendWeights.y
									+ mul((float3x3)matWorldArray[vBlendIndices.z], vNormal) * vBlendWeights.z
									+ mul((float3x3)matWorldArray[vBlendIndices.w], vNormal) * vBlendWeights.w);
									
		if(use_bumpmap)
		{
			vObjectT = normalize(  mul((float3x3)matWorldArray[vBlendIndices.x], vTangent) * vBlendWeights.x
										+ mul((float3x3)matWorldArray[vBlendIndices.y], vTangent) * vBlendWeights.y
										+ mul((float3x3)matWorldArray[vBlendIndices.z], vTangent) * vBlendWeights.z
										+ mul((float3x3)matWorldArray[vBlendIndices.w], vTangent) * vBlendWeights.w);
			
			// vObjectB = normalize(  mul((float3x3)matWorldArray[vBlendIndices.x], vBinormal) * vBlendWeights.x
			// 				+ mul((float3x3)matWorldArray[vBlendIndices.y], vBinormal) * vBlendWeights.y
			// 				+ mul((float3x3)matWorldArray[vBlendIndices.z], vBinormal) * vBlendWeights.z
			// 				+ mul((float3x3)matWorldArray[vBlendIndices.w], vBinormal) * vBlendWeights.w);
			vObjectB = /*normalize*/( cross( vObjectN, vObjectT ));	
			bool left_handed = (dot(cross(vNormal,vTangent),vBinormal) < 0.0f);
			if(left_handed) {
				vObjectB = -vObjectB;
			}
		}
	}
	else {
		vObjectPos = vPosition;
		
		vObjectN = vNormal;
									
		if(use_bumpmap)
		{
			vObjectT = vTangent;
			vObjectB = vBinormal;
		}
	}
	
	float4 vWorldPos = mul(matWorld, vObjectPos);
	float3 vWorldN = normalize(mul((float3x3)matWorld, vObjectN));	
	
	const bool use_motion_blur = bUseMotionBlur && (!use_skinning);
	
	if(use_motion_blur)	//motion blur flag!?!
	{
		#ifdef STATIC_MOVEDIR //(used in instanced rendering )
			const float blur_len = 0.25f;
			float3 moveDirection = -normalize( float3(matWorld[0][0],matWorld[1][0],matWorld[2][0]) );
			moveDirection.y -= blur_len * 0.285;	//low down blur for big blur_lens (show more like a spline)
			float4 vWorldPos1 = vWorldPos + float4(moveDirection,0) * blur_len;
		#else 
			float4 vWorldPos1 = mul(matMotionBlur, vObjectPos);
			float3 moveDirection = normalize(vWorldPos1 - vWorldPos);
		#endif
		
		   
		float delta_coefficient_sharp = (dot(vWorldN, moveDirection) > 0.1f) ? 1 : 0;

		float y_factor = saturate(vObjectPos.y+0.15);
		vWorldPos = lerp(vWorldPos, vWorldPos1, delta_coefficient_sharp * y_factor);

		float delta_coefficient_smooth = saturate(dot(vWorldN, moveDirection) + 0.5f);

		float extra_alpha = 0.1f;
		float start_alpha = (1.0f+extra_alpha);
		float end_alpha = start_alpha - 1.8f;
		float alpha = saturate(lerp(start_alpha, end_alpha, delta_coefficient_smooth));
		vVertexColor.a = saturate(0.5f - vObjectPos.y) + alpha + 0.25;
	}

	if(use_motion_blur)
	{
		Out.Pos = mul(matViewProj, vWorldPos);
	}
	else 
	{
		Out.Pos = mul(matWorldViewProj, vObjectPos);
	}

	Out.Tex0 = tc;
	
	
	if(use_bumpmap)
	{
		float3 vWorld_binormal = normalize(mul((float3x3)matWorld, vObjectB));
		float3 vWorld_tangent  = normalize(mul((float3x3)matWorld, vObjectT));
		float3x3 TBNMatrix = float3x3(vWorld_tangent, vWorld_binormal, vWorldN); 

		Out.SunLightDir = normalize(mul(TBNMatrix, -vSunDir));
		//Out.SkyLightDir = mul(TBNMatrix, -vSkyLightDir);
		Out.SkyLightDir = mul(TBNMatrix, float3(0,0,1)); //STR_TEMP!?
		Out.VertexColor = vVertexColor;
		
		
		//point lights
		#ifdef INCLUDE_VERTEX_LIGHTING
		Out.VertexLighting = calculate_point_lights_diffuse(vWorldPos, vWorldN, false, true);
		#endif
		
		#ifndef USE_LIGHTING_PASS 
		const int effective_light_index = iLightIndices[0];
		float3 point_to_light = vLightPosDir[effective_light_index]-vWorldPos.xyz;
		Out.PointLightDir.xyz = mul(TBNMatrix, normalize(point_to_light));
		
		float LD = dot(point_to_light, point_to_light);
		Out.PointLightDir.a = saturate(1.0f/LD);	//prevent bloom for 1 meters
		#endif
		
		float3 viewdir = normalize(vCameraPos.xyz - vWorldPos.xyz);
		Out.ViewDir =  mul(TBNMatrix, viewdir);
		
		#ifndef USE_LIGHTING_PASS
		if (PcfMode == PCF_NONE)
		{
			Out.ShadowTexCoord = calculate_point_lights_specular(vWorldPos, vWorldN, viewdir, true);
		}
		#endif
	}
	else {

		Out.VertexColor = vVertexColor;
		#ifdef INCLUDE_VERTEX_LIGHTING
		Out.VertexLighting = calculate_point_lights_diffuse(vWorldPos, vWorldN, false, false);
		#endif
		
		Out.ViewDir =  normalize(vCameraPos.xyz - vWorldPos.xyz);
		
		Out.SunLightDir = vWorldN;
		#ifndef USE_LIGHTING_PASS
		Out.SkyLightDir = calculate_point_lights_specular(vWorldPos, vWorldN, Out.ViewDir, false);
		#endif
	}
	
	Out.VertexColor.a *= vMaterialColor.a;

	
	

	if (PcfMode != PCF_NONE)
	{
		float4 vWorldPos2 = mul(matWorld, vPos_without_movement);
		float4 ShadowPos = mul(matSunViewProj, vWorldPos);
		Out.ShadowTexCoord = ShadowPos;
		Out.ShadowTexCoord.z /= ShadowPos.w;
		Out.ShadowTexCoord.w = 1.0f;
		Out.ShadowTexelPos = Out.ShadowTexCoord * fShadowMapSize;
		//shadow mapping variables end
	}
	
	//apply fog
	float3 P = mul(matWorldView, vObjectPos); //position in view space
	float d = length(P);
	Out.Fog = get_fog_amount_new(d, vWorldPos.z);
		
	return Out;
}
//END SAILS


PS_OUTPUT ps_main_standart_sails ( VS_OUTPUT_STANDART In, uniform const int PcfMode, 
									uniform const bool use_bumpmap, uniform const bool use_specularfactor, 
									uniform const bool use_specularmap, uniform const bool ps2x, 
									uniform const bool use_aniso, uniform const bool terrain_color_ambient = true )
{ 
	PS_OUTPUT Output;

	float3 normal;
	if(use_bumpmap) {
		normal = (2.0f * tex2D(NormalTextureSampler, In.Tex0) - 1.0f);
	}
	else 
	{
		normal = In.SunLightDir;
	}
	
	float sun_amount = 1;
	if (PcfMode != PCF_NONE)
	{
		if((PcfMode == PCF_NVIDIA) || ps2x)		//we have more ins count for shadow, add some ambient factor to sun amount
			sun_amount = 0.05f + GetSunAmount(PcfMode, In.ShadowTexCoord, In.ShadowTexelPos);
		else
			sun_amount = GetSunAmount(PcfMode, In.ShadowTexCoord, In.ShadowTexelPos);
	}
		
	//define ambient term:
	const int ambientTermType = ( terrain_color_ambient && (ps2x || !use_specularfactor) ) ? 1 : 0;
	const float3 DirToSky = use_bumpmap ? In.SkyLightDir : float3(0.0f, 0.0f, 1.0f);
	float4 total_light = get_ambientTerm(ambientTermType, normal, DirToSky, sun_amount);
	
	
	float3 aniso_specular = 0;
	if(use_aniso) {
		if(!ps2x){
			GIVE_ERROR_HERE;
		}
		float3 direction = float3(0,1,0);
		aniso_specular  = calculate_hair_specular(normal, direction, ((use_bumpmap) ?  In.SunLightDir : -vSunDir), In.ViewDir, In.Tex0);
	}
		
	if( use_bumpmap) 
	{
		total_light.rgb += (saturate(dot(In.SunLightDir.xyz, normal.xyz)) + aniso_specular) * sun_amount * vSunColor;
	
		if(ps2x || !use_specularfactor) {
			total_light += saturate(dot(In.SkyLightDir.xyz, normal.xyz)) * vSkyLightColor;
		}
		#ifdef INCLUDE_VERTEX_LIGHTING
		if(ps2x || !use_specularfactor || (PcfMode == PCF_NONE))
		{
			total_light.rgb += In.VertexLighting;
		}
		#endif
		
		#ifndef USE_LIGHTING_PASS 
			float light_atten = In.PointLightDir.a;
			const int effective_light_index = iLightIndices[0];
			total_light += saturate(dot(In.PointLightDir.xyz, normal.xyz) * vLightDiffuse[effective_light_index]  * light_atten);
		#endif
	}
	else {
		total_light.rgb += (saturate(dot(-vSunDir, normal.xyz)) + aniso_specular) * sun_amount * vSunColor;
		
		if(ambientTermType != 1 && !ps2x) {
			total_light += saturate(dot(-vSkyLightDir.xyz, normal.xyz)) * vSkyLightColor;
		}
		#ifdef INCLUDE_VERTEX_LIGHTING
		total_light.rgb += In.VertexLighting;
		#endif
	}

	if (PcfMode != PCF_NONE)
		Output.RGBColor.rgb = total_light.rgb;
	else
		Output.RGBColor.rgb = min(total_light.rgb, 2.0f);
		
	// Output.RGBColor.rgb = total_light.rgb;	//saturate?
	Output.RGBColor.rgb *= vMaterialColor.rgb;
	
	float4 tex_col = tex2D(MeshTextureSampler, In.Tex0);
	INPUT_TEX_GAMMA(tex_col.rgb);

	Output.RGBColor.rgb *= tex_col.rgb;
	Output.RGBColor.rgb *= In.VertexColor.rgb;
	
	//add specular terms 
	if(use_specularfactor) {
		float4 fSpecular = 0;
		
		float4 specColor = 0.1 * spec_coef * vSpecularColor;
		if(use_specularmap) {
			float spec_tex_factor = dot(tex2D(SpecularTextureSampler, In.Tex0).rgb,0.33);	//get more precision from specularmap
			specColor *= spec_tex_factor;
		}
		else //if(use_specular_alpha)	//is that always true?
		{
			specColor *= tex_col.a;
		}
		
		float4 sun_specColor = specColor * vSunColor * sun_amount;
		
		//sun specular
		float3 vHalf = normalize( In.ViewDir + ((use_bumpmap) ?  In.SunLightDir : -vSunDir) );
		fSpecular = sun_specColor * pow( saturate(dot(vHalf, normal)), fMaterialPower);
		if(PcfMode != PCF_DEFAULT)	//we have 64 ins limit 
		{
			fSpecular *= In.VertexColor;
		}
		
		if(use_bumpmap) 
		{
			if(PcfMode == PCF_NONE)	//add point lights' specular color for indoors
			{
				fSpecular.rgb += specColor * In.ShadowTexCoord.rgb;	//ShadowTexCoord => point lights specular! (calculate_point_lights_specular)
			}
			
			//add more effects for ps2a version:
			if(ps2x || (PcfMode == PCF_NONE)) {
			
				#ifndef USE_LIGHTING_PASS 
				//effective point light specular
				float light_atten = In.PointLightDir.a;
				const int effective_light_index = iLightIndices[0];
				float4 light_specColor = specColor * vLightDiffuse[effective_light_index] * (light_atten * 0.5); 	//dec. spec term to remove "effective light change" artifacts
				vHalf = normalize( In.ViewDir + In.PointLightDir );
				fSpecular += light_specColor * pow( saturate(dot(vHalf, normal)), fMaterialPower);
				#endif
			}
		}
		else
		{
			fSpecular.rgb += specColor * In.SkyLightDir * 0.1;	//SkyLightDir-> holds lights specular color (calculate_point_lights_specular)
		}
			
		Output.RGBColor += fSpecular;
	}
	else if(use_specularmap) {
		GIVE_ERROR_HERE; 
	}
	
	OUTPUT_GAMMA(Output.RGBColor.rgb);	
	
	
	
	Output.RGBColor.r = 0.9;
	Output.RGBColor.gb = 0.2;
	
	
	//if we dont use alpha channel for specular-> use it for alpha
	Output.RGBColor.a = 1.0 ; //In.VertexColor.a;	//we dont control bUseMotionBlur to fit in 64 instruction
	
	if( (!use_specularfactor) || use_specularmap) {
		Output.RGBColor.a *= tex_col.a;
	}

	return Output;
}



PS_OUTPUT ps_main_standart ( VS_OUTPUT_STANDART In, uniform const int PcfMode, 
									uniform const bool use_bumpmap, uniform const bool use_specularfactor, 
									uniform const bool use_specularmap, uniform const bool ps2x, 
									uniform const bool use_aniso, uniform const bool terrain_color_ambient = true )
{ 
	PS_OUTPUT Output;

	float3 normal;
	if(use_bumpmap) {
		normal = (2.0f * tex2D(NormalTextureSampler, In.Tex0) - 1.0f);
	}
	else 
	{
		normal = In.SunLightDir;
	}
	
	float sun_amount = 1;
	if (PcfMode != PCF_NONE)
	{
		if((PcfMode == PCF_NVIDIA) || ps2x)		//we have more ins count for shadow, add some ambient factor to sun amount
			sun_amount = 0.05f + GetSunAmount(PcfMode, In.ShadowTexCoord, In.ShadowTexelPos);
		else
			sun_amount = GetSunAmount(PcfMode, In.ShadowTexCoord, In.ShadowTexelPos);
	}
		
	//define ambient term:
	const int ambientTermType = ( terrain_color_ambient && (ps2x || !use_specularfactor) ) ? 1 : 0;
	const float3 DirToSky = use_bumpmap ? In.SkyLightDir : float3(0.0f, 0.0f, 1.0f);
	float4 total_light = get_ambientTerm(ambientTermType, normal, DirToSky, sun_amount);
	
	
	float3 aniso_specular = 0;
	if(use_aniso) {
		if(!ps2x){
			GIVE_ERROR_HERE;
		}
		float3 direction = float3(0,1,0);
		aniso_specular  = calculate_hair_specular(normal, direction, ((use_bumpmap) ?  In.SunLightDir : -vSunDir), In.ViewDir, In.Tex0);
	}
		
	if( use_bumpmap) 
	{
		total_light.rgb += (saturate(dot(In.SunLightDir.xyz, normal.xyz)) + aniso_specular) * sun_amount * vSunColor;
	
		if(ps2x || !use_specularfactor) {
			total_light += saturate(dot(In.SkyLightDir.xyz, normal.xyz)) * vSkyLightColor;
		}
		#ifdef INCLUDE_VERTEX_LIGHTING
		if(ps2x || !use_specularfactor || (PcfMode == PCF_NONE))
		{
			total_light.rgb += In.VertexLighting;
		}
		#endif
		
		#ifndef USE_LIGHTING_PASS 
			float light_atten = In.PointLightDir.a;
			const int effective_light_index = iLightIndices[0];
			total_light += saturate(dot(In.PointLightDir.xyz, normal.xyz) * vLightDiffuse[effective_light_index]  * light_atten);
		#endif
	}
	else {
		total_light.rgb += (saturate(dot(-vSunDir, normal.xyz)) + aniso_specular) * sun_amount * vSunColor;
		
		if(ambientTermType != 1 && !ps2x) {
			total_light += saturate(dot(-vSkyLightDir.xyz, normal.xyz)) * vSkyLightColor;
		}
		#ifdef INCLUDE_VERTEX_LIGHTING
		total_light.rgb += In.VertexLighting;
		#endif
	}
	
	

	if (PcfMode != PCF_NONE)
		Output.RGBColor.rgb = total_light.rgb;
	else
		Output.RGBColor.rgb = min(total_light.rgb, 2.0f);
		
	// Output.RGBColor.rgb = total_light.rgb;	//saturate?
	Output.RGBColor.rgb *= vMaterialColor.rgb;
	
	float4 tex_col = tex2D(MeshTextureSampler, In.Tex0);
	INPUT_TEX_GAMMA(tex_col.rgb);

	Output.RGBColor.rgb *= tex_col.rgb;
	Output.RGBColor.rgb *= In.VertexColor.rgb;
	
	//add specular terms 
	if(use_specularfactor) {
		float4 fSpecular = 0;
		
		float4 specColor = 0.1 * spec_coef * vSpecularColor;
		if(use_specularmap) {
			float spec_tex_factor = dot(tex2D(SpecularTextureSampler, In.Tex0).rgb,0.33);	//get more precision from specularmap
			specColor *= spec_tex_factor;
		}
		else //if(use_specular_alpha)	//is that always true?
		{
			specColor *= tex_col.a;
		}
		
		float4 sun_specColor = specColor * vSunColor * sun_amount;
		
		//sun specular
		float3 vHalf = normalize( In.ViewDir + ((use_bumpmap) ?  In.SunLightDir : -vSunDir) );
		fSpecular = sun_specColor * pow( saturate(dot(vHalf, normal)), fMaterialPower);
		if(PcfMode != PCF_DEFAULT)	//we have 64 ins limit 
		{
			fSpecular *= In.VertexColor;
		}
		
		if(use_bumpmap) 
		{
			if(PcfMode == PCF_NONE)	//add point lights' specular color for indoors
			{
				fSpecular.rgb += specColor * In.ShadowTexCoord.rgb;	//ShadowTexCoord => point lights specular! (calculate_point_lights_specular)
			}
			
			//add more effects for ps2a version:
			if(ps2x || (PcfMode == PCF_NONE)) {
			
				#ifndef USE_LIGHTING_PASS 
				//effective point light specular
				float light_atten = In.PointLightDir.a;
				const int effective_light_index = iLightIndices[0];
				float4 light_specColor = specColor * vLightDiffuse[effective_light_index] * (light_atten * 0.5); 	//dec. spec term to remove "effective light change" artifacts
				vHalf = normalize( In.ViewDir + In.PointLightDir );
				fSpecular += light_specColor * pow( saturate(dot(vHalf, normal)), fMaterialPower);
				#endif
			}
		}
		else
		{
			fSpecular.rgb += specColor * In.SkyLightDir * 0.1;	//SkyLightDir-> holds lights specular color (calculate_point_lights_specular)
		}
			
		Output.RGBColor += fSpecular;
	}
	else if(use_specularmap) {
		GIVE_ERROR_HERE; 
	}
	
	OUTPUT_GAMMA(Output.RGBColor.rgb);	
	
	
	//if we dont use alpha channel for specular-> use it for alpha
	Output.RGBColor.a = In.VertexColor.a;	//we dont control bUseMotionBlur to fit in 64 instruction
	
	if( (!use_specularfactor) || use_specularmap) {
		Output.RGBColor.a *= tex_col.a;
	}

	return Output;
}





PS_OUTPUT ps_main_standart_fresnel ( VS_OUTPUT_STANDART In, uniform const int PcfMode, 
									uniform const bool use_bumpmap, uniform const bool use_specularfactor, 
									uniform const bool use_specularmap, uniform const bool ps2x, 
									uniform const bool use_aniso, uniform const bool terrain_color_ambient = true )
{ 
	PS_OUTPUT Output;

	float3 normal;
	if(use_bumpmap) {
		normal = (2.0f * tex2D(NormalTextureSampler, In.Tex0) - 1.0f);
	}
	else 
	{
		normal = In.SunLightDir;
	}
	
	float sun_amount = 1;
	if (PcfMode != PCF_NONE)
	{
		if((PcfMode == PCF_NVIDIA) || ps2x)		//we have more ins count for shadow, add some ambient factor to sun amount
			sun_amount = 0.05f + GetSunAmount(PcfMode, In.ShadowTexCoord, In.ShadowTexelPos);
		else
			sun_amount = GetSunAmount(PcfMode, In.ShadowTexCoord, In.ShadowTexelPos);
	}
		
	//define ambient term:
	const int ambientTermType = ( terrain_color_ambient && (ps2x || !use_specularfactor) ) ? 1 : 0;
	const float3 DirToSky = use_bumpmap ? In.SkyLightDir : float3(0.0f, 0.0f, 1.0f);
	float4 total_light = get_ambientTerm(ambientTermType, normal, DirToSky, sun_amount);
	
	
	float3 aniso_specular = 0;
	if(use_aniso) {
		if(!ps2x){
			GIVE_ERROR_HERE;
		}
		float3 direction = float3(0,1,0);
		aniso_specular  = calculate_hair_specular(normal, direction, ((use_bumpmap) ?  In.SunLightDir : -vSunDir), In.ViewDir, In.Tex0);
	}
		
	if( use_bumpmap) 
	{
		total_light.rgb += (saturate(dot(In.SunLightDir.xyz, normal.xyz)) + aniso_specular) * sun_amount * vSunColor;
	
		if(ps2x || !use_specularfactor) {
			total_light += saturate(dot(In.SkyLightDir.xyz, normal.xyz)) * vSkyLightColor;
		}
		#ifdef INCLUDE_VERTEX_LIGHTING
		if(ps2x || !use_specularfactor || (PcfMode == PCF_NONE))
		{
			total_light.rgb += In.VertexLighting;
		}
		#endif
		
		#ifndef USE_LIGHTING_PASS 
			float light_atten = In.PointLightDir.a;
			const int effective_light_index = iLightIndices[0];
			total_light += saturate(dot(In.PointLightDir.xyz, normal.xyz) * vLightDiffuse[effective_light_index]  * light_atten);
		#endif
	}
	else {
		total_light.rgb += (saturate(dot(-vSunDir, normal.xyz)) + aniso_specular) * sun_amount * vSunColor;
		
		if(ambientTermType != 1 && !ps2x) {
			total_light += saturate(dot(-vSkyLightDir.xyz, normal.xyz)) * vSkyLightColor;
		}
		#ifdef INCLUDE_VERTEX_LIGHTING
		total_light.rgb += In.VertexLighting;
		#endif
	}
	
	
		
	//FRESNEL
	float3 vView = normalize(In.ViewDir);
	float3 fresnel = 1-(saturate(dot(vView, normal)));
	fresnel = 0.0204f + 0.9796 * (fresnel* fresnel * fresnel * fresnel);
	fresnel *= 4.0;
	total_light.rgb += total_light*fresnel; 
	fresnel = pow(fresnel,2);
	total_light.rgb += 0.020*(total_light*fresnel); 
//	total_light = saturate(total_light);
///////////	

	
	

	if (PcfMode != PCF_NONE)
		Output.RGBColor.rgb = total_light.rgb;
	else
		Output.RGBColor.rgb = min(total_light.rgb, 2.0f);
		
	// Output.RGBColor.rgb = total_light.rgb;	//saturate?
	Output.RGBColor.rgb *= vMaterialColor.rgb;
	
	float4 tex_col = tex2D(MeshTextureSampler, In.Tex0);
	INPUT_TEX_GAMMA(tex_col.rgb);

	Output.RGBColor.rgb *= tex_col.rgb;
	Output.RGBColor.rgb *= In.VertexColor.rgb;
	
	//add specular terms 
	if(use_specularfactor) {
		float4 fSpecular = 0;
		
		float4 specColor = 0.1 * spec_coef * vSpecularColor;
		if(use_specularmap) {
			float spec_tex_factor = dot(tex2D(SpecularTextureSampler, In.Tex0).rgb,0.33);	//get more precision from specularmap
			specColor *= spec_tex_factor;
		}
		else //if(use_specular_alpha)	//is that always true?
		{
			specColor *= tex_col.a;
		}
		
		float4 sun_specColor = specColor * vSunColor * sun_amount;
		
		//sun specular
		float3 vHalf = normalize( In.ViewDir + ((use_bumpmap) ?  In.SunLightDir : -vSunDir) );
		fSpecular = sun_specColor * pow( saturate(dot(vHalf, normal)), fMaterialPower);
		if(PcfMode != PCF_DEFAULT)	//we have 64 ins limit 
		{
			fSpecular *= In.VertexColor;
		}
		
		if(use_bumpmap) 
		{
			if(PcfMode == PCF_NONE)	//add point lights' specular color for indoors
			{
				fSpecular.rgb += specColor * In.ShadowTexCoord.rgb;	//ShadowTexCoord => point lights specular! (calculate_point_lights_specular)
			}
			
			//add more effects for ps2a version:
			if(ps2x || (PcfMode == PCF_NONE)) {
			
				#ifndef USE_LIGHTING_PASS 
				//effective point light specular
				float light_atten = In.PointLightDir.a;
				const int effective_light_index = iLightIndices[0];
				float4 light_specColor = specColor * vLightDiffuse[effective_light_index] * (light_atten * 0.5); 	//dec. spec term to remove "effective light change" artifacts
				vHalf = normalize( In.ViewDir + In.PointLightDir );
				fSpecular += light_specColor * pow( saturate(dot(vHalf, normal)), fMaterialPower);
				#endif
			}
		}
		else
		{
			fSpecular.rgb += specColor * In.SkyLightDir * 0.1;	//SkyLightDir-> holds lights specular color (calculate_point_lights_specular)
		}
			
		Output.RGBColor += fSpecular;
	}
	else if(use_specularmap) {
		GIVE_ERROR_HERE; 
	}
	
	OUTPUT_GAMMA(Output.RGBColor.rgb);	
	
	
	//if we dont use alpha channel for specular-> use it for alpha
	Output.RGBColor.a = In.VertexColor.a;	//we dont control bUseMotionBlur to fit in 64 instruction
	
	if( (!use_specularfactor) || use_specularmap) {
		Output.RGBColor.a *= tex_col.a;
	}

	return Output;
}









PS_OUTPUT ps_main_standart_old_good( VS_OUTPUT_STANDART In, uniform const int PcfMode, uniform const bool use_specularmap, uniform const bool use_aniso )
{
	PS_OUTPUT Output;
	
	
	float sun_amount = 1;
	if (PcfMode != PCF_NONE)
	{
		sun_amount = 0.03f + GetSunAmount(PcfMode, In.ShadowTexCoord, In.ShadowTexelPos);
	}

	float3 normal = (2.0f * tex2D(NormalTextureSampler, In.Tex0) - 1.0f);
	
	//define ambient term:
	static const int ambientTermType = 1;
	float3 DirToSky = In.SkyLightDir;
	float4 total_light = get_ambientTerm(ambientTermType, normal, DirToSky, sun_amount);
	
	float4 specColor = vSunColor * (vSpecularColor*0.1);
	if(use_specularmap) {
		float spec_tex_factor = dot(tex2D(SpecularTextureSampler, In.Tex0).rgb,0.33);	//get more precision from specularmap
		specColor *= spec_tex_factor;
	}
	
	float3 vHalf = normalize(In.ViewDir + In.SunLightDir);
	float4 fSpecular = specColor * pow( saturate(dot(vHalf, normal)), fMaterialPower); // saturate(dot(In.SunLightDir, normal));
	
	
	if(use_aniso) {
		float3 tangent_ = float3(0,1,0);
		fSpecular.rgb += calculate_hair_specular(normal, tangent_, In.SunLightDir, In.ViewDir, In.Tex0);
	}
	else {
		fSpecular.rgb *= spec_coef;
	}
	
		
	total_light += (saturate(dot(In.SunLightDir.xyz, normal.xyz)) + fSpecular) * sun_amount * vSunColor;
	total_light += saturate(dot(In.SkyLightDir.xyz, normal.xyz)) * vSkyLightColor;
	
	
	#ifndef USE_LIGHTING_PASS 
	float light_atten = In.PointLightDir.a;
	const int effective_light_index = iLightIndices[0];
	total_light += saturate(dot(In.PointLightDir.xyz, normal.xyz)) * vLightDiffuse[effective_light_index]  * light_atten;
	#endif
	
	#ifdef INCLUDE_VERTEX_LIGHTING
		total_light.rgb += In.VertexLighting;
	#endif
	

	Output.RGBColor.rgb = total_light.rgb; //saturate(total_light.rgb);	//false!
	Output.RGBColor.a = 1.0f;
	Output.RGBColor *= vMaterialColor;
	
	float4 tex_col = tex2D(MeshTextureSampler, In.Tex0);
	INPUT_TEX_GAMMA(tex_col.rgb);

	Output.RGBColor *= tex_col;
	Output.RGBColor *= In.VertexColor;
	
	OUTPUT_GAMMA(Output.RGBColor.rgb);	
	Output.RGBColor.a = In.VertexColor.a * tex_col.a;

	return Output;
}

#ifdef USE_PRECOMPILED_SHADER_LISTS
																		//use_bumpmap, use_skinning, 
VertexShader standart_vs_noshadow[] = { compile vs_2_0 vs_main_standart(PCF_NONE, 0,0), 
										compile vs_2_0 vs_main_standart(PCF_NONE, 0,1), 
										compile vs_2_0 vs_main_standart(PCF_NONE, 1,0), 
										compile vs_2_0 vs_main_standart(PCF_NONE, 1,1)};
										
VertexShader standart_vs_default[] = { 	compile vs_2_0 vs_main_standart(PCF_DEFAULT, 0,0), 
										compile vs_2_0 vs_main_standart(PCF_DEFAULT, 0,1), 
										compile vs_2_0 vs_main_standart(PCF_DEFAULT, 1,0), 
										compile vs_2_0 vs_main_standart(PCF_DEFAULT, 1,1)};
										                            
VertexShader standart_vs_nvidia[] = { 	compile vs_2_0 vs_main_standart(PCF_NVIDIA, 0,0), 	//ps_main_standart compiled versions?!
										compile vs_2_0 vs_main_standart(PCF_NVIDIA, 0,1), 
										compile vs_2_0 vs_main_standart(PCF_NVIDIA, 1,0), 
										compile vs_2_0 vs_main_standart(PCF_NVIDIA, 1,1)};
										
#define DEFINE_STANDART_TECHNIQUE(tech_name, use_bumpmap, use_skinning, use_specularfactor, use_specularmap, use_aniso, terraincolor)	\
				technique tech_name	\
				{ pass P0 { VertexShader = standart_vs_noshadow[(2*use_bumpmap) + use_skinning]; \
							PixelShader = compile ps_2_0 ps_main_standart(PCF_NONE, use_bumpmap, use_specularfactor, use_specularmap, false, use_aniso, terraincolor);} } \
				technique tech_name##_SHDW	\
				{ pass P0 { VertexShader = standart_vs_default[(2*use_bumpmap) + use_skinning]; \
							PixelShader = compile ps_2_0 ps_main_standart(PCF_DEFAULT, use_bumpmap, use_specularfactor, use_specularmap, false, use_aniso, terraincolor);} } \
				technique tech_name##_SHDWNVIDIA	\
				{ pass P0 { VertexShader = standart_vs_nvidia[(2*use_bumpmap) + use_skinning]; \
							PixelShader = compile ps_2_a ps_main_standart(PCF_NVIDIA, use_bumpmap, use_specularfactor, use_specularmap, true, use_aniso, terraincolor);} }  \
				DEFINE_LIGHTING_TECHNIQUE(tech_name, 0, use_bumpmap, use_skinning, use_specularfactor, use_specularmap)

							
#define DEFINE_STANDART_TECHNIQUE_HIGH(tech_name, use_bumpmap, use_skinning, use_specularfactor, use_specularmap, use_aniso, terraincolor)	\
				technique tech_name	\
				{ pass P0 { VertexShader = compile vs_2_0 vs_main_standart(PCF_NONE, use_bumpmap, use_skinning); \
							PixelShader = compile PS_2_X ps_main_standart(PCF_NONE, use_bumpmap, use_specularfactor, use_specularmap, true, use_aniso, terraincolor);} } \
				technique tech_name##_SHDW	\
				{ pass P0 { VertexShader = compile vs_2_0 vs_main_standart(PCF_DEFAULT, use_bumpmap, use_skinning); \
							PixelShader = compile PS_2_X ps_main_standart(PCF_DEFAULT, use_bumpmap, use_specularfactor, use_specularmap, true, use_aniso, terraincolor);} } \
				technique tech_name##_SHDWNVIDIA	\
				{ pass P0 { VertexShader = compile vs_2_0 vs_main_standart(PCF_NVIDIA, use_bumpmap, use_skinning); \
							PixelShader = compile ps_2_a ps_main_standart(PCF_NVIDIA, use_bumpmap, use_specularfactor, use_specularmap, true, use_aniso, terraincolor);} } \
				DEFINE_LIGHTING_TECHNIQUE(tech_name, 0, use_bumpmap, use_skinning, use_specularfactor, use_specularmap)
				
////FRESNEL				
#define DEFINE_STANDART_TECHNIQUE_HIGH_FRESNEL(tech_name, use_bumpmap, use_skinning, use_specularfactor, use_specularmap, use_aniso, terraincolor)	\
				technique tech_name	\
				{ pass P0 { VertexShader = compile vs_2_0 vs_main_standart(PCF_NONE, use_bumpmap, use_skinning); \
							PixelShader = compile PS_2_X ps_main_standart_fresnel(PCF_NONE, use_bumpmap, use_specularfactor, use_specularmap, true, use_aniso, terraincolor);} } \
				technique tech_name##_SHDW	\
				{ pass P0 { VertexShader = compile vs_2_0 vs_main_standart(PCF_DEFAULT, use_bumpmap, use_skinning); \
							PixelShader = compile PS_2_X ps_main_standart_fresnel(PCF_DEFAULT, use_bumpmap, use_specularfactor, use_specularmap, true, use_aniso, terraincolor);} } \
				technique tech_name##_SHDWNVIDIA	\
				{ pass P0 { VertexShader = compile vs_2_0 vs_main_standart(PCF_NVIDIA, use_bumpmap, use_skinning); \
							PixelShader = compile PS_2_X ps_main_standart_fresnel(PCF_NVIDIA, use_bumpmap, use_specularfactor, use_specularmap, true, use_aniso, terraincolor);} } \
				DEFINE_LIGHTING_TECHNIQUE(tech_name, 0, use_bumpmap, use_skinning, use_specularfactor, use_specularmap)
//////
				
#define DEFINE_STANDART_TECHNIQUE_INSTANCED(tech_name, use_bumpmap, use_skinning, use_specularfactor, use_specularmap, use_aniso, terraincolor)	\
				technique tech_name	\
				{ pass P0 { VertexShader = compile vs_2_0 vs_main_standart_Instanced(PCF_NONE, use_bumpmap, false); \
							PixelShader = compile PS_2_X ps_main_standart(PCF_NONE, use_bumpmap, use_specularfactor, use_specularmap, true, use_aniso, terraincolor);} } \
				technique tech_name##_SHDW	\
				{ pass P0 { VertexShader = compile vs_2_0 vs_main_standart_Instanced(PCF_DEFAULT, use_bumpmap, false); \
							PixelShader = compile PS_2_X ps_main_standart(PCF_DEFAULT, use_bumpmap, use_specularfactor, use_specularmap, true, use_aniso, terraincolor);} } \
				technique tech_name##_SHDWNVIDIA	\
				{ pass P0 { VertexShader = compile vs_2_0 vs_main_standart_Instanced(PCF_NVIDIA, use_bumpmap, false); \
							PixelShader = compile ps_2_a ps_main_standart(PCF_NVIDIA, use_bumpmap, use_specularfactor, use_specularmap, true, use_aniso, terraincolor);} } //lighting?
							
							
#define DEFINE_STANDART_TECHNIQUE_HIGH_INSTANCED(tech_name, use_bumpmap, use_skinning, use_specularfactor, use_specularmap, use_aniso)	\
				technique tech_name	\
				{ pass P0 { VertexShader = compile vs_2_0 vs_main_standart_Instanced(PCF_NONE, use_bumpmap, use_skinning); \
							PixelShader = compile PS_2_X ps_main_standart(PCF_NONE, use_bumpmap, use_specularfactor, use_specularmap, true, use_aniso);} } \
				technique tech_name##_SHDW	\
				{ pass P0 { VertexShader = compile vs_2_0 vs_main_standart_Instanced(PCF_DEFAULT, use_bumpmap, use_skinning); \
							PixelShader = compile PS_2_X ps_main_standart(PCF_DEFAULT, use_bumpmap, use_specularfactor, use_specularmap, true, use_aniso);} } \
				technique tech_name##_SHDWNVIDIA	\
				{ pass P0 { VertexShader = compile vs_2_0 vs_main_standart_Instanced(PCF_NVIDIA, use_bumpmap, use_skinning); \
							PixelShader = compile ps_2_a ps_main_standart(PCF_NVIDIA, use_bumpmap, use_specularfactor, use_specularmap, true, use_aniso);} } 

//FOR SAILS SAME AS STANDART_TECHNIQUE_HIGH but uses vertex shader vs_main_standart_sails
#define DEFINE_STANDART_TECHNIQUE_HIGH_SAILS(tech_name, use_bumpmap, use_skinning, use_specularfactor, use_specularmap, use_aniso, terraincolor)	\
				technique tech_name	\
				{ pass P0 { VertexShader = compile vs_2_0 vs_main_standart_sails(PCF_NONE, use_bumpmap, use_skinning); \
							PixelShader = compile PS_2_X ps_main_standart_fresnel(PCF_NONE, use_bumpmap, use_specularfactor, use_specularmap, true, use_aniso, terraincolor);} } \
				technique tech_name##_SHDW	\
				{ pass P0 { VertexShader = compile vs_2_0 vs_main_standart_sails(PCF_DEFAULT, use_bumpmap, use_skinning); \
							PixelShader = compile PS_2_X ps_main_standart_fresnel(PCF_DEFAULT, use_bumpmap, use_specularfactor, use_specularmap, true, use_aniso, terraincolor);} } \
				technique tech_name##_SHDWNVIDIA	\
				{ pass P0 { VertexShader = compile vs_2_0 vs_main_standart_sails(PCF_NVIDIA, use_bumpmap, use_skinning); \
							PixelShader = compile PS_2_X ps_main_standart_fresnel(PCF_NVIDIA, use_bumpmap, use_specularfactor, use_specularmap, true, use_aniso, terraincolor);} } \
				DEFINE_LIGHTING_TECHNIQUE(tech_name, 0, use_bumpmap, use_skinning, use_specularfactor, use_specularmap)							
				
#else 

#define DEFINE_STANDART_TECHNIQUE(tech_name, use_bumpmap, use_skinning, use_specularfactor, use_specularmap, use_aniso)	\
				technique tech_name	\
				{ pass P0 { VertexShader = compile vs_2_0 vs_main_standart(PCF_NONE, use_bumpmap, use_skinning); \
							PixelShader = compile ps_2_0 ps_main_standart(PCF_NONE, use_bumpmap, use_specularfactor, use_specularmap, false, use_aniso);} } \
				technique tech_name##_SHDW	\
				{ pass P0 { VertexShader = compile vs_2_0 vs_main_standart(PCF_DEFAULT, use_bumpmap, use_skinning); \
							PixelShader = compile ps_2_0 ps_main_standart(PCF_DEFAULT, use_bumpmap, use_specularfactor, use_specularmap, false, use_aniso);} } \
				technique tech_name##_SHDWNVIDIA	\
				{ pass P0 { VertexShader = compile vs_2_0 vs_main_standart(PCF_NVIDIA, use_bumpmap, use_skinning); \
							PixelShader = compile ps_2_a ps_main_standart(PCF_NVIDIA, use_bumpmap, use_specularfactor, use_specularmap, true, use_aniso);} }  \
				DEFINE_LIGHTING_TECHNIQUE(tech_name, 0, use_bumpmap, use_skinning, use_specularfactor, use_specularmap)

							

#define DEFINE_STANDART_TECHNIQUE_HIGH(tech_name, use_bumpmap, use_skinning, use_specularfactor, use_specularmap, use_aniso)	\
				technique tech_name	\
				{ pass P0 { VertexShader = compile vs_2_0 vs_main_standart(PCF_NONE, use_bumpmap, use_skinning); \
							PixelShader = compile PS_2_X ps_main_standart(PCF_NONE, use_bumpmap, use_specularfactor, use_specularmap, true, use_aniso);} } \
				technique tech_name##_SHDW	\
				{ pass P0 { VertexShader = compile vs_2_0 vs_main_standart(PCF_DEFAULT, use_bumpmap, use_skinning); \
							PixelShader = compile PS_2_X ps_main_standart(PCF_DEFAULT, use_bumpmap, use_specularfactor, use_specularmap, true, use_aniso);} } \
				technique tech_name##_SHDWNVIDIA	\
				{ pass P0 { VertexShader = compile vs_2_0 vs_main_standart(PCF_NVIDIA, use_bumpmap, use_skinning); \
							PixelShader = compile ps_2_a ps_main_standart(PCF_NVIDIA, use_bumpmap, use_specularfactor, use_specularmap, true, use_aniso);} } \
				DEFINE_LIGHTING_TECHNIQUE(tech_name, 0, use_bumpmap, use_skinning, use_specularfactor, use_specularmap)

				
///FRESNEL				
#define DEFINE_STANDART_TECHNIQUE_HIGH_FRESNEL(tech_name, use_bumpmap, use_skinning, use_specularfactor, use_specularmap, use_aniso)	\
				technique tech_name	\
				{ pass P0 { VertexShader = compile vs_2_0 vs_main_standart(PCF_NONE, use_bumpmap, use_skinning); \
							PixelShader = compile PS_2_X ps_main_standart_fresnel(PCF_NONE, use_bumpmap, use_specularfactor, use_specularmap, true, use_aniso);} } \
				technique tech_name##_SHDW	\
				{ pass P0 { VertexShader = compile vs_2_0 vs_main_standart(PCF_DEFAULT, use_bumpmap, use_skinning); \
							PixelShader = compile PS_2_X ps_main_standart_fresnel(PCF_DEFAULT, use_bumpmap, use_specularfactor, use_specularmap, true, use_aniso);} } \
				technique tech_name##_SHDWNVIDIA	\
				{ pass P0 { VertexShader = compile vs_2_0 vs_main_standart(PCF_NVIDIA, use_bumpmap, use_skinning); \
							PixelShader = compile PS_2_X ps_main_standart_fresnel(PCF_NVIDIA, use_bumpmap, use_specularfactor, use_specularmap, true, use_aniso);} } \
				DEFINE_LIGHTING_TECHNIQUE(tech_name, 0, use_bumpmap, use_skinning, use_specularfactor, use_specularmap)
/////////////////						

				
#define DEFINE_STANDART_TECHNIQUE_INSTANCED(tech_name, use_bumpmap, use_skinning, use_specularfactor, use_specularmap, use_aniso)	\
				technique tech_name	\
				{ pass P0 { VertexShader = compile vs_2_0 vs_main_standart_Instanced(PCF_NONE, use_bumpmap, false); \
							PixelShader = compile PS_2_X ps_main_standart(PCF_NONE, use_bumpmap, use_specularfactor, use_specularmap, true, use_aniso);} } \
				technique tech_name##_SHDW	\
				{ pass P0 { VertexShader = compile vs_2_0 vs_main_standart_Instanced(PCF_DEFAULT, use_bumpmap, false); \
							PixelShader = compile PS_2_X ps_main_standart(PCF_DEFAULT, use_bumpmap, use_specularfactor, use_specularmap, true, use_aniso);} } \
				technique tech_name##_SHDWNVIDIA	\
				{ pass P0 { VertexShader = compile vs_2_0 vs_main_standart_Instanced(PCF_NVIDIA, use_bumpmap, false); \
							PixelShader = compile ps_2_a ps_main_standart(PCF_NVIDIA, use_bumpmap, use_specularfactor, use_specularmap, true, use_aniso);} } // lighting?
							
							
#define DEFINE_STANDART_TECHNIQUE_HIGH_INSTANCED(tech_name, use_bumpmap, use_skinning, use_specularfactor, use_specularmap, use_aniso)	\
				technique tech_name	\
				{ pass P0 { VertexShader = compile vs_2_0 vs_main_standart_Instanced(PCF_NONE, use_bumpmap, use_skinning); \
							PixelShader = compile PS_2_X ps_main_standart(PCF_NONE, use_bumpmap, use_specularfactor, use_specularmap, true, use_aniso);} } \
				technique tech_name##_SHDW	\
				{ pass P0 { VertexShader = compile vs_2_0 vs_main_standart_Instanced(PCF_DEFAULT, use_bumpmap, use_skinning); \
							PixelShader = compile PS_2_X ps_main_standart(PCF_DEFAULT, use_bumpmap, use_specularfactor, use_specularmap, true, use_aniso);} } \
				technique tech_name##_SHDWNVIDIA	\
				{ pass P0 { VertexShader = compile vs_2_0 vs_main_standart_Instanced(PCF_NVIDIA, use_bumpmap, use_skinning); \
							PixelShader = compile ps_2_a ps_main_standart(PCF_NVIDIA, use_bumpmap, use_specularfactor, use_specularmap, true, use_aniso);} } 

#define DEFINE_STANDART_TECHNIQUE_HIGH_SAILS(tech_name, use_bumpmap, use_skinning, use_specularfactor, use_specularmap, use_aniso)	\
				technique tech_name	\
				{ pass P0 { VertexShader = compile vs_2_0 vs_main_standart_sails(PCF_NONE, use_bumpmap, use_skinning); \
							PixelShader = compile PS_2_X ps_main_standart_fresnel(PCF_NONE, use_bumpmap, use_specularfactor, use_specularmap, true, use_aniso);} } \
				technique tech_name##_SHDW	\
				{ pass P0 { VertexShader = compile vs_2_0 vs_main_standart_sails(PCF_DEFAULT, use_bumpmap, use_skinning); \
							PixelShader = compile PS_2_X ps_main_standart_fresnel(PCF_DEFAULT, use_bumpmap, use_specularfactor, use_specularmap, true, use_aniso);} } \
				technique tech_name##_SHDWNVIDIA	\
				{ pass P0 { VertexShader = compile vs_2_0 vs_main_standart_sails(PCF_NVIDIA, use_bumpmap, use_skinning); \
							PixelShader = compile PS_2_X ps_main_standart_fresnel(PCF_NVIDIA, use_bumpmap, use_specularfactor, use_specularmap, true, use_aniso);} } \
				DEFINE_LIGHTING_TECHNIQUE(tech_name, 0, use_bumpmap, use_skinning, use_specularfactor, use_specularmap)

				
#endif //USE_PRECOMPILED_SHADER_LISTS


DEFINE_STANDART_TECHNIQUE( standart_noskin_bump_nospecmap, 				true, false, true, false, false, true)
DEFINE_STANDART_TECHNIQUE( standart_noskin_bump_specmap, 				true, false, true, true,  false, true)
DEFINE_STANDART_TECHNIQUE( standart_skin_bump_nospecmap, 				true, true,  true, false, false, true)
DEFINE_STANDART_TECHNIQUE( standart_skin_bump_specmap, 					true, true,  true, true,  false, true)
                        
//high versions: 
DEFINE_STANDART_TECHNIQUE_HIGH( standart_skin_bump_nospecmap_high, 		true, true,  true, false, false, true)
DEFINE_STANDART_TECHNIQUE_HIGH( standart_skin_bump_specmap_high, 		true, true,  true, true , false, true)

//fresnel
DEFINE_STANDART_TECHNIQUE_HIGH_FRESNEL(standart_skin_bump_specmap_high_fresnel, 		true, true,  true, true , false, true)
///

DEFINE_STANDART_TECHNIQUE_HIGH( standart_noskin_bump_nospecmap_high, 	true, false,  true, false, false, true)
DEFINE_STANDART_TECHNIQUE_HIGH( standart_noskin_bump_specmap_high, 		true, false,  true, true , false, true)
           
//SAILS - SAME AS ABOVE BASICALLY BUT WITH MOVEMENT		   
DEFINE_STANDART_TECHNIQUE_HIGH_SAILS (standart_noskin_bump_specmap_high_sails, 		true, false,  true, true , false, true)			
//-----------------------------------------------
//nobump versions:
DEFINE_STANDART_TECHNIQUE( standart_noskin_nobump_nospecmap, 			false, false, true, false, false, true)
DEFINE_STANDART_TECHNIQUE( standart_noskin_nobump_specmap, 				false, false, true, true , false, true)
DEFINE_STANDART_TECHNIQUE( standart_skin_nobump_nospecmap, 				false,  true, true, false, false, true)
DEFINE_STANDART_TECHNIQUE( standart_skin_nobump_specmap, 				false,  true, true, true , false, true)
                                                                                        
//-----------------------------------------------
//nospec versions:
//
DEFINE_STANDART_TECHNIQUE( standart_noskin_nobump_nospec, 				false, false, false, false, false, true)
DEFINE_STANDART_TECHNIQUE( standart_noskin_bump_nospec, 				true,  false, false, false, false, true)
DEFINE_STANDART_TECHNIQUE( standart_noskin_bump_nospec_noterraincolor, 	true,  false, false, false, false, false)
DEFINE_STANDART_TECHNIQUE( standart_skin_nobump_nospec, 				false,  true, false, false, false, true)
DEFINE_STANDART_TECHNIQUE( standart_skin_bump_nospec, 					true,   true, false, false, false, true)
                                                                                         
//nospec_high
DEFINE_STANDART_TECHNIQUE_HIGH( standart_noskin_bump_nospec_high, 				true, false, false, false, false, true)
DEFINE_STANDART_TECHNIQUE_HIGH( standart_noskin_bump_nospec_high_noterraincolor,true, false, false, false, false, false)
DEFINE_STANDART_TECHNIQUE_HIGH( standart_skin_bump_nospec_high, 				true,  true, false, false, false, true)


///--------
DEFINE_STANDART_TECHNIQUE_INSTANCED( standart_noskin_bump_nospecmap_Instanced, 					true, false, true, false, false, true)
DEFINE_STANDART_TECHNIQUE_INSTANCED( standart_noskin_nobump_specmap_Instanced, 					false, false, true, true , false, true)
DEFINE_STANDART_TECHNIQUE_INSTANCED( standart_noskin_bump_specmap_Instanced, 					true, false, true, true,  false, true)
DEFINE_STANDART_TECHNIQUE_INSTANCED( standart_noskin_nobump_nospecmap_Instanced, 				false, false, true, false, false, true)
DEFINE_STANDART_TECHNIQUE_INSTANCED( standart_noskin_bump_nospec_high_Instanced, 				true, false, false, false, false, true)
DEFINE_STANDART_TECHNIQUE_INSTANCED( standart_noskin_bump_nospec_high_noterraincolor_Instanced, true, false, false, false, false, false)

DEFINE_STANDART_TECHNIQUE_HIGH_INSTANCED( standart_noskin_bump_specmap_high_Instanced, 		true, false,  true, true , false)
DEFINE_STANDART_TECHNIQUE_HIGH_INSTANCED( standart_noskin_bump_nospecmap_high_Instanced, 	true, false,  true, false, false)

//aniso versions:       
// technique nospecular_skin_bumpmap_high_aniso
technique standart_skin_bump_nospecmap_high_aniso
{
	pass P0
	{
		VertexShader = compile vs_2_0 vs_main_standart(PCF_NONE, true, true);
		//PixelShader = compile PS_2_X ps_main_standart(PCF_NONE, true, true, false, true, true);
		PixelShader = compile PS_2_X ps_main_standart_old_good(PCF_NONE, false, true);
	}
}
technique standart_skin_bump_nospecmap_high_aniso_SHDW
{
	pass P0
	{
		VertexShader = compile vs_2_0 vs_main_standart(PCF_DEFAULT, true, true);
		//PixelShader = compile PS_2_X ps_main_standart(PCF_DEFAULT, true, true, false, true, true);
		PixelShader = compile PS_2_X ps_main_standart_old_good(PCF_DEFAULT, false, true);
	}
}
technique standart_skin_bump_nospecmap_high_aniso_SHDWNVIDIA
{
	pass P0
	{
		VertexShader = compile vs_2_a vs_main_standart(PCF_NVIDIA, true, true);
		//PixelShader = compile ps_2_a ps_main_standart(PCF_NVIDIA, true, true, false, true, true);
		PixelShader = compile ps_2_a ps_main_standart_old_good(PCF_NVIDIA, false, true);
	}
}

// technique specular_skin_bumpmap_high_aniso
technique standart_skin_bump_specmap_high_aniso
{
	pass P0
	{
		VertexShader = compile vs_2_0 vs_main_standart(PCF_NONE, true, true);
		//PixelShader = compile PS_2_X ps_main_standart(PCF_NONE, true, true, true, true, true);
		PixelShader = compile PS_2_X ps_main_standart_old_good(PCF_NONE, true, true);
	}
}
technique standart_skin_bump_specmap_high_aniso_SHDW
{
	pass P0
	{
		VertexShader = compile vs_2_0 vs_main_standart(PCF_DEFAULT, true, true);
		//PixelShader = compile PS_2_X ps_main_standart(PCF_DEFAULT, true, true, true, true, true);
		PixelShader = compile PS_2_X ps_main_standart_old_good(PCF_DEFAULT, true, true);
	}
}
technique standart_skin_bump_specmap_high_aniso_SHDWNVIDIA
{
	pass P0
	{
		VertexShader = compile vs_2_a vs_main_standart(PCF_NVIDIA, true, true);
		//PixelShader = compile ps_2_a ps_main_standart(PCF_NVIDIA, true, true, true, true);
		PixelShader = compile ps_2_a ps_main_standart_old_good(PCF_NVIDIA, true, true);
	}
}


// !  technique specular_diffuse -> standart_noskin_nobump_specmap
// !  technique specular_diffuse_skin -> standart_skin_nobump_specmap
// !  technique specular_alpha -> standart_noskin_nobump_nospecmap
// !  technique specular_alpha_skin -> standart_skin_nobump_nospecmap
////////////////////////////
#endif

/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#ifdef HAIR_SHADERS

struct VS_OUTPUT_SIMPLE_HAIR
{
	float4 Pos					: POSITION;
	float4 Color				: COLOR0;
	float2 Tex0					: TEXCOORD0;
	float4 SunLight				: TEXCOORD1;
	float4 ShadowTexCoord		: TEXCOORD2;
	float2 ShadowTexelPos		: TEXCOORD3;
	float  Fog				    : FOG;
};

VS_OUTPUT_SIMPLE_HAIR vs_hair (uniform const int PcfMode, float4 vPosition : POSITION, float3 vNormal : NORMAL, float2 tc : TEXCOORD0, float4 vColor : COLOR0)
{
	INITIALIZE_OUTPUT(VS_OUTPUT_SIMPLE_HAIR, Out);
	
	Out.Pos = mul(matWorldViewProj, vPosition);

	float4 vWorldPos = (float4)mul(matWorld,vPosition);
	float3 vWorldN = normalize(mul((float3x3)matWorld, vNormal)); //normal in world space

	float3 P = mul(matWorldView, vPosition); //position in view space

	Out.Tex0 = tc;

	float4 diffuse_light = vAmbientColor;
	//   diffuse_light.rgb *= gradient_factor * (gradient_offset + vWorldN.z);

	//directional lights, compute diffuse color
	diffuse_light += saturate(dot(vWorldN, -vSkyLightDir)) * vSkyLightColor;

	//point lights
	#ifndef USE_LIGHTING_PASS
	diffuse_light += calculate_point_lights_diffuse(vWorldPos, vWorldN, true, false);
	#endif
	
	//apply material color
	//	Out.Color = min(1, vMaterialColor * vColor * diffuse_light);
	Out.Color = vColor * diffuse_light;

	//shadow mapping variables
	float wNdotSun = dot(vWorldN, -vSunDir);
	Out.SunLight =  max(0.2f * (wNdotSun + 0.9f),wNdotSun) * vSunColor * vColor;
	if (PcfMode != PCF_NONE)
	{
		float4 ShadowPos = mul(matSunViewProj, vWorldPos);
		Out.ShadowTexCoord = ShadowPos;
		Out.ShadowTexCoord.z /= ShadowPos.w;
		Out.ShadowTexCoord.w = 1.0f;
		Out.ShadowTexelPos = Out.ShadowTexCoord * fShadowMapSize;
		//shadow mapping variables end
	}
	
	//apply fog
	float d = length(P);

	Out.Fog = get_fog_amount_new(d, vWorldPos.z);
	return Out;
}
PS_OUTPUT ps_hair(VS_OUTPUT_SIMPLE_HAIR In, uniform const int PcfMode)
{
	PS_OUTPUT Output;
	
	float4 tex1_col = tex2D(MeshTextureSampler, In.Tex0);
	float4 tex2_col = tex2D(Diffuse2Sampler, In.Tex0);
	
	float4 final_col;
	
	INPUT_TEX_GAMMA(tex1_col.rgb);
	
	final_col = tex1_col * vMaterialColor;
	
	float alpha = saturate(((2.0f * vMaterialColor2.a ) + tex2_col.a) - 1.9f);
	final_col.rgb *= (1.0f - alpha);
	final_col.rgb += tex2_col.rgb * alpha;
	
	//    tex_col = tex2_col * vMaterialColor2.a + tex1_col * (1.0f - vMaterialColor2.a);
	
	
	float4 total_light = In.Color;
	if ((PcfMode != PCF_NONE))
	{
		float sun_amount = GetSunAmount(PcfMode, In.ShadowTexCoord, In.ShadowTexelPos);
		total_light.rgb += In.SunLight.rgb * sun_amount;
	}
	else
	{
		total_light.rgb += In.SunLight.rgb;
	}
	Output.RGBColor =  final_col * total_light;
	OUTPUT_GAMMA(Output.RGBColor.rgb);
	return Output;
}

DEFINE_TECHNIQUES(hair_shader, vs_hair, ps_hair)


struct VS_INPUT_HAIR
{
	float4 vPosition : POSITION;
	float3 vNormal : NORMAL;
	float3 vTangent : BINORMAL;
	
	float2 tc : TEXCOORD0;
	float4 vColor : COLOR0;
};
struct VS_OUTPUT_HAIR
{
	float4 Pos					: POSITION;
	float2 Tex0					: TEXCOORD0;
	
	float4 VertexLighting		: TEXCOORD1;
	
	float3 viewVec				: TEXCOORD2;
	float3 normal				: TEXCOORD3;
	float3 tangent				: TEXCOORD4;
	float4 VertexColor			: COLOR0;
	
	
	float4 ShadowTexCoord		: TEXCOORD6;
	float2 ShadowTexelPos		: TEXCOORD7;
	float  Fog				    : FOG;
};

VS_OUTPUT_HAIR vs_hair_aniso (uniform const int PcfMode, VS_INPUT_HAIR In)
{
	INITIALIZE_OUTPUT(VS_OUTPUT_HAIR, Out);

	float4 vWorldPosi = (float4)mul(matWorld,In.vPosition);
	float2 Period = float2(25,20);
	float2 Amplitude = float2(0.01,0.008);
	if (In.vPosition.y < 0.08)
	{
	In.vPosition.x = In.vPosition.x + Amplitude.x * sin(Period.x *  In.vPosition.y + 2*time_var); //
	In.vPosition.z = In.vPosition.z + Amplitude.y * sin(Period.y *  In.vPosition.y + 2*time_var); //
	}
	else if (In.vPosition.z > 0.085)
	{
	In.vPosition.x = In.vPosition.x + (Amplitude.y*0.35) * sin(Period.x *  In.vPosition.y + 1.7*time_var); //
	In.vPosition.y = In.vPosition.y + (Amplitude.y*0.2) * sin(Period.y *  In.vPosition.z + 1*time_var); //
	}
	Out.Pos = mul(matWorldViewProj, In.vPosition);

	float4 vWorldPos = (float4)mul(matWorld,In.vPosition);
	float3 vWorldN = normalize(mul((float3x3)matWorld, In.vNormal)); //normal in world space

	float3 P = mul(matWorldView, In.vPosition); //position in view space

	float2 sintc = In.tc + 0.01*float2(sin(Period.x *  In.tc.y + 1.5*time_var),0);
	Out.Tex0 = sintc;

	float4 diffuse_light = vAmbientColor;
	//   diffuse_light.rgb *= gradient_factor * (gradient_offset + vWorldN.z);

	//directional lights, compute diffuse color
	diffuse_light += saturate(dot(vWorldN, -vSkyLightDir)) * vSkyLightColor;

	//point lights
	#ifndef USE_LIGHTING_PASS
	diffuse_light += calculate_point_lights_diffuse(vWorldPos, vWorldN, true, false);
	#endif
	
	//apply material color
	Out.VertexLighting = saturate(In.vColor * diffuse_light);
	
	Out.VertexColor = In.vColor;
	
	if(true) {
		float3 Pview = vCameraPos - vWorldPos;
		Out.normal = normalize( mul( matWorld, In.vNormal ) );
		Out.tangent = normalize( mul( matWorld, In.vTangent ) );
		Out.viewVec = normalize( Pview );
	}
	
	if (PcfMode != PCF_NONE)
	{
		float4 ShadowPos = mul(matSunViewProj, vWorldPos);
		Out.ShadowTexCoord = ShadowPos;
		Out.ShadowTexCoord.z /= ShadowPos.w;
		Out.ShadowTexCoord.w = 1.0f;
		Out.ShadowTexelPos = Out.ShadowTexCoord * fShadowMapSize;
		//shadow mapping variables end
	}
	
	//apply fog
	float d = length(P);

	Out.Fog = get_fog_amount_new(d, vWorldPos.z);
	return Out;
}


VS_OUTPUT_HAIR vs_hair_aniso_static (uniform const int PcfMode, VS_INPUT_HAIR In)
{
	INITIALIZE_OUTPUT(VS_OUTPUT_HAIR, Out);

	float2 Period = float2(25,20);

	Out.Pos = mul(matWorldViewProj, In.vPosition);

	float4 vWorldPos = (float4)mul(matWorld,In.vPosition);
	float3 vWorldN = normalize(mul((float3x3)matWorld, In.vNormal)); //normal in world space

	float3 P = mul(matWorldView, In.vPosition); //position in view space

	float2 sintc = In.tc + 0.01*float2(sin(Period.x *  In.tc.y + 1.5*time_var),0);
	Out.Tex0 = sintc;

	float4 diffuse_light = vAmbientColor;
	//   diffuse_light.rgb *= gradient_factor * (gradient_offset + vWorldN.z);

	//directional lights, compute diffuse color
	diffuse_light += saturate(dot(vWorldN, -vSkyLightDir)) * vSkyLightColor;

	//point lights
	#ifndef USE_LIGHTING_PASS
	diffuse_light += calculate_point_lights_diffuse(vWorldPos, vWorldN, true, false);
	#endif
	
	//apply material color
	Out.VertexLighting = saturate(In.vColor * diffuse_light);
	
	Out.VertexColor = In.vColor;
	
	if(true) {
		float3 Pview = vCameraPos - vWorldPos;
		Out.normal = normalize( mul( matWorld, In.vNormal ) );
		Out.tangent = normalize( mul( matWorld, In.vTangent ) );
		Out.viewVec = normalize( Pview );
	}
	
	if (PcfMode != PCF_NONE)
	{
		float4 ShadowPos = mul(matSunViewProj, vWorldPos);
		Out.ShadowTexCoord = ShadowPos;
		Out.ShadowTexCoord.z /= ShadowPos.w;
		Out.ShadowTexCoord.w = 1.0f;
		Out.ShadowTexelPos = Out.ShadowTexCoord * fShadowMapSize;
		//shadow mapping variables end
	}
	
	//apply fog
	float d = length(P);

	Out.Fog = get_fog_amount_new(d, vWorldPos.z);
	return Out;
}


PS_OUTPUT ps_hair_aniso(VS_OUTPUT_HAIR In, uniform const int PcfMode)
{
	PS_OUTPUT Output;

	//vMaterialColor2.a -> age slider 0..1
	//vMaterialColor -> hair color
	
	float3 lightDir = -vSunDir;
	float3 hairBaseColor = vMaterialColor.rgb;


	// diffuse term
	float3 diffuse = hairBaseColor * vSunColor.rgb * In.VertexColor.rgb * HairDiffuseTerm(In.normal, lightDir);
			

	float4 tex1_col = tex2D(MeshTextureSampler, In.Tex0);
	INPUT_TEX_GAMMA(tex1_col.rgb);
	float4 tex2_col = tex2D(Diffuse2Sampler, In.Tex0);
	float alpha = saturate(((2.0f * vMaterialColor2.a ) + tex2_col.a) - 1.9f);
	
	float4 final_col = tex1_col;
	final_col.rgb *= hairBaseColor;
	final_col.rgb *= (1.0f - alpha);
	final_col.rgb += tex2_col.rgb * alpha;
		
	float sun_amount = 1;
	if ((PcfMode != PCF_NONE))
	{
		 sun_amount = GetSunAmount(PcfMode, In.ShadowTexCoord, In.ShadowTexelPos);
	}
	
	float3 specular = calculate_hair_specular(In.normal, In.tangent, lightDir, In.viewVec, In.Tex0);
	
	float4 total_light = vAmbientColor;
	total_light.rgb += (((diffuse + specular) * sun_amount));
	
	//float4 total_light = vAmbientColor;
	//total_light.rgb += diffuse+ * sun_amount;
	total_light.rgb += In.VertexLighting.rgb;
	
	Output.RGBColor.rgb = total_light * final_col.rgb;
	OUTPUT_GAMMA(Output.RGBColor.rgb);
	
	Output.RGBColor.a = tex1_col.a * vMaterialColor.a;
	
	Output.RGBColor = saturate(Output.RGBColor);	//do not bloom!	
	
	return Output;
}

technique hair_shader_aniso
{
	pass P0
	{
		VertexShader = compile vs_2_0 vs_hair_aniso(PCF_NONE);
		PixelShader = compile PS_2_X ps_hair_aniso(PCF_NONE);
	}
}
technique hair_shader_aniso_SHDW
{
	pass P0
	{
		VertexShader = compile vs_2_0 vs_hair_aniso(PCF_DEFAULT);
		PixelShader = compile PS_2_X ps_hair_aniso(PCF_DEFAULT);
	}
}
technique hair_shader_aniso_SHDWNVIDIA
{
	pass P0
	{
		VertexShader = compile vs_2_a vs_hair_aniso(PCF_NVIDIA);
		PixelShader = compile ps_2_a ps_hair_aniso(PCF_NVIDIA);
	}
}



technique hair_shader_aniso_static
{
	pass P0
	{
		VertexShader = compile vs_2_0 vs_hair_aniso_static(PCF_NONE);
		PixelShader = compile PS_2_X ps_hair_aniso(PCF_NONE);
	}
}
technique hair_shader_aniso_static_SHDW
{
	pass P0
	{
		VertexShader = compile vs_2_0 vs_hair_aniso_static(PCF_DEFAULT);
		PixelShader = compile PS_2_X ps_hair_aniso(PCF_DEFAULT);
	}
}
technique hair_shader_aniso_static_SHDWNVIDIA
{
	pass P0
	{
		VertexShader = compile vs_2_a vs_hair_aniso_static(PCF_NVIDIA);
		PixelShader = compile ps_2_a ps_hair_aniso(PCF_NVIDIA);
	}
}



#endif

/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#ifdef FACE_SHADERS

struct VS_OUTPUT_SIMPLE_FACE
{
	float4 Pos					: POSITION;
	float4 Color					: COLOR0;
	float2 Tex0					: TEXCOORD0;
	float4 SunLight				: TEXCOORD1;
	float4 ShadowTexCoord		: TEXCOORD2;
	float2 ShadowTexelPos		: TEXCOORD3;
	float  Fog				    : FOG;
};
VS_OUTPUT_SIMPLE_FACE vs_face (uniform const int PcfMode, float4 vPosition : POSITION, float3 vNormal : NORMAL, float2 tc : TEXCOORD0, float4 vColor : COLOR0)
{
	INITIALIZE_OUTPUT(VS_OUTPUT_SIMPLE_FACE, Out);

	Out.Pos = mul(matWorldViewProj, vPosition);

	float4 vWorldPos = (float4)mul(matWorld,vPosition);
	float3 vWorldN = normalize(mul((float3x3)matWorld, vNormal)); //normal in world space

	float3 P = mul(matWorldView, vPosition); //position in view space

	Out.Tex0 = tc;

	float4 diffuse_light = vAmbientColor;
	//   diffuse_light.rgb *= gradient_factor * (gradient_offset + vWorldN.z);

	//directional lights, compute diffuse color
	diffuse_light += saturate(dot(vWorldN, -vSkyLightDir)) * vSkyLightColor;

	//point lights
	#ifndef USE_LIGHTING_PASS
	diffuse_light += calculate_point_lights_diffuse(vWorldPos, vWorldN, true, false);
	#endif
	
	//apply material color
	//	Out.Color = min(1, vMaterialColor * vColor * diffuse_light);
	Out.Color = vMaterialColor * vColor * diffuse_light;

	//shadow mapping variables
	float wNdotSun = dot(vWorldN, -vSunDir);
	Out.SunLight =  max(0.2f * (wNdotSun + 0.9f),wNdotSun) * vSunColor * vMaterialColor * vColor;
	if (PcfMode != PCF_NONE)
	{
		float4 ShadowPos = mul(matSunViewProj, vWorldPos);
		Out.ShadowTexCoord = ShadowPos;
		Out.ShadowTexCoord.z /= ShadowPos.w;
		Out.ShadowTexCoord.w = 1.0f;
		Out.ShadowTexelPos = Out.ShadowTexCoord * fShadowMapSize;
		//shadow mapping variables end
	}
	
	//apply fog
	float d = length(P);

	Out.Fog = get_fog_amount_new(d, vWorldPos.z);
	return Out;
}
PS_OUTPUT ps_face(VS_OUTPUT_SIMPLE_FACE In, uniform const int PcfMode)
{
	PS_OUTPUT Output;
	
	float4 tex1_col = tex2D(MeshTextureSampler, In.Tex0);
	float4 tex2_col = tex2D(Diffuse2Sampler, In.Tex0);
	
	float4 tex_col;
	
	tex_col = tex2_col * In.Color.a + tex1_col * (1.0f - In.Color.a);
	
	INPUT_TEX_GAMMA(tex_col.rgb);
	
	if ((PcfMode != PCF_NONE))
	{
		float sun_amount = GetSunAmount(PcfMode, In.ShadowTexCoord, In.ShadowTexelPos);
		//		sun_amount *= sun_amount;
		Output.RGBColor =  tex_col * ((In.Color + In.SunLight * sun_amount));
	}
	else
	{
		Output.RGBColor = tex_col * (In.Color + In.SunLight);
	}
	// gamma correct
	OUTPUT_GAMMA(Output.RGBColor.rgb);
	Output.RGBColor.a = vMaterialColor.a;
	
	return Output;
}

DEFINE_TECHNIQUES(face_shader, vs_face, ps_face)

DEFINE_LIGHTING_TECHNIQUE(face_shader, 0, 0, 0, 0, 0)

////////////////////////////////////////
struct VS_INPUT_FACE
{
	float4 Position 	: POSITION;
	float2 TC 			: TEXCOORD0; 
	
	float4 VertexColor	: COLOR0; 
	
	float3 Normal 		: NORMAL;
	float3 Tangent 		: TANGENT;
	float3 Binormal 	: BINORMAL;
};
struct VS_OUTPUT_FACE
{
	float4 Pos					: POSITION;
	float  Fog				    : FOG;

	float4 VertexColor			: COLOR0;
	float2 Tex0					: TEXCOORD0;

	float3 WorldPos             : TEXCOORD1;
	float3 ViewVec              : TEXCOORD2;
	
	float3 SunLightDir			: TEXCOORD3;
	float4 PointLightDir		: TEXCOORD4;
	
	float4 ShadowTexCoord		: TEXCOORD5;
	float2 ShadowTexelPos		: TEXCOORD6;
#ifdef  INCLUDE_VERTEX_LIGHTING
	float3 VertexLighting		: TEXCOORD7;
#endif
};

VS_OUTPUT_STANDART vs_main_standart_face_mod (uniform const int PcfMode, 
										uniform const bool use_bumpmap, 
										float4 vPosition : POSITION, 
										float3 vNormal : NORMAL, 
										float2 tc : TEXCOORD0,  
										float3 vTangent : TANGENT, 
										float3 vBinormal : BINORMAL, 
										float4 vVertexColor : COLOR0, 
										float4 vBlendWeights : BLENDWEIGHT,
										float4 vBlendIndices : BLENDINDICES)
{
	INITIALIZE_OUTPUT(VS_OUTPUT_STANDART, Out);

	
	float4 vObjectPos;
	float3 vObjectN, vObjectT, vObjectB;
	
	vObjectPos = vPosition;
	
	vObjectN = vNormal;
	if(use_bumpmap) {
		vObjectT = vTangent;
		vObjectB = vBinormal;
	}
		
	float4 vWorldPos = mul(matWorld, vObjectPos);
	Out.Pos = mul(matWorldViewProj, vPosition);
	Out.Tex0 = tc;

	
	float3 vWorldN = normalize(mul((float3x3)matWorld, vObjectN));
	
	float3x3 TBNMatrix;
	if(use_bumpmap) {
		float3 vWorld_binormal = normalize(mul((float3x3)matWorld, vObjectB));
		float3 vWorld_tangent  = normalize(mul((float3x3)matWorld, vObjectT));
		TBNMatrix = float3x3(vWorld_tangent, vWorld_binormal, vWorldN); 
	}
	

	if (PcfMode != PCF_NONE)
	{
		float4 ShadowPos = mul(matSunViewProj, vWorldPos);
		Out.ShadowTexCoord = ShadowPos;
		Out.ShadowTexCoord.z /= ShadowPos.w;
		Out.ShadowTexCoord.w = 1.0f;
		Out.ShadowTexelPos = Out.ShadowTexCoord * fShadowMapSize;
	}

	if(use_bumpmap) {
		Out.SunLightDir = normalize(mul(TBNMatrix, -vSunDir));
		Out.SkyLightDir = mul(TBNMatrix, -vSkyLightDir);
	} else {
		Out.SunLightDir = vWorldN;
	}
	Out.VertexColor = vVertexColor;
	
	
	//point lights
	#ifdef INCLUDE_VERTEX_LIGHTING
	Out.VertexLighting = calculate_point_lights_diffuse(vWorldPos, vWorldN, true, true);
	#endif
	
	
	#ifndef USE_LIGHTING_PASS 
	const int effective_light_index = iLightIndices[0];
	float3 point_to_light = vLightPosDir[effective_light_index]-vWorldPos.xyz;
	float LD = dot(point_to_light, point_to_light);
	Out.PointLightDir.a = saturate(1.0f/LD);	//prevent bloom for 1 meters
	
	if(use_bumpmap) {
		Out.PointLightDir.xyz = mul(TBNMatrix, normalize(point_to_light));
	} else {
		Out.PointLightDir.xyz = normalize(point_to_light);
	}
	#endif
	
	
	if(use_bumpmap) {
		Out.ViewDir =  mul(TBNMatrix, normalize(vCameraPos.xyz - vWorldPos.xyz));
	}
	else {
		Out.ViewDir =  normalize(vCameraPos.xyz - vWorldPos.xyz);
	}
	
	float3 P = mul(matWorldView, vObjectPos); //position in view space
	
	//apply fog
	float d = length(P);
	Out.Fog = get_fog_amount_new(d, vWorldPos.z);

	return Out;
}

PS_OUTPUT ps_main_standart_face_mod( VS_OUTPUT_STANDART In, uniform const int PcfMode, 
										uniform const bool use_bumpmap, uniform const bool use_ps2a )
{ 
	PS_OUTPUT Output;

	float4 total_light = vAmbientColor;//In.LightAmbient;

	float3 normal;
	
	if(use_bumpmap)
	{
		float3 tex1_norm, tex2_norm;
		tex1_norm = tex2D(NormalTextureSampler, In.Tex0);
		
		if(use_ps2a) {//add old's normal map with ps2a 
			tex2_norm = tex2D(SpecularTextureSampler, In.Tex0);
			normal = lerp(tex1_norm, tex2_norm, In.VertexColor.a);	// blend normals different?
			normal = 2.0f * normal - 1.0f;		
			normal = normalize(normal);
		}
		else {
			normal = (2 * tex1_norm - 1);
		}
	}
	else {
		normal = In.SunLightDir.xyz;
	}
	
	float sun_amount = 1;
	if (PcfMode != PCF_NONE)
	{
		sun_amount = GetSunAmount(PcfMode, In.ShadowTexCoord, In.ShadowTexelPos);
	}
	
	if(use_bumpmap)
	{
		total_light += face_NdotL(In.SunLightDir.xyz, normal.xyz) * sun_amount * vSunColor;
		if(use_ps2a) {
			total_light += face_NdotL(In.SkyLightDir.xyz, normal.xyz) * vSkyLightColor;
		}
	}
	else 
	{
		total_light += face_NdotL(-vSunDir, normal.xyz) * sun_amount * vSunColor;
		if(use_ps2a) {
			total_light += face_NdotL(-vSkyLightDir, normal.xyz) * vSkyLightColor;
		}
	}

	float3 point_lighting = 0;
	#ifndef USE_LIGHTING_PASS 
		float light_atten = In.PointLightDir.a * 0.9f;
		const int effective_light_index = iLightIndices[0];
		point_lighting += light_atten * face_NdotL(In.PointLightDir.xyz, normal.xyz) * vLightDiffuse[effective_light_index];
	#endif
	
	#ifdef INCLUDE_VERTEX_LIGHTING
		if(use_ps2a) { point_lighting += In.VertexLighting; }
	#endif
	total_light.rgb += point_lighting;

	
	float fresnel = 1-(saturate(dot(normal,In.ViewDir)));
	fresnel = fresnel + (0.55*pow(fresnel,4));

	float lightintensity = dot(total_light.rgb, float3(0.3, 0.59, 0.11));
	lightintensity = max(lightintensity,0.10);
	lightintensity = min(lightintensity,0.75);
	fresnel = fresnel*lightintensity;
	
	float3 skinlight =  float3(0.73,0.2,0.13);
	float3 greyskinlight = dot(skinlight.rgb, float3(0.3, 0.59, 0.11));
	skinlight = lerp(greyskinlight,skinlight,0.75);
	skinlight = skinlight *fresnel;
	total_light.rgb += max(0,skinlight);
	
	
	if (PcfMode != PCF_NONE)
		Output.RGBColor.rgb = total_light.rgb;
	else
		Output.RGBColor.rgb = min(total_light.rgb, 2.0f);
		
	// Output.RGBColor.rgb = total_light.rgb;
	
	
	
	
	
	
	
	float4 tex1_col = tex2D(MeshTextureSampler, In.Tex0);
	float4 tex2_col = tex2D(Diffuse2Sampler, In.Tex0);
	float4 tex_col = lerp(tex1_col, tex2_col, In.VertexColor.a);
	
	INPUT_TEX_GAMMA(tex_col.rgb);
	
	Output.RGBColor *= tex_col;
	Output.RGBColor.rgb *= (In.VertexColor.rgb * vMaterialColor.rgb);
	
	if(use_ps2a) {
		float fSpecular = 0;
		
		float4 specColor =  vSpecularColor * vSunColor;	//float4(1.0, 0.9, 0.8, 1.0) * 2;//
		if(false) {	//we dont have specularmap yet-> used for normalmap2
			specColor *= tex2D(SpecularTextureSampler, In.Tex0);
		}
		
		float3 vHalf = normalize( In.ViewDir + In.SunLightDir );
		fSpecular = specColor * pow( saturate(dot(vHalf, normal)), fMaterialPower) * sun_amount; 
		
		float fresnel = saturate(1.0f - dot(In.ViewDir, normal));
		Output.RGBColor += fresnel * fSpecular;
	}
	

	//Output.RGBColor.rgb = Output.RGBColor.rgb*(1.5*skinlight);
	
	//Output.RGBColor = saturate(Output.RGBColor);
	Output.RGBColor.rgb = saturate( OUTPUT_GAMMA(Output.RGBColor.rgb) );	//do not bloom!
	Output.RGBColor.a = vMaterialColor.a;
	////
	//Output.RGBColor = face_NdotL(In.PointLightDir.xyz, normal.xyz) * vLightDiffuse[effective_light_index] * In.PointLightDir.a;
	//Output.RGBColor.rgb += In.VertexLighting;
	//Output.RGBColor.a = 1;

	

	
	return Output;
}

////////////////////
technique face_shader_high
{
	pass P0
	{
		VertexShader = compile vs_2_0 vs_main_standart_face_mod(PCF_NONE, true);
		PixelShader = compile PS_2_X ps_main_standart_face_mod(PCF_NONE, true, false);
	}
}
technique face_shader_high_SHDW
{
	pass P0
	{
		VertexShader = compile vs_2_0 vs_main_standart_face_mod(PCF_DEFAULT, true);
		PixelShader = compile PS_2_X ps_main_standart_face_mod(PCF_DEFAULT, true, false);

	}
}
technique face_shader_high_SHDWNVIDIA
{
	pass P0
	{
		VertexShader = compile vs_2_a vs_main_standart_face_mod(PCF_NVIDIA, true);
		PixelShader = compile PS_2_X ps_main_standart_face_mod(PCF_NVIDIA, true, false);
	}
}

DEFINE_LIGHTING_TECHNIQUE(face_shader_high, 0, 1, 0, 0, 0)	

////////////////////
technique faceshader_high_specular
{
	pass P0
	{
		VertexShader = compile vs_2_0 vs_main_standart_face_mod(PCF_NONE, true);
		PixelShader = compile PS_2_X ps_main_standart_face_mod(PCF_NONE, true, true);
	}
}
technique faceshader_high_specular_SHDW
{
	pass P0
	{
		VertexShader = compile vs_2_0 vs_main_standart_face_mod(PCF_DEFAULT, true);
		PixelShader = compile PS_2_X ps_main_standart_face_mod(PCF_DEFAULT, true, true);

	}
}
technique faceshader_high_specular_SHDWNVIDIA
{
	pass P0
	{
		VertexShader = compile vs_2_a vs_main_standart_face_mod(PCF_NVIDIA, true);
		PixelShader = compile PS_2_X ps_main_standart_face_mod(PCF_NVIDIA, true, true);
	}
}

DEFINE_LIGHTING_TECHNIQUE(faceshader_high_specular, 0, 1, 0, 0, 0)	


////////////////////
technique faceshader_simple
{
	pass P0
	{
		VertexShader = compile vs_2_0 vs_main_standart_face_mod(PCF_NONE, false);
		PixelShader = compile PS_2_X ps_main_standart_face_mod(PCF_NONE, false, false);
	}
}
technique faceshader_simple_SHDW
{
	pass P0
	{
		VertexShader = compile vs_2_0 vs_main_standart_face_mod(PCF_DEFAULT, false);
		PixelShader = compile PS_2_X ps_main_standart_face_mod(PCF_DEFAULT, false, false);

	}
}
technique faceshader_simple_SHDWNVIDIA
{
	pass P0
	{
		VertexShader = compile vs_2_a vs_main_standart_face_mod(PCF_NVIDIA, false);
		PixelShader = compile PS_2_X ps_main_standart_face_mod(PCF_NVIDIA, false, false);
	}
}

DEFINE_LIGHTING_TECHNIQUE(faceshader_high_specular, 0, 1, 0, 0, 0)	

////////////////////////////////////////
VS_OUTPUT vs_main_skin (float4 vPosition : POSITION, float3 vNormal : NORMAL, float2 tc : TEXCOORD0, float4 vColor : COLOR, float4 vBlendWeights : BLENDWEIGHT, float4 vBlendIndices : BLENDINDICES, uniform const int PcfMode)
{
	INITIALIZE_OUTPUT(VS_OUTPUT, Out);

	float4 vObjectPos = skinning_deform(vPosition, vBlendWeights, vBlendIndices);
	
	float3 vObjectN = normalize(  mul((float3x3)matWorldArray[vBlendIndices.x], vNormal) * vBlendWeights.x
								+ mul((float3x3)matWorldArray[vBlendIndices.y], vNormal) * vBlendWeights.y
								+ mul((float3x3)matWorldArray[vBlendIndices.z], vNormal) * vBlendWeights.z
								+ mul((float3x3)matWorldArray[vBlendIndices.w], vNormal) * vBlendWeights.w);

	float4 vWorldPos = mul(matWorld,vObjectPos);
	Out.Pos = mul(matWorldViewProj, vObjectPos);
	float3 vWorldN = normalize(mul((float3x3)matWorld, vObjectN)); //normal in world space

	float3 P = mul(matView, vWorldPos); //position in view space

	Out.Tex0 = tc;

	//light computation
	Out.Color = vAmbientColor;
	//   Out.Color.rgb *= gradient_factor * (gradient_offset + vWorldN.z);

	//directional lights, compute diffuse color
	Out.Color += saturate(dot(vWorldN, -vSkyLightDir)) * vSkyLightColor;

	//point lights
	#ifndef USE_LIGHTING_PASS
	Out.Color += calculate_point_lights_diffuse(vWorldPos, vWorldN, false, false);
	#endif

	//apply material color
	Out.Color *= vMaterialColor * vColor;
	Out.Color = min(1, Out.Color);

	//shadow mapping variables
	float wNdotSun = saturate(dot(vWorldN, -vSunDir));
	Out.SunLight = wNdotSun * vSunColor * vMaterialColor * vColor;
	if (PcfMode != PCF_NONE)
	{
		float4 ShadowPos = mul(matSunViewProj, vWorldPos);
		Out.ShadowTexCoord = ShadowPos;
		Out.ShadowTexCoord.z /= ShadowPos.w;
		Out.ShadowTexCoord.w = 1.0f;
		Out.ShadowTexelPos = Out.ShadowTexCoord * fShadowMapSize;
		//shadow mapping variables end
	}

	//apply fog
	float d = length(P);
	Out.Fog = get_fog_amount_new(d, vWorldPos.z);

	return Out;
}

technique skin_diffuse
{
	pass P0
	{
		VertexShader = compile vs_2_0 vs_main_skin(PCF_NONE);
		PixelShader = ps_main_compiled_PCF_NONE;
	}
}
technique skin_diffuse_SHDW
{
	pass P0
	{
		VertexShader = compile vs_2_0 vs_main_skin(PCF_DEFAULT);
		PixelShader = ps_main_compiled_PCF_DEFAULT;
	}
}
technique skin_diffuse_SHDWNVIDIA
{
	pass P0
	{
		VertexShader = compile vs_2_a vs_main_skin(PCF_NVIDIA);
		PixelShader = ps_main_compiled_PCF_NVIDIA;
	}
}

DEFINE_LIGHTING_TECHNIQUE(skin_diffuse, 0, 0, 1, 0, 0)	


#endif

/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#ifdef FLORA_SHADERS

struct VS_OUTPUT_FLORA
{
	float4 Pos					: POSITION;
	float  Fog				    : FOG;
	
	float4 Color				: COLOR0;
	float2 Tex0					: TEXCOORD0;
	float4 SunLight				: TEXCOORD1;
	float4 ShadowTexCoord		: TEXCOORD2;
	float2 ShadowTexelPos		: TEXCOORD3;
};

struct VS_OUTPUT_FLORA_NO_SHADOW
{
	float4 Pos					: POSITION;
	float4 Color					: COLOR0;
	float2 Tex0					: TEXCOORD0;
	float  Fog				    : FOG;
};

VS_OUTPUT_FLORA vs_flora(uniform const int PcfMode, float4 vPosition : POSITION, float4 vColor : COLOR0, float2 tc : TEXCOORD0)
{
	INITIALIZE_OUTPUT(VS_OUTPUT_FLORA, Out);

	float4 vPositionAltered = float4(vPosition.xyz,vPosition.z-0.1);
	float4 ShadowedPos = (float4)mul(matWorld,vPositionAltered);
	
	
	float windAmount = 0;
    windAmount*=windAmount; 
    float2 treePos = //float2 (matWorld._m03, matWorld._m13) + 
                    vPosition.xy;
    float t2 = time_var + dot( treePos , float2(6.5,4.5)) ;
    float windPhase = sin(t2*3.9)*cos(t2*2.3);
    vPosition.xy += float2(0.018,0.018) // *(vPosition.z+50.0)
				    *windPhase*(windAmount+0.2)
                   *(ShadowedPos.z*0.1); // distance from ground stored in alpha channes with openbrf easteregg! ;)
 	vPosition.z += 0.02 * sin(0.1* vPosition.y + 0.7 * time_var); // NO.1= HEIGHT OF WAVE       NO.2= NUMBER OF WAVES    NO.3= SPEED OF WAVES
	
	Out.Pos = mul(matWorldViewProj, vPosition);
	float4 vWorldPos = (float4)mul(matWorld,vPosition);


	Out.Tex0 = tc;
	//   Out.Color = vColor * vMaterialColor;
	Out.Color = vColor * (vAmbientColor + vSunColor * 0.06f); //add some sun color to simulate sun passing through leaves.
	Out.Color.a *= vMaterialColor.a;

	//   Out.Color = vColor * vMaterialColor * (vAmbientColor + vSunColor * 0.15f);
	//shadow mapping variables
	Out.SunLight = (vSunColor * 0.34f)* vMaterialColor * vColor;

	if (PcfMode != PCF_NONE)
	{
		float4 ShadowPos = mul(matSunViewProj, vWorldPos);
		Out.ShadowTexCoord = ShadowPos;
		Out.ShadowTexCoord.z /= ShadowPos.w;
		Out.ShadowTexCoord.w = 1.0f;
		Out.ShadowTexelPos = Out.ShadowTexCoord * fShadowMapSize;
	}
	//shadow mapping variables end
	
	//apply fog
	float3 P = mul(matWorldView, vPosition); //position in view space
	float d = length(P);
	Out.Fog = get_fog_amount_new(d, vWorldPos.z);

	return Out;
}


VS_OUTPUT_FLORA vs_flora_Instanced(uniform const int PcfMode, float4 vPosition : POSITION, float4 vColor : COLOR0, float2 tc : TEXCOORD0,
								   //instance data:
								   float3   vInstanceData0 : TEXCOORD1,
								   float3   vInstanceData1 : TEXCOORD2,
								   float3   vInstanceData2 : TEXCOORD3,
								   float3   vInstanceData3 : TEXCOORD4)
{
	INITIALIZE_OUTPUT(VS_OUTPUT_FLORA, Out);
	

	
	
	float4x4 matWorldOfInstance = build_instance_frame_matrix(vInstanceData0, vInstanceData1, vInstanceData2, vInstanceData3);

	float4 vWorldPos = (float4)mul(matWorldOfInstance,vPosition);
	Out.Pos = mul(matViewProj, vWorldPos);

	Out.Tex0 = tc;
	//   Out.Color = vColor * vMaterialColor;
	Out.Color = vColor * (vAmbientColor + vSunColor * 0.06f); //add some sun color to simulate sun passing through leaves.
	Out.Color.a *= vMaterialColor.a;

	//   Out.Color = vColor * vMaterialColor * (vAmbientColor + vSunColor * 0.15f);
	//shadow mapping variables
	Out.SunLight = (vSunColor * 0.34f)* vMaterialColor * vColor;

	if (PcfMode != PCF_NONE)
	{
		float4 ShadowPos = mul(matSunViewProj, vWorldPos);
		Out.ShadowTexCoord = ShadowPos;
		Out.ShadowTexCoord.z /= ShadowPos.w;
		Out.ShadowTexCoord.w = 1.0f;
		Out.ShadowTexelPos = Out.ShadowTexCoord * fShadowMapSize;
	}
	//shadow mapping variables end
	
	//apply fog
	float3 P = mul(matView, vWorldPos); //position in view space
	float d = length(P);
	Out.Fog = get_fog_amount_new(d, vWorldPos.z);

	return Out;
}

PS_OUTPUT ps_flora(VS_OUTPUT_FLORA In, uniform const int PcfMode) 
{ 
	PS_OUTPUT Output;
	float4 tex_col = tex2D(MeshTextureSampler, In.Tex0);
	clip(tex_col.a - 0.05f);
	
	INPUT_TEX_GAMMA(tex_col.rgb);


	if (PcfMode != PCF_NONE)
	{
		float sun_amount = GetSunAmount(PcfMode, In.ShadowTexCoord, In.ShadowTexelPos);
		Output.RGBColor =  tex_col * ((In.Color + In.SunLight * sun_amount));
	}
	else
	{
		Output.RGBColor =  tex_col * ((In.Color + In.SunLight));
	}

	//Output.RGBColor = tex_col * In.Color;
	OUTPUT_GAMMA(Output.RGBColor.rgb);
	
	return Output;
}

VS_OUTPUT_FLORA_NO_SHADOW vs_flora_no_shadow(float4 vPosition : POSITION, float4 vColor : COLOR0, float2 tc : TEXCOORD0)
{
	INITIALIZE_OUTPUT(VS_OUTPUT_FLORA_NO_SHADOW, Out);
    float windAmount = 0;
    windAmount*=windAmount; 
    float2 treePos = vPosition.xy;
    float t2 = time_var + dot( treePos , float2(6.5,4.5)) ;
    float windPhase = sin(t2*3.9)*cos(t2*2.3);
    vPosition.xy += float2(0.018,0.018) // *(vPosition.z+50.0)
				    *windPhase*(windAmount+0.2)
                   *vColor.w; // distance from ground stored in alpha channes with openbrf easteregg! ;)

	
	Out.Pos = mul(matWorldViewProj, vPosition);
	float4 vWorldPos = (float4)mul(matWorld,vPosition);

	float3 P = mul(matWorldView, vPosition); //position in view space

	Out.Tex0 = tc;
	Out.Color = vColor * vMaterialColor;

	//apply fog
	float d = length(P);
	Out.Fog = get_fog_amount_new(d, vWorldPos.z);

	return Out;
}

PS_OUTPUT ps_flora_no_shadow(VS_OUTPUT_FLORA_NO_SHADOW In) 
{ 
	PS_OUTPUT Output;
	float4 tex_col = tex2D(MeshTextureSampler, In.Tex0);
	clip(tex_col.a - 0.05f);
	
	INPUT_TEX_GAMMA(tex_col.rgb);

	Output.RGBColor = tex_col * In.Color;
	OUTPUT_GAMMA(Output.RGBColor.rgb);
	
	return Output;
}





	
	
	

	
//////////
VS_OUTPUT_FLORA vs_grass(uniform const int PcfMode, float4 vPosition : POSITION, float4 vColor : COLOR0, float2 tc : TEXCOORD0)
{
	INITIALIZE_OUTPUT(VS_OUTPUT_FLORA, Out);

	
	float4 WorldPosit = (float4)mul(matWorld,vPosition);
	float timer_variable = tree_rate * time_var;
	float WindFactor = 0.333 * GetWindAmountNew(1.0f, vPosition.z); //range of 0 to 3
	
	
	float texcordY = 1-tc.y;
	if ((tc.y < 0.15)||((tc.y > 0.165) && (tc.y < 0.320))||((tc.x > 0.500) && (tc.y > 0.330) && (tc.y < 0.640)))
	{
	float2 WorldPosition = float2(WorldPosit.z,WorldPosit.y);//float2((matWorldViewProj,vPosition.x),(matWorldViewProj,vPosition.y));
	float2 OriginalPosition = float2(vPosition.x,vPosition.y);
	vPosition.x = vPosition.x + (WindFactor*(TreeAmplitude.x*0.35)) * sin(TreePeriod.x *  WorldPosition.x + (timer_variable)); //
	vPosition.x = vPosition.x + (WindFactor*(TreeAmplitude.x*0.35)) * sin((TreePeriod.x * 30.5) * WorldPosition.x + ((0.2*timer_variable))); //
	vPosition.y = vPosition.y + (WindFactor*(TreeAmplitude.x*0.35)) * sin((TreePeriod.x * 30.76) * WorldPosition.x + ((1.1*timer_variable))); //
	vPosition.z -= 0.1*sqrt(pow((OriginalPosition.x-vPosition.x),2));
	}
	else //vert is a bottom vert
	{
	//vPosition.z += 0.10;
	}
	
	
	float4 vWorldPos = (float4)mul(matWorld,vPosition);

	Out.Pos = mul(matWorldViewProj, vPosition);
	
	float3 P = mul(matWorldView, vPosition); //position in view space

	//leaf shimmering waving - should be fastish(by altering time vra below (perhaps use the stuff from windyflora
    float2 coords = float2(tc.x,tc.y);
	float moveamount = sin(time_var + dot(vPosition.xy , float2(6.5,4.5))) * GetSeasonWindFactor();	//! GetSeasonWindFactor
    coords.x +=  0.015*moveamount;
	
	coords.x = lerp(coords.x, tc.x, saturate(tc.y*tc.y+0.1f));	//!

	Out.Tex0 = coords;
	Out.Color = vColor * vAmbientColor;

	//shadow mapping variables
	if (PcfMode != PCF_NONE)
	{
		Out.SunLight = (vSunColor * 0.55f) * vMaterialColor * vColor;
		float4 ShadowPos = mul(matSunViewProj, vWorldPos);
		Out.ShadowTexCoord = ShadowPos;
		Out.ShadowTexCoord.z /= ShadowPos.w;
		Out.ShadowTexCoord.w = 1.0f;
		Out.ShadowTexelPos = Out.ShadowTexCoord * fShadowMapSize;
	}
	else
	{
		Out.SunLight = vSunColor * 0.5f * vColor;
	}
	//shadow mapping variables end
	//apply fog
	float d = length(P);
	Out.Fog = get_fog_amount_new(d, vWorldPos.z);

	Out.Color.a = min(1.0f,(1.0f - (d / 50.0f)) * 2.0f);

	return Out;
}

PS_OUTPUT ps_grass(VS_OUTPUT_FLORA In, uniform const int PcfMode) 
{ 
	PS_OUTPUT Output;
	float4 tex_col = tex2D(GrassTextureSampler, In.Tex0);
		float season = GetSeason();
	if (season < 0.5) //0= spring
	{
	tex_col = tex2D(MeshTextureSampler, In.Tex0);
	}
	else if ((season > 0.5)&&(season < 1.5)) //1= summer
	{
	tex_col = tex2D(Diffuse2Sampler, In.Tex0);
	}
	else if ((season > 1.5)&&(season < 2.5)) //2= autumn
	{
	tex_col = tex2D(NormalTextureSampler, In.Tex0);
	}
	else if ((season > 2.5)) //3= winter
	{
	tex_col = tex2D(SpecularTextureSampler, In.Tex0);
	}
	//    clip(tex_col.a - 0.05f);
	clip(tex_col.a - 0.1f);
	
	INPUT_TEX_GAMMA(tex_col.rgb);

	if ((PcfMode != PCF_NONE))
	{
		float sun_amount = GetSunAmount(PcfMode, In.ShadowTexCoord, In.ShadowTexelPos);
		Output.RGBColor =  tex_col * ((In.Color + In.SunLight * sun_amount));
	}
	else
	{
		Output.RGBColor =  tex_col * ((In.Color + In.SunLight));
	}

	//    	Output.RGBColor = tex_col * (In.Color + In.SunLight);
	//	Output.RGBColor = tex_col * In.Color;
	OUTPUT_GAMMA(Output.RGBColor.rgb);
	
	return Output;
}

VS_OUTPUT_FLORA_NO_SHADOW vs_grass_no_shadow(float4 vPosition : POSITION, float4 vColor : COLOR0, float2 tc : TEXCOORD0)
{
	INITIALIZE_OUTPUT(VS_OUTPUT_FLORA_NO_SHADOW, Out);

	
	
	
	Out.Pos = mul(matWorldViewProj, vPosition);
	float4 vWorldPos = (float4)mul(matWorld,vPosition);

	float3 P = mul(matWorldView, vPosition); //position in view space

	Out.Tex0 = tc;
	Out.Color = vColor * vMaterialColor;

	//apply fog
	float d = length(P);
	Out.Fog = get_fog_amount_new(d, vWorldPos.z);

	Out.Color.a = min(1.0f,(1.0f - (d / 50.0f)) * 2.0f);

	return Out;
}

PS_OUTPUT ps_grass_no_shadow(VS_OUTPUT_FLORA_NO_SHADOW In) 
{ 
	PS_OUTPUT Output;
	float4 tex_col = tex2D(MeshTextureSampler, In.Tex0);
			float season = GetSeason();
	if (season < 0.5) //0= spring
	{
	tex_col = tex2D(MeshTextureSampler, In.Tex0);
	}
	else if ((season > 0.5)&&(season < 1.5)) //1= summer
	{
	tex_col = tex2D(Diffuse2Sampler, In.Tex0);
	}
	else if ((season > 1.5)&&(season < 2.5)) //2= autumn
	{
	tex_col = tex2D(NormalTextureSampler, In.Tex0);
	}
	else if ((season > 2.5)) //3= winter
	{
	tex_col = tex2D(SpecularTextureSampler, In.Tex0);
	}
	clip(tex_col.a - 0.1f);
	
	INPUT_TEX_GAMMA(tex_col.rgb);

	Output.RGBColor = tex_col * In.Color;
	OUTPUT_GAMMA(Output.RGBColor.rgb);
	return Output;
}

DEFINE_TECHNIQUES(flora, vs_flora, ps_flora)

technique flora_PRESHADED
{
	pass P0
	{
		VertexShader = compile vs_2_0 vs_flora_no_shadow();
		PixelShader = compile ps_2_0 ps_flora_no_shadow();
	}
}
DEFINE_LIGHTING_TECHNIQUE(flora, 0, 0, 0, 0, 0)


///NEW FLORA SESON SHADER
/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

struct VS_OUTPUT_FLORA_SEASON
{
	float4 Pos					: POSITION;
	float  Fog				    : FOG;
	
	float4 Color				: COLOR0;
	float2 Tex0					: TEXCOORD0;
	float4 SunLight				: TEXCOORD1;
	float4 ShadowTexCoord		: TEXCOORD2;
	float2 ShadowTexelPos		: TEXCOORD3;
};

struct VS_OUTPUT_FLORA_SEASON_NO_SHADOW
{
	float4 Pos					: POSITION;
	float4 Color					: COLOR0;
	float2 Tex0					: TEXCOORD0;
	float  Fog				    : FOG;
};

VS_OUTPUT_FLORA_SEASON vs_flora_season(uniform const int PcfMode, float4 vPosition : POSITION, float4 vColor : COLOR0, float2 tc : TEXCOORD0)
{
	INITIALIZE_OUTPUT(VS_OUTPUT_FLORA_SEASON, Out);

	
	float4 WorldPosit = (float4)mul(matWorld,vPosition);
	float WindFactor = 0.333 * GetWindAmountNew(1.0f, vPosition.z); //range of 0 to 3
	
	
	float2 WorldPosition = float2(WorldPosit.z,WorldPosit.y);//float2((matWorldViewProj,vPosition.x),(matWorldViewProj,vPosition.y));
	float timer_variable = tree_rate * time_var;
	float2 OriginalPosition = float2(vPosition.x,vPosition.y);
	vPosition.x = vPosition.x + (WindFactor*(TreeAmplitude.x*0.5)) * sin(TreePeriod.x *  WorldPosition.x + (timer_variable)); //
	vPosition.x = vPosition.x + (WindFactor*(TreeAmplitude.x*0.5)) * sin((TreePeriod.x * 0.5) * WorldPosition.x + ((0.2*timer_variable))); //
	vPosition.y = vPosition.y + (WindFactor*(TreeAmplitude.x*0.5)) * sin((TreePeriod.x * 0.76) * WorldPosition.x + ((1.1*timer_variable))); //
	
	
	vPosition.z -= 0.3*sqrt(pow((OriginalPosition.x-vPosition.x),2));

	
	Out.Pos = mul(matWorldViewProj, vPosition);
	float4 vWorldPos = (float4)mul(matWorld,vPosition);

	//leaf shimmering waving - should be fastish(by altering time vra below (perhaps use the stuff from windyflora
    float2 coords = float2(tc.x,tc.y);
	coords.x = tc.x + ((WindFactor*1.5*(0.033* (1-tc.y))) * sin(5 * (1-tc.y) + 1.75*timer_variable)); //
	coords.x = coords.x + ((WindFactor*1.5*(0.10* (1-tc.y))) * sin(5 * (1-tc.y) + 0.25*timer_variable)); //
	float moveamount = sin(time_var + dot(vPosition.xy , float2(6.5,4.5))) * GetSeasonWindFactor();	//! GetSeasonWindFactor
    coords.x +=  0.015*moveamount;
	
	coords.x = lerp(coords.x, tc.x, saturate(tc.y*tc.y+0.1f));	//!
	
	Out.Tex0 = coords;
	//   Out.Color = vColor * vMaterialColor;
	Out.Color = vColor * (vAmbientColor + vSunColor * 0.06f); //add some sun color to simulate sun passing through leaves.
	Out.Color.a *= vMaterialColor.a;

	//   Out.Color = vColor * vMaterialColor * (vAmbientColor + vSunColor * 0.15f);
	//shadow mapping variables
	Out.SunLight = (vSunColor * 0.34f)* vMaterialColor * vColor;

	if (PcfMode != PCF_NONE)
	{
		float4 ShadowPos = mul(matSunViewProj, vWorldPos);
		Out.ShadowTexCoord = ShadowPos;
		Out.ShadowTexCoord.z /= ShadowPos.w;
		Out.ShadowTexCoord.w = 1.0f;
		Out.ShadowTexelPos = Out.ShadowTexCoord * fShadowMapSize;
	}
	//shadow mapping variables end
	
	//apply fog
	float3 P = mul(matWorldView, vPosition); //position in view space
	float d = length(P);
	Out.Fog = get_fog_amount_new(d, vWorldPos.z);

	return Out;
}



PS_OUTPUT ps_flora_season(VS_OUTPUT_FLORA_SEASON In, uniform const int PcfMode) 
{ 
	PS_OUTPUT Output;
	
	float4 tex_col = tex2D(MeshTextureSampler, In.Tex0);
	float season = GetSeason();
	
	if (season < 0.5) //0= spring
	{
	tex_col = tex2D(MeshTextureSampler, In.Tex0);
	}
	else if ((season > 0.5)&&(season < 1.5)) //1= summer
	{
	tex_col = tex2D(Diffuse2Sampler, In.Tex0);
	}
	else if ((season > 1.5)&&(season < 2.5)) //2= autumn
	{
	tex_col = tex2D(NormalTextureSampler, In.Tex0);
	}
	else if ((season > 2.5)) //3= winter
	{
	tex_col = tex2D(SpecularTextureSampler, In.Tex0);
	}
	
	clip(tex_col.a - 0.05f);
	
	INPUT_TEX_GAMMA(tex_col.rgb);


	if (PcfMode != PCF_NONE)
	{
		float sun_amount = GetSunAmount(PcfMode, In.ShadowTexCoord, In.ShadowTexelPos);
		Output.RGBColor =  tex_col * ((In.Color + In.SunLight * sun_amount));
	}
	else
	{
		Output.RGBColor =  tex_col * ((In.Color + In.SunLight));
	}

	//Output.RGBColor = tex_col * In.Color;
	OUTPUT_GAMMA(Output.RGBColor.rgb);
	
	return Output;
}

VS_OUTPUT_FLORA_SEASON_NO_SHADOW vs_flora_season_no_shadow(float4 vPosition : POSITION, float4 vColor : COLOR0, float2 tc : TEXCOORD0)
{
	INITIALIZE_OUTPUT(VS_OUTPUT_FLORA_SEASON_NO_SHADOW, Out);
	
	
	float4 WorldPosit = (float4)mul(matWorld,vPosition);
	float WindFactor = 0.333 * GetWindAmountNew(1.0f, vPosition.z); //range of 0 to 3
	
	
	float2 WorldPosition = float2(WorldPosit.z,WorldPosit.y);//float2((matWorldViewProj,vPosition.x),(matWorldViewProj,vPosition.y));
	float timer_variable = tree_rate * time_var;
	float2 OriginalPosition = float2(vPosition.x,vPosition.y);
	vPosition.x = vPosition.x + (WindFactor*(TreeAmplitude.x*0.5)) * sin(TreePeriod.x *  WorldPosition.x + (timer_variable)); //
	vPosition.x = vPosition.x + (WindFactor*(TreeAmplitude.x*0.5)) * sin((TreePeriod.x * 0.5) * WorldPosition.x + ((0.2*timer_variable))); //
	vPosition.y = vPosition.y + (WindFactor*(TreeAmplitude.x*0.5)) * sin((TreePeriod.x * 0.76) * WorldPosition.x + ((1.1*timer_variable))); //
	
	
	vPosition.z -= 0.3*sqrt(pow((OriginalPosition.x-vPosition.x),2));

	
	Out.Pos = mul(matWorldViewProj, vPosition);
	float4 vWorldPos = (float4)mul(matWorld,vPosition);

	//leaf shimmering waving - should be fastish(by altering time vra below (perhaps use the stuff from windyflora
    float2 coords = float2(tc.x,tc.y);
	coords.x = tc.x + ((0.033* (1-tc.y)) * sin(5 * (1-tc.y) + 1.75*timer_variable)); //
	coords.x = coords.x + ((0.10* (1-tc.y)) * sin(5 * (1-tc.y) + 0.25*timer_variable)); //
	
	Out.Tex0 = coords;
	
	float3 P = mul(matWorldView, vPosition); //position in view space

	Out.Color = vColor * vMaterialColor;

	//apply fog
	float d = length(P);
	Out.Fog = get_fog_amount_new(d, vWorldPos.z);

	return Out;
}

PS_OUTPUT ps_flora_season_no_shadow(VS_OUTPUT_FLORA_SEASON_NO_SHADOW In) 
{ 
	PS_OUTPUT Output;
	float4 tex_col = tex2D(MeshTextureSampler, In.Tex0);
	
	float season = GetSeason();
	if (season < 0.5) //0= spring
	{
	tex_col = tex2D(MeshTextureSampler, In.Tex0);
	}
	else if ((season > 0.5)&&(season < 1.5)) //1= summer
	{
	tex_col = tex2D(Diffuse2Sampler, In.Tex0);
	}
	else if ((season > 1.5)&&(season < 2.5)) //2= autumn
	{
	tex_col = tex2D(NormalTextureSampler, In.Tex0);
	}
	else if ((season > 2.5)) //3= winter
	{
	tex_col = tex2D(SpecularTextureSampler, In.Tex0);
	}
	
	
	clip(tex_col.a - 0.05f);
	
	INPUT_TEX_GAMMA(tex_col.rgb);

	Output.RGBColor = tex_col * In.Color;
	OUTPUT_GAMMA(Output.RGBColor.rgb);
	
	return Output;
}





DEFINE_TECHNIQUES(flora_season, vs_flora_season, ps_flora_season)

technique flora_season_PRESHADED
{
	pass P0
	{
		VertexShader = compile vs_2_0 vs_flora_season_no_shadow();
		PixelShader = compile ps_2_0 ps_flora_season_no_shadow();
	}
}
DEFINE_LIGHTING_TECHNIQUE(flora_season, 0, 0, 0, 0, 0)




VS_OUTPUT_FLORA_SEASON vs_flora_season_grass(uniform const int PcfMode, float4 vPosition : POSITION, float4 vColor : COLOR0, float2 tc : TEXCOORD0)
{
	INITIALIZE_OUTPUT(VS_OUTPUT_FLORA_SEASON, Out);

	
	float4 WorldPosit = (float4)mul(matWorld,vPosition);
	float timer_variable = tree_rate * time_var;
	float WindFactor = 0.333 * GetWindAmountNew(1.0f, vPosition.z); //range of 0 to 3
	
	
	float texcordY = 1-tc.y;
	if ((tc.y < 0.15)||((tc.y > 0.165) && (tc.y < 0.320))||((tc.x > 0.500) && (tc.y > 0.330) && (tc.y < 0.640)))
	{
	float2 WorldPosition = float2(WorldPosit.z,WorldPosit.y);//float2((matWorldViewProj,vPosition.x),(matWorldViewProj,vPosition.y));
	float2 OriginalPosition = float2(vPosition.x,vPosition.y);
	vPosition.x = vPosition.x + (WindFactor*(TreeAmplitude.x*0.35)) * sin(TreePeriod.x *  WorldPosition.x + (timer_variable)); //
	vPosition.x = vPosition.x + (WindFactor*(TreeAmplitude.x*0.35)) * sin((TreePeriod.x * 30.5) * WorldPosition.x + ((0.2*timer_variable))); //
	vPosition.y = vPosition.y + (WindFactor*(TreeAmplitude.x*0.35)) * sin((TreePeriod.x * 30.76) * WorldPosition.x + ((1.1*timer_variable))); //
	//vPosition.z -= 0.1*sqrt(pow((OriginalPosition.x-vPosition.x),2));
	}
	else //vert is a bottom vert
	{
	//vPosition.z += 0.10;
	}
	
	Out.Pos = mul(matWorldViewProj, vPosition);
	float4 vWorldPos = (float4)mul(matWorld,vPosition);

	//leaf shimmering waving - should be fastish(by altering time vra below (perhaps use the stuff from windyflora
    float2 coords = float2(tc.x,tc.y);
	float moveamount = sin(time_var + dot(vPosition.xy , float2(6.5,4.5))) * GetSeasonWindFactor();	//: GetSeasonWindFactor
    coords.x +=  0.015*moveamount;
	
	coords.x = lerp(coords.x, tc.x, saturate(tc.y*tc.y+0.1f));	//!

	Out.Tex0 = coords;

	//   Out.Color = vColor * vMaterialColor;
	Out.Color = vColor * (vAmbientColor + vSunColor * 0.06f); //add some sun color to simulate sun passing through leaves.
	Out.Color.a *= vMaterialColor.a;

	//   Out.Color = vColor * vMaterialColor * (vAmbientColor + vSunColor * 0.15f);
	//shadow mapping variables
	Out.SunLight = (vSunColor * 0.34f)* vMaterialColor * vColor;

	if (PcfMode != PCF_NONE)
	{
		float4 ShadowPos = mul(matSunViewProj, vWorldPos);
		Out.ShadowTexCoord = ShadowPos;
		Out.ShadowTexCoord.z /= ShadowPos.w;
		Out.ShadowTexCoord.w = 1.0f;
		Out.ShadowTexelPos = Out.ShadowTexCoord * fShadowMapSize;
	}
	//shadow mapping variables end
	
	//apply fog
	float3 P = mul(matWorldView, vPosition); //position in view space
	float d = length(P);
	Out.Fog = get_fog_amount_new(d, vWorldPos.z);
	
	Out.Color.a *= min(1.0f,(1.0f - (d / 50.0f)) * 2.0f);

	return Out;
}



PS_OUTPUT ps_flora_season_grass(VS_OUTPUT_FLORA_SEASON In, uniform const int PcfMode) 
{ 
	PS_OUTPUT Output;
	
	float4 tex_col = tex2D(MeshTextureSampler, In.Tex0);
	float season = GetSeason();
	
	if (season < 0.5) //0= spring
	{
	tex_col = tex2D(MeshTextureSampler, In.Tex0);
	}
	else if ((season > 0.5)&&(season < 1.5)) //1= summer
	{
	tex_col = tex2D(EnvTextureSampler, In.Tex0);
	}
	else if ((season > 1.5)&&(season < 2.5)) //2= autumn
	{
	tex_col = tex2D(NormalTextureSampler, In.Tex0);
	}
	else if ((season > 2.5)) //3= winter
	{
	tex_col = tex2D(SpecularTextureSampler, In.Tex0);
	}
	
	clip(tex_col.a - 0.05f);
	
	INPUT_TEX_GAMMA(tex_col.rgb);


	if (PcfMode != PCF_NONE)
	{
		float sun_amount = GetSunAmount(PcfMode, In.ShadowTexCoord, In.ShadowTexelPos);
		Output.RGBColor =  tex_col * ((In.Color + In.SunLight * sun_amount));
	}
	else
	{
		Output.RGBColor =  tex_col * ((In.Color + In.SunLight));
	}

	//Output.RGBColor = tex_col * In.Color;
	OUTPUT_GAMMA(Output.RGBColor.rgb);
	
	return Output;
}


VS_OUTPUT_FLORA_SEASON_NO_SHADOW vs_flora_season_grass_no_shadow(float4 vPosition : POSITION, float4 vColor : COLOR0, float2 tc : TEXCOORD0)
{
	INITIALIZE_OUTPUT(VS_OUTPUT_FLORA_SEASON_NO_SHADOW, Out);
	
	
	float4 WorldPosit = (float4)mul(matWorld,vPosition);
	float timer_variable = tree_rate * time_var;
	float WindFactor = 0.333 * GetWindAmountNew(1.0f, vPosition.z); //range of 0 to 3
	
	
	float texcordY = 1-tc.y;
	if ((tc.y < 0.15)||((tc.y > 0.165) && (tc.y < 0.320))||((tc.x > 0.500) && (tc.y > 0.330) && (tc.y < 0.640)))
	{
	float2 WorldPosition = float2(WorldPosit.z,WorldPosit.y);//float2((matWorldViewProj,vPosition.x),(matWorldViewProj,vPosition.y));
	float2 OriginalPosition = float2(vPosition.x,vPosition.y);
	vPosition.x = vPosition.x + (WindFactor*(TreeAmplitude.x*0.35)) * sin(TreePeriod.x *  WorldPosition.x + (timer_variable)); //
	vPosition.x = vPosition.x + (WindFactor*(TreeAmplitude.x*0.35)) * sin((TreePeriod.x * 30.5) * WorldPosition.x + ((0.2*timer_variable))); //
	vPosition.y = vPosition.y + (WindFactor*(TreeAmplitude.x*0.35)) * sin((TreePeriod.x * 30.76) * WorldPosition.x + ((1.1*timer_variable))); //
	//vPosition.z -= 0.1*sqrt(pow((OriginalPosition.x-vPosition.x),2));
	}
	else //vert is a bottom vert
	{
	//vPosition.z += 0.10;
	}
	
	Out.Pos = mul(matWorldViewProj, vPosition);
	//float4 vWorldPos = (float4)mul(matWorld,vPosition);
float4 vWorldPos = (float4)mul(matWorld,vPosition);
	
	float3 P = mul(matWorldView, vPosition); //position in view space

		//leaf shimmering waving - should be fastish(by altering time vra below (perhaps use the stuff from windyflora
    float2 coords = float2(tc.x,tc.y);
	float moveamount = sin(time_var + dot(vPosition.xy , float2(6.5,4.5))) * GetSeasonWindFactor();	//!: GetSeasonWindFactor
    coords.x +=  0.015*moveamount;
	
	coords.x = lerp(coords.x, tc.x, saturate(tc.y*tc.y+0.1f));	//!

	Out.Tex0 = coords;
	Out.Color = vColor * vMaterialColor;

	//apply fog
	float d = length(P);
	Out.Fog = get_fog_amount_new(d, vWorldPos.z);
	
	Out.Color.a = min(1.0f,(1.0f - (d / 50.0f)) * 2.0f);

	return Out;
}

PS_OUTPUT ps_flora_season_grass_no_shadow(VS_OUTPUT_FLORA_SEASON_NO_SHADOW In) 
{ 
	PS_OUTPUT Output;
	
	float4 tex_col = tex2D(MeshTextureSampler, In.Tex0);
	
	float season = GetSeason();
	if (season < 0.5) //0= spring
	{
	tex_col = tex2D(MeshTextureSampler, In.Tex0);
	}
	else if ((season > 0.5)&&(season < 1.5)) //1= summer
	{
	tex_col = tex2D(EnvTextureSampler, In.Tex0);
	}
	else if ((season > 1.5)&&(season < 2.5)) //2= autumn
	{
	tex_col = tex2D(NormalTextureSampler, In.Tex0);
	}
	else if ((season > 2.5)) //3= winter
	{
	tex_col = tex2D(SpecularTextureSampler, In.Tex0);
	}
	
	//
	clip(tex_col.a - 0.05f);
	
	INPUT_TEX_GAMMA(tex_col.rgb);

	Output.RGBColor = tex_col * In.Color;
	OUTPUT_GAMMA(Output.RGBColor.rgb);
	
	return Output;
}


DEFINE_TECHNIQUES(flora_season_grass, vs_flora_season_grass, ps_flora_season_grass)

technique flora_season_grass_PRESHADED
{
	pass P0
	{
		VertexShader = compile vs_2_0 vs_flora_season_grass_no_shadow();
		PixelShader = compile ps_2_0 ps_flora_season_grass_no_shadow();
	}
}
DEFINE_LIGHTING_TECHNIQUE(flora_season_grass, 0, 0, 0, 0, 0)



struct VS_OUTPUT_FLORA_MAP
{
	float4 Pos					: POSITION;
	float  Fog				    : FOG;
	
	float4 Color				: COLOR0;
	float4 Tex0					: TEXCOORD0;
	float4 SunLight				: TEXCOORD1;
	float4 ShadowTexCoord		: TEXCOORD2;
	float2 ShadowTexelPos		: TEXCOORD3;
	float2 WorldPos		: TEXCOORD4;
};


/////////FLORA MAP SHADER
VS_OUTPUT_FLORA_MAP vs_flora_map(uniform const int PcfMode, float4 vPosition : POSITION, float4 vColor : COLOR0, float2 tc : TEXCOORD0)
{
	INITIALIZE_OUTPUT(VS_OUTPUT_FLORA_MAP, Out);

	float3 vecObjectPos = vPosition.xyz;
	float4 vecWorldPositiom = (float4)mul(matWorld,vPosition);
	//change to objspacce / vpos is in worldspace

	vPosition.z += 0.01 * sin(0.7* vPosition.y + 0.5 * time_var);
	vPosition.x += 0.015 * sin(0.9* vPosition.y + 0.4 * time_var);
	
	
	
	Out.Pos = mul(matWorldViewProj, vPosition);
	float4 vWorldPos = (float4)mul(matWorld,vPosition);
	Out.WorldPos = vWorldPos.xy;
	

	Out.Tex0.xy = tc;
	
	
	Out.Tex0.xy = tc;
	Out.Tex0.z = (0.7f * (vWorldPos.z - 1.5f));
	Out.Tex0.w = vWorldPos.x;

	
	
	
	//   Out.Color = vColor * vMaterialColor;
	Out.Color = vColor * (vAmbientColor + vSunColor * 0.06f); //add some sun color to simulate sun passing through leaves.
	Out.Color.a *= vMaterialColor.a;

	//   Out.Color = vColor * vMaterialColor * (vAmbientColor + vSunColor * 0.15f);
	//shadow mapping variables
	Out.SunLight = (vSunColor * 0.34f)* vMaterialColor * vColor;

	if (PcfMode != PCF_NONE)
	{
		float4 ShadowPos = mul(matSunViewProj, vWorldPos);
		Out.ShadowTexCoord = ShadowPos;
		Out.ShadowTexCoord.z /= ShadowPos.w;
		Out.ShadowTexCoord.w = 1.0f;
		Out.ShadowTexelPos = Out.ShadowTexCoord * fShadowMapSize;
	}
	//shadow mapping variables end
	
	//apply fog
	float3 P = mul(matWorldView, vPosition); //position in view space
	float d = length(P);
	Out.Fog = get_fog_amount_new(d, vWorldPos.z);

	return Out;
}


PS_OUTPUT ps_flora_map(VS_OUTPUT_FLORA_MAP In, uniform const int PcfMode) 
{ 
	PS_OUTPUT Output;
	
	float2 TexCoord = In.Tex0.xy;
	float4 wave_amp = tex2D(SpecularTextureSampler, In.Tex0.xy);
	wave_amp.r = saturate(wave_amp.r*0.01); //0.0 to 0.
	
	
	TexCoord.x += wave_amp.r * sin(10.9* TexCoord.y + 0.7 * time_var); // NO.1= HEIGHT OF WAVE       NO.2= NUMBER OF WAVES    NO.3= SPEED OF WAVES
	
	float4 tex_col = tex2D(MeshTextureSampler, TexCoord);
	float4 tex_col_snow = tex2D(Diffuse2Sampler, TexCoord);
	float snow_amount = 1;//tex2D(NormalTextureSampler, (In.WorldPos*0.01)).a;
	
	INPUT_TEX_GAMMA(tex_col.rgb);

	float season = GetSeason();
	float height = In.Tex0.z;
	if (season > 2.5) //3= winter
	{
	
	height *= 2;
	height -= 0.7;
	}
	else
	{
	height *=0.1;
	}
	
	snow_amount = saturate(height * (snow_amount) - 1.5f);
	tex_col = lerp(tex_col,tex_col_snow,snow_amount);
	
	
	
	
	clip(tex_col.a - 0.05f);
	



	if (PcfMode != PCF_NONE)
	{
		float sun_amount = GetSunAmount(PcfMode, In.ShadowTexCoord, In.ShadowTexelPos);
		Output.RGBColor =  tex_col * ((In.Color + In.SunLight * sun_amount));
	}
	else
	{
		Output.RGBColor =  tex_col * ((In.Color + In.SunLight));
	}

	//Output.RGBColor = tex_col * In.Color;
	OUTPUT_GAMMA(Output.RGBColor.rgb);
	
	return Output;
}



VS_OUTPUT_FLORA_NO_SHADOW vs_flora_map_no_shadow(float4 vPosition : POSITION, float4 vColor : COLOR0, float2 tc : TEXCOORD0)
{
	INITIALIZE_OUTPUT(VS_OUTPUT_FLORA_NO_SHADOW, Out);
	
	Out.Pos = mul(matWorldViewProj, vPosition);
	float4 vWorldPos = (float4)mul(matWorld,vPosition);

	float3 P = mul(matWorldView, vPosition); //position in view space

	Out.Tex0 = tc;
	Out.Color = vColor * vMaterialColor;

	//apply fog
	float d = length(P);
	Out.Fog = get_fog_amount_new(d, vWorldPos.z);

	return Out;
}

PS_OUTPUT ps_flora_map_no_shadow(VS_OUTPUT_FLORA_NO_SHADOW In) 
{ 
	PS_OUTPUT Output;
	
	float2 TexCoord = In.Tex0;
	float4 wave_amp = tex2D(SpecularTextureSampler, In.Tex0);
	wave_amp.r *= 0.5; //0.0 to 0.5
	wave_amp.r *= 0.1; //0.0 to 0.05
	
	TexCoord.x += wave_amp.r * sin(5.9* TexCoord.y + 0.7 * time_var); // NO.1= HEIGHT OF WAVE       NO.2= NUMBER OF WAVES    NO.3= SPEED OF WAVES
	
	float4 tex_col = tex2D(MeshTextureSampler, TexCoord);

	clip(tex_col.a - 0.05f);
	
	INPUT_TEX_GAMMA(tex_col.rgb);

	Output.RGBColor = tex_col * In.Color;
	OUTPUT_GAMMA(Output.RGBColor.rgb);
	
	return Output;
}




DEFINE_TECHNIQUES(flora_map, vs_flora_map, ps_flora_map)

technique flora_map_PRESHADED
{
	pass P0
	{
		VertexShader = compile vs_2_0 vs_flora_map_no_shadow();
		PixelShader = compile ps_2_0 ps_flora_map_no_shadow();
	}
}
DEFINE_LIGHTING_TECHNIQUE(flora_map, 0, 0, 0, 0, 0)


////END MAP FLORA



DEFINE_TECHNIQUES(flora_Instanced, vs_flora_Instanced, ps_flora)


technique grass_no_shadow
{
	pass P0
	{
		VertexShader = compile vs_2_0 vs_grass_no_shadow();
		PixelShader = compile ps_2_0 ps_grass_no_shadow();
	}
}

DEFINE_TECHNIQUES(grass, vs_grass, ps_grass)

technique grass_PRESHADED
{
	pass P0
	{
		VertexShader = compile vs_2_0 vs_grass_no_shadow();
		PixelShader = compile ps_2_0 ps_grass_no_shadow();
	}
}
DEFINE_LIGHTING_TECHNIQUE(grass, 0, 0, 0, 0, 0)
#endif

/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#ifdef MAP_SHADERS



struct VS_OUTPUT_NEW_MAP
{
	float4 Pos					: POSITION;
	float4 Color				: COLOR0;
	float4 Tex0					: TEXCOORD0;
	float3 CameraDir				: TEXCOORD1;
	float4 ShadowTexCoord		: TEXCOORD2;
	float2 ShadowTexelPos		: TEXCOORD3;
	float  Fog				    : FOG;
	
	float3 SunLightDir			: TEXCOORD4;
	float3 SkyLightDir			: TEXCOORD5;
	
	float3 ViewDir				: TEXCOORD6;
	float3 WorldNormal			: TEXCOORD7;
};
VS_OUTPUT_NEW_MAP vs_new_map(uniform const int PcfMode, float4 vPosition : POSITION, 
									float3 vNormal : NORMAL, float3 vTangent : TANGENT, float3 vBinormal : BINORMAL,
									float2 tc : TEXCOORD0, float4 vColor : COLOR0,float4 vLightColor : COLOR1)
{
	INITIALIZE_OUTPUT(VS_OUTPUT_NEW_MAP, Out);

	Out.Pos = mul(matWorldViewProj, vPosition);

	float4 vWorldPos = (float4)mul(matWorld,vPosition);
	
	float3 vWorldN = normalize(mul((float3x3)matWorld, vNormal)); //normal in world space
	float3 vWorld_binormal = normalize(mul((float3x3)matWorld, vBinormal)); //normal in world space
	float3 vWorld_tangent  = normalize(mul((float3x3)matWorld, vTangent)); //normal in world space
	float3x3 TBNMatrix = float3x3(vWorld_tangent, vWorld_binormal, vWorldN); 
	
	Out.Tex0.xy = tc;
	Out.Tex0.z = (0.7f * (vWorldPos.z - 1.5f));
	Out.Tex0.w = vWorldPos.x;

	float4 diffuse_light = vAmbientColor;

	if (true /*_UseSecondLight*/)
	{
		diffuse_light += vLightColor;
	}

	//directional lights, compute diffuse color
	diffuse_light += saturate(dot(vWorldN, -vSkyLightDir)) * vSkyLightColor;
	
	//point lights
	#ifndef USE_LIGHTING_PASS
	diffuse_light += calculate_point_lights_diffuse(vWorldPos, vWorldN, false, false);
	#endif
	
	//apply material color
	//	Out.Color = min(1, vMaterialColor * vColor * diffuse_light);
	Out.Color = (vMaterialColor * vColor * diffuse_light);

	//shadow mapping variables

	//move sun light to pixel shader
	//float wNdotSun = saturate(dot(vWorldN, -vSunDir));
	//Out.SunLight = (wNdotSun) * vSunColor * vMaterialColor * vColor;
	Out.SunLightDir = normalize(mul(TBNMatrix, -vSunDir));
	
	if (PcfMode != PCF_NONE)
	{
		float4 ShadowPos = mul(matSunViewProj, vWorldPos);
		Out.ShadowTexCoord = ShadowPos;
		Out.ShadowTexCoord.z /= ShadowPos.w;
		Out.ShadowTexCoord.w = 1.0f;
		Out.ShadowTexelPos = Out.ShadowTexCoord * fShadowMapSize;
		//shadow mapping variables end
	}
	
	Out.ViewDir = normalize(vCameraPos-vWorldPos);
	Out.CameraDir = mul(TBNMatrix, -Out.ViewDir.xyz);
	
	Out.WorldNormal = vWorldN;
	
	//apply fog
	float3 P = mul(matWorldView, vPosition); //position in view space
	float d = length(P);

	Out.Fog = get_fog_amount_new(d, vWorldPos.z);
	return Out;
}


PS_OUTPUT ps_new_map(VS_OUTPUT_NEW_MAP In, uniform const int PcfMode)
{
	PS_OUTPUT Output;
	
	
	
		
	float2 parallaxcoords = 0.95*In.Tex0.xy;
	parallaxcoords.x = parallaxcoords.x + 0.1*sin(parallaxcoords.y);
	
//PARALLAX SECTION
	float3 viewVec = normalize(In.CameraDir);
	{
     float factor = (0.01f * vSpecularColor.x);
     float volume = (factor * 1.0);//0.04;
     float bias = (factor * -0.5f);//-0.02; 

	//PARALLAX TEX A
	float height = tex2D(EnvTextureSampler, parallaxcoords).a;
	float offset = height * volume + bias;
	
	//APPLY PARALLAX TO TEXCOORDS
	In.Tex0.xy += offset * viewVec.xy;
	//In.PosWater.xy += offset * viewVec.xy;
	parallaxcoords +=offset * viewVec.xy;
	}
//PARALLAX END

	
	
	float4 tex_col = tex2D(MeshTextureSampler, In.Tex0.xy);
	INPUT_TEX_GAMMA(tex_col.rgb);
	
	float season = GetSeason();
	float height = In.Tex0.z;
	if (season > 2.5) //3= winter
	{
	
	height *= 2;
	height += 1.65;
	}
	else
	{
	height *=1;
	}
	
	tex_col.rgb += saturate(height * (tex_col.a) - 1.5f);
	tex_col.a = 1.0f;
	
	//parallax darkening
	tex_col.rgb = lerp(tex_col.rgb*float3(0.8,0.75,0.65), tex_col.rgb*1.30,1-tex2D(EnvTextureSampler, parallaxcoords).a);
	//
	
	
	
	float3 normal = (2.0f * tex2D(NormalTextureSampler, In.Tex0.xy * map_normal_detail_factor).rgb - 1.0f);
	float3 normalpara = (2.0f * tex2D(EnvTextureSampler, parallaxcoords).rgb - 1.0f);
	
	//float wNdotSun = saturate(dot(vWorldN, -vSunDir));
	//Out.SunLight = (wNdotSun) * vSunColor * vMaterialColor * vColor;
	float4 In_SunLight = saturate(dot(normal, In.SunLightDir)) * vSunColor * vMaterialColor;// * vColor;  vertex color needed??
	
	float sun_amount = 1;
	if ((PcfMode != PCF_NONE))
	{
		sun_amount = GetSunAmount(PcfMode, In.ShadowTexCoord, In.ShadowTexelPos);
	}
	

	
	Output.RGBColor =  tex_col * ((In.Color + In_SunLight * sun_amount));
	
	
	//add fresnel term
	{
		float fresnel = 1-(saturate(dot( normalize(In.ViewDir), normalpara)));
		float fresnel2 = 1-(saturate(dot( normalize(In.ViewDir), normal)));
		
		fresnel *= fresnel2; 
		//fresnel = max(0.75,fresnel);
		//fresnel = min(0.3,fresnel);
		Output.RGBColor.rgb = lerp(Output.RGBColor.rgb,Output.RGBColor.rgb*fresnel,0.5);//max(0.6,fresnel+0.1); 
	}	
	// gamma correct
	OUTPUT_GAMMA(Output.RGBColor.rgb);
	
	
	return Output;
}

VertexShader vs_new_map_compiled_PCF_NONE = compile vs_2_0 vs_new_map(PCF_NONE);
VertexShader vs_new_map_compiled_PCF_DEFAULT = compile vs_2_0 vs_new_map(PCF_DEFAULT);
VertexShader vs_new_map_compiled_PCF_NVIDIA = compile vs_2_0 vs_new_map(PCF_NVIDIA);

technique new_map_shader
{
	pass P0
	{
		VertexShader = vs_new_map_compiled_PCF_NONE;
		PixelShader = compile PS_2_X ps_new_map(PCF_NONE);
	}
}


PS_OUTPUT ps_new_map_2(VS_OUTPUT_NEW_MAP In, uniform const int PcfMode)
{
	PS_OUTPUT Output;
	
	
	
		
	float2 parallaxcoords = 0.95*In.Tex0.xy;
	parallaxcoords.x = parallaxcoords.x + 0.1*sin(parallaxcoords.y);
	
//PARALLAX SECTION
	float3 viewVec = normalize(In.CameraDir);
	{
     float factor = (0.01f * vSpecularColor.x);
     float volume = (factor * 1.0);//0.04;
     float bias = (factor * -0.5f);//-0.02; 

	//PARALLAX TEX A
	float height = tex2D(EnvTextureSampler, parallaxcoords).a;
	float offset = height * volume + bias;
	
	//APPLY PARALLAX TO TEXCOORDS
	In.Tex0.xy += offset * viewVec.xy;
	//In.PosWater.xy += offset * viewVec.xy;
	parallaxcoords +=offset * viewVec.xy;
	}
//PARALLAX END

	
	
	float4 tex_col = tex2D(MeshTextureSampler, In.Tex0.xy);
	INPUT_TEX_GAMMA(tex_col.rgb);
	
	float season = GetSeason();
	float height = In.Tex0.z;
	float latitude = In.Tex0.w + 155; //(so oriin is in mid north sea)
	if (season > 2.5) //3= winter
	{
	height *= 2;
	height += 1;
	height *= 1.5;
	}
	else
	{
	height *= 2;
	height += 1;
	latitude = 1-saturate(latitude);
	latitude += 0.5;
	height *= latitude;
	}
	
	tex_col.rgb += saturate(height * (tex_col.a) - 1.5f);
	tex_col.a = 1.0f;
	
	//parallax darkening
	tex_col.rgb = lerp(tex_col.rgb*float3(0.8,0.75,0.65), tex_col.rgb*1.30,1-tex2D(EnvTextureSampler, parallaxcoords).a);
	//
	
	
	
	float3 normal = (2.0f * tex2D(NormalTextureSampler, In.Tex0.xy * map_normal_detail_factor).rgb - 1.0f);
	float3 normalpara = (2.0f * tex2D(EnvTextureSampler, parallaxcoords).rgb - 1.0f);
	
	//float wNdotSun = saturate(dot(vWorldN, -vSunDir));
	//Out.SunLight = (wNdotSun) * vSunColor * vMaterialColor * vColor;
	float4 In_SunLight = saturate(dot(normal, In.SunLightDir)) * vSunColor * vMaterialColor;// * vColor;  vertex color needed??
	
	float sun_amount = 1;
	if ((PcfMode != PCF_NONE))
	{
		sun_amount = GetSunAmount(PcfMode, In.ShadowTexCoord, In.ShadowTexelPos);
	}
	

	
	Output.RGBColor =  tex_col * ((In.Color + In_SunLight * sun_amount));
	
	
	//add fresnel term
	{
		float fresnel = 1-(saturate(dot( normalize(In.ViewDir), normalpara)));
		float fresnel2 = 1-(saturate(dot( normalize(In.ViewDir), normal)));
		
		fresnel *= fresnel2; 
		//fresnel = max(0.75,fresnel);
		//fresnel = min(0.3,fresnel);
		Output.RGBColor.rgb = lerp(Output.RGBColor.rgb,Output.RGBColor.rgb*fresnel,0.5);//max(0.6,fresnel+0.1); 
	}	
	// gamma correct
	OUTPUT_GAMMA(Output.RGBColor.rgb);
	
	
	return Output;
}



technique new_map_shader_snow
{
	pass P0
	{
		VertexShader = vs_new_map_compiled_PCF_NONE;
		PixelShader = compile PS_2_X ps_new_map_2(PCF_NONE);
	}
}






//---
struct VS_OUTPUT_MAP
{
	float4 Pos					: POSITION;
	float4 Color				: COLOR0;
	float2 Tex0					: TEXCOORD0;
	float4 SunLight				: TEXCOORD1;
	float4 ShadowTexCoord		: TEXCOORD2;
	float2 ShadowTexelPos		: TEXCOORD3;
	float  Fog				    : FOG;
	
	float3 ViewDir				: TEXCOORD6;
	float3 WorldNormal			: TEXCOORD7;
};
VS_OUTPUT_MAP vs_main_map(uniform const int PcfMode, float4 vPosition : POSITION, float3 vNormal : NORMAL, 
							float2 tc : TEXCOORD0, float4 vColor : COLOR0, float4 vLightColor : COLOR1)
{
	INITIALIZE_OUTPUT(VS_OUTPUT_MAP, Out);

	Out.Pos = mul(matWorldViewProj, vPosition);

	float4 vWorldPos = (float4)mul(matWorld,vPosition);
	float3 vWorldN = normalize(mul((float3x3)matWorld, vNormal)); //normal in world space


	Out.Tex0 = tc;

	float4 diffuse_light = vAmbientColor;

	if (true /*_UseSecondLight*/)
	{
		diffuse_light += vLightColor;
	}

	//directional lights, compute diffuse color
	diffuse_light += saturate(dot(vWorldN, -vSkyLightDir)) * vSkyLightColor;
	
	//apply material color
	//	Out.Color = min(1, vMaterialColor * vColor * diffuse_light);
	Out.Color = (vMaterialColor * vColor * diffuse_light);

	//shadow mapping variables
	float wNdotSun = saturate(dot(vWorldN, -vSunDir));
	Out.SunLight = (wNdotSun) * vSunColor * vMaterialColor * vColor;
	if (PcfMode != PCF_NONE)
	{
		float4 ShadowPos = mul(matSunViewProj, vWorldPos);
		Out.ShadowTexCoord = ShadowPos;
		Out.ShadowTexCoord.z /= ShadowPos.w;
		Out.ShadowTexCoord.w = 1.0f;
		Out.ShadowTexelPos = Out.ShadowTexCoord * fShadowMapSize;
		//shadow mapping variables end
	}
	
	Out.ViewDir = normalize(vCameraPos-vWorldPos);
	Out.WorldNormal = vWorldN;
	
	//apply fog
	float3 P = mul(matWorldView, vPosition); //position in view space
	float d = length(P);

	Out.Fog = get_fog_amount_new(d, vWorldPos.z);
	return Out;
}
PS_OUTPUT ps_main_map(VS_OUTPUT_MAP In, uniform const int PcfMode)
{
	PS_OUTPUT Output;
	
	float4 tex_col = tex2D(MeshTextureSampler, In.Tex0);
	INPUT_TEX_GAMMA(tex_col.rgb);
	
	float sun_amount = 1;
	if ((PcfMode != PCF_NONE))
	{
		sun_amount = GetSunAmount(PcfMode, In.ShadowTexCoord, In.ShadowTexelPos);
	}
	Output.RGBColor =  tex_col * ((In.Color + In.SunLight * sun_amount));
	
	
	//add fresnel term
	{
		float fresnel = 1-(saturate(dot( normalize(In.ViewDir), normalize(In.WorldNormal))));
		fresnel *= fresnel;
		Output.RGBColor.rgb *= max(0.6,fresnel+0.1); 
	}	
	// gamma correct
	OUTPUT_GAMMA(Output.RGBColor.rgb);
	
	return Output;
}

DEFINE_TECHNIQUES(diffuse_map, vs_main_map, ps_main_map)	//diffuse shader with fresnel effect

//---
struct VS_OUTPUT_MAP_BUMP
{
	float4 Pos					: POSITION;
	float4 Color				: COLOR0;
	float2 Tex0					: TEXCOORD0;
	//float4 SunLight				: TEXCOORD1;
	float4 ShadowTexCoord		: TEXCOORD2;
	float2 ShadowTexelPos		: TEXCOORD3;
	float  Fog				    : FOG;
	
	float3 SunLightDir			: TEXCOORD4;
	float3 SkyLightDir			: TEXCOORD5;
	
	float3 ViewDir				: TEXCOORD6;
	float3 WorldNormal			: TEXCOORD7;
};
VS_OUTPUT_MAP_BUMP vs_main_map_bump(uniform const int PcfMode, float4 vPosition : POSITION, 
									float3 vNormal : NORMAL, float3 vTangent : TANGENT, float3 vBinormal : BINORMAL,
									float2 tc : TEXCOORD0, float4 vColor : COLOR0,float4 vLightColor : COLOR1)
{
	INITIALIZE_OUTPUT(VS_OUTPUT_MAP_BUMP, Out);

	Out.Pos = mul(matWorldViewProj, vPosition);

	float4 vWorldPos = (float4)mul(matWorld,vPosition);
	
	float3 vWorldN = normalize(mul((float3x3)matWorld, vNormal)); //normal in world space
	float3 vWorld_binormal = normalize(mul((float3x3)matWorld, vBinormal)); //normal in world space
	float3 vWorld_tangent  = normalize(mul((float3x3)matWorld, vTangent)); //normal in world space
	float3x3 TBNMatrix = float3x3(vWorld_tangent, vWorld_binormal, vWorldN); 
	
	Out.Tex0 = tc;

	float4 diffuse_light = vAmbientColor;

	if (true /*_UseSecondLight*/)
	{
		diffuse_light += vLightColor;
	}

	//directional lights, compute diffuse color
	diffuse_light += saturate(dot(vWorldN, -vSkyLightDir)) * vSkyLightColor;
	
	//point lights
	#ifndef USE_LIGHTING_PASS
	diffuse_light += calculate_point_lights_diffuse(vWorldPos, vWorldN, false, false);
	#endif
	
	//apply material color
	//	Out.Color = min(1, vMaterialColor * vColor * diffuse_light);
	Out.Color = (vMaterialColor * vColor * diffuse_light);

	//shadow mapping variables

	//move sun light to pixel shader
	//float wNdotSun = saturate(dot(vWorldN, -vSunDir));
	//Out.SunLight = (wNdotSun) * vSunColor * vMaterialColor * vColor;
	Out.SunLightDir = normalize(mul(TBNMatrix, -vSunDir));
	
	if (PcfMode != PCF_NONE)
	{
		float4 ShadowPos = mul(matSunViewProj, vWorldPos);
		Out.ShadowTexCoord = ShadowPos;
		Out.ShadowTexCoord.z /= ShadowPos.w;
		Out.ShadowTexCoord.w = 1.0f;
		Out.ShadowTexelPos = Out.ShadowTexCoord * fShadowMapSize;
		//shadow mapping variables end
	}
	
	Out.ViewDir = normalize(vCameraPos-vWorldPos);
	Out.WorldNormal = vWorldN;
	
	//apply fog
	float3 P = mul(matWorldView, vPosition); //position in view space
	float d = length(P);

	Out.Fog = get_fog_amount_new(d, vWorldPos.z);
	return Out;
}
PS_OUTPUT ps_main_map_bump(VS_OUTPUT_MAP_BUMP In, uniform const int PcfMode)
{
	PS_OUTPUT Output;
	
	float4 tex_col = tex2D(MeshTextureSampler, In.Tex0);
	INPUT_TEX_GAMMA(tex_col.rgb);
	
	
	float3 normal = (2.0f * tex2D(NormalTextureSampler, In.Tex0 * map_normal_detail_factor).rgb - 1.0f);
	
	//float wNdotSun = saturate(dot(vWorldN, -vSunDir));
	//Out.SunLight = (wNdotSun) * vSunColor * vMaterialColor * vColor;
	float4 In_SunLight = saturate(dot(normal, In.SunLightDir)) * vSunColor * vMaterialColor;// * vColor;  vertex color needed??
	
	float sun_amount = 1;
	if ((PcfMode != PCF_NONE))
	{
		sun_amount = GetSunAmount(PcfMode, In.ShadowTexCoord, In.ShadowTexelPos);
	}
	Output.RGBColor =  tex_col * ((In.Color + In_SunLight * sun_amount));
	
	
	//add fresnel term
	{
		float fresnel = 1-(saturate(dot( normalize(In.ViewDir), normalize(In.WorldNormal))));
		fresnel *= fresnel;
		Output.RGBColor.rgb *= max(0.6,fresnel+0.1); 
	}	
	// gamma correct
	OUTPUT_GAMMA(Output.RGBColor.rgb);
	
	
	return Output;
}

DEFINE_TECHNIQUES(diffuse_map_bump, vs_main_map_bump, ps_main_map_bump)	//diffuse shader with fresnel effect + bumpmapping(if shader_quality medium)..


struct VS_OUTPUT_MAP_BUMP_BEACH
{
	float4 Pos					: POSITION;
	float4 Color				: COLOR0;
	float2 Tex0					: TEXCOORD0;
	float2 VertPos				: TEXCOORD1;
	float4 ShadowTexCoord		: TEXCOORD2;
	float2 ShadowTexelPos		: TEXCOORD3;
	float  Fog				    : FOG;
	
	float3 SunLightDir			: TEXCOORD4;
	float3 SkyLightDir			: TEXCOORD5;
	
	float3 ViewDir				: TEXCOORD6;
	float3 WorldNormal			: TEXCOORD7;
};
VS_OUTPUT_MAP_BUMP_BEACH vs_main_map_bump_beach(uniform const int PcfMode, float4 vPosition : POSITION, 
									float3 vNormal : NORMAL, float3 vTangent : TANGENT, float3 vBinormal : BINORMAL,
									float2 tc : TEXCOORD0, float4 vColor : COLOR0,float4 vLightColor : COLOR1)
{
	INITIALIZE_OUTPUT(VS_OUTPUT_MAP_BUMP_BEACH, Out);

	Out.Pos = mul(matWorldViewProj, vPosition);
	
	Out.VertPos.x = vPosition.z;
	Out.VertPos.y = -30.02 + 0.03 * sin(35.8*  vPosition.x + 2.5 * time_var); // 3 is approximate level of water, and equation after is water including waves

	float4 vWorldPos = (float4)mul(matWorld,vPosition);
	
	float3 vWorldN = normalize(mul((float3x3)matWorld, vNormal)); //normal in world space
	float3 vWorld_binormal = normalize(mul((float3x3)matWorld, vBinormal)); //normal in world space
	float3 vWorld_tangent  = normalize(mul((float3x3)matWorld, vTangent)); //normal in world space
	float3x3 TBNMatrix = float3x3(vWorld_tangent, vWorld_binormal, vWorldN); 
	
	Out.Tex0 = tc;

	float4 diffuse_light = vAmbientColor;

	if (true /*_UseSecondLight*/)
	{
		diffuse_light += vLightColor;
	}

	//directional lights, compute diffuse color
	diffuse_light += saturate(dot(vWorldN, -vSkyLightDir)) * vSkyLightColor;
	
	//point lights
	#ifndef USE_LIGHTING_PASS
	diffuse_light += calculate_point_lights_diffuse(vWorldPos, vWorldN, false, false);
	#endif
	
	//apply material color
	//	Out.Color = min(1, vMaterialColor * vColor * diffuse_light);
	Out.Color = (vMaterialColor * vColor * diffuse_light);

	//shadow mapping variables

	//move sun light to pixel shader
	//float wNdotSun = saturate(dot(vWorldN, -vSunDir));
	//Out.SunLight = (wNdotSun) * vSunColor * vMaterialColor * vColor;
	Out.SunLightDir = normalize(mul(TBNMatrix, -vSunDir));
	
	if (PcfMode != PCF_NONE)
	{
		float4 ShadowPos = mul(matSunViewProj, vWorldPos);
		Out.ShadowTexCoord = ShadowPos;
		Out.ShadowTexCoord.z /= ShadowPos.w;
		Out.ShadowTexCoord.w = 1.0f;
		Out.ShadowTexelPos = Out.ShadowTexCoord * fShadowMapSize;
		//shadow mapping variables end
	}
	
	Out.ViewDir = normalize(vCameraPos-vWorldPos);
	Out.WorldNormal = vWorldN;
	
	//apply fog
	float3 P = mul(matWorldView, vPosition); //position in view space
	float d = length(P);

	Out.Fog = get_fog_amount_new(d, vWorldPos.z);
	return Out;
}
PS_OUTPUT ps_main_map_bump_beach(VS_OUTPUT_MAP_BUMP_BEACH In, uniform const int PcfMode)
{
	PS_OUTPUT Output;
	
	float4 tex_col = tex2D(MeshTextureSampler, In.Tex0);
	INPUT_TEX_GAMMA(tex_col.rgb);
	
	
	float3 normal = (2.0f * tex2D(NormalTextureSampler, In.Tex0 * map_normal_detail_factor).rgb - 1.0f);
	
	//float wNdotSun = saturate(dot(vWorldN, -vSunDir));
	//Out.SunLight = (wNdotSun) * vSunColor * vMaterialColor * vColor;
	float4 In_SunLight = saturate(dot(normal, In.SunLightDir)) * vSunColor * vMaterialColor;// * vColor;  vertex color needed??
	
	float sun_amount = 1;
	if ((PcfMode != PCF_NONE))
	{
		sun_amount = GetSunAmount(PcfMode, In.ShadowTexCoord, In.ShadowTexelPos);
	}
	Output.RGBColor =  tex_col * ((In.Color + In_SunLight * sun_amount));
	
	
	//add fresnel term
	{
		float fresnel = 1-(saturate(dot( normalize(In.ViewDir), normalize(In.WorldNormal))));
		fresnel *= fresnel;
		Output.RGBColor.rgb *= max(0.6,fresnel+0.1); 
	}	
	// gamma correct
	OUTPUT_GAMMA(Output.RGBColor.rgb);
	
	
	
	if (In.VertPos.x < In.VertPos.y) //if pixel is below height of 
	{
	float2 TexSiz = In.Tex0 ;
	TexSiz.x += (time_var * 0.1);	
	Output.RGBColor.rgb += (0.5 * tex2D(Diffuse2Sampler, TexSiz));// saturate(0.0 + (In.ViewDir.w/2));
	TexSiz.x = In.Tex0.x - (time_var * 0.1);	
	Output.RGBColor.rgb += (0.5* tex2D(Diffuse2Sampler, TexSiz));// saturate(0.0 + (In.ViewDir.w/2));
	//Output.RGBColor.rgb *= 0.6;
	Output.RGBColor.rgb *= saturate(0.08*(In.VertPos.x));
	}
	
	
	
	return Output;
}

DEFINE_TECHNIQUES(diffuse_map_bump_beach, vs_main_map_bump_beach, ps_main_map_bump_beach)	//diffuse shader with fresnel effect + bumpmapping(if shader_quality medium)..



//---
struct VS_OUTPUT_MAP_MOUNTAIN
{
	float4 Pos					: POSITION;
	float  Fog				    : FOG;
	
	float4 Color				: COLOR0;
	float3 Tex0					: TEXCOORD0;
	float4 SunLight				: TEXCOORD1;
	float4 ShadowTexCoord		: TEXCOORD2;
	float2 ShadowTexelPos		: TEXCOORD3;
	
	float3 ViewDir				: TEXCOORD6;
	float3 WorldNormal			: TEXCOORD7;
};

VS_OUTPUT_MAP_MOUNTAIN vs_map_mountain(uniform const int PcfMode, float4 vPosition : POSITION, float3 vNormal : NORMAL, 
										float2 tc : TEXCOORD0, float4 vColor : COLOR0, float4 vLightColor : COLOR1)
{
	INITIALIZE_OUTPUT(VS_OUTPUT_MAP_MOUNTAIN, Out);

	Out.Pos = mul(matWorldViewProj, vPosition);

	float4 vWorldPos = (float4)mul(matWorld,vPosition);
	float3 vWorldN = normalize(mul((float3x3)matWorld, vNormal)); //normal in world space

	float3 P = mul(matWorldView, vPosition); //position in view space

	Out.Tex0.xy = tc;
	Out.Tex0.z = /*saturate*/(0.7f * (vWorldPos.z - 1.5f));

	float4 diffuse_light = vAmbientColor;
	if (true /*_UseSecondLight*/)
	{
		diffuse_light += vLightColor;
	}

	//directional lights, compute diffuse color
	diffuse_light += saturate(dot(vWorldN, -vSkyLightDir)) * vSkyLightColor;

	//apply material color
	//	Out.Color = min(1, vMaterialColor * vColor * diffuse_light);
	Out.Color = (vMaterialColor * vColor * diffuse_light);

	//shadow mapping variables
	float wNdotSun = saturate(dot(vWorldN, -vSunDir));
	Out.SunLight = (wNdotSun) * vSunColor;
	if (PcfMode != PCF_NONE)
	{
		float4 ShadowPos = mul(matSunViewProj, vWorldPos);
		Out.ShadowTexCoord = ShadowPos;
		Out.ShadowTexCoord.z /= ShadowPos.w;
		Out.ShadowTexCoord.w = 1.0f;
		Out.ShadowTexelPos = Out.ShadowTexCoord * fShadowMapSize;
		//shadow mapping variables end
	}
	
	
	Out.ViewDir = normalize(vCameraPos-vWorldPos);
	Out.WorldNormal = vWorldN;
	
	
	//apply fog
	float d = length(P);

	Out.Fog = get_fog_amount_new(d, vWorldPos.z);
	return Out;
}

PS_OUTPUT ps_map_mountain(VS_OUTPUT_MAP_MOUNTAIN In, uniform const int PcfMode)
{
	PS_OUTPUT Output;
	
	float4 tex_col = tex2D(MeshTextureSampler, In.Tex0.xy);
	INPUT_TEX_GAMMA(tex_col.rgb);
	
	tex_col.rgb += saturate(In.Tex0.z * (tex_col.a) - 1.5f);
	tex_col.a = 1.0f;
	
	if ((PcfMode != PCF_NONE))
	{
		float sun_amount = GetSunAmount(PcfMode, In.ShadowTexCoord, In.ShadowTexelPos);
		//		sun_amount *= sun_amount;
		Output.RGBColor =  saturate(tex_col) * ((In.Color + In.SunLight * sun_amount));
	}
	else
	{
		Output.RGBColor = saturate(tex_col) * (In.Color + In.SunLight);
	}
	
	{
		float fresnel = 1-(saturate(dot( In.ViewDir, In.WorldNormal)));
	//	fresnel *= fresnel;
		Output.RGBColor.rgb *= max(0.6,fresnel+0.1); 
	}	
	
	
	// gamma correct
	OUTPUT_GAMMA(Output.RGBColor.rgb);
	
	
	return Output;
}

DEFINE_TECHNIQUES(map_mountain, vs_map_mountain, ps_map_mountain)


//---
struct VS_OUTPUT_MAP_MOUNTAIN_BUMP
{
	float4 Pos					: POSITION;
	float4 Color					: COLOR0;
	float3 Tex0					: TEXCOORD0;
	//float4 SunLight				: TEXCOORD1;
	float4 ShadowTexCoord		: TEXCOORD2;
	float2 ShadowTexelPos		: TEXCOORD3;
	float  Fog				    : FOG;
	
	float3 SunLightDir			: TEXCOORD4;
	float3 SkyLightDir			: TEXCOORD5;
	
	float3 ViewDir				: TEXCOORD6;
	float3 WorldNormal			: TEXCOORD7;
};
VS_OUTPUT_MAP_MOUNTAIN_BUMP vs_map_mountain_bump(uniform const int PcfMode, float4 vPosition : POSITION, 
												float3 vNormal : NORMAL,  float3 vTangent : TANGENT, float3 vBinormal : BINORMAL,
												float2 tc : TEXCOORD0, float4 vColor : COLOR0, float4 vLightColor : COLOR1)
{
	INITIALIZE_OUTPUT(VS_OUTPUT_MAP_MOUNTAIN_BUMP, Out);

	Out.Pos = mul(matWorldViewProj, vPosition);

	float4 vWorldPos = (float4)mul(matWorld,vPosition);
	float3 vWorldN = normalize(mul((float3x3)matWorld, vNormal)); //normal in world space
	float3 vWorld_binormal = normalize(mul((float3x3)matWorld, vBinormal)); //normal in world space
	float3 vWorld_tangent  = normalize(mul((float3x3)matWorld, vTangent)); //normal in world space
	float3x3 TBNMatrix = float3x3(vWorld_tangent, vWorld_binormal, vWorldN); 

	float3 P = mul(matWorldView, vPosition); //position in view space

	Out.Tex0.xy = tc;
	Out.Tex0.z = /*saturate*/(0.7f * (vWorldPos.z - 1.5f));

	float4 diffuse_light = vAmbientColor;
	if (true /*_UseSecondLight*/)
	{
		diffuse_light += vLightColor;
	}

	//directional lights, compute diffuse color
	diffuse_light += saturate(dot(vWorldN, -vSkyLightDir)) * vSkyLightColor;

	//apply material color
	//	Out.Color = min(1, vMaterialColor * vColor * diffuse_light);
	Out.Color = (vMaterialColor * vColor * diffuse_light);

	//shadow mapping variables
	//float wNdotSun = saturate(dot(vWorldN, -vSunDir));
	//Out.SunLight = (wNdotSun) * vSunColor;
	Out.SunLightDir = normalize(mul(TBNMatrix, -vSunDir));
			
	if (PcfMode != PCF_NONE)
	{
		float4 ShadowPos = mul(matSunViewProj, vWorldPos);
		Out.ShadowTexCoord = ShadowPos;
		Out.ShadowTexCoord.z /= ShadowPos.w;
		Out.ShadowTexCoord.w = 1.0f;
		Out.ShadowTexelPos = Out.ShadowTexCoord * fShadowMapSize;
		//shadow mapping variables end
	}
	
	
	Out.ViewDir = normalize(vCameraPos-vWorldPos);
	Out.WorldNormal = vWorldN;
	
	
	//apply fog
	float d = length(P);

	Out.Fog = get_fog_amount_new(d, vWorldPos.z);
	return Out;
}
PS_OUTPUT ps_map_mountain_bump(VS_OUTPUT_MAP_MOUNTAIN_BUMP In, uniform const int PcfMode)
{
	PS_OUTPUT Output;
	
	float4 sample_col = tex2D(MeshTextureSampler, In.Tex0.xy);
	
	INPUT_TEX_GAMMA(sample_col.rgb);
	float4 tex_col = sample_col;
	
	tex_col.rgb += saturate(In.Tex0.z * (sample_col.a) - 1.5f);
	tex_col.a = 1.0f;
	/*    
	float snow = In.Tex0.z * (0.1f + sample_col.a) - 1.5f;
	if (snow > 0.5f)
	{
		tex_col = float4(1.0f,1.0f,1.0f,1.0f);
	}
*/    

	
	float3 normal = (2.0f * tex2D(NormalTextureSampler, In.Tex0 * map_normal_detail_factor).rgb - 1.0f);
	
	//float wNdotSun = saturate(dot(vWorldN, -vSunDir));
	//Out.SunLight = (wNdotSun) * vSunColor;
	float4 In_SunLight = saturate(dot(normal, In.SunLightDir)) * vSunColor;
	

	if ((PcfMode != PCF_NONE))
	{
		float sun_amount = GetSunAmount(PcfMode, In.ShadowTexCoord, In.ShadowTexelPos);
		//		sun_amount *= sun_amount;
		Output.RGBColor =  saturate(tex_col) * ((In.Color + In_SunLight * sun_amount));
	}
	else
	{
		Output.RGBColor = saturate(tex_col) * (In.Color + In_SunLight);
	}
	
	{
		float fresnel = 1-(saturate(dot( In.ViewDir, In.WorldNormal)));
	//	fresnel *= fresnel;
		Output.RGBColor.rgb *= max(0.6,fresnel+0.1); 
	}	
	
	
	// gamma correct
	OUTPUT_GAMMA(Output.RGBColor.rgb);
	
	
	return Output;
}

DEFINE_TECHNIQUES(map_mountain_bump, vs_map_mountain_bump, ps_map_mountain_bump)

//---
struct VS_OUTPUT_MAP_WATER
{
	float4 Pos           : POSITION;
	float4 Color	     : COLOR0;
	float2 Tex0          : TEXCOORD0;
	float3 LightDir		 : TEXCOORD1;//light direction for bump
	float3 CameraDir	 : TEXCOORD3;//camera direction for bump
	float4 PosWater		 : TEXCOORD4;//position according to the water camera
	float  Fog           : FOG;
};
VS_OUTPUT_MAP_WATER vs_map_water (uniform const bool reflections, float4 vPosition : POSITION, float3 vNormal : NORMAL, float2 tc : TEXCOORD0, float4 vColor : COLOR0, float4 vLightColor : COLOR1)
{
	INITIALIZE_OUTPUT(VS_OUTPUT_MAP_WATER, Out);

	Out.Pos = mul(matWorldViewProj, vPosition);

	float4 vWorldPos = (float4)mul(matWorld,vPosition);
	float3 vWorldN = normalize(mul((float3x3)matWorld, vNormal)); //normal in world space

	float3 P = mul(matWorldView, vPosition); //position in view space

	Out.Tex0 = tc + texture_offset.xy;


	float4 diffuse_light = vAmbientColor + vLightColor;

	//directional lights, compute diffuse color
	diffuse_light += saturate(dot(vWorldN, -vSkyLightDir)) * vSkyLightColor;

	float wNdotSun = max(-0.0001f,dot(vWorldN, -vSunDir));
	diffuse_light += (wNdotSun) * vSunColor;

	//apply material color
	//	Out.Color = min(1, vMaterialColor * vColor * diffuse_light);
	Out.Color = (vMaterialColor * vColor) * diffuse_light;
	
	
	if(reflections)
	{
		float4 water_pos = mul(matWaterViewProj, vWorldPos);
		Out.PosWater.xy = (float2(water_pos.x, -water_pos.y)+water_pos.w)/2;
		Out.PosWater.xy += (vDepthRT_HalfPixel_ViewportSizeInv.xy * water_pos.w);
		Out.PosWater.zw = water_pos.zw;
	}
	
	{
		float3 vWorldN = float3(0,0,1); //vNormal; //normalize(mul((float3x3)matWorld, vNormal)); //normal in world space
		float3 vWorld_tangent  = float3(1,0,0); //normalize(mul((float3x3)matWorld, vTangent)); //normal in world space
		float3 vWorld_binormal = float3(0,1,0); //normalize(cross(vWorld_tangent, vNormal)); //normalize(mul((float3x3)matWorld, vBinormal)); //normal in world space

		float3x3 TBNMatrix = float3x3(vWorld_tangent, vWorld_binormal, vWorldN); 

		float3 point_to_camera_normal = normalize(vCameraPos.xyz - vWorldPos.xyz);
		Out.CameraDir = mul(TBNMatrix, -point_to_camera_normal);
		Out.LightDir = mul(TBNMatrix, -vSunDir);
	}


	//apply fog
	float d = length(P);
	Out.Fog = get_fog_amount_new(d, vWorldPos.z);
	
	return Out;
}




PS_OUTPUT ps_map_water(uniform const bool reflections, VS_OUTPUT_MAP_WATER In) 
{ 
	PS_OUTPUT Output;
	Output.RGBColor =  In.Color;

	float4 tex_col = tex2D(MeshTextureSampler, In.Tex0);
	INPUT_TEX_GAMMA(tex_col.rgb);
	
	/////////////////////
	float3 normal;
	normal.xy = (2.0f * tex2D(NormalTextureSampler, In.Tex0 * 8).ag - 1.0f);
	normal.z = sqrt(1.0f - dot(normal.xy, normal.xy));
	
	float NdotL = saturate( dot(normal, In.LightDir) );
	float3 vView = normalize(In.CameraDir);

	// Fresnel term
	float fresnel = 1-(saturate(dot(vView, normal)));
	fresnel = 0.0204f + 0.9796 * (fresnel * fresnel * fresnel * fresnel * fresnel);
	Output.RGBColor.rgb += fresnel * In.Color.rgb;
	/////////////////////
		
	if(reflections)
	{
		//float4 tex = tex2D(ReflectionTextureSampler, g_HalfPixel_ViewportSizeInv.xy + 0.25f * normal.xy + float2(0.5f + 0.5f * (In.PosWater.x / In.PosWater.w), 0.5f - 0.5f * (In.PosWater.y / In.PosWater.w)));
		In.PosWater.xy += 0.35f * normal.xy;
		float4 tex = tex2Dproj(ReflectionTextureSampler, In.PosWater);
		INPUT_OUTPUT_GAMMA(tex.rgb);
		tex.rgb = min(tex.rgb, 4.0f);
		
		Output.RGBColor.rgb *= NdotL * lerp(tex_col.rgb, tex.rgb, reflection_factor);
	}
	else 
	{
		Output.RGBColor.rgb *= tex_col.rgb;
	}

	OUTPUT_GAMMA(Output.RGBColor.rgb);	//0.5 * normal + 0.5; //
	//Output.RGBColor.rgb = In.Color.rgb;
	
	Output.RGBColor.a = In.Color.a * tex_col.a;
	
	return Output;
}







//////
VS_OUTPUT_MAP_WATER vs_map_foam (uniform const bool reflections, float4 vPosition : POSITION, float3 vNormal : NORMAL, float2 tc : TEXCOORD0, float4 vColor : COLOR0, float4 vLightColor : COLOR1)
{
	INITIALIZE_OUTPUT(VS_OUTPUT_MAP_WATER, Out);

	float2 Amplitude = float2(0.2,1);
	float2 Period = float2(20,10);
	
	float2 WorldPosition = float2(tc.x,tc.y);//float2((matWorldViewProj,vPosition.x),(matWorldViewProj,vPosition.y));
	
	
	
	if (vPosition.z < 0.7)
	{
	vPosition.z = vPosition.z + Amplitude.x * sin(Period.x *  WorldPosition.x + time_var); //
	vPosition.z = vPosition.z + Amplitude.y * sin(Period.y *  WorldPosition.y + time_var); //
	}
		
	Out.Pos = mul(matWorldViewProj, vPosition);

	float4 vWorldPos = (float4)mul(matWorld,vPosition);
	float3 vWorldN = normalize(mul((float3x3)matWorld, vNormal)); //normal in world space

	float3 P = mul(matWorldView, vPosition); //position in view space

	Out.Tex0 = tc;


	float4 diffuse_light = vAmbientColor + vLightColor;

	//directional lights, compute diffuse color
	diffuse_light += saturate(dot(vWorldN, -vSkyLightDir)) * vSkyLightColor;

	float wNdotSun = max(-0.0001f,dot(vWorldN, -vSunDir));
	diffuse_light += (wNdotSun) * vSunColor;

	//apply material color
	//	Out.Color = min(1, vMaterialColor * vColor * diffuse_light);
	Out.Color = (vMaterialColor * vColor) * diffuse_light;
	
	Out.PosWater = vWorldPos;
	
	
	{
		float3 vWorldN = float3(0,0,1); //vNormal; //normalize(mul((float3x3)matWorld, vNormal)); //normal in world space
		float3 vWorld_tangent  = float3(1,0,0); //normalize(mul((float3x3)matWorld, vTangent)); //normal in world space
		float3 vWorld_binormal = float3(0,1,0); //normalize(cross(vWorld_tangent, vNormal)); //normalize(mul((float3x3)matWorld, vBinormal)); //normal in world space

		float3x3 TBNMatrix = float3x3(vWorld_tangent, vWorld_binormal, vWorldN); 

		float3 point_to_camera_normal = normalize(vCameraPos.xyz - vWorldPos.xyz);
		Out.CameraDir = mul(TBNMatrix, -point_to_camera_normal);
		Out.LightDir = mul(TBNMatrix, -vSunDir);
	}


	//apply fog
	float d = length(P);
	Out.Fog = get_fog_amount_new(d, vWorldPos.z);
	
	return Out;
}




PS_OUTPUT ps_map_foam(uniform const bool reflections, VS_OUTPUT_MAP_WATER In) 
{ 
	PS_OUTPUT Output;
	Output.RGBColor =  In.Color;

	
			
	float3 WorldPosition = In.PosWater.xyz;
	if ((WorldPosition.x < -125))
	{
	In.Tex0 *=0.75;
	In.Tex0 = rotatevector(In.Tex0.xy,225);
	In.Tex0.y -= (0.05*time_var);
	}
	
	else if ((WorldPosition.y > 273) && (WorldPosition.x < -75))
	{
	In.Tex0 *=0.75;
	In.Tex0 = 1-In.Tex0;
	In.Tex0.y -= (0.05*time_var);
	}
	else if ((WorldPosition.y > 213) && (WorldPosition.x > -75))
	{
	In.Tex0 *=0.75;
	In.Tex0.y -= (0.05*time_var);
	}
	else if ((WorldPosition.x > -125) && (WorldPosition.x < -50))
	{
	In.Tex0 *=0.75;
	In.Tex0 = rotatevector(In.Tex0.xy,90);
	In.Tex0.y -= (0.05*time_var);
	}
	else if ((WorldPosition.y < 213) && (WorldPosition.x > -50))
	{
	In.Tex0 *=0.75;
	In.Tex0 = rotatevector(In.Tex0.xy,270);
	In.Tex0.y -= (0.05*time_var);
	}
	else
	{
	In.Tex0.y -= (0.05*time_var);
	}
	float4 tex_col = tex2D(MeshTextureSampler, In.Tex0);
	INPUT_TEX_GAMMA(tex_col.rgb);
	
	/////////////////////
	float3 normal;
	normal.xy = (2.0f * tex2D(NormalTextureSampler, In.Tex0 * 8).ag - 1.0f);
	normal.z = sqrt(1.0f - dot(normal.xy, normal.xy));
	
	float NdotL = saturate( dot(normal, In.LightDir) );
	float3 vView = normalize(In.CameraDir);

	// Fresnel term
	float fresnel = 1-(saturate(dot(vView, normal)));
	fresnel = 0.0204f + 0.9796 * (fresnel * fresnel * fresnel * fresnel * fresnel);
	Output.RGBColor.rgb += fresnel * In.Color.rgb;
	/////////////////////


	Output.RGBColor.rgb *= tex_col.rgb;

    Output.RGBColor.rgb *= 0.8;
	OUTPUT_GAMMA(Output.RGBColor.rgb);	//0.5 * normal + 0.5; //
	//Output.RGBColor.rgb = In.Color.rgb;
	
	Output.RGBColor.a = In.Color.a * tex_col.a;
	
	/*
	if ((WorldPosition.x < -146) && (WorldPosition.x > -255) && (WorldPosition.y < 235) && (WorldPosition.y > 188))
		{
	Output.RGBColor.rgb = float3(1.8,0.2,0.2);
		}
	else if (WorldPosition.x > -146)
	{
	Output.RGBColor.rgb = float3(0.2,1.8,0.2);
	}
	*/
	
	
	
	return Output;
}

technique map_water
{
	pass P0
	{
		VertexShader = compile vs_2_0 vs_map_water(false);
		PixelShader = compile ps_2_0 ps_map_water(false);
	}
}
technique map_water_high
{
	pass P0
	{
		VertexShader = compile vs_2_0 vs_map_water(true);
		PixelShader = compile ps_2_0 ps_map_water(true);
	}
}

technique map_foam
{
	pass P0
	{
		VertexShader = compile vs_3_0 vs_map_foam(true);
		PixelShader = compile ps_3_0 ps_map_foam(true);
	}
}


//LAGRANDMASTERS NEW MAP WATER SHADERS
struct VS_OUTPUT_MAP_WATER_NEWb
{
	float4 Pos          : POSITION;
	float2 Tex0         : TEXCOORD0;
	float4 LightDir_Alpha	: TEXCOORD1;//light direction for bump
	float4 LightDif		: TEXCOORD2;//light diffuse for bump
	float4 CameraDir	: TEXCOORD3;//camera direction for bump
	float4 PosWater		: TEXCOORD4;//position according to the water camera
	float  Fog          : FOG;
	
	float4 projCoord 	: TEXCOORD5;
	float  Depth    	: TEXCOORD6; 
	float3 WaveDiff		: TEXCOORD7;
};
/////////////////////////////


struct VS_OUTPUT_MAP_WATER_NEW
{
	float4 Pos           : POSITION;
	float4 Color	     : COLOR0;
	float2 Tex0          : TEXCOORD0;
	//float3 LightDir		 : TEXCOORD1;//light direction for bump
	float3 CameraDir	 : TEXCOORD3;//camera direction for bump
	float4 PosWater		 : TEXCOORD4;//position according to the water camera
	float  Fog           : FOG;
	
	float4 projCoord 	: TEXCOORD5;
	float2  Depth    	: TEXCOORD6; 
	
	float4 LightDir_Alpha	: TEXCOORD1;//light direction for bump
	float4 LightDif		: TEXCOORD2;//light diffuse for bump
	
};



	
VS_OUTPUT_MAP_WATER_NEW vs_map_water_new (uniform const bool reflections, float4 vPosition : POSITION, float3 vNormal : NORMAL, float3 vTangent : TANGENT, float3 vBinormal : BINORMAL, float2 tc : TEXCOORD0, float4 vColor : COLOR0, float4 vLightColor : COLOR1)
{
	INITIALIZE_OUTPUT(VS_OUTPUT_MAP_WATER_NEW, Out);

	float4 vWorldPosNoMove = (float4)mul(matWorld,vPosition);
	
	
	float2 Amplitude = float2(0.07,0.08);
	float2 Period = float2(20,13);
	float2 WorldPosition = float2(tc.x,tc.y);//float2((matWorldViewProj,vPosition.x),(matWorldViewProj,vPosition.y));
	
	if (vPosition.z < 0.7)
	{
	vPosition.z = vPosition.z + Amplitude.x * sin(Period.x *  WorldPosition.x + time_var); //
	vPosition.z = vPosition.z + Amplitude.y * sin(Period.y *  WorldPosition.y + time_var); //
	 }
	Out.Pos = mul(matWorldViewProj, vPosition);

	float4 vWorldPos = (float4)mul(matWorld,vPosition);
	
	//parallax
	float3 vWorldN = normalize(mul((float3x3)matWorld, vNormal)); //normal in world space
	float3 vWorld_binormal = normalize(mul((float3x3)matWorld, vBinormal)); //normal in world space
	float3 vWorld_tangent  = normalize(mul((float3x3)matWorld, vTangent)); //normal in world space
	float3x3 TBNMatrix = float3x3(vWorld_tangent, vWorld_binormal, vWorldN); 
	
	
	//float3 vWorldN = normalize(mul((float3x3)matWorld, vNormal)); //normal in world space

	float3 P = mul(matWorldView, vPosition); //position in view space

	Out.Tex0 = 0.065*float2(vWorldPos.x,vWorldPos.y);
    Out.Tex0.y *= 0.75;

	float4 diffuse_light = vAmbientColor + vLightColor;

	//directional lights, compute diffuse color
	diffuse_light += saturate(dot(vWorldN, -vSkyLightDir)) * vSkyLightColor;

	float wNdotSun = max(-0.0001f,dot(vWorldN, -vSunDir));
	diffuse_light += (wNdotSun) * vSunColor;

	//apply material color
	//	Out.Color = min(1, vMaterialColor * vColor * diffuse_light);
	Out.Color = (vMaterialColor * vColor) * diffuse_light;
	Out.Color.w = vWorldPosNoMove.z;
	
	//if(reflections)
	{
		float4 water_pos = mul(matWaterViewProj, vWorldPos);
		Out.PosWater.xy = (float2(water_pos.x, -water_pos.y)+water_pos.w)/2;
		Out.PosWater.xy += (vDepthRT_HalfPixel_ViewportSizeInv.xy * water_pos.w);
		Out.PosWater.zw = water_pos.zw;
	}
	Out.PosWater = mul(matWaterWorldViewProj, vPosition);
	{

	
		float3 point_to_camera_normal = normalize(vCameraPos.xyz - vWorldPos.xyz);
		Out.CameraDir = mul(TBNMatrix, point_to_camera_normal);
	//	Out.LightDir = mul(TBNMatrix, -vSunDir);
	}

	    Out.projCoord.xy = (float2(Out.Pos.x, -Out.Pos.y)+Out.Pos.w)/2;
		Out.projCoord.xy += (vDepthRT_HalfPixel_ViewportSizeInv.xy * Out.Pos.w);
		Out.projCoord.zw = Out.Pos.zw;
		Out.Depth.x = Out.Pos.z * far_clip_Inv;
		
		
	Out.LightDif = 0; //vAmbientColor;
	float totalLightPower = 0;

	//directional lights, compute diffuse color
	Out.LightDir_Alpha.xyz = mul(TBNMatrix, -vSunDir);
	Out.LightDif += vSunColor * vColor;
	totalLightPower += length(vSunColor.xyz);
	
	Out.LightDir_Alpha.a = vColor.a;
		
	float3 view_vec = (vCameraPos.xyz - vWorldPos.xyz);
	Out.Depth.y = length(view_vec);
		
		

	//apply fog
	float d = length(P);
	Out.Fog = get_fog_amount_new(d, vWorldPos.z);
	
	return Out;
}




	






PS_OUTPUT ps_map_water_new(uniform const bool reflections, VS_OUTPUT_MAP_WATER_NEW In) 
{ 
	PS_OUTPUT Output;
	Output.RGBColor =  0.25*In.Color;

	In.Tex0 *= 1.5;
	
	float time_variable = 0.2*time_var;//Timer;//
	float2 TexOffsetA =In.Tex0;
	float2 TexOffsetB =In.Tex0;
	
	
	
//PARALLAX SECTION
	float3 viewVec = normalize(In.CameraDir);
	{
     float factor = (0.01f * vSpecularColor.x);
     float volume = (factor * 1.4);//0.04;
     float bias = (factor * -0.7f);//-0.02; 

	//PARALLAX TEX A
	TexOffsetA = float2(In.Tex0.x + (0.25*time_variable),In.Tex0.y );
	float height = tex2D(Diffuse2Sampler, TexOffsetA).a;
	//height *= sin(0.5*time_var + 10*In.Tex0.x);
	float offset = height * volume + bias;
	
	//PARALLAX TEX B
	TexOffsetB = float2(In.Tex0.x,In.Tex0.y + (0.15*time_variable));
	float heightB = tex2D(Diffuse2Sampler, TexOffsetB).a;
	//height *= sin(0.5*time_var + 10*In.Tex0.x);
	float offsetB = heightB * volume + bias;
	
	//APPLY PARALLAX TO TEXCOORDS
	In.Tex0 += offset * (viewVec.xy);
	In.Tex0 += offsetB * (viewVec.xy);
	}
//PARALLAX END
	

//NORMAL CALCULATED (USING PARALLAXED TEX COORDS)
	float3 normal;
	float3 normal2;
   //Normalmap A
		TexOffsetA = float2(In.Tex0.x + (0.25*time_variable),In.Tex0.y );
		normal.xy = (2.0f * tex2D(NormalTextureSampler, TexOffsetA).ag - 1.0f);
		normal.z = sqrt(1.0f - dot(normal.xy, normal.xy));
		
		
		TexOffsetB = float2(In.Tex0.x,In.Tex0.y + (0.15*time_variable));
		normal2.xy = (2.0f * tex2D(NormalTextureSampler, TexOffsetB).ag - 1.0f);
		normal2.z = sqrt(1.0f - dot(normal2.xy, normal2.xy));
		
	normal = lerp(normal,normal2,0.5);
//END NORMAL CALCULATIONS	
	
	
	float dist = In.Depth.y;
	dist = saturate(dist*0.0075);
    
//Lihting	
	float NdotL = saturate(dot(normal, In.LightDir_Alpha.xyz));

	Output.RGBColor = 0.01f * NdotL * In.LightDif;
	
	float3 vView = normalize(In.CameraDir);
	float2 reflectcoords = (0.25f * normal.xy) + float2(0.5f + 0.5f * (In.PosWater.x / In.PosWater.w), 0.5f - 0.5f * (In.PosWater.y / In.PosWater.w));
	float4	tex = tex2D(ReflectionTextureSampler,reflectcoords);
	INPUT_OUTPUT_GAMMA(tex.rgb);

	
	float fresnel = 1-(saturate(dot(vView, normal)));
	fresnel = 0.0204f + 0.9796 * (fresnel * fresnel * fresnel * fresnel * fresnel);
	float3 RefColor = saturate((tex.rgb * fresnel));
		
	float coastheight = saturate((In.Color.w - 0.361)*2);
    float3 coastproximity = saturate(min(pow(coastheight+0.23,2.3),coastheight));
    //RefColor *= saturate(0.8-coastproximity);
	
	Output.RGBColor.a = 1.0f - 0.3f * In.CameraDir.z;
	float vertex_alpha = In.LightDir_Alpha.a;
	Output.RGBColor.a *= vertex_alpha;
	
//Diffuse Colouring
	float3 cWaterColor = 5*float3(1.0f/255.0f, 5.0f/255.0f, 10.0f/255.0f);
	
	float3 WaterColorLightDark = lerp(cWaterColor*0.5,cWaterColor*1.2, 1-(tex2D(Diffuse2Sampler, TexOffsetA).a));//saturate(dot(vView, normal)));
	cWaterColor = lerp(WaterColorLightDark,cWaterColor,dist);//make ligth dark only when close
	
	float fresnel2 = 1-saturate(dot(In.CameraDir, normal));
	fresnel2 *= max(0.25,In.Color);
	cWaterColor = cWaterColor * fresnel2;

	
   float fog_fresnel_factor = saturate(dot(In.CameraDir, normal));
	float3 DifColor = cWaterColor;//(2*cWaterColor) * fresnel;
	
//IMPLEMENTING COLOURING AND LIGHTING (more reflections when zoomed out)
	

	if (In.CameraDir.z > 0.5)
	{
	Output.RGBColor.rgb += lerp((DifColor+RefColor),(12.0*DifColor+5.0*RefColor),In.CameraDir.z -0.5);
   }
   else
   {
   Output.RGBColor.rgb += (DifColor+RefColor);
   }
   

	//implement foam coords
    float2 FoamOffset = float2(2*In.Tex0.x,2*In.Tex0.y - (0.1*time_variable));


	
//OCEAN FLOOR PARALLAX SECTION
	float2 oceanfloorcord = In.Tex0;
	float3 viewVecOceanFloor = normalize(In.CameraDir);
	{
     float factor = (0.01f * vSpecularColor.x);
     float volume = (factor * 20.0);//0.04;
     float bias = (factor * -10.0);//-0.02; 

	//PARALLAX TEX A
	float height = 1-(0.5*coastheight);//tex2D(Diffuse2Sampler, TexOffsetA).a;
	float offset = height * volume + bias;
	
	//APPLY PARALLAX TO TEXCOORDS
	In.Tex0.y *= 1.333;
	oceanfloorcord = In.Tex0 - offset * viewVecOceanFloor.xy;
	oceanfloorcord *=2;
	
		if (coastheight > 0.08)
		{
			float3 oceanfloorstrong = 0.5*(coastheight-0.08)*(tex2D(SpecularTextureSampler,oceanfloorcord).rgb);
			float3 oceanfloorweak = 0.17*(coastheight-0.08)*(tex2D(SpecularTextureSampler,oceanfloorcord).rgb);
			oceanfloorstrong*= max(0.25,In.Color);
			oceanfloorweak*= max(0.25,In.Color);

			Output.RGBColor.rgb = lerp(Output.RGBColor.rgb +oceanfloorstrong,Output.RGBColor.rgb +oceanfloorweak,saturate(dist*1.8));//min(dist,0.85));
		
		//caustics
		float3 caustics = 0.5*saturate((coastheight-0.08)*(float3(0.0,0.0,0.0) +(tex2D(SpecularTextureSampler,(0.4*oceanfloorcord)+0.075*time_var).a)));
		caustics += 0.5*saturate((coastheight-0.08)*(float3(0.0,0.0,0.0) +(tex2D(SpecularTextureSampler,float2((0.4*oceanfloorcord.x)-0.08*time_var,(0.4*oceanfloorcord.x)-0.089*time_var)).a)));
		caustics *=0.5;
		caustics *= float3 (0.2,0.2,1.0);
		caustics*= max(0.25,In.Color);
		Output.RGBColor.rgb = lerp(Output.RGBColor.rgb+0.95*caustics,Output.RGBColor.rgb+0.25*caustics,saturate(dist*1.5));//min(dist,0.85));
		
		//foam
		float3 FoamColor = saturate(float3(0,0,0)+0.4*((coastheight-0.08)* pow(tex2D(MeshTextureSampler, FoamOffset).a,2)));
		FoamColor*= max(0.25,In.Color);
		Output.RGBColor.rgb = lerp(Output.RGBColor.rgb+0.95*FoamColor,Output.RGBColor.rgb+0.10*FoamColor,saturate(dist*2));//min(dist,0.85));
		
		
		}
	}

	Output.RGBColor.a = 1;			
	OUTPUT_GAMMA(Output.RGBColor.rgb);
	Output.RGBColor.a = saturate(Output.RGBColor.a);


	return Output;
}



VS_OUTPUT_MAP_WATER_NEW vs_map_water_river_new (uniform const bool reflections, float4 vPosition : POSITION, float3 vNormal : NORMAL, float3 vTangent : TANGENT, float3 vBinormal : BINORMAL, float2 tc : TEXCOORD0, float4 vColor : COLOR0, float4 vLightColor : COLOR1)
{
	INITIALIZE_OUTPUT(VS_OUTPUT_MAP_WATER_NEW, Out);

	
	float2 Amplitude = float2(0.2,1);
	float2 Period = float2(20,10);
	float2 WorldPosition = float2(tc.x,tc.y);//float2((matWorldViewProj,vPosition.x),(matWorldViewProj,vPosition.y));
	
	if (vPosition.z < 0.95)
	{
	vPosition.z = vPosition.z + Amplitude.x * sin(Period.x *  WorldPosition.x + time_var); //
	}
	vPosition.z = vPosition.z -5.5;
	 
	Out.Pos = mul(matWorldViewProj, vPosition);

	float4 vWorldPos = (float4)mul(matWorld,vPosition);
	
	//parallax
	float3 vWorldN = normalize(mul((float3x3)matWorld, vNormal)); //normal in world space
	float3 vWorld_binormal = normalize(mul((float3x3)matWorld, vBinormal)); //normal in world space
	float3 vWorld_tangent  = normalize(mul((float3x3)matWorld, vTangent)); //normal in world space
	float3x3 TBNMatrix = float3x3(vWorld_tangent, vWorld_binormal, vWorldN); 
	
	
	//float3 vWorldN = normalize(mul((float3x3)matWorld, vNormal)); //normal in world space

	float3 P = mul(matWorldView, vPosition); //position in view space

	Out.Tex0 = 0.065*float2(vWorldPos.x,vWorldPos.y);
    Out.Tex0.y *= 0.75;

	float4 diffuse_light = vAmbientColor + vLightColor;

	//directional lights, compute diffuse color
	diffuse_light += saturate(dot(vWorldN, -vSkyLightDir)) * vSkyLightColor;

	float wNdotSun = max(-0.0001f,dot(vWorldN, -vSunDir));
	diffuse_light += (wNdotSun) * vSunColor;

	//apply material color
	//	Out.Color = min(1, vMaterialColor * vColor * diffuse_light);
	Out.Color = (vMaterialColor * vColor) * diffuse_light;
	
	
	//if(reflections)
	{
		float4 water_pos = mul(matWaterViewProj, vWorldPos);
		Out.PosWater.xy = (float2(water_pos.x, -water_pos.y)+water_pos.w)/2;
		Out.PosWater.xy += (vDepthRT_HalfPixel_ViewportSizeInv.xy * water_pos.w);
		Out.PosWater.zw = water_pos.zw;
	}
	Out.PosWater = mul(matWaterWorldViewProj, vPosition);
	{


		float3 point_to_camera_normal = normalize(vCameraPos.xyz - vWorldPos.xyz);
		Out.CameraDir = mul(TBNMatrix, -point_to_camera_normal);
	//	Out.LightDir = mul(TBNMatrix, -vSunDir);
	}

	    Out.projCoord.xy = (float2(Out.Pos.x, -Out.Pos.y)+Out.Pos.w)/2;
		Out.projCoord.xy += (vDepthRT_HalfPixel_ViewportSizeInv.xy * Out.Pos.w);
		Out.projCoord.zw = Out.Pos.zw;
		Out.Depth.x = Out.Pos.z * far_clip_Inv;
		
		
	Out.LightDif = 0; //vAmbientColor;
	float totalLightPower = 0;

	//directional lights, compute diffuse color
	Out.LightDir_Alpha.xyz = mul(TBNMatrix, -vSunDir);
	Out.LightDif += vSunColor * vColor;
	totalLightPower += length(vSunColor.xyz);
	
	Out.LightDir_Alpha.a = vColor.a;
		
	float3 view_vec = (vCameraPos.xyz - vWorldPos.xyz);
	Out.Depth.y = length(view_vec);
		
		

	//apply fog
	float d = length(P);
	Out.Fog = get_fog_amount_new(d, vWorldPos.z);
	
	return Out;
}




PS_OUTPUT ps_map_water_river_new(uniform const bool reflections, VS_OUTPUT_MAP_WATER_NEW In) 
{ 
	PS_OUTPUT Output;
	In.Color *= 0.5;
	Output.RGBColor =  0.25*In.Color;

	
	float time_variable = 0.2*time_var;//Timer;//
	float2 TexOffsetA =In.Tex0;
	float2 TexOffsetB =In.Tex0;
	
	
	
//PARALLAX SECTION
	float3 viewVec = normalize(In.CameraDir);
	{
     float factor = (0.01f * vSpecularColor.x);
     float volume = (factor * 1.0);//0.04;
     float bias = (factor * -0.5f);//-0.02; 

	//PARALLAX TEX A
	TexOffsetA = float2(In.Tex0.x,In.Tex0.y + (0.1*time_variable));
	float height = tex2D(Diffuse2Sampler, TexOffsetA).a;
	//height *= sin(0.5*time_var + 10*In.Tex0.x);
	float offset = height * volume + bias;
	
	//APPLY PARALLAX TO TEXCOORDS
	In.Tex0 += offset * viewVec.xy;
	//In.PosWater.xy += offset * viewVec.xy;
	}
//PARALLAX END
	

//NORMAL CALCULATED (USING PARALLAXED TEX COORDS)
	float3 normal;
	float3 normal2;
   //Normalmap A
		TexOffsetA = float2(In.Tex0.x,In.Tex0.y + (0.1*time_variable));
		normal.xy = (2.0f * tex2D(NormalTextureSampler, TexOffsetA).ag - 1.0f);
		normal.z = sqrt(1.0f - dot(normal.xy, normal.xy));
//END NORMAL CALCULATIONS	
	
	
	
//Lihting	
	float NdotL = saturate(dot(normal, In.LightDir_Alpha.xyz));

	//float NdotL = saturate( dot(normal, In.LightDir) );
	Output.RGBColor = 0.01f * NdotL * In.LightDif;
	
	float3 vView = normalize(In.CameraDir);
	float2 reflectcoords = (0.25f * normal.xy) + float2(0.5f + 0.5f * (In.PosWater.x / In.PosWater.w), 0.5f - 0.5f * (In.PosWater.y / In.PosWater.w));
	float4	tex = tex2D(ReflectionTextureSampler,reflectcoords);
	INPUT_OUTPUT_GAMMA(tex.rgb);

	
	float fresnel = 1-(saturate(dot(vView, normal)));
	fresnel = 0.0204f + 0.9796 * (fresnel * fresnel * fresnel * fresnel * fresnel);
	float3 RefColor = saturate((0.5*(tex.rgb * fresnel)));
		
    float3 coastproximity = saturate(min(pow(In.Color+0.23,2.3),In.Color));
    RefColor *= saturate(0.8-coastproximity);
	
	Output.RGBColor.a = 1.0f - 0.3f * In.CameraDir.z;
	float vertex_alpha = In.LightDir_Alpha.a;
	Output.RGBColor.a *= vertex_alpha;
	
//Diffuse Colouring
	const float3 g_cDownWaterColor = lerp(float3(4.5f/255.0f, 8.0f/255.0f, 6.0f/255.0f),float3(1.0f/255.0f, 4.0f/255.0f, 6.0f/255.0f),(1-In.Color));
	const float3 g_cUpWaterColor   = lerp(float3(5.0f/255.0f, 7.0f/255.0f, 7.0f/255.0f),float3(1.0f/255.0f, 5.0f/255.0f, 10.0f/255.0f),(1-In.Color));
	float3 cWaterColor = lerp( g_cUpWaterColor, g_cDownWaterColor, 1- (tex2D(Diffuse2Sampler, TexOffsetA).a));//saturate(dot(vView, normal)));

	float dist = In.Depth.y;
	dist = saturate(dist*0.0075);
	cWaterColor = lerp(cWaterColor, g_cUpWaterColor, dist);//saturate(dot(vView, normal)));
	
	
	
   float fog_fresnel_factor = saturate(dot(In.CameraDir, normal));
	cWaterColor *= 3;
	fog_fresnel_factor *= fog_fresnel_factor;
	fog_fresnel_factor *= fog_fresnel_factor;
	float3 DifColor = cWaterColor * saturate(0.5*fog_fresnel_factor);
	DifColor = (2*cWaterColor) * fresnel;
	
//IMPLEMENTING COLOURING AND LIGHTING (less reflections when zoomed out)
	//float dist = In.Depth.y;
	//dist = saturate(dist*0.0075);
    Output.RGBColor.rgb += lerp((DifColor+0.65*RefColor),(DifColor+0.45*RefColor),dist);
   
   
   
   //implement foam
    float2 FoamTexCo = float2((In.Tex0.x + 0.10*sin(2*In.Tex0.y)),(In.Tex0.y+ 0.10*sin(2.4*In.Tex0.y)));
	float2 FoamOffset = float2(In.Tex0.x,In.Tex0.y - (0.1*time_variable));
	float foam = tex2D(MeshTextureSampler, FoamOffset).a;
	float3 FoamColor = lerp(Output.RGBColor.rgb,Output.RGBColor.rgb+foam,saturate(pow(In.Color+0.25,2))); //lerp so more foam near coasts (In.Color)
	Output.RGBColor.rgb = lerp(FoamColor,Output.RGBColor.rgb,min(dist,0.85));//lerp so more foam less visible when far zoomed out
	//
/////
	

	
	
////


	//PERHAPS SINE THE TEX COORDS SO THAT THEY ARE NOT SO REPETITIVE
	//NEXT MOVE ON TO DENMARK?UK? THEN LASTLY USE THORGGRIMS TO SCULPT BEACHES ECT
	
	
//OCEAN FLOOR PARALLAX SECTION
	float2 oceanfloorcord = In.Tex0;
	float3 viewVecOceanFloor = normalize(In.CameraDir);
	{
     float factor = (0.01f * vSpecularColor.x);
     float volume = (factor * 15.0);//0.04;
     float bias = (factor * -12.5f);//-0.02; 

	//PARALLAX TEX A
	float height = 1;//tex2D(Diffuse2Sampler, TexOffsetA).a;
	//height *= sin(0.5*time_var + 10*In.Tex0.x);
	float offset = height * volume + bias;
	
	//APPLY PARALLAX TO TEXCOORDS
	In.Tex0.y *= 1.333;
	oceanfloorcord = In.Tex0 - offset * viewVecOceanFloor.xy;
	
		if (In.Color.r > 0.08)
		{
		Output.RGBColor.rgb += (In.Color.r-0.08)*(tex2D(SpecularTextureSampler,oceanfloorcord));
		//extra foam
		Output.RGBColor.rgb += 0.15*((In.Color.r-0.08)* tex2D(MeshTextureSampler, FoamOffset).a);
		}
	}
	

//OCEAN FLOOR PARALLAX END
  // Output.RGBColor.rgb = lerp(Output.RGBColor.rgb,Output.RGBColor.rgb*In.LightDif.rgb,0.5);

    Output.RGBColor.rgb = saturate(Output.RGBColor.rgb);
	 Output.RGBColor.rgb = lerp(Output.RGBColor.rgb,Output.RGBColor.rgb*In.LightDif.rgb,0.75);

Output.RGBColor.g *= 0.95;
	Output.RGBColor.a = 1;			
	OUTPUT_GAMMA(Output.RGBColor.rgb);
	Output.RGBColor.a = saturate(Output.RGBColor.a);


	return Output;
}




technique map_water_new
{
	pass P0
	{
		VertexShader = compile vs_3_0 vs_map_water_new(true);
		PixelShader = compile ps_3_0 ps_map_water_new(true);
	}
}
technique map_water_new_high
{
	pass P0
	{
		VertexShader = compile vs_3_0 vs_map_water_new(true);
		PixelShader = compile ps_3_0 ps_map_water_new(true);
	}
}




technique map_water_river_new
{
	pass P0
	{
		VertexShader = compile vs_3_0 vs_map_water_new(true);
		PixelShader = compile ps_3_0 ps_map_water_new(true);
	}
}
technique map_water_river_new_high
{		
	pass P0
	{
		VertexShader = compile vs_3_0 vs_map_water_new(true);
		PixelShader = compile ps_3_0 ps_map_water_new(true);
	}
}

#endif

/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#ifdef SOFT_PARTICLE_SHADERS
struct VS_DEPTHED_FLARE
{
	float4 Pos					: POSITION;
	float4 Color				: COLOR0;
	float2 Tex0					: TEXCOORD0;
	float  Fog				    : FOG;
	
	float4 projCoord			: TEXCOORD1;
	float  Depth				: TEXCOORD2;
};

VS_DEPTHED_FLARE vs_main_depthed_flare(float4 vPosition : POSITION, float4 vColor : COLOR, float2 tc : TEXCOORD0)
{
	VS_DEPTHED_FLARE Out;

	Out.Pos = mul(matWorldViewProj, vPosition);


	Out.Tex0 = tc;
	Out.Color = vColor * vMaterialColor;
	
	
	if(use_depth_effects) {
		Out.projCoord.xy = (float2(Out.Pos.x, -Out.Pos.y)+Out.Pos.w)/2;
		Out.projCoord.xy += (vDepthRT_HalfPixel_ViewportSizeInv.xy * Out.Pos.w);
		Out.projCoord.zw = Out.Pos.zw;
		Out.Depth = Out.Pos.z * far_clip_Inv;
	}

	//apply fog
	float3 P = mul(matWorldView, vPosition); //position in view space
	float4 vWorldPos = (float4)mul(matWorld,vPosition);
	float d = length(P);
	Out.Fog = get_fog_amount_new(d, vWorldPos.z);

	return Out;
}

PS_OUTPUT ps_main_depthed_flare(VS_DEPTHED_FLARE In, uniform const bool sun_like, uniform const bool blend_adding) 
{ 
	PS_OUTPUT Output;
	Output.RGBColor =  In.Color;
	Output.RGBColor *= tex2D(MeshTextureSampler, In.Tex0);

	if(!blend_adding) {
		//this shader replaces "ps_main_no_shadow" which uses gamma correction..
		OUTPUT_GAMMA(Output.RGBColor.rgb);
	}
	
	if(use_depth_effects) {	//add volume to in.depth?
		float depth = tex2Dproj(DepthTextureSampler, In.projCoord).r;
		
		float alpha_factor;
		
		if(sun_like) {
			float my_depth = 0;	//STR?: wignette like volume? tc!
			alpha_factor = depth;
			float fog_factor = 1.001f - (10.f * (fFogDensity+0.001f));	//0.1 -> 0.0  & 0.01 -> 1.0
			alpha_factor *= fog_factor;
		}
		else {
			alpha_factor = saturate((depth-In.Depth) * 4096); 
		}
		
		if(blend_adding)  {
			Output.RGBColor *= alpha_factor;	//pre-multiplied alpha
		}
		else  {
			Output.RGBColor.a *= alpha_factor;
		}
	}
	
	//Output.RGBColor.rgb = float3(0.8,0,0);
	//Output.RGBColor.w = 1;
	
	return Output;
}


VertexShader vs_main_depthed_flare_compiled = compile vs_2_0 vs_main_depthed_flare();

technique soft_sunflare
{
	pass P0
	{
		VertexShader = vs_main_depthed_flare_compiled;
		PixelShader = compile ps_2_0 ps_main_depthed_flare(true,true);
	}
}


technique soft_particle_add
{
	pass P0
	{
		VertexShader = vs_main_depthed_flare_compiled;
		PixelShader = compile ps_2_0 ps_main_depthed_flare(false,true);
	}
}

technique soft_particle_modulate
{
	pass P0
	{
		VertexShader = vs_main_depthed_flare_compiled;
		PixelShader = compile ps_2_0 ps_main_depthed_flare(false,false);
	}
}
#endif

/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#ifdef OCEAN_SHADERS

struct VS_OUTPUT_OCEAN
{
	float4 Pos          : POSITION;
	float2 Tex0         : TEXCOORD0;
	float3 LightDir		: TEXCOORD1;
	float4 LightDif		: TEXCOORD2;//light diffuse for bump
	float3 CameraDir	: TEXCOORD3;
	float4 PosWater		: TEXCOORD4;//position according to the water camera
	
	float  Fog          : FOG;
};

inline float get_wave_height_temp(const float pos[2], const float coef, const float freq1, const float freq2, const float time)
{
	return coef * sin( (pos[0]+pos[1]) * freq1 + time) * cos( (pos[0]-pos[1]) * freq2 + (time+4));// + (coef * 0.05 * sin( (pos[0]*pos[1]) * (freq1 * 200 * time) + time));
}
VS_OUTPUT_OCEAN vs_main_ocean(float4 vPosition : POSITION, float2 tc : TEXCOORD0)
{
	VS_OUTPUT_OCEAN Out = (VS_OUTPUT_OCEAN) 0;

	float4 vWorldPos = mul(matWorld,vPosition);
	
	float3 viewVec = vCameraPos.xyz - vWorldPos.xyz;
	float wave_distance_factor = (1.0f - saturate(length(viewVec) * 0.01));	//no wave after 100 meters
	
	float pos_vector[2] = {vWorldPos.x, vWorldPos.y};
	vWorldPos.z += get_wave_height_temp(pos_vector, debug_vector.z, debug_vector.x, debug_vector.y, time_var) * wave_distance_factor; 

	Out.Pos = mul(matViewProj, vWorldPos);
	
	Out.PosWater = mul(matWaterViewProj, vWorldPos);

	
	//calculate new normal:
	float3 vNormal;
	if(wave_distance_factor > 0.0f)
	{
		float3 near_wave_heights[2];
		near_wave_heights[0].xy = vWorldPos.xy + float2(0.1f, 0.0f);
		near_wave_heights[1].xy = vWorldPos.xy + float2(0.0f, 1.0f);
		
		float pos_vector0[2] = {near_wave_heights[0].x, near_wave_heights[0].y};
		near_wave_heights[0].z = get_wave_height_temp(pos_vector0, debug_vector.z, debug_vector.x, debug_vector.y, time_var);
		float pos_vector1[2] = {near_wave_heights[1].x, near_wave_heights[1].y};
		near_wave_heights[1].z = get_wave_height_temp(pos_vector1, debug_vector.z, debug_vector.x, debug_vector.y, time_var);
		
		float3 v0 = normalize(near_wave_heights[0] - vWorldPos.xyz);
		float3 v1 = normalize(near_wave_heights[1] - vWorldPos.xyz);
		
		vNormal = cross(v0,v1);
	}
	else 
	{
		vNormal = float3(0,0,1);
	}
	
	
	float3 vWorldN = vNormal; //float3(0,0,1); //normalize(mul((float3x3)matWorld, vNormal)); //normal in world space
	float3 vWorld_tangent  = float3(1,0,0); //normalize(mul((float3x3)matWorld, vTangent)); //normal in world space
	float3 vWorld_binormal = normalize(cross(vWorld_tangent, vNormal)); //float3(0,1,0); //normalize(mul((float3x3)matWorld, vBinormal)); //normal in world space

	float3x3 TBNMatrix = float3x3(vWorld_tangent, vWorld_binormal, vWorldN); 

	float3 point_to_camera_normal = normalize(vCameraPos.xyz - vWorldPos.xyz);
	Out.CameraDir = mul(TBNMatrix, point_to_camera_normal);

	Out.Tex0 = vWorldPos.xy; //tc + texture_offset.xy;	

	Out.LightDir = 0;
	Out.LightDif = vAmbientColor;

	//directional lights, compute diffuse color
	Out.LightDir += mul(TBNMatrix, -vSunDir);
	Out.LightDif += vSunColor;
	Out.LightDir = normalize(Out.LightDir);

	//apply fog
	float3 P = mul(matWorldView, vPosition); //position in view space
	float d = length(P);
	Out.Fog = get_fog_amount_new(d, vWorldPos.z);
	
	
	//Out.PosWater.xyz = vNormal;
	
	return Out;
}
PS_OUTPUT ps_main_ocean( VS_OUTPUT_OCEAN In )
{ 
	PS_OUTPUT Output;
	
	const float texture_factor = 1.0f;
	
	float3 normal;
	normal.xy = (2.0f * tex2D(NormalTextureSampler, In.Tex0 * texture_factor).ag - 1.0f);
	normal.z = sqrt(1.0f - dot(normal.xy, normal.xy));
	
	
	static const float detail_factor = 16 * texture_factor;
	float3 detail_normal;
	detail_normal.xy = (2.0f * tex2D(NormalTextureSampler, In.Tex0 * detail_factor).ag - 1.0f);
	detail_normal.z = sqrt(1.0f - dot(normal.xy, normal.xy));
	
	float NdotL = saturate(dot(normal, In.LightDir));
	
	
	float4 tex = tex2D(ReflectionTextureSampler, 0.5f * normal.xy + float2(0.5f + 0.5f * (In.PosWater.x / In.PosWater.w), 0.5f - 0.5f * (In.PosWater.y / In.PosWater.w)));
	INPUT_OUTPUT_GAMMA(tex.rgb);
	
	Output.RGBColor = 0.01f * NdotL * In.LightDif;
	
	float3 vView = normalize(In.CameraDir);

	// Fresnel term
	float fresnel = 1-(saturate(dot(vView, normal)));
	fresnel = 0.0204f + 0.9796 * (fresnel * fresnel * fresnel * fresnel * fresnel);

	Output.RGBColor.rgb += (tex.rgb * fresnel);
	Output.RGBColor.w = 1.0f - 0.3f * In.CameraDir.z;
	
	float3 cWaterColor = 2 * float3(20.0f/255.0f, 45.0f/255.0f, 100.0f/255.0f) * vSunColor;
	//float3 cWaterColor = lerp( g_cUpWaterColor, g_cDownWaterColor,  saturate(dot(vView, normal)));
	
	float fog_fresnel_factor = saturate(dot(In.CameraDir, normal));
	fog_fresnel_factor *= fog_fresnel_factor;
	fog_fresnel_factor *= fog_fresnel_factor;
	Output.RGBColor.rgb += cWaterColor * fog_fresnel_factor;
	
	OUTPUT_GAMMA(Output.RGBColor.rgb);
	Output.RGBColor.a = 1;
	
	
	//Output.RGBColor.rgb = dot(In.PosWater.xyz, float3(0,0,1));
	//Output.RGBColor.rgb = NdotL * vSunColor;
	
	return Output;
}
technique simple_ocean
{
	pass P0
	{
		VertexShader = compile vs_2_0 vs_main_ocean();
		PixelShader = compile ps_2_0 ps_main_ocean();
	}
}
#endif

/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#ifdef NEWTREE_SHADERS


VS_OUTPUT_FLORA vs_flora_billboards(uniform const int PcfMode, 
												float4 vPosition : POSITION, 
												float3 vNormal : NORMAL, 
												float2 tc : TEXCOORD0, 
												float4 vColor : COLOR0)
{
	INITIALIZE_OUTPUT(VS_OUTPUT_FLORA, Out);

	float4 vWorldPos = (float4)mul(matWorld,vPosition);
	
	float3 view_vec = (vCameraPos.xyz - vWorldPos.xyz);
	float dist_to_vertex = length(view_vec);
	
	/*if(dist_to_vertex < flora_detail_clip)
	{
		//Out.Pos = float4(0,0,-1,1);	// str: we can just blend but "more vs instruction" generates less pixel to process, so faster
		Out.Color.a = 0.0f;
		//return Out;
	}*/
	
	float alpha_val = saturate(0.5f + ((dist_to_vertex - flora_detail_fade) / flora_detail_fade_inv ));
	 
	
	Out.Pos = mul(matWorldViewProj, vPosition);
	
	float3 vWorldN = normalize(mul((float3x3)matWorld, vNormal)); //normal in world space
	

	Out.Tex0 = tc;

	float4 diffuse_light = vAmbientColor;

	//directional lights, compute diffuse color
	diffuse_light += saturate(dot(vWorldN, -vSkyLightDir)) * vSkyLightColor;

	//point lights
	diffuse_light += calculate_point_lights_diffuse(vWorldPos, vWorldN, false, false);
	
	//apply material color
	Out.Color = (vMaterialColor * vColor * diffuse_light);
	Out.Color.a *= alpha_val;

	//shadow mapping variables
	float wNdotSun = saturate(dot(vWorldN, -vSunDir));
	Out.SunLight = (wNdotSun) * vSunColor * vMaterialColor * vColor;
	if (PcfMode != PCF_NONE)
	{
		float4 ShadowPos = mul(matSunViewProj, vWorldPos);
		Out.ShadowTexCoord = ShadowPos;
		Out.ShadowTexCoord.z /= ShadowPos.w;
		Out.ShadowTexCoord.w = 1.0f;
		Out.ShadowTexelPos = Out.ShadowTexCoord * fShadowMapSize;
		//shadow mapping variables end
	}
	
	//apply fog
	float3 P = mul(matWorldView, vPosition); //position in view space
	float d = length(P);

	Out.Fog = get_fog_amount_new(d, vWorldPos.z);
	return Out;
}


DEFINE_TECHNIQUES(tree_billboards_flora, vs_flora_billboards, ps_flora)

VS_OUTPUT_BUMP vs_main_bump_billboards (uniform const int PcfMode, float4 vPosition : POSITION, float3 vNormal : NORMAL, float2 tc : TEXCOORD0,  float3 vTangent : TANGENT, float3 vBinormal : BINORMAL, float4 vVertexColor : COLOR0, float4 vPointLightDir : COLOR1)
{
	INITIALIZE_OUTPUT(VS_OUTPUT_BUMP, Out);

	float4 vWorldPos = (float4)mul(matWorld,vPosition);
	
	float3 view_vec = (vCameraPos.xyz - vWorldPos.xyz);
	float dist_to_vertex = length(view_vec);
	
	if(dist_to_vertex < flora_detail_clip)
	{
		Out.Pos = float4(0,0,-1,1);	// str: we can just blend but "more vs instruction" generates less pixel to process, so faster
		return Out;
	}
	
	float alpha_val = saturate(0.5f + ((dist_to_vertex - flora_detail_fade) / flora_detail_fade_inv ));
	 

	Out.Pos = mul(matWorldViewProj, vPosition);
	Out.Tex0 = tc;


	float3 vWorldN = normalize(mul((float3x3)matWorld, vNormal)); //normal in world space
	float3 vWorld_binormal = normalize(mul((float3x3)matWorld, vBinormal)); //normal in world space
	float3 vWorld_tangent  = normalize(mul((float3x3)matWorld, vTangent)); //normal in world space

	float3 P = mul(matWorldView, vPosition); //position in view space

	float3x3 TBNMatrix = float3x3(vWorld_tangent, vWorld_binormal, vWorldN); 

	if (PcfMode != PCF_NONE)
	{	
		float4 ShadowPos = mul(matSunViewProj, vWorldPos);
		Out.ShadowTexCoord = ShadowPos;
		Out.ShadowTexCoord.z /= ShadowPos.w;
		Out.ShadowTexCoord.w = 1.0f;
		Out.ShadowTexelPos = Out.ShadowTexCoord * fShadowMapSize;
		//shadow mapping variables end
	}

	Out.SunLightDir = mul(TBNMatrix, -vSunDir);
	Out.SkyLightDir = mul(TBNMatrix, -vSkyLightDir);
	
	#ifdef USE_LIGHTING_PASS
	Out.PointLightDir = vWorldPos;
	#else
	Out.PointLightDir.rgb = 2.0f * vPointLightDir.rgb - 1.0f;
	Out.PointLightDir.a = vPointLightDir.a;
	#endif
	
	Out.VertexColor = vVertexColor;
	Out.VertexColor.a *= alpha_val;
	
	//STR: note that these are not in TBN space.. (used for fresnel only..)
	Out.ViewDir = normalize(vCameraPos.xyz - vWorldPos.xyz); //normalize(mul(TBNMatrix, (vCameraPos.xyz - vWorldPos.xyz) ));	// 
	Out.WorldNormal = vWorldN;

	//apply fog
	float d = length(P);
	Out.Fog = get_fog_amount_new(d, vWorldPos.z);

	return Out;
}

DEFINE_TECHNIQUES(tree_billboards_dot3_alpha, vs_main_bump_billboards, ps_main_bump_simple)


#endif
