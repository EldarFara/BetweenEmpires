
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
	VSOut.VertexColor = VertexColor; 
	VSOut.Tex0 = Tex0;
#ifndef USE_LIGHTING_PASS
	VSOut.vec_to_light_0 = vec_to_light_0;
	VSOut.vec_to_light_1 = vec_to_light_1;
	VSOut.vec_to_light_2 = vec_to_light_2;
#endif
	VSOut.Fog = Fog;

	gl_FragColor = ps_main_bump_interior(VSOut).RGBColor;
}
