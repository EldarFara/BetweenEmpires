
attribute vec3 inPosition;
attribute vec3 inNormal;
attribute vec4 inColor0;
attribute vec4 inColor1;
attribute vec2 inTexCoord;
attribute vec3 inTangent;
attribute vec3 inBinormal;

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
	VSOut = vs_main_water(vec4(inPosition, 1.0), inNormal, inColor0, inTexCoord, inTangent, inBinormal);

	gl_Position = VSOut.Pos;
	Tex0 = VSOut.Tex0;
	LightDir_Alpha = VSOut.LightDir_Alpha;
	LightDif = VSOut.LightDif;
	CameraDir = VSOut.CameraDir;
	PosWater = VSOut.PosWater;
	Fog = VSOut.Fog;
	projCoord = VSOut.projCoord;
	Depth = VSOut.Depth;
}
