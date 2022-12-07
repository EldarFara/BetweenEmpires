
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
	VSOut.Fog = Fog;
	VSOut.VertexColor = VertexColor;
#ifdef INCLUDE_VERTEX_LIGHTING 
	VSOut.VertexLighting = VertexLighting;
#endif
	VSOut.Tex0 = Tex0;
	VSOut.SunLightDir = SunLightDir;
	VSOut.SkyLightDir = SkyLightDir;
#ifndef USE_LIGHTING_PASS 
	VSOut.PointLightDir = PointLightDir;
#endif
	VSOut.ShadowTexCoord = ShadowTexCoord;
	#ifdef USE_ShadowTexelPos_INTERPOLATOR
		VSOut.ShadowTexelPos = ShadowTexelPos;
	#endif
	VSOut.ViewDir = ViewDir;
	
	gl_FragColor = ps_main_standart(VSOut, CURRENT_PCF_MODE,  true, false, false, false, false, false, false, false, false).RGBColor;
}
