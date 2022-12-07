
attribute vec3 inPosition;
attribute vec4 inColor0;
attribute vec2 inTexCoord;

varying float4 Color;
varying float2 Tex0;
varying float  Fog;

void main()
{
	VS_OUTPUT_FLORA_NO_SHADOW VSOut;
	VSOut = vs_flora_no_shadow(vec4(inPosition, 1.0), inColor0, inTexCoord);
	
	gl_Position = VSOut.Pos;
	Fog = VSOut.Fog;
	Color = VSOut.Color;
	Tex0 = VSOut.Tex0;
}
