
attribute vec3 inPosition;
attribute vec3 inNormal;
attribute vec4 inColor0;
attribute vec2 inTexCoord;
attribute vec3 inTangent;
attribute vec3 inBinormal;
attribute vec4 inBlendWeight;
attribute vec4 inBlendIndices;

varying float4 Pos;
varying float Fog;
varying float4 VertexColor;
#ifdef INCLUDE_VERTEX_LIGHTING 
	varying float3 VertexLighting;
#endif
varying float2 Tex0;
varying float3 SunLightDir;
varying float3 SkyLightDir;
#ifndef USE_LIGHTING_PASS 
	varying float4 PointLightDir;
#endif
varying float4 ShadowTexCoord;
#ifdef USE_ShadowTexelPos_INTERPOLATOR
	varying float2 ShadowTexelPos;
#endif
varying float3 ViewDir;

void main()
{
	VS_OUTPUT_STANDART VSOut;
	VSOut = vs_main_standart(vec4(inPosition, 1.0), inTexCoord, inNormal, inColor0, inTangent, inBinormal, inBlendWeight, inBlendIndices, CURRENT_PCF_MODE, true, true, 0);
	
	gl_Position = VSOut.Pos;
	Fog = VSOut.Fog;
	VertexColor = VSOut.VertexColor;
	#ifdef INCLUDE_VERTEX_LIGHTING 
		VertexLighting = VSOut.VertexLighting;
	#endif
	Tex0 = VSOut.Tex0;
	SunLightDir = VSOut.SunLightDir;
	SkyLightDir = VSOut.SkyLightDir;
	#ifndef USE_LIGHTING_PASS 
		PointLightDir = VSOut.PointLightDir;
	#endif
	ShadowTexCoord = VSOut.ShadowTexCoord;
	#ifdef USE_ShadowTexelPos_INTERPOLATOR
		ShadowTexelPos = VSOut.ShadowTexelPos;
	#endif
	ViewDir = VSOut.ViewDir;
}
