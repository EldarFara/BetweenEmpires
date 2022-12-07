
attribute vec3 inPosition;
attribute vec3 inNormal;
attribute vec4 inColor0;
attribute vec4 inColor1;
attribute vec2 inTexCoord;

varying float4 Pos;
varying float Fog;
varying float4 Color;
varying float2 Tex0;
varying float4 SunLight;
varying float4 ShadowTexCoord;
#ifdef USE_ShadowTexelPos_INTERPOLATOR
	varying float2 ShadowTexelPos;
#endif

void main()
{
	VS_OUTPUT VSOut;
	VSOut = vs_main(CURRENT_PCF_MODE, false, vec4(inPosition, 1.0), inNormal, inTexCoord, inColor0, inColor1);

	gl_Position = VSOut.Pos;
	Fog = VSOut.Fog;
	Color = VSOut.Color;
	Tex0 = VSOut.Tex0;
	SunLight = VSOut.SunLight;
	ShadowTexCoord = VSOut.ShadowTexCoord;
	#ifdef USE_ShadowTexelPos_INTERPOLATOR
		ShadowTexelPos = VSOut.ShadowTexelPos;
	#endif
}
