
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
	VSOut.Tex0 = Tex0;
	VSOut.VertexLighting = VertexLighting;
	VSOut.viewVec = viewVec;
	VSOut.normal = normal;
	VSOut.tangent = tangent;
	VSOut.VertexColor = VertexColor;	
	VSOut.ShadowTexCoord = ShadowTexCoord;
	#ifdef USE_ShadowTexelPos_INTERPOLATOR
		VSOut.ShadowTexelPos = ShadowTexelPos;
	#endif
	VSOut.Fog = Fog;

	gl_FragColor = ps_hair_aniso(VSOut, CURRENT_PCF_MODE, false).RGBColor;
}
