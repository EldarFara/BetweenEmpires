
varying float4 VertexColor;
varying float2 Tex0;
varying float3 SunLightDir;
varying float3 SkyLightDir;
varying float4 PointLightDir;
varying float4 ShadowTexCoord;
#ifdef USE_ShadowTexelPos_INTERPOLATOR
	varying float2 ShadowTexelPos;
#endif
varying float Fog;
varying float3 ViewDir;
varying float3 WorldNormal;

void main()
{
	VS_OUTPUT_BUMP VSOut;
	VSOut.VertexColor = VertexColor;
	VSOut.Tex0 = Tex0;
	VSOut.SunLightDir = SunLightDir;
	VSOut.SkyLightDir = SkyLightDir;
	VSOut.PointLightDir = PointLightDir;
	VSOut.ShadowTexCoord = ShadowTexCoord;
	#ifdef USE_ShadowTexelPos_INTERPOLATOR
		VSOut.ShadowTexelPos = ShadowTexelPos;
	#endif
	VSOut.Fog = Fog;
	VSOut.ViewDir = ViewDir;
	VSOut.WorldNormal = WorldNormal;

	gl_FragColor = ps_main_bump_simple_multitex(VSOut, CURRENT_PCF_MODE, false).RGBColor;
}
