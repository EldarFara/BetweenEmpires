
attribute vec3 inPosition;
attribute vec3 inNormal;
attribute vec4 inColor0;
attribute vec2 inTexCoord;
attribute vec3 inTangent;
attribute vec3 inBinormal;

varying float4 VertexColor;
varying float2 Tex0;
#ifndef USE_LIGHTING_PASS
	varying float3 vec_to_light_0;
	varying float3 vec_to_light_1;
	varying float3 vec_to_light_2;
#endif
varying float Fog;

void main()
{
	VS_OUTPUT_BUMP_DYNAMIC VSOut;
	VSOut = vs_main_bump_interior(vec4(inPosition, 1.0), inNormal, inTexCoord, inTangent, inBinormal, inColor0);

	gl_Position = VSOut.Pos;
	VertexColor = VSOut.VertexColor;
	Tex0 = VSOut.Tex0;
#ifndef USE_LIGHTING_PASS
	vec_to_light_0 = VSOut.vec_to_light_0;
	vec_to_light_1 = VSOut.vec_to_light_1;
	vec_to_light_2 = VSOut.vec_to_light_2;
#endif
	Fog = VSOut.Fog;
}
