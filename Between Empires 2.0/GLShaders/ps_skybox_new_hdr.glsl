
varying float4 Pos;
varying float Fog;
varying float4 Color;
varying float2 Tex0;

void main()
{
	VS_OUTPUT_FONT VSOut;
	VSOut.Fog = Fog;
	VSOut.Color = Color;
	VSOut.Tex0 = Tex0;
	
	gl_FragColor = ps_skybox_shading_new(true, VSOut).RGBColor;
}
