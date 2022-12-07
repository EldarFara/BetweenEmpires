
attribute vec3 inPosition;
attribute vec4 inColor0;
attribute vec2 inTexCoord;

varying float4 Color;
varying float2 Tex0;
varying float  Fog;	
varying float4 projCoord;
varying float  Depth;

void main()
{
	VS_DEPTHED_FLARE VSOut;
	VSOut = vs_main_depthed_flare(vec4(inPosition, 1.0), inColor0, inTexCoord);

	gl_Position = VSOut.Pos;
	Color = VSOut.Color;
	Tex0 = VSOut.Tex0;
	Fog = VSOut.Fog;	
	projCoord = VSOut.projCoord;
	Depth = VSOut.Depth;
}
