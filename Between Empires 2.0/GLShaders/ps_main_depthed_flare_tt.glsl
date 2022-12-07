
varying float4 Color;
varying float2 Tex0;
varying float Fog;	
varying float4 projCoord;
varying float Depth;

void main()
{
	VS_DEPTHED_FLARE VSOut;
	VSOut.Color = Color;
	VSOut.Tex0 = Tex0;
	VSOut.Fog = Fog;	
	VSOut.projCoord = projCoord;
	VSOut.Depth = Depth;

	gl_FragColor = ps_main_depthed_flare(VSOut, true, true).RGBColor;
}
