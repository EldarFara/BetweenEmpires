
varying float4 Pos;
varying float2 Tex0;
varying float4 LightDir_Alpha;
varying float4 LightDif;
varying float3 CameraDir;
varying float4 PosWater;
varying float Fog;
varying float4 projCoord;
varying float  Depth; 

void main()
{ 
	VS_OUTPUT_WATER VSOut;
	
	VSOut.Tex0 = Tex0;
	VSOut.LightDir_Alpha = LightDir_Alpha;
	VSOut.LightDif = LightDif;
	VSOut.CameraDir = CameraDir;
	VSOut.PosWater = PosWater;
	VSOut.Fog = Fog;
	VSOut.projCoord = projCoord;
	VSOut.Depth = Depth;
	gl_FragColor = ps_main_water(VSOut, true, true, true).RGBColor;
}
