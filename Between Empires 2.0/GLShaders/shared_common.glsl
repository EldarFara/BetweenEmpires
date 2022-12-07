
//#define SET_SHADOWCOORD_W_TO_1
//#define USE_ShadowTexelPos_INTERPOLATOR

// Definitions
#define float4 vec4
#define float3 vec3
#define float2 vec2
#define int4 ivec4
#define float2x2 mat2
#define float3x3 mat3
#define float4x4 mat4

#define lerp(in0, in1, in2) mix((in0), (in1), (in2))
#define saturate(in0) clamp((in0), 0.0, 1.0)
#define frac(in0) fract((in0))
//#define mul(in0, in1) (in1 * in0)
#define mul(in0, in1) (in0 * in1)
#define ddx(in0) dFdx((in0))
#define ddy(in0) dFdy((in0))
#define fmod(in0,in1) ((in0) - (in1) * trunc((in0)/(in1)))
#define atan2(in0, in1) atan((in1), (in0))
#define tex2Dgrad texture2DGrad

#define NUM_LIGHTS					4
#define NUM_SIMUL_LIGHTS			4

#define NUM_WORLD_MATRICES			32

#define PCF_NONE					0
#define PCF_DEFAULT					1
#define PCF_NVIDIA					2

#define INCLUDE_VERTEX_LIGHTING
#define VERTEX_LIGHTING_SCALER   1.0	//used for diffuse calculation
#define VERTEX_LIGHTING_SPECULAR_SCALER   1.0
#define USE_NEW_TREE_SYSTEM
#define FLORA_DETAIL_FADE_MUL	0.75
//#define USE_CONSTANT_GAMMA
//#define DISABLE_GPU_SKINNING

// UNIFORMS
uniform sampler2D diffuse_texture;
uniform sampler2D diffuse_texture_2;
uniform sampler2D specular_texture;
uniform sampler2D normal_texture;
uniform sampler2D env_texture;
uniform sampler2D shadowmap_texture;
uniform samplerCube cubic_texture;
uniform sampler2D depth_texture;
uniform sampler2D screen_texture;

uniform float4 vLightDiffuse[NUM_LIGHTS];
uniform float4 vMaterialColor;
uniform float4 vMaterialColor2;
uniform float4 vSpecularColor;
uniform float4 vSunDir;
uniform float4 vSunColor;
uniform float4 vAmbientColor;
uniform float4 vGroundAmbientColor;
uniform float4 vSkyLightDir;
uniform float4 vSkyLightColor;
uniform float4 vPointLightColor;
uniform float4 vFogColor;
uniform float4 debug_vector;

#ifndef USE_CONSTANT_GAMMA
uniform float4 output_gamma;
uniform float4 output_gamma_inv;
#endif

uniform float fMaterialPower;
uniform float fFogDensity;
uniform float reflection_factor;
uniform float far_clip_Inv;
uniform float spec_coef;	//valid value after module_data!

uniform int iLightPointCount;
uniform int iLightIndices[NUM_SIMUL_LIGHTS];

uniform bool bUseMotionBlur;
uniform bool use_depth_effects;
uniform bool showing_ranged_data;

uniform float far_clip;

uniform float vTimer;
uniform float vSeason;

uniform float4 vWaveInfo;
uniform float4 vWaveOrigin;

uniform float vWindStrength;
uniform float vWindDirection;

uniform float time_var;

#ifndef USE_CONSTANT_GAMMA
const float3 input_gamma = float3(2.2, 2.2, 2.2);
#endif
const float map_normal_detail_factor = 1.4;
const float uv_2_scale = 1.237;
const float fShadowBias = 0.00002;//-0.000002;

const float2 specularShift = float2(0.138 - 0.5, 0.254 - 0.5);
const float2 specularExp = float2(256.0, 32.0) * 0.7;
const float3 specularColor0 = float3(0.9, 1.0, 1.0) * 0.898 * 0.99;
const float3 specularColor1 = float3(1.0, 0.9, 1.0) * 0.74 * 0.99;

const float3 LUMINANCE_WEIGHTS = float3(0.299, 0.587, 0.114);
const float min_exposure = 0.15;
const float max_exposure = 3.0;

const float2 TreeAmplitude = float2(0.9, 1.0);
const float2 TreePeriod = float2(0.025, 100.0);
const float tree_rate = 1.5;

