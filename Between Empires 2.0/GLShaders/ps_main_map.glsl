
varying float4 Color;
varying float2 Tex0;
varying float4 SunLight;
varying float4 ShadowTexCoord;
#ifdef USE_ShadowTexelPos_INTERPOLATOR
	varying float2 ShadowTexelPos;
#endif
varying float Fog;
varying float3 ViewDir;
varying float3 WorldNormal;

void main()
{
	VS_OUTPUT_MAP VSOut;
	VSOut.Color = Color;
	VSOut.Tex0 = Tex0;
	VSOut.SunLight = SunLight;
	VSOut.ShadowTexCoord = ShadowTexCoord;
	#ifdef USE_ShadowTexelPos_INTERPOLATOR
		VSOut.ShadowTexelPos = ShadowTexelPos;
	#endif
	VSOut.Fog = Fog;
	VSOut.ViewDir = ViewDir;
	VSOut.WorldNormal = WorldNormal;
	
	gl_FragColor = ps_main_map(VSOut, CURRENT_PCF_MODE).RGBColor;
}
