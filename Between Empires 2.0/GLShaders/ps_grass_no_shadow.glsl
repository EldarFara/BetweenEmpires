
varying float4 Color;
varying float2 Tex0;
varying float  Fog;

void main()
{
	VS_OUTPUT_FLORA_NO_SHADOW VSOut;
	VSOut.Fog = Fog;
	VSOut.Color = Color;
	VSOut.Tex0 = Tex0;

	gl_FragColor = ps_grass_no_shadow(VSOut).RGBColor;
}