#define MeshTextureSampler diffuse_texture
#define Diffuse2Sampler diffuse_texture_2
#define SpecularTextureSampler specular_texture
#define NormalTextureSampler normal_texture
#define EnvTextureSampler env_texture
#define ShadowmapTextureSampler shadowmap_texture
#define CubicTextureSampler cubic_texture
#define DepthTextureSampler depth_texture
#define ScreenTextureSampler screen_texture

#define ReflectionTextureSampler env_texture
#define FontTextureSampler diffuse_texture
#define ClampedTextureSampler diffuse_texture
#define FontTextureSampler diffuse_texture
#define CharacterShadowTextureSampler diffuse_texture
#define MeshTextureSamplerNoFilter diffuse_texture
#define DiffuseTextureSamplerNoWrap diffuse_texture
#define GrassTextureSampler diffuse_texture

#define flora_detail_fade 		(flora_detail*FLORA_DETAIL_FADE_MUL)
#define flora_detail_fade_inv 	(flora_detail-flora_detail_fade)
#define flora_detail_clip 		(max(0.0, flora_detail_fade - 20.0))

#define ERROR_OUT(c) c = float4(texCoord.x * 10 - floor(texCoord.x * 10) > 0.5, texCoord.y * 10 - floor(texCoord.y * 10) > 0.5, 0, 1)

#ifndef PS_2_X
	#define PS_2_X ps_2_b
#endif

#ifdef USE_PREDEFINED_POSTFX_PARAMS
	#define postfxTonemapOp 0
	#define postfxParams1 (float4(16.0, 1.0, 1.0, 1.0))
	#define postfxParams2 (float4( 1.0, 1.0, 1.0, 1.0))
#else
	uniform float4 postfx_editor_vector[4];
	#define postfxTonemapOp (postfx_editor_vector[0].x)
	#define postfxParams1 (postfx_editor_vector[1])
	#define postfxParams2 (postfx_editor_vector[2])
#endif

#define RELATIVE_PS_TARGET ps_2_0

#define HDRRange 				(postfxParams1.x)
#define HDRExposureScaler 		(postfxParams1.y)
#define LuminanceAverageScaler 	(postfxParams1.z)
#define LuminanceMaxScaler 		(postfxParams1.w)

#define BrightpassTreshold 	(postfxParams2.x)
#define BrightpassPostPower (postfxParams2.y)
#define BlurStrenght 		(postfxParams2.z)
#define BlurAmount 			(postfxParams2.w)

#define HDRRangeInv 		(1.0 / HDRRange)

//#define HDRRange 1.0
//#define HDRRangeInv 1.0

// STRUCTS
struct VS_OUTPUT
{
	float4 Pos;
	float  Fog;
	
	float4 Color;
	float2 Tex0;
	float4 SunLight;
	float4 ShadowTexCoord;
	#ifdef USE_ShadowTexelPos_INTERPOLATOR
		float2 ShadowTexelPos;
	#endif
};

struct VS_OUTPUT_FONT
{
	float4 Pos;
	float  Fog;
	
	float4 Color;
	float2 Tex0;
};

struct VS_OUTPUT_STANDART 
{
	float4 Pos;
	float  Fog;
	
	float4 VertexColor;
	#ifdef INCLUDE_VERTEX_LIGHTING 
		float3 VertexLighting;
	#endif
	
	float2 Tex0;
	float3 SunLightDir;
	float3 SkyLightDir;
	#ifndef USE_LIGHTING_PASS 
	float4 PointLightDir;
	#endif
	float4 ShadowTexCoord;
	#ifdef USE_ShadowTexelPos_INTERPOLATOR
		float2 ShadowTexelPos;
	#endif
	float3 ViewDir;
};

struct VS_OUTPUT_BUMP
{
	float4 Pos;
	float4 VertexColor;
	float2 Tex0;
	float3 SunLightDir;//sun light dir in pixel coordinates
	float3 SkyLightDir;//light diffuse for bump
	float4 PointLightDir;//light ambient for bump
	float4 ShadowTexCoord;
	#ifdef USE_ShadowTexelPos_INTERPOLATOR
		float2 ShadowTexelPos;
	#endif
	float Fog;
	
