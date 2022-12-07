
varying float4 Color;
varying float2 Tex0;
varying float3 LightDir;
varying float3 CameraDir;
varying float4 PosWater;
varying float Fog;

void main()
{
	VS_OUTPUT_MAP_WATER VSOut;
	VSOut.Color = Color;
	VSOut.Tex0 = Tex0;
	VSOut.LightDir = LightDir;
	VSOut.CameraDir = CameraDir;
	VSOut.PosWater = PosWater;
	VSOut.Fog = Fog;

	gl_FragColor = ps_map_water(true, VSOut).RGBColor;
}
