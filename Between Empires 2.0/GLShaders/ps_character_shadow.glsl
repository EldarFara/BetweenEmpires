
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
	VSOut.Fog = Fog;
	VSOut.Tex0 = Tex0;
	VSOut.Color = Color;
	VSOut.SunLight = SunLight;
	VSOut.ShadowTexCoord = ShadowTexCoord;
	#ifdef USE_ShadowTexelPos_INTERPOLATOR
		VSOut.ShadowTexelPos = ShadowTexelPos;
	#endif

	gl_FragColor = ps_character_shadow(CURRENT_PCF_MODE, VSOut).RGBColor;
}