	float3 ViewDir;
	float3 WorldNormal;
};

struct VS_OUTPUT_FLORA
{
	float4 Pos;
	float  Fog;
	
	float4 Color;
	float2 Tex0;
	float4 SunLight;
	float4 ShadowTexCoord;
	#ifdef USE_ShadowTexelPos_INTERPOLATOR
		float2 ShadowTexelPos;
	#endif
};

struct VS_OUTPUT_FLORA_NO_SHADOW
{
	float4 Pos;
	float4 Color;
	float2 Tex0;
	float  Fog;
};

struct VS_OUTPUT_ENVMAP_SPECULAR
{
	float4 Pos;
	float  Fog;
	
	float4 Color;
	float4 Tex0;
	float4 SunLight;
	float4 ShadowTexCoord;
	#ifdef USE_ShadowTexelPos_INTERPOLATOR
		float2 ShadowTexelPos;
	#endif
	float3 vSpecular;
};

struct VS_OUTPUT_CHARACTER_SHADOW
{
	float4 Pos;
	float  Fog;
	
	float2 Tex0;
	float4 Color;
	float4 SunLight;
	float4 ShadowTexCoord;
	#ifdef USE_ShadowTexelPos_INTERPOLATOR
		float2 ShadowTexelPos;
	#endif
};

struct VS_OUTPUT_WATER
{
	float4 Pos;
	float2 Tex0;
	float4 LightDir_Alpha;//light direction for bump
	float4 LightDif;//light diffuse for bump
	float3 CameraDir;//camera direction for bump
	float4 PosWater;//position according to the water camera
	float  Fog;
	
	float4 projCoord;
	float  Depth; 
};

struct VS_OUTPUT_BUMP_DYNAMIC
{
	float4 Pos;
	float4 VertexColor;
	float2 Tex0;
	#ifndef USE_LIGHTING_PASS
		float3 vec_to_light_0;
		float3 vec_to_light_1;
		float3 vec_to_light_2;
	#endif
	float  Fog;
};

struct VS_OUTPUT_BUMP_DYNAMIC_NEW
{
	float4 Pos;
	float4 VertexColor;
	float2 Tex0	;
	#ifndef USE_LIGHTING_PASS
		float3 vec_to_light_0;
		float3 vec_to_light_1;
		float3 vec_to_light_2;
	#endif
	float3 ViewDir;
	
	float  Fog;
};

struct VS_OUTPUT_SIMPLE_HAIR
{
	float4 Pos;
	float4 Color;
	float2 Tex0;
	float4 SunLight;
	float4 ShadowTexCoord;
	#ifdef USE_ShadowTexelPos_INTERPOLATOR
		float2 ShadowTexelPos;
	#endif
	float  Fog;
};

struct VS_OUTPUT_HAIR
{
	float4 Pos;
	float2 Tex0;
	
	float4 VertexLighting;
	
	float3 viewVec;
	float3 normal;
	float3 tangent;
	float4 VertexColor;	
	
	float4 ShadowTexCoord;
	#ifdef USE_ShadowTexelPos_INTERPOLATOR
		float2 ShadowTexelPos;
	#endif
	float  Fog;
};

struct VS_OUTPUT_SIMPLE_FACE
{
	float4 Pos;
	float4 Color;
	float2 Tex0;
	float4 SunLight;
	float4 ShadowTexCoord;
	#ifdef USE_ShadowTexelPos_INTERPOLATOR
		float2 ShadowTexelPos;
	#endif
	float  Fog;
};

struct VS_OUTPUT_FACE
{
	float4 Pos;
	float  Fog;

	float4 VertexColor;
	float2 Tex0;

	float3 WorldPos;
	float3 ViewVec;
	
	float3 SunLightDir;
	float4 PointLightDir;
	
	float4 ShadowTexCoord;
	#ifdef USE_ShadowTexelPos_INTERPOLATOR
		float2 ShadowTexelPos;
	#endif
#ifdef  INCLUDE_VERTEX_LIGHTING
	float3 VertexLighting;
#endif
};

struct VS_DEPTHED_FLARE
{
	float4 Pos;
	float4 Color;
	float2 Tex0;
	float  Fog;
	
	float4 projCoord;
	float  Depth;
};

