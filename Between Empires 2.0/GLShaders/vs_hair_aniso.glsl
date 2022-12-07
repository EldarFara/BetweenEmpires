
attribute vec3 inPosition;
attribute vec3 inNormal;
attribute vec3 inTangent;
attribute vec3 inBinormal;
attribute vec4 inColor0;
attribute vec2 inTexCoord;

varying float2 Tex0;
varying float4 VertexLighting;
varying float3 viewVec;
varying float3 normal;
varying float3 tangent;
varying float4 VertexColor;	
varying float4 ShadowTexCoord;
#ifdef USE_ShadowTexelPos_INTERPOLATOR
	varying float2 ShadowTexelPos;
#endif
varying float  Fog;

void main()
{
	VS_OUTPUT_HAIR VSOut;
	VSOut = vs_hair_aniso(CURRENT_PCF_MODE, vec4(inPosition, 1.0), inNormal, inTangent, inBinormal, inTexCoord, inColor0);

	gl_Position = VSOut.Pos;
	Tex0 = VSOut.Tex0;
	VertexLighting = VSOut.VertexLighting;
	viewVec = VSOut.viewVec;
	normal = VSOut.normal;
	tangent = VSOut.tangent;
	VertexColor = VSOut.VertexColor;	
	ShadowTexCoord = VSOut.ShadowTexCoord;
	#ifdef USE_ShadowTexelPos_INTERPOLATOR
		ShadowTexelPos = VSOut.ShadowTexelPos;
	#endif
	Fog = VSOut.Fog;
}
