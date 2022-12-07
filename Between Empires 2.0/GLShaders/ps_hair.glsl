
varying float4 Color;
varying float2 Tex0;
varying float4 SunLight;
varying float4 ShadowTexCoord;
#ifdef USE_ShadowTexelPos_INTERPOLATOR
	varying float2 ShadowTexelPos;
#endif
varying float Fog;

void main()
{ 
	VS_OUTPUT_SIMPLE_HAIR VSOut;
	VSOut.Color = Color;
	VSOut.Tex0 = Tex0;
	VSOut.SunLight = SunLight;
	VSOut.ShadowTexCoord = ShadowTexCoord;
	#ifdef USE_ShadowTexelPos_INTERPOLATOR
		VSOut.ShadowTexelPos = ShadowTexelPos;
	#endif
	VSOut.Fog = Fog;

	gl_FragColor = ps_hair(VSOut, CURRENT_PCF_MODE).RGBColor;
}