struct VS_OUTPUT_OCEAN
{
	float4 Pos;
	float2 Tex0;
	float3 LightDir;
	float4 LightDif;//light diffuse for bump
	float3 CameraDir;
	float4 PosWater;//position according to the water camera	
	float  Fog;
};

struct VS_OUTPUT_MAP
{
	float4 Pos;
	float4 Color;
	float2 Tex0;
	float4 SunLight;
	float4 ShadowTexCoord;
	#ifdef USE_ShadowTexelPos_INTERPOLATOR
		float2 ShadowTexelPos;
	#endif
	float  Fog;
	
	float3 ViewDir;
	float3 WorldNormal;
};

struct VS_OUTPUT_MAP_BUMP
{
	float4 Pos;
	float4 Color;
	float2 Tex0;
	float4 ShadowTexCoord;
	#ifdef USE_ShadowTexelPos_INTERPOLATOR
		float2 ShadowTexelPos;
	#endif
	float  Fog;
	
	float3 SunLightDir;
	float3 SkyLightDir;
	
	float3 ViewDir;
	float3 WorldNormal;
};

struct VS_OUTPUT_MAP_MOUNTAIN
{
	float4 Pos;
	float  Fog;
	
	float4 Color;
	float3 Tex0;
	float4 SunLight;
	float4 ShadowTexCoord;
	#ifdef USE_ShadowTexelPos_INTERPOLATOR
		float2 ShadowTexelPos;
	#endif
	
	float3 ViewDir;
	float3 WorldNormal;
};

struct VS_OUTPUT_MAP_MOUNTAIN_BUMP
{
	float4 Pos;
	float4 Color;
	float3 Tex0;
	float4 ShadowTexCoord;
	#ifdef USE_ShadowTexelPos_INTERPOLATOR
		float2 ShadowTexelPos;
	#endif
	float  Fog;
	
	float3 SunLightDir;
	float3 SkyLightDir;
	
	float3 ViewDir;
	float3 WorldNormal;
};

struct VS_OUTPUT_MAP_WATER
{
	float4 Pos;
	float4 Color;
	float2 Tex0;
	float3 LightDir;//light direction for bump
	float3 CameraDir;//camera direction for bump
	float4 PosWater;//position according to the water camera
	float  Fog;
};

struct VS_OUTPUT_PARALLAX_WATER
{
	float4 Pos;
	float2 Tex0;
	
	float4 LightDir_Alpha;
	float4 LightDif;
	
	float3 ViewDir;
	float3 CameraDir;
	float4 PosWater;	
	
	float4 projCoord;
	float  Depth;
	float  Fog;
};

struct VS_OUT_EARLYZ
{
	float4 Pos;	
	float2 TC;
	float  Depth;
};

struct VsOut_Convert_FP2I 
{
	float4 Pos;
	float2 texCoord0;
	float2 texCoord1;
	float2 texCoord2;
	float2 texCoord3;
};

struct VS_OUT_POSTFX
{
	float4 Pos;
	float2 Tex;
};

struct VS_OUTPUT_MAP_FONT
{
	float4 Pos;
	float  Fog;
	
	float4 Color;
	float2 Tex0;
	float Map;
};

struct VS_OUTPUT_SKYBOX
{
	float4 Pos;
	float  Fog;
	
	float4 Color;
	float2 Tex0;
	float VertHeight;
};

struct VS_OUTPUT_ICON_SEASONAL
{
	float4 Pos;
	float  Fog;
	
	float4 Color;
	float4 Tex0;
	float4 SunLight;
	float4 ShadowTexCoord;
	float2 ShadowTexelPos;
	float4 WorldPos;
};

struct VS_OUTPUT_SEA_FOAM
{
	float4 Pos;
	float  Fog;
	
	float4 Color;
	float4 Tex0;
	float4 SunLight;
	float4 ShadowTexCoord;
	float2 ShadowTexelPos;
	float4 WorldPos;
};

struct VS_OUTPUT_PARALLAX
{
	float4 Pos;
	float4 VertexColor;
	float2 Tex0;
	float3 SunLightDir;
	float3 SkyLightDir;
	float4 PointLightDir;
	float4 ShadowTexCoord;
	#ifdef USE_ShadowTexelPos_INTERPOLATOR
		float2 ShadowTexelPos;
	#endif
	
	float3 ViewDir;
	float4 WorldNormal;
	float  Fog;
};

