
attribute vec3 inPosition;
attribute vec3 inNormal;
attribute vec3 inTangent;
attribute vec3 inBinormal;
attribute vec4 inColor0;
attribute vec4 inColor1;
attribute vec2 inTexCoord;

varying float2 Tex0;
varying float3 SkyDir;
varying float3 SunDir;
varying float4 vColor;
varying float Fog;

void main()
{
	VS_OUTPUT_FONT_X_BUMP VSOut;
	VSOut = vs_main_no_shadow_bump(vec4(inPosition, 1.0), inNormal, inTexCoord, inColor0, inTangent, inBinormal);

	gl_Position = VSOut.Pos;
	Tex0 = VSOut.Tex0;
	SkyDir = VSOut.SkyDir;
	SunDir = VSOut.SunDir;
	vColor = VSOut.vColor;
	Fog = VSOut.Fog;
}