
attribute vec3 inPosition;
attribute vec3 inNormal;
attribute vec4 inColor0;
attribute vec4 inColor1;
attribute vec2 inTexCoord;
attribute vec3 inTangent;
attribute vec3 inBinormal;
attribute vec4 inBlendWeight;
attribute vec4 inBlendIndices;

varying float  Fog;
varying float2 Tex0;
varying float4 Color;
varying float4 SunLight;
varying float4 ShadowTexCoord;
#ifdef USE_ShadowTexelPos_INTERPOLATOR
	varying float2 ShadowTexelPos;
#endif

void main()
{
	VS_OUTPUT_CHARACTER_SHADOW VSOut;
	VSOut = vs_character_shadow(CURRENT_PCF_MODE, vec4(inPosition, 1.0), inNormal, inTexCoord, inColor0);
	
	gl_Position = VSOut.Pos;
	Fog = VSOut.Fog;
	Tex0 = VSOut.Tex0;
	Color = VSOut.Color;
	SunLight = VSOut.SunLight;
	ShadowTexCoord = VSOut.ShadowTexCoord;
	#ifdef USE_ShadowTexelPos_INTERPOLATOR
		ShadowTexelPos = VSOut.ShadowTexelPos;
	#endif
}