struct VS_OUTPUT_FLORA_SEASON
{
	float4 Pos;
	float  Fog;
	
	float4 Color;
	float2 Tex0;
	float4 SunLight;
	float4 ShadowTexCoord;
	float2 ShadowTexelPos;
};

struct VS_OUTPUT_FLORA_SEASON_NO_SHADOW
{
	float4 Pos;
	float4 Color;
	float2 Tex0;
	float  Fog;
};

struct VS_OUTPUT_FLORA_MAP
{
	float4 Pos;
	float  Fog;
	
	float4 Color;
	float4 Tex0;
	float4 SunLight;
	float4 ShadowTexCoord;
	float2 ShadowTexelPos;
	float2 WorldPos;
};

struct VS_OUTPUT_NEW_MAP
{
	float4 Pos;
	float4 Color;
	float4 Tex0;
	float3 CameraDir;
	float4 ShadowTexCoord;
	float2 ShadowTexelPos;
	float  Fog;
	
	float3 SunLightDir;
	float3 SkyLightDir;
	
	float3 ViewDir;
	float3 WorldNormal;
};

struct VS_OUTPUT_MAP_WATER_NEW
{
	float4 Pos;
	float4 Color;
	float2 Tex0;
	float3 CameraDir;
	float4 PosWater;
	float  Fog;
	
	float4 projCoord;
	float2  Depth;
	
	float4 LightDir_Alpha;
	float4 LightDif;	
};

struct VS_OUTPUT_FONT_X_BUMP
{
	float4 Pos;
	float2 Tex0;
	float3 SkyDir;
	float3 SunDir;
	float4 vColor;
	float  Fog;
};

struct PS_OUTPUT
{
	float4 RGBColor;
};

// FUNCTIONS

#ifdef USE_CONSTANT_GAMMA
#define INPUT_TEX_GAMMA(col_rgb) (col_rgb) = (col_rgb) * (col_rgb)
#define INPUT_OUTPUT_GAMMA(col_rgb) (col_rgb) = (col_rgb) * (col_rgb)
#define OUTPUT_GAMMA(col_rgb) (col_rgb) = sqrt(col_rgb)
#else
#define INPUT_TEX_GAMMA(col_rgb) (col_rgb) = pow((col_rgb), input_gamma)
#define INPUT_OUTPUT_GAMMA(col_rgb) (col_rgb) = pow((col_rgb), output_gamma.xyz)
#define OUTPUT_GAMMA(col_rgb) (col_rgb) = pow((col_rgb), output_gamma_inv.xyz)
#endif

float get_fog_amount(float d)
{
	return 1.0 / exp2(d * fFogDensity);
}

float get_fog_amount_new(float d, float wz)
{
	//you can implement world.z based algorithms here
	return get_fog_amount(d);
}

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

float HairDiffuseTerm(float3 N, float3 L)
{
    return saturate(0.75 * dot(N, L) + 0.25);
}

float face_NdotL(float3 n, float3 l) 
{
	float wNdotL = dot(n.xyz, l.xyz);
	return saturate(max(0.2 * (wNdotL + 0.9), wNdotL));
}

float GetTimer(float e)
{	
	return vTimer * (10.0 * e); 
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
	return vSeason;
}

float GetSeasonWindFactor()
{	
	if ((vSeason > 2.5)) //3= winter
	{
		return 0.25;
	}
	return 1.0;
}

float GetWindAmount(float e)
{	
	float wind = vWindStrength * e; 
	wind = max(1.5, wind);

	return wind; 
}

float GetWindAmountNew(float e, float position_z)
{	
	float wind = vWindStrength * e; 
	wind = max(1.5, wind);

	float z_factor = clamp(position_z * 0.03 - 0.01, 0.0, 0.5);
	
	return wind * z_factor; //!
}

float GetWindDirection(float e)
{	
	return vWindDirection * e; 
}

float2 rotatevector (float2 originalvector, float d)
{
	float radians = d * 0.0174532925; //convert degrees to radians
	//ROTATE
	float2 newvector;
	newvector.x = (cos(radians) * originalvector.x) - (sin(radians) * originalvector.y);
	newvector.y = (sin(radians) * originalvector.x) + (cos(radians) * originalvector.y);
	return newvector;
}
