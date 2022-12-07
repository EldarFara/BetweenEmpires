
attribute vec3 inPosition;
attribute vec3 inNormal;
attribute vec4 inColor0;
attribute vec4 inColor1;
attribute vec2 inTexCoord;

varying float4 Color;
varying float2 Tex0;
varying float3 LightDir;
varying float3 CameraDir;
varying float4 PosWater;
varying float Fog;

void main()
{
	VS_OUTPUT_MAP_WATER VSOut;
	VSOut = vs_map_water(false, vec4(inPosition, 1.0), inNormal, inTexCoord, inColor0, inColor1);

	gl_Position = VSOut.Pos;
	Color = VSOut.Color;
	Tex0 = VSOut.Tex0;
	LightDir = VSOut.LightDir;
	CameraDir = VSOut.CameraDir;
	PosWater = VSOut.PosWater;
	Fog = VSOut.Fog;
}